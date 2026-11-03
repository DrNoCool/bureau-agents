"""Dessine les images de départ du bureau, en PNG, à leur taille réelle.

Usage : python outils/dessins_initiaux.py

Écrase les images existantes, même celles remplacées à la main (ChatGPT ou
autres) : git garde l'ancienne version.
"""
from pathlib import Path

from PIL import Image

RACINE = Path(__file__).resolve().parent.parent


def ecrire(chemin: Path, grille: list[str], palette: dict[str, str]) -> None:
    largeur = len(grille[0])
    for i, rangee in enumerate(grille):
        assert len(rangee) == largeur, f"{chemin} : rangée {i} de {len(rangee)} pixels au lieu de {largeur}"
    img = Image.new("RGBA", (largeur, len(grille)), (0, 0, 0, 0))
    for y, rangee in enumerate(grille):
        for x, c in enumerate(rangee):
            if c != ".":
                h = palette[c].lstrip("#")
                img.putpixel((x, y), (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), 255))
    chemin.parent.mkdir(parents=True, exist_ok=True)
    img.save(chemin)
    print(f"dessiné   {chemin.relative_to(RACINE)}")


# ---------------------------------------------------------------- personnages
# Gabarits 16 × 16 : o contour, h cheveux, s peau, e yeux, c chandail,
# C ombre du chandail, p pantalon, b souliers. a et g : casquette et lunettes.

CORPS_FACE = [
    "...ooccccccoo...",
    "..osccccccccso..",
    "..osccccccccso..",
    "...oCCCCCCCCo...",
    "....oppppppo....",
    "....oppooppo....",
]
POSES = {
    "bas0": [
        "................",
        ".....oooooo.....",
        "....ohhhhhho....",
        "...ohhhhhhhho...",
        "...ohhsssshho...",
        "...ohsessesho...",
        "...ohssssssho...",
        "....osssssso....",
        *CORPS_FACE,
        "....oppooppo....",
        "....obboobbo....",
    ],
    "bas1": [
        "................",
        ".....oooooo.....",
        "....ohhhhhho....",
        "...ohhhhhhhho...",
        "...ohhsssshho...",
        "...ohsessesho...",
        "...ohssssssho...",
        "....osssssso....",
        *CORPS_FACE,
        "....oppoobbo....",
        "....obbo........",
    ],
    "haut0": [
        "................",
        ".....oooooo.....",
        "....ohhhhhho....",
        "...ohhhhhhhho...",
        "...ohhhhhhhho...",
        "...ohhhhhhhho...",
        "...ohhhhhhhho...",
        "....ohhhhhho....",
        *CORPS_FACE,
        "....oppooppo....",
        "....obboobbo....",
    ],
    "haut1": [
        "................",
        ".....oooooo.....",
        "....ohhhhhho....",
        "...ohhhhhhhho...",
        "...ohhhhhhhho...",
        "...ohhhhhhhho...",
        "...ohhhhhhhho...",
        "....ohhhhhho....",
        *CORPS_FACE,
        "....obbooppo....",
        "........obbo....",
    ],
    "gauche0": [
        "................",
        "......ooooo.....",
        ".....ohhhhho....",
        "....ohhhhhhho...",
        "....osshhhhho...",
        "....osesshhho...",
        "...ossssshhho...",
        "....osssssso....",
        ".....occccco....",
        ".....occccco....",
        ".....oscccco....",
        ".....oCCCCCo....",
        "......opppo.....",
        "......opppo.....",
        "......opppo.....",
        ".....obbbo......",
    ],
    "gauche1": [
        "................",
        "......ooooo.....",
        ".....ohhhhho....",
        "....ohhhhhhho...",
        "....osshhhhho...",
        "....osesshhho...",
        "...ossssshhho...",
        "....osssssso....",
        ".....occccco....",
        ".....occccco....",
        ".....oscccco....",
        ".....oCCCCCo....",
        ".....oppoppo....",
        "....opo..opo....",
        "...obbo..obo....",
        "................",
    ],
}

