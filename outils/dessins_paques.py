"""Dessine le thème de Pâques (avril), dans themes/paques/.

Usage : python outils/dessins_paques.py

Écrase les images existantes : git garde l'ancienne version. Ce qui n'est pas
dessiné ici garde, en avril, son dessin de tous les jours.
"""
from atelier import (ARBRE, COL, CRAVATE, HERBE, LUNETTES_NOIRES, PERSONNAGES, RACINE, VIDE, ecrire,
                     moulure, personnages, r, recolorer)

THEME = RACINE / "themes" / "paques"

# ---------------------------------------------------------------- personnages
# Le chef devient le lapin de Pâques, en veston et cravate orange ; l'employé,
# un poussin ; l'auditeur, tout en noir, un lapin en chocolat noir, lunettes
# comprises ; l'explorateur part à la chasse aux cocos ; le générique est un
# coco décoré, sur pattes.


def lapin(fourrure: str, oreille: str, yeux: str, nez: str) -> dict:
    """Une tête de lapin, longues oreilles comprises : fourrure, dedans des oreilles, yeux, nez."""
    f, o_, y, n = fourrure, oreille, yeux, nez
    return {
        "bas": {0: r(4, "oo....oo"), 1: r(3, f"o{f}{o_}o..o{o_}{f}o"), 2: r(3, f"o{f}{o_}o..o{o_}{f}o"),
                3: r(3, f"o{f}{f}oooo{f}{f}o"), 4: r(3, f"o{f * 8}o"), 5: r(3, f"o{f}{f}{y}{f}{f}{y}{f}{f}o"),
                6: r(3, f"o{f * 3}{n}{n}{f * 3}o"), 7: r(4, f"o{f * 6}o")},
        "haut": {0: r(4, "oo....oo"), 1: r(3, f"o{f}{f}o..o{f}{f}o"), 2: r(3, f"o{f}{f}o..o{f}{f}o"),
                 3: r(3, f"o{f}{f}oooo{f}{f}o"), 4: r(3, f"o{f * 8}o"), 5: r(3, f"o{f * 8}o"),
                 6: r(3, f"o{f * 8}o"), 7: r(4, f"o{f * 6}o")},
        "gauche": {0: r(8, "oo"), 1: r(7, f"o{f}{o_}o"), 2: r(6, f"o{f}{o_}o"), 3: r(4, f"o{f * 7}o"),
                   4: r(4, f"o{f * 7}o"), 5: r(4, f"o{f}{y}{f * 5}o"), 6: r(3, f"o{n}{f * 7}o"),
                   7: r(4, f"o{f * 6}o")},
    }


# Le lapin de Pâques : blanc (w), oreilles roses (P), nez rose.
LAPIN = lapin("w", "P", "e", "P")
# Le lapin en chocolat noir (h), reflets plus clairs (H), lunettes noires qui brillent (W) ; un nœud rouge (R) au cou.
CHOCOLAT = lapin("h", "H", "e", "H")
CHOCOLAT["bas"][5] = r(3, "ogWgggWggo")
CHOCOLAT["gauche"][5] = r(4, "ogWgHhhho")
NOEUD = {"bas": {8: r(3, "oocRRRRcoo")}, "gauche": {8: r(5, "oRRccco")}}

# Le poussin : tout jaune (y), une houppe, un bec orange (B) ; la chemise bleue de l'employé.
POUSSIN = {
    "bas": {0: r(6, "y.y"), 1: r(5, "oooooo"), 2: r(4, "oyyyyyyo"), 3: r(3, "oyyyyyyyyo"), 4: r(3, "oyyyyyyyyo"),
            5: r(3, "oyyeyyeyyo"), 6: r(3, "oyyyBByyyo"), 7: r(4, "oyyyyyyo")},
    "haut": {0: r(6, "y.y"), 1: r(5, "oooooo"), 2: r(4, "oyyyyyyo"), 3: r(3, "oyyyyyyyyo"),
             4: r(3, "oyyyyyyyyo"), 5: r(3, "oyyyyyyyyo"), 6: r(3, "oyyyyyyyyo"), 7: r(4, "oyyyyyyo")},
    "gauche": {0: r(7, "y.y"), 1: r(6, "ooooo"), 2: r(5, "oyyyyyo"), 3: r(4, "oyyyyyyyo"),
               4: r(4, "oyyyyyyyo"), 5: r(4, "oyeyyyyyo"), 6: r(2, "oBByyyyyyyo"), 7: r(4, "oyyyyyyo")},
}

# L'explorateur : un panier (n) plein de cocos (P, y, B) dans les bras.
PANIER_DANS_LES_BRAS = {
    "bas": {9: r(2, "osccPyBPccso"), 10: r(2, "oscnnnnnncso"), 11: r(3, "oCnnnnnnCo")},
    "haut": {},
    "gauche": {9: r(2, "PyBocccco"), 10: r(2, "nnnoscccco"), 11: r(3, "nnoCCCCCo")},
}


