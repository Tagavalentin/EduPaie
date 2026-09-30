# Guide d'installation de l'exécutable EduPaie

## Prérequis

- Windows 10 ou supérieur
- 100 Mo d'espace disque libre
- Permissions d'écriture dans le dossier utilisateur

## Installation

### Option 1 : Télécharger l'exécutable

1. Téléchargez le fichier `EduPaie.exe` depuis le dépôt ou le lien fourni
2. Placez-le dans un dossier de votre choix (ex: `C:\Program Files\EduPaie`)
3. Double-cliquez sur `EduPaie.exe` pour lancer l'application

### Option 2 : À partir du code source

Si vous avez le code source, vous pouvez construire l'exécutable vous-même :

1. Assurez-vous d'avoir Python 3.10+ installé
2. Naviguez vers le dossier du projet
3. Exécutez le script de build :
   ```
   build\build.bat
   ```
4. L'exécutable sera généré dans le dossier `dist/`
5. Copiez `dist\EduPaie.exe` vers le dossier d'installation souhaité

## Premier lancement

Au premier lancement :

1. L'application créera automatiquement les dossiers nécessaires :
   - `%LOCALAPPDATA%\EduPaie\` pour les données
   - `%USERPROFILE%\.edupaie\logs\` pour les logs

2. La base de données sera initialisée avec :
   - Le schéma des tables
   - 15 élèves de test avec paiements variés

3. Vous verrez la fenêtre principale avec le tableau de bord

## Dossier de données

Les données de l'application sont stockées dans :

```
%LOCALAPPDATA%\EduPaie\
└── edupaie.db
```

**Important** : Ne supprimez pas ce dossier si vous voulez conserver vos données.

## Sauvegarde des données

Pour sauvegarder vos données :

1. Fermez l'application EduPaie
2. Copiez le fichier `%LOCALAPPDATA%\EduPaie\edupaie.db`
3. Collez-le dans un dossier de sauvegarde (ex: clé USB, cloud)

Pour restaurer :

1. Fermez l'application EduPaie
2. Copiez votre fichier de sauvegarde
3. Remplacez `%LOCALAPPDATA%\EduPaie\edupaie.db` par votre sauvegarde
4. Relancez l'application

## Désinstallation

Pour désinstaller EduPaie :

1. Supprimez le fichier `EduPaie.exe`
2. Supprimez le dossier de données si vous ne voulez plus conserver vos données :
   - `%LOCALAPPDATA%\EduPaie\`
   - `%USERPROFILE%\.edupaie\`

## Mise à jour

Pour mettre à jour EduPaie :

1. Téléchargez la nouvelle version de `EduPaie.exe`
2. Remplacez l'ancien fichier par le nouveau
3. Relancez l'application

**Note** : Vos données sont conservées automatiquement car elles sont stockées dans le dossier utilisateur, pas dans le dossier de l'exécutable.

## Problèmes courants

### "L'application ne démarre pas"

- Vérifiez que Windows Defender ou votre antivirus ne bloque pas l'exécutable
- Ajoutez une exception pour `EduPaie.exe` si nécessaire
- Exécutez en tant qu'administrateur si vous rencontrez des problèmes de permissions

### "Erreur d'accès à la base de données"

- Vérifiez que vous avez les permissions d'écriture dans `%LOCALAPPDATA%`
- Désactivez temporairement votre antivirus si nécessaire

### "L'application plante au démarrage"

- Consultez les logs dans `%USERPROFILE%\.edupaie\logs\`
- Envoyez le fichier de log au support technique

## Ports réseau

EduPaie n'utilise aucun port réseau. Elle fonctionne entièrement hors-ligne.

## Antivirus

Certains antivirus peuvent marquer l'exécutable comme suspect car il est généré avec PyInstaller. Si cela se produit :

1. Ajoutez une exception pour `EduPaie.exe`
2. Ou désactivez temporairement l'antivirus pour l'installation
3. L'application est signée numériquement (si disponible)

## Configuration requise

- **Système** : Windows 10 ou supérieur
- **Processeur** : Intel Core i3 ou équivalent
- **RAM** : 2 Go minimum (4 Go recommandé)
- **Espace disque** : 100 Mo minimum
- **Écran** : 1024x768 minimum

## Support

Pour toute question ou problème de installation, consultez :
- Le manuel utilisateur : `docs/manuel_utilisateur.md`
- La documentation technique : `docs/architecture.md`