# Accessoires : rangées remplacées, par pose.
# Chapeau de brousse, façon Crocodile Dundee : la calotte (a), le ruban (A)
# avec deux dents de crocodile (w), et le large rebord (a).
CHAPEAU_BROUSSE = {
    "bas": {2: "....oaaaaaao....", 3: "....oAwAAwAo....", 4: ".oaaaaaaaaaaaao."},
    "haut": {2: "....oaaaaaao....", 3: "....oAAAAAAo....", 4: ".oaaaaaaaaaaaao."},
    "gauche": {2: ".....oaaaaao....", 3: ".....oAwAAAo....", 4: ".oaaaaaaaaaaao.."},
}
# Cheveux courts plaqués : le visage prend toute la largeur, lunettes comprises.
LUNETTES_NOIRES = {
    "bas": {4: "...o" + "s" * 8 + "o...", 5: "...o" + "g" * 8 + "o...", 6: "...o" + "s" * 8 + "o..."},
    "haut": {},
    "gauche": {5: "....ogggshhho..."},
}
# Col blanc (w) et cravate (t) sur le veston (c).
CRAVATE = {
    "bas": {8: "...oocwttwcoo...", 9: "..oscccttcccso.."},
    "haut": {},
    "gauche": {8: ".....owcccco...."},
}
COL = {
    "bas": {8: "...oocwccwcoo..."},
    "haut": {},
    "gauche": {8: ".....owcccco...."},
}

# Le gestionnaire, c'est Claude ; les employés, les subagents ; les auditeurs,
# les relecteurs. L'explorateur, ceux qui cherchent ; le générique, tout agent sans rôle.
PERSONNAGES = {
    "gestionnaire": ({"h": "#8a8a8a", "s": "#f2c7a5", "c": "#2f3e5c", "C": "#23304a", "p": "#23304a",
                      "t": "#d97757"}, [CRAVATE]),
    "employe": ({"h": "#5a3a22", "s": "#e8b996", "c": "#8fb8de", "C": "#6f95b8", "p": "#4a4f5a"}, [COL]),
    "generique": ({"h": "#5a3a22", "s": "#e8b996", "c": "#f2d23c", "C": "#c9aa22", "p": "#6b4a2e"}, [COL]),
    "auditeur": ({"h": "#141414", "s": "#f0d2bc", "c": "#1c1c1c", "C": "#0e0e0e", "p": "#1c1c1c",
                  "t": "#050505", "g": "#050505"}, [CRAVATE, LUNETTES_NOIRES]),
    # Tout en beige, façon Steve Irwin : chemise kaki, short plus foncé, chapeau de cuir.
    "explorateur": ({"h": "#5a3a22", "s": "#d9a07a", "c": "#d8c49a", "C": "#b8a478", "p": "#9c8658",
                     "a": "#8b6a3e", "A": "#4a3424"}, [CHAPEAU_BROUSSE]),
}
COMMUNES = {"o": "#2b1d16", "e": "#2b1d16", "b": "#2b1d16", "g": "#1d1d1d", "w": "#f4f4f4"}

# La planche : 3 colonnes × 2 rangées, dans l'ordre que construire.py attend.
ORDRE = [["bas0", "haut0", "gauche0"], ["bas1", "haut1", "gauche1"]]

for nom, (couleurs, accessoires) in PERSONNAGES.items():
    planche = []
    for rangee_poses in ORDRE:
        grilles = []
        for pose in rangee_poses:
            grille = list(POSES[pose])
            for accessoire in accessoires:
                for i, rangee in accessoire.get(pose.rstrip("01"), {}).items():
                    grille[i] = rangee
            grilles.append(grille)
        planche += ["".join(g[y] for g in grilles) for y in range(16)]
    ecrire(RACINE / "personnages" / nom / "planche.png", planche, {**COMMUNES, **couleurs})

# ---------------------------------------------------------------------- décor

BOIS = {"a": "#e3c08d", "b": "#c49a66", "c": "#d6b07b"}
MOULURE = {"w": "#f1e3c6", "x": "#e2cfa9", "m": "#9c6b43", "n": "#6e4a2e", "k": "#4a3424"}

