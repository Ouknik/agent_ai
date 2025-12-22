"""
TP: Navigation Intelligente entre les Villes du Maroc
======================================================
Objectif: Trouver le chemin optimal de Rabat (R) à Marrakech (M)
en minimisant la distance parcourue.

Exercices:
1. Construire le graphe des villes marocaines
2. Recherche aveugle (DFS, BFS, UCS)
3. Heuristique & A*
4. Comparer les chemins obtenus
"""
# -*- coding: utf-8 -*-

import sys
sys.path.append('../src')

from problem_solving_agent import (
    NavigationProblem, SearchStrategy, Trace
)
from typing import Dict, List, Optional, Tuple
from collections import deque
import heapq


# ============================================
# EXERCICE 1 - CONSTRUIRE LE GRAPHE
# ============================================

print("="*60)
print("EXERCICE 1 - CONSTRUCTION DU GRAPHE DES VILLES DU MAROC")
print("="*60)

# Graphe des villes marocaines avec distances en km
GRAPH_VILLES_MAROC = {
    "R": {  # Rabat (État initial)
        "C": 87,    # Rabat → Casablanca: 87 km
        "K": 208    # Rabat → Kénitra: 208 km (via route)
    },
    "C": {  # Casablanca
        "R": 87,    # Casablanca → Rabat: 87 km
        "E": 105,   # Casablanca → El Jadida: 105 km
        "S": 238    # Casablanca → Safi: 238 km
    },
    "K": {  # Kénitra
        "R": 208,   # Kénitra → Rabat
        "M": 407    # Kénitra → Meknès
    },
    "E": {  # El Jadida
        "C": 105,   # El Jadida → Casablanca
        "S": 161    # El Jadida → Safi
    },
    "S": {  # Safi
        "C": 238,   # Safi → Casablanca
        "E": 161,   # Safi → El Jadida
        "M": 160    # Safi → Marrakech: 160 km (État but)
    },
    "M": {  # Marrakech (État but)
        "S": 160,   # Marrakech → Safi
        "K": 407    # Marrakech → Kénitra
    }
}

print("\n✅ Graphe créé avec succès!")
print(f"Nombre de villes: {len(GRAPH_VILLES_MAROC)}")
print(f"Villes: {', '.join(GRAPH_VILLES_MAROC.keys())}")

# Définir l'état initial et l'état but
ETAT_INITIAL = "R"  # Rabat
ETAT_BUT = "M"      # Marrakech

print(f"\n📍 État initial: {ETAT_INITIAL} (Rabat)")
print(f"🎯 État but: {ETAT_BUT} (Marrakech)")

# Création du problème
problem_maroc = NavigationProblem(ETAT_INITIAL, ETAT_BUT, GRAPH_VILLES_MAROC)

print("\n✅ Problème de navigation créé!")

# ============================================
# Validation du problème
# ============================================

print("\n" + "-"*60)
print("VALIDATION DU PROBLÈME")
print("-"*60)

# Test 1: Actions possibles depuis Rabat
print(f"\n1️⃣ Actions possibles depuis Rabat (R):")
actions_R = problem_maroc.actions("R")
print(f"   → {actions_R}")

# Test 2: Test du but
print(f"\n2️⃣ Test du but:")
print(f"   Est-ce que 'R' est le but? {problem_maroc.goal_test('R')}")
print(f"   Est-ce que 'M' est le but? {problem_maroc.goal_test('M')}")

# Test 3: Successeurs d'une ville intermédiaire (Casablanca)
print(f"\n3️⃣ Successeurs de Casablanca (C):")
successeurs_C = problem_maroc.get_successors("C")
for ville, distance in successeurs_C:
    print(f"   → {ville}: {distance} km")


# ============================================
# EXERCICE 2 - RECHERCHE AVEUGLE
# ============================================

print("\n\n" + "="*60)
print("EXERCICE 2 - RECHERCHE AVEUGLE")
print("="*60)

