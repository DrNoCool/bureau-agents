"""Les dessins retirés du bureau, gardés pour pouvoir les ressortir.

Usage : python archives/dessins_archives.py

Chaque élément archivé écrit dans archives/<élément>/<version>/, hors de
decor/ : la page ne le charge pas. Pour en ressortir un, recopier son dossier
dans decor/<élément>/, remettre sa taille dans « tailles » et son emplacement
dans « objets » de bureau.json (le commentaire au-dessus de chacun les donne),
puis lancer construire.py.

Rien n'entre ici sans la confirmation de l'analyste.
"""
from pathlib import Path

from PIL import Image

ARCHIVES = Path(__file__).resolve().parent


# Le même que dans outils/dessins_initiaux.py : une grille de caractères et une
# palette.
def ecrire(chemin: Path, grille: list[str], palette: dict[str, str]) -> None:
    largeur = len(grille[0])
    for i, rangee in enumerate(grille):
        assert len(rangee) == largeur, f"{chemin} : rangée {i} de {len(rangee)} pixels au lieu de {largeur}"
    img = Image.new("RGBA", (largeur, len(grille)), (0, 0, 0, 0))
    for y, rangee in enumerate(grille):
        for x, c in enumerate(rangee):
            if c != ".":
                h = palette[c].lstrip("#")
                img.putpixel((x, y), (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), 255))
    chemin.parent.mkdir(parents=True, exist_ok=True)
    img.save(chemin)
    print(f"dessiné   {chemin.relative_to(ARCHIVES)}")


# ------------------------------------------------------------- plante / verte
# Archivée le 2026-10-22, remplacée par la plante carnivore ; ressortie le
# 2026-10-23 (recopiée dans decor/plante/), une seule, à la place de la
# carnivore : { "asset": "plante", "x": 1, "y": 2, ... }. La carnivore et le
# sapin sont devenus ses dessins d'Halloween et de Noël.
# Taille : 16 × 16 (« tailles » : "plante": [16, 16]).

ecrire(ARCHIVES / "plante" / "verte" / "image.png", [
    "......V..v......",
    "....vvV.vvV.....",
    "...vvvVvvvvV....",
    "..vvVvvvVvvvV...",
    "..vVvvVvvvVvv...",
    "...vvvvVvvvVv...",
    "..VvvVvvvVvvv...",
    "...vvvvvVvvV....",
    ".....vvVvv......",
    "....qqqqqqqq....",
    "....rrrrrrrr....",
    ".....rrrrrr.....",
    ".....rrrrrr.....",
    ".....qrrrrq.....",
    "......qqqq......",
    "................",
], {"v": "#5a9e4b", "V": "#3d7a35", "r": "#b5523b", "q": "#8e3b2a"})


# --------------------------------------------------------- plante / carnivore-profil
# Essayée le 2026-10-22, gardée aux archives ; la version de face a été retenue.
# Ses images sont aussi recopiées dans decor/carnivore/ et
# themes/halloween/decor/plante/, préfixées « pose2- » : c'est la pose2 de la
# plante de face, sa tête tournée (toutes les 15 à 60 minutes).
# Taille : 24 × 24 (« tailles » : "carnivore": [24, 24]).
# Pour la ressortir seule, à la place de la plante, avec son rythme et sa gueule :
#   { "asset": "carnivore", "x": 1, "y": 2, "rythme": 0.6, "gueule": true }
# Fichier « <état>-<n>.png » : l'état de la gueule (fermee, entrouverte,
# ouverte), puis l'image de la respiration (la tête suit la tige une image plus tard).


def toile(largeur: int, hauteur: int) -> list[list[str]]:
    return [["."] * largeur for _ in range(hauteur)]


def rect(g: list[list[str]], x: int, y: int, w: int, h: int, c: str) -> None:
    for j in range(y, y + h):
        for i in range(x, x + w):
            g[j][i] = c


def contourner(g: list[list[str]]) -> None:
    """Entoure d'un trait foncé tout ce qui est dessiné."""
    h, w = len(g), len(g[0])
    a_entourer = [(x, y) for y in range(h) for x in range(w) if g[y][x] == "." and any(
        0 <= x + dx < w and 0 <= y + dy < h and g[y + dy][x + dx] not in ".o"
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))]
    for x, y in a_entourer:
        g[y][x] = "o"