ecrire(RACINE / "decor" / "sol" / "image.png", [
    "aaaaaaabaaaaaaaa",
    "aaaaaaabaaaaacaa",
    "aacaaaabaaaaaaaa",
    "bbbbbbbbbbbbbbbb",
    "aaaaaaaaaaabaaaa",
    "aacaaaaaaaabaaca",
    "aaaaaaaaaaabaaaa",
    "bbbbbbbbbbbbbbbb",
    "aaaabaaaaaaaaaaa",
    "aaaabaaaacaaaaaa",
    "aaaabaaaaaaaaaca",
    "bbbbbbbbbbbbbbbb",
    "aaaaaaaaaaaaaaab",
    "aacaaaaaaaaaaaab",
    "aaaaaaacaaaaaaab",
    "bbbbbbbbbbbbbbbb",
], BOIS)

ecrire(RACINE / "decor" / "mur" / "image.png", [
    *["wwwwwwwxwwwwwwwx"] * 10,
    "mmmmmmmmmmmmmmmm",
    "xxxxxxxmxxxxxxxm",
    "xxxxxxxmxxxxxxxm",
    "xxxxxxxmxxxxxxxm",
    "mmmmmmmmmmmmmmmm",
    "nnnnnnnnnnnnnnnn",
], MOULURE)

ecrire(RACINE / "decor" / "mur-bas" / "image.png", [
    *["................"] * 10,
    "mmmmmmmmmmmmmmmm",
    *["nnnnnnnnnnnnnnnn"] * 5,
], MOULURE)

ecrire(RACINE / "decor" / "porte" / "image.png", [
    *["................................"] * 6,
    "mm..rrrrrrrrrrrrrrrrrrrrrrrr..mm",
    "mm..rrrrrrrrrrrrrrrrrrrrrrrr..mm",
    "mm..qqqqqqqqqqqqqqqqqqqqqqqq..mm",
    "mm..rrrrrrrrrrrrrrrrrrrrrrrr..mm",
    "mm..qqqqqqqqqqqqqqqqqqqqqqqq..mm",
    "mm..rrrrrrrrrrrrrrrrrrrrrrrr..mm",
    "mm..rrrrrrrrrrrrrrrrrrrrrrrr..mm",
    "mmkkkkkkkkkkkkkkkkkkkkkkkkkkkkmm",
    "mmkkkkkkkkkkkkkkkkkkkkkkkkkkkkmm",
    "mmkkkkkkkkkkkkkkkkkkkkkkkkkkkkmm",
], {**MOULURE, "r": "#b5523b", "q": "#8e3b2a"})

def fenetre() -> list[str]:
    """32 × 16 : deux vitres, un reflet en diagonale, un rebord."""
    bord = ".." + "m" * 27 + "..."

    def vitre(i: int) -> str:
        gauche = ["g"] * 12
        droite = ["g"] * 11
        gauche[i] = droite[i] = "l"
        return "..m" + "".join(gauche) + "mm" + "".join(droite) + "m..."

    vide = "." * 32
    return [vide, vide, bord, *map(vitre, range(4)), bord, *map(vitre, range(5, 9)), bord,
            "." + "n" * 29 + "..", vide]


ecrire(RACINE / "decor" / "fenetre" / "image.png", fenetre(), {**MOULURE, "g": "#9fd3e6", "l": "#e3f5fb"})

ecrire(RACINE / "decor" / "cadre" / "image.png", [
    "................",
    "................",
    "................",
    "...nnnnnnnnnn...",
    "...nggggggyyn...",
    "...nggggggyyn...",
    "...nggggggggn...",
    "...ngggvvgggn...",
    "...nggvvvvgvn...",
    "...nvvvvvvvvn...",
    "...nvvvvvvvvn...",
    "...nnnnnnnnnn...",
    "................",
    "................",
    "................",
    "................",
], {**MOULURE, "g": "#bfe3f0", "v": "#6aa84f", "y": "#f2c14e"})

# La plante verte se dessine aux archives (archives/dessins_archives.py),
# recopiée dans decor/plante/. La plante carnivore (son dessin d'Halloween,
# recopié dans themes/halloween/decor/plante/) et la pancarte sont à la fin du fichier.


# ----------------------------------------------------------------- la ville
# Les grandes images se dessinent par rectangles plutôt que pixel par pixel.


def toile(largeur: int, hauteur: int) -> list[list[str]]:
    return [["."] * largeur for _ in range(hauteur)]


def rect(g: list[list[str]], x: int, y: int, w: int, h: int, c: str) -> None:
    for j in range(y, y + h):
        for i in range(x, x + w):
            g[j][i] = c


