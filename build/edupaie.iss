#define AppName "EduPaie"
#define AppVersion "1.0.0"
#define AppPublisher "EduPaie"
#define AppExeName "EduPaie.exe"

[Setup]
AppId={{78F3112C-E974-43CE-AE55-DC848C78A252}
AppName={#AppName}
AppVersion={#AppVersion}
AppPublisher={#AppPublisher}
DefaultDirName={localappdata}\Programs\EduPaie
DefaultGroupName={#AppName}
DisableProgramGroupPage=yes
PrivilegesRequired=lowest
UninstallDisplayName={#AppName}
UninstallDisplayIcon={app}\{#AppExeName}
OutputDir=..\dist\installer
OutputBaseFilename=EduPaie-Setup
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
CloseApplications=yes
SetupLogging=yes

[Tasks]
Name: "desktopicon"; Description: "Créer un raccourci sur le Bureau"; GroupDescription: "Raccourcis supplémentaires :"; Flags: unchecked

[Dirs]
Name: "{localappdata}\EduPaie"; Flags: uninsneveruninstall

[Files]
Source: "..\dist\EduPaie.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{autoprograms}\EduPaie"; Filename: "{app}\{#AppExeName}"; WorkingDir: "{app}"
Name: "{autodesktop}\EduPaie"; Filename: "{app}\{#AppExeName}"; WorkingDir: "{app}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#AppExeName}"; Description: "Lancer EduPaie"; Flags: nowait postinstall skipifsilent