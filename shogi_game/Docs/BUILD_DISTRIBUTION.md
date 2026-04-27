# 配布用ビルド手順

このドキュメントでは、Pythonがインストールされていない環境でも動作する配布パッケージの作成方法を説明します。

## 目次

1. [前提条件](#前提条件)
2. [PyInstallerでのEXE化](#pyinstallerでのexe化)
3. [Inno Setupでのインストーラー作成](#inno-setupでのインストーラー作成)
4. [配布パッケージの作成](#配布パッケージの作成)
5. [エンドユーザー向けインストール手順](#エンドユーザー向けインストール手順)

---

## 前提条件

### 開発環境（ビルドする側）

- Windows 10/11（推奨）
- Python 3.8以上
- 必要なパッケージ：
  ```bash
  pip install pyinstaller pillow
  ```

### Inno Setup（インストーラー作成用）

[Inno Setup 公式サイト](https://jrsoftware.org/isinfo.php)からダウンロードしてインストール

---

## PyInstallerでのEXE化

### 最も簡単な方法：ビルドスクリプトを使用（推奨）

プロジェクトには既に設定済みの `.spec` ファイルとビルドスクリプトが含まれています。

#### Windowsの場合:
```cmd
build.bat
```

#### macOS/Linuxの場合:
```bash
bash build.sh
```

これらのスクリプトが自動的に以下を実行します：
- 古いビルドファイルのクリーンアップ
- PyInstallerによるビルド  
- 実行ファイルの生成

### ステップ1: PyInstallerのインストール

```bash
pip install -r requirements.txt
pip install pyinstaller
```

### ステップ2: ビルドの実行

#### 方法A: ビルドスクリプトを使用（推奨）

```bash
# Windowsの場合
build.bat

# macOS/Linuxの場合
bash build.sh
```

#### 方法B: specファイルを直接使用

```bash
cd shogi_game
pyinstaller shogi_game.spec
```

既存の `shogi_game.spec` には以下が設定済みです：
- アプリケーションアイコン（`assets/icons/shogi_icon.ico`）
- 画像ファイルの自動同梱
- 詰将棋問題データの同梱
- 不要なモジュールの除外

既存の `shogi_game.spec` には以下が設定済みです：
- アプリケーションアイコン（`assets/icons/shogi_icon.ico`）
- 画像ファイルの自動同梱
- 詰将棋問題データの同梱
- 不要なモジュールの除外

#### specファイルの主な設定内容:

```python
# -*- mode: python ; coding: utf-8 -*-
block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('assets', 'assets'),           # 画像ファイルを含める
        ('data', 'data'),                # 詰将棋問題を含める
    ],
    hiddenimports=[
        'PIL._tkinter_finder',          # Pillowのtkinter連携
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',                    # 不要なモジュールを除外
        'numpy',
        'pandas',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='将棋ゲーム',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,              # コンソールウィンドウを表示しない
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/icons/shogi_icon.ico'  # アイコンを設定
)
```

### ステップ3: 動作確認

ビルドが成功すると、`dist/将棋ゲーム.exe` が生成されます。

```bash
cd dist
./将棋ゲーム.exe
```

### 確認事項
- ✅ アプリケーションが起動する
- ✅ アイコンが正しく表示される（タイトルバー、タスクバー）
- ✅ 盤面画像が表示される
- ✅ 駒画像（15種類すべて）が表示される
- ✅ ゲームが正常に動作する
- ✅ 保存/読み込み機能が動作する

### トラブルシューティング

#### エラー: モジュールが見つからない

```bash
# 必要なモジュールを明示的に指定
pyinstaller --hidden-import=PIL --hidden-import=tkinter 将棋ゲーム.spec
```

#### 起動が遅い

`--onefile` オプションを外して、ディレクトリ形式でビルド：

```python
# .specファイルで onefile=False に変更
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,  # これを追加
    name='将棋ゲーム',
    # ...
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='将棋ゲーム',
)
```

---

## Inno Setupでのインストーラー作成

### ステップ1: Inno Setupのインストール

[Inno Setup](https://jrsoftware.org/isinfo.php) をダウンロードしてインストール

### ステップ2: スクリプトファイルの作成

`shogi_installer.iss` ファイルを作成：

```iss
; 将棋ゲーム インストーラースクリプト

#define MyAppName "将棋ゲーム"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "Your Name"
#define MyAppExeName "将棋ゲーム.exe"

[Setup]
; アプリケーション情報
AppId={{YOUR-UNIQUE-APP-ID-HERE}}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
OutputDir=installer_output
OutputBaseFilename=将棋ゲーム_Setup_v{#MyAppVersion}
Compression=lzma
SolidCompression=yes
WizardStyle=modern

; インストール要件
ArchitecturesAllowed=x64
ArchitecturesInstallIn64BitMode=x64

; アイコン（オプション）
; SetupIconFile=assets\icon.ico

[Languages]
Name: "japanese"; MessagesFile: "compiler:Languages\Japanese.isl"

[Tasks]
Name: "desktopicon"; Description: "デスクトップにショートカットを作成(&D)"; GroupDescription: "追加のアイコン:";

[Files]
; 実行ファイル（onefile版）
Source: "dist\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion

; または、ディレクトリ版の場合
; Source: "dist\将棋ゲーム\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

; README
Source: "README.md"; DestDir: "{app}"; Flags: ignoreversion

; ライセンス（あれば）
; Source: "LICENSE.txt"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\アンインストール {#MyAppName}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent
```

### ステップ3: AppIdの生成

Inno Setup Compilerで `Tools` > `Generate GUID` を選択してユニークなIDを生成し、`{YOUR-UNIQUE-APP-ID-HERE}` を置き換えます。

### ステップ4: コンパイル

#### GUI から：
1. Inno Setup Compilerを起動
2. `File` > `Open` で `shogi_installer.iss` を開く
3. `Build` > `Compile` でビルド

#### コマンドラインから：
```bash
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" shogi_installer.iss
```

### ステップ5: インストーラーの確認

`installer_output/将棋ゲーム_Setup_v1.0.0.exe` が生成されます。

---

## 配布パッケージの作成

### 方法1: インストーラー配布（推奨）

**メリット:**
- ユーザーが簡単にインストールできる
- スタートメニューとデスクトップにショートカット作成
- アンインストール機能付き

**配布ファイル:**
- `将棋ゲーム_Setup_v1.0.0.exe` （約10-20MB）

### 方法2: ZIP配布（シンプル）

**メリット:**
- インストール不要
- ポータブル版として使用可能

**手順:**
1. `dist/将棋ゲーム.exe` を取得
2. `README.md` と一緒にZIPに圧縮
3. `将棋ゲーム_v1.0.0_portable.zip` として配布

**フォルダ構成例:**
```
将棋ゲーム_v1.0.0_portable/
├── 将棋ゲーム.exe
├── README.md
└── 使い方.txt
```

### 方法3: ディレクトリ版（軽量起動）

onefile版が起動が遅い場合はディレクトリ版を使用：

**手順:**
1. `--onefile` なしでビルド
2. `dist/将棋ゲーム/` フォルダ全体をZIPに圧縮

---

## エンドユーザー向けインストール手順

### インストーラー版の場合

#### インストール

1. `将棋ゲーム_Setup_v1.0.0.exe` をダブルクリック
2. セットアップウィザードに従ってインストール
3. 「次へ」をクリックして進める
4. インストール先を選択（デフォルトでOK）
5. 「デスクトップにショートカットを作成」にチェック
6. 「インストール」をクリック

#### 起動

- デスクトップの「将棋ゲーム」アイコンをダブルクリック
- または、スタートメニューから「将棋ゲーム」を検索して起動

#### アンインストール

1. Windowsの「設定」を開く
2. 「アプリ」→「インストールされているアプリ」
3. 「将棋ゲーム」を選択して「アンインストール」

### ZIP版（ポータブル版）の場合

#### インストール

1. ZIPファイルを解凍
2. 好きな場所に配置（例：デスクトップ、ドキュメントフォルダなど）

#### 起動

- `将棋ゲーム.exe` をダブルクリック

#### アンインストール

- フォルダごと削除

---

## よくある質問（FAQ）

### Q: Windows Defenderに警告される

**A:** 署名されていない実行ファイルのため警告が出ます。以下の手順で実行できます：
1. 「詳細情報」をクリック
2. 「実行」をクリック

### Q: 起動に時間がかかる

**A:** onefile版は初回起動時に一時展開されるため時間がかかります。
- ディレクトリ版を使用するか
- インストーラー版を使用してください

### Q: セーブデータの保存場所は？

**A:** `C:\Users\[ユーザー名]\.shogi_game\saves\` に保存されます

### Q: アプリケーションアイコンを変更したい

**A:** 
1. ICO形式のアイコンファイルを準備
2. `assets/icon.ico` として保存
3. `.spec` ファイルで `icon='assets/icon.ico'` を指定
4. 再ビルド

---

## チェックリスト

### ビルド前
- [ ] すべての画像ファイルが `assets/` にある
- [ ] `data/tsume_problems.json` が準備されている
- [ ] 依存パッケージがインストールされている
- [ ] ローカル環境で正常に動作する

### ビルド時
- [ ] PyInstallerでEXEが生成される
- [ ] EXEが単体で起動する
- [ ] 画像が正しく表示される
- [ ] セーブ機能が動作する

### 配布前
- [ ] 別のPCでEXEが動作するか確認
- [ ] Pythonがインストールされていない環境でテスト
- [ ] README等のドキュメントを同梱
- [ ] バージョン番号を確認

---

## サポート

問題が発生した場合は、以下の情報と共にお問い合わせください：
- Windowsのバージョン
- エラーメッセージ（あれば）
- 実行した手順

---

## 更新履歴

- v1.0.0 (2026-04-27): 初回リリース
