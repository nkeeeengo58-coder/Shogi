# Shogi - Python将棋ゲーム

PC上でオフラインでも操作できる将棋ゲームです。

## 特徴

- 🎮 **通常将棋モード**: 4段階の難易度でCPUと対局
- 🧩 **詰将棋モード**: 1手詰めから7手詰め以上まで対応
- 🖼️ **美しい画像表示**: 高品質な盤面と駒の画像
- 💾 **保存機能**: ゲームを保存して後で再開可能
- 🎨 **カスタマイズ**: 盤や駒の見た目を変更可能

## 📸 画像について

### 現在実装済み
- ✅ 盤面画像（雅デザイン）
- ✅ 駒画像15種類（基本駒9種 + 成駒6種）
  - 基本駒: 歩、香、桂、銀、金、角、飛、玉、王
  - 成駒: と金、成香、成桂、成銀、龍馬、竜王
- ✅ アプリケーションアイコン
- ✅ 画像の自動リサイズと回転機能

## クイックスタート

### 開発環境で実行

```bash
cd shogi_game
pip install -r requirements.txt
python main.py
```

### 配布用EXEを作成（Pythonなし環境向け）

```bash
cd shogi_game

# 依存ライブラリとPyInstallerをインストール
pip install -r requirements.txt
pip install pyinstaller

# ビルドスクリプトを実行
./build.sh    # Linux/Mac
build.bat     # Windows

# dist/将棋ゲーム.exe が生成されます
```

生成されたEXEファイルは、**Pythonがインストールされていない環境でも動作します**。

詳細は [shogi_game/Docs/BUILD_DISTRIBUTION.md](shogi_game/Docs/BUILD_DISTRIBUTION.md) をご覧ください。

## 技術仕様

- **言語**: Python 3.12+
- **GUI**: Tkinter
- **画像処理**: Pillow (PIL)
- **データ形式**: JSON

## プロジェクト構成

```
Shogi/
└── shogi_game/          # メインプロジェクト
    ├── main.py          # エントリーポイント
    ├── app.py           # アプリケーション
    ├── game/            # ゲームロジック
    ├── ui/              # UI（画像対応済み）
    ├── assets/          # 画像リソース
    │   ├── board/       # 盤面画像
    │   └── pieces/      # 駒画像
    ├── data/            # 詰将棋問題
    └── saves/           # セーブデータ
```

## ライセンス

このプロジェクトは個人利用を目的としています。
