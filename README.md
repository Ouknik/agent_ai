<div align="center">

# 🚗 Agent de Navigation Intelligente au Maroc

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Completed-success.svg)]()

**Un projet d'intelligence artificielle implémentant des algorithmes de recherche pour la navigation autonome**

🏙️ **Rabat** (Quartiers) • 🗺️ **Maroc** (Villes) • 🤖 **Problem Solving Agent**

[Installation](#-installation) • [Utilisation](#-utilisation) • [Documentation](#-documentation) • [Résultats](#-résultats)

</div>

---

## 📑 Table des Matières

- [À propos](#-à-propos)
- [Fonctionnalités](#-fonctionnalités)
- [Installation](#-installation)
- [Utilisation](#-utilisation)
- [Architecture](#-architecture)
- [Résultats](#-résultats)
- [Structure du Projet](#-structure-du-projet)
- [Exemples](#-exemples)
- [Documentation](#-documentation)
- [Contribution](#-contribution)
- [Licence](#-licence)

---

## 🎯 À propos

Ce projet implémente des **agents intelligents de navigation** capables de se déplacer automatiquement en utilisant des algorithmes de recherche classiques de l'intelligence artificielle.

### Deux Applications Pratiques

1. **🏙️ Navigation Rabat** (`rabat_navigation_tp.py`)
   - Navigation entre les **quartiers de Rabat**
   - Graphe de **8 quartiers** (Agdal, Hassan, Medina, Ocean, etc.)
   - Distances en **minutes**

2. **🗺️ Navigation Maroc** (`tp_villes_maroc.py`)
   - Navigation entre les **villes marocaines**
   - Graphe de **6 villes** (Rabat, Casablanca, Marrakech, etc.)
   - Distances en **kilomètres** 

### Objectifs pédagogiques
- Comprendre l'**architecture AIMA** (Artificial Intelligence: A Modern Approach)
- Maîtriser la **formulation de problèmes** en IA
- Implémenter et comparer des **algorithmes de recherche**
- Développer un **Problem Solving Agent** complet
- Appliquer les concepts sur des **cas réels** (Rabat et Maroc)

### Contexte
Les problèmes sont modélisés par des **graphes pondérés** où:
- Les **nœuds** représentent des lieux (quartiers ou villes)
- Les **arêtes** représentent les routes/chemins
- Les **poids** représentent les distances (minutes ou kilomètres)

---

## ✨ Fonctionnalités

### 🔍 Algorithmes de Recherche Implémentés

| Algorithme | Type | Optimalité | Complexité |
|-----------|------|-----------|------------|
| **DFS** | Non-informé | ❌ Non | O(b^m) |
| **BFS** | Non-informé | ✅ Oui (si coût uniforme) | O(b^d) |
| **UCS** | Non-informé | ✅ Oui | O(b^(C*/ε)) |
| **A*** | Informé | ✅ Oui (heuristique admissible) | O(b^d) |
s Disponibles

#### 🏙️ Graphe de Rabat (8 quartiers)
```
    Agdal ──10── Hassan ──8── Medina ──5── Kasbah
      │            │           │
      8           20          12
      │            │           │
   Aviation ──15── Ocean ──18── Souissi
      │                         │
      8                        10
      └────── Hay_Riad ────────┘
               (15)
```

#### 🗺️ Graphe du Maroc (6 villes)
```
                    K (Kénitra)
                   / \
               208/   \407
                 /     \
            R (Rabat)   M (Marrakech)
                |         |
              87|         |160
                |         |
            C (Casablanca)|
               / \        |
           105/   \238    |
             /     \      |
       E (El Jadida)  S (Safi)
             \     /
           161\   /160
               \ /iad ────────┘
               (15)
```

### 🤖 Problem Solving Agent

Agent intelligent suivant le cycle:
```
Percevoir → Formuler Objectif → Formuler Problème → Rechercher → Exécuter
```

---

## 🚀 Installation

### Prérequis
- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)

### Étapes d'installation

1. **Cloner le dépôt**
```bash
git clone https://github.com/votre-username/agent_ai.git
cd agent_ai
```
#### 🏙️ Navigation Rabat
```bash
cd AiPython/ch2_agent/notebooks
python rabat_navigation_tp.py
```

**Le programme exécute automatiquement trois parties:**

1. **Partie 1**: Comparaison des 4 algorithmes (Agdal → Ocean)
2. **Partie 2**: Test du Problem Solving Agent (Agdal → Kasbah)
3. **Partie 3**: Suivi détaillé de BFS (Agdal → Medina)

#### 🗺️ Navigation Maroc
```bash
cd AiPython/ch2_agent/notebooks
python tp_villes_maroc.py
```

**Le programme exécute les 4 exercices:**

1. **Exercice 1**: Construction du graphe (Rabat → Marrakech)
2. **Exercice 2**: Recherche aveugle (DFS, BFS, UCS)
3. **Exercice 3**: Heuristiques & A*
4. **Exercice 4**: Comparaison des chemins

### Personnalisation

#### Pour Rabat (`rabat_navigation_tp.py`):
```python
# Changer le point de départ et d'arrivée
start = "Souissi"
goal = "Kasbah"

# Utiliser une heuristique différente
solution = RabatSearchStrategy.a_star(problem, HEURISTICS_TO_KASBAH)
```

#### Pour le Maroc (`tp_villes_maroc.py`):
```python
# Modifier l'état initial et but
ETAT_INITIAL = "C"  # Casablanca
ETAT_BUT = "K"      # Kénitra

# Tester un seul algorithme
solution = VillesMarocSearchStrategy.ucs(problem_maroc, verbose=True
```

### Options d'Exécution

Le programme exécute automatiquement trois parties:

1. **Partie 1**: Comparaison des 4 algorithmes (Agdal → Ocean)
2. **Partie 2**: Test du Problem Solving Agent (Agdal → Kasbah)
3. **Partie 3**: Suivi détaillé de BFS (Agdal → Medina)

### Personnalisation

Modifiez les paramètres dans `rabat_navigation_tp.py`:

```python
# Changer le point de départ et d'arrivée
start = "Souissi"
goal = "Kasbah"

# Utiliser une heuristique différente
solution = RabatSearchStrategy.a_star(problem, HEURISTICS_TO_KASBAH)
```
🏙️ Résultats - Navigation Rabat (Agdal → Ocean)

| Algorithme | Chemin | Coût (min) | Étapes | Optimal |
|-----------|--------|------------|---------|---------|
| **DFS** | Agdal → Hassan → Ocean | 30 | 2 | ❌ |
| **BFS** | Agdal → Hassan → Ocean | 30 | 2 | ❌ |
| **UCS** | Agdal → Aviation → Ocean | **23** | 2 | ✅ |
| **A*** | Agdal → Aviation → Ocean | **23** | 2 | ✅ |

### 🗺️ Résultats - Navigation Maroc (Rabat → Marrakech)

| Algorithme | Chemin | Coût (km) | Étapes | Optimal |
|-----------|--------|-----------|---------|---------|
| **DFS** | R → C → S → M | **485** | 3 | ✅ |
| **BFS** | R → K → M | 615 | 2 | ❌ |
| **UCS** | R → C → S → M | **485** | 3 | ✅ |
| **A*** | R → C → S → M | **485** | 3 | ✅ |

### 🎯 Analyse Comparative

#### Navigation Rabat:
- ✅ **UCS** et **A*** trouvent le chemin optimal (23 min)
- ⚠️ **DFS** et **BFS** trouvent une solution sous-optimale (30 min)
- 🚀 **A*** utilise l'heuristique pour optimiser la recherche

#### Navigation Maroc:
- ✅ **DFS**, **UCS** et **A*** trouvent le chemin optimal (485 km)
- ⚠️ **BFS** trouve le chemin avec moins d'étapes mais distance plus longue (615 km)
- 📍 Le chemin optimal: **R → C → S → M** (3 étapes, 485 km)
- 🔍 **BFS** privilégie le nombre d'étapes, pas la distance optimal
       │                   ┌──────────┐
       │                   │ Problem  │
       │                   └──────────┘
       │                         │
┌─────────────┐           ┌──────────────────┐
│Environment  │           │ NavigationProblem│
│  (Abstract) │           └──────────────────┘
└─────────────┘                   │
       ▲                    ┌──────────────┐
       │                    │SearchStrategy│
┌──────────────┐            └──────────────┘
│RabatEnviron- │
│    ment      │
└──────────────┘
```
├── requirements.txt                   # Dépendances Python
│
└── AiPython/
    └── ch2_agent/
        ├── src/
        │   ├── __init__.py
        │   ├── agent.py               # Classes de base (Agent, Environment)
        │   └── problem_solving_agent.py  # Problem, SearchStrategy, Trace
        │
        └── notebooks/
            ├── rabat_navigation_tp.py     # 🏙️ Navigation Rabat (Quartiers)
            ├── tp_villes_maroc.py         # 🗺️ Navigation Maroc (Villes)
            └── README_TP.md               # Documentation détaillée
```

### Relations entre les Fichiers

```Navigation Rabat (Recherche Simple)

```python
from problem_solving_agent import NavigationProblem
from rabat_navigation_tp import RabatSearchStrategy, RABAT_GRAPH

# Créer un problème
problem = NavigationProblem("Agdal", "Ocean", RABAT_GRAPH)

# Utiliser BFS
solution = RabatSearchStrategy.bfs(problem, verbose=False)
print(f"Chemin trouvé: {' → '.join(solution)}")
# Output: Agdal → Hassan → Ocean
```

### Exemple 2: Navigation Maroc (Recherche avec Heuristique)

```python
from problem_solving_agent import NavigationProblem
from tp_villes_maroc import VillesMarocSearchStrategy, GRAPH_VILLES_MAROC, HEURISTIQUES_MARRAKECH

# Créer le problème
problem = NavigationProblem("R", "M", GRAPH_VILLES_MAROC)

# Utiliser A* avec heuristique
solution = VillesMarocSearchStrategy.a_star(problem, HEURISTIQUES_MARRAKECH, verbose=False)
print(f"Chemin optimal: {' → '.join(solution)}")
# Output: R → C → S → M (485 km)
```

### Exemple 3: Comparaison d'Algorithmes

```python
# Pour Rabat
results_rabat = compare_all_algorithms()

# Afficher les résultats
for algo, path in results_rabat.items():
    print(f"{algo}: {' → '.join(path)}")
```

### Exemple 4re du Projet

```
agentAi/
│
├── README.md                          # Ce fichier
├── LICENSE                            # Licence MIT
│
└── AiPython/
    └── ch2_agent/
        ├── src/
        │   ├── __init__.py
        │   ├── agent.py               # Classes de base (Agent, Environment)
        │   └── problem_solving_agent.py  # Problem, SearchStrategy, Trace
        │
        └── notebooks/
            ├── rabat_navigation_tp.py # 🌟 Programme principal
            └── README_TP.md           # Documentation détaillée
```

---

## 🔬 Exemples

### Exemple 1: Recherche Simple

```python
from problem_solving_agent import NavigationProblem
from rabat_navigation_tp import RabatSearchStrategy, RABAT_GRAPH

# Créer un problème
problem = NavigationProblem("Agdal", "Ocean", RABAT_GRAPH)
#### Classes de Recherche - Rabat

```python
# RabatSearchStrategy
RabatSearchStrategy.dfs(problem, verbose=True)
RabatSearchStrategy.bfs(problem, verbose=True)
RabatSearchStrategy.ucs(problem, verbose=True)
RabatSearchStrategy.a_star(problem, heuristics, verbose=True)
```

#### Classes de Recherche - Maroc

```python
# VillesMarocSearchStrategy
VillesMarocSearchStrategy.dfs(problem, verbose=True)
VillesMarocSearchStrategy.bfs(problem, verbose=True)
VillesMarocSearchStrategy.ucs(problem, verbose=True)
VillesMarocSearchStrategy.a_star(problem, heuristics, verbose=True)
```

#### Environnement et Agent

```python
# Environnement
env = RabatEnvironment(graph)
env.set_agent_location(agent, location)
env.get_percepts(agent)
env.apply_action(agent, action)

# Problem Solving Agent
agent = ProblemSolvingAgent(name, search_strategy, problem)
agent.program(perceptms()

# Afficher les résultats
for algo, path in results.items():
    print(f"{algo}: {' → '.join(path)}")
```

### Exemple 3: Agent Autonome

```python
# Créer un agent de résolution de problème
agent = ProblemSolvingAgent(
    name="NavigatorBot",
    search_strategy=lambda p: RabatSearchStrategy.a_star(p, HEURISTICS_TO_KASBAH),
    problem=problem
)

# L'agent navigue automatiquement
env = RabatEnvironment(RABAT_GRAPH)
env.set_agent_location(agent, "Agdal")
```

---

## 📚 Documentation

### Algorithmes Détaillés

#### DFS (Depth-First Search)
- **Stratégie**: Explore en profondeur d'abord
- **Structure**: Stack (LIFO)
- **Complet**: Non (peut boucler)
- **Optimal**: Non

#### BFS (Breadth-First Search)
- **Stratégie**: Explore niveau par niveau
- **Structure**: Queue (FIFO)
### Algorithmes
- [ ] Ajouter d'autres algorithmes (IDS, Bidirectional Search)
- [ ] Implémenter des variantes (Greedy Best-First, Weighted A*)

### Visualisation
- [ ] Interface graphique pour visualiser les chemins
- [ ] Animation des algorithmes en temps réel
- [ ] Graphiques de comparaison des performances

### Fonctionnalités
- [ ] Support de graphes dynamiques (embouteillages, routes fermées)
- [ ] Intégration avec des cartes réelles (OpenStreetMap)
- [ ] API REST pour le service de navigation
- [ ] Plus de villes et quartiers marocains

### Qualité
- [ ] Tests unitaires complets
- [ ] Benchmarks de performance
- [ ] Documentation API complètee
- **Équipe Projet** - *Développement initial*

### Contributions

- **Navigation Rabat**: Implémentation complète avec Problem Solving Agent
- **Navigation Maroc**: Exercices pratiques avec 4 algorithmes comparés
- **Architecture AIMA**: Classes de base suivant les standards AIMA
- **Optimal**: Oui

#### A* (A-star)
- **Stratégie**: f(n) = g(n) + h(n)
- **Structure**: Priority Queue
- **Complet**: Oui
- **Optimal**: Oui (heuristique admissible)

### API Reference

```python
# Classe principale
RabatSearchStrategy.dfs(problem, verbose=True)
RabatSearchStrategy.bfs(problem, verbose=True)
RabatSearchStrategy.ucs(problem, verbose=True)
RabatSearchStrategy.a_star(problem, heuristics, verbose=True)

# Environnement
env = RabatEnvironment(graph)
env.set_agent_location(agent, location)
env.get_percepts(agent)
env.apply_action(agent, action)
```

---

## 🛠️ Technologies Utilisées

- **Python 3.8+** - Langage de programmation
- **Collections** - Structures de données (deque)
- **Heapq** - File de priorité pour UCS et A*
- **ABC** - Classes abstraites
- **Typing** - Annotations de type

---

## 🤝 Contribution

Les contributions sont les bienvenues! Voici comment participer:

1. **Fork** le projet
2. **Créer** une branche (`git checkout -b feature/amelioration`)
3. **Commit** vos changements (`git commit -m 'Ajout d'une fonctionnalité'`)
4. **Push** vers la branche (`git push origin feature/amelioration`)
5. **Ouvrir** une Pull Request

### Guidelines

- Suivre les conventions PEP 8
- Ajouter des tests pour les nouvelles fonctionnalités
- Documenter le code en français
- Mettre à jour le README si nécessaire

---

## 📝 Améliorations Futures

- [ ] Ajouter d'autres algorithmes (IDS, Bidirectional Search)
- [ ] Interface graphique pour visualiser les chemins
- [ ] Support de graphes dynamiques (embouteillages)
- [ ] Intégration avec des cartes réelles (OpenStreetMap)
- [ ] API REST pour le service de navigation
- [ ] Tests unitaires complets

---

## 📖 Références

- **AIMA**: Russell, S., & Norvig, P. (2020). *Artificial Intelligence: A Modern Approach* (4th ed.)
- **Algorithmes de recherche**: Introduction to Algorithms, Cormen et al.
- **Python Best Practices**: PEP 8 Style Guide

---

## 👥 Auteurs

- **Votre Nom** - *Développement initial*

---

## 📄 Licence

Ce projet est sous licence MIT - voir le fichier [LICENSE](LICENSE) pour plus de détails.

---

## 🙏 Remerciements

- Professeur pour le sujet du TP
- Communauté Python pour les outils excellents
- Contributeurs et testeurs

---

<div align="center">

**⭐ Si ce projet vous a aidé, n'oubliez pas de lui donner une étoile! ⭐**

Made with ❤️ and 🐍 Python

</div>
