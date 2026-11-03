"""Dessine le thème d'Halloween (octobre), dans themes/halloween/.

Usage : python outils/dessins_halloween.py

Même règle que dessins_initiaux.py : écrase les images existantes, et git
garde l'ancienne version. Ce qui n'est pas dessiné ici garde, en octobre, son
dessin de tous les jours (la plante carnivore, par exemple).
"""
from atelier import CHAPEAU_BROUSSE, COL, CRAVATE, PERSONNAGES, RACINE, ecrire, personnages, recolorer

THEME = RACINE / "themes" / "halloween"


# ---------------------------------------------------------------- personnages
# La mécanique (pose de base, puis rangées remplacées) est dans atelier.py.
# Chacun reste dans la logique de son rôle : le chef reste le chef, en veston
# et cravate orange ; l'auditeur, tout en noir ; l'explorateur, en beige.

# Le gestionnaire : une tête de citrouille sculptée, la lumière dans les yeux
# et la bouche (y), la queue verte (v). Le roi d'Halloween, en veston.
TETE_CITROUILLE = {
    "bas": {0: ".......vv.......", 1: ".....oovvoo.....", 2: "...ooqQqqQqoo...",
            3: "..oqqQqqqqQqqo..", 4: "..oqyyyQQyyyqo..", 5: "..oqqyqQQqyqqo..",
            6: "..oqyyyyyyyyqo..", 7: "...oqyqyyqyqo..."},
    "haut": {0: ".......vv.......", 1: ".....oovvoo.....", 2: "...ooqQqqQqoo...",
             3: "..oqqQqqqqQqqo..", 4: "..oqqQqqqqQqqo..", 5: "..oqqQqqqqQqqo..",
             6: "..oqqQqqqqQqqo..", 7: "...oqQqqqqQqo..."},
    "gauche": {0: "........v.......", 1: "......oovoo.....", 2: "....ooqqQqqoo...",
               3: "...oqqqQqqqQqo..", 4: "...oyyyqQqqQqo..", 5: "...oqyqqQqqQqo..",
               6: "...oyyyyQqqQqo..", 7: "....oqyyqqqQo..."},
}

# L'employé : un loup-garou. Oreilles pointues, museau (m), yeux jaunes (y),
# crocs (w) ; sa chemise bleue est déchirée et la fourrure (f) passe au travers.
TETE_LOUP = {
    "bas": {0: "...o........o...", 1: "..ofo......ofo..", 2: "..offooooooffo..",
            3: "..offffffffffo..", 4: "..offyffffyffo..", 5: "..offfmmmmfffo..",
            6: "...ofmmeemmfo...", 7: "....omwmmwmo....", 11: "...oCfCCCCfCo..."},
    "haut": {0: "...o........o...", 1: "..ofo......ofo..", 2: "..offooooooffo..",
             3: "..offffffffffo..", 4: "..offfFffFfffo..", 5: "..offffffffffo..",
             6: "...offFffFffo...", 7: "....offffffo....", 11: "...oCfCCCCfCo..."},
    "gauche": {0: "........o.......", 1: ".......ofo......", 2: ".....oooffoo....",
               3: "....offfffffo...", 4: "...offyffffffo..", 5: ".omfffffffffo...",
               6: ".oemmmffffffo...", 7: "..owmmmmffo.....", 11: ".....oCfCCCo...."},
}

