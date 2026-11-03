"""Dessine le thème de Noël (décembre), dans themes/noel/.

Usage : python outils/dessins_noel.py

Écrase les images existantes : git garde l'ancienne version. Ce qui n'est pas
dessiné ici garde, en décembre, son dessin de tous les jours.
"""
from atelier import (COL, FENETRE, CADRE, MAISON, PANCARTE, PERSONNAGES, RACINE,
                     VIDE, ecrire, moulure, neige, personnages, r, recolorer, sur)

THEME = RACINE / "themes" / "noel"

# ---------------------------------------------------------------- personnages
# Le chef devient le père Noël ; l'employé, un lutin ; l'auditeur, raide et
# sévère, un casse-noisette ; l'explorateur part au pôle en parka ; le
# générique, sans allure propre, un bonhomme de neige.

# Le père Noël : tuque rouge (R) à bordure blanche (W), cheveux et barbe blancs, ceinture noire.
PERE_NOEL = {
    "bas": {0: r(6, "oWWo"), 1: r(5, "oRRRRo"), 2: r(4, "oRRRRRRo"), 3: r(3, "oWWWWWWWWo"),
            4: r(3, "ohssssssho"), 5: r(3, "ohsessesho"), 6: r(3, "oWWWWWWWWo"), 7: r(4, "oWWWWWWo"),
            8: r(3, "oocWWWWcoo"), 11: r(3, "okkkyykkko")},
    "haut": {0: r(6, "oWWo"), 1: r(5, "oRRRRo"), 2: r(4, "oRRRRRRo"), 3: r(3, "oWWWWWWWWo"),
             11: r(3, "okkkyykkko")},
    "gauche": {0: r(6, "oWWo"), 1: r(5, "oRRRRo"), 2: r(5, "oRRRRRRo"), 3: r(4, "oWWWWWWWWo"),
               6: r(2, "oWWWWWshhho"), 7: r(3, "oWWWWsso"), 8: r(4, "oWWcccco"), 11: r(5, "okyykko")},
}

# Le lutin : bonnet vert (G) à grelot (y) et bande rouge, oreilles pointues, tunique verte.
LUTIN = {
    "bas": {0: r(10, "oyo"), 1: r(6, "ooooGo"), 2: r(4, "oGGGGGGo"), 3: r(3, "orrrrrrrro"),
            4: r(1, "osohhsssshhoso")},
    "haut": {0: r(10, "oyo"), 1: r(6, "ooooGo"), 2: r(4, "oGGGGGGo"), 3: r(3, "orrrrrrrro"),
             4: r(1, "osohhhhhhhhoso")},
    "gauche": {0: r(10, "oyo"), 1: r(7, "ooGGo"), 2: r(5, "oGGGGGGo"), 3: r(4, "orrrrrrrro"),
               4: r(4, "osshhhhhoso")},
}

# Le casse-noisette : grand bonnet noir (k) à bande dorée (y), joues roses (S),
# moustache et mâchoire blanches, veste rouge à boutons dorés.
CASSE_NOISETTE = {
    "bas": {0: r(5, "oooooo"), 1: r(4, "okkkkkko"), 2: r(4, "okkkkkko"), 3: r(3, "oyyyyyyyyo"),
            4: r(3, "osesssseso"), 5: r(3, "oSssssssSo"), 6: r(3, "owwwwwwwwo"), 7: r(4, "owwkkwwo"),
            8: r(3, "ooyccccyoo"), 9: r(2, "oscccyycccso"), 10: r(2, "oscccyycccso"),
            11: r(3, "okkkyykkko")},
    "haut": {0: r(5, "oooooo"), 1: r(4, "okkkkkko"), 2: r(4, "okkkkkko"), 3: r(3, "oyyyyyyyyo"),
             11: r(3, "okkkyykkko")},
    "gauche": {0: r(6, "ooooo"), 1: r(5, "okkkkko"), 2: r(5, "okkkkko"), 3: r(4, "oyyyyyyyo"),
               5: r(4, "osesShhho"), 6: r(3, "owwwwshhho"), 7: r(3, "owwkwsso"), 11: r(5, "okyykko")},
}

# L'explorateur polaire : capuchon de parka beige bordé de fourrure (F), foulard rouge.
PARKA = {
    "bas": {1: r(4, "oooooooo"), 2: r(3, "oaaaaaaaao"), 3: r(2, "oaFFFFFFFFao"), 4: r(2, "oaFhsssshFao"),
            5: r(2, "oaFsessesFao"), 6: r(2, "oaFssssssFao"), 7: r(3, "oaFFFFFFao"),
            8: r(3, "oorrrrrroo"), 9: r(2, "osccrcccccso")},
    "haut": {1: r(4, "oooooooo"), 2: r(3, "oaaaaaaaao"), 3: r(2, "oaaaaaaaaaao"), 4: r(2, "oaaaaaaaaaao"),
             5: r(2, "oaaaaaaaaaao"), 6: r(2, "oaaaaaaaaaao"), 7: r(3, "oaaaaaaaao"), 8: r(3, "oorrrrrroo")},
    "gauche": {1: r(5, "ooooooo"), 2: r(4, "oaaaaaaao"), 3: r(3, "oFFFFFaaaao"), 4: r(3, "oFsssFaaaao"),
               5: r(3, "oFessFaaaao"), 6: r(3, "oFsssFaaaao"), 7: r(3, "oFFFFFaaao"), 8: r(5, "orrrrro")},
}