def cadre(g: list[list[str]], x: int, y: int, w: int, h: int, bord: str, fond: str) -> None:
    rect(g, x, y, w, h, bord)
    rect(g, x + 1, y + 1, w - 2, h - 2, fond)


def texte(g: list[list[str]]) -> list[str]:
    return ["".join(r) for r in g]


def maison(fenetre: str, fumee: int | None) -> list[str]:
    """48 × 48 : toit, cheminée, façade, porte et deux fenêtres."""
    g = toile(48, 48)
    cadre(g, 33, 4, 6, 10, "o", "C")
    if fumee is not None:
        for i, (x, y) in enumerate([(35, 2), (37, 0), (34, 0)]):
            if (i + fumee) % 2 == 0:
                rect(g, x, y, 2, 2, "f")
    cadre(g, 2, 8, 44, 16, "o", "R")
    for y in range(11, 23, 4):
        rect(g, 3, y, 42, 1, "r")
    cadre(g, 5, 23, 38, 23, "o", "W")
    rect(g, 6, 23, 36, 2, "w")
    cadre(g, 20, 33, 8, 13, "o", "D")
    rect(g, 25, 39, 2, 2, "d")
    for x in (9, 31):
        cadre(g, x, 28, 8, 8, "F", fenetre)
        rect(g, x + 1, 31, 6, 1, "F")
    rect(g, 18, 46, 12, 2, "S")
    return texte(g)


MAISON = {"o": "#3b2a20", "C": "#8b5e3c", "f": "#d8d8d8", "R": "#c0503a", "r": "#96392a",
          "W": "#f0e0c0", "w": "#d8c49c", "D": "#7a4a2a", "d": "#e0b04a", "F": "#6e4a2e",
          "N": "#2f3a4a", "Y": "#f6d365", "S": "#a89880"}
ecrire(RACINE / "decor" / "maison" / "calme.png", maison("N", None), MAISON)
ecrire(RACINE / "decor" / "maison" / "active-1.png", maison("Y", 0), MAISON)
ecrire(RACINE / "decor" / "maison" / "active-2.png", maison("Y", 1), MAISON)

ecrire(RACINE / "decor" / "herbe" / "image.png", [
    "gggggggggggggggg",
    "gggGgggggggggggg",
    "ggGgGgggggggGggg",
    "gggggggggggGgGgg",
    "gggggggggggggggg",
    "gggggggGgggggggg",
    "ggggggGgGggggggg",
    "gggggggggggggggg",
    "gggggggggggggGgg",
    "gGgggggggggGgGgg",
    "GgGggggggggggggg",
    "gggggggggggggggg",
    "gggggggGgggggggg",
    "ggggggGgGggggggg",
    "gggggggggggggggg",
    "gggggggggggggggg",
], {"g": "#8cc06a", "G": "#6fa452"})

ecrire(RACINE / "decor" / "route" / "image.png", [
    "ssssssssssssssss",
    "ssssssSsssssssss",
    "ssssssssssssssss",
    "ssSsssssssssSsss",
    "ssssssssssssssss",
    "ssssssssssssssss",
    "sssssssssSssssss",
    "ssssssssssssssss",
    "sSssssssssssssss",
    "ssssssssssssssSs",
    "ssssssssssssssss",
    "sssssSssssssssss",
    "ssssssssssssssss",
    "ssssssssssSsssss",
    "ssSsssssssssssss",
    "ssssssssssssssss",
], {"s": "#e8d5a0", "S": "#cdb67e"})

ecrire(RACINE / "decor" / "arbre" / "image.png", [
    "......VVVV......",
    "....VVvvvvVV....",
    "...VvvvvvvvvV...",
    "..VvvvvvvvvvvV..",
    "..VvvVvvvvVvvV..",
    ".VvvvvvvvvvvvvV.",
    ".VvvvvvVvvvvvvV.",
    ".VvVvvvvvvvVvvV.",
    ".VvvvvvvvvvvvvV.",
    "..VvvvVvvvvvvV..",
    "..VVvvvvvvvvVV..",
    "....VVVVVVVV....",
    "......tttt......",
    "......tTtt......",
    ".....tttttt.....",
    "................",
], {"v": "#4f9a4a", "V": "#2f6b33", "t": "#7a4a2a", "T": "#5c3820"})