# Le coco décoré : rayures pastel, deux yeux, sur ses pattes.
def coco() -> dict:
    rayures = [r(6, "oooo"), r(5, "oPPPPo"), r(4, "oPPPPPPo"), r(3, "oYYYYYYYYo"), r(3, "oddddddddo"),
               r(3, "oZZZZZZZZo"), r(3, "oddddddddo"), r(3, "oBBBBBBBBo"), r(3, "oddddddddo"),
               r(3, "oPPPPPPPPo"), r(4, "oddddddo"), r(5, "oooooo")]
    face = list(rayures)
    face[4] = r(3, "oddeddeddo")
    cote = list(rayures)
    cote[4] = r(3, "odeddddddo")
    return {"bas": dict(enumerate(face, 1)), "haut": dict(enumerate(rayures, 1)),
            "gauche": dict(enumerate(cote, 1))}


personnages(THEME, {
    "gestionnaire": ({**PERSONNAGES["gestionnaire"][0], "w": "#f4f4f4", "P": "#f4a0b4"}, [LAPIN, CRAVATE]),
    "employe": ({**PERSONNAGES["employe"][0], "y": "#f6d84a", "B": "#e8822a", "s": "#f6d84a", "p": "#e8822a",
                 "b": "#c86a1a"}, [POUSSIN, COL]),
    "auditeur": ({"h": "#4a2a1a", "H": "#7a4a2a", "g": "#050505", "W": "#c8c8d0", "c": "#4a2a1a", "C": "#3a1e12",
                  "p": "#4a2a1a", "s": "#4a2a1a", "R": "#c0202a", "b": "#3a1e12"}, [CHOCOLAT, NOEUD]),
    "explorateur": ({**PERSONNAGES["explorateur"][0], "P": "#f4a0b4", "y": "#f6d84a", "B": "#8ad0e0",
                     "n": "#a0703a"}, [*PERSONNAGES["explorateur"][1], PANIER_DANS_LES_BRAS]),
    "generique": ({"d": "#f8f0d8", "P": "#f4a0b4", "Y": "#f6d365", "Z": "#8ad0e0", "B": "#b8a0e0",
                   "p": "#f4f4f4"}, [coco()]),
})

# ---------------------------------------------------------------------- décor
# Les murs jaune pâle, la moulure vert tendre. Dehors, le printemps : l'herbe
# fleurie, les arbres en fleurs.

MURS = moulure("#f8eab0", "#f0dc98", "#8ab868", "#6a9a4a")
recolorer(THEME, "mur", MURS)
recolorer(THEME, "mur-bas", MURS)
recolorer(THEME, "porte", MURS)
FLEURS = {"p": "#f4a0b4", "y": "#f6d365", "w": "#f4f4f4"}
recolorer(THEME, "herbe", {HERBE["g"]: "#9ad078", HERBE["G"]: "#7ab85e"},
          [(4, 4, ["p"], FLEURS), (11, 9, ["y"], FLEURS), (2, 12, ["w"], FLEURS), (13, 2, ["w"], FLEURS)])
recolorer(THEME, "arbre", {ARBRE["v"]: "#f4b0c8", ARBRE["V"]: "#d88aa8"})

# ------------------------------------------------- les objets propres au thème

OEUFS = {"o": "#5a4030", "P": "#f4a0b4", "Y": "#f6d365", "Z": "#8ad0e0", "B": "#b8a0e0", "n": "#a0703a",
         "N": "#7a5028", "g": "#7ab85e"}

# Un panier d'osier (n) plein de cocos.
ecrire(THEME / "decor" / "panier" / "image.png", [
    *[VIDE] * 4, r(4, "nnnnnnnn"), r(3, "n......n"), r(2, "n........n"), r(3, "oPoYoBoZo"), r(2, "oPPYYoBBZZo"),
    r(1, "nnnnnnnnnnnnn"), r(1, "nNnNnNnNnNnNn"), r(2, "nnnnnnnnnnn"), r(2, "nNnNnNnNnNn"), r(3, "nnnnnnnnn"),
    r(4, "NNNNNNN"), VIDE,
], OEUFS)

# Trois cocos cachés dans l'herbe.
ecrire(THEME / "decor" / "oeufs" / "image.png", [
    *[VIDE] * 8, r(2, "oo"), r(1, "oPPo.....oo"), r(1, "oPPo....oYYo"), r(1, "gPPg.oo.oYYo"),
    r(2, "gg.oZZo.gg"), r(4, "gZZg..g"), r(5, "gg"), VIDE,
], OEUFS)

# Des tulipes.
ecrire(THEME / "decor" / "tulipes" / "image.png", [
    *[VIDE] * 6, r(1, "R.R...Y.Y"), r(1, "RRR...YYY..P.P"), r(1, "RRR...YYY..PPP"), r(2, "g.....g...PPP"),
    r(2, "g.....g....g"), r(1, "gg.....gg..g"), r(2, "g.....g...gg"), r(2, "g.....g....g"), *[VIDE] * 2,
], {"R": "#e8402a", "Y": "#f6d365", "P": "#f4a0b4", "g": "#3f8a3a"})

# Une guirlande de fanions pastel, aux deux coins du mur.
ecrire(THEME / "decor" / "coin" / "image.png", [
    VIDE, "llllllllllllllll", "PPP.YYY.ZZZ.BBB.", ".P...Y...Z...B..", *[VIDE] * 12,
], {"l": "#a08060", "P": "#f4a0b4", "Y": "#f6d365", "Z": "#8ad0e0", "B": "#b8a0e0"})
