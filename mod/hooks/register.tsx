import { atom, read, update } from 'claude-code'
import type { Register } from 'claude-code'

import type { Agent, Etape, Etapes, Limit } from '../types'

// La ville des agents. Le mod écoute la session (agents qui démarrent, outils
// lancés, fin de travail) et écrit son état dans vue/sessions/<id>.js ; la page
// vue/bureau.html dessine la ville et les bureaux à partir de ces fichiers.
// Le panneau de Claude Code (/bureau) n'affiche que le texte.

const PANE = 'bureau'
const PORT = 8765
const ADRESSE = `http://127.0.0.1:${PORT}/bureau.html`

const agents = atom({ plugin: 'bureau-agents', key: 'agents' } as const, [])
const main = atom({ plugin: 'bureau-agents', key: 'main' } as const, { isWorking: false })
const limits = atom({ plugin: 'bureau-agents', key: 'limits' } as const, [])
const etapes = atom({ plugin: 'bureau-agents', key: 'etapes' } as const, { etapes: [] })
const journal = atom({ plugin: 'bureau-agents', key: 'journal' } as const, [])

// L'outil que Claude appelle pour remplacer la liste d'étapes. Elle est gardée
// par projet ($.store), pour la retrouver dans une session suivante.
const OUTIL_ETAPES = 'etapes'
const NOM_OUTIL_ETAPES = 'mcp__bureau-agents__etapes'
const ETATS: Etape['etat'][] = ['fait', 'en_cours', 'a_faire']
const cleEtapes = () => `etapes:${racine ?? projet}`

function lireEtapes(brut: unknown): Etapes | string {
  const e = brut as { titre?: unknown; etapes?: unknown; notes?: unknown }
  if (!Array.isArray(e?.etapes)) return 'etapes doit être une liste'
  const liste: Etape[] = []
  for (const [i, x] of (e.etapes as unknown[]).entries()) {
    const t = x as { texte?: unknown; etat?: unknown; details?: unknown; code?: unknown }
    if (typeof t?.texte !== 'string' || !ETATS.includes(t.etat as Etape['etat'])) {
      return `étape ${i + 1} : texte (texte) et etat (fait, en_cours ou a_faire) obligatoires`
    }
    const details = Array.isArray(t.details) ? t.details.filter((d): d is string => typeof d === 'string') : undefined
    const code = typeof t.code === 'string' && t.code.trim() ? t.code : undefined
    liste.push({ texte: t.texte, etat: t.etat as Etape['etat'], ...(details?.length ? { details } : {}), ...(code ? { code } : {}) })
  }
  const notes = Array.isArray(e.notes) ? e.notes.filter((n): n is string => typeof n === 'string') : undefined
  return { ...(typeof e.titre === 'string' ? { titre: e.titre } : {}), etapes: liste, ...(notes?.length ? { notes } : {}) }
}

// Ce que le mod lit de bureau.json : le nombre de postes et qui est qui.
type Plan = {
  postes: unknown[]
  personnages: Record<string, string>
  // Le nom affiché d'un type d'agent (« Explore » → « explorateur ») ; sans nom, le type.
  noms?: Record<string, string>
}
type Moteur = Parameters<typeof read>[0] & {
  fs: { read: (chemin: string) => Promise<string>; write: (chemin: string, texte: string) => Promise<void> }
  plugin: { root: string }
  clock: { now: () => Promise<number>; after: (ms: number, fn: () => void) => { cancel: () => void } }
  process: {
    run: (argv: readonly string[], init?: { cwd?: string; timeoutMs?: number }) => Promise<{ exitCode: number; stdout: string }>
    spawn: (request: { argv: readonly string[] }) => AsyncGenerator<unknown, unknown>
  }
}
type Registre = Record<string, { projet: string; battement: number }>

// Relus au démarrage et à chaque /bureau. Le mod vit dans mod/ ; les images,
// le plan et la page vivent dans le dossier du projet, nommé par
// mod/projet.json : écrire dans le dossier du mod le ferait se recharger.
let dossier: string | undefined
let sessionId: string | undefined
let projet = '?'
let plan: Plan | undefined
let probleme: string | undefined

