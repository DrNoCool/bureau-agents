"""Dessine le thème de la fête du Canada (juillet), dans themes/fete-du-canada/.

Usage : python outils/dessins_fete_du_canada.py

Écrase les images existantes : git garde l'ancienne version. Ce qui n'est pas
dessiné ici garde, en juillet, son dessin de tous les jours.
"""
from atelier import COL, PERSONNAGES, RACINE, VIDE, ecrire, moulure, personnages, r, recolorer

THEME = RACINE / "themes" / "fete-du-canada"
ROUGE, ROUGE_FONCE, BLANC = "#c8202a", "#9a1820", "#f4f4f4"

# ---------------------------------------------------------------- personnages
# Le chef, en gendarme de la GRC ; l'employé, en bûcheron ; l'auditeur, qui
# juge, en arbitre de hockey ; l'explorateur, en canot, la pagaie à la main ;
# le générique devient un castor.

# Le gendarme : chapeau de feutre brun (H) à bande noire, tunique rouge, ceinture brune (n).
GENDARME = {
    "bas": {1: r(5, "oHHHHo"), 2: r(4, "okkkkkko"), 3: r(1, "oHHHHHHHHHHHHo"), 11: r(3, "onnnyynnno")},
    "haut": {1: r(5, "oHHHHo"), 2: r(4, "okkkkkko"), 3: r(1, "oHHHHHHHHHHHHo"), 11: r(3, "onnnnnnnno")},
    "gauche": {1: r(6, "oHHHo"), 2: r(5, "okkkkko"), 3: r(2, "oHHHHHHHHHHHo"), 11: r(5, "onyynno")},
}

# Le bûcheron : barbe brune, chemise à carreaux rouges et noirs (c, k).
BUCHERON = {
    "bas": {6: r(3, "ohhhsshhho"), 7: r(4, "ohhhhhho"), 8: r(3, "oockckckoo"), 9: r(2, "oskckckckcso"),
            10: r(2, "osckckckckso"), 11: r(3, "okckckckco")},
    "haut": {8: r(3, "oockckckoo"), 9: r(2, "oskckckckcso"), 10: r(2, "osckckckckso"), 11: r(3, "okckckckco")},
    "gauche": {6: r(3, "ohhhhhhhho"), 7: r(4, "ohhhhhho"), 8: r(5, "ockckco"), 9: r(5, "okckcko"),
               10: r(5, "oskckco"), 11: r(5, "ockckco")},
}

# L'arbitre : chandail rayé noir et blanc (k, w), brassards orange (R).
ARBITRE = {
    "bas": {8: r(3, "oowkwkwkoo"), 9: r(2, "oRkwkwkwkwRo"), 10: r(2, "oskwkwkwkwso"), 11: r(3, "okwkwkwkwo")},
    "haut": {8: r(3, "oowkwkwkoo"), 9: r(2, "oRkwkwkwkwRo"), 10: r(2, "oskwkwkwkwso"), 11: r(3, "okwkwkwkwo")},
    "gauche": {8: r(5, "owkwkwo"), 9: r(5, "okwkwko"), 10: r(5, "oRwkwko"), 11: r(5, "okwkwko")},
}

# L'explorateur en canot : une feuille d'érable (R) sur le chapeau, la pagaie (n) à la main.
PAGAIE = {
    "bas": {3: r(4, "oAARRAAo"), **{i: (14, "n") for i in range(4, 11)}, 11: (13, "nnn"), 12: (13, "nnn"),
            13: (13, "nnn"), 14: (14, "n")},
    "haut": {**{i: (1, "n") for i in range(4, 11)}, 11: (0, "nnn"), 12: (0, "nnn"), 13: (0, "nnn"), 14: (1, "n")},
    "gauche": {3: (5, "oRAAAo"), **{i: (3, "n") for i in range(6, 11)}, 11: (2, "nnn"), 12: (2, "nnn"),
               13: (2, "nnn"), 14: (3, "n")},
}

# Le castor : brun, museau clair (m), deux grandes dents (w) ; de dos, sa queue plate (T).
CASTOR = {
    "bas": {4: r(3, "ohhhhhhhho"), 5: r(3, "ohhehhehho"), 6: r(3, "ohhmeemhho"), 7: r(4, "ohmwwmho"),
            9: r(2, "oscmmmmmmcso"), 10: r(2, "oscmmmmmmcso")},
    "haut": {12: r(4, "oTTTTTTo"), 13: r(4, "oTtTtTTo"), 14: r(4, "oTTtTtTo"), 15: r(5, "oooooo")},
    "gauche": {7: r(3, "owsssssso"), 11: r(5, "oCCCCCoTTTo")},
}

