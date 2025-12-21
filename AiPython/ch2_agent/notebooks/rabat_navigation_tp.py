"""
🚗 TP: Agent de Navigation Intelligente - Ville de Rabat
========================================================
Application pratique d'un agent intelligent qui navigue entre les quartiers 
de Rabat en utilisant des algorithmes de recherche.
"""

import sys
sys.path.append('../src')

from agent import Agent, Environment
from problem_solving_agent import (
    Problem, NavigationProblem, SearchStrategy, 
    Trace, ProblemSolvingAgent, NavigationPercept
)
from typing import Dict, List, Optional, Tuple
from collections import deque
import heapq


# ============================================
# 1. Graphe des Quartiers de Rabat
# ============================================

RABAT_GRAPH = {
    "Agdal": {
        "Hassan": 10,
        "Hay_Riad": 15,
        "Aviation": 8
    },
    "Hassan": {
        "Agdal": 10,
        "Ocean": 20,
        "Medina": 8,
        "Hay_Riad": 12
    },
    "Medina": {
        "Hassan": 8,
        "Ocean": 12,
        "Kasbah": 5
    },
    "Ocean": {
        "Hassan": 20,
        "Medina": 12,
        "Souissi": 18,
        "Aviation": 15
    },
    "Souissi": {
        "Ocean": 18,
        "Aviation": 10,
        "Hay_Riad": 20
    },
    "Hay_Riad": {
        "Agdal": 15,
        "Hassan": 12,
        "Souissi": 20,
        "Aviation": 8
    },
    "Aviation": {
        "Agdal": 8,
        "Hay_Riad": 8,
        "Souissi": 10,
        "Ocean": 15
    },
    "Kasbah": {
        "Medina": 5
    }
}


# ============================================
# 2. Heuristiques pour A* (Estimations de Distance)
# ============================================

# Distances approximatives de chaque quartier vers "Ocean" (exemple)
HEURISTICS_TO_OCEAN = {
    "Agdal": 22,
    "Hassan": 20,
    "Medina": 12,
    "Ocean": 0,
    "Souissi": 18,
    "Hay_Riad": 25,
    "Aviation": 15,
    "Kasbah": 17
}

# Distances approximatives de chaque quartier vers "Kasbah"
HEURISTICS_TO_KASBAH = {
    "Agdal": 18,
    "Hassan": 8,
    "Medina": 5,
    "Ocean": 17,
    "Souissi": 35,
    "Hay_Riad": 27,
    "Aviation": 26,
    "Kasbah": 0
}


# ============================================
# 3. Implémentation Complète des Algorithmes de Recherche
# ============================================