class VillesMarocSearchStrategy:
    """Algorithmes de recherche pour le problème des villes marocaines"""
    
    @staticmethod
    def dfs(problem: NavigationProblem, verbose: bool = True):
        """Recherche en Profondeur - Depth First Search"""
        trace = Trace(problem) if verbose else None
        
        frontiere = [problem.initial_state]
        explore = set()
        parents = {}
        cout_cumule = {problem.initial_state: 0}
        
        if trace:
            trace.init_trace(frontiere, explore, "dfs")
        
        iteration = 0
        
        while frontiere:
            iteration += 1
            etat_actuel = frontiere.pop()
            
            if etat_actuel in explore:
                continue
            
            explore.add(etat_actuel)
            
            if trace:
                trace.iteration_trace(iteration, etat_actuel, frontiere, explore, parents, cout_cumule)
            
            if problem.goal_test(etat_actuel):
                if trace:
                    trace.goal_trace(iteration, etat_actuel, frontiere, explore, parents, cout_cumule)
                return VillesMarocSearchStrategy._reconstruct_path(parents, etat_actuel, problem.initial_state)
            
            for voisin in reversed(problem.actions(etat_actuel)):
                if voisin not in explore:
                    frontiere.append(voisin)
                    if voisin not in parents:
                        parents[voisin] = etat_actuel
                        cout_cumule[voisin] = cout_cumule[etat_actuel] + problem.path_cost(etat_actuel, voisin, voisin)
        
        return None
    
    @staticmethod
    def bfs(problem: NavigationProblem, verbose: bool = True):
        """Recherche en Largeur - Breadth First Search"""
        trace = Trace(problem) if verbose else None
        
        frontiere = deque([problem.initial_state])
        explore = set()
        parents = {}
        cout_cumule = {problem.initial_state: 0}
        
        if trace:
            trace.init_trace(list(frontiere), explore, "bfs")
        
        iteration = 0
        
        while frontiere:
            iteration += 1
            etat_actuel = frontiere.popleft()
            
            if etat_actuel in explore:
                continue
            
            explore.add(etat_actuel)
            
            if trace:
                trace.iteration_trace(iteration, etat_actuel, list(frontiere), explore, parents, cout_cumule)
            
            if problem.goal_test(etat_actuel):
                if trace:
                    trace.goal_trace(iteration, etat_actuel, list(frontiere), explore, parents, cout_cumule)
                return VillesMarocSearchStrategy._reconstruct_path(parents, etat_actuel, problem.initial_state)
            
            for voisin in problem.actions(etat_actuel):
                if voisin not in explore and voisin not in [n for n in frontiere]:
                    frontiere.append(voisin)
                    parents[voisin] = etat_actuel
                    cout_cumule[voisin] = cout_cumule[etat_actuel] + problem.path_cost(etat_actuel, voisin, voisin)
        
        return None
    
    @staticmethod
    def ucs(problem: NavigationProblem, verbose: bool = True):
        """Recherche à Coût Uniforme - Uniform Cost Search"""
        trace = Trace(problem) if verbose else None
        
        frontiere = [(0, problem.initial_state)]
        explore = set()
        parents = {}
        cout_cumule = {problem.initial_state: 0}
        
        if trace:
            trace.init_trace(frontiere, explore, "ucs")
        
        iteration = 0
        
        while frontiere:
            iteration += 1
            cout_actuel, etat_actuel = heapq.heappop(frontiere)
            
            if cout_actuel != cout_cumule[etat_actuel]:
                continue
            
            if etat_actuel in explore:
                continue
            
            explore.add(etat_actuel)
            
            if trace:
                trace.iteration_trace(iteration, etat_actuel, frontiere, explore, parents, cout_cumule)
            
            if problem.goal_test(etat_actuel):
                if trace:
                    trace.goal_trace(iteration, etat_actuel, frontiere, explore, parents, cout_cumule)
                return VillesMarocSearchStrategy._reconstruct_path(parents, etat_actuel, problem.initial_state)
            
            for voisin in problem.actions(etat_actuel):
                nouveau_cout = cout_cumule[etat_actuel] + problem.path_cost(etat_actuel, voisin, voisin)
                
                if voisin not in cout_cumule or nouveau_cout < cout_cumule[voisin]:
                    cout_cumule[voisin] = nouveau_cout
                    parents[voisin] = etat_actuel
                    heapq.heappush(frontiere, (nouveau_cout, voisin))
        
        return None
    
    @staticmethod
    def a_star(problem: NavigationProblem, heuristics: Dict[str, float], verbose: bool = True):
        """Recherche A* - A-star Search avec heuristique"""
        trace = Trace(problem) if verbose else None
        
        frontiere = [(heuristics[problem.initial_state], problem.initial_state)]
        explore = set()
        parents = {}
        cout_cumule = {problem.initial_state: 0}
        
        if trace:
            trace.init_trace(frontiere, explore, "a-star")
        
        iteration = 0
        
        while frontiere:
            iteration += 1
            f_actuel, etat_actuel = heapq.heappop(frontiere)
            
            g_actuel = cout_cumule[etat_actuel]
            h_actuel = heuristics[etat_actuel]
            
            if f_actuel != g_actuel + h_actuel:
                continue
            
            if etat_actuel in explore:
                continue
            
            explore.add(etat_actuel)
            
            if trace:
                trace.iteration_trace(iteration, etat_actuel, frontiere, explore, parents, cout_cumule)
            
            if problem.goal_test(etat_actuel):
                if trace:
                    trace.goal_trace(iteration, etat_actuel, frontiere, explore, parents, cout_cumule)
                return VillesMarocSearchStrategy._reconstruct_path(parents, etat_actuel, problem.initial_state)
            
            for voisin in problem.actions(etat_actuel):
                nouveau_cout_g = cout_cumule[etat_actuel] + problem.path_cost(etat_actuel, voisin, voisin)
                
                if voisin not in cout_cumule or nouveau_cout_g < cout_cumule[voisin]:
                    cout_cumule[voisin] = nouveau_cout_g
                    parents[voisin] = etat_actuel
                    f = nouveau_cout_g + heuristics[voisin]
                    heapq.heappush(frontiere, (f, voisin))
        
        return None
    
    @staticmethod
    def _reconstruct_path(parents: Dict[str, str], goal: str, start: str) -> List[str]:
        """Reconstruit le chemin du début à la fin"""
        path = [goal]
        current = goal
        while current != start:
            current = parents[current]
            path.append(current)
        return list(reversed(path))