# Le bonhomme de neige : chapeau noir, nez-carotte (n), foulard rouge ; il glisse, sans jambes.
def bonhomme() -> dict:
    chapeau = [r(5, "oooooo"), r(5, "okkkko"), r(5, "okkkko"), r(3, "okkkkkkkko")]
    corps = [r(3, "orrrrrrrro"), r(2, "odddddddrddo"), r(1, "odddddeddddddo"), r(1, "oddddddddddddo"),
             r(1, "odddddeddddddo"), r(1, "oDddddddddddDo"), r(2, "oDDDDDDDDDDo"), r(3, "oooooooooo")]
    face = chapeau + [r(4, "oddddddo"), r(3, "oddeddeddo"), r(3, "odddnndddo"), r(4, "oddeeddo")] + corps
    dos = chapeau + [r(4, "oddddddo"), r(3, "oddddddddo"), r(3, "oddddddddo"), r(4, "oddddddo")] + \
        [r(3, "orrrrrrrro")] + [c.replace("e", "d") for c in corps[1:]]
    cote = [r(6, "oooooo"), r(6, "okkkko"), r(6, "okkkko"), r(4, "okkkkkkkko"), r(5, "oddddddo"),
            r(4, "odeddddddo"), r(2, "nnoddddddddo"), r(5, "oddddddo")] + \
        [r(3, "orrrrrrrro")] + [c.replace("e", "d") for c in corps[1:]]
    poses = {}
    for n in (0, 1):
        poses[f"bas{n}"] = dict(enumerate(face))
        poses[f"haut{n}"] = dict(enumerate(dos))
        poses[f"gauche{n}"] = dict(enumerate(cote))
    return poses


personnages(THEME, {
    "gestionnaire": ({**PERSONNAGES["gestionnaire"][0], "R": "#c8202a", "W": "#f4f4f4", "h": "#f4f4f4",
                      "c": "#c8202a", "C": "#9a1820", "p": "#c8202a", "k": "#1d1d1d", "y": "#e0b04a"},
                     [PERE_NOEL]),
    "employe": ({"h": "#b5612a", "s": "#f0c8a8", "G": "#2e8b3e", "r": "#c8202a", "y": "#e0b04a",
                 "c": "#2e8b3e", "C": "#1f6a2c", "p": "#c8202a"}, [LUTIN, COL]),
    "auditeur": ({"h": "#141414", "s": "#f0d2bc", "S": "#e88a8a", "k": "#141414", "y": "#e0b04a",
                  "c": "#c8202a", "C": "#9a1820", "p": "#1c1c1c"}, [CASSE_NOISETTE]),
    "explorateur": ({**PERSONNAGES["explorateur"][0], "a": "#d8c49a", "F": "#f4f0e8", "r": "#c8202a"},
                    [PARKA]),
    "generique": ({"d": "#f4f6fa", "D": "#c8d0dc", "k": "#1d1d1d", "n": "#e8822a", "r": "#c8202a"},
                  [bonhomme()]),
})

# ---------------------------------------------------------------------- décor
# Les murs vert sapin, la moulure rouge. Dehors, la neige.

MURS = moulure("#2e5a3a", "#264d31", "#8a1c24", "#5e1218")
recolorer(THEME, "mur", MURS)
recolorer(THEME, "mur-bas", MURS)
recolorer(THEME, "porte", MURS)

# La fenêtre : la nuit, les flocons, la neige sur le rebord.
FLOCONS = {"f": "#f4f6fa"}
recolorer(THEME, "fenetre", {**MURS, FENETRE["g"]: "#3a4a6a", FENETRE["l"]: "#4a5a80"}, [
    (4, 3, ["f....f.....", "...f.....f.", ".f.....f...", "....f.....f"], FLOCONS),
    (18, 8, ["f....f....", "...f....f.", ".f.....f.."], FLOCONS),
    (1, 13, ["f" * 29], FLOCONS),
])
# Le cadre : le même paysage, sous la neige.
recolorer(THEME, "cadre", {**MURS, CADRE["g"]: "#cfe0ee", CADRE["v"]: "#f4f6fa", CADRE["y"]: "#f8f0c8"})
recolorer(THEME, "pancarte", {PANCARTE["u"]: "#2e8b3e"})

# La ville sous la neige : la neige sur les toits, une guirlande de lumières
# sous le toit, une couronne sur la porte.
neige(THEME)
LUMIERES = {"r": "#e8402a", "g": "#3fbf5a", "y": "#ffd34a", "b": "#4a8ae8", "G": "#2e6b2e", "R": "#c8202a"}
recolorer(THEME, "maison", {MAISON["R"]: "#f4f6fa", MAISON["r"]: "#d0dbe6", MAISON["Y"]: "#ffd890"}, [
    (6, 25, ["r.g.y.b." * 4 + "r.g."], LUMIERES),
    (22, 35, [".GGG.", "GG.GG", "G...G", "GG.GG", ".GRG."], LUMIERES),
])

