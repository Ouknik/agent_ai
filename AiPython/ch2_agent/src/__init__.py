
from typing import Dict, Optional
from .agent import Agent, Environment, Sensor, Actuator

# Types de base
Percept = Dict
Action = str


# ============================================
# Agent de nettoyage simple
# ============================================

class SimpleCleaningAgent(Agent):
    """Robot de nettoyage simple et facile à comprendre"""
    
    def __init__(self, name: str):
        super().__init__(name)
        self.energy = 100  #  (0-100)
        self.cleaned_count = 0  # Nombre des  nettoyées
        
    def program(self, percept: Percept = None) -> Optional[Action]:
        """Le cerveau du robot - décide quoi faire"""
        
        if not percept:
            return None
        
        # Lire les informations
        energy = percept.get("energy", 100)
        is_dirty = percept.get("is_dirty", False)
        
        # Règle 1: Si énergie faible → dormir
        if energy < 30:
            return "sleep"
        
        # Règle 2: Si la cellule est sale → nettoyer
        if is_dirty:
            return "clean"
        
        # Règle 3: Sinon → se déplacer
        return "move"


from typing import Dict, Optional
from .agent import Agent, Environment, Sensor, Actuator

# Types de base
Percept = Dict
Action = str


# ============================================
# 1. ROBOT DE NETTOYAGE (Agent)
# ============================================

class RobotNettoyage(Agent):
    """Un robot simple qui nettoie"""
    
    def __init__(self, name: str):
        super().__init__(name)
        self.energie = 100  # Énergie: 0 à 100
        
    def program(self, percept: Percept = None) -> Optional[Action]:
        """Le robot décide quoi faire"""
        
        # Lire: est-ce que c'est sale?
        est_sale = percept.get("sale", False)
        
        # Décider:
        if est_sale:
            return "nettoyer"  # Si sale → nettoyer
        else:
            return "avancer"   # Si propre → avancer


# ============================================
# 2. CAPTEUR (Sensor)
# ============================================

class CapteurSimple(Sensor):
    """Le capteur regarde si c'est sale ou propre"""
    
    def sense(self, env, agent) -> Percept:
        position = env.position_robot
        est_sale = env.pieces[position]  # True = sale, False = propre
        
        return {
            "sale": est_sale,
            "position": position
        }


# ============================================
# 3. ACTIONNEUR (Actuator)
# ============================================

class ActionneurSimple(Actuator):
    """L'actionneur fait les actions"""
    
    def act(self, env, agent, action: Action) -> None:
        
        if action == "nettoyer":
            # Nettoyer la pièce actuelle
            env.pieces[env.position_robot] = False  # Devient propre
            agent.energie -= 5
            agent.performance += 10
            print(f"   → 🧹 Nettoyage de la pièce {env.position_robot}")
            
        elif action == "avancer":
            # Aller à la pièce suivante
            env.position_robot += 1
            agent.energie -= 2
            print(f"   → 🚶 Avance vers la pièce {env.position_robot}")


# ============================================
# 4. ENVIRONNEMENT (Environment)
# ============================================

class MaisonSimple(Environment):
    """Une maison avec 5 pièces"""
    
    def __init__(self):
        super().__init__()
        # Liste des pièces: True = sale, False = propre
        self.pieces = [True, True, False, True, False]  
        self.position_robot = 0  
        self.capteur = CapteurSimple()
        self.actionneur = ActionneurSimple()
        
    def get_percepts(self, agent) -> Percept:
        return self.capteur.sense(self, agent)
    
    def apply_action(self, agent, action: Action) -> None:
        self.actionneur.act(self, agent, action)
    
    def est_fini(self) -> bool:
        # Fini si le robot a visité toutes les pièces
        return self.position_robot >= len(self.pieces)
    
    def afficher(self):
        print("\n   Pièces de la maison:")
        for i, sale in enumerate(self.pieces):
            if i == self.position_robot:
                etat = "🤖💩" if sale else "🤖✨"
            else:
                etat = "💩" if sale else "✨"
            print(f"   Pièce {i}: {etat}")


# ============================================
# 5. PROGRAMME PRINCIPAL
# ============================================

if __name__ == "__main__":
    
    print("\n" + "="*50)
    print("🤖 ROBOT DE NETTOYAGE SIMPLE")
    print("="*50)
    
    # Créer la maison et le robot
    maison = MaisonSimple()
    robot = RobotNettoyage("CleanBot")
    
    print(f"\n🏠 Maison avec {len(maison.pieces)} pièces")
    print(f"   Pièces sales: {sum(maison.pieces)} pièces")
    maison.afficher()
    
    print(f"\n🤖 Robot: {robot.name}")
    print(f"   Énergie: {robot.energie}%")
    
    # Boucle de nettoyage
    print("\n" + "="*50)
    print("▶️  DÉBUT DU NETTOYAGE")
    print("="*50)
    
    etape = 1
    while not maison.est_fini():
        print(f"\n📍 Étape {etape} - Pièce {maison.position_robot}")
        
        # 1. Regarder (Percevoir)
        percept = maison.get_percepts(robot)
        print(f"   👁️  Le robot voit: {'Sale 💩' if percept['sale'] else 'Propre ✨'}")
        
        # 2. Décider
        action = robot.program(percept)
        print(f"   🧠 Le robot décide: {action}")
        
        # 3. Agir
        maison.apply_action(robot, action)
        
        etape += 1
    
    # Résultat final
    print("\n" + "="*50)
    print("✅ NETTOYAGE TERMINÉ!")
    print("="*50)
    maison.afficher()
    print(f"\n📊 Résultats:")
    print(f"   Pièces sales restantes: {sum(maison.pieces)}")
    print(f"   Énergie restante: {robot.energie}%")
    print(f"   Performance: {robot.performance}")
    print("="*50 + "\n")