def dans_ellipse(x: int, y: int, cx: float, cy: float, rx: float, ry: float) -> bool:
    return ((x + 0.5 - cx) / rx) ** 2 + ((y + 0.5 - cy) / ry) ** 2 <= 1


def pot_et_tige(g, dy_feuilles: int, bas_tete: int) -> None:
    rect(g, 6, 17, 12, 2, "q")
    rect(g, 7, 19, 10, 2, "r")
    rect(g, 8, 21, 8, 2, "r")
    rect(g, 9, 19, 1, 4, "R")
    rect(g, 11, bas_tete, 2, 17 - bas_tete, "s")
    y = 15 + dy_feuilles
    rect(g, 8, y, 3, 1, "v")
    rect(g, 6, y - 1, 3, 1, "v")
    rect(g, 13, y, 3, 1, "v")
    rect(g, 15, y - 1, 3, 1, "v")
    rect(g, 9, y + 1, 2, 1, "V")
    rect(g, 13, y + 1, 2, 1, "V")


def tete_profil(g, cx: float, m: int, ouverture: int) -> None:
    """Tournée vers la droite : les mâchoires pivotent sur la charnière, à gauche."""
    charniere, bout = round(cx - 7), round(cx + 8)

    def ecart(x):  # combien la mâchoire s'est levée (ou baissée) à cette colonne
        return round(ouverture * 1.5 * max(0, x - charniere) / (bout - charniere))
    for x in range(24):
        e = ecart(x)
        for y in range(24):
            if y < m - e and dans_ellipse(x, y + e, cx, m, 9, 6):
                g[y][x] = "v"
            elif y > m + e and dans_ellipse(x, y - e, cx, m + 1, 8.5, 4):
                # Le haut de la mâchoire, plus foncé, la détache du dôme.
                g[y][x] = "v" if dans_ellipse(x, y - e - 1, cx, m + 1, 8.5, 4) else "V"
    for x, y in ((-5, -4), (-2, -5), (2, -4), (-6, -2)):
        rect(g, round(cx + x), m - ecart(round(cx + x)) + y, 1, 1, "l")
    # Les lèvres, du milieu jusqu'au bout du museau.
    for x in range(round(cx - 3), bout + 1):
        e = ecart(x)
        if g[m - e - 1][x] != ".":
            g[m - e - 1][x] = "L"
        if g[m + e + 1][x] != ".":
            g[m + e + 1][x] = "L"
        if ouverture == 0:
            g[m][x] = "M"
        else:
            rect(g, x, m - e, 1, 2 * e + 1, "b")
            if e >= 1 and x % 2 == 0:
                g[m - e][x] = "w"
                if ouverture == 2:
                    g[m + e][x] = "w"
    if ouverture == 0:
        rect(g, charniere + 1, m, round(cx - 3) - charniere - 1, 1, "v")
    if ouverture == 2:
        rect(g, round(cx + 1), m + 1, 3, 1, "t")


def carnivore_profil(ouverture: int, dy_feuilles: int, dy_tete: int) -> list[str]:
    g = toile(24, 24)
    m = 9 + dy_tete
    pot_et_tige(g, dy_feuilles, m + ouverture + 3)
    tete_profil(g, 11, m, ouverture)
    contourner(g)
    return ["".join(r) for r in g]


CARNIVORE = {"o": "#1d2a12", "v": "#5fa83c", "V": "#3f7a2a", "l": "#a6d86a", "s": "#3d7a35",
             "L": "#d8435a", "M": "#7a1a2c", "b": "#3a0d14", "w": "#f4f0e0", "t": "#e87a8a",
             "q": "#8e3b2a", "r": "#b5523b", "R": "#cf6a4e"}
for etat, ouverture in {"fermee": 0, "entrouverte": 1, "ouverte": 2}.items():
    for n, pose in enumerate([(0, 0), (-1, 0), (-1, -1), (0, -1)], 1):
        ecrire(ARCHIVES / "plante" / "carnivore-profil" / f"{etat}-{n}.png", carnivore_profil(ouverture, *pose), CARNIVORE)