# ------------------------------------------------------- les bureaux en papier
# Vus d'en haut, l'agent assis derrière, face à nous. Les 3 rangées du haut
# restent vides : la tête et les épaules de l'agent dépassent du bureau.
# États : inactif, et une animation par sorte de travail (travail, redaction,
# audit), choisie par la section « activites » de bureau.json.

PAPIER = {"o": "#5c3b22", "t": "#c8935a", "d": "#9c6b43", "p": "#fbf6e9", "P": "#d9d2bf",
          "l": "#7a7a8a", "k": "#2b2b2b", "r": "#c0392b", "R": "#e05a4a", "b": "#7a5230",
          "y": "#e0b04a"}


def table(largeur: int, hauteur: int) -> list[list[str]]:
    g = toile(largeur, hauteur)
    cadre(g, 0, 3, largeur, hauteur - 9, "o", "t")
    cadre(g, 0, hauteur - 7, largeur, 6, "o", "d")
    return g


def pile(g: list[list[str]], x: int, y: int) -> None:
    """Une pile de feuilles bien rangée."""
    cadre(g, x, y + 1, 7, 6, "o", "P")
    cadre(g, x, y, 7, 6, "o", "p")


def feuille(g: list[list[str]], x: int, y: int, lignes: int = 0) -> None:
    cadre(g, x, y, 11, 9, "o", "p")
    for i in range(lignes):
        rect(g, x + 2, y + 2 + 2 * i, 7 if i < 2 else 4, 1, "l")


def poste(dessin) -> list[str]:
    g = table(32, 20)
    pile(g, 23, 5)
    dessin(g)
    return texte(g)


ecrire(RACINE / "decor" / "poste" / "inactif.png", poste(lambda g: None), PAPIER)

# Travail ordinaire : les feuilles se déplacent d'une image à l'autre.
ecrire(RACINE / "decor" / "poste" / "travail-1.png", poste(lambda g: (feuille(g, 4, 4, 2), feuille(g, 10, 6, 1))), PAPIER)
ecrire(RACINE / "decor" / "poste" / "travail-2.png", poste(lambda g: (feuille(g, 10, 6, 1), feuille(g, 5, 5, 2))), PAPIER)


# Rédaction : les lignes apparaissent une à une, le stylo au bout.
def redaction(n: int):
    def dessin(g):
        feuille(g, 8, 4)
        for i in range(n):
            rect(g, 10, 6 + 2 * i, 7 if i < 2 else 4, 1, "l")
        x, y = (17 if n < 3 else 14), 4 + 2 * n
        rect(g, x, y, 1, 1, "k")
        rect(g, x + 1, y - 1, 1, 1, "k")
        rect(g, x + 2, y - 2, 1, 1, "y")
    return dessin


for n in (1, 2, 3):
    ecrire(RACINE / "decor" / "poste" / f"redaction-{n}.png", poste(redaction(n)), PAPIER)


# Audit : le tampon se lève, puis s'abat et laisse sa marque rouge.
def audit(isBaisse: bool):
    def dessin(g):
        feuille(g, 8, 5, 3)
        if isBaisse:
            rect(g, 12, 8, 4, 3, "r")
            cadre(g, 11, 5, 6, 3, "o", "b")
            rect(g, 13, 3, 2, 2, "b")
        else:
            cadre(g, 11, 0, 6, 3, "o", "b")
            rect(g, 13, 3, 2, 1, "b")
    return dessin


ecrire(RACINE / "decor" / "poste" / "audit-1.png", poste(audit(False)), PAPIER)
ecrire(RACINE / "decor" / "poste" / "audit-2.png", poste(audit(True)), PAPIER)


# Le cigare du gestionnaire qui attend : posé sur sa bouche (16 × 16, comme
# un personnage), la fumée monte en trois images.
def cigare(image: int) -> list[str]:
    g = toile(16, 16)
    rect(g, 9, 7, 4, 1, "c")
    rect(g, 13, 7, 1, 1, "f")
    bouffees = [[(13, 5), (14, 3)], [(14, 4), (13, 2)], [(13, 3), (14, 1), (13, 0)]]
    for x, y in bouffees[image]:
        rect(g, x, y, 1, 1, "s")
    rect(g, *[(14, 5), (13, 4), (14, 2)][image], 1, 1, "S")
    return texte(g)