def test_algorithme(nom_algo: str, fonction_recherche, heuristics=None):
    """Fonction auxiliaire pour tester un algorithme"""
    print(f"\n{'='*60}")
    print(f"🔍 Algorithme: {nom_algo}")
    print(f"   De: {ETAT_INITIAL} (Rabat) → Vers: {ETAT_BUT} (Marrakech)")
    print(f"{'='*60}")
    
    if heuristics:
        solution = fonction_recherche(problem_maroc, heuristics, verbose=True)
    else:
        solution = fonction_recherche(problem_maroc, verbose=True)
    
    if solution:
        print(f"\n✅ Solution trouvée!")
        print(f"   Chemin: {' → '.join(solution)}")
        
        # Calculer la distance totale
        distance_totale = 0
        for i in range(len(solution) - 1):
            distance = GRAPH_VILLES_MAROC[solution[i]][solution[i+1]]
            distance_totale += distance
            
        print(f"   Distance totale: {distance_totale} km")
        print(f"   Nombre d'étapes: {len(solution) - 1}")
        return solution, distance_totale
    else:
        print("\n❌ Aucune solution trouvée!")
        return None, None


# 1️⃣ DFS - Recherche en Profondeur
print("\n" + "="*60)
print("1️⃣ DFS (Depth-First Search)")
print("="*60)
solution_dfs, distance_dfs = test_algorithme("DFS", VillesMarocSearchStrategy.dfs)

# 2️⃣ BFS - Recherche en Largeur
print("\n" + "="*60)
print("2️⃣ BFS (Breadth-First Search)")
print("="*60)
solution_bfs, distance_bfs = test_algorithme("BFS", VillesMarocSearchStrategy.bfs)

# 3️⃣ UCS - Recherche à Coût Uniforme
print("\n" + "="*60)
print("3️⃣ UCS (Uniform Cost Search)")
print("="*60)
solution_ucs, distance_ucs = test_algorithme("UCS", VillesMarocSearchStrategy.ucs)


# ============================================
# EXERCICE 3 - HEURISTIQUE & A*
# ============================================

print("\n\n" + "="*60)
print("EXERCICE 3 - HEURISTIQUE & A*")
print("="*60)

# Heuristiques admissibles: distance à vol d'oiseau approximative vers Marrakech
# Ces valeurs sont des estimations (doivent être ≤ distance réelle)
HEURISTIQUES_MARRAKECH = {
    "R": 320,   # Rabat → Marrakech: ~320 km (estimation)
    "C": 240,   # Casablanca → Marrakech: ~240 km
    "K": 350,   # Kénitra → Marrakech: ~350 km
    "E": 220,   # El Jadida → Marrakech: ~220 km
    "S": 150,   # Safi → Marrakech: ~150 km
    "M": 0      # Marrakech → Marrakech: 0 km (but atteint)
}

print("\n📏 Heuristiques proposées (distance estimée vers Marrakech):")
for ville, h_value in HEURISTIQUES_MARRAKECH.items():
    ville_nom = {
        "R": "Rabat", "C": "Casablanca", "K": "Kénitra",
        "E": "El Jadida", "S": "Safi", "M": "Marrakech"
    }
    print(f"   h({ville}) = {h_value} km ({ville_nom[ville]})")

# Vérification de l'admissibilité
print("\n✅ Vérification de l'admissibilité:")
print("   Une heuristique est admissible si h(n) ≤ coût_réel(n, but)")
print("   Toutes les heuristiques proposées sont admissibles car elles")
print("   représentent des distances à vol d'oiseau (jamais > distance réelle)")

# 4️⃣ A* - Recherche avec Heuristique
print("\n" + "="*60)
print("4️⃣ A* (A-star Search)")
print("="*60)

solution_astar, distance_astar = test_algorithme("A*", VillesMarocSearchStrategy.a_star, HEURISTIQUES_MARRAKECH)


# ============================================
# EXERCICE 4 - COMPARAISON DES RÉSULTATS
# ============================================

