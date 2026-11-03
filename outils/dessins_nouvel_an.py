"""Dessine le thème du jour de l'An (janvier), dans themes/nouvel-an/.

Usage : python outils/dessins_nouvel_an.py

Écrase les images existantes : git garde l'ancienne version. Ce qui n'est pas
dessiné ici garde, en janvier, son dessin de tous les jours.
"""
from atelier import (ARBRE_NU, ARBRE_NU_COULEURS, CADRE, FENETRE, MAISON, PERSONNAGES, RACINE, VIDE,
                     ecrire, moulure, neige, personnages, r, recolorer)

THEME = RACINE / "themes" / "nouvel-an"

# ---------------------------------------------------------------- personnages
# Le chef reçoit, en haut-de-forme ; l'employé fait la fête ; l'auditeur, en
# noir, devient le Père Temps qui ferme l'année ; l'explorateur part en
# coureur des bois ; le générique, l'inconnu de l'année qui vient, en bébé de l'An.

# Le chef : haut-de-forme noir (k) à ruban doré (y), nœud papillon orange (t).
HAUT_DE_FORME = {
    "bas": {0: r(5, "oooooo"), 1: r(5, "okkkko"), 2: r(5, "okyyko"), 3: r(3, "okkkkkkkko"),
            8: r(3, "oocttttcoo")},
    "haut": {0: r(5, "oooooo"), 1: r(5, "okkkko"), 2: r(5, "okyyko"), 3: r(3, "okkkkkkkko")},
    "gauche": {0: r(6, "ooooo"), 1: r(6, "okkko"), 2: r(6, "okyko"), 3: r(4, "okkkkkkkko"),
               8: r(5, "otcccco")},
}

# L'employé : chapeau de fête rayé (P, B) à pompon (y), une langue de belle-mère (Y) au bec.
CHAPEAU_FETE = {
    "bas": {0: r(7, "yy"), 1: r(6, "oPPo"), 2: r(5, "oBBBBo"), 3: r(3, "ohPPPPPPho"),
            7: r(4, "ossssssoYY")},
    "haut": {0: r(7, "yy"), 1: r(6, "oPPo"), 2: r(5, "oBBBBo"), 3: r(3, "ohPPPPPPho")},
    "gauche": {0: r(7, "yy"), 1: r(6, "oPPo"), 2: r(5, "oBBBBo"), 3: r(4, "ohPPPPPho"),
               7: r(1, "YYYosssssso")},
}

# Le Père Temps : chauve, cheveux et longue barbe blancs, robe noire, un sablier (y, Y) à la main.
PERE_TEMPS = {
    "bas": {2: r(4, "osssssso"), 3: r(3, "ohssssssho"), 4: r(3, "ohssssssho"), 6: r(3, "owwwsswwwo"),
            7: r(4, "owwwwwwo"), 8: r(3, "oocwwwwcoo"), 9: r(2, "oscwwwwwwcsoy"),
            10: r(2, "osccwwwwccsoY"), 11: r(3, "oCCCwwCCCo.y")},
    "haut": {2: r(4, "osssssso")},
    "gauche": {2: r(5, "ossssso"), 3: r(4, "osssshhho"), 6: r(2, "owwwwwshhho"), 7: r(3, "owwwwsso"),
               8: r(4, "owwwccco"), 9: r(2, "y..occccco"), 10: r(2, "Y..oscccco"), 11: r(2, "y..oCCCCCo")},
}

# Le coureur des bois : tuque rouge (r) à bordure blanche, ceinture fléchée (R, U, Y).
COUREUR_DES_BOIS = {
    "bas": {0: r(7, "WW"), 1: r(5, "orrrro"), 2: r(4, "orrrrrro"), 3: r(3, "oWWWWWWWWo"),
            11: r(3, "oRURYRURYo")},
    "haut": {0: r(7, "WW"), 1: r(5, "orrrro"), 2: r(4, "orrrrrro"), 3: r(3, "oWWWWWWWWo"),
             11: r(3, "oRURYRURYo")},
    "gauche": {0: r(8, "WW"), 1: r(6, "orrro"), 2: r(5, "orrrrro"), 3: r(4, "oWWWWWWWo"),
               11: r(5, "oRURYRo")},
}

# Le bébé de l'An : chauve avec une boucle, une écharpe rouge en travers, une couche.
BEBE = {
    "bas": {1: r(5, "ooohoo"), 9: r(2, "oscrccccccso"), 10: r(2, "osccrcccccso"),
            8: r(3, "oorcccccoo"), 11: r(3, "oddddddddo"), 12: r(4, "oddddddo")},
    "haut": {1: r(5, "ooohoo"), 8: r(3, "oorcccccoo"), 11: r(3, "oddddddddo"), 12: r(4, "oddddddo")},
    "gauche": {1: r(6, "oohoo"), 9: r(5, "orcccco"), 11: r(5, "oddddddo")},
}