BRUN = "#8a5a32"
personnages(THEME, {
    "gestionnaire": ({**PERSONNAGES["gestionnaire"][0], "H": "#8b6a3e", "k": "#1d1d1d", "n": "#5c3b22",
                      "y": "#e0b04a", "c": ROUGE, "C": ROUGE_FONCE, "p": "#1c2a4a"}, [GENDARME]),
    "employe": ({**PERSONNAGES["employe"][0], "h": "#5a3a22", "c": ROUGE, "k": "#1d1d1d", "p": "#3a5a8a"},
                [BUCHERON]),
    "auditeur": ({"h": "#141414", "s": "#f0d2bc", "k": "#141414", "w": BLANC, "R": "#e8602a", "p": "#141414",
                  "C": "#141414"}, [ARBITRE]),
    "explorateur": ({**PERSONNAGES["explorateur"][0], "R": ROUGE, "n": "#a0703a"},
                    [*PERSONNAGES["explorateur"][1], PAGAIE]),
    "generique": ({"h": BRUN, "c": BRUN, "C": "#6e4626", "m": "#c89a6a", "s": "#c89a6a", "T": "#4a3020",
                   "t": "#6a4a30", "p": "#6e4626", "b": "#4a3020"}, [CASTOR]),
})

# ---------------------------------------------------------------------- décor
# Les murs blancs, la moulure rouge.

MURS = moulure("#f4f0ec", "#e8e0d8", ROUGE, ROUGE_FONCE)
recolorer(THEME, "mur", MURS)
recolorer(THEME, "mur-bas", MURS)
recolorer(THEME, "porte", MURS)
recolorer(THEME, "fenetre", MURS)

# Le cadre : une feuille d'érable rouge sur fond blanc, bandes rouges de chaque côté.
ecrire(THEME / "decor" / "cadre" / "image.png", [
    *[VIDE] * 3, r(3, "nnnnnnnnnn"), r(3, "nrrwwwwrrn"), r(3, "nrrwRRwrrn"), r(3, "nrrRRRRrrn"),
    r(3, "nrrwRRwrrn"), r(3, "nrrwwRwrrn"), r(3, "nrrwwwwrrn"), r(3, "nrrwwwwrrn"), r(3, "nnnnnnnnnn"),
    *[VIDE] * 4,
], {"n": "#6e4a2e", "r": ROUGE, "R": ROUGE, "w": BLANC})

# ------------------------------------------------- les objets propres au thème

FANIONS = {"r": ROUGE, "w": BLANC}

# Une guirlande de fanions rouges et blancs, aux deux coins du mur.
ecrire(THEME / "decor" / "coin" / "image.png", [
    VIDE, "llllllllllllllll", "rrr.www.rrr.www.", ".r...w...r...w..", *[VIDE] * 12,
], {"l": "#5c3b22", **FANIONS})


# Le drapeau du Canada sur son mât, 16 × 24 ; il claque au vent.
def drapeau(image: int) -> list[str]:
    toile = ["rrwwwwrr", "rrwwRwrr", "rrwRRRrr", "rrwwRwrr", "rrwwwwrr"]
    if image == 2:
        toile = [t[:6] + "." + t[7] if i % 2 else t for i, t in enumerate(toile)]
    return [r(4, "y"), *[r(4, "m" + t) for t in toile], *[r(4, "m")] * 16, r(3, "mmm"), VIDE]


for n in (1, 2):
    ecrire(THEME / "decor" / "drapeau" / f"vent-{n}.png", drapeau(n),
           {"y": "#e0b04a", "m": "#7a5230", "R": ROUGE, **FANIONS})

# Un gâteau blanc, une feuille d'érable rouge dessus.
ecrire(THEME / "decor" / "gateau" / "image.png", [
    *[VIDE] * 5, r(7, "y"), r(7, "w"), r(3, "oooooooooo"), r(3, "owwwRRwwwo"), r(3, "owwRRRRwwo"),
    r(3, "orrrrrrrro"), r(3, "owwwwwwwwo"), r(3, "orrrrrrrro"), r(2, "oppppppppppo"), r(2, "oooooooooooo"), VIDE,
], {"o": "#5c3b22", "w": BLANC, "R": ROUGE, "r": ROUGE, "y": "#ffd34a", "p": "#c8c8d0"})


# Un feu d'artifice rouge et blanc, qui monte, éclate et retombe.
def feu(image: int) -> list[str]:
    images = [
        [*[VIDE] * 12, r(7, "w"), r(7, "w"), r(7, "W"), VIDE],
        [*[VIDE] * 3, r(7, "w"), r(5, "w.w.w"), r(6, "www"), r(4, "wwwWwww"), r(6, "www"),
         r(5, "w.w.w"), r(7, "w"), *[VIDE] * 6],
        [VIDE, r(7, "r"), r(3, "r..r.r..r"), r(4, "r.r.r.r"), r(5, "r.w.r"), r(2, "rrr.wWw.rrr"),
         r(5, "r.w.r"), r(4, "r.r.r.r"), r(3, "r..r.r..r"), r(7, "r"), *[VIDE] * 6],
        [*[VIDE] * 2, r(3, "r.......r"), r(7, "w"), r(2, "r...w.w...r"), *[VIDE] * 2,
         r(2, "w.........w"), r(7, "r"), r(4, "w.....w"), *[VIDE] * 6],
    ]
    return images[image]


for i in range(4):
    ecrire(THEME / "decor" / "feu-artifice" / f"eclat-{i + 1}.png", feu(i),
           {"w": BLANC, "W": "#fff4b0", "r": ROUGE})