# L'auditeur : un vampire lugubre. Teint blafard, cheveux en pointe sur le
# front, yeux rouges (r), crocs (w), cape noire (k) au col doublé de rouge (R).
VAMPIRE = {
    "bas": {4: "...ohsshhssho...", 5: "...ohsrssrsho...", 6: "..RohsssssshoR..",
            7: "..RRoswsswsoRR..", 8: "..kRocwttwcoRk..", 9: ".koscccttcccsok.",
            10: ".kosccccccccsok.", 11: ".kkoCCCCCCCCokk.", 12: ".kkkoppppppokkk.",
            13: "..kkoppooppokk.."},
    "haut": {6: "..RohhhhhhhhoR..", 7: "..RRohhhhhhoRR..", 8: "..kkkkkkkkkkkk..",
             9: ".kkkkkkkkkkkkkk.", 10: ".kkkkkkkkkkkkkk.", 11: ".kkkkkkkkkkkkkk.",
             12: ".kkkkkkkkkkkkkk.", 13: "..kkkkkkkkkkkk.."},
    "gauche": {5: "....osrsshhho...", 6: "...ossssshhhoR..", 7: "....oswssssoRR..",
               8: ".....occccokk...", 9: ".....occccokkk..", 10: ".....oscccokkkk.",
               11: ".....oCCCCokkkk."},
}

# L'explorateur : un zombie, sorti de la jungle avec son chapeau. Peau verdâtre
# (s, S), un œil vide (w), la bouche ouverte (m) ; sa chemise kaki délavée est
# déchirée, la peau passe par les trous, une tache de sang séché (r). De
# profil, il tend les bras devant lui.
ZOMBIE = {
    "bas": {5: "...ohswsseSho...", 6: "...ohsmwmwsho...", 7: "....osssSsso....",
            8: "...oocccsccoo...", 9: "..oscCcsccrcso..", 10: "..osccscccccso..",
            11: "...oCsCCsCCso..."},
    "haut": {9: "..oscccsccccso..", 11: "...oCsCCCCsCo..."},
    "gauche": {5: "....oswsshhho...", 6: "...omwsSshhho...", 8: "..ooooccccco....",
               9: "..osscccccco....", 10: "..ooooCcccco....", 11: ".....oCsCsCo...."},
}


# Le générique : un fantôme sous son drap, sans visage propre, comme il est
# sans allure propre. Il flotte : l'ourlet ondule d'une image à l'autre.
def fantome() -> dict:
    haut = ["................", "......oooo......", "....ooddddoo....", "...oddddddddo...",
            "...oddddddddo...", "..oddddddddddo..", "..oddddddddddo..", "..oddddddddddo..",
            "..oddddddddddo..", ".oddddddddddddo.", ".oddddddddddddo.", ".oDddddddddddDo.",
            ".oDddddddddddDo.", ".oDDDDDDDDDDDDo."]
    ourlets = [["..oDo.oDDo.oDo..", "...o...oo...o..."], ["..oDDo.oDo.oDo..", "...oo...o...o..."]]
    visage = {5: "..oddeeddeeddo..", 6: "..oddeeddeeddo..", 8: "..oddddeeddddo.."}
    cote = ["................", "......oooo......", ".....oddddoo....", "....oddddddo....",
            "...oddddddddo...", "...oeedddddddo..", "...oeedddddddo..", "...odddddddddo..",
            "...odddddddddo..", "...oddddddddddo.", "..oddddddddddDo.", "..oddddddddddDo.",
            "..oDdddddddddDo.", "..oDDDDDDDDDDDo."]
    ourlets_cote = [["...oDo.oDo.oDDo.", "....o...o...oo.."], ["..oDDo.oDo.oDo..", "...oo...o...o..."]]
    poses = {}
    for n in (0, 1):
        dos = haut + ourlets[n]
        face = [visage.get(i, r) for i, r in enumerate(dos)]
        poses[f"bas{n}"] = dict(enumerate(face))
        poses[f"haut{n}"] = dict(enumerate(dos))
        poses[f"gauche{n}"] = dict(enumerate(cote + ourlets_cote[n]))
    return poses


