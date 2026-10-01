# Manuel utilisateur - EduPaie

## Introduction

EduPaie est une application de gestion des paiements scolaires pour les écoles. Elle permet d'enregistrer les élèves, leurs frais de scolarité, de suivre les paiements et d'imprimer des reçus numérotés.

## Premier lancement

Au premier lancement, l'application :
1. Crée automatiquement la base de données
2. Insère des données de test (15 élèves avec paiements variés)
3. Initialise le système de numérotation des reçus

## Interface principale

L'interface se compose de :

- **Barre latérale** (gauche) : Navigation entre les vues
  - Tableau de bord
  - Élèves
  - Quitter

- **Zone de contenu** (droite) : Vue courante avec titre en haut

## Tableau de bord

Le tableau de bord affiche 4 cartes de statistiques :

1. **Nombre d'élèves** : Total des élèves enregistrés
2. **Total encaissé** : Somme de tous les paiements reçus
3. **Total restant dû** : Solde cumulé de tous les élèves
4. **Élèves non soldés** : Nombre d'élèves qui n'ont pas payé en totalité

### Liste des élèves

Le tableau de bord permet de filtrer les élèves par statut :
- **Tous** : Affiche tous les élèves
- **Soldé** : Élèves qui ont payé la totalité
- **Partiellement payé** : Élèves qui ont effectué un paiement mais ont encore un solde
- **Non payé** : Élèves qui n'ont effectué aucun paiement

Cliquez sur **Actualiser** pour rafraîchir les données.

## Gestion des élèves

### Ajouter un élève

1. Cliquez sur le bouton **Élèves** dans la barre latérale
2. Cliquez sur le bouton **Ajouter**
3. Remplissez le formulaire :
   - **Nom** : Nom de famille de l'élève (obligatoire)
   - **Prénom** : Prénom de l'élève (obligatoire)
   - **Classe** : Ex: 6ème A, 5ème B (obligatoire)
   - **Année scolaire** : Ex: 2025-2026 (obligatoire)
   - **Total dû (FCFA)** : Montant total de la scolarité (obligatoire)
4. Cliquez sur **Enregistrer**

### Modifier un élève

1. Sélectionnez l'élève dans la liste
2. Cliquez sur le bouton **Modifier**
3. Modifiez les champs souhaités
4. Cliquez sur **Enregistrer**

### Supprimer un élève

1. Sélectionnez l'élève dans la liste
2. Cliquez sur le bouton **Supprimer**
3. Confirmez la suppression

**Attention** : Un élève qui a des paiements ne peut pas être supprimé.

### Rechercher un élève

Utilisez la barre de recherche en haut pour chercher par nom ou prénom. La recherche est insensible à la casse.

### Filtrer par classe

Utilisez la liste déroulante pour afficher uniquement les élèves d'une classe spécifique.

### Voir les détails d'un élève

- Double-cliquez sur une ligne
- Ou cliquez droit → **Voir les détails**

La fiche élève affiche :
- Informations de base (nom, prénom, classe, année)
- Situation financière (total dû, payé, solde, statut)
- Historique chronologique des paiements

## Enregistrement des paiements

### Enregistrer un paiement

1. Depuis la liste des élèves, sélectionnez l'élève
2. Cliquez sur le bouton **Enregistrer paiement**
3. Remplissez le formulaire :
   - **Montant (FCFA)** : Montant du versement (doit être positif et ne pas dépasser le solde)
   - **Date du paiement** : Date du versement
   - **Mode de paiement** : Espèces, Chèque, Virement ou Mobile Money
4. Le solde avant et après paiement s'affiche en temps réel
5. Cliquez sur **Enregistrer**
6. Confirmez le paiement

Le reçu PDF est envoyé à l'imprimante par défaut après validation et enregistré dans `data/recus_pdf`. Dans la version installée, il se trouve dans le dossier de données utilisateur EduPaie.

### Règles de validation

- Le montant doit être un entier positif
- Le montant ne peut pas dépasser le solde restant
- La date doit être valide
- Le mode de paiement doit être choisi parmi les quatre modes proposés

### Réimprimer un reçu

1. Ouvrez la fiche de l'élève
2. Dans l'historique des paiements, sélectionnez le paiement
3. Cliquez sur le bouton **Imprimer le reçu**

Le reçu sera régénéré à l'identique et ouvert.

## Reçus PDF

Chaque reçu contient :
- Numéro unique (ex: REC-2025-000001)
- Nom de l'établissement
- Informations de l'élève (nom, prénom, classe)
- Détails du paiement (date, mode, montant)
- Montant en toutes lettres
- Solde restant après ce paiement
- Date de génération du reçu

## Statuts de paiement

Trois statuts sont possibles :

- **Soldé** (vert) : L'élève a payé la totalité
- **Partiellement payé** (orange) : L'élève a effectué un paiement mais a encore un solde
- **Non payé** (rouge) : L'élève n'a effectué aucun paiement

## Astuces

- Utilisez la barre de recherche pour trouver rapidement un élève
- Le tableau de bord vous donne une vue d'ensemble de la situation financière
- Les reçus sont automatiquement numérotés de façon unique
- Vous pouvez réimprimer un reçu à tout moment depuis l'historique
- Le solde affiché est calculé en temps réel

## Dépannage

### L'application ne démarre pas

- Vérifiez que Python 3.10+ est installé
- Vérifiez que les dépendances sont installées : `pip install -r requirements.txt`
- Consultez le fichier de log dans `~/.edupaie/logs/`

### Erreur "Base de données introuvable"

- Exécutez : `python -m src.database.init_db`
- Cela recréera la base de données

### Le reçu PDF ne s'ouvre pas

- Vérifiez que vous avez une application PDF installée (Adobe Reader, etc.)
- Le reçu est enregistré sur votre bureau

### Les montants s'affichent mal

- Les montants sont toujours en FCFA, sans décimales
- Utilisez uniquement des entiers (ex: 50000, pas 50000.50)

## Support

Pour toute question ou problème, consultez la documentation technique dans `docs/`.