PEAU_BEBE = "#f2c7a5"
personnages(THEME, {
    "gestionnaire": ({**PERSONNAGES["gestionnaire"][0], "k": "#141414", "y": "#e0b04a"}, [HAUT_DE_FORME]),
    "employe": ({**PERSONNAGES["employe"][0], "P": "#e85a9a", "B": "#4a8ae8", "y": "#ffd34a",
                 "Y": "#ffd34a"}, [CHAPEAU_FETE, *PERSONNAGES["employe"][1]]),
    "auditeur": ({"h": "#e8e8e8", "s": "#f0d2bc", "c": "#1c1c1c", "C": "#0e0e0e", "p": "#1c1c1c",
                  "y": "#e0b04a", "Y": "#e8d8a0"}, [PERE_TEMPS]),
    "explorateur": ({**PERSONNAGES["explorateur"][0], "r": "#c8202a", "W": "#f4f4f4", "R": "#c8202a",
                     "U": "#2f5a9a", "Y": "#e0b04a"}, [COUREUR_DES_BOIS]),
    "generique": ({"h": PEAU_BEBE, "s": PEAU_BEBE, "c": PEAU_BEBE, "C": "#dca88a", "p": PEAU_BEBE,
                   "b": "#dca88a", "r": "#c8202a", "d": "#f4f4f4"}, [BEBE]),
})

# ---------------------------------------------------------------------- décor
# Une soirée chic : murs bleu nuit, moulure dorée. Dehors, la neige et les feux d'artifice.

MURS = moulure("#1e2a4a", "#18223e", "#c8a040", "#8a6a2a")
recolorer(THEME, "mur", MURS)
recolorer(THEME, "mur-bas", MURS)
recolorer(THEME, "porte", MURS)

FEUX = {"r": "#e8402a", "y": "#ffd34a", "b": "#6ab0ff", "p": "#e85a9a"}
recolorer(THEME, "fenetre", {**MURS, FENETRE["g"]: "#141a34", FENETRE["l"]: "#20284a"}, [
    (5, 3, [".r.r.", "..r..", ".r.r."], FEUX),
    (10, 4, ["y.y", ".y.", "y.y"], FEUX),
    (19, 8, [".b.b.", "..b..", ".b.b."], FEUX),
    (24, 9, ["p.p", ".p.", "p.p"], FEUX),
])
recolorer(THEME, "cadre", {**MURS, CADRE["g"]: "#141a34", CADRE["v"]: "#f4f6fa", CADRE["y"]: "#f4e8a0"})

neige(THEME)
recolorer(THEME, "maison", {MAISON["R"]: "#f4f6fa", MAISON["r"]: "#d0dbe6"})
ecrire(THEME / "decor" / "arbre" / "image.png", ARBRE_NU, ARBRE_NU_COULEURS)

# ------------------------------------------------- les objets propres au thème

# Une horloge au coin gauche du mur, les aiguilles sur minuit.
ecrire(THEME / "decor" / "coin-gauche" / "image.png", [
    VIDE, r(5, "oooooo"), r(4, "oyyyyyyo"), r(3, "oywwkwwwyo"), r(3, "oywwkwwwyo"), r(3, "oywwkwwwyo"),
    r(3, "oywwwwwwyo"), r(3, "oywwwwwwyo"), r(4, "oyyyyyyo"), r(5, "oooooo"), *[VIDE] * 6,
], {"o": "#3a2a10", "y": "#c8a040", "w": "#f4f0e0", "k": "#1d1d1d"})


# Une grappe de ballons sur leurs fils, 16 × 24 ; elle se balance d'un pixel.
def ballons(dx: int) -> list[str]:
    haut = ["..ooo....ooo....",
            ".orrro..oyyyo...",
            ".orwro..oywyo...",
            ".orrroooooyyo...",
            "..ooobbbbbooo...",
            "....obwbbbo.....",
            "....obbbbbo.....",
            ".....obbbo......",
            "...l..ooo..l....",
            "....l..l..l....."]
    fils = [r(7, "l") for _ in range(8)]
    return [VIDE] + [("." * dx + l)[:16] for l in haut] + fils + [r(6, "kkk"), *[VIDE] * 4]


for n, dx in enumerate([0, 1], 1):
    ecrire(THEME / "decor" / "ballons" / f"vent-{n}.png", ballons(dx),
           {"o": "#2b1d16", "r": "#e8402a", "y": "#ffd34a", "b": "#4a8ae8", "w": "#f4f4f4", "l": "#c8c8c8",
            "k": "#5c3b22"})


# Un feu d'artifice qui monte, éclate et retombe.
def feu(image: int) -> list[str]:
    images = [
        [*[VIDE] * 12, r(7, "y"), r(7, "y"), r(7, "Y"), VIDE],
        [*[VIDE] * 3, r(7, "y"), r(5, "y.y.y"), r(6, "yyy"), r(4, "yyyYyyy"), r(6, "yyy"),
         r(5, "y.y.y"), r(7, "y"), *[VIDE] * 6],
        [VIDE, r(7, "r"), r(3, "r..r.r..r"), r(4, "r.r.r.r"), r(5, "r.y.r"), r(2, "rrr.yYy.rrr"),
         r(5, "r.y.r"), r(4, "r.r.r.r"), r(3, "r..r.r..r"), r(7, "r"), *[VIDE] * 6],
        [*[VIDE] * 2, r(3, "p.......p"), r(7, "p"), r(2, "p...p.p...p"), *[VIDE] * 2,
         r(2, "p.........p"), r(7, "p"), r(4, "p.....p"), *[VIDE] * 6],
    ]
    return images[image]


for i in range(4):
    ecrire(THEME / "decor" / "feu-artifice" / f"eclat-{i + 1}.png", feu(i),
           {"y": "#ffd34a", "Y": "#fff4b0", "r": "#e8402a", "p": "#e85a9a"})
