# EduPaie - Gestion des paiements scolaires

Application desktop pour la gestion des paiements scolaires en FCFA (Franc CFA).

## Fonctionnalités

- **Gestion des élèves** : Ajout, modification, suppression des élèves avec leurs frais de scolarité
- **Enregistrement des paiements** : Saisie des versements avec validation automatique du solde
- **Reçus PDF** : Génération automatique de reçus numérotés à chaque paiement
- **Historique** : Consultation de l'historique des paiements par élève
- **Tableau de bord** : Statistiques globales (total encaissé, restant dû, nombre d'élèves)
- **Recherche et filtrage** : Recherche par nom/prénom, filtrage par classe et statut de paiement

## Installation

### Prérequis

- Python 3.10 ou supérieur
- pip (gestionnaire de paquets Python)

### Installation des dépendances

```bash
pip install -r requirements.txt
```

### Initialisation de la base de données

```bash
python -m src.database.init_db
```

Cela créera la base de données `data/edupaie.db` avec le schéma et des données de test (15 élèves).

## Lancement

```bash
python main.py
```

## Structure du projet

```
edupaie/
├── main.py                      # Point d'entrée de l'application
├── requirements.txt            # Dépendances Python
├── README.md                    # Ce fichier
├── .gitignore                   # Fichiers ignorés par Git
├── sql/                         # Scripts SQL
│   ├── schema.sql              # Schéma de la base de données
│   └── seed.sql                # Données de test
├── data/                        # Base de données (générée)
│   └── edupaie.db
├── src/                         # Code source
│   ├── database/               # Couche d'accès aux données
│   │   ├── connection.py       # Gestion de la connexion SQLite
│   │   └── init_db.py         # Initialisation de la base
│   ├── repositories/           # DAO (Data Access Objects)
│   │   ├── student_repository.py
│   │   └── payment_repository.py
│   ├── services/               # Logique métier
│   │   ├── student_service.py
│   │   ├── payment_service.py
│   │   ├── receipt_service.py
│   │   └── dashboard_service.py
│   ├── models/                 # Dataclasses
│   │   ├── student.py
│   │   └── payment.py
│   ├── ui/                     # Interface PySide6
│   │   ├── main_window.py
│   │   ├── students_view.py
│   │   ├── student_form.py
│   │   ├── student_detail.py
│   │   ├── payment_dialog.py
│   │   ├── dashboard_view.py
│   │   ├── students_table_model.py
│   │   └── payments_table_model.py
│   └── utils/                  # Utilitaires
│       ├── formatters.py       # Formatage FCFA
│       ├── validators.py       # Validation des données
│       ├── pdf_generator.py   # Génération PDF
│       ├── paths.py            # Gestion des chemins
│       └── error_handler.py   # Gestion des erreurs
├── tests/                       # Tests unitaires
│   ├── test_student_repository.py
│   ├── test_payment_repository.py
│   ├── test_business_logic.py
│   └── test_pdf_generator.py
├── docs/                        # Documentation
│   └── mcd.md                  # Modèle Conceptuel de Données
└── build/                       # Configuration PyInstaller
    ├── edupaie.spec
    └── build.bat
```

## Documentation

- **Manuel utilisateur** : [docs/manuel_utilisateur.md](docs/manuel_utilisateur.md) - Guide complet pour les utilisateurs
- **Architecture** : [docs/architecture.md](docs/architecture.md) - Description technique de l'architecture
- **Guide d'installation** : [docs/guide_installation.md](docs/guide_installation.md) - Instructions pour l'exécutable
- **MCD/MLD** : [docs/mcd.md](docs/mcd.md) - Modèle Conceptuel de Données

## Tests

Lancer les tests unitaires :

```bash
pytest
```

Ou avec verbose :

```bash
pytest -v
```

## Build de l'exécutable (Windows)

### Prérequis

- PyInstaller (inclus dans requirements.txt)

### Build manuel

```bash
pyinstaller build/edupaie.spec --onefile --windowed
```

L'exécutable sera généré dans le dossier `dist/`.

### Build avec le script automatisé

```bash
build\build.bat
```

Ce script :
1. Vérifie que PyInstaller est installé
2. Initialise la base de données si nécessaire
3. Lance le build PyInstaller
4. Affiche le résultat

## Architecture

L'application suit une architecture en 3 couches :

1. **Couche données** (`src/repositories/`) : Accès à la base SQLite via des DAO
2. **Couche métier** (`src/services/`) : Logique de validation, calcul du solde, génération de reçus
3. **Couche présentation** (`src/ui/`) : Interface PySide6

Règle importante : un widget n'exécute jamais de requête SQL directement.

## Technologies

- **Python** 3.10+
- **PySide6** : Interface graphique (Qt)
- **SQLite** : Base de données (module standard sqlite3)
- **reportlab** : Génération de PDF
- **num2words** : Conversion montants en toutes lettres
- **pytest** : Tests unitaires
- **PyInstaller** : Packaging

## Devise

Tous les montants sont en FCFA (Franc CFA), stockés comme entiers (pas de décimales). L'affichage utilise le format `150 000 FCFA` avec séparateur de milliers par espace.

## Licence

Ce projet est un exercice pédagogique.
