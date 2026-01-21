# Résumé pour Codex (version projet scolaire)

## Objectif du projet

Développer une application de démonstration capable d’analyser en temps réel le contenu affiché à l’écran d’un joueur dans un environnement de test, afin d’identifier des éléments interactifs (ex : ressources récoltables) et déclencher des actions automatiques (clic / déplacement) selon une logique définie.

**Contrainte éthique :** l’application est uniquement utilisée dans un cadre éducatif et technique, sur une version de test / environnement simulé, et n’est pas destinée à une utilisation en production ni en ligne.

## Fonctionnalités principales (MVP)

### Capture d’écran en temps réel

- Lecture continue du flux écran de la zone de jeu (ex : 10–30 FPS)
- Possibilité de limiter la capture à une région (ROI) pour optimiser

### Détection d’objets d’intérêt

- Détecter des ressources récoltables via :
  - classification/détection d’image (modèle type YOLO / template matching)
  - ou détection par couleur + contours (si éléments visuels stables)
- Retourner : position (x,y), classe, score de confiance

### Prise de décision

- Sélectionner la cible optimale (la plus proche, meilleure priorité, etc.)
- Définir une machine à états :
  - SEARCH (chercher une ressource)
  - MOVE_TO_TARGET (se déplacer vers la cible)
  - HARVEST (interagir / récolter)
  - MOUNT (monter)
  - RETURN_SEARCH (retour à la recherche)

### Action simulée

- Envoyer des actions de haut niveau :
  - clic sur la ressource
  - déplacement vers une position
  - interaction / raccourcis
- Ajout de délais aléatoires + anti-boucle (pour stabilité)

## Périmètre (phase 1)

- Fonctionne dans une seule map
- Quelques ressources détectables (2–3 types)
- Chemin simple : « aller → récolter → remonter → repartir »
- Pas de gestion de combat / ennemis / inventaire / multi-map

## Architecture proposée

### Modules

- **ScreenCapture** : acquisition du flux écran
- **Detector** : modèle/détection + post-processing
- **Tracker** (optionnel) : stabiliser la cible dans le temps
- **DecisionEngine** : machine à états + logique de priorité
- **ActionExecutor** : interface d’entrée (clic, clavier)
- **Logger/UI** : overlay debug + logs + FPS

### Pipeline

Capture → Détection → Filtrage → Choix cible → Action → Vérification → boucle

## Données & entraînement (si ML)

### Dataset maison

- captures d’écran annotées (ressource / non ressource)
- augmentation simple (contraste, zoom, bruit)

### Évaluation

- précision / rappel sur images test
- FPS et latence globale

## Critères de réussite

- Détection stable (peu de faux positifs)
- Comportement cohérent sur une map donnée
- Logs montrant :
  - nombre de ressources détectées / récoltées
  - temps moyen par cycle
  - états de la machine

## Livrables attendus

- Code source structuré
- Documentation (README) :
  - installation
  - limites
  - mode debug
- Démo vidéo + rapport court expliquant :
  - méthode de détection
  - décisions
  - choix techniques
  - considérations éthiques

## Options

Si tu veux, je peux aussi faire :

- une version ultra courte « copiable dans Codex »
- un plan de rapport scolaire (intro → méthode → résultats → limites → éthique)

## Démarrage rapide (prototype)

Ce dépôt inclut un pipeline minimal en Python pour simuler la boucle capture → détection → décision → action.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
PYTHONPATH=src python -m codex_demo.main
```

Exemple avec ROI et couleur cible (ici jaune/vert) :

```bash
PYTHONPATH=src python -m codex_demo.main --roi 100 100 800 600 --hsv-lower 25 80 80 --hsv-upper 40 255 255
```

## Pour compléter le projet

Il faudra remplacer les stubs par des implémentations réelles :

- **Capture écran** : intégrer un backend (ex : mss, dxcam) + gestion ROI + FPS stable.
- **Détection** : brancher un modèle (YOLO, template matching, ou couleur/contours) + NMS + seuils.
- **Tracking** (optionnel) : associer les détections sur plusieurs frames pour stabiliser la cible.
- **Actions** : connecter un contrôleur d’entrées (clics/clavier) avec sécurité et délais.
- **UI/Logs** : overlay debug (FPS, bbox), enregistrement de statistiques, export CSV/JSON.
- **Données** : constituer un dataset annoté + scripts d’augmentation + évaluation précision/rappel.
