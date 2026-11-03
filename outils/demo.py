"""Joue une fausse session dans la ville, pour voir les animations sans agents.

Usage : python outils/demo.py [tours]   (3 tours par défaut, environ une minute chacun)

Une maison « Démo » apparaît dans la ville : clique dessus. Le script écrit
les mêmes fichiers que le mod (vue/registre.js et vue/sessions/demo.js),
puis retire la maison à la fin, ou à Ctrl+C.
"""
import json
import sys
import time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

VUE = Path(__file__).resolve().parent.parent / "vue"
ID = "demo"
TOURS = int(sys.argv[1]) if len(sys.argv) > 1 else 3

# Le scénario d'un tour : (seconde d'arrivée, seconde de départ, type,
# personnage, notebook, et ce qu'il fait au fil du temps).
AGENTS = [
    (3, 42, "redacteur", "employe", "NBK_CreationInitTables", [("Read", "?"), ("Edit", "$"), ("Bash", ">")]),
    (7, 24, "Explore", "explorateur", None, [("Glob", "?"), ("Grep", "?")]),
    (17, 26, "relecteur", "auditeur", "NBK_CreationInitTables", [("Read", "?"), ("Grep", "?")]),
    (30, 37, "relecteur", "auditeur", "NBK_CreationInitTables", [("Read", "?")]),
    (3, 34, "general-purpose", "generique", None, [("Read", "?"), ("Bash", ">")]),
]
# Le générique entre en même temps que le rédacteur : ils font la file à la
# porte. Les deux auditeurs sont appelés par le premier rédacteur : ils
# marchent jusqu'à son bureau. Le premier trouve des erreurs (il sacre), le
# second des remarques seulement (visage neutre) ; les autres agents finissent
# sans rien (crochet vert, s'ils étaient visiteurs).
PARENTS = {2: 0, 3: 0}
CONCLUSIONS = {2: "erreurs", 3: "remarques"}
# Les rédacteurs passent le contrôle mécanique trois fois, comme dans
# redacteur.md : le contrôle de départ (§ 2, aucun écart), puis après leur
# travail (§ 4, des écarts), puis après correction (aucun écart). En secondes
# après leur arrivée ; chaque passage fait son aller-retour.
CONTROLES = [(5, "ok"), (12, "ecarts"), (22, "ok")]
DUREE = 55
# Le gestionnaire travaille seul au début et à la fin ; entre les deux, il
# attend ses agents (et fume).
TRAVAIL = [(1, 3), (48, 53)]
# La fiche de chaque agent dans le panneau : modèle et effort, selon son type.
FICHES = {"redacteur": ("claude-sonnet-5-5", "high"), "relecteur": ("claude-opus-5-5", "medium"),
          "Explore": ("claude-haiku-5-5", "low"), "general-purpose": ("claude-sonnet-5-5", "medium")}
# Le premier rédacteur demande une permission (la main levée, la notification)
# entre ces deux secondes du tour.
PERMISSION = (8, 13)


def ecrire_registre(isPresente: bool) -> None:
    chemin = VUE / "registre.js"
    registre = {}
    if chemin.exists():
        brut = chemin.read_text(encoding="utf-8")
        try:
            registre = json.loads(brut[brut.index("=") + 1: brut.rindex(";")])
        except ValueError:
            pass
    registre.pop(ID, None)
    if isPresente:
        registre[ID] = {"projet": "Démo", "battement": int(time.time() * 1000)}
    chemin.write_text(f"window.BUREAU_REGISTRE = {json.dumps(registre, ensure_ascii=False)};\n", encoding="utf-8")


def ecrire_session(seconde: float, isFermee: bool = False) -> None:
    maintenant = time.time()
    debut = maintenant - seconde
    presents = []
    journal = []
    for i, (arrivee, depart, type_, perso, notebook, gestes) in enumerate(AGENTS):
        # Comme le mod : un agent fini reste dix secondes, avec sa conclusion.
        # Le journal du tour, comme celui du mod : arrivées, fins, permission.
        if seconde >= arrivee:
            journal.append({"t": int((debut + arrivee) * 1000), "texte": f"→ {type_} · démonstration"})
        if seconde >= depart:
            conclu = CONCLUSIONS.get(i, "ok")
            journal.append({"t": int((debut + depart) * 1000),
                            "texte": f"✓ {type_} fini{'' if conclu == 'ok' else ' · ' + conclu}"})
        if i == 0 and seconde >= PERMISSION[0]:
            journal.append({"t": int((debut + PERMISSION[0]) * 1000), "texte": f"? {type_} demande Bash"})
        if arrivee <= seconde < depart + 10:
            outil, glyph = gestes[int((seconde - arrivee) // 6) % len(gestes)]
            modele, effort = FICHES.get(type_, ("claude-sonnet-5-5", "medium"))
            ecoule = min(seconde, depart) - arrivee
            passes = [v for delai, v in CONTROLES if type_ == "redacteur" and seconde - arrivee >= delai]
            presents.append({"id": f"demo-{i}", "type": type_, "description": "démonstration",
                             "desk": -1, "enteredAt": int((debut + arrivee) * 1000),
                             "personnage": perso, "notebook": notebook,
                             "modele": modele, "effort": effort, "req": int(ecoule // 3) + 1,
                             "ctx": int(18000 + ecoule * 1500), "out": int(ecoule * 120),
                             "permission": i == 0 and PERMISSION[0] <= seconde < PERMISSION[1],
                             "activity": f"{outil} {notebook or 'exemple'}", "glyph": glyph,
                             "controles": len(passes), "verdicts": passes,
                             "parent": f"demo-{PARENTS[i]}" if i in PARENTS else None,
                             "fini": seconde >= depart,
                             "conclusion": CONCLUSIONS.get(i, "ok") if seconde >= depart else None})
    seul = any(debut <= seconde < fin for debut, fin in TRAVAIL)
    etat = {
        "projet": "Démo",
        "fermee": isFermee,
        "claude": {"personnage": "gestionnaire", "isWorking": seul,
                   "attente": 0 if seul else sum(not p["fini"] for p in presents),
                   "activity": "Edit PROJET.md", "glyph": "$",
                   "modele": "claude-opus-5-5", "effort": "medium", "reponse": int((debut + 3) * 1000),
                   "contexte": {"tokens": int(240000 + seconde * 900), "window": 1000000,
                                "percent": int((240000 + seconde * 900) / 10000)},
                   "out": int(seconde * 60), "cout": round(4.2 + seconde * 0.03, 2)},
        "agents": presents,
        "limites": "5h 42 % 2h10  ·  7j 12 %",
        "journal": sorted(journal, key=lambda l: l["t"])[-15:],
        "battement": int(time.time() * 1000),
    }
    (VUE / "sessions").mkdir(exist_ok=True)
    (VUE / "sessions" / f"{ID}.js").write_text(
        f"(window.BUREAU_SESSIONS = window.BUREAU_SESSIONS || {{}})[{json.dumps(ID)}] = "
        f"{json.dumps(etat, ensure_ascii=False)};\n",
        encoding="utf-8",
    )


try:
    for tour in range(1, TOURS + 1):
        print(f"tour {tour} de {TOURS}")
        debut = time.time()
        while (seconde := time.time() - debut) < DUREE:
            ecrire_session(seconde)
            if int(seconde) % 5 == 0:
                ecrire_registre(True)
            time.sleep(0.5)
finally:
    ecrire_session(DUREE, isFermee=True)
    ecrire_registre(False)
    print("démo terminée, maison retirée")
