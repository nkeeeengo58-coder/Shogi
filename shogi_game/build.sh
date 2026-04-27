#!/bin/bash
# 将棋ゲーム ビルドスクリプト (Linux/Mac)
# このスクリプトは PyInstaller でバイナリを作成します

set -e

echo "========================================"
echo "将棋ゲーム ビルドスクリプト"
echo "========================================"
echo ""

# 必要なパッケージの確認
echo "[1/5] 必要なパッケージを確認中..."
if ! python3 -c "import PyInstaller" 2>/dev/null; then
    echo "PyInstaller がインストールされていません。"
    read -p "インストールしますか？ [Y/n] " install_pyinstaller
    if [[ $install_pyinstaller == "Y" || $install_pyinstaller == "y" ]]; then
        pip3 install pyinstaller
    else
        echo "ビルドを中止しました。"
        exit 1
    fi
fi

if ! python3 -c "import PIL" 2>/dev/null; then
    echo "Pillow がインストールされていません。"
    read -p "インストールしますか？ [Y/n] " install_pillow
    if [[ $install_pillow == "Y" || $install_pillow == "y" ]]; then
        pip3 install Pillow
    else
        echo "ビルドを中止しました。"
        exit 1
    fi
fi

echo "必要なパッケージが揃っています。"
echo ""

# アイコンファイルの確認と生成
echo "[2/6] アイコンファイルを確認中..."
if [ ! -f "assets/icons/shogi_icon.ico" ]; then
    echo "アイコンファイルが見つかりません。"
    echo "PNGファイルから生成します..."
    if [ -f "assets/icons/将棋ゲームアイコン.png" ]; then
        python3 convert_icon.py
        if [ $? -ne 0 ]; then
            echo "警告: アイコンの生成に失敗しました。"
            echo "ビルドは続行しますが、デフォルトアイコンになります。"
        else
            echo "アイコンの生成に成功しました。"
        fi
    else
        echo "警告: PNG画像も見つかりません。"
        echo "ビルドは続行しますが、デフォルトアイコンになります。"
    fi
else
    echo "アイコンファイルが見つかりました: assets/icons/shogi_icon.ico"
fi
echo ""

# 古いビルドを削除
echo "[3/6] 古いビルドファイルを削除中..."
rm -rf build dist
echo "削除完了。"
echo ""

# ビルド実行
echo "[4/6] PyInstaller でビルド中..."
echo "これには数分かかる場合があります。"
echo ""
pyinstaller shogi_game.spec

echo ""
echo "ビルド完了！"
echo ""

# ファイルの確認
echo "[5/6] 生成されたファイルを確認中..."
if [ -f "dist/将棋ゲーム" ]; then
    echo "将棋ゲーム が生成されました。"
    ls -lh "dist/将棋ゲーム"
else
    echo "エラー: 将棋ゲーム が見つかりません。"
    exit 1
fi
echo ""

# 配布用パッケージの作成
echo "[6/6] 配布用パッケージを作成中..."
VERSION="1.0.0"
OS_NAME=$(uname -s)
PACKAGE_NAME="将棋ゲーム_v${VERSION}_${OS_NAME}"

rm -rf "${PACKAGE_NAME}"
mkdir -p "${PACKAGE_NAME}"

cp "dist/将棋ゲーム" "${PACKAGE_NAME}/"
cp "README.md" "${PACKAGE_NAME}/"
cp "Docs/USER_GUIDE.md" "${PACKAGE_NAME}/使い方.md"

# 実行権限を付与
chmod +x "${PACKAGE_NAME}/将棋ゲーム"

echo ""
echo "========================================"
echo "ビルドが完了しました！"
echo "========================================"
echo ""
echo "生成されたファイル:"
echo "  - dist/将棋ゲーム"
echo "  - ${PACKAGE_NAME}/"
echo ""
echo "次のステップ:"
echo "  1. dist/将棋ゲーム を実行してテスト"
echo "  2. ${PACKAGE_NAME} フォルダをtar.gzで圧縮して配布"
echo ""
echo "実行方法:"
echo "  ./dist/将棋ゲーム"
echo ""
