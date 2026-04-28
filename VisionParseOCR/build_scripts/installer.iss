[Setup]
AppId=VisionParseOCR
AppName=VisionParseOCR
AppVersion=1.0.0
AppPublisher=Lindineu Duran
DefaultDirName={autopf}\VisionParseOCR
DefaultGroupName=VisionParseOCR
OutputDir=..\dist
OutputBaseFilename=VisionParseOCRInstaller
Compression=lzma
SolidCompression=yes
WizardStyle=modern
ArchitecturesInstallIn64BitMode=x64compatible
PrivilegesRequired=admin
UninstallDisplayIcon={app}\VisionParseOCR.exe

[Languages]
Name: "brazilianportuguese"; MessagesFile: "compiler:Languages\BrazilianPortuguese.isl"

[Tasks]
Name: "desktopicon"; Description: "Criar ícone na Área de Trabalho"; Flags: unchecked

[Files]
Source: "..\dist\VisionParseOCR\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\VisionParseOCR"; Filename: "{app}\VisionParseOCR.exe"
Name: "{autodesktop}\VisionParseOCR"; Filename: "{app}\VisionParseOCR.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\VisionParseOCR.exe"; Description: "Executar VisionParseOCR"; Flags: nowait postinstall skipifsilent