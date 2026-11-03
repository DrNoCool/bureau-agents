"""Dessine le thème de la Saint-Patrick (mars), dans themes/saint-patrick/.

Usage : python outils/dessins_saint_patrick.py

Écrase les images existantes : git garde l'ancienne version. Ce qui n'est pas
dessiné ici garde, en mars, son dessin de tous les jours.
"""
from atelier import (COL, FENETRE, HERBE, PERSONNAGES, RACINE, VIDE, ecrire, moulure, personnages, r,
                     recolorer)

THEME = RACINE / "themes" / "saint-patrick"

# ---------------------------------------------------------------- personnages
# Le chef devient le farfadet, gardien de l'or, sa barbe orange comme la
# cravate de tous les jours ; l'employé porte le chapeau melon vert ;
# l'auditeur, autorité sévère, devient saint Patrick lui-même, en évêque ;
# l'explorateur a trouvé le chaudron d'or ; le générique s'habille en vert.

# Le farfadet : haut-de-forme vert (G) à boucle dorée (y), cheveux et barbe orange (h).
FARFADET = {
    "bas": {0: r(5, "oooooo"), 1: r(5, "oGGGGo"), 2: r(5, "okyyko"), 3: r(3, "oGGGGGGGGo"),
            6: r(3, "ohhhhhhhho"), 7: r(4, "ohhhhhho"), 8: r(3, "oochhhhcoo")},
    "haut": {0: r(5, "oooooo"), 1: r(5, "oGGGGo"), 2: r(5, "okkkko"), 3: r(3, "oGGGGGGGGo")},
    "gauche": {0: r(6, "ooooo"), 1: r(6, "oGGGo"), 2: r(6, "okyko"), 3: r(4, "oGGGGGGGGo"),
               6: r(3, "ohhhhhhhho"), 7: r(4, "ohhhhhho"), 8: r(5, "ohhccco")},
}

# L'employé : chapeau melon vert, un trèfle (T) sur la chemise.
MELON = {
    "bas": {1: r(5, "oooooo"), 2: r(4, "oGGGGGGo"), 3: r(2, "oGGGGGGGGGGo"), 9: r(2, "oscTcccccccso")},
    "haut": {1: r(5, "oooooo"), 2: r(4, "oGGGGGGo"), 3: r(2, "oGGGGGGGGGGo")},
    "gauche": {1: r(6, "ooooo"), 2: r(5, "oGGGGGo"), 3: r(3, "oGGGGGGGGGo")},
}

# Saint Patrick : mitre verte (G) à croix dorée (y), barbe blanche, robe verte, la crosse dorée.
EVEQUE = {
    "bas": {0: r(7, "oo"), 1: r(6, "oGGo"), 2: r(5, "oGyyGo"), 3: r(3, "ohGGyyGGho"), 4: r(3, "ohssssssho"),
            6: r(3, "owwwsswwwo"), 7: r(4, "owwwwwwo"), 8: r(3, "oocwwwwcoo")},
    "haut": {0: r(7, "oo"), 1: r(6, "oGGo"), 2: r(5, "oGGGGo"), 3: r(3, "ohGGGGGGho")},
    "gauche": {0: r(7, "oo"), 1: r(6, "oGGo"), 2: r(5, "oGyyGo"), 3: r(4, "ohGGyGGho"),
               6: r(2, "owwwwwshhho"), 7: r(3, "owwwwsso"), 8: r(4, "owwccco")},
}
# La crosse, posée par-dessus, à droite ; de profil, elle est cachée derrière.
CROSSE = [(13, "yyy"), (13, "y.y"), (15, "y")] + [(15, "y")] * 13
CROSSE = {d: dict(enumerate(CROSSE)) for d in ("bas", "haut")}

# L'explorateur : le chaudron noir (k) plein d'or (y) dans les bras, un ruban vert au chapeau.
CHAUDRON = {
    "bas": {9: r(2, "oscyyyyyycso"), 10: r(2, "osckkkkkkcso"), 11: r(3, "oCkkkkkkCo")},
    "haut": {},
    "gauche": {9: r(2, "yyyocccco"), 10: r(2, "kkkoscccco"), 11: r(3, "kkoCCCCCo")},
}

# Le générique : chandail vert, un trèfle (T) dessus.
TREFLE_POITRINE = {
    "bas": {9: r(2, "oscccTTcccso"), 10: r(2, "osccccTcccso")},
    "haut": {},
    "gauche": {9: r(5, "oTcccco")},
}

VERT, VERT_FONCE = "#2e8b3e", "#1f6a2c"
personnages(THEME, {
    "gestionnaire": ({**PERSONNAGES["gestionnaire"][0], "G": VERT, "k": "#141414", "y": "#e0b04a",
                      "h": "#d97757", "c": VERT, "C": VERT_FONCE, "p": VERT_FONCE}, [FARFADET]),
    "employe": ({**PERSONNAGES["employe"][0], "G": VERT_FONCE, "c": "#7cc86a", "C": "#5fae4a", "T": VERT_FONCE},
                [MELON, COL]),
    "auditeur": ({"h": "#e8e8e8", "s": "#f0d2bc", "G": VERT, "y": "#e0b04a", "c": VERT, "C": VERT_FONCE,
                  "p": VERT_FONCE}, [EVEQUE, CROSSE]),
    "explorateur": ({**PERSONNAGES["explorateur"][0], "A": VERT, "k": "#1d1d1d", "y": "#ffd34a"},
                    [*PERSONNAGES["explorateur"][1], CHAUDRON]),
    "generique": ({**PERSONNAGES["generique"][0], "c": "#3fae4a", "C": VERT, "T": "#f4f4f4"},
                  [*PERSONNAGES["generique"][1], TREFLE_POITRINE]),
})

# ---------------------------------------------------------------------- décor
# Les murs vert pomme, la moulure dorée. Dehors, le printemps et un arc-en-ciel.

MURS = moulure("#4a9a5a", "#3e8a4c", "#c8a040", "#8a6a2a")
recolorer(THEME, "mur", MURS)
recolorer(THEME, "mur-bas", MURS)
recolorer(THEME, "porte", MURS)
ARC = {"r": "#e8402a", "o": "#f0902a", "y": "#ffd34a", "g": "#3fbf5a", "b": "#4a8ae8"}
recolorer(THEME, "fenetre", MURS, [
    (17, 3, ["..rrrrrrr..", ".rooooooor.", "royyyyyyyor", "oyg.....gyo"], ARC),
])
recolorer(THEME, "herbe", {HERBE["g"]: "#7cc85a", HERBE["G"]: "#5fae4a"})
TREFLE_PORTE = {"T": "#2e8b3e"}
recolorer(THEME, "maison", {}, [(22, 35, [".T.", "TTT", ".T."], TREFLE_PORTE)])

# ------------------------------------------------- les objets propres au thème

# Un grand trèfle aux deux coins du mur.
TREFLE = [VIDE, r(4, "oo..oo"), r(3, "oTTooTTo"), r(3, "oTTTTTTo"), r(4, "oTTTTo"), r(3, "oTTTTTTo"),
          r(3, "oTTooTTo"), r(4, "oo.too"), r(7, "t"), r(6, "t"), *[VIDE] * 6]
ecrire(THEME / "decor" / "coin" / "image.png", TREFLE, {"o": "#1f5a2a", "T": "#3fae4a", "t": "#2e8b3e"})

# Des trèfles dans l'herbe.
ecrire(THEME / "decor" / "trefles" / "image.png", [
    *[VIDE] * 8, r(2, "T.T.......T.T"), r(3, "T.........T"), r(2, "T.T..T.T..T.T"), r(3, "t....T....t"),
    r(5, "t.T.T"), r(7, "t"), VIDE, VIDE,
], {"T": "#2e8b3e", "t": "#1f6a2c"})


# Le chaudron d'or ; une pièce brille en haut, puis une autre.
def pot(image: int) -> list[str]:
    or_ = r(4, "yYyyyyYy") if image == 1 else r(4, "yyyYyyyy")
    return [*[VIDE] * 6, r(5, "y..Y.."), r(3, "oyyyyyyyyo"), or_, r(3, "okkkkkkkko"), r(2, "okkkkkkkkkko"),
            r(2, "okkkkkkkkkko"), r(2, "okkkkkkkkkko"), r(3, "okkkkkkkko"), r(3, "oo.oooo.oo"), VIDE]


for n in (1, 2):
    ecrire(THEME / "decor" / "pot-or" / f"brille-{n}.png", pot(n),
           {"o": "#0e0e0e", "k": "#2b2b30", "y": "#e0b04a", "Y": "#fff4b0"})
