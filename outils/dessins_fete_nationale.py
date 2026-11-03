"""Dessine le thème de la Fête nationale du Québec (juin), dans themes/fete-nationale/.

Usage : python outils/dessins_fete_nationale.py

Écrase les images existantes : git garde l'ancienne version. Ce qui n'est pas
dessiné ici garde, en juin, son dessin de tous les jours.
"""
from atelier import (COL, CRAVATE, LUNETTES_NOIRES, MAISON, PERSONNAGES, RACINE, VIDE, ecrire, moulure,
                     personnages, r, recolorer)

THEME = RACINE / "themes" / "fete-nationale"
BLEU, BLEU_FONCE, BLANC = "#1f4fa0", "#163a78", "#f4f6fa"

# ---------------------------------------------------------------- personnages
# Le chef, en veston bleu, les joues peintes ; l'employé, en chandail
# fleurdelisé ; l'auditeur, tout en noir, devient le chansonnier du feu de
# joie ; l'explorateur devient Jacques Cartier ; le générique, le mouton
# des défilés de la Saint-Jean d'autrefois.

# Le chef : veston bleu, cravate blanche, une fleur de lys peinte (B) sur chaque joue.
JOUES_PEINTES = {"bas": {6: r(3, "ohBssssBho")}, "gauche": {6: r(3, "osBssshhho")}}

# L'employé : chandail bleu à croix blanche (w), comme le drapeau.
CHANDAIL_DRAPEAU = {
    "bas": {9: r(2, "oscccwwcccso"), 10: r(2, "oswwwwwwwwso"), 11: r(3, "oCCCwwCCCo")},
    "haut": {9: r(2, "oscccwwcccso"), 10: r(2, "oswwwwwwwwso"), 11: r(3, "oCCCwwCCCo")},
    "gauche": {9: r(5, "occwcco"), 10: r(5, "owwwwwo"), 11: r(5, "oCCwCCo")},
}

# Le chansonnier : lunettes noires, chandail noir, une guitare (G) en bandoulière, le manche (n) à droite.
GUITARE = {
    "bas": {9: r(2, "oscGGGnnnnnno"), 10: r(2, "osGGkGGcccso"), 11: r(3, "oGGGCCCCCo")},
    "haut": {9: r(13, "nn")},
    "gauche": {9: r(3, "nnGGGcco"), 10: r(4, "GkGcccco"), 11: r(4, "GGGCCCCo")},
}

# Jacques Cartier : béret noir (k) à plume blanche (W), barbe, fraise blanche au cou.
CARTIER = {
    "bas": {0: r(11, "oWo"), 1: r(4, "oooooooWo"), 2: r(2, "okkkkkkkkkWo"), 3: r(3, "ohhhhhhhho"),
            6: r(3, "ohhhsshhho"), 7: r(4, "ohhhhhho"), 8: r(3, "owwwwwwwwo")},
    "haut": {0: r(11, "oWo"), 1: r(4, "oooooooWo"), 2: r(2, "okkkkkkkkkWo"), 8: r(3, "owwwwwwwwo")},
    "gauche": {0: r(11, "oWo"), 1: r(5, "ooooooWo"), 2: r(3, "okkkkkkkkWo"), 6: r(3, "ohhhhhhhho"),
               7: r(4, "ohhhhhho"), 8: r(4, "owwwwwwo")},
}

# Le mouton : laine blanche (d), tête et pattes noires (k).
MOUTON = {
    "bas": {1: r(4, "oooooooo"), 2: r(3, "oddddddddo"), 3: r(1, "okkoddddddokko"), 4: r(3, "odkkkkkkdo"),
            5: r(3, "odkwkkwkdo"), 6: r(3, "odkkkkkkdo"), 7: r(4, "okkkkkko"), 8: r(2, "oddddddddddo"),
            9: r(1, "oddddddddddddo"), 10: r(1, "odddDddddDdddo"), 11: r(1, "oddddddddddddo"),
            12: r(2, "oDDDDDDDDDDo")},
    "haut": {1: r(4, "oooooooo"), 2: r(3, "oddddddddo"), 3: r(1, "okkoddddddokko"), 4: r(3, "oddddddddo"),
             5: r(3, "oddddddddo"), 6: r(3, "oddddddddo"), 7: r(4, "oddddddo"), 8: r(2, "oddddddddddo"),
             9: r(1, "oddddddddddddo"), 10: r(1, "odddDddddDdddo"), 11: r(1, "oddddddddddddo"),
             12: r(2, "oDDDDDDDDDDo")},
    "gauche": {1: r(5, "oooooo"), 2: r(4, "oddddddo"), 3: r(2, "okkoddddddo"), 4: r(1, "okkkkoddddddo"),
               5: r(1, "okwkkoddddddo"), 6: r(1, "okkkkoddddddo"), 7: r(2, "ooooddddddo"),
               8: r(3, "oddddddddddo"), 9: r(3, "oddddddddddo"), 10: r(3, "oddDdddDdddo"),
               11: r(3, "oddddddddddo"), 12: r(4, "oDDDDDDDDo")},
}