for i in range(3):
    ecrire(RACINE / "decor" / "cigare" / f"fume-{i + 1}.png", cigare(i),
           {"c": "#6b3e26", "f": "#e8743b", "s": "#d8d8d8", "S": "#f4f4f4"})


# Les chaises, vues de face derrière celui qui s'y assoit : seulement le
# dossier, plus large que les épaules. La page le place assez bas pour que
# son pied disparaisse derrière le bureau et que son haut dépasse à peine des
# épaules. Le fauteuil du gestionnaire est plus large, en cuir capitonné.
def arrondir(g: list[list[str]]) -> None:
    """Arrondit les quatre coins d'un dossier : deux pixels retirés, le contour rentré d'un cran."""
    h, w = len(g), len(g[0])
    for y, x, dy, dx in [(0, 0, 1, 1), (0, w - 1, 1, -1), (h - 1, 0, -1, 1), (h - 1, w - 1, -1, -1)]:
        g[y][x] = g[y][x + dx] = g[y + dy][x] = "."
        g[y + dy][x + dx] = "o"


def chaise() -> list[str]:
    g = toile(16, 12)
    cadre(g, 0, 0, 16, 12, "o", "c")
    rect(g, 2, 1, 12, 1, "C")
    arrondir(g)
    return texte(g)


def fauteuil() -> list[str]:
    g = toile(20, 12)
    cadre(g, 0, 0, 20, 12, "o", "c")
    rect(g, 2, 1, 16, 1, "C")
    for x, y in [(4, 4), (10, 4), (15, 4), (7, 8), (12, 8)]:
        rect(g, x, y, 1, 1, "b")
    arrondir(g)
    return texte(g)


ecrire(RACINE / "decor" / "chaise" / "image.png", chaise(), {"o": "#1f2530", "c": "#3d4a5c", "C": "#5a6a80"})
ecrire(RACINE / "decor" / "fauteuil" / "image.png", fauteuil(),
       {"o": "#2b1610", "c": "#7a3e26", "C": "#9a5636", "b": "#4a2416"})


# La photocopieuse du bureau, où l'on va faire passer le contrôle mécanique.
# États : repos, imprime (le voyant clignote, la feuille sort), puis le
# verdict : ok (voyant vert, feuille propre) ou ecarts (voyant rouge, feuille
# couverte de marques).
def photocopieuse(voyant: str, feuille_sortie: int, marques: bool = False) -> list[str]:
    g = toile(16, 24)
    cadre(g, 1, 4, 14, 6, "o", "G")
    rect(g, 2, 5, 12, 1, "W")
    cadre(g, 1, 9, 14, 13, "o", "g")
    cadre(g, 9, 10, 5, 3, "o", "k")
    rect(g, 11, 11, 2, 1, voyant)
    rect(g, 2, 15, 7, 1, "k")
    if feuille_sortie:
        cadre(g, 3, 15, 5, 1 + feuille_sortie, "o", "p")
        if marques:
            rect(g, 4, 16, 2, 1, "r")
            if feuille_sortie > 3:
                rect(g, 5, 18, 2, 1, "r")
    rect(g, 1, 22, 14, 2, "k")
    return texte(g)


COPIEUSE = {"o": "#2b2b2b", "G": "#9a9a92", "W": "#c8c8c0", "g": "#d8d8d0", "k": "#3a3a3a",
            "p": "#fbf6e9", "a": "#e0b04a", "n": "#555555", "v": "#3fbf5a", "r": "#d0402f"}
ecrire(RACINE / "decor" / "photocopieuse" / "repos.png", photocopieuse("n", 0), COPIEUSE)
ecrire(RACINE / "decor" / "photocopieuse" / "imprime-1.png", photocopieuse("a", 2), COPIEUSE)
ecrire(RACINE / "decor" / "photocopieuse" / "imprime-2.png", photocopieuse("n", 4), COPIEUSE)
ecrire(RACINE / "decor" / "photocopieuse" / "ok.png", photocopieuse("v", 5), COPIEUSE)
ecrire(RACINE / "decor" / "photocopieuse" / "ecarts.png", photocopieuse("r", 5, marques=True), COPIEUSE)


