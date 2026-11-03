"""Les outils communs aux scripts des thèmes (dessins_<thème>.py).

Les gabarits des personnages et les outils de dessin viennent de
dessins_initiaux.py, lus sans l'exécuter : l'importer redessinerait tout le
décor de tous les jours.
"""
import ast
from pathlib import Path

from PIL import Image

RACINE = Path(__file__).resolve().parent.parent

EMPRUNTS = ["ecrire", "toile", "rect", "cadre", "texte", "POSES", "ORDRE", "COMMUNES",
            "CHAPEAU_BROUSSE", "LUNETTES_NOIRES", "COL", "CRAVATE", "PERSONNAGES"]
_source = ast.parse((RACINE / "outils" / "dessins_initiaux.py").read_text(encoding="utf-8"))
_noeuds = [n for n in _source.body
           if (isinstance(n, ast.FunctionDef) and n.name in EMPRUNTS)
           or (isinstance(n, ast.Assign) and getattr(n.targets[0], "id", None) in EMPRUNTS + ["CORPS_FACE"])]
_emprunts = {"RACINE": RACINE, "Image": Image, "Path": Path}
exec(compile(ast.Module(_noeuds, type_ignores=[]), "dessins_initiaux.py", "exec"), _emprunts)
(ecrire, toile, rect, cadre, texte, POSES, ORDRE, COMMUNES,
 CHAPEAU_BROUSSE, LUNETTES_NOIRES, COL, CRAVATE, PERSONNAGES) = (_emprunts[n] for n in EMPRUNTS)

VIDE = "." * 16


def r(x: int, s: str, largeur: int = 16) -> str:
    """Une rangée : s posé à la colonne x, du vide autour."""
    assert x + len(s) <= largeur, f"« {s} » à la colonne {x} déborde de {largeur} pixels"
    return "." * x + s + "." * (largeur - x - len(s))


def sur(rangee: str, x: int, s: str) -> str:
    """s posé par-dessus une rangée existante, ses points laissant voir dessous."""
    pixels = list(rangee)
    for i, c in enumerate(s):
        if c != ".":
            pixels[x + i] = c
    return "".join(pixels)


def rgb(couleur: str) -> tuple:
    h = couleur.lstrip("#")
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), 255


# ---------------------------------------------------------------- personnages
# Même mécanique que les personnages de tous les jours : la pose de base, puis
# les accessoires, rangée par rangée. Une clé « bas0 » l'emporte sur « bas » :
# elle ne vaut que pour cette image de la marche. Une rangée en texte remplace
# celle de la pose ; un couple (x, texte) se pose par-dessus, à la colonne x.

def personnages(theme: Path, definitions: dict) -> None:
    for nom, (couleurs, accessoires) in definitions.items():
        planche = []
        for rangee_poses in ORDRE:
            grilles = []
            for pose in rangee_poses:
                grille = list(POSES[pose])
                for accessoire in accessoires:
                    for i, rangee in accessoire.get(pose, accessoire.get(pose.rstrip("01"), {})).items():
                        grille[i] = rangee if isinstance(rangee, str) else sur(grille[i], *rangee)
                grilles.append(grille)
            planche += ["".join(g[y] for g in grilles) for y in range(16)]
        ecrire(theme / "personnages" / nom / "planche.png", planche, {**COMMUNES, **couleurs})


# ---------------------------------------------------------------------- décor

def recolorer(theme: Path, element: str, couleurs: dict[str, str], motifs=()) -> None:
    """Chaque image de decor/<element>/, couleur pour couleur ; puis les motifs (x, y, grille, palette)."""
    for source in sorted((RACINE / "decor" / element).glob("*.png")):
        chemin = theme / "decor" / element / source.name
        img = Image.open(source).convert("RGBA")
        px = img.load()
        nouvelles = {rgb(a)[:3]: rgb(b) for a, b in couleurs.items()}
        for y in range(img.height):
            for x in range(img.width):
                if px[x, y][3] and px[x, y][:3] in nouvelles:
                    px[x, y] = nouvelles[px[x, y][:3]]
        for mx, my, grille, palette in motifs:
            for j, rangee in enumerate(grille):
                for i, c in enumerate(rangee):
                    if c != ".":
                        px[mx + i, my + j] = rgb(palette[c])
        chemin.parent.mkdir(parents=True, exist_ok=True)
        img.save(chemin)
        print(f"dessiné   {chemin.relative_to(RACINE)}")


# Les couleurs de tous les jours, pour les recolorer.
MOULURE = {"w": "#f1e3c6", "x": "#e2cfa9", "m": "#9c6b43", "n": "#6e4a2e", "k": "#4a3424"}
HERBE = {"g": "#8cc06a", "G": "#6fa452"}
ROUTE = {"s": "#e8d5a0", "S": "#cdb67e"}
FENETRE = {"g": "#9fd3e6", "l": "#e3f5fb"}
CADRE = {"g": "#bfe3f0", "v": "#6aa84f", "y": "#f2c14e"}
MAISON = {"R": "#c0503a", "r": "#96392a", "W": "#f0e0c0", "w": "#d8c49c", "Y": "#f6d365",
          "N": "#2f3a4a", "D": "#7a4a2a"}
ARBRE = {"v": "#4f9a4a", "V": "#2f6b33"}
PANCARTE = {"r": "#d0402f", "u": "#3b6fb6", "n": "#7a5230", "N": "#5c3b22", "b": "#9c6b43"}


def moulure(w: str, x: str, m: str, n: str) -> dict[str, str]:
    """Les murs (papier peint w et x, moulure m et n) : la table de recoloriage."""
    return {MOULURE["w"]: w, MOULURE["x"]: x, MOULURE["m"]: m, MOULURE["n"]: n}


def neige(theme: Path) -> None:
    """L'herbe sous la neige, la route déneigée."""
    recolorer(theme, "herbe", {HERBE["g"]: "#eef2f6", HERBE["G"]: "#d0dbe6"})
    recolorer(theme, "route", {ROUTE["s"]: "#b8b8c0", ROUTE["S"]: "#9a9aa4"})


# Un arbre nu, la neige sur les branches.
ARBRE_NU = [
    VIDE,
    "..t.........t...",
    "..Wt...t...tW...",
    "t..t..WtW.t...t.",
    ".tWtt..t.tt..tW.",
    "..t..t.t.t..t...",
    "...t..ttt..t....",
    "....tt.tt.t.....",
    "......ttttt.....",
    "......tTtt......",
    "......tTtt......",
    "......tTtt......",
    "......tTtt......",
    ".....ttTttt.....",
    "....WWWWWWWW....",
    VIDE,
]
ARBRE_NU_COULEURS = {"t": "#3a2a22", "T": "#24180f", "W": "#f4f6fa"}