# Le sapin enneigé, à la place de l'arbre.
ecrire(THEME / "decor" / "arbre" / "image.png", [
    r(7, "W"), r(6, "WvW"), r(5, "vvWvv"), r(4, "VvvvvvV"), r(5, "WWvWW"), r(4, "vvvvvvv"),
    r(3, "VvvWvvvvV"), r(4, "WWWvWWW"), r(3, "vvvvvvvvv"), r(2, "VvvvvWvvvvV"), r(3, "WWWWWWWWW"),
    r(2, "VVVVVVVVVVV"), r(7, "tt"), r(7, "tt"), r(4, "WWWWWWWW"), VIDE,
], {"v": "#2f6b33", "V": "#1f4a24", "W": "#f4f6fa", "t": "#5c3820"})

# ------------------------------------------------- les objets propres au thème

# Le sapin décoré, 16 × 24 : les boules clignotent, l'étoile reste allumée.
def sapin(image: int) -> list[str]:
    boules = "rbyg" if image == 1 else "gyrb"
    lignes = [r(7, "yy"), r(6, "yYYy"), r(7, "yy"), r(7, "vv"), r(6, "vvvv"), r(5, "vv1vvv"),
              r(5, "vvvvvv"), r(4, "vvvv2vvv"), r(3, "VvvvvvvvvV"), r(4, "v3vvvvvv"),
              r(3, "vvvvvv4vvv"), r(2, "VvvvvvvvvvvV"), r(3, "vv1vvvvvvv"), r(2, "vvvvvvv2vvvv"),
              r(1, "VvvvvvvvvvvvvV"), r(1, "vvv3vvvvvv4vvv"), r(0, "VvvvvvvvvvvvvvvV"),
              r(0, "VVVVVVVVVVVVVVVV"), r(7, "tt"), r(7, "tt"), r(5, "pppppp"), r(5, "PPPPPP"),
              VIDE, VIDE]
    return [l.replace("1", boules[0]).replace("2", boules[1]).replace("3", boules[2]).replace("4", boules[3])
            for l in lignes]


SAPIN = {"y": "#ffd34a", "Y": "#fff4b0", "v": "#2f8b3a", "V": "#1f6a2c", "t": "#5c3820",
         "r": "#e8402a", "b": "#4a8ae8", "g": "#f4f4f4", "p": "#c8202a", "P": "#9a1820", "W": "#f4f6fa"}


# Sa pose2, à l'emplacement de la plante : la neige tombe doucement autour,
# un pixel par image. Chaque flocon (colonne, décalage) repasse toutes les
# 8 rangées ; il passe derrière le sapin. 8 images : les boules clignotent
# toujours une image sur deux.
FLOCONS = [(0, 0), (2, 5), (4, 2), (11, 6), (13, 3), (15, 1)]


def sapin_neige(image: int) -> list[str]:
    lignes = sapin(2 - image % 2)
    for x, decalage in FLOCONS:
        for y in range(len(lignes)):
            if (y - decalage - image) % 8 == 0 and lignes[y][x] == ".":
                lignes[y] = sur(lignes[y], x, "W")
    return lignes


for n in (1, 2):
    ecrire(THEME / "decor" / "sapin-noel" / f"lumieres-{n}.png", sapin(n), SAPIN)
    ecrire(THEME / "decor" / "plante" / f"lumieres-{n}.png", sapin(n), SAPIN)
for n in range(1, 9):
    ecrire(THEME / "decor" / "plante" / f"pose2-lumieres-{n}.png", sapin_neige(n), SAPIN)

# Un cadeau emballé, ruban doré.
ecrire(THEME / "decor" / "cadeau" / "image.png", [
    *[VIDE] * 6, r(5, "yy.yy"), r(6, "yyy"), r(3, "oooooyoooo"), r(3, "oRRRRyRRRo"), r(3, "oRRRRyRRRo"),
    r(3, "oyyyyyyyyo"), r(3, "oRRRRyRRRo"), r(3, "oRRRRyRRRo"), r(3, "oRRRRyRRRo"), r(3, "oooooooooo"),
], {"o": "#3a1010", "R": "#c8202a", "y": "#e0b04a"})

# Une couronne de sapin aux deux coins du mur, ruban rouge.
ecrire(THEME / "decor" / "coin" / "image.png", [
    VIDE, r(5, "oGGGGo"), r(4, "GGvGGvGG"), r(3, "GvG....GvG"), r(3, "GG......GG"), r(3, "Gr......rG"),
    r(3, "GG......GG"), r(3, "GvG....GvG"), r(4, "GGvRRvGG"), r(5, "oRRRRo"), r(6, "R..R"), r(6, "R..R"),
    *[VIDE] * 4,
], {"o": "#1f4a24", "G": "#2f8b3a", "v": "#1f6a2c", "r": "#e8402a", "R": "#c8202a"})
