# Nature Atlas — Atlas animalier interactif

Découvrez la biodiversité mondiale à travers une carte interactive et un quiz de connaissances.
Explorez 100 animaux répartis sur 10 régions du globe, consultez leurs fiches détaillées et testez vos connaissances !

---

## 📋 Sommaire

- [📥 Installation et dépendances](#-installation-et-dépendances)
- [⏯️ Lancement de l'application](#-lancement-de-lapplication)
- [🎮 Utilisation](#-utilisation)
- [🧨 Bugs et problèmes connus](#-bugs-et-problèmes-connus)
- [⚙️ Description technique du projet](#-description-technique-du-projet)
- [👥 Crédits](#-crédits)

---

## 📥 Installation et dépendances


### Dépendances

Ce projet nécessite **Python 3.8 ou supérieur**.

Les bibliothèques nécessaires sont listées dans `requirements.txt`.
Leur installation se fait avec la commande suivante :

```
pip install -r requirements.txt
```

La seule bibliothèque externe requise est :
- **Pillow** — traitement et affichage des images

> `tkinter` et `sqlite3` sont inclus par défaut dans Python standard, aucune installation supplémentaire n'est nécessaire.

### Structure du projet

```
Nature_Atlas/
├── Licence.txt
├── Presentation.md
├── README.md
├── requirements.txt
├── data/
│   ├── animaux/
│   └── images/
└── sources/
    ├── atlas_animaux.py
    ├── carte.py
    ├── Index.py
    └── Quiz.py
```

---

## ⏯️ Lancement de l'application

### Étape 1 — Générer la base de données

Avant le premier lancement, exécutez le script de création de la base :

```
python sources/atlas_animaux.py
```

Ce script crée le fichier `atlas_animaux.db` et y insère les 100 animaux répartis en 10 régions.
Un message de confirmation s'affiche : `Base créée avec succès : 100 animaux insérés.`

> ⚠️ Cette étape n'est à effectuer qu'**une seule fois**.

### Étape 2 — Lancer le menu principal

```
python sources/Index.py
```

La fenêtre principale s'ouvre en plein écran. Depuis là, vous pouvez accéder à la carte ou au quiz.

---

## 🎮 Utilisation

### Menu principal

Deux options sont disponibles depuis l'écran d'accueil :

- **Accès à la carte** — ouvre la carte interactive du monde
- **Faire le quiz** — lance le quiz de 10 questions

### La carte interactive

1. La carte du monde s'affiche avec des marqueurs colorés pour chaque région.
2. Cliquez sur un **marqueur** ou sur un **nom de région** dans la légende à gauche pour afficher les animaux de cette région.
3. Cliquez sur une **carte animal** dans la galerie pour ouvrir sa fiche détaillée (photo, nom scientifique, habitat, régime alimentaire, taille, poids, espérance de vie, niveau trophique, description).
4. Fermez les fenêtres avec le bouton **✕ Fermer**.
5. Le bouton **<<< Retourner au menu** (en haut à gauche) revient au menu principal.

### Le quiz

1. Lisez les règles sur l'écran d'accueil, puis cliquez sur **▶ Lancer le quiz**.
2. Pour chaque question, observez la photo et le nom de l'animal, puis cliquez sur sa **région d'origine** parmi les 4 propositions.
3. La correction s'affiche immédiatement — vert pour une bonne réponse, rouge pour une mauvaise.
4. Cliquez sur **Question suivante ›** pour continuer.
5. À la fin des 10 questions, votre **score sur 10** s'affiche avec un message personnalisé.
6. Vous pouvez **rejouer**, **consulter la carte** pour réviser, ou **retourner au menu**.

---

## 🧨 Bugs et problèmes connus

- **Images manquantes.** Si le dossier `data/animaux/images/` est absent ou incomplet, les fiches animaux affichent un cadre vert vide à la place de la photo. L'application reste fonctionnelle.

- **Fenêtre trop petite.** L'application est conçue pour un écran ≥ 1280×768. Sur les très petits écrans, certains éléments peuvent être tronqués.

---

## ⚙️ Description technique du projet

Le fichier `sources/atlas_animaux.py` contient toutes les données (animaux, régions, habitats, régimes alimentaires) et crée la base de données SQLite `atlas_animaux.db` à la première exécution.

Le fichier `sources/Index.py` est le point d'entrée de l'application. Il affiche le menu principal et lance les deux modules.

Le fichier `sources/carte.py` contient tout le code relatif à la carte interactive : affichage de la carte du monde, placement des marqueurs de région, galerie d'animaux par région, et fiches détaillées.

Le fichier `sources/Quiz.py` contient le module quiz : tirage aléatoire des questions, affichage des propositions, correction immédiate, et écran de résultats.

Le dossier `data/animaux/images/` contient les images des 100 animaux au format `.jpg`, `.png` ou `.jpeg`.

---

## 👥 Crédits

### Cadre de réalisation

Ce projet a été créé dans le cadre des Trophées NSI, édition 2026, par Gabriel RATINET et Gregory LIS sur le thème **Nature & Informatique**.

### Usage de l'IA

L'assistant Claude (Anthropic) a été utilisé comme outil durant le projet, aux fins suivantes :

- Aide à la rédaction des descriptions des 100 animaux.
- Vérification de la cohérence des données scientifiques (noms latins, habitats, régimes alimentaires).

