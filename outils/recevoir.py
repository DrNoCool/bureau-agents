"""Reçoit les dessins et le plan du bureau perso : personnages/, decor/, themes/ et bureau.json.

Usage : python outils/recevoir.py <source>

<source> : un dépôt GitHub public (https://github.com/<compte>/<dépôt>),
l'adresse https d'un .zip, un .zip local ou un dossier local.

Le perso est la source (décision 0001) : personnages/, decor/ et themes/ sont
remplacés au complet, sans sauvegarde, et bureau.json aussi. Seuls des PNG et
bureau.json sont pris, jamais de code. Si une vérification échoue, rien ne
change. Ensuite : /bureau, pour reconstruire et voir le résultat.
"""
import io
import json
import os
import re
import shutil
import stat
import sys
import time
import urllib.request
import zipfile
from pathlib import Path, PurePosixPath

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

RACINE = Path(__file__).resolve().parent.parent
DOSSIERS = ("personnages", "decor", "themes")
SIGNATURE_PNG = b"\x89PNG\r\n\x1a\n"
IMAGE_MAX = 2 * 1024 * 1024          # un dessin du bureau pèse quelques Ko
ARCHIVE_MAX = 200 * 1024 * 1024


def lire_source(source: str) -> dict[str, bytes]:
    """Tous les fichiers de la source, chemin (avec /) → contenu."""
    chemin = Path(source)
    if chemin.is_dir():
        return {f.relative_to(chemin).as_posix(): f.read_bytes() for f in chemin.rglob("*") if f.is_file()}
    if chemin.is_file():
        donnees = chemin.read_bytes()
    elif source.startswith("https://"):
        m = re.fullmatch(r"https://github\.com/([\w.-]+)/([\w.-]+?)(?:\.git)?/?", source)
        url = f"https://github.com/{m[1]}/{m[2]}/archive/HEAD.zip" if m else source
        print(f"téléchargement  {url}")
        with urllib.request.urlopen(url, timeout=60) as r:
            donnees = r.read(ARCHIVE_MAX + 1)
        if len(donnees) > ARCHIVE_MAX:
            sys.exit("Archive trop grosse : rien n'a changé.")
    else:
        sys.exit(f"Source introuvable : {source} (un dossier, un .zip, ou une adresse https).")
    with zipfile.ZipFile(io.BytesIO(donnees)) as z:
        return {i.filename: z.read(i) for i in z.infolist() if not i.is_dir()}


def trier(fichiers: dict[str, bytes]) -> tuple[dict[str, bytes], bytes, int]:
    """Les PNG des trois dossiers et bureau.json, relatifs au dossier du bureau dans la source."""
    # Le bureau, dans la source, est le dossier le moins profond qui a bureau.json et personnages/.
    prefixes = sorted((c[: -len("bureau.json")] for c in fichiers if c == "bureau.json" or c.endswith("/bureau.json")),
                      key=len)
    prefixe = next((p for p in prefixes if any(c.startswith(p + "personnages/") for c in fichiers)), None)
    if prefixe is None:
        sys.exit("Aucun bureau dans la source (bureau.json à côté de personnages/) : rien n'a changé.")
    images, ignores = {}, 0
    for chemin, contenu in fichiers.items():
        if not chemin.startswith(prefixe):
            continue
        rel = PurePosixPath(chemin[len(prefixe):])
        if rel.parts[0] not in DOSSIERS or rel.suffix.lower() != ".png":
            ignores += rel.as_posix() != "bureau.json"
            continue
        if ".." in rel.parts or rel.is_absolute():
            sys.exit(f"Chemin refusé : {chemin}. Rien n'a changé.")
        if len(contenu) > IMAGE_MAX or not contenu.startswith(SIGNATURE_PNG):
            sys.exit(f"Pas un dessin du bureau : {chemin}. Rien n'a changé.")
        images[rel.as_posix()] = contenu
    plan = fichiers[prefixe + "bureau.json"]
    if not isinstance(json.loads(plan.decode("utf-8")), dict):
        sys.exit("bureau.json n'est pas un plan : rien n'a changé.")
    for dossier in ("personnages", "decor"):
        if not any(c.startswith(dossier + "/") for c in images):
            sys.exit(f"La source n'a aucun dessin dans {dossier}/ : rien n'a changé.")
    return images, plan, ignores


def actuels() -> dict[str, bytes]:
    return {f.relative_to(RACINE).as_posix(): f.read_bytes()
            for d in DOSSIERS if (RACINE / d).is_dir() for f in (RACINE / d).rglob("*.png")}


def effacer(dossier: Path) -> None:
    """Efface un dossier, même les fichiers en lecture seule (desktop.ini) ; un reste ne bloque rien."""
    def forcer(fonction, chemin, _):
        os.chmod(chemin, stat.S_IWRITE)
        fonction(chemin)
    if dossier.exists():
        shutil.rmtree(dossier, onerror=forcer)


def deplacer(source: Path, cible: Path) -> None:
    # Windows refuse parfois un instant : un antivirus ou l'indexation tient encore le dossier.
    for essai in range(10):
        try:
            source.rename(cible)
            return
        except PermissionError:
            if essai == 9:
                raise
            time.sleep(0.3)


def installer(images: dict[str, bytes], plan: bytes) -> None:
    """Écrit à côté, puis échange les dossiers par renommage : un échec remet le bureau comme avant."""
    attente, ancien = RACINE / ".reception", RACINE / ".ancien"
    effacer(attente)
    effacer(ancien)
    for rel, contenu in images.items():
        (attente / rel).parent.mkdir(parents=True, exist_ok=True)
        (attente / rel).write_bytes(contenu)
    for d in DOSSIERS:
        (attente / d).mkdir(parents=True, exist_ok=True)
    ancien.mkdir()
    echanges = []
    try:
        for d in DOSSIERS:
            if (RACINE / d).exists():
                deplacer(RACINE / d, ancien / d)
            echanges.append(d)
            deplacer(attente / d, RACINE / d)
    except OSError as err:
        for d in reversed(echanges):
            if (ancien / d).exists():
                if (RACINE / d).exists():
                    deplacer(RACINE / d, attente / d)
                deplacer(ancien / d, RACINE / d)
        sys.exit(f"Échange impossible ({err}) : le bureau est remis comme avant.")
    (RACINE / "bureau.json").write_bytes(plan)
    effacer(attente)
    effacer(ancien)


if len(sys.argv) != 2:
    sys.exit(__doc__)
images, plan, ignores = trier(lire_source(sys.argv[1]))
avant = actuels()
nouveaux = sum(rel not in avant for rel in images)
changes = sum(rel in avant and avant[rel] != c for rel, c in images.items())
retires = sum(rel not in images for rel in avant)
plan_change = (RACINE / "bureau.json").read_bytes() != plan if (RACINE / "bureau.json").exists() else True
installer(images, plan)

print(f"{len(images)} dessins reçus : {nouveaux} nouveaux, {changes} changés, {retires} retirés.")
print(f"bureau.json : {'changé' if plan_change else 'identique'}.")
if ignores:
    print(f"{ignores} autres fichiers de la source ignorés (code, documentation) : seuls les dessins et le plan sont pris.")
print("Lance /bureau pour reconstruire et voir le résultat.")
