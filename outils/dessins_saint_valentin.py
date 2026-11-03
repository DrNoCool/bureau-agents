"""Dessine le thème de la Saint-Valentin (février), dans themes/saint-valentin/.

Usage : python outils/dessins_saint_valentin.py

Écrase les images existantes : git garde l'ancienne version. Ce qui n'est pas
dessiné ici garde, en février, son dessin de tous les jours.
"""
from atelier import (ARBRE_NU, ARBRE_NU_COULEURS, CADRE, CRAVATE, FENETRE, MAISON, PERSONNAGES,
                     RACINE, VIDE, ecrire, moulure, neige, personnages, r, recolorer)

THEME = RACINE / "themes" / "saint-valentin"

# ---------------------------------------------------------------- personnages
# Le chef devient le roi de cœur ; l'employé, Cupidon, qui fait le travail ;
# l'auditeur garde son noir, mais ses lunettes sont des cœurs ; l'explorateur
# rapporte un bouquet ; le générique devient un ourson en peluche.

# Le roi de cœur : couronne dorée (y) à rubis (R), veston rouge.
COURONNE = {
    "bas": {0: r(4, "y..yy..y"), 1: r(4, "yyyRRyyy"), 2: r(4, "yyyyyyyy")},
    "haut": {0: r(4, "y..yy..y"), 1: r(4, "yyyyyyyy"), 2: r(4, "yyyyyyyy")},
    "gauche": {0: r(5, "y..y..y"), 1: r(5, "yyRyyyy"), 2: r(5, "yyyyyyy")},
}

# Cupidon : cheveux blonds bouclés, tunique blanche, petites ailes (W) dans le dos.
AILES = {
    "bas": {7: "oW..osssssso..Wo", 8: "oWWooccccccooWWo", 9: "oWosccccccccsoWo", 10: ".oosccccccccsoo."},
    "haut": {7: "oW..ohhhhhho..Wo", 8: "oWWooccccccooWWo", 9: "oWosccccccccsoWo", 10: ".oosccccccccsoo."},
    "gauche": {7: r(4, "osssssso.Wo"), 8: r(5, "occcccoWWo"), 9: r(5, "occcccoWo")},
}

# L'auditeur : ses lunettes noires deviennent des cœurs rouges (R) ; une rose (P) à la boutonnière.
LUNETTES_COEUR = {
    "bas": {4: r(3, "oRsRssRsRo"), 5: r(3, "oRRRkkRRRo"), 6: r(3, "osRssssRso"), 9: r(2, "oscPcttcccso")},
    "haut": {},
    "gauche": {4: r(4, "oRsRhhhho"), 5: r(4, "oRRRshhho"), 6: r(3, "osRssshhho")},
}

# L'explorateur : un bouquet de roses (R, G) dans les bras, un cœur sur le ruban du chapeau.
BOUQUET_DANS_LES_BRAS = {
    "bas": {3: r(4, "oAARRAAo"), 9: r(2, "oscccRRcccso"), 10: r(2, "osccRGGRccso"), 11: r(3, "oCCCGGCCCo")},
    "haut": {},
    "gauche": {9: r(3, "RRocccco"), 10: r(3, "RGoscccco"), 11: r(4, "GoCCCCCo")},
}

# L'ourson : oreilles rondes (B), museau clair (m), un cœur rouge sur le ventre.
OURSON = {
    "bas": {1: r(3, "oo......oo"), 2: r(2, "oBBooooooBBo"), 3: r(2, "oBhhhhhhhhBo"), 4: r(3, "ohhhhhhhho"),
            5: r(3, "ohhehhehho"), 6: r(3, "ohhmmmmhho"), 7: r(4, "ohmeemho"),
            9: r(2, "osccRRRRccso"), 10: r(2, "oscccRRcccso")},
    "haut": {1: r(3, "oo......oo"), 2: r(2, "oBBooooooBBo"), 3: r(2, "oBhhhhhhhhBo")},
    "gauche": {1: r(9, "oo"), 2: r(5, "ohhhoBo")},
}

