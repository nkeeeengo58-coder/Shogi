"""
アイコン画像をICO形式に変換するスクリプト
"""
from PIL import Image
import os

def convert_png_to_ico():
    """PNG画像をICO形式に変換"""
    png_path = os.path.join('assets', 'icons', '将棋ゲームアイコン.png')
    ico_path = os.path.join('assets', 'icons', 'shogi_icon.ico')
    
    if not os.path.exists(png_path):
        print(f"✗ PNG画像が見つかりません: {png_path}")
        return False
    
    try:
        # PNG画像を開く
        img = Image.open(png_path)
        
        # ICO形式で保存（複数サイズを含める）
        icon_sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
        img.save(ico_path, format='ICO', sizes=icon_sizes)
        
        print(f"✓ ICOファイルを作成しました: {ico_path}")
        print(f"  サイズ: {icon_sizes}")
        return True
        
    except Exception as e:
        print(f"✗ 変換エラー: {e}")
        return False

if __name__ == "__main__":
    print("PNG -> ICO 変換\n")
    convert_png_to_ico()
