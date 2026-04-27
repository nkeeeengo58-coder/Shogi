# 将棋ゲーム
通常将棋と詰将棋の両方を楽しめます。

## 特徴

- **通常将棋モード**: CPUと対局できます（4段階の難易度）
- **詰将棋モード**: 1手詰めから7手詰め以上まで対応
- **保存機能**: ゲームを保存して後で再開できます
- **UIカスタマイズ**: 盤や駒の見た目を変更できます

## 動作環境

- Python 3.6以上
- Tkinter（Python標準ライブラリ）

## インストール

```bash
# リポジトリをクローン
git clone <repository-url>
cd Shogi/shogi_game

# 実行
python main.py
```

## ディレクトリ構成

```
shogi_game/
├── main.py              # エントリーポイント
├── app.py               # アプリケーションメインクラス
├── game/                # ゲームロジック
│   ├── board.py         # 盤面クラス
│   ├── piece.py         # 駒クラス
│   ├── move.py          # 手クラス
│   ├── rules.py         # ルール判定
│   ├── engine.py        # CPU思考エンジン
│   ├── tsume.py         # 詰将棋モジュール
│   └── save_load.py     # 保存・読み込み
├── ui/                  # UIモジュール
│   ├── screens.py       # 各種画面
│   ├── board_view.py    # 盤面表示
│   ├── menu.py          # メニューバー
│   └── customize.py     # UIカスタマイズ
├── assets/              # 画像・音声ファイル
│   ├── board/           # 盤の画像
│   ├── pieces/          # 駒の画像
│   └── sounds/          # 効果音
├── data/                # データファイル
│   └── tsume_problems.json  # 詰将棋問題
└── saves/               # 保存データ
```

## 遊び方

### 起動フロー

1. ソフトを起動
2. モード選択（通常将棋 or 詰将棋）
3. 難易度選択（初級/中級/上級/超上級）
4. 確認画面で「はい」を選択してゲーム開始

### 操作方法

#### 駒を動かす
1. 動かしたい駒をクリック
2. 移動先のマスをクリック
3. 成れる場合はダイアログで選択

#### 持ち駒を打つ
1. 持ち駒エリアの駒をクリック
2. 打ちたいマスをクリック

### ゲームモード

#### 通常将棋モード
- 人 vs CPU
- 持ち駒あり、成りあり
- 二歩禁止、王手放置禁止、打ち歩詰め禁止
- 行き所のない駒打ち禁止
- 千日手は引き分け

#### 詰将棋モード
- 難易度別の問題を出題
- 初級：1手詰め
- 中級：3手詰め
- 上級：5手詰め
- 超上級：7手詰め以上

### 難易度

#### 通常将棋
- **初級**: ランダム寄りの選択（明らかな悪手は避ける）
- **中級**: 1〜2手読み（駒得、成り、王の安全を評価）
- **上級**: 3〜4手読み（ミニマックス + αβ枝刈り）
- **超上級**: 4手以上の探索（詳細な局面評価）

#### 詰将棋
- **初級**: 1手詰め
- **中級**: 3手詰め
- **上級**: 5手詰め
- **超上級**: 7手詰め以上

## 保存・読み込み

- メニューの「ファイル」→「保存」でゲームを保存
- メニューの「ファイル」→「読み込み」で保存したゲームを再開
- 保存データは`~/.shogi_game/saves/`に保存されます

## UIカスタマイズ

メニューの「設定」→「UIカスタマイズ」から以下を変更できます：

- 盤のテーマ
- 駒画像セット
- 文字サイズ
- ハイライト透明度
- 音声のON/OFF

## 画像ファイルについて

### ✅ 完全実装：画像表示機能

盤面と駒の画像表示機能が完全に実装されました！

#### 現在の画像ファイル

**盤面画像:**
- ✅ 盤面_雅.png (1306x1204) - `assets/board/`

**駒画像（すべて1254x1254）:** - `assets/pieces/`

基本駒（9種類）:
- ✅ 駒_歩兵.png
- ✅ 駒_香車.png
- ✅ 駒_桂馬.png
- ✅ 駒_銀将.png
- ✅ 駒_金将.png
- ✅ 駒_角行.png
- ✅ 駒_飛車.png
- ✅ 駒_玉将.png
- ✅ 駒_王将.png

成駒（6種類）:
- ✅ 駒_成_と金.png（成歩）
- ✅ 駒_成_成香.png（成香）
- ✅ 駒_成_成桂.png（成桂）
- ✅ 駒_成_成銀.png（成銀）
- ✅ 駒_成_龍馬.png（成角）
- ✅ 駒_成_竜王.png（成飛車）

**アイコン画像:** - `assets/icons/`
- ✅ 将棋ゲームアイコン.png (512x512)
- ✅ shogi_icon.ico（Windows用アイコン、複数サイズ対応）

#### 画像のテスト

```bash
python test_images.py
```

このスクリプトで、すべての画像が正しく読み込めるかテストできます。