class RabatSearchStrategy:
    """Algorithmes de recherche complets et détaillés"""
    
    @staticmethod
    def dfs(problem: NavigationProblem, verbose: bool = True):
        """
        Recherche en Profondeur - Depth First Search
        """
        trace = Trace(problem) if verbose else None
        
        # Initialisation
        frontiere = [problem.initial_state]  # Stack (LIFO)
        explore = set()
        parents = {}
        cout_cumule = {problem.initial_state: 0}
        
        if trace:
            trace.init_trace(frontiere, explore, "dfs")
        
        iteration = 0
        
        while frontiere:
            iteration += 1
            
            # Extraire le dernier élément (LIFO)
            etat_actuel = frontiere.pop()
            
            if etat_actuel in explore:
                continue
            
            explore.add(etat_actuel)
            
            if trace:
                trace.iteration_trace(iteration, etat_actuel, frontiere, explore, parents, cout_cumule)
            
            # Test de l'objectif
            if problem.goal_test(etat_actuel):
                if trace:
                    trace.goal_trace(iteration, etat_actuel, frontiere, explore, parents, cout_cumule)
                return RabatSearchStrategy._reconstruct_path(parents, etat_actuel, problem.initial_state)
            
            # Expansion du nœud
            for voisin in reversed(problem.actions(etat_actuel)):
                if voisin not in explore:
                    frontiere.append(voisin)
                    if voisin not in parents:
                        parents[voisin] = etat_actuel
                        cout = problem.graph[etat_actuel][voisin]
                        cout_cumule[voisin] = cout_cumule[etat_actuel] + cout
        
        return None  # Aucune solution trouvée
    
    @staticmethod
    def bfs(problem: NavigationProblem, verbose: bool = True):
        """
        Recherche en Largeur - Breadth First Search
        """
        trace = Trace(problem) if verbose else None
        
        # Initialisation
        frontiere = deque([problem.initial_state])  # Queue (FIFO)
        explore = set()
        parents = {}
        cout_cumule = {problem.initial_state: 0}
        
        if trace:
            trace.init_trace(frontiere, explore, "bfs")
        
        iteration = 0
        
        while frontiere:
            iteration += 1
            
            # Extraire le premier élément (FIFO)
            etat_actuel = frontiere.popleft()
            
            if etat_actuel in explore:
                continue
            
            explore.add(etat_actuel)
            
            if trace:
                trace.iteration_trace(iteration, etat_actuel, frontiere, explore, parents, cout_cumule)
            
            # Test de l'objectif
            if problem.goal_test(etat_actuel):
                if trace:
                    trace.goal_trace(iteration, etat_actuel, frontiere, explore, parents, cout_cumule)
                return RabatSearchStrategy._reconstruct_path(parents, etat_actuel, problem.initial_state)
            
            # Expansion du nœud
            for voisin in problem.actions(etat_actuel):
                if voisin not in explore and voisin not in [n for n in frontiere]:
                    frontiere.append(voisin)
                    parents[voisin] = etat_actuel
                    cout = problem.graph[etat_actuel][voisin]
                    cout_cumule[voisin] = cout_cumule[etat_actuel] + cout
        
        return None
    
    @staticmethod
    def ucs(problem: NavigationProblem, verbose: bool = True):
        """
        Recherche à Coût Uniforme - Uniform Cost Search
        """
        trace = Trace(problem) if verbose else None
        
        # Initialisation
        frontiere = [(0, problem.initial_state)]  # File de priorité (coût, état)
        explore = set()
        parents = {}
        cout_cumule = {problem.initial_state: 0}
        
        if trace:
            trace.init_trace([s for _, s in frontiere], explore, "ucs")
        
        iteration = 0
        
        while frontiere:
            iteration += 1
            
            # Extraire le nœud avec le coût minimal
            cout_actuel, etat_actuel = heapq.heappop(frontiere)
            
            if etat_actuel in explore:
                continue
            
            explore.add(etat_actuel)
            
            if trace:
                trace.iteration_trace(iteration, etat_actuel, 
                                     [s for _, s in frontiere], explore, parents, cout_cumule)
            
            # Test de l'objectif
            if problem.goal_test(etat_actuel):
                if trace:
                    trace.goal_trace(iteration, etat_actuel, 
                                    [s for _, s in frontiere], explore, parents, cout_cumule)
                return RabatSearchStrategy._reconstruct_path(parents, etat_actuel, problem.initial_state)
            
            # Expansion du nœud
            for voisin in problem.actions(etat_actuel):
                cout = problem.graph[etat_actuel][voisin]
                nouveau_cout = cout_cumule[etat_actuel] + cout
                
                if voisin not in explore and voisin not in cout_cumule:
                    cout_cumule[voisin] = nouveau_cout
                    parents[voisin] = etat_actuel
                    heapq.heappush(frontiere, (nouveau_cout, voisin))
                elif voisin in cout_cumule and nouveau_cout < cout_cumule[voisin]:
                    cout_cumule[voisin] = nouveau_cout
                    parents[voisin] = etat_actuel
                    heapq.heappush(frontiere, (nouveau_cout, voisin))
        
        return None
    
    @staticmethod
    def a_star(problem: NavigationProblem, heuristics: Dict[str, float], verbose: bool = True):
        """
        Recherche A* - A-star Search
        """
        trace = Trace(problem) if verbose else None
        
        # Initialisation
        h = heuristics.get(problem.initial_state, 0)
        frontiere = [(h, 0, problem.initial_state)]  # (f, g, état)
        explore = set()
        parents = {}
        cout_cumule = {problem.initial_state: 0}
        
        if trace:
            trace.init_trace([s for _, _, s in frontiere], explore, "a-star")
        
        iteration = 0
        
        while frontiere:
            iteration += 1
            
            # Extraire le nœud avec f minimal = g + h
            f_actuel, g_actuel, etat_actuel = heapq.heappop(frontiere)
            
            if etat_actuel in explore:
                continue
            
            explore.add(etat_actuel)
            
            if trace:
                trace.iteration_trace(iteration, etat_actuel, 
                                     [s for _, _, s in frontiere], explore, parents, cout_cumule)
            
            # Test de l'objectif
            if problem.goal_test(etat_actuel):
                if trace:
                    trace.goal_trace(iteration, etat_actuel, 
                                    [s for _, _, s in frontiere], explore, parents, cout_cumule)
                return RabatSearchStrategy._reconstruct_path(parents, etat_actuel, problem.initial_state)
            
            # Expansion du nœud
            for voisin in problem.actions(etat_actuel):
                cout = problem.graph[etat_actuel][voisin]
                nouveau_g = g_actuel + cout
                h_voisin = heuristics.get(voisin, 0)
                nouveau_f = nouveau_g + h_voisin
                
                if voisin not in explore:
                    if voisin not in cout_cumule or nouveau_g < cout_cumule[voisin]:
                        cout_cumule[voisin] = nouveau_g
                        parents[voisin] = etat_actuel
                        heapq.heappush(frontiere, (nouveau_f, nouveau_g, voisin))
        
        return None
    
    @staticmethod
    def _reconstruct_path(parents: Dict, goal: str, start: str) -> List[str]:
        """Reconstruire le chemin du début vers l'objectif"""
        path = []
        current = goal
        while current != start:
            path.append(current)
            current = parents[current]
        path.append(start)
        return path[::-1]