personnages(THEME, {
    "gestionnaire": ({**PERSONNAGES["gestionnaire"][0], "c": BLEU, "C": BLEU_FONCE, "p": BLEU_FONCE,
                      "t": BLANC, "B": BLEU}, [CRAVATE, JOUES_PEINTES]),
    "employe": ({**PERSONNAGES["employe"][0], "c": BLEU, "C": BLEU_FONCE, "w": BLANC}, [CHANDAIL_DRAPEAU]),
    "auditeur": ({**PERSONNAGES["auditeur"][0], "G": "#a0602a", "n": "#5c3b22", "k": "#1d1d1d"},
                 [LUNETTES_NOIRES, GUITARE]),
    "explorateur": ({**PERSONNAGES["explorateur"][0], "k": "#1d1d1d", "W": BLANC, "h": "#5a3a22"}, [CARTIER]),
    "generique": ({"d": "#f0f0e8", "D": "#c8c8bc", "k": "#3a3a3a", "w": BLANC, "p": "#3a3a3a",
                   "b": "#1d1d1d"}, [MOUTON]),
})

# ---------------------------------------------------------------------- décor
# Les murs bleu ciel, la moulure bleu drapeau ; des fanions dans les maisons.

MURS = moulure("#c8d8f0", "#b0c4e8", BLEU, BLEU_FONCE)
recolorer(THEME, "mur", MURS)
recolorer(THEME, "mur-bas", MURS)
recolorer(THEME, "porte", MURS)
recolorer(THEME, "fenetre", MURS)

# Le cadre : le drapeau fleurdelisé.
ecrire(THEME / "decor" / "cadre" / "image.png", [
    *[VIDE] * 3, r(3, "nnnnnnnnnn"), r(3, "nbbbwwbbbn"), r(3, "nbwbwwbwbn"), r(3, "nbbbwwbbbn"),
    r(3, "nwwwwwwwwn"), r(3, "nbbbwwbbbn"), r(3, "nbwbwwbwbn"), r(3, "nbbbwwbbbn"), r(3, "nnnnnnnnnn"),
    *[VIDE] * 4,
], {"n": BLEU_FONCE, "b": BLEU, "w": BLANC})

FANIONS = {"b": BLEU, "w": BLANC}
recolorer(THEME, "maison", {MAISON["R"]: "#2f5aa8", MAISON["r"]: "#1f4a8a"},
          [(6, 25, ["bbb.www." * 4 + "bbb."], FANIONS), (7, 26, [".b...w.." * 4 + ".b.."], FANIONS)])

# ------------------------------------------------- les objets propres au thème

# Une guirlande de fanions bleus et blancs, aux deux coins du mur.
ecrire(THEME / "decor" / "coin" / "image.png", [
    VIDE, "llllllllllllllll", "bbb.www.bbb.www.", ".b...w...b...w..", *[VIDE] * 12,
], {"l": "#5c3b22", **FANIONS})


# Le drapeau fleurdelisé sur son mât, 16 × 24 ; il claque au vent.
def drapeau(image: int) -> list[str]:
    toile = ["bbbwbbbb", "bwbwbwbb", "bbbwbbbb", "wwwwwwww", "bbbwbbbb", "bwbwbwbb", "bbbwbbbb"]
    if image == 2:
        toile = [t[:6] + "." + t[7] if i % 2 else t for i, t in enumerate(toile)]
    return [r(4, "y"), *[r(4, "m" + t) for t in toile], *[r(4, "m")] * 14, r(3, "mmm"), VIDE]


for n in (1, 2):
    ecrire(THEME / "decor" / "drapeau" / f"vent-{n}.png", drapeau(n),
           {"y": "#e0b04a", "m": "#7a5230", **FANIONS})


# Le feu de joie : les bûches (n), les flammes (r, o, y) qui dansent.
def feu(image: int) -> list[str]:
    flammes = [
        [r(7, "y"), r(6, "yo"), r(5, "yoor"), r(4, "roooyr"), r(4, "royyor"), r(3, "rroyyorr")],
        [r(8, "y"), r(7, "oy"), r(5, "royo"), r(4, "rooyor"), r(4, "royyor"), r(3, "rroyyorr")],
        [r(6, "y"), r(6, "oy"), r(5, "royyr"), r(4, "royoor"), r(4, "royyor"), r(3, "rroyyorr")],
    ][image]
    return [*[VIDE] * 7, *flammes, r(2, "nnNnnnnNnnn"), r(3, "NnnnNnnnN"), VIDE]


for i in range(3):
    ecrire(THEME / "decor" / "feu-de-joie" / f"flamme-{i + 1}.png", feu(i),
           {"y": "#ffd34a", "o": "#f0902a", "r": "#d8402a", "n": "#7a4a2a", "N": "#4a2a1a"})
