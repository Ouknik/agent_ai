"""
PROJET AI - AGENT DE SÉCURITÉ INTELLIGENT
Système de surveillance et détection dans un bâtiment
"""

from collections import deque
import heapq

# ============================================================================
# ÉTAPE 1 - CONSTRUCTION DU GRAPHE
# ============================================================================

# Graphe représentant le bâtiment avec 12 zones
# Coût = temps de déplacement en minutes
graphe = {
    'Poste_Securite': [('Entrée', 2), ('Hall', 3)],
    'Entrée': [('Poste_Securite', 2), ('Hall', 1)],
    'Hall': [('Poste_Securite', 3), ('Entrée', 1), ('Couloir_A', 2), ('Couloir_B', 2), ('Cafeteria', 4)],
    'Couloir_A': [('Hall', 2), ('Bureau_1', 3), ('Salle_Serveurs', 5)],
    'Couloir_B': [('Hall', 2), ('Bureau_2', 3), ('Parking', 4)],
    'Bureau_1': [('Couloir_A', 3), ('Sortie_Urgence', 6)],
    'Bureau_2': [('Couloir_B', 3), ('Cafeteria', 3)],
    'Parking': [('Couloir_B', 4), ('Sortie_Urgence', 7)],
    'Salle_Serveurs': [('Couloir_A', 5), ('Toit', 4)],
    'Sortie_Urgence': [('Bureau_1', 6), ('Parking', 7)],
    'Cafeteria': [('Hall', 4), ('Bureau_2', 3), ('Toit', 5)],
    'Toit': [('Salle_Serveurs', 4), ('Cafeteria', 5)]
}

print("=" * 80)
print("ÉTAPE 1 - GRAPHE DU BÂTIMENT")
print("=" * 80)
print(f"\n📊 Nombre de zones: {len(graphe)}")
print(f"🔗 Zones: {', '.join(graphe.keys())}\n")

for zone, voisins in graphe.items():
    print(f"{zone}: {voisins}")


# ============================================================================
# ÉTAPE 2 - FORMULATION DU PROBLÈME
# ============================================================================

class ProblemeSurveillance:
    """Classe représentant le problème de surveillance"""
    
    def __init__(self, etat_initial, etat_but, graphe):
        self.etat_initial = etat_initial
        self.etat_but = etat_but
        self.graphe = graphe
    
    def actions(self, etat):
        """Retourne les actions possibles depuis un état"""
        return [voisin for voisin, cout in self.graphe.get(etat, [])]
    
    def resultat(self, etat, action):
        """Retourne l'état résultant d'une action"""
        return action
    
    def cout(self, etat, action):
        """Retourne le coût d'une action"""
        for voisin, cout in self.graphe.get(etat, []):
            if voisin == action:
                return cout
        return float('inf')
    
    def test_but(self, etat):
        """Teste si l'état est le but"""
        return etat == self.etat_but
    
    def successeurs(self, etat):
        """Retourne les successeurs avec leurs coûts"""
        return [(action, self.resultat(etat, action), self.cout(etat, action)) 
                for action in self.actions(etat)]


# Définition du problème : Alerte détectée à la Salle_Serveurs
etat_initial = "Poste_Securite"
etat_but = "Salle_Serveurs"
probleme = ProblemeSurveillance(etat_initial, etat_but, graphe)

print("\n" + "=" * 80)
print("ÉTAPE 2 - FORMULATION DU PROBLÈME")
print("=" * 80)
print(f"\n🚨 ALERTE: Mouvement suspect détecté!")
print(f"📍 État initial: {etat_initial}")
print(f"🎯 État but: {etat_but}")


# ============================================================================
# ÉTAPE 3 - VALIDATION DU PROBLÈME
# ============================================================================

print("\n" + "=" * 80)
print("ÉTAPE 3 - VALIDATION DU PROBLÈME")
print("=" * 80)

print(f"\n✅ Actions possibles depuis {etat_initial}:")
actions_possibles = probleme.actions(etat_initial)
print(f"   {actions_possibles}")

print(f"\n✅ Test du but:")
print(f"   {etat_initial} est le but ? {probleme.test_but(etat_initial)}")
print(f"   {etat_but} est le but ? {probleme.test_but(etat_but)}")

print(f"\n✅ Successeurs de {etat_initial}:")
for action, succ, cout in probleme.successeurs(etat_initial):
    print(f"   Action: {action} → Successeur: {succ}, Coût: {cout}")

print(f"\n✅ Vérification cohérence du graphe:")
total_aretes = sum(len(voisins) for voisins in graphe.values())
print(f"   Nombre total d'arêtes: {total_aretes // 2} (bidirectionnelles)")


# ============================================================================
# ÉTAPE 4 - ALGORITHMES DE RECHERCHE
# ============================================================================

