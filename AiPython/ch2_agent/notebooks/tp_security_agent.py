"""
TP: Agent de Sécurité Intelligent
==================================
Module: Intelligence Artificielle
Objectif: Trouver le chemin optimal pour atteindre les zones à surveiller

Description:
- L'environnement est modélisé sous forme de graphe orienté et pondéré
- 12 nœuds (zones) et 15 arêtes (passages)
- Les coûts représentent le temps de déplacement en minutes

⚠️ Ce projet est strictement académique et pédagogique.
"""
# -*- coding: utf-8 -*-

import sys
sys.path.append('../src')

# Importation des fonctions depuis src/problem_solving_agent.py
from problem_solving_agent import bfs, dfs, ucs, astar

# ============================================
# EXERCICE 1 - CONSTRUCTION DU GRAPHE
# ============================================
print("="*70)
print("EXERCICE 1 - CONSTRUCTION DU GRAPHE DU BÂTIMENT")
print("="*70)

# Graphe représentant le bâtiment avec 12 zones
# Format: {"zone": {"voisin": coût}} - coût = temps en minutes
graphe = {
    "Poste_Securite": {"Entree": 2, "Hall": 3},
    "Entree": {"Poste_Securite": 2, "Hall": 1},
    "Hall": {"Poste_Securite": 3, "Entree": 1, "Couloir_B": 2, "Couloir_A": 2, "Cafeteria": 4},
    "Couloir_B": {"Hall": 2, "Bureau_2": 3, "Parking": 4},
    "Couloir_A": {"Hall": 2, "Bureau_1": 3, "Salle_Serveurs": 5},
    "Bureau_2": {"Couloir_B": 3, "Cafeteria": 6},
    "Bureau_1": {"Couloir_A": 3, "Salle_Serveurs": 5},
    "Parking": {"Couloir_B": 4, "Sortie_Urgence": 7},
    "Cafeteria": {"Hall": 4, "Bureau_2": 6, "Sortie_Urgence": 5, "Toit": 5},
    "Sortie_Urgence": {"Parking": 7, "Cafeteria": 5},
    "Toit": {"Cafeteria": 5, "Salle_Serveurs": 4},
    "Salle_Serveurs": {"Couloir_A": 5, "Bureau_1": 5, "Toit": 4}
}

# Définition de l'état initial et l'état but
etat_initial = "Poste_Securite"
etat_but = "Salle_Serveurs"

print(f"\n📍 Point de départ (vert): {etat_initial}")
print(f"🎯 Zone critique (rouge): {etat_but}")
print(f"📊 Nombre de zones: {len(graphe)}")
print(f"\n🔗 Structure du graphe:")
print("-"*50)
for zone, voisins in graphe.items():
    print(f"   {zone}: {voisins}")

# ============================================
# EXERCICE 2 - VALIDATION DU PROBLÈME
# ============================================
print("\n\n" + "="*70)
print("EXERCICE 2 - VALIDATION DU PROBLÈME")
print("="*70)

print(f"\n🚨 ALERTE: Mouvement suspect détecté dans la Salle des Serveurs!")
print(f"📍 Position de l'agent: {etat_initial}")
print(f"🎯 Objectif: Atteindre {etat_but}")

print(f"\n✅ Voisins de {etat_initial}: {list(graphe[etat_initial].keys())}")
print(f"✅ Voisins de {etat_but}: {list(graphe[etat_but].keys())}")

# ============================================
# EXERCICE 3 - RECHERCHE AVEUGLE
# ============================================
print("\n\n" + "="*70)
print("EXERCICE 3 - RECHERCHE AVEUGLE (BFS, DFS, UCS)")
print("="*70)

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
# EXERCICE 4 - HEURISTIQUE ET A*
# ============================================
print("\n\n" + "="*70)
print("EXERCICE 4 - A* AVEC HEURISTIQUE ADMISSIBLE")
print("="*70)