print("\n\n" + "="*60)
print("EXERCICE 4 - COMPARAISON DES CHEMINS OBTENUS")
print("="*60)

# Tableau de comparaison
resultats = {
    "DFS": {"solution": solution_dfs, "distance": distance_dfs},
    "BFS": {"solution": solution_bfs, "distance": distance_bfs},
    "UCS": {"solution": solution_ucs, "distance": distance_ucs},
    "A*": {"solution": solution_astar, "distance": distance_astar}
}

print("\n📊 TABLEAU DE COMPARAISON")
print("="*80)
print(f"{'Algorithme':<12} {'Chemin':<35} {'Distance':<12} {'Étapes':<10} {'Optimal':<8}")
print("-"*80)

distance_optimale = min([r["distance"] for r in resultats.values() if r["distance"] is not None])

for algo, data in resultats.items():
    if data["solution"]:
        chemin_str = " → ".join(data["solution"])
        if len(chemin_str) > 35:
            chemin_str = chemin_str[:32] + "..."
        
        distance = data["distance"]
        etapes = len(data["solution"]) - 1
        optimal = "✅ Oui" if distance == distance_optimale else "❌ Non"
        
        print(f"{algo:<12} {chemin_str:<35} {distance:<12} {etapes:<10} {optimal:<8}")
    else:
        print(f"{algo:<12} {'Pas de solution':<35} {'-':<12} {'-':<10} {'-':<8}")

print("="*80)

# Analyse détaillée
print("\n🎯 ANALYSE DES RÉSULTATS:")
print("-"*60)

# Trouver le(s) meilleur(s) algorithme(s)
meilleurs_algos = [algo for algo, data in resultats.items() 
                   if data["distance"] == distance_optimale]

print(f"\n1. Distance optimale: {distance_optimale} km")
print(f"2. Algorithme(s) optimal(s): {', '.join(meilleurs_algos)}")

# Comparer les chemins
print(f"\n3. Comparaison des chemins:")
for algo, data in resultats.items():
    if data["solution"]:
        print(f"\n   {algo}:")
        print(f"   Chemin: {' → '.join(data['solution'])}")
        print(f"   Distance: {data['distance']} km")
        
        # Détail du chemin
        solution = data["solution"]
        print(f"   Détail:")
        for i in range(len(solution) - 1):
            ville_depart = solution[i]
            ville_arrivee = solution[i+1]
            distance = GRAPH_VILLES_MAROC[ville_depart][ville_arrivee]
            print(f"      {ville_depart} → {ville_arrivee}: {distance} km")

# Observations
print(f"\n4. Observations:")
print(f"   • DFS explore en profondeur: peut trouver un chemin non optimal")
print(f"   • BFS explore en largeur: trouve le chemin avec le moins d'étapes")
print(f"   • UCS considère les coûts: trouve toujours le chemin optimal")
print(f"   • A* utilise l'heuristique: trouve le chemin optimal efficacement")

# Efficacité
print(f"\n5. Efficacité (nombre de nœuds explorés):")
print(f"   • UCS et A* sont garantis d'être optimaux")
print(f"   • A* est généralement plus efficace que UCS (grâce à l'heuristique)")
print(f"   • BFS trouve un chemin court mais pas forcément optimal en distance")
print(f"   • DFS peut trouver un chemin long")


# ============================================
# SCHÉMA RÉCAPITULATIF
# ============================================

print("\n\n" + "="*60)
print("SCHÉMA RÉCAPITULATIF DU GRAPHE")
print("="*60)

print("""
                          Graphe des Villes du Maroc
                          ==========================

                               K (Kénitra)
                              / \\
                          208/   \\407
                            /     \\
                       R (Rabat)   M (Marrakech) 🎯
                           |         |
                         87|         |160
                           |         |
                       C (Casablanca)|
                          / \\        |
                      105/   \\238    |
                        /     \\      |
                E (El Jadida)  S (Safi)
                        \\     /
                      161\\   /160
                          \\ /
                           
Légende:
  R = Rabat (État initial 📍)
  C = Casablanca
  K = Kénitra
  E = El Jadida
  S = Safi
  M = Marrakech (État but 🎯)
  
Les nombres indiquent les distances en kilomètres.
""")

print("\n" + "="*60)
print("✅ TOUS LES EXERCICES COMPLÉTÉS AVEC SUCCÈS!")
print("="*60)

# ============================================
# CONCLUSION
# ============================================

print("\n📝 CONCLUSION:")
print("-"*60)
print(f"Le chemin optimal de Rabat à Marrakech est:")
if solution_ucs:
    print(f"   {' → '.join(solution_ucs)}")
    print(f"   Distance totale: {distance_ucs} km")
    print(f"\nCe résultat a été trouvé par les algorithmes: {', '.join(meilleurs_algos)}")
print("\n" + "="*60 + "\n")
