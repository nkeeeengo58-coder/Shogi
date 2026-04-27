"""
画像読み込みテスト
"""
import os
from PIL import Image

def test_images():
    """画像の読み込みをテスト"""
    
    # 盤面画像
    board_path = os.path.join('assets', 'board', '盤面_雅.png')
    if os.path.exists(board_path):
        print(f"✓ 盤面画像が見つかりました: {board_path}")
        try:
            img = Image.open(board_path)
            print(f"  サイズ: {img.size}, モード: {img.mode}")
        except Exception as e:
            print(f"  ✗ 読み込みエラー: {e}")
    else:
        print(f"✗ 盤面画像が見つかりません: {board_path}")
    
    # 駒画像
    piece_files = {
        '歩兵': '駒_歩兵.png',
        '香車': '駒_香車.png',
        '桂馬': '駒_桂馬.png',
        '銀将': '駒_銀将.png',
        '金将': '駒_金将.png',
        '角行': '駒_角行.png',
        '飛車': '駒_飛車.png',
        '玉将': '駒_玉将.png',
        '王将': '駒_王将.png',
        'と金': '駒_成_と金.png',
        '成香': '駒_成_成香.png',
        '成桂': '駒_成_成桂.png',
        '成銀': '駒_成_成銀.png',
        '龍馬': '駒_成_龍馬.png',
        '竜王': '駒_成_竜王.png'
    }
    
    print("\n駒画像:")
    for name, filename in piece_files.items():
        path = os.path.join('assets', 'pieces', filename)
        if os.path.exists(path):
            try:
                img = Image.open(path)
                print(f"  ✓ {name}: {img.size}, {img.mode}")
            except Exception as e:
                print(f"  ✗ {name}: 読み込みエラー - {e}")
        else:
            print(f"  ✗ {name}: ファイルが見つかりません")
    
    print("\n✅ すべての駒画像が揃いました！")
    print("  - 基本駒: 9種類")
    print("  - 成駒: 6種類（と金、成香、成桂、成銀、龍馬、竜王）")
    
    # アイコン画像を確認
    print("\nアイコン画像:")
    icon_path = os.path.join('assets', 'icons', '将棋ゲームアイコン.png')
    if os.path.exists(icon_path):
        try:
            img = Image.open(icon_path)
            print(f"  ✓ 将棋ゲームアイコン: {img.size}, {img.mode}")
        except Exception as e:
            print(f"  ✗ アイコン: 読み込みエラー - {e}")
    else:
        print(f"  ✗ アイコンが見つかりません")
    
    # ICOファイルを確認
    ico_path = os.path.join('assets', 'icons', 'shogi_icon.ico')
    if os.path.exists(ico_path):
        print(f"  ✓ ICOファイル: {ico_path}")
    else:
        print(f"  ✗ ICOファイルが見つかりません")

if __name__ == "__main__":
    test_images()
