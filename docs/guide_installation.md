# Guide d'installation de l'exécutable EduPaie

## Prérequis

- Windows 10 ou supérieur
- 100 Mo d'espace disque libre
- Permissions d'écriture dans le dossier utilisateur

## Installation de l'application

### Depuis l'installateur

1. Téléchargez `EduPaie-Setup-1.0.1.exe` depuis les
   [releases GitHub](https://github.com/Tagavalentin/EduPaie/releases), puis ouvrez-le.
2. L'installation se fait pour votre compte Windows, sans droits administrateur,
   dans `%LOCALAPPDATA%\Programs\EduPaie`.
3. Lancez EduPaie depuis le menu Démarrer. Un raccourci sur le Bureau peut être
   sélectionné pendant l'installation.

### Construire l'installateur depuis les sources

Installez Python 3.10+ et Inno Setup 6, puis :

1. Ouvrez le dossier du projet.
2. Exécutez le script de build :
   ```
   build\build.bat
   ```
3. L'installateur est créé dans `dist\installer\EduPaie-Setup-1.0.1.exe`.

## Premier lancement

Au premier lancement :

1. L'application créera automatiquement les dossiers nécessaires :
   - `%LOCALAPPDATA%\EduPaie\` pour la base et les reçus
   - `%USERPROFILE%\.edupaie\logs\` pour les logs

2. La base de données sera initialisée avec :
   - Le schéma des tables
   - Aucun élève de démonstration ; vous pourrez saisir les élèves de l'établissement

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

Dans **Paramètres Windows > Applications > Applications installées**, choisissez
EduPaie puis **Désinstaller**. Le désinstalleur retire l'application et ses
raccourcis, mais conserve la base et les reçus dans `%LOCALAPPDATA%\EduPaie\`.

Pour supprimer aussi les données, fermez EduPaie puis supprimez séparément :

- `%LOCALAPPDATA%\EduPaie\`
- `%USERPROFILE%\.edupaie\`

## Mise à jour

Pour mettre à jour EduPaie :

1. Fermez EduPaie.
2. Téléchargez et exécutez la nouvelle version de `EduPaie-Setup-*.exe`.
3. Gardez le même dossier d'installation afin de mettre à jour la version en
   place.
4. Relancez EduPaie depuis le menu Démarrer.

**Note** : la base et les reçus restent dans `%LOCALAPPDATA%\EduPaie\`, séparés
des fichiers remplacés par l'installation.

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
3. Les versions publiées ne sont pas signées numériquement pour le moment.
   Vérifiez que le fichier provient bien des releases officielles EduPaie.

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
