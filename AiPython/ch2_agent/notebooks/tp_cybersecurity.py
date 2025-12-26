"""
TP: Agent Intelligent pour l'Analyse de Scénarios d'Attaque
============================================================
Module: Intelligence Artificielle
Objectif: Trouver le chemin optimal de External à RootAccess

Description:
- L'environnement est modélisé sous forme de graphe orienté et pondéré
- Chaque nœud représente un état du système
- Chaque arête représente une action possible
- Chaque poids représente le coût (temps, risque ou difficulté)

⚠️ Ce projet est strictement académique et pédagogique.
"""
# -*- coding: utf-8 -*-

import sys
sys.path.append('../src')

from problem_solving_agent import bfs, dfs, ucs, astar

# ============================================
# EXERCICE 1 - CONSTRUCTION DU GRAPHE
# ============================================
print("="*60)
print("EXERCICE 1 - CONSTRUCTION DU GRAPHE D'ATTAQUE")
print("="*60)

# Graphe orienté et pondéré représentant les scénarios d'attaque
# Chaque nœud = état du système
# Chaque arête = action possible avec son coût
graphe = {
    "External": {"Scan": 1},
    "Scan": {"Bruteforce": 4, "WebExploit": 2},
    "Bruteforce": {"UserAccess": 3},
    "WebExploit": {"UserAccess": 2},
    "UserAccess": {"PrivilegeEsc": 3, "Pivot": 2},
    "PrivilegeEsc": {"AdminAccess": 2},
    "AdminAccess": {"RootAccess": 1},
    "Pivot": {"DBServer": 3},
    "DBServer": {"RootAccess": 2},
    "RootAccess": {}
}

# Définition de l'état initial et l'état but
etat_initial = "External"
etat_but = "RootAccess"

print(f"\n📍 État initial: {etat_initial}")
print(f"🎯 État but: {etat_but}")
print(f"📊 Nombre de nœuds: {len(graphe)}")
print(f"🔗 Nœuds: {', '.join(graphe.keys())}")

# ============================================
# EXERCICE 2 - RECHERCHE AVEUGLE
# ============================================
print("\n\n" + "="*60)
print("EXERCICE 2 - RECHERCHE AVEUGLE (BFS, DFS, UCS)")
print("="*60)

# --- BFS ---
print("\n" + "-"*60)
print("🔍 BFS - Breadth First Search (Recherche en Largeur)")
print("-"*60)
chemin_bfs = bfs(graphe, etat_initial, etat_but)

# --- DFS ---
print("\n" + "-"*60)
print("🔍 DFS - Depth First Search (Recherche en Profondeur)")
print("-"*60)
chemin_dfs = dfs(graphe, etat_initial, etat_but)

# --- UCS ---
print("\n" + "-"*60)
print("🔍 UCS - Uniform Cost Search (Recherche à Coût Uniforme)")
print("-"*60)
chemin_ucs = ucs(graphe, etat_initial, etat_but)

# ============================================
# EXERCICE 3 - HEURISTIQUE ET A*
# ============================================
print("\n\n" + "="*60)
print("EXERCICE 3 - A* AVEC HEURISTIQUE ADMISSIBLE")
print("="*60)

# Heuristique admissible: estimation de la distance vers RootAccess
# Une heuristique est admissible si elle ne surestime jamais le coût réel
heuristique = {
    "External": 6,      # Loin du but
    "Scan": 5,          
    "Bruteforce": 4,    
    "WebExploit": 4,    
    "UserAccess": 3,    
    "PrivilegeEsc": 2,  
    "AdminAccess": 1,   
    "Pivot": 3,         
    "DBServer": 2,      
    "RootAccess": 0     # But atteint
}

print("\n📊 Heuristique admissible définie:")
print("-"*40)
for etat, h in heuristique.items():
    print(f"   h({etat}) = {h}")

print("\n" + "-"*60)
print("🔍 A* Search (Recherche A*)")
print("-"*60)
chemin_astar = astar(graphe, etat_initial, etat_but, heuristique)

# ============================================
# EXERCICE 4 - COMPARAISON DES RÉSULTATS
# ============================================
print("\n\n" + "="*60)
print("EXERCICE 4 - COMPARAISON DES ALGORITHMES")
print("="*60)

def calculer_cout(chemin, graphe):
    """Calcule le coût total d'un chemin"""
    if not chemin:
        return float('inf')
    cout = 0
    for i in range(len(chemin) - 1):
        cout += graphe[chemin[i]][chemin[i+1]]
    return cout

# Stocker les résultats
resultats = {
    "BFS": chemin_bfs,
    "DFS": chemin_dfs,
    "UCS": chemin_ucs,
    "A*": chemin_astar
}

# Affichage comparatif
print(f"\n{'Algorithme':<12} | {'Chemin':<55} | {'Coût':<6} | {'Nœuds':<6}")
print("-"*90)

for algo, chemin in resultats.items():
    if chemin:
        chemin_str = " → ".join(chemin)
        cout = calculer_cout(chemin, graphe)
        nb_noeuds = len(chemin)
        print(f"{algo:<12} | {chemin_str:<55} | {cout:<6} | {nb_noeuds:<6}")
    else:
        print(f"{algo:<12} | {'Aucun chemin trouvé':<55} | {'-':<6} | {'-':<6}")

# ============================================
# CONCLUSION
# ============================================
print("\n\n" + "="*60)
print("CONCLUSION")
print("="*60)

print("""
📌 Analyse des résultats:

1. BFS (Breadth First Search):
   - Explore niveau par niveau
   - Garantit le chemin le plus court en nombre d'étapes
   - Ne considère pas les coûts des arêtes

2. DFS (Depth First Search):
   - Explore en profondeur d'abord
   - Peut trouver une solution rapidement
   - Ne garantit pas le chemin optimal

3. UCS (Uniform Cost Search):
   - Explore par coût croissant
   - Garantit le chemin optimal en termes de coût
   - Plus efficace que BFS pour les graphes pondérés

4. A* (A-Star):
   - Utilise une heuristique pour guider la recherche
   - Combine le coût réel et l'estimation vers le but
   - Optimal si l'heuristique est admissible
   - Généralement plus efficace que UCS
""")

print("✅ TP Terminé avec succès!")
