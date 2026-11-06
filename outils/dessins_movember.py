"""Dessine le thème de Movember (novembre), dans themes/movember/.

Usage : python outils/dessins_movember.py

Écrase les images existantes : git garde l'ancienne version. Ce qui n'est pas
dessiné ici garde, en novembre, son dessin de tous les jours.
"""
from atelier import (ARBRE, COL, CRAVATE, FENETRE, HERBE, MAISON, PERSONNAGES, RACINE, ROUTE, VIDE, ecrire,
                     moulure, personnages, r, recolorer)

THEME = RACINE / "themes" / "movember"

# ---------------------------------------------------------------- personnages
# Le bureau devient un salon de barbier, et chacun a sa moustache (M). Le chef
# porte la plus grande ; l'employé, celui qui travaille, est le barbier ;
# l'auditeur, autorité sévère, est un vieux colonel ; l'explorateur a laissé
# pousser la sienne en brousse ; le générique a la grosse moustache de morse.
# À 16 pixels, une moustache se lit à sa silhouette : elle déborde du visage.

# Les yeux remontent d'un pixel : une ligne de peau les sépare de la moustache,
# sinon les deux se fondent en une seule bande foncée.
YEUX = {
    "bas": {4: "...ohsessesho...", 5: "...ohssssssho..."},
    "haut": {},
    "gauche": {4: "....osesshhho...", 5: "....osssshhho..."},
}

# Le gestionnaire : la moustache en guidon, plus large que sa tête, les pointes relevées.
GUIDON = {
    "bas": {4: (1, "M............M"), 5: (1, "MM..........MM"), 6: (2, "MMMMMMMMMMMM"), 7: (6, "MMMM")},
    "haut": {5: (1, "M............M"), 6: (1, "MMM........MMM")},
    "gauche": {4: (1, "M"), 5: (1, "MM"), 6: (2, "MMMMMM"), 7: (4, "MMM")},
}

# L'employé : la moustache courte aux bouts retroussés, le tablier blanc (T), les ciseaux (S) en poche.
TABLIER = {
    "bas": {5: (3, "M........M"), 6: (3, "MMMMMMMMMM"), 7: (5, "MM..MM"),
            9: (5, "TTTTTT"), 10: (5, "TTSTST"), 11: (5, "TTTSTT")},
    "haut": {},
    "gauche": {5: (2, "M"), 6: (2, "MMMMM"), 7: (5, "MM"), 9: (6, "TTTT"), 10: (6, "TTTT"), 11: (6, "TTTT")},
}

# L'auditeur : casquette d'officier (N), visière (k), insigne doré (y), moustache
# grise tombante et médailles sur l'uniforme.
COLONEL = {
    "bas": {1: r(4, "oooooooo"), 2: r(3, "oNNNNNNNNo"), 3: r(3, "oNNNyyNNNo"), 4: r(3, "okkkkkkkko"),
            6: (4, "MMMMMMMM"), 7: (4, "MM....MM"), 8: (4, "M......M"), 9: (9, "yR")},
    "haut": {1: r(4, "oooooooo"), 2: r(3, "oNNNNNNNNo"), 3: r(3, "oNNNNNNNNo")},
    "gauche": {1: r(5, "ooooooo"), 2: r(4, "oNNNNNNNo"), 3: r(4, "oNNyNNNNo"), 4: r(2, "okkkkhhhhho"),
               6: (3, "MMMMM"), 7: (4, "MMM"), 8: (5, "M")},
}

# L'explorateur : sa tenue et son chapeau, plus une moustache rousse en fer à cheval.
FER_A_CHEVAL = {
    "bas": {6: (5, "MMMMMM"), 7: (5, "M....M"), 8: (5, "M....M")},
    "haut": {},
    "gauche": {6: (4, "MMMM"), 7: (5, "M"), 8: (6, "M")},
}

# Le générique : chauve, pour que rien ne se confonde avec sa grosse moustache
# de morse, touffue, qui tombe de chaque côté de la bouche.
MORSE = {
    "bas": {6: (4, "MMMMMMMM"), 7: (3, "MMMMMMMMMM"), 8: (3, "MM......MM"), 9: (3, "M........M")},
    "haut": {},
    "gauche": {6: (3, "MMMMM"), 7: (2, "MMMMM"), 8: (2, "MM"), 9: (2, "M")},
}

NOIR, GRIS = "#1c1c1c", "#c8c8c8"
personnages(THEME, {
    "gestionnaire": ({**PERSONNAGES["gestionnaire"][0], "M": NOIR, "t": "#6fb3e0"},
                     [CRAVATE, YEUX, GUIDON]),
    "employe": ({**PERSONNAGES["employe"][0], "M": NOIR, "T": "#f4f4f4", "S": "#6a7482"},
                [COL, YEUX, TABLIER]),
    "auditeur": ({"h": "#b8b8b8", "s": "#f0d2bc", "c": "#3d4f63", "C": "#2f3e50", "p": "#2f3e50", "M": GRIS,
                  "N": "#2f3e50", "k": "#141414", "y": "#e0b04a", "R": "#c0503a"}, [COLONEL]),
    "explorateur": ({**PERSONNAGES["explorateur"][0], "M": "#c8632a"},
                    [*PERSONNAGES["explorateur"][1], FER_A_CHEVAL]),
    "generique": ({**PERSONNAGES["generique"][0], "h": PERSONNAGES["generique"][0]["s"], "M": NOIR},
                  [*PERSONNAGES["generique"][1], YEUX, MORSE]),
})

