# Puissance 4 - IA Minimax

<img width="632" height="770" alt="image" src="https://github.com/user-attachments/assets/52c95738-0d3a-4716-b8e2-f1b88a10a9e6" />

Un jeu de Puissance 4 (Connect 4) avec une intelligence artificielle avancée développé en Python avec Tkinter.

## 🎯 Fonctionnalités

- **Interface graphique moderne** avec animations fluides
- **IA intelligente** utilisant l'algorithme Minimax avec élagage Alpha-Beta
- **Choix de couleur** pour l'IA (Rouge ou Jaune)
- **Suggestions visuelles** avec flèches animées
- **Animations de chute** des pièces avec effets de rebond
- **Détection automatique** des victoires et matchs nuls
- **Design personnalisé** avec tokens étoilés et couleurs attrayantes

## 🚀 Installation et Lancement

### Prérequis
- Python 3.7 ou plus récent
- Tkinter (généralement inclus avec Python)

### Installation
```bash
git clone https://github.com/Geoffreypierre/power4IA.git
cd power4IA
```
### Lancement
```bash
python main.py
```

## 🎮 Comment Jouer

1. **Démarrage** : Lancez l'application et choisissez la couleur de l'IA
2. **Placement** : Cliquez sur une colonne pour y placer votre pièce
3. **Objectif** : Alignez 4 pièces (horizontalement, verticalement ou en diagonale)
4. **IA** : L'intelligence artificielle joue automatiquement à son tour
5. **Recommencer** : Cliquez sur "NOUVELLE PARTIE" pour relancer

6. <img width="625" height="591" alt="image" src="https://github.com/user-attachments/assets/6913b14f-9ab8-42b8-94ac-a03c9584b649" />


## 🤖 Intelligence Artificielle

L'IA utilise plusieurs techniques avancées :

### Algorithme Minimax
- **Profondeur** : 7 niveaux d'anticipation
- **Élagage Alpha-Beta** : Optimisation des performances
- **Évaluation heuristique** : Analyse des positions et menaces

### Stratégies Implémentées
1. **Coups gagnants immédiats** : Priorité absolue aux victoires en 1 coup
2. **Blocage défensif** : Empêche l'adversaire de gagner
3. **Contrôle du centre** : Favorise les colonnes centrales
4. **Évaluation des menaces** : Détecte et contre les alignements adverses
5. **Optimisation des coups** : Ordonnancement intelligent pour l'élagage

### Système d'Évaluation
- **Victoire** : ±10000 points
- **3 alignés + 1 libre** : ±90 points (défense renforcée)
- **2 alignés + 2 libres** : ±5 points
- **Position centrale** : +6 points par pièce

## 🎨 Interface Utilisateur

### Éléments Visuels
- **Plateau** : Design sombre moderne (#2c2444)
- **Pièces** : Tokens avec étoiles intégrées et effets de profondeur
- **Animations** : Chute réaliste avec gravité et rebonds
- **Suggestions** : Flèches animées pour les coups de l'IA
- **Survol** : Prévisualisation transparente des coups

### Couleurs
- **Rouge** : #c62128 (Joueur/IA Rouge)
- **Jaune** : #f8ff0c (Joueur/IA Jaune)  
- **Cyan** : #00d2d3 (Suggestions IA)
- **Fond** : Thème sombre élégant

## 📁 Structure du Code

```
connect4_game.py
├── Connect4Game (Classe principale)
├── Interface graphique (Tkinter)
├── Logique de jeu
├── Intelligence artificielle
└── Animations et effets
```

### Méthodes Principales
- `setup_gui()` : Initialisation de l'interface
- `minimax()` : Algorithme d'IA avec élagage Alpha-Beta
- `find_winning_move()` : Détection des coups critiques
- `evaluate_board_for_ai()` : Évaluation des positions
- `animate_piece_drop()` : Animations de chute

## ⚙️ Configuration

### Paramètres Modifiables
```python
ROWS = 6              # Hauteur du plateau
COLS = 7              # Largeur du plateau  
CELL_SIZE = 80        # Taille des cellules
ANIMATION_SPEED = 8   # Vitesse d'animation
depth = 7             # Profondeur de l'IA
```

## 🏆 Niveaux de Difficulté

L'IA est configurée pour être très compétitive :
- **Anticipation** : 7 coups à l'avance
- **Réactivité** : Blocage automatique des menaces
- **Stratégie** : Jeu positionnel optimisé

Pour ajuster la difficulté, modifiez la profondeur dans `get_best_move()`.
---

**Amusez-vous bien et essayez de battre l'IA ! 🎮**