#### 画像の仕様

- 盤面画像は自動的に9マス×9マスに合わせてリサイズされます
- 駒画像は盤面のマスサイズに合わせてリサイズされます
- 後手の駒は自動的に180度回転されます
- 持ち駒は小さめに表示されます

独自の画像を使用する場合は、以下のディレクトリに配置してください：

- `assets/board/`: 盤の画像
- `assets/pieces/`: 駒の画像（各駒セット用にサブディレクトリ作成可能）
- `assets/sounds/`: 効果音ファイル

## 詰将棋問題の追加

`data/tsume_problems.json`に問題を追加できます。
JSON形式で盤面データと正解手順を記述してください。

## 配布（Pythonがない環境向け）

### 📦 クイックビルド

**Windows:**
```cmd
build.bat
```

**Linux/Mac:**
```bash
chmod +x build.sh
./build.sh
```

これらのスクリプトを実行すると、**Pythonがインストールされていない環境でも動作する実行ファイル**（約15-20MB）が `dist/将棋ゲーム.exe` として生成されます。

#### CLI実行例:

```bash
# プロジェクトディレクトリに移動
cd /path/to/Shogi/shogi_game

# 依存ライブラリをインストール（初回のみ）
pip install -r requirements.txt

# PyInstallerをインストール（初回のみ）
pip install pyinstaller

# ビルドスクリプトを実行
./build.sh    # Linux/Mac
# または
build.bat     # Windows

# 実行ファイルの生成を確認
ls -lh dist/将棋ゲーム.exe  # Linux/Mac
dir dist\将棋ゲーム.exe     # Windows

# 動作確認
cd dist
./将棋ゲーム.exe
```

### 📚 詳細な配布手順

以下のドキュメントを参照してください：

- **[配布ビルド手順](Docs/BUILD_DISTRIBUTION.md)** - 開発者向け：PyInstallerとInno Setupを使った配布パッケージの作成方法
- **[使い方ガイド](Docs/USER_GUIDE.md)** - エンドユーザー向け：インストールと使い方

### 📁 配布形態

1. **インストーラー版（推奨）**
   - `将棋ゲーム_Setup_v1.0.0.exe`
   - 自動インストール、アンインストール機能付き
   - デスクトップとスタートメニューにショートカット作成

2. **ZIP版（ポータブル）**
   - `将棋ゲーム_v1.0.0_portable.zip`
   - インストール不要、展開するだけで使用可能
   - USBメモリなどで持ち運び可能

### 🛠️ ビルドファイル

- `shogi_game.spec` - PyInstaller設定ファイル（アイコン設定済み）
- `shogi_installer.iss` - Inno Setup設定ファイル
- `build.bat` - Windows用自動ビルドスクリプト
- `build.sh` - Linux/Mac用自動ビルドスクリプト
- `convert_icon.py` - PNG画像からICOファイルを生成するスクリプト

### 🖼️ アイコンとアセット

すべての画像ファイルが揃っています：

- **盤面画像**: 1枚（雅デザイン）
- **駒画像**: 15種類（基本駒9種 + 成駒6種）
- **アイコン**: PNG（512x512）とICO（複数サイズ）形式

アイコンは実行ファイルに自動的に埋め込まれ、タイトルバーやタスクバーに表示されます。

## ライセンス

このソフトウェアは個人使用を目的として作成されています。

## 開発者向け

### テスト

各モジュールは独立しており、単体でテスト可能です。

#### 機能テスト:

```bash
# すべての画像が正しく読み込めるかテスト
python test_images.py

# すべての駒の表示テスト
python test_all_pieces.py

# レイアウトのテスト
python test_layout.py

# 実際の盤面レイアウトのテスト
python test_realistic_layout.py
```

#### コードテスト:

```python
# 盤面のテスト
from game.board import Board
board = Board()
board.initialize_normal_game()

# ルールのテスト
from game.rules import Rules
moves = Rules.get_piece_moves(board, 6, 4)

# CPU思考のテスト
from game.engine import Engine
engine = Engine('medium')
move = engine.get_best_move(board)
```

### 拡張

- `game/engine.py`: CPU思考の改善
- `data/tsume_problems.json`: 詰将棋問題の追加
- `ui/board_view.py`: 盤面表示のカスタマイズ
- `assets/`: 画像・音声の追加

## トラブルシューティング

### Tkinterが見つからない

```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# macOS (Homebrewの場合)
brew install python-tk
```

### 保存データが読み込めない

`~/.shogi_game/saves/`内のJSONファイルを確認してください。
破損している場合は削除して新規ゲームを開始してください。

## 今後の改善案

- [ ] 棋譜の保存・再生機能
- [ ] 入玉・持将棋の実装
- [ ] オンライン対戦機能
- [ ] より多くの詰将棋問題
- [ ] 定跡データベース
- [ ] 画像・音声ファイルの同梱

## お問い合わせ

バグや要望がありましたら、GitHubのIssuesまでお願いします。