FOURRURE = "#8a5a32"
personnages(THEME, {
    "gestionnaire": ({**PERSONNAGES["gestionnaire"][0], "y": "#e0b04a", "R": "#c8202a", "c": "#b0203a",
                      "C": "#8a1830", "p": "#3a1a2a"}, [COURONNE, CRAVATE]),
    "employe": ({"h": "#f2d27a", "s": "#f2c7a5", "c": "#f4f4f4", "C": "#d8d8e0", "p": "#f4a0b4",
                 "W": "#eef4ff"}, [AILES]),
    "auditeur": ({**PERSONNAGES["auditeur"][0], "R": "#e0204a", "k": "#141414", "P": "#e0204a"},
                 [*PERSONNAGES["auditeur"][1], LUNETTES_COEUR]),
    "explorateur": ({**PERSONNAGES["explorateur"][0], "R": "#e0204a", "G": "#3f8a3a"},
                    [*PERSONNAGES["explorateur"][1], BOUQUET_DANS_LES_BRAS]),
    "generique": ({"h": FOURRURE, "B": "#c89a6a", "m": "#c89a6a", "s": "#c89a6a", "c": FOURRURE,
                   "C": "#6e4626", "p": FOURRURE, "b": "#6e4626", "R": "#e0204a"}, [OURSON]),
})

# ---------------------------------------------------------------------- décor
# Les murs rose tendre, la moulure framboise. Dehors, encore la neige.

MURS = moulure("#f0b8c8", "#e6a6b8", "#a03050", "#7a2040")
recolorer(THEME, "mur", MURS)
recolorer(THEME, "mur-bas", MURS)
recolorer(THEME, "porte", MURS)

COEURS = {"R": "#e0204a"}
COEUR = ["RR.RR", "RRRRR", ".RRR.", "..R.."]
recolorer(THEME, "fenetre", {**MURS, FENETRE["g"]: "#cfe0ee", FENETRE["l"]: "#e8f0f8"},
          [(6, 3, COEUR, COEURS), (20, 8, COEUR, COEURS)])
# Le cadre : un cœur sur fond rose, à la place du paysage.
recolorer(THEME, "cadre", {**MURS, CADRE["g"]: "#f8d0dc", CADRE["v"]: "#f8d0dc", CADRE["y"]: "#f8d0dc"},
          [(5, 5, COEUR, COEURS)])
# Le fauteuil du roi, en velours rouge.
recolorer(THEME, "fauteuil", {"#7a3e26": "#a01830", "#9a5636": "#c02040", "#4a2416": "#6a0a1a"})

neige(THEME)
recolorer(THEME, "maison", {MAISON["R"]: "#f4f6fa", MAISON["r"]: "#d0dbe6", MAISON["Y"]: "#ff9ab4"},
          [(21, 35, COEUR, COEURS)])
ecrire(THEME / "decor" / "arbre" / "image.png", ARBRE_NU, ARBRE_NU_COULEURS)

# ------------------------------------------------- les objets propres au thème

# Une guirlande de cœurs aux deux coins du mur, qui pend en arc.
ecrire(THEME / "decor" / "coin" / "image.png", [
    "llllllllllllllll", "l..............l", ".R............R.", "RRR..........RRR", ".R.l........l.R.",
    "....R......R....", "...RRR....RRR...", "....R.l..l.R....", ".......RR.......", "......RRRR......",
    ".......RR.......", *[VIDE] * 5,
], {"l": "#c8a0b0", "R": "#e0204a"})

# Un bouquet de roses dans un vase.
ecrire(THEME / "decor" / "bouquet" / "image.png", [
    *[VIDE] * 3, r(4, "RR.RR.RR"), r(3, "RrRRrRRrR"), r(4, "RR.RR.RR"), r(5, "G.GG.G"), r(4, "GG.GG.GG"),
    r(6, "GGGG"), r(5, "oooooo"), r(5, "ovvvvo"), r(5, "ovVvvo"), r(5, "ovvvvo"), r(5, "ovvvvo"),
    r(6, "oooo"), VIDE,
], {"R": "#e0204a", "r": "#a01030", "G": "#3f8a3a", "o": "#2b2b40", "v": "#a8c8e8", "V": "#e8f4ff"})


# Un ballon en cœur au bout de son fil, 16 × 24 ; il flotte d'un pixel.
def ballon_coeur(dy: int) -> list[str]:
    coeur = [r(3, "ooo..ooo"),
             r(2, "oRRRooRRRo"), r(2, "oRwRRRRRRo"), r(2, "oRRRRRRRRo"), r(3, "oRRRRRRo"),
             r(4, "oRRRRo"), r(5, "oRRo"), r(6, "oo")]
    fil = [r(6, "l") if i % 2 == 0 else r(7, "l") for i in range(14)]
    lignes = [VIDE] * (1 + dy) + coeur + fil
    return (lignes + [VIDE] * 24)[:24]


for n, dy in enumerate([0, 1], 1):
    ecrire(THEME / "decor" / "ballon-coeur" / f"flotte-{n}.png", ballon_coeur(dy),
           {"o": "#6a0a1a", "R": "#e0204a", "w": "#f8c0cc", "l": "#c8c8c8"})