class Noeud:
    """Classe représentant un nœud dans l'arbre de recherche"""
    
    def __init__(self, etat, parent=None, action=None, cout=0):
        self.etat = etat
        self.parent = parent
        self.action = action
        self.cout = cout
        self.profondeur = 0 if parent is None else parent.profondeur + 1
    
    def chemin(self):
        """Reconstruit le chemin depuis la racine"""
        noeud, chemin = self, []
        while noeud:
            chemin.append(noeud.etat)
            noeud = noeud.parent
        return list(reversed(chemin))
    
    def __lt__(self, autre):
        return self.cout < autre.cout


def BFS(probleme):
    """Breadth-First Search (Parcours en largeur)"""
    noeud_initial = Noeud(probleme.etat_initial)
    
    if probleme.test_but(noeud_initial.etat):
        return noeud_initial, 1
    
    frontiere = deque([noeud_initial])
    explores = set()
    noeuds_explores = 0
    
    while frontiere:
        noeud = frontiere.popleft()
        explores.add(noeud.etat)
        noeuds_explores += 1
        
        for action, succ, cout in probleme.successeurs(noeud.etat):
            enfant = Noeud(succ, noeud, action, noeud.cout + cout)
            
            if enfant.etat not in explores and enfant not in frontiere:
                if probleme.test_but(enfant.etat):
                    return enfant, noeuds_explores
                frontiere.append(enfant)
    
    return None, noeuds_explores


def DFS(probleme):
    """Depth-First Search (Parcours en profondeur)"""
    noeud_initial = Noeud(probleme.etat_initial)
    
    if probleme.test_but(noeud_initial.etat):
        return noeud_initial, 1
    
    frontiere = [noeud_initial]
    explores = set()
    noeuds_explores = 0
    
    while frontiere:
        noeud = frontiere.pop()
        
        if noeud.etat in explores:
            continue
            
        explores.add(noeud.etat)
        noeuds_explores += 1
        
        if probleme.test_but(noeud.etat):
            return noeud, noeuds_explores
        
        for action, succ, cout in reversed(probleme.successeurs(noeud.etat)):
            if succ not in explores:
                enfant = Noeud(succ, noeud, action, noeud.cout + cout)
                frontiere.append(enfant)
    
    return None, noeuds_explores


def UCS(probleme):
    """Uniform Cost Search (Recherche à coût uniforme)"""
    noeud_initial = Noeud(probleme.etat_initial)
    frontiere = []
    heapq.heappush(frontiere, (0, id(noeud_initial), noeud_initial))
    explores = {}
    noeuds_explores = 0
    
    while frontiere:
        _, _, noeud = heapq.heappop(frontiere)
        
        if probleme.test_but(noeud.etat):
            return noeud, noeuds_explores
        
        if noeud.etat in explores and explores[noeud.etat] <= noeud.cout:
            continue
        
        explores[noeud.etat] = noeud.cout
        noeuds_explores += 1
        
        for action, succ, cout in probleme.successeurs(noeud.etat):
            enfant = Noeud(succ, noeud, action, noeud.cout + cout)
            if succ not in explores or explores[succ] > enfant.cout:
                heapq.heappush(frontiere, (enfant.cout, id(enfant), enfant))
    
    return None, noeuds_explores


# ============================================================================
# ÉTAPE 5 - HEURISTIQUE
# ============================================================================

# Heuristique: Distance estimée (nombre minimal de transitions)
# Cette heuristique est admissible car elle ne surestime jamais le coût réel
heuristique = {
    'Poste_Securite': 3,  # 3 transitions minimum vers Salle_Serveurs
    'Entrée': 3,
    'Hall': 2,
    'Couloir_A': 1,
    'Couloir_B': 4,
    'Bureau_1': 2,
    'Bureau_2': 5,
    'Parking': 5,
    'Salle_Serveurs': 0,  # But atteint
    'Sortie_Urgence': 3,
    'Cafeteria': 3,
    'Toit': 1
}


def A_star(probleme, heuristique):
    """A* Search (A étoile)"""
    noeud_initial = Noeud(probleme.etat_initial)
    f_initial = noeud_initial.cout + heuristique[noeud_initial.etat]
    
    frontiere = []
    heapq.heappush(frontiere, (f_initial, id(noeud_initial), noeud_initial))
    explores = {}
    noeuds_explores = 0
    
    while frontiere:
        _, _, noeud = heapq.heappop(frontiere)
        
        if probleme.test_but(noeud.etat):
            return noeud, noeuds_explores
        
        if noeud.etat in explores and explores[noeud.etat] <= noeud.cout:
            continue
        
        explores[noeud.etat] = noeud.cout
        noeuds_explores += 1
        
        for action, succ, cout in probleme.successeurs(noeud.etat):
            enfant = Noeud(succ, noeud, action, noeud.cout + cout)
            f = enfant.cout + heuristique[succ]
            
            if succ not in explores or explores[succ] > enfant.cout:
                heapq.heappush(frontiere, (f, id(enfant), enfant))
    
    return None, noeuds_explores


