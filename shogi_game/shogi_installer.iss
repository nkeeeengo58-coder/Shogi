; 将棋ゲーム インストーラースクリプト
; Inno Setup 6.0 以降が必要です

#define MyAppName "将棋ゲーム"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "将棋ゲーム開発チーム"
#define MyAppURL "https://github.com/nkeeeengo58-coder/Shogi"
#define MyAppExeName "将棋ゲーム.exe"

[Setup]
; アプリケーション情報
AppId={{8F5A2D3E-1B4C-4A5E-9D7F-2C8B6E1A3F9D}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}

; インストール設定
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
DisableProgramGroupPage=yes

; 出力設定
OutputDir=installer_output
OutputBaseFilename=将棋ゲーム_Setup_v{#MyAppVersion}
SetupIconFile=compiler:SetupClassicIcon.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern

; システム要件
ArchitecturesAllowed=x64
ArchitecturesInstallIn64BitMode=x64
MinVersion=6.1sp1

; 権限
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog

[Languages]
Name: "japanese"; MessagesFile: "compiler:Languages\Japanese.isl"

[CustomMessages]
japanese.NameAndVersion=%1 バージョン %2
japanese.AdditionalIcons=追加のアイコン:
japanese.CreateDesktopIcon=デスクトップにショートカットを作成する(&D)
japanese.CreateQuickLaunchIcon=クイック起動バーにショートカットを作成する(&Q)
japanese.ProgramOnTheWeb=%1 Web サイト
japanese.UninstallProgram=%1 をアンインストール
japanese.LaunchProgram=%1 を起動
japanese.AssocFileExtension=%2 ファイル拡張子を %1 に関連付ける(&A)
japanese.AssocingFileExtension=%2 ファイル拡張子を %1 に関連付けています...
japanese.AutoStartProgram=%1 を自動的に起動
japanese.RunAfterInstall=インストール後に %1 を起動する
japanese.ReadyMemoTasks=追加タスク:

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
; 実行ファイル
Source: "dist\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion

; ドキュメント
Source: "README.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "Docs\USER_GUIDE.md"; DestDir: "{app}"; DestName: "使い方.md"; Flags: ignoreversion

; NOTE: すべてのファイルに "Flags: ignoreversion" を使用しています

[Icons]
; スタートメニュー
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\使い方を見る"; Filename: "{app}\使い方.md"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"

; デスクトップ
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
; インストール後の実行
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
; アンインストール時にユーザーデータも削除するか確認
Type: filesandordirs; Name: "{userappdata}\shogi_game"

[Code]
// カスタム処理（必要に応じて追加）

// 既存のインストールをチェック
function InitializeSetup(): Boolean;
var
  OldVersion: String;
begin
  Result := True;
  
  // 既存のバージョンがインストールされているかチェック
  if RegQueryStringValue(HKLM, 'Software\Microsoft\Windows\CurrentVersion\Uninstall\{#SetupSetting("AppId")}_is1',
     'DisplayVersion', OldVersion) then
  begin
    if MsgBox('既に {#MyAppName} バージョン ' + OldVersion + ' がインストールされています。' + #13#10 +
              'アップデートを続行しますか？',
              mbConfirmation, MB_YESNO) = IDNO then
    begin
      Result := False;
    end;
  end;
end;

// インストール完了時の処理
procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssPostInstall then
  begin
    // 必要に応じて初回起動時の設定など
  end;
end;

// アンインストール開始時の処理
function InitializeUninstall(): Boolean;
begin
  Result := True;
  
  if MsgBox('セーブデータも削除しますか？' + #13#10 + #13#10 +
            'いいえを選択すると、セーブデータは保持されます。',
            mbConfirmation, MB_YESNO) = IDYES then
  begin
    // セーブデータの削除はUninstallDeleteセクションで処理
    Result := True;
  end
  else
  begin
    // セーブデータを保持
    Result := True;
  end;
end;
