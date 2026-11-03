// Un subagent : son entrée, sa sortie, son notebook et ce qu'il fait.
export type Agent = {
  id: string
  type: string
  description: string
  // Index d'un poste libre au départ ; la page place elle-même les agents.
  desk: number
  enteredAt: number
  leftAt?: number
  notebook?: string
  // L'agent qui l'a lancé (un rédacteur qui appelle son auditeur), s'il y en a un.
  parent?: string
  // Sa conclusion, lue sur la ligne « Bilan » de sa réponse finale : des ⛔, des ⚠ seulement, ou rien.
  conclusion?: 'ok' | 'remarques' | 'erreurs'
  // Contrôles mécaniques lancés, et le verdict de chacun, dans l'ordre.
  controles?: number
  verdicts?: ('ok' | 'ecarts')[]
  activity?: string
  glyph?: string
  // Sa dernière requête au modèle : modèle, effort ; req : ses requêtes ;
  // ctx : l'entrée de la dernière (son contexte), out : ce qu'il a écrit en tout.
  modele?: string
  effort?: string
  req?: number
  ctx?: number
  out?: number
  // Une demande de permission l'attend : vrai jusqu'à la fin de l'outil demandé.
  permission?: boolean
}

// Claude, le gestionnaire. attente : agents lancés qu'il attend en ce moment.
// modele, effort : ceux de sa dernière requête ; reponse : quand elle a fini
// (le cache court à partir de là) ; contexte : sa fenêtre de contexte.
// req : ses propres requêtes au modèle ; cout : ce que la session aurait coûté
// au prix de l'API, agents compris, en dollars US (comme /cost).
export type Main = {
  isWorking: boolean
  attente?: number
  activity?: string
  glyph?: string
  modele?: string
  effort?: string
  reponse?: number
  contexte?: { tokens?: number; window: number; percent?: number }
  req?: number
  cout?: number
  // Les jetons qu'il a écrits en tout, comme « out » d'un agent.
  out?: number
  // Une demande de permission l'attend : vrai jusqu'à la fin de l'outil demandé.
  permission?: boolean
}

// Une ligne du journal : quand, et ce qui s'est passé.
export type Ligne = { t: number; texte: string }

export type Limit = { kind: string; percentUsed: number; resetsAt?: string }

// La liste d'étapes que Claude tient à jour pour la personne, par l'outil
// « etapes » ; la page l'affiche dans le panneau de droite du bureau.
// code : un bloc à copier tel quel (paramètres, requête), affiché en police fixe.
export type Etape = { texte: string; etat: 'fait' | 'en_cours' | 'a_faire'; details?: string[]; code?: string }
export type Etapes = { titre?: string; etapes: Etape[]; notes?: string[]; maj?: number }

declare module 'claude-code' {
  interface PluginState {
    'bureau-agents': { agents: Agent[]; main: Main; limits: Limit[]; etapes: Etapes; journal: Ligne[] }
  }
}