HALLOWEEN = {
    "gestionnaire": ({**PERSONNAGES["gestionnaire"][0], "q": "#e8822a", "Q": "#b85c1a",
                      "y": "#ffd34a", "v": "#4f7a2a"}, [TETE_CITROUILLE, CRAVATE]),
    "employe": ({**PERSONNAGES["employe"][0], "f": "#7a6450", "F": "#5a4838", "m": "#c8b49a",
                 "y": "#f2d23c", "s": "#7a6450"}, [TETE_LOUP, COL]),
    "auditeur": ({"h": "#141414", "s": "#d6dcd4", "r": "#c0202a", "R": "#8a1020", "k": "#0e0e0e",
                  "c": "#1c1c1c", "C": "#0e0e0e", "p": "#1c1c1c", "t": "#8a1020"}, [VAMPIRE]),
    "explorateur": ({**PERSONNAGES["explorateur"][0], "s": "#9cb27a", "S": "#6f8a55",
                     "c": "#c9b88e", "C": "#a8946a", "m": "#3a1f1a", "r": "#7a2a22"},
                    [CHAPEAU_BROUSSE, ZOMBIE]),
    "generique": ({"d": "#ecebf2", "D": "#b9b6cc"}, [fantome()]),
}

personnages(THEME, HALLOWEEN)


# ---------------------------------------------------------------------- décor
# La plupart des dessins de tous les jours sont repris et recolorés pour la
# nuit ; quelques-uns reçoivent un motif par-dessus (la lune à la fenêtre,
# une citrouille devant chaque maison).

# Les murs et les moulures, en violet sombre ; le plancher, en bois foncé.
MOULURE_NUIT = {"#f1e3c6": "#3e3150", "#e2cfa9": "#342a44", "#9c6b43": "#241c2e",
                "#6e4a2e": "#18121e", "#4a3424": "#100c14"}
recolorer(THEME, "sol", {"#e3c08d": "#5a4234", "#c49a66": "#3e2c22", "#d6b07b": "#6a4e3e"})
recolorer(THEME, "mur", MOULURE_NUIT)
recolorer(THEME, "mur-bas", MOULURE_NUIT)
recolorer(THEME, "porte", {**MOULURE_NUIT, "#b5523b": "#4a2a5a", "#8e3b2a": "#341c40"})

# La fenêtre : un ciel de nuit, un croissant de lune à gauche, une chauve-souris à droite.
LUNE = {"M": "#f4e8a0", "k": "#0e0a12"}
recolorer(THEME, "fenetre", {**MOULURE_NUIT, "#9fd3e6": "#1d2244", "#e3f5fb": "#2e3766"}, [
    (5, 3, [".MM.", "MM..", "MM..", ".MM."], LUNE),
    (20, 9, ["k...k", ".kkk."], LUNE),
])

# Le cadre : le même paysage, la nuit. Le soleil devient la lune, les collines, des ombres.
recolorer(THEME, "cadre", {**MOULURE_NUIT, "#bfe3f0": "#3a2e5c", "#6aa84f": "#141018", "#f2c14e": "#f4e8a0"})

# Le bois des bureaux, foncé ; la plaque et la pointe du stylo, orange. Les feuilles restent claires.
BUREAUX = {"#c8935a": "#6e4a36", "#9c6b43": "#4a3024", "#7a5230": "#3a2a22", "#e0b04a": "#e8822a"}
recolorer(THEME, "poste", BUREAUX)
recolorer(THEME, "bureau-gestionnaire", BUREAUX)
recolorer(THEME, "chaise", {"#3d4a5c": "#3a2a4a", "#5a6a80": "#54406a"})
# Le fauteuil du chef, en velours rouge sang.
recolorer(THEME, "fauteuil", {"#7a3e26": "#6a1424", "#9a5636": "#8a2034", "#4a2416": "#3a0a14"})
# Une fumée verdâtre, de chaudron.
recolorer(THEME, "cigare", {"#d8d8d8": "#a8d8a0", "#f4f4f4": "#c8f0c0"})
# Une araignée pend au-dessus de chaque photocopieuse.
recolorer(THEME, "photocopieuse", {}, [(11, 0, [".g.", ".g.", "kKk", "k.k"],
                                 {"g": "#c8c8c8", "k": "#0e0a12", "K": "#3a1a2a"})])
# Le chevalet en bois foncé, les crayons orange et violet. La feuille reste claire : la légende doit se lire.
recolorer(THEME, "pancarte", {"#7a5230": "#3a2a22", "#5c3b22": "#24180f", "#9c6b43": "#4a3024",
                       "#d0402f": "#e8822a", "#3b6fb6": "#6a3a8a"})