# Le grand bureau du gestionnaire : corbeille à gauche, plaque devant.
def gestionnaire(dessin) -> list[str]:
    g = table(48, 24)
    cadre(g, 3, 5, 11, 8, "o", "b")
    rect(g, 4, 6, 9, 2, "p")
    pile(g, 37, 5)
    cadre(g, 18, 18, 12, 4, "o", "y")
    dessin(g)
    return texte(g)


ecrire(RACINE / "decor" / "bureau-gestionnaire" / "inactif.png", gestionnaire(lambda g: None), PAPIER)
ecrire(RACINE / "decor" / "bureau-gestionnaire" / "actif-1.png", gestionnaire(lambda g: feuille(g, 18, 5, 2)), PAPIER)
ecrire(RACINE / "decor" / "bureau-gestionnaire" / "actif-2.png", gestionnaire(lambda g: feuille(g, 19, 5, 3)), PAPIER)


# La plante carnivore, façon Little Shop of Horrors : une grosse gueule verte
# à lèvres rouges dans un pot, de face, 24 × 24. Trois états de la gueule
# (fermee, entrouverte, ouverte) ; dans chacun, quatre images de respiration.
# La version de profil est aux archives (archives/dessins_archives.py).


def contourner(g: list[list[str]]) -> None:
    """Entoure d'un trait foncé tout ce qui est dessiné."""
    h, w = len(g), len(g[0])
    a_entourer = [(x, y) for y in range(h) for x in range(w) if g[y][x] == "." and any(
        0 <= x + dx < w and 0 <= y + dy < h and g[y + dy][x + dx] not in ".o"
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))]
    for x, y in a_entourer:
        g[y][x] = "o"


def dans_ellipse(x: int, y: int, cx: float, cy: float, rx: float, ry: float) -> bool:
    return ((x + 0.5 - cx) / rx) ** 2 + ((y + 0.5 - cy) / ry) ** 2 <= 1


def pot_et_tige(g, dy_feuilles: int, bas_tete: int) -> None:
    # Le pot en terre cuite, fixe : rebord, puis le corps qui s'amincit.
    rect(g, 6, 17, 12, 2, "q")
    rect(g, 7, 19, 10, 2, "r")
    rect(g, 8, 21, 8, 2, "r")
    rect(g, 9, 19, 1, 4, "R")
    # La tige monte du pot jusqu'au dessous de la tête.
    rect(g, 11, bas_tete, 2, 17 - bas_tete, "s")
    # Deux feuilles en pointe au pied de la tige.
    y = 15 + dy_feuilles
    rect(g, 8, y, 3, 1, "v")
    rect(g, 6, y - 1, 3, 1, "v")
    rect(g, 13, y, 3, 1, "v")
    rect(g, 15, y - 1, 3, 1, "v")
    rect(g, 9, y + 1, 2, 1, "V")
    rect(g, 13, y + 1, 2, 1, "V")


# De combien le dôme monte et la mâchoire descend, par ouverture. C'est
# surtout la mâchoire qui s'ouvre : un dôme qui monte sortirait de l'image
# quand la tête est en haut de sa respiration.
ECARTS_GUEULE = {0: (0, 0), 1: (0, 1), 2: (1, 3)}


def tete_face(g, cx: float, m: int, ouverture: int) -> None:
    """Le dôme du haut et la mâchoire du bas s'écartent de part et d'autre de la bouche (rangée m)."""
    haut, bas = ECARTS_GUEULE[ouverture]
    for y in range(24):
        for x in range(24):
            if y < m - haut and dans_ellipse(x, y, cx, m - haut, 9, 6):
                g[y][x] = "v"
            elif y > m + bas and dans_ellipse(x, y, cx, m + bas + 1, 8, 4):
                g[y][x] = "V" if y == m + bas + 3 else "v"
    # Les taches claires sur le dôme.
    for x, y in ((-5, -4), (-2, -5), (3, -4), (5, -2), (-6, -2)):
        rect(g, round(cx + x), m - haut + y, 1, 1, "l")
    # Les lèvres : une lèvre en bas du dôme, une en haut de la mâchoire.
    gauche, droite = round(cx - 7), round(cx + 7)
    rect(g, gauche, m - haut - 1, droite - gauche, 1, "L")
    rect(g, gauche + 1, m + bas + 1, droite - gauche - 2, 1, "L")
    if ouverture == 0:
        rect(g, gauche + 1, m, droite - gauche - 2, 1, "M")
        return
    # La gueule ouverte : le dedans sombre, les dents, la langue.
    rect(g, gauche, m - haut, droite - gauche, haut + bas + 1, "b")
    for x in range(gauche + 1, droite - 1, 2):
        rect(g, x, m - haut, 1, 1, "w")
        if ouverture == 2:
            rect(g, x + 1, m + bas, 1, 1, "w")
    if ouverture == 2:
        rect(g, round(cx - 2), m + bas - 1, 4, 1, "t")


