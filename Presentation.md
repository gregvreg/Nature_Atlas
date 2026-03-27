# Nature Atlas — Présentation du projet

---

## 1. Présentation globale du projet

### Naissance de l'idée

L'idée d'**Nature Atlas** est née d'un constat simple : la biodiversité mondiale est un sujet fascinant, mais souvent abordé de manière abstraite dans les cours. Nous voulions créer un outil qui permette de découvrir les animaux du monde de manière visuelle, interactive et ludique, en alliant une carte géographique à un système de quiz.

Le thème de l'édition 2026 des Trophées NSI — **Nature & Informatique** — correspondait parfaitement à cette envie.

### Problématique initiale

Comment créer une application éducative sur la faune mondiale qui soit à la fois agréable à utiliser, techniquement solide et représentative des compétences acquises en NSI ?

### Objectifs

- Concevoir une base de données relationnelle regroupant 100 espèces animales réparties sur 10 régions du monde.
- Développer une interface graphique complète en Python/Tkinter permettant d'explorer ces données visuellement.
- Proposer un module de quiz pour tester ses connaissances de manière ludique.
- Produire un projet fonctionnel, documenté et reproductible.

---

## 2. Organisation du travail

### Présentation de l'équipe

Le projet a été réalisé en équipe dans le cadre du cours de NSI.

### Répartition des tâches

| Membre | Responsabilités principales |
|--------|----------------------------|
| Gregory LIS | Base de données SQLite, script `sources/atlas_animaux.py`, données des animaux, module quiz (`sources/Quiz.py`), logique de tirage et affichage des scores |
| Gabriel RATINET | Module carte interactive (`sources/carte.py`), positionnement des régions, menu principal (`sources/Index.py`), cohérence visuelle, documentation |



### Temps passé sur le projet

Le projet a été développé sur plusieurs mois. Les principales phases ont été :

- Conception de la base de données et collecte des données : environ 2 semaines
- Développement de l'interface carte : environ 1 mois
- Développement du quiz : environ 1 mois
- Tests, corrections et documentation : environ 3 semaines

---

## 3. Présentation des étapes du projet

### Étape 1 — Conception de la base de données

La première étape a consisté à définir la structure de la base de données SQLite. Nous avons créé 4 tables : `Regions`, `Habitats`, `RegimesAlimentaires` et `Especes`, reliées par des clés étrangères. Nous avons ensuite sélectionné 100 animaux (10 par région), rédigé leurs descriptions et constitué le fichier `sources/atlas_animaux.py` qui peuple la base automatiquement.

### Étape 2 — Développement de la carte interactive

Nous avons ensuite travaillé sur le module `sources/carte.py`. La principale difficulté a été de positionner correctement les marqueurs de chaque région sur une image de carte du monde, en utilisant des coordonnées exprimées en pourcentage de la taille du canvas pour s'adapter à tous les écrans. Nous avons intégré un mode debug pour calibrer les positions.

### Étape 3 — Développement du quiz

Le module `sources/Quiz.py` propose un quiz de 10 questions tirées aléatoirement parmi les 100 animaux. Pour chaque question, 3 mauvaises régions sont tirées aléatoirement parmi les 9 restantes, et les 4 propositions sont mélangées. La correction est immédiate avec un retour visuel coloré.

### Étape 4 — Intégration et menu principal

Le fichier `sources/Index.py` a été développé en dernier pour assurer la cohérence visuelle entre les trois modules et offrir un point d'entrée unique à l'application. Les transitions entre modules sont gérées par des appels `subprocess` pour éviter les conflits entre fenêtres Tkinter.

### Étape 5 — Documentation et finalisation

La dernière étape a consisté à rédiger la documentation technique (ce fichier, le README, la licence) et à effectuer les tests finaux.

---

## 4. Validation de l'opérationnalité et du fonctionnement

### État d'avancement au moment du dépôt

Le projet est **entièrement fonctionnel** au moment du dépôt :

- La base de données se génère correctement via `python sources/atlas_animaux.py`.
- La carte interactive s'affiche avec les 10 régions, les galeries d'animaux et les fiches détaillées.
- Le quiz fonctionne correctement : tirage aléatoire, correction, score final.
- La navigation entre les modules (menu → carte → menu, menu → quiz → menu) est opérationnelle.

### Approches mises en œuvre pour vérifier l'absence de bugs

- Tests manuels répétés de tous les parcours utilisateur (clic sur chaque région, ouverture de chaque fiche, plusieurs parties de quiz).
- Test du comportement en cas de fichiers manquants (images, carte du monde) : l'application affiche un fallback sans planter.
- Test sur différentes résolutions d'écran pour vérifier l'adaptation de l'interface.

### Difficultés rencontrées et solutions apportées

**Problème 1 — Positionnement des marqueurs sur la carte.**
La carte du monde est redimensionnée dynamiquement selon la résolution de l'écran. Les marqueurs devaient donc être positionnés en coordonnées relatives (pourcentages) et non absolues. Nous avons créé un mode debug (`DEBUG_MODE = True`) qui affiche les coordonnées au clic pour calibrer les positions.

**Problème 2 — Gestion des images manquantes.**
Certaines images d'animaux pouvaient être absentes ou dans un format non supporté. Nous avons mis en place une fonction `load_image()` qui tente plusieurs extensions (`.jpg`, `.png`, `.avif`, `.webp`) et affiche un cadre vert de remplacement si aucune image n'est trouvée, évitant ainsi tout crash.

**Problème 3 — Navigation entre fenêtres Tkinter.**
La coexistence de plusieurs fenêtres Tkinter dans un même processus pouvait causer des conflits. Nous avons résolu ce problème en lançant chaque module dans un processus séparé via `subprocess.Popen()` et en quittant le processus courant avec `sys.exit()`.

---

## 5. Ouverture

### Idées d'amélioration

- Ajouter un **filtre par habitat ou régime alimentaire** sur la carte pour croiser les données.
- Implémenter un **système de scores sauvegardés** entre les sessions, en stockant les résultats du quiz dans la base SQLite.
- Ajouter un **mode apprentissage** : avant le quiz, l'utilisateur parcourt les fiches des animaux qui seront posés.
- Enrichir la base avec davantage d'espèces et de régions, ou ajouter des informations sur les espèces menacées.
- Proposer une **version web** du projet avec Flask et une interface HTML/CSS pour le rendre accessible sans installation.

### Analyse critique

Le projet remplit les objectifs fixés au départ. La base de données relationnelle est solide et extensible. L'interface graphique est cohérente et agréable à utiliser. Le quiz est fonctionnel et rejouable à l'infini.

En revanche, nous aurions pu mieux organiser notre code en séparant davantage la logique métier (accès à la base) de la logique d'affichage (Tkinter), selon le principe MVC. Cela aurait facilité la maintenance et les tests unitaires.

### Compétences développées

- Conception et manipulation d'une base de données relationnelle avec SQLite3.
- Développement d'interfaces graphiques en Python avec Tkinter.
- Gestion de fichiers et d'images avec Pillow.
- Organisation d'un projet en équipe : répartition des tâches, communication, gestion de version.
- Rédaction d'une documentation technique complète.

### Démarche d'inclusion

Le thème de la biodiversité mondiale a été choisi pour sa portée universelle. L'interface a été conçue avec un contraste élevé (thème sombre, textes clairs) pour améliorer la lisibilité. Les noms scientifiques latins sont systématiquement affichés aux côtés des noms communs.