async function charger($: Moteur): Promise<void> {
  try {
    dossier = (JSON.parse(await $.fs.read(`${$.plugin.root}/projet.json`)) as { dossier: string }).dossier
    plan = JSON.parse(await $.fs.read(`${dossier}/bureau.json`)) as Plan
    probleme = undefined
  } catch (err) {
    probleme = `Lecture de projet.json ou bureau.json impossible : ${String(err)}`
  }
}

// L'état git du dossier de la session, relu au démarrage et après chaque commit
// ou push du gestionnaire. Rien n'est tiré du serveur (pas de fetch) : « à
// tirer » date du dernier fetch ou pull.
const RELEVE = 15 * 60000
type Depot =
  | { isGit: false }
  | { isGit: true; branche: string; isSuivie: boolean; aPousser: number; aTirer: number; modifies: number }
// Quand l'utilisation a été mesurée pour la dernière fois. Les limites sont
// celles du compte : la page prend la mesure la plus fraîche de toutes les sessions.
let mesure: number | undefined
let racine: string | undefined
let depot: Depot | undefined
let prochainReleve: { cancel: () => void } | undefined

// Claude fait les commits ; seul le push peut venir d'ailleurs (de toi, dans
// VS Code). Tant qu'il reste des commits à pousser, un relevé 15 minutes
// après le dernier, quelle qu'en soit la cause. Rien à pousser, ou pas un
// dépôt git : plus de relevé jusqu'au prochain commit du gestionnaire.
async function relever($: Moteur): Promise<void> {
  prochainReleve?.cancel()
  prochainReleve = undefined
  await lireDepot($)
  await publier($)
  const isEnAttente = depot?.isGit === true && (depot.aPousser > 0 || !depot.isSuivie)
  if (isEnAttente) prochainReleve = $.clock.after(RELEVE, () => void relever($))
}

async function lireDepot($: Moteur): Promise<void> {
  if (!racine) return
  try {
    const r = await $.process.run(['git', 'status', '--porcelain=v2', '--branch'], { cwd: racine, timeoutMs: 10000 })
    if (r.exitCode !== 0) {
      depot = { isGit: false }
      return
    }
    const lignes = r.stdout.split('\n').filter(Boolean)
    const entete = (cle: string) => lignes.find(l => l.startsWith(`# branch.${cle} `))?.split(' ').slice(2)
    const ecart = entete('ab') // [« +2 », « -0 »] : en avance, en retard sur la branche suivie
    depot = {
      isGit: true,
      branche: entete('head')?.[0] ?? '?',
      isSuivie: ecart !== undefined,
      aPousser: Number(ecart?.[0]?.slice(1) ?? 0),
      aTirer: Number(ecart?.[1]?.slice(1) ?? 0),
      modifies: lignes.filter(l => !l.startsWith('#')).length,
    }
  } catch {
    // git absent : on garde le dernier état connu.
  }
}

// Claude est le gestionnaire ; chaque type de subagent a son personnage.
const nomDe = (type: string): string => plan?.noms?.[type] ?? type

function personnageDe(type: string): string {
  return plan?.personnages[type] ?? plan?.personnages['*'] ?? 'employe'
}

// La page montre une ville : une maison par session ouverte. Chaque session
// écrit son propre fichier, vue/sessions/<id>.js, que la page relit toutes les
// demi-secondes. Il ne contient que les agents présents : c'est la page qui
// décide, à son horloge, quand un nouveau venu entre et quand un absent va
// remettre son travail puis sort. Le battement dit à la page que la session vit.
// L'anti-veille : tant que Claude travaille, attend ses agents ou qu'un agent
// tourne encore, le mod garde outils/rester_eveille.ps1 en marche ; au repos,
// il l'arrête et l'ordinateur peut de nouveau se mettre en veille. Seule la
// veille est bloquée : l'écran s'éteint et se verrouille comme d'habitude.
let eveil: AsyncGenerator<unknown, unknown> | undefined

function veiller($: Moteur, isActif: boolean): void {
  if (!dossier) return
  if (isActif && !eveil) {
    const script = `${dossier}/outils/rester_eveille.ps1`
    const enfant = $.process.spawn({ argv: ['powershell', '-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', script] })
    eveil = enfant
    void (async () => {
      try {
        for await (const _ligne of enfant) {
          // Le script note son signe de vie ; rien à en faire.
        }
      } catch {
        // PowerShell absent ou script introuvable : la page dira « inactif ».
      } finally {
        if (eveil === enfant) eveil = undefined
      }
    })()
  } else if (!isActif && eveil) {
    // Quitter la boucle tue le script ; Windows rétablit alors la veille.
    void eveil.return(undefined)
    eveil = undefined
  }
}

async function publier($: Moteur, isFermee = false): Promise<void> {
  if (!dossier || !sessionId) return
  try {
    const [liste, m, lim, et, jo, maintenant] = await Promise.all([
      read($, agents),
      read($, main),
      read($, limits),
      read($, etapes),
      read($, journal),
      $.clock.now(),
    ])
    veiller($, !isFermee && (m.isWorking || (m.attente ?? 0) > 0 || liste.some(a => a.leftAt === undefined)))
    // Un agent qui vient de finir reste dix secondes dans le fichier, marqué
    // « fini » : la page y lit sa conclusion avant de le faire partir.
    const etat = {
      projet,
      fermee: isFermee,
      claude: { personnage: personnageDe('claude'), ...m },
      agents: liste
        .filter(a => a.leftAt === undefined || maintenant - a.leftAt < 10000
          || liste.some(b => b.leftAt === undefined && b.parent === a.id))
        .map(a => ({ ...a, personnage: personnageDe(a.type), fini: a.leftAt !== undefined })),
      limites: ligneLimites(lim, maintenant),
      mesure: lim.length ? mesure : undefined,
      depot,
      etapes: et.etapes.length ? et : undefined,
      journal: jo.slice(-15),
      battement: maintenant,
    }
    await $.fs.write(
      `${dossier}/vue/sessions/${sessionId}.js`,
      `(window.BUREAU_SESSIONS = window.BUREAU_SESSIONS || {})[${JSON.stringify(sessionId)}] = ${JSON.stringify(etat)};\n`,
    )
  } catch {
    // La page garde le dernier état.
  }
}

// Le registre (vue/registre.js) dit à la page quelles sessions existent.
// Toutes les sessions l'écrivent : chacune s'y réinscrit à chaque battement,
// ce qui répare une inscription perdue quand deux sessions écrivent en même temps.
async function inscrire($: Moteur, isPresente: boolean): Promise<void> {
  if (!dossier || !sessionId) return
  const chemin = `${dossier}/vue/registre.js`
  try {
    let registre: Registre = {}
    try {
      const brut = await $.fs.read(chemin)
      registre = JSON.parse(brut.slice(brut.indexOf('=') + 1, brut.lastIndexOf(';'))) as Registre
    } catch {
      // Pas encore de registre : on part de zéro.
    }
    const maintenant = await $.clock.now()
    for (const [id, inscrit] of Object.entries(registre)) {
      if (maintenant - inscrit.battement > 120000) delete registre[id]
    }
    if (isPresente) registre[sessionId] = { projet, battement: maintenant }
    else delete registre[sessionId]
    await $.fs.write(chemin, `window.BUREAU_REGISTRE = ${JSON.stringify(registre)};\n`)
  } catch {
    // La page retrouvera la session au prochain battement.
  }
}

// Le notebook d'un agent, deviné dans son mandat (« … NBK_X.Notebook … »),
// pour l'étiquette de son bureau. Rien de plus : le mod ne suit pas les
// fichiers que l'agent ouvre.
const GUID = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i

function devinerNotebook(texte: string): string | undefined {
  const m = texte.match(/([\w-]+)\.Notebook/) ?? texte.match(/\b(NBK_\w+)/)
  return m && !GUID.test(m[1]) ? m[1] : undefined
}

// Ce que fait un outil, en quelques mots, et son pictogramme dans la bulle.
const LIRE = ['Read', 'Grep', 'Glob', 'WebFetch', 'WebSearch', 'ToolSearch']
const ECRIRE = ['Edit', 'Write', 'NotebookEdit']
const COMMANDE = ['Bash', 'PowerShell']
// Les commandes d'essai d'un rédacteur : tests automatiques ou vérification de l'app.
const ESSAI = /\b(npm|pnpm|yarn)\s+(run\s+)?test\b|\bpytest\b|\bnode\s+--check\b|\bpython\s+-m\s+unittest\b|\bvitest\b|\bjest\b/

function decrire(e: { tool: string }): { texte: string; glyph: string } {
  const a = e as unknown as Record<string, unknown>
  const cible = a.file_path ?? a.notebook_path ?? a.pattern ?? a.command ?? a.url ?? a.query ?? a.description ?? a.path
  let detail = typeof cible === 'string' ? cible : ''
  if (detail && (a.file_path || a.notebook_path)) detail = detail.split(/[\\/]/).pop() ?? detail
  if (detail.length > 50) detail = `${detail.slice(0, 47)}...`
  const glyph = LIRE.includes(e.tool)
    ? '?'
    : ECRIRE.includes(e.tool)
      ? '$'
      : COMMANDE.includes(e.tool)
        ? '>'
        : e.tool === 'Agent'
          ? '+'
          : '*'
  return { texte: detail ? `${e.tool} ${detail}` : e.tool, glyph }
}

const NOMS: Record<string, string> = { five_hour: '5h', seven_day: '7j' }

// « 5h 80 % 1h15m  ·  7j 11 % 3j » : la page en tire une jauge par fenêtre,
// avec le temps qui reste avant que chacune reparte. Avant la première mesure :
// « 5h ?  ·  7j ? ».
// Dès 24 h, des jours et des heures (« 1j12h ») ; en deçà, des heures (« 23h »),
// avec leurs minutes sous 10 h (« 1h15m », « 56m »). Une seconde unité à zéro
// tombe (« 1j », « 1h »). La jauge tient alors dans sa colonne.
function tempsRestant(min: number): string {
  const [j, h, m] = [Math.floor(min / 1440), Math.floor((min % 1440) / 60), min % 60]
  if (j) return h ? `${j}j${h}h` : `${j}j`
  if (h >= 10 || (h && !m)) return `${h}h`
  return h ? `${h}h${m}m` : `${m}m`
}

function ligneLimites(liste: Limit[], maintenant: number): string {
  if (liste.length === 0) return '5h ?  ·  7j ?'
  return liste
    .map(l => {
      const base = `${NOMS[l.kind] ?? l.kind} ${l.percentUsed} %`
      if (!l.resetsAt) return base
      const min = Math.max(0, Math.round((new Date(l.resetsAt).getTime() - maintenant) / 60000))
      return `${base} ${tempsRestant(min)}`
    })
    .join('  ·  ')
}

const EN_COURS = ['pending', 'running', 'waiting']

// Le journal : une ligne par agent lancé ou fini, fichier modifié, erreur
// d'outil, demande de permission et commit. Les lectures n'y vont pas : elles
// noieraient le reste. On en garde 50 ; la page montre les 15 dernières.
const JOURNAL_MAX = 50
async function noter($: Moteur, texte: string): Promise<void> {
  const t = await $.clock.now()
  await update($, journal, l => [...l, { t, texte }].slice(-JOURNAL_MAX))
}
// Lève la marque « t'attend » de Claude (agentId absent) ou d'un agent.
async function lever($: Moteur, agentId?: string): Promise<void> {
  if (agentId === undefined) {
    if ((await read($, main)).permission) await update($, main, m => ({ ...m, permission: false }))
  } else if ((await read($, agents)).some(a => a.id === agentId && a.permission)) {
    await update($, agents, l => l.map(a => (a.id === agentId ? { ...a, permission: false } : a)))
  }
}

// Qui a fait le geste : Claude, ou le type de l'agent.
const qui = (agentId?: string) => {
  const type = agentId === undefined ? undefined : connus.get(agentId)?.type
  return agentId === undefined ? 'Claude' : type ? nomDe(type) : 'agent'
}

// Un relecteur termine par « Bilan : 1 ⛔, 3 ⚠️ » ou « Bilan : rien ». Des ⛔,
// il sacre ; des ⚠️ seulement, il a des remarques ; sinon, il coche en vert.
// Seul le dernier bilan compte : un ⛔ cité ailleurs dans le texte ne dit rien.
function conclure(texte: string): Agent['conclusion'] {
  const bilan = [...texte.matchAll(/Bilan\s*:([^\n]*)/g)].pop()?.[1] ?? ''
  const compte = (motif: RegExp) => Number(bilan.match(motif)?.[1] ?? 0)
  if (compte(/(\d+)\s*⛔/) > 0) return 'erreurs'
  if (compte(/(\d+)\s*⚠/) > 0) return 'remarques'
  return 'ok'
}

// La fiche de chaque agent vu dans la session, gardée après son départ : un
// agent relancé (SendMessage) revient sans nouveau lancement.
const connus = new Map<string, Agent>()

// Un agent qui reprend après être parti revient dans la liste, à un poste
// libre, comme un nouveau venu. Rend vrai s'il est revenu.
async function revenir($: Moteur, id: string): Promise<boolean> {
  const fiche = connus.get(id)
  if (!fiche) return false
  const liste = await read($, agents)
  if (liste.some(a => a.id === id && a.leftAt === undefined)) return false
  const maintenant = await $.clock.now()
  const postes = plan?.postes.length ?? 0
  await update($, agents, l => {
    const autres = l.filter(a => a.id !== id)
    const pris = new Set(autres.filter(a => a.leftAt === undefined).map(a => a.desk))
    const libre = Array.from({ length: postes }, (_, i) => i).find(i => !pris.has(i))
    return [...autres, { ...fiche, desk: libre ?? -1, enteredAt: maintenant }]
  })
  return true
}

export const register: Register = on => {
  let menage: { cancel: () => void } | undefined
  let battement: { cancel: () => void } | undefined
  let isServeurLance = false

  on('session.start', async ($, e, next) => {
    await charger($)
    sessionId = await $.session.id()
    // La racine du projet, pas le dossier courant : un « cd » dans le
    // terminal de Claude déplace le second, jamais la première.
    racine = await $.session.root().catch(() => e.cwd)
    projet = racine.split(/[\\/]/).filter(Boolean).pop() ?? racine
    try {
      const garde = await $.store.get(cleEtapes())
      if (garde && typeof garde === 'object') await update($, etapes, () => garde as Etapes)
    } catch {
      // Rien de gardé pour ce projet : la liste attend le premier appel de l'outil.
    }
    await $.tool.register({
      name: OUTIL_ETAPES,
      isDeferred: false,
      description:
        "Remplace la liste d'étapes affichée à la personne dans le panneau de droite du bureau (bouton « Étapes »). " +
        "Appelle-la chaque fois qu'une liste d'étapes de travail change (étape confirmée, ajoutée ou retirée), avec la liste complète. " +
        'Chaque étape : texte, etat (fait, en_cours ou a_faire), details (lignes facultatives), ' +
        'code (facultatif : bloc à copier tel quel, comme des paramètres ou une requête, affiché en police fixe avec un bouton Copier). ' +
        'notes : points en attente, hors des étapes. La liste est gardée par projet.',
      inputSchema: {
        type: 'object',
        properties: {
          titre: { type: 'string', description: 'Le titre de la liste' },
          etapes: {
            type: 'array',
            items: {
              type: 'object',
              properties: {
                texte: { type: 'string' },
                etat: { type: 'string', enum: ETATS },
                details: { type: 'array', items: { type: 'string' } },
                code: { type: 'string', description: 'Bloc à copier tel quel, sauts de ligne compris' },
              },
              required: ['texte', 'etat'],
            },
          },
          notes: { type: 'array', items: { type: 'string' } },
        },
        required: ['etapes'],
      },
    })
    await relever($)

    // Un mini-serveur web pour vue/ : le navigateur intégré de VS Code (Open
    // Integrated Browser) n'ouvre que des adresses http. Il n'écoute que ce
    // poste (127.0.0.1). Une seule session le tient ; les autres réessaient à
    // chaque battement, pour prendre le relais quand elle se ferme.
    const lancerServeur = () => {
      if (!dossier || isServeurLance) return
      isServeurLance = true
      const vue = `${dossier}/vue`
      void (async () => {
        try {
          const serveur = $.process.spawn({
            argv: ['python', '-m', 'http.server', String(PORT), '--bind', '127.0.0.1', '--directory', vue],
          })
          for await (const _ligne of serveur) {
            // Le serveur note chaque requête ; rien à en faire.
          }
        } catch {
          // Python absent, ou port déjà pris par une autre session.
        } finally {
          isServeurLance = false
        }
      })()
    }
    lancerServeur()
    await inscrire($, true)
    battement?.cancel()
    battement = $.clock.every(10000, () => {
      lancerServeur()
      void inscrire($, true)
      void publier($)
    })
    await $.command.register({
      name: 'bureau',
      description: 'Reconvertit les images du bureau et ouvre le résumé des agents',
    })
    // Pas d'ouverture automatique du panneau : la ville vit dans la page web,
    // et le panneau s'ouvre sur demande seulement (/bureau).
    try {
      const usage = await $.session.usage()
      await update($, limits, () => usage.rateLimits)
      mesure = await $.clock.now()
      await update($, main, m => ({ ...m, contexte: usage.context, cout: usage.cost?.usd }))
    } catch {
      // Pas encore de mesure : la ligne d'utilisation attendra session.measure.
    }
    // Le modèle se lit dès le départ ; l'effort et le cache attendent la
    // première requête.
    try {
      const modele = await $.session.model()
      await update($, main, m => ({ ...m, modele: m.modele ?? modele }))
    } catch {
      // Pas de modèle encore : la première requête le dira.
    }
    await publier($)

    // Filet de sécurité : un agent qui a fini sans qu'on l'entende part quand
    // même, et ceux qui sont partis depuis longtemps quittent la liste.
    menage?.cancel()
    menage = $.clock.every(3000, () => {
      void (async () => {
        let [liste, vivants, maintenant] = await Promise.all([
          read($, agents),
          $.agent.list(),
          $.clock.now(),
        ])
        const actifs = new Set(vivants.filter(v => EN_COURS.includes(v.status)).map(v => v.id))
        // Un agent relancé qu'on n'a pas entendu reprendre revient quand même.
        let revenus = false
        for (const id of actifs) revenus = (await revenir($, id)) || revenus
        if (revenus) liste = await read($, agents)
        const suite = liste
          .filter(a => a.leftAt === undefined || maintenant - a.leftAt < 15000)
          .map(a => (a.leftAt === undefined && !actifs.has(a.id) ? { ...a, leftAt: maintenant } : a))
        if (JSON.stringify(suite) !== JSON.stringify(liste)) {
          await update($, agents, () => suite)
          await publier($)
        }
      })()
    })

    return next(e)
  })

  // La maison disparaît de la ville tout de suite, sans attendre que son
  // battement s'éteigne.
  on('session.end', async ($, e, next) => {
    battement?.cancel()
    prochainReleve?.cancel()
    await Promise.all([publier($, true), inscrire($, false)])

    return next(e)
  })

  // /bureau : reconvertit les PNG (outils/construire.py), relit, et ouvre.
  on('command.run', { command: 'bureau' }, async $ => {
    let rapport = 'Images reconverties.'
    try {
      if (!dossier) await charger($)
      const r = await $.process.run(['python', `${dossier}/outils/construire.py`], {
        cwd: dossier,
        timeoutMs: 120000,
      })
      if (r.exitCode !== 0) rapport = `La conversion a échoué ; la ville garde ses images d'avant.\n${r.stderr}`
    } catch (err) {
      rapport = `Python introuvable ; la ville garde ses images d'avant. (${String(err)})`
    }
    await charger($)
    await publier($)
    $.ui.invalidate('ui.render')
    await $.ui.open({ id: PANE, title: 'Bureau' })

    return {
      text:
        probleme ??
        `${rapport} Recharge la page pour voir les nouvelles images.\nDans VS Code : Ctrl+Maj+P, « Open Integrated Browser », puis ${ADRESSE}\nDans Edge : ouvre ${dossier}/vue/bureau.html, puis F11.`,
    }
  })

  on('session.measure', async ($, e, next) => {
    await update($, limits, () => e.rateLimits)
    mesure = await $.clock.now()
    await update($, main, m => ({ ...m, contexte: e.context, cout: e.cost?.usd ?? m.cout }))
    await publier($)

    return next(e)
  })

  // Chaque requête au modèle. Pour le gestionnaire : quel modèle, quel effort,
  // et quand la réponse a fini (le cache du contexte court à partir de là).
  // Pour un agent : la fiche de sa carte (modèle, effort, requêtes, contexte,
  // jetons écrits).
  on('turn.step', async function* ($, e, next) {
    const r = yield* next(e)
    if (e.agentId === undefined) {
      const maintenant = await $.clock.now()
      const effort = e.effort === undefined ? undefined : String(e.effort)
      const out = r.usage?.output_tokens ?? 0
      await update($, main, m => ({ ...m, modele: e.model, effort, reponse: maintenant, req: (m.req ?? 0) + 1, out: (m.out ?? 0) + out }))
      await publier($)
    } else {
      const u = r.usage
      const effort = e.effort === undefined ? undefined : String(e.effort)
      const ctx = u ? u.input_tokens + u.cache_read_input_tokens + u.cache_creation_input_tokens : undefined
      await update($, agents, liste =>
        liste.map(a =>
          a.id === e.agentId
            ? { ...a, modele: e.model, effort, req: (a.req ?? 0) + 1, ctx: ctx ?? a.ctx, out: (a.out ?? 0) + (u?.output_tokens ?? 0) }
            : a,
        ),
      )
    }

    return r
  })

  on('agent.spawn', async ($, e, next) => {
    const r = await next(e)
    const id = 'agentId' in r ? r.agentId : undefined
    if (id) {
      const maintenant = await $.clock.now()
      const postes = plan?.postes.length ?? 0
      const fiche: Agent = {
        id,
        type: e.subagentType,
        description: e.description,
        desk: -1,
        enteredAt: maintenant,
        notebook: devinerNotebook(`${e.description} ${e.prompt}`),
        parent: e.parentAgentId,
      }
      connus.set(id, fiche)
      await noter($, `→ ${nomDe(e.subagentType)} · ${e.description}`)
      await update($, agents, liste => {
        const pris = new Set(liste.filter(a => a.leftAt === undefined).map(a => a.desk))
        const libre = Array.from({ length: postes }, (_, i) => i).find(i => !pris.has(i))
        return [...liste, { ...fiche, desk: libre ?? -1 }]
      })
      await publier($)
    }

    return r
  })

  on('turn.start', async ($, e, next) => {
    if (e.agentId === undefined) {
      await update($, main, m => ({ ...m, isWorking: true }))
      await publier($)
    } else if (await revenir($, e.agentId)) {
      await publier($)
    }

    return next(e)
  })

  on('turn.complete', async ($, e, next) => {
    const r = await next(e)
    if (e.agentId === undefined) {
      // Le tour fini efface ce qu'il faisait, pas sa fiche (modèle, effort, contexte, cache).
      await update($, main, ({ modele, effort, reponse, contexte, req, cout, out }) => ({ isWorking: false, modele, effort, reponse, contexte, req, cout, out, permission: false }))
    } else {
      // Sa conclusion décide s'il sacre, s'il a des remarques ou s'il coche en vert.
      const conclusion = conclure(r.text ?? '')
      const maintenant = await $.clock.now()
      const conclu = conclusion === 'erreurs' ? ' · erreurs' : conclusion === 'remarques' ? ' · remarques' : ''
      await noter($, `✓ ${qui(e.agentId)} fini${conclu}`)
      await update($, agents, liste =>
        liste.map(a =>
          a.id === e.agentId && a.leftAt === undefined ? { ...a, leftAt: maintenant, conclusion } : a,
        ),
      )
    }
    await publier($)

    return r
  })

  on('tool.call', async ($, e, next) => {
    const { texte, glyph } = decrire(e)
    const isPrincipal = e.agentId === undefined
    // Le journal : les fichiers modifiés et les erreurs d'outil, une fois l'outil fini.
    const journaliser = async <R extends { isError?: boolean }>(r: R): Promise<R> => {
      await lever($, e.agentId)
      if (r.isError) await noter($, `✗ ${qui(e.agentId)} · ${texte}`)
      else if (ECRIRE.includes(e.tool)) await noter($, `✎ ${qui(e.agentId)} · ${texte}`)
      if (r.isError || ECRIRE.includes(e.tool)) await publier($)

      return r
    }
    if (isPrincipal) {
      await update($, main, m => ({ ...m, activity: texte, glyph }))
    } else if ((await revenir($, e.agentId)) || (await read($, agents)).some(a => a.id === e.agentId)) {
      await update($, agents, liste =>
        liste.map(a => (a.id === e.agentId ? { ...a, activity: texte, glyph } : a)),
      )
    }
    await publier($)

    // L'essai du rédacteur (tests, vérification de l'app) : la page envoie
    // l'employé à la photocopieuse, et le verdict allume le voyant vert ou rouge.
    const commande = (e as unknown as { command?: unknown }).command
    if (!isPrincipal && COMMANDE.includes(e.tool) && typeof commande === 'string' && ESSAI.test(commande)) {
      await update($, agents, liste =>
        liste.map(a => (a.id === e.agentId ? { ...a, controles: (a.controles ?? 0) + 1 } : a)),
      )
      const r = await next(e)
      // Chaque passage garde son verdict : la page fait un aller-retour par passage.
      const verdict = r.isError ? 'ecarts' : 'ok'
      await update($, agents, liste =>
        liste.map(a => (a.id === e.agentId ? { ...a, verdicts: [...(a.verdicts ?? []), verdict] } : a)),
      )
      await publier($)

      return journaliser(r)
    }
    // Un commit ou un push du gestionnaire : git est relu une fois la commande
    // terminée (next rend la main après), donc le commit est déjà écrit.
    if (isPrincipal && COMMANDE.includes(e.tool) && typeof commande === 'string' && /\bgit\b[^|;&]*\b(commit|push)\b/.test(commande)) {
      const r = await next(e)
      if (!r.isError) await noter($, /\bpush\b/.test(commande) ? '● push' : '● commit')
      await relever($)

      return journaliser(r)
    }
    if (!isPrincipal || e.tool !== 'Agent') return journaliser(await next(e))

    // Le gestionnaire attend (et fume) pendant qu'un agent qu'il a lancé travaille.
    await update($, main, m => ({ ...m, attente: (m.attente ?? 0) + 1 }))
    await publier($)
    try {
      return await next(e)
    } finally {
      await update($, main, m => ({ ...m, attente: Math.max(0, (m.attente ?? 1) - 1) }))
      await publier($)
    }
  })

  // Une demande de permission, de Claude ou d'un agent : au journal, et la page
  // marque celui qui attend (✋) jusqu'à la fin de l'outil demandé.
  on('classic.PermissionRequest', async ($, e, next) => {
    await noter($, `? ${qui(e.agent_id)} demande ${e.tool_name}`)
    if (e.agent_id === undefined) await update($, main, m => ({ ...m, permission: true }))
    else await update($, agents, l => l.map(a => (a.id === e.agent_id ? { ...a, permission: true } : a)))
    await publier($)

    return next(e)
  })

  on('tool.call', { tool: NOM_OUTIL_ETAPES }, async ($, e) => {
    const lu = lireEtapes(e)
    if (typeof lu === 'string') return { deny: lu }
    const liste = { ...lu, maj: await $.clock.now() }
    await update($, etapes, () => liste)
    await $.store.set(cleEtapes(), liste)
    await publier($)
    const reste = liste.etapes.filter(x => x.etat !== 'fait').length

    return { result: `Liste affichée : ${liste.etapes.length} étapes, ${reste} à faire ou en cours.` }
  })

  on('ui.render', { component: 'Pane', requestId: PANE }, async ($, e) => {
    const { Box, Text } = $.ui.resolve(e)
    const [liste, m, lim, maintenant] = await Promise.all([read($, agents), read($, main), read($, limits), $.clock.now()])
    const presents = liste.filter(a => a.leftAt === undefined)

    return (
      <Box flexDirection="column">
        {probleme ? <Text color="red">{probleme}</Text> : null}
        <Text>{ligneLimites(lim, maintenant)}</Text>
        <Text>
          Gestionnaire (Claude) :{' '}
          {(m.attente ?? 0) > 0 ? 'attend ses agents' : m.isWorking ? (m.activity ?? 'réfléchit') : 'au repos'}
        </Text>
        {presents.map(a => (
          <Text>
            {personnageDe(a.type)} · {a.type}
            {a.notebook ? ` · ${a.notebook}` : ''} ({a.description}) : {a.activity ?? 'arrive'}
          </Text>
        ))}
        <Text dimColor>La ville : {ADRESSE}</Text>
      </Box>
    )
  })
}