# ============================================
# 4. Environnement de Rabat
# ============================================

class RabatEnvironment(Environment):
    """Environnement représentant la ville de Rabat"""
    
    def __init__(self, graph: Dict):
        super().__init__()
        self.graph = graph
        self.current_location = None
        
    def set_agent_location(self, agent: Agent, location: str):
        """Définir la localisation de l'agent"""
        self.current_location = location
        agent.current_location = location
    
    def get_percepts(self, agent: Agent):
        """Obtenir les perceptions de l'agent"""
        return {
            "location": agent.current_location,
            "neighbors": list(self.graph.get(agent.current_location, {}).keys())
        }
    
    def apply_action(self, agent: Agent, action: str):
        """Appliquer l'action"""
        if action and action in self.graph.get(agent.current_location, {}):
            cost = self.graph[agent.current_location][action]
            agent.current_location = action
            self.current_location = action
            agent.performance -= cost
            print(f"   🚗 Déplacement de {agent.history[-1][0]['location']} vers {action} (coût: {cost} minutes)")


# ============================================
# 5. Test des Algorithmes
# ============================================

def test_algorithm(algo_name: str, problem: NavigationProblem, 
                   search_func, heuristics=None, verbose=True):
    """
    Tester un algorithme de recherche
    """
    print(f"\n{'='*60}")
    print(f"🔍 Test de l'algorithme: {algo_name}")
    print(f"   De: {problem.initial_state} → Vers: {problem.goal_state}")
    print(f"{'='*60}")
    
    if heuristics:
        solution = search_func(problem, heuristics, verbose)
    else:
        solution = search_func(problem, verbose)
    
    if solution:
        print(f"\n✅ Solution trouvée!")
        print(f"   Chemin: {' → '.join(solution)}")
        
        # Calculer le coût total
        total_cost = 0
        for i in range(len(solution) - 1):
            cost = problem.graph[solution[i]][solution[i+1]]
            total_cost += cost
        print(f"   Coût total: {total_cost} minutes")
        print(f"   Nombre d'étapes: {len(solution) - 1}")
    else:
        print("\n❌ Aucune solution trouvée!")
    
    return solution


def compare_all_algorithms():
    """
    Comparer les quatre algorithmes
    """
    print("\n" + "="*60)
    print("🏙️  Projet TP: Agent de Navigation Intelligente - Ville de Rabat")
    print("="*60)
    
    # Créer le problème de navigation
    start = "Agdal"
    goal = "Ocean"
    problem = NavigationProblem(start, goal, RABAT_GRAPH)
    
    print(f"\n📍 Mission: Se déplacer de {start} vers {goal}")
    print(f"🗺️  Le graphe contient {len(RABAT_GRAPH)} quartiers")
    
    results = {}
    
    # 1. DFS
    print("\n" + "="*60)
    print("1️⃣  Algorithme DFS (Recherche en Profondeur)")
    print("="*60)
    solution_dfs = test_algorithm("DFS", problem, RabatSearchStrategy.dfs, verbose=False)
    results["DFS"] = solution_dfs
    
    # 2. BFS
    print("\n" + "="*60)
    print("2️⃣  Algorithme BFS (Recherche en Largeur)")
    print("="*60)
    solution_bfs = test_algorithm("BFS", problem, RabatSearchStrategy.bfs, verbose=False)
    results["BFS"] = solution_bfs
    
    # 3. UCS
    print("\n" + "="*60)
    print("3️⃣  Algorithme UCS (Recherche à Coût Uniforme)")
    print("="*60)
    solution_ucs = test_algorithm("UCS", problem, RabatSearchStrategy.ucs, verbose=False)
    results["UCS"] = solution_ucs
    
    # 4. A*
    print("\n" + "="*60)
    print("4️⃣  Algorithme A* (Recherche avec Heuristique)")
    print("="*60)
    solution_astar = test_algorithm("A*", problem, RabatSearchStrategy.a_star, 
                                    HEURISTICS_TO_OCEAN, verbose=False)
    results["A*"] = solution_astar
    
    # Tableau de comparaison
    print("\n" + "="*60)
    print("📊 Tableau de Comparaison des Algorithmes")
    print("="*60)
    print(f"{'Algorithme':<15} {'Chemin':<30} {'Coût':<10} {'Étapes':<10}")
    print("-"*60)
    
    for algo_name, solution in results.items():
        if solution:
            path_str = " → ".join(solution[:4]) + ("..." if len(solution) > 4 else "")
            total_cost = sum(problem.graph[solution[i]][solution[i+1]] 
                           for i in range(len(solution) - 1))
            steps = len(solution) - 1
            print(f"{algo_name:<15} {path_str:<30} {total_cost:<10} {steps:<10}")
        else:
            print(f"{algo_name:<15} {'Pas de solution':<30} {'-':<10} {'-':<10}")
    
    print("="*60)
    
    return results


