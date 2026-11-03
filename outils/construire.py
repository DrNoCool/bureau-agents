"""Convertit les images du bureau en assets.json, le seul fichier que le mod lit.

Usage : python outils/construire.py   (la commande /bureau le lance aussi)

Une image plus grande que sa taille cible (une planche de ChatGPT, par
exemple) est ramenée à cette taille : chaque bloc de pixels devient sa
couleur la plus fréquente. Le magenta (#FF00FF) et la transparence
deviennent du vide.

Lit aussi themes/<nom>/ (mêmes dossiers, seulement ce que le thème change).

Produit aussi des aperçus agrandis : apercu.png à la racine et dans chaque
thème, et apercu.png dans chaque dossier de personnage.
"""
import json
import sys
import time
from collections import Counter
from pathlib import Path

from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")

RACINE = Path(__file__).resolve().parent.parent
PLAN = json.loads((RACINE / "bureau.json").read_text(encoding="utf-8"))
T = PLAN["tuile"]
ORDRE = [["bas0", "haut0", "gauche0"], ["bas1", "haut1", "gauche1"]]
MAX_COULEURS = 16
# Les places du mur (« cadre-droit », « coin-gauche »…) : sans dessin propre,
# une place prend le dessin commun (« cadre », « coin »), et sa taille.
COTES = ("-gauche", "-droite", "-droit")


def commun(nom: str) -> str:
    return next((nom[: -len(c)] for c in COTES if nom.endswith(c)), nom)


def vide(px: tuple) -> bool:
    r, g, b, a = px
    return a < 128 or (r > 200 and g < 90 and b > 200)


def reduire(img: Image.Image, largeur: int, hauteur: int) -> Image.Image:
    img = img.convert("RGBA")
    if img.size == (largeur, hauteur):
        return img
    # Moins de couleurs d'abord : le flou d'une image générée en invente des centaines.
    masque = img.getchannel("A")
    rgb = img.convert("RGB").quantize(colors=MAX_COULEURS, method=Image.Quantize.MEDIANCUT).convert("RGB")
    img = rgb.convert("RGBA")
    img.putalpha(masque)
    sortie = Image.new("RGBA", (largeur, hauteur), (0, 0, 0, 0))
    px = img.load()
    for y in range(hauteur):
        for x in range(largeur):
            x0, x1 = x * img.width // largeur, max((x + 1) * img.width // largeur, x * img.width // largeur + 1)
            y0, y1 = y * img.height // hauteur, max((y + 1) * img.height // hauteur, y * img.height // hauteur + 1)
            votes = Counter(
                None if vide(px[i, j]) else px[i, j][:3] for j in range(y0, y1) for i in range(x0, x1)
            )
            gagnant = votes.most_common(1)[0][0]
            if gagnant is not None:
                sortie.putpixel((x, y), (*gagnant, 255))
    return sortie


def couches(img: Image.Image) -> list[dict]:
    """Une forme SVG par couleur : chaque suite de pixels devient « M x y h n v1 h-n z »."""
    traces: dict[str, list[str]] = {}
    px = img.load()
    for y in range(img.height):
        x = 0
        while x < img.width:
            p = px[x, y]
            fin = x
            while fin < img.width and px[fin, y] == p:
                fin += 1
            if not vide(p):
                couleur = "#%02x%02x%02x" % p[:3]
                traces.setdefault(couleur, []).append(f"M{x} {y}h{fin - x}v1h-{fin - x}z")
            x = fin
    return [{"fill": c, "d": "".join(d)} for c, d in traces.items()]


def forme(img: Image.Image) -> dict:
    return {"w": img.width, "h": img.height, "couches": couches(img)}


def agrandir(img: Image.Image, facteur: int) -> Image.Image:
    return img.resize((img.width * facteur, img.height * facteur), Image.Resampling.NEAREST)


