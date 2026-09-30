# EduPaie - Gestion des paiements scolaires

Application desktop pour la gestion des paiements scolaires en FCFA (Franc CFA).

## Installation

```bash
pip install -r requirements.txt
```

## Lancement

```bash
python main.py
```

## Structure du projet

- `src/database/` : Connexion et initialisation de la base SQLite
- `src/repositories/` : DAO pour les élèves et paiements
- `src/services/` : Logique métier (solde, statut, validation)
- `src/models/` : Dataclasses (Student, Payment)
- `src/ui/` : Interface PySide6
- `src/utils/` : Utilitaires (formatters, validators, PDF)
- `tests/` : Tests unitaires
- `sql/` : Schéma et données de test
- `data/` : Base SQLite

## Technologies

- Python 3.10+
- PySide6 (interface)
- SQLite (base de données)
- reportlab (génération PDF)