# La ville : un toit violet, des murs gris, la lumière orange aux fenêtres, une
# citrouille allumée devant chaque porte. L'herbe et la route, plus ternes.
CITROUILLE_PORCHE = ["..vv..", ".PPPP.", "PyPPyP", "PPyyPP", ".PPPP."]
recolorer(THEME, "maison", {"#c0503a": "#4e4060", "#96392a": "#3a2e4a", "#f0e0c0": "#a8a090",
                     "#d8c49c": "#8a8272", "#f6d365": "#ff9a2a", "#7a4a2a": "#3a2a2a"},
          [(12, 41, CITROUILLE_PORCHE, {"v": "#4f7a2a", "P": "#e8822a", "y": "#ffd34a"})])
recolorer(THEME, "herbe", {"#8cc06a": "#6a8a48", "#6fa452": "#4a6a34"})
recolorer(THEME, "route", {"#e8d5a0": "#a8987a", "#cdb67e": "#857560"})

# Un arbre mort, sans feuilles.
ecrire(THEME / "decor" / "arbre" / "image.png", [
    "................",
    "..t.........t...",
    "...t...t...t....",
    "t..t...t..t...t.",
    ".t.tt..t.tt..t..",
    "..t..t.t.t..t...",
    "...t..ttt..t....",
    "....tt.tt.t.....",
    "......ttttt.....",
    "......tTtt......",
    "......tTtt......",
    "......tTtt......",
    "......tTtt......",
    ".....ttTttt.....",
    "....tt.tT.tt....",
    "................",
], {"t": "#3a2a22", "T": "#24180f"})


# ------------------------------------------------- les objets propres au thème

# Une citrouille sculptée, posée par terre ; la flamme dedans vacille.
def citrouille() -> list[str]:
    return [*["................"] * 7,
            ".......vv.......",
            ".....oovvoo.....",
            "...ooqQqqQqoo...",
            "..oqqQqqqqQqqo..",
            "..oqyyqQQqyyqo..",
            "..oqqqqQQqqqqo..",
            "..oqyyyyyyyyqo..",
            "...oqyqyyqyqo...",
            "....oooooooo...."]


for n, flamme in enumerate(["#ffd34a", "#e8a030"], 1):
    ecrire(THEME / "decor" / "citrouille" / f"flamme-{n}.png", citrouille(),
           {"o": "#3b1d0a", "q": "#e8822a", "Q": "#b85c1a", "v": "#4f7a2a", "y": flamme})

# Une toile d'araignée dans chaque coin du plafond ; à droite, retournée.
TOILE = [
    "wwwwwwwwwwww....",
    "ww....w...w.....",
    "w.w...w..w......",
    "w..wwwwww.......",
    "w...w..w........",
    "ww..w.w.........",
    "w.w.ww..........",
    "w..ww...........",
    "wwww............",
    "w.w.............",
    "ww..............",
    "w...............",
    *["................"] * 4,
]
ecrire(THEME / "decor" / "coin-gauche" / "image.png", TOILE, {"w": "#c8c8d4"})
ecrire(THEME / "decor" / "coin-droit" / "image.png", [r[::-1] for r in TOILE], {"w": "#c8c8d4"})

# Une pierre tombale sur un monticule de terre, avec sa croix.
ecrire(THEME / "decor" / "tombe" / "image.png", [
    *["................"] * 4,
    ".....oooooo.....",
    "....oggggggo....",
    "...oggggggggo...",
    "...ogggGGgggo...",
    "...ogGGGGGGgo...",
    "...ogggGGgggo...",
    "...ogggGGgggo...",
    "...oggggggggo...",
    "...oggggggggo...",
    "..ommmmmmmmmmo..",
    ".ommmMmmmmMmmmo.",
    "................",
], {"o": "#2b2b30", "g": "#9a9aa4", "G": "#5a5a66", "m": "#5a4030", "M": "#3e2c20"})