# Personnages : une planche de 3 × 2 poses par dossier.
def lire_personnages(racine: Path, assets: dict, images: dict) -> None:
    w, h = PLAN["tailles"]["personnage"]
    for dossier in sorted((racine / "personnages").glob("*/")):
        planche_png = dossier / "planche.png"
        if not planche_png.exists():
            print(f"ignoré    {dossier.name} : pas de planche.png")
            continue
        planche = Image.open(planche_png).convert("RGBA")
        cw, ch = planche.width / 3, planche.height / 2
        poses = {}
        for r, rangee in enumerate(ORDRE):
            for c, pose in enumerate(rangee):
                case = planche.crop((round(c * cw), round(r * ch), round((c + 1) * cw), round((r + 1) * ch)))
                poses[pose] = reduire(case, w, h)
        images["personnages"][dossier.name] = poses
        assets["personnages"][dossier.name] = {pose: forme(img) for pose, img in poses.items()}
        apercu = Image.new("RGBA", (w * 3, h * 2), (255, 255, 255, 255))
        for r, rangee in enumerate(ORDRE):
            for c, pose in enumerate(rangee):
                apercu.alpha_composite(poses[pose], (c * w, r * h))
        agrandir(apercu, 8).save(dossier / "apercu.png")
        print(f"converti  {dossier.relative_to(RACINE).as_posix()} ({planche.width}×{planche.height})")


# Décor : un dossier par objet ; chaque PNG est un état (« inactif »),
# ou une image d'animation (« actif-1 », « actif-2 »…). Un thème peut donner
# sa propre taille à un objet (« tailles » du thème) : son dessin remplaçant
# n'a pas toujours celle de tous les jours (la plante devient sapin à Noël).
def lire_decor(racine: Path, assets: dict, images: dict, tailles: dict | None = None) -> None:
    for dossier in sorted((racine / "decor").glob("*/")):
        taille = next((t.get(n) for n in (dossier.name, commun(dossier.name))
                       for t in (tailles or {}, PLAN["tailles"]) if t.get(n)), None)
        etats: dict[str, list] = {}
        for png in sorted(dossier.glob("*.png")):
            etat, _, numero = png.stem.rpartition("-")
            if not (etat and numero.isdigit()):
                etat = png.stem
            img = Image.open(png).convert("RGBA")
            etats.setdefault(etat, []).append(reduire(img, *taille) if taille else img)
        if not etats:
            continue
        images["decor"][dossier.name] = etats
        assets["decor"][dossier.name] = {e: [forme(i) for i in imgs] for e, imgs in etats.items()}
        print(f"converti  {dossier.relative_to(RACINE).as_posix()} : "
              f"{', '.join(f'{e} ({len(i)})' for e, i in etats.items())}")


assets: dict = {"personnages": {}, "decor": {}, "themes": {}}
images: dict = {"personnages": {}, "decor": {}}
lire_personnages(RACINE, assets, images)
lire_decor(RACINE, assets, images)

# Les thèmes : themes/<nom>/ a les mêmes dossiers, avec seulement ce qui change.
# Un dessin du thème remplace celui de tous les jours qui porte le même nom.
images_themes: dict = {}
for dossier in sorted((RACINE / "themes").glob("*/")):
    assets["themes"][dossier.name] = {"personnages": {}, "decor": {}}
    images_themes[dossier.name] = {"personnages": {}, "decor": {}}
    lire_personnages(dossier, assets["themes"][dossier.name], images_themes[dossier.name])
    lire_decor(dossier, assets["themes"][dossier.name], images_themes[dossier.name],
               PLAN.get("themes", {}).get(dossier.name, {}).get("tailles"))

(RACINE / "assets.json").write_text(json.dumps(assets, separators=(",", ":")), encoding="utf-8")

# La page plein écran ne peut pas lire un .json depuis le disque (le navigateur
# l'interdit pour une page locale), mais elle peut charger un script.
(RACINE / "vue").mkdir(exist_ok=True)
(RACINE / "vue" / "donnees.js").write_text(
    f"window.BUREAU_PLAN = {json.dumps(PLAN, ensure_ascii=False)};\n"
    f"window.BUREAU_ASSETS = {json.dumps(assets, separators=(',', ':'))};\n",
    encoding="utf-8",
)