# Heuristique admissible: estimation du temps minimal vers Salle_Serveurs
# Une heuristique est admissible si elle ne surestime jamais le coût réel
heuristique = {
    "Poste_Securite": 7,    # Estimation: loin de la cible
    "Entree": 8,            # Doit passer par Hall
    "Hall": 5,              # Accès direct via Couloir_A
    "Couloir_B": 10,        # Chemin plus long
    "Couloir_A": 4,         # Proche de Salle_Serveurs
    "Bureau_2": 11,         # Très éloigné
    "Bureau_1": 4,          # Adjacent à Salle_Serveurs
    "Parking": 12,          # Le plus éloigné
    "Cafeteria": 8,         # Via Toit possible
    "Sortie_Urgence": 13,   # Très éloigné
    "Toit": 4,              # Adjacent à Salle_Serveurs
    "Salle_Serveurs": 0     # But atteint
}

print("\n📊 Heuristique admissible définie (temps estimé en minutes):")
print("-"*50)
for zone, h in heuristique.items():
    status = "🎯 BUT" if h == 0 else ""
    print(f"   h({zone}) = {h} {status}")

print("\n" + "-"*60)
print("🔍 A* Search (Recherche A*)")
print("-"*60)
chemin_astar = astar(graphe, etat_initial, etat_but, heuristique)

# ============================================
# EXERCICE 5 - COMPARAISON DES RÉSULTATS
# ============================================
print("\n\n" + "="*70)
print("EXERCICE 5 - COMPARAISON DES ALGORITHMES")
print("="*70)

def calculer_cout(chemin, graphe):
    """Calcule le coût total d'un chemin (temps en minutes)"""
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
print(f"\n{'Algorithme':<12} | {'Chemin':<50} | {'Coût (min)':<10}")
print("-"*80)

for algo, chemin in resultats.items():
    if chemin:
        chemin_str = " → ".join(chemin)
        cout = calculer_cout(chemin, graphe)
        print(f"{algo:<12} | {chemin_str:<50} | {cout:<10}")
    else:
        print(f"{algo:<12} | {'Aucun chemin trouvé':<50} | {'-':<10}")

# ============================================
# EXERCICE 6 - SIMULATION DE L'AGENT
# ============================================
print("\n\n" + "="*70)
print("EXERCICE 6 - SIMULATION DE LA MISSION")
print("="*70)

# Utiliser le meilleur chemin (A* ou UCS)
meilleur_chemin = chemin_astar if chemin_astar else chemin_ucs
meilleur_cout = calculer_cout(meilleur_chemin, graphe)

print(f"\n🤖 AGENT DE SÉCURITÉ - MISSION DE SURVEILLANCE")
print("-"*50)
print(f"📍 Position initiale: {etat_initial}")
print(f"🎯 Objectif: {etat_but}")
print(f"⚙️  Algorithme utilisé: A*")
print(f"\n📋 SÉQUENCE DE DÉPLACEMENT:")
print("-"*50)

if meilleur_chemin:
    for i, zone in enumerate(meilleur_chemin):
        if i == 0:
            print(f"  Étape {i+1}: 🟢 Départ de {zone}")
        elif i == len(meilleur_chemin) - 1:
            print(f"  Étape {i+1}: 🔴 Arrivée à {zone} - ALERTE TRAITÉE ✓")
        else:
            print(f"  Étape {i+1}: 🔵 Transit par {zone}")
    
    print(f"\n✅ Mission accomplie en {meilleur_cout} minutes")

# ============================================
# CONCLUSION
# ============================================
print("\n\n" + "="*70)
print("CONCLUSION - ANALYSE DES PERFORMANCES")
print("="*70)

print("""
📊 COMPARAISON DES ALGORITHMES:
─────────────────────────────────
• BFS: Trouve le chemin avec le moins d'étapes (pas forcément optimal en coût)
• DFS: Rapide mais ne garantit pas l'optimalité
• UCS: Garantit le chemin de coût minimal
• A*:  Optimal + efficace grâce à l'heuristique

🏆 ALGORITHME RECOMMANDÉ: A*
─────────────────────────────────
✓ Trouve le chemin optimal (même résultat que UCS)
✓ Explore moins de nœuds grâce à l'heuristique
✓ Idéal pour les situations d'urgence (efficacité maximale)
✓ Adapté à notre problème de surveillance
""")

print("="*70)
print("✅ TP TERMINÉ AVEC SUCCÈS!")
print("="*70)