# ---------------------------------------------------------------------- décor
# Les murs gris-bleu de novembre, la moulure crème d'un salon de barbier.
# Dehors, le ciel gris, des feuilles qui tombent et des arbres couleur de rouille.

MURS = moulure("#7f97ad", "#6f879d", "#e8e4da", "#b8b2a4")
recolorer(THEME, "mur", MURS)
recolorer(THEME, "mur-bas", MURS)
recolorer(THEME, "porte", MURS)

FEUILLE = {"f": "#c8632a", "F": "#e0a03a"}
recolorer(THEME, "fenetre", {**MURS, FENETRE["g"]: "#b4c0c8", FENETRE["l"]: "#d0d8de"}, [
    (6, 4, ["f.", "ff"], FEUILLE), (11, 8, [".F", "FF"], FEUILLE),
    (21, 5, [".f", "ff"], FEUILLE), (26, 9, ["F.", "FF"], FEUILLE),
])

# Le portrait au mur : un ancêtre moustachu.
PORTRAIT = {"K": "#efe6d2", "H": "#3a2415", "S": "#e8b996", "e": "#2b1d16", "M": "#1c1c1c", "c": "#2f3e5c"}
recolorer(THEME, "cadre", MURS, [(4, 4, [
    "KKHHHHKK",
    "KHSSSSHK",
    "KSeSSeSK",
    "MMMMMMMM",
    "M.SSSS.M",
    "KcccccKK",
    "cccccccc",
], {**PORTRAIT, ".": "#efe6d2"})])

# La grande moustache de novembre : au-dessus de la porte des maisons, et aux coins du mur.
MOUSTACHE = [
    "..MM........MM..",
    ".M..M......M..M.",
    ".M............M.",
    ".MM..MM..MM..MM.",
    "..MMMMMMMMMMMM..",
    "...MMMMMMMMMM...",
    "....MMM..MMM....",
]
NOIR = {"M": "#1c1c1c"}

# La ville : les fenêtres font des yeux, la porte une bouche, et chaque maison a sa moustache.
recolorer(THEME, "maison", {MAISON["R"]: "#4a5a70", MAISON["r"]: "#364456"}, [(16, 25, MOUSTACHE, NOIR)])
recolorer(THEME, "herbe", {HERBE["g"]: "#8a9a62", HERBE["G"]: "#6e7f4e"})
recolorer(THEME, "route", {ROUTE["s"]: "#c4b490", ROUTE["S"]: "#a8987a"})
recolorer(THEME, "arbre", {ARBRE["v"]: "#b8722e", ARBRE["V"]: "#8a4f1e"})

# ------------------------------------------------- les objets propres au thème

# À la place de la plante : un fauteuil de barbier en cuir rouge, sur son pied de chrome.
ecrire(THEME / "decor" / "plante" / "image.png", [
    VIDE,
    r(6, "oooo"),
    r(5, "oRRRRo"),
    r(5, "orRRro"),
    r(6, "oAAo"),
    r(4, "oooooooo"),
    r(3, "oRRRRRRRRo"),
    r(3, "oRrRRRRrRo"),
    r(3, "oRRRRRRRRo"),
    r(3, "oRrRRRRrRo"),
    r(3, "oRRRRRRRRo"),
    r(3, "oRrRRRRrRo"),
    r(1, "oooRRRRRRRRooo"),
    r(1, "oAAoRRRRRRoAAo"),
    r(1, "oAaorrrrrroaAo"),
    r(1, "oooooooooooooo"),
    r(3, "oRRRRRRRRo"),
    r(3, "orrrrrrrro"),
    r(4, "oooooooo"),
    r(6, "oAao"),
    r(6, "oAao"),
    r(3, "oooAAAaaooo"),
    r(2, "oAAAAAAaaaao"),
    r(2, "oooooooooooo"),
], {"o": "#2b2b30", "R": "#b8342a", "r": "#8e2620", "A": "#d4dae2", "a": "#8a92a0"})

# Une grande moustache accrochée aux deux coins du mur, comme un trophée.
ecrire(THEME / "decor" / "coin" / "image.png", [
    VIDE,
    VIDE,
    *MOUSTACHE,
    *[VIDE] * 7,
], NOIR)

# Des feuilles mortes dans l'herbe.
ecrire(THEME / "decor" / "feuilles" / "image.png", [
    *[VIDE] * 8, r(2, "ff.......F"), r(2, "fff.....FFF"), r(3, "f.......F"), r(6, "FF"), r(5, "FFF.....ff"),
    r(11, "ffff"), r(1, "f"), VIDE,
], FEUILLE)


# Le poteau de barbier : ses bandes rouges, blanches et bleues montent sans fin.
def poteau(image: int) -> list[str]:
    bandes = "RRWBBW"
    tube = [r(5, "o" + "".join(bandes[(x + y + image) % 6] for x in range(4)) + "o") for y in range(14)]
    return [r(6, "oooo"), r(5, "oAAAAo"), r(4, "oAAAAAAo"), r(4, "oooooooo"), *tube, r(4, "oooooooo"),
            r(4, "oAAAAAAo"), r(5, "oAAAAo"), r(3, "oAAAAAAAAo"), r(3, "oooooooooo"), VIDE]


for n in range(6):
    ecrire(THEME / "decor" / "poteau-barbier" / f"tourne-{n + 1}.png", poteau(5 - n),
           {"o": "#2b2b30", "A": "#b8bec8", "R": "#d0402f", "W": "#f4f4f4", "B": "#3b6fb6"})