# Chaque session laisse son fichier dans vue/sessions/ : ceux de plus d'une
# journée ne servent plus à rien.
for vieux in (RACINE / "vue" / "sessions").glob("*.js"):
    if time.time() - vieux.stat().st_mtime > 86400:
        vieux.unlink()


# Aperçu du bureau entier : chaque personnage assis à un poste.
def apercu(images: dict, objets: list[dict], chemin: Path) -> None:
    def premier(objet: str, etat: str | None = None) -> Image.Image | None:
        etats = images["decor"].get(objet) or images["decor"].get(commun(objet), {})
        imgs = etats.get(etat) if etat else None
        imgs = imgs or next(iter(etats.values()), None)
        return imgs[0] if imgs else None

    def poser(img: Image.Image | None, x: int, y: int) -> None:
        if img is not None:
            fond.alpha_composite(img, (x, y))

    L, H = PLAN["colonnes"] * T, PLAN["rangees"] * T
    fond = Image.new("RGBA", (L, H), (0, 0, 0, 255))
    for ty in range(PLAN["rangees"]):
        for tx in range(PLAN["colonnes"]):
            poser(premier("sol"), tx * T, ty * T)
    for tx in range(PLAN["colonnes"]):
        poser(premier("mur"), tx * T, 0)
        if not PLAN["porte"]["x"] <= tx < PLAN["porte"]["x"] + 2:
            poser(premier("mur-bas"), tx * T, (PLAN["rangees"] - 1) * T)
    porte = premier("porte")
    if porte:
        poser(porte, PLAN["porte"]["x"] * T, (PLAN["porte"]["y"] + 1) * T - porte.height)
    for objet in [*objets, {"asset": "pancarte", **PLAN.get("pancarte", {})}]:
        img = premier(objet["asset"], objet.get("etat"))
        if img and "x" in objet:
            poser(img, round(objet["x"] * T), round((objet["y"] + 1) * T) - img.height)

    # Chacun est assis derrière son bureau, face à nous : le personnage d'abord,
    # le bureau par-dessus, qui cache tout sous les épaules.
    def attabler(meuble: str, etat: str, place: dict, nom: str | None) -> None:
        table = premier(meuble, etat)
        if not table:
            return
        x = round(place["x"] * T)
        bas = (place["y"] + 1) * T
        if nom in images["personnages"]:
            poser(images["personnages"][nom]["bas0"], x + table.width // 2 - 8, bas - table.height - 10)
        poser(table, x, bas - table.height)

    gestionnaire = PLAN["personnages"].get("claude", "gestionnaire")
    attabler("bureau-gestionnaire", "actif", PLAN["gestionnaire"], gestionnaire)
    employes = [n for n in images["personnages"] if n != gestionnaire]
    etats_poste = [e for e in ("redaction", "audit", "travail") if e in images["decor"].get("poste", {})]
    for i, place in enumerate(PLAN["postes"]):
        nom = employes[i % len(employes)] if employes and i < 4 else None
        etat = etats_poste[i % len(etats_poste)] if nom and etats_poste else "inactif"
        attabler("poste", etat, place, nom)

    agrandir(fond, 4).save(chemin)
    print(f"aperçu    {chemin.relative_to(RACINE).as_posix()}")


apercu(images, PLAN["objets"], RACINE / "apercu.png")
# Un aperçu par thème, dans son dossier : les dessins de tous les jours, sauf ce que le thème remplace.
for nom, propres in images_themes.items():
    melange = {k: {**images[k], **propres[k]} for k in images}
    # Le dessin commun du thème l'emporte sur une place dessinée pour tous les jours.
    for place in images["decor"]:
        if commun(place) in propres["decor"] and place not in propres["decor"]:
            melange["decor"].pop(place)
    objets = [*PLAN["objets"], *PLAN.get("themes", {}).get(nom, {}).get("objets", [])]
    apercu(melange, objets, RACINE / "themes" / nom / "apercu.png")
