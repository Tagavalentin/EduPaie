# Architecture d'EduPaie

## Vue d'ensemble

EduPaie est une application desktop Python suivant une architecture en 3 couches strictement séparées.

## Couches de l'architecture

### 1. Couche d'accès aux données (Repositories)

**Emplacement** : `src/repositories/`

**Responsabilités** :
- Encapsuler tout le code SQL
- Fournir des méthodes CRUD pour les entités
- Gérer les transactions (commit/rollback)
- Ne contenir aucune règle métier

**Exemples** :
- `StudentRepository` : create, get_by_id, get_all, search_by_name, filter_by_class, update, delete
- `PaymentRepository` : create, get_by_id, get_by_student, get_sum_by_student

**Contrainte** : Toutes les requêtes SQL sont paramétrées pour éviter les injections SQL.

### 2. Couche métier (Services)

**Emplacement** : `src/services/`

**Responsabilités** :
- Contenir toute la logique métier
- Valider les données (montants, dates, règles)
- Calculer les valeurs dérivées (solde, statut)
- Coordonner les opérations entre plusieurs repositories
- Générer les numéros de reçus de façon atomique

**Exemples** :
- `StudentService` : calcul du solde, détermination du statut, vérification de suppression
- `PaymentService` : validation du montant, génération du numéro de reçu, création atomique
- `DashboardService` : calcul des statistiques globales

**Contrainte** : Aucun accès direct à la base de données. Toujours passer par les repositories.

### 3. Couche présentation (UI)

**Emplacement** : `src/ui/`

**Responsabilités** :
- Afficher les données à l'utilisateur
- Capturer les entrées utilisateur
- Gérer les interactions (clics, saisies)
- Appeler les services pour les opérations métier

**Exemples** :
- `MainWindow` : Fenêtre principale avec navigation
- `StudentsView` : Liste des élèves avec recherche et filtrage
- `StudentForm` : Formulaire d'ajout/modification
- `PaymentDialog` : Dialogue d'enregistrement de paiement
- `DashboardView` : Tableau de bord avec statistiques

**Contrainte** : Un widget n'exécute jamais de requête SQL. Toute opération passe par les services.

## Flux de données typique

```
UI (Widget) → Service → Repository → Base de données
```

Exemple pour l'enregistrement d'un paiement :

1. `PaymentDialog` capture les données utilisateur
2. `PaymentDialog` appelle `PaymentService.create_payment()`
3. `PaymentService` valide le montant via `StudentService.calculate_balance()`
4. `PaymentService` génère le numéro de reçu de façon atomique
5. `PaymentService` appelle `PaymentRepository.create()` dans une transaction
6. `PaymentRepository` exécute la requête SQL paramétrée
7. Le paiement est enregistré avec le solde figé
8. `PaymentService` retourne le paiement créé
9. `PaymentDialog` génère le PDF via `PDFGenerator`
10. `PaymentDialog` affiche un message de succès

## Choix techniques

### Pourquoi SQLite ?

- Base de données intégrée, pas de serveur à installer
- Suffisant pour une application mono-utilisateur
- Module standard Python, pas de dépendance externe
- Transactions ACID garanties

### Pourquoi PySide6 et non Tkinter ?

- Qt moderne et professionnel
- Richesse des widgets (QTableView, QDateEdit, etc.)
- Styling QSS puissant
- Meilleure performance pour les tableaux
- Support natif sur chaque plateforme

### Pourquoi reportlab ?

- Génération PDF fiable et mature
- Contrôle total sur le layout
- Pas de dépendance externe (contrairement à wkhtmltopdf)
- Fonctionne hors-ligne

### Pourquoi num2words ?

- Conversion en toutes lettres multilingue
- Support du français natif
- Évite une implémentation manuelle complexe

### Pourquoi pas d'ORM ?

- SQL simple à lire et à maintenir
- Performance optimale (pas d'overhead)
- Contrôle total sur les requêtes
- Adapté à un schéma simple

## Gestion des erreurs

- Hook global `sys.excepthook` pour capturer les exceptions non gérées
- Logging dans un fichier utilisateur (`~/.edupaie/logs/`)
- QMessageBox pour les erreurs utilisateur
- Validation des champs avant les opérations
- Messages explicites pour éviter la confusion

## Chemins des fichiers

### En développement
- Base de données : `data/edupaie.db`
- Scripts SQL : `sql/`
- Logs : `~/.edupaie/logs/`

### En production (PyInstaller)
- Base de données : `%LOCALAPPDATA%\EduPaie\edupaie.db` (Windows)
- Scripts SQL : inclus dans l'exécutable via `sys._MEIPASS`
- Logs : `~/.edupaie/logs/`

## Limites connues

1. **Mono-utilisateur** : Pas de gestion multi-utilisateur ni de concurrence
2. **Pas de sauvegarde automatique** : L'utilisateur doit sauvegarder la base manuellement
3. **Pas d'export/import** : Impossible d'exporter les données en CSV/Excel
4. **Pas de rapports avancés** : Pas de graphiques ou de rapports périodiques
5. **Reçu simple** : Le reçu PDF est basique, pas de logo personnalisable
6. **Pas de multi-devise** : FCFA uniquement
