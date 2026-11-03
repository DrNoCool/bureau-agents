"""Importe une planche de ChatGPT : la découpe en poses, efface le fond, et
range chaque pose dans un dossier du bureau.

Usage :
  python outils/importer.py <planche.png> <dossier> <nom1,nom2,...> [--miroir] [--bas Y]

  <dossier>  où ranger les poses, par exemple decor/detente
  <noms>     un nom par pose, de gauche à droite (fume-1,fume-2,fume-3)
  --miroir   retourne chaque pose (un personnage tourné du mauvais côté)
  --bas Y    coupe tout ce qui est sous la rangée Y de la planche

Les poses sont repérées par les bandes de fond qui les séparent. Le fond
(blanc ou magenta) est effacé en partant des bords : un blanc entouré d'un
contour, comme une chemise, reste intact. Toutes les poses gardent le même
cadre, pour que l'animation ne saute pas. Les images restent à leur taille ;
construire.py (ou /bureau) les ramène à la taille de bureau.json.
"""
import sys
from collections import deque
from pathlib import Path

from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
RACINE = Path(__file__).resolve().parent.parent

args = [a for a in sys.argv[1:] if not a.startswith("--")]
source, dossier, noms = Path(args[0]), RACINE / args[1], args[2].split(",")
miroir = "--miroir" in sys.argv
bas = int(sys.argv[sys.argv.index("--bas") + 1]) if "--bas" in sys.argv else None

img = Image.open(source).convert("RGBA")
if bas:
    img = img.crop((0, 0, img.width, bas))
W, H = img.size
px = img.load()


def fond(p) -> bool:
    r, g, b, a = p
    blanc = min(r, g, b) > 205 and max(r, g, b) - min(r, g, b) < 30
    magenta = r > 190 and g < 100 and b > 190
    return a < 128 or blanc or magenta


# Le fond, effacé en partant des bords.
vu = [[False] * H for _ in range(W)]
file = deque((x, y) for x in range(W) for y in (0, H - 1)) + deque((x, y) for y in range(H) for x in (0, W - 1))
while file:
    x, y = file.popleft()
    if not (0 <= x < W and 0 <= y < H) or vu[x][y] or not fond(px[x, y]):
        continue
    vu[x][y] = True
    px[x, y] = (0, 0, 0, 0)
    file.extend(((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)))

# Les poses : des groupes de colonnes non vides, séparés par du fond.
pleines = [x for x in range(W) if any(px[x, y][3] for y in range(H))]
groupes, debut, prec = [], pleines[0], pleines[0]
for x in pleines[1:]:
    if x - prec > 10:
        groupes.append((debut, prec))
        debut = x
    prec = x
groupes.append((debut, prec))
if len(groupes) != len(noms):
    sys.exit(f"{len(groupes)} poses trouvées, {len(noms)} noms donnés : {groupes}")

# Un même cadre pour toutes : la plus large, du plus haut au plus bas pixel.
largeur = max(b - a + 1 for a, b in groupes)
lignes = [y for y in range(H) if any(px[x, y][3] for x in range(0, W, 2))]
haut, fin = min(lignes), max(lignes) + 1
dossier.mkdir(parents=True, exist_ok=True)
for (a, _), nom in zip(groupes, noms):
    pose = img.crop((a, haut, a + largeur, fin))
    if miroir:
        pose = pose.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    pose.save(dossier / f"{nom}.png")
    print(f"importé   {dossier.relative_to(RACINE)}/{nom}.png  ({pose.width}×{pose.height})")