# ============================================
# 6. Test du Problem Solving Agent
# ============================================

def test_problem_solving_agent():
    """
    Tester l'agent de résolution de problèmes
    """
    print("\n" + "="*60)
    print("🤖 Test du Problem Solving Agent")
    print("="*60)
    
    # Créer le problème et l'agent
    start = "Agdal"
    goal = "Kasbah"
    problem = NavigationProblem(start, goal, RABAT_GRAPH)
    
    # Créer l'agent avec la stratégie A*
    agent = ProblemSolvingAgent(
        name="RabatNavigator",
        search_strategy=lambda p: RabatSearchStrategy.a_star(p, HEURISTICS_TO_KASBAH, verbose=False),
        problem=problem
    )
    
    # Créer l'environnement
    env = RabatEnvironment(RABAT_GRAPH)
    env.set_agent_location(agent, start)
    
    print(f"\n🚗 Agent: {agent.name}")
    print(f"📍 Position actuelle: {start}")
    print(f"🎯 Objectif: {goal}")
    
    # Exécuter l'agent
    print(f"\n{'='*60}")
    print("▶️  Démarrage de la navigation...")
    print(f"{'='*60}")
    
    step = 1
    while not problem.goal_test(agent.current_location):
        print(f"\n🔄 Étape {step}:")
        print(f"   📍 Position: {agent.current_location}")
        
        # Obtenir les perceptions
        percept = env.get_percepts(agent)
        print(f"   👁️  Perceptions: {percept}")
        
        # L'agent décide
        action = agent.program(percept)
        
        if action:
            print(f"   🧠 Décision: Se déplacer vers {action}")
            env.apply_action(agent, action)
        else:
            print("   ❌ Aucune action disponible")
            break
        
        step += 1
        
        if step > 20:  # Protection contre les boucles infinies
            print("\n⚠️  Nombre maximum d'étapes dépassé!")
            break
    
    print(f"\n{'='*60}")
    print("✅ L'agent a atteint l'objectif!")
    print(f"{'='*60}")
    print(f"📊 Statistiques:")
    print(f"   Nombre d'étapes: {step}")
    print(f"   Performance finale: {agent.performance}")
    print(f"{'='*60}\n")


# ============================================
# 7. Programme Principal
# ============================================

if __name__ == "__main__":
    
    print("\n" + "🌟"*30)
    print("      🚗 TP: Agent de Navigation Intelligente - Rabat 🏙️")
    print("🌟"*30)
    
    # Partie 1: Comparaison des algorithmes
    print("\n📚 Partie 1: Comparaison des Algorithmes de Recherche")
    results = compare_all_algorithms()
    
    # Partie 2: Problem Solving Agent
    print("\n\n📚 Partie 2: Problem Solving Agent")
    test_problem_solving_agent()
    
    # Test détaillé d'un algorithme
    print("\n\n📚 Partie 3: Suivi Détaillé d'un Algorithme")
    problem_detailed = NavigationProblem("Agdal", "Medina", RABAT_GRAPH)
    print("\n🔍 Suivi détaillé de l'algorithme BFS:")
    test_algorithm("BFS (détaillé)", problem_detailed, RabatSearchStrategy.bfs, verbose=True)
    
    print("\n" + "🌟"*30)
    print("          ✅ TP terminé avec succès!")
    print("🌟"*30 + "\n")