# Exécution des algorithmes
print("\n" + "=" * 80)
print("ÉTAPE 4 & 5 - EXÉCUTION DES ALGORITHMES")
print("=" * 80)

algorithmes = [
    ("BFS (Breadth-First Search)", lambda: BFS(probleme)),
    ("DFS (Depth-First Search)", lambda: DFS(probleme)),
    ("UCS (Uniform Cost Search)", lambda: UCS(probleme)),
    ("A* (A étoile)", lambda: A_star(probleme, heuristique))
]

resultats = []

for nom, algo in algorithmes:
    print(f"\n{'=' * 40}")
    print(f"🔍 {nom}")
    print('=' * 40)
    
    solution, noeuds_explores = algo()
    
    if solution:
        chemin = solution.chemin()
        print(f"✅ Solution trouvée!")
        print(f"📍 Chemin: {' → '.join(chemin)}")
        print(f"💰 Coût total: {solution.cout} minutes")
        print(f"🔢 Nœuds explorés: {noeuds_explores}")
        print(f"📏 Longueur du chemin: {len(chemin)} zones")
        
        resultats.append({
            'nom': nom,
            'chemin': chemin,
            'cout': solution.cout,
            'noeuds': noeuds_explores,
            'longueur': len(chemin)
        })
    else:
        print("❌ Aucune solution trouvée")


# ============================================================================
# TABLEAU COMPARATIF
# ============================================================================

print("\n" + "=" * 80)
print("TABLEAU COMPARATIF DES ALGORITHMES")
print("=" * 80)
print(f"\n{'Algorithme':<30} {'Coût':<10} {'Nœuds':<15} {'Longueur':<10}")
print("-" * 65)

for r in resultats:
    print(f"{r['nom']:<30} {r['cout']:<10} {r['noeuds']:<15} {r['longueur']:<10}")


# ============================================================================
# ÉTAPE 6 - SIMULATION DE L'AGENT
# ============================================================================

class AgentSurveillance:
    """Agent intelligent de surveillance"""
    
    def __init__(self, probleme):
        self.probleme = probleme
        self.position = probleme.etat_initial
        self.strategie = None
        self.chemin = []
    
    def choisir_strategie(self, nom_strategie):
        """Choisit l'algorithme de recherche"""
        strategies = {
            'BFS': BFS,
            'DFS': DFS,
            'UCS': UCS,
            'A*': lambda p: A_star(p, heuristique)
        }
        self.strategie = strategies.get(nom_strategie)
        return self.strategie is not None
    
    def executer(self):
        """Exécute la mission de surveillance"""
        if not self.strategie:
            return False
        
        print(f"\n🤖 Agent initialisé à: {self.position}")
        print(f"🎯 Objectif: Atteindre {self.probleme.etat_but}")
        print(f"⚙️  Stratégie: {self.strategie.__name__}\n")
        
        solution, noeuds = self.strategie(self.probleme)
        
        if solution:
            self.chemin = solution.chemin()
            print("📋 SÉQUENCE DE DÉPLACEMENT:")
            print("-" * 50)
            
            for i, zone in enumerate(self.chemin):
                if i == 0:
                    print(f"  Étape {i+1}: 🟢 Départ de {zone}")
                elif i == len(self.chemin) - 1:
                    print(f"  Étape {i+1}: 🔴 Arrivée à {zone} - ALERTE TRAITÉE ✓")
                else:
                    print(f"  Étape {i+1}: ⚪ Transit par {zone}")
            
            print(f"\n✅ Mission accomplie en {solution.cout} minutes")
            print(f"📊 Efficacité: {noeuds} nœuds explorés")
            return True
        else:
            print("❌ Échec: Impossible d'atteindre l'objectif")
            return False


print("\n" + "=" * 80)
print("ÉTAPE 6 - SIMULATION DE L'AGENT")
print("=" * 80)

# Création et exécution de l'agent avec A*
agent = AgentSurveillance(probleme)
agent.choisir_strategie('A*')
agent.executer()


# ============================================================================
# ANALYSE FINALE
# ============================================================================

print("\n" + "=" * 80)
print("ANALYSE DES PERFORMANCES")
print("=" * 80)

print("\n📊 COMPARAISON:")
print("-" * 50)
print("• BFS: Trouve le chemin optimal en nombre d'étapes")
print("• DFS: Rapide mais ne garantit pas l'optimalité")
print("• UCS: Trouve le chemin de coût minimal")
print("• A*: Le plus efficace (optimal + moins de nœuds explorés)")

print("\n🏆 ALGORITHME RECOMMANDÉ: A*")
print("-" * 50)
print("Raisons:")
print("  ✓ Trouve le chemin optimal (même coût que UCS)")
print("  ✓ Explore moins de nœuds grâce à l'heuristique")
print("  ✓ Idéal pour des situations d'urgence (efficacité)")
print("  ✓ Adapté à notre problème de surveillance")

print("\n" + "=" * 80)
print("FIN DE LA SIMULATION")
print("=" * 80)