def carnivore(ouverture: int, dy_feuilles: int, dy_tete: int) -> list[str]:
    g = toile(24, 24)
    m = 9 + dy_tete
    pot_et_tige(g, dy_feuilles, m + ECARTS_GUEULE[ouverture][1] + 3)
    tete_face(g, 12, m, ouverture)
    contourner(g)
    return texte(g)


CARNIVORE = {"o": "#1d2a12", "v": "#5fa83c", "V": "#3f7a2a", "l": "#a6d86a", "s": "#3d7a35",
             "L": "#d8435a", "M": "#7a1a2c", "b": "#3a0d14", "w": "#f4f0e0", "t": "#e87a8a",
             "q": "#8e3b2a", "r": "#b5523b", "R": "#cf6a4e"}
# La respiration : la tige (les feuilles) monte, et la tête suit une image plus tard.
RESPIRE = [(0, 0), (-1, 0), (-1, -1), (0, -1)]
GUEULE = {"fermee": 0, "entrouverte": 1, "ouverte": 2}

# Fichier « <état>-<n>.png » : l'état de la gueule, puis l'image de la respiration.
for etat, ouverture in GUEULE.items():
    for n, pose in enumerate(RESPIRE, 1):
        ecrire(RACINE / "decor" / "carnivore" / f"{etat}-{n}.png", carnivore(ouverture, *pose), CARNIVORE)


# La pancarte : un tableau à feuilles sur chevalet, 16 × 24, la taille la plus
# grande que prend la plante (le sapin, la carnivore). Deux états : « petite »,
# la feuille couverte de quelques gribouillis (une image d'écriture, pas les vraies lignes),
# posée dans le bureau ; « vierge », la feuille blanche, que la page agrandit au
# clic et sur laquelle elle écrit la légende, entre les rangées 3 et 15 et les
# colonnes 2 et 13 (l'intérieur de la feuille).
def pancarte(petite: bool) -> list[str]:
    g = toile(16, 24)
    # Les pattes : deux devant, écartées, une derrière, plus courte.
    for i in range(3):
        rect(g, 2 - i, 21 + i, 2, 1, "n")
        rect(g, 12 + i, 21 + i, 2, 1, "n")
    rect(g, 7, 21, 2, 2, "N")
    # La tablette où reposent les crayons, sous la feuille.
    cadre(g, 0, 18, 16, 3, "o", "b")
    rect(g, 3, 17, 3, 1, "r")
    rect(g, 7, 17, 3, 1, "u")
    # La feuille, et la pince qui la tient en haut.
    cadre(g, 1, 2, 14, 15, "o", "p")
    cadre(g, 2, 0, 12, 3, "o", "n")
    rect(g, 7, 1, 2, 1, "k")
    if petite:
        # Quatre lignes, pour l'idée : un symbole d'un pixel, puis des mots en traits.
        for n, y in enumerate(range(5, 15, 3)):
            g[y][3] = "rou"[n % 3]
            x, fin = 5, 13 - (n * 3) % 5
            for m in range(5):
                trait = 2 + (n + m) % 2
                rect(g, x, y, min(trait, fin - x), 1, "s")
                x += trait + 1
                if x >= fin:
                    break
    return texte(g)


PANCARTE = {"o": "#2b2b2b", "p": "#fbf6e9", "u": "#3b6fb6", "s": "#8a7f74",
            "r": "#d0402f", "n": "#7a5230", "N": "#5c3b22", "b": "#9c6b43", "k": "#c8c8c0"}
ecrire(RACINE / "decor" / "pancarte" / "petite.png", pancarte(True), PANCARTE)
ecrire(RACINE / "decor" / "pancarte" / "vierge.png", pancarte(False), PANCARTE)
