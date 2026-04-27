"""
すべての駒（成駒含む）の表示テスト
"""
import os
from PIL import Image, ImageDraw, ImageFont

def create_all_pieces_test():
    """すべての駒を並べて表示するテスト画像を生成"""
    
    CELL_SIZE = 60
    piece_size = CELL_SIZE - 8  # 52
    
    # 駒の種類（表示順）
    pieces = [
        ('駒_歩兵.png', '歩'),
        ('駒_香車.png', '香'),
        ('駒_桂馬.png', '桂'),
        ('駒_銀将.png', '銀'),
        ('駒_金将.png', '金'),
        ('駒_角行.png', '角'),
        ('駒_飛車.png', '飛'),
        ('駒_玉将.png', '玉'),
        ('駒_王将.png', '王'),
        ('駒_成_と金.png', 'と金'),
        ('駒_成_成香.png', '成香'),
        ('駒_成_成桂.png', '成桂'),
        ('駒_成_成銀.png', '成銀'),
        ('駒_成_龍馬.png', '龍馬'),
        ('駒_成_竜王.png', '竜王'),
    ]
    
    # キャンバスサイズ（5列×3行）
    cols = 5
    rows = 3
    padding = 20
    canvas_width = cols * CELL_SIZE + padding * 2
    canvas_height = rows * CELL_SIZE + padding * 2 + 50  # タイトル用の余白
    
    # 画像を作成
    img = Image.new('RGB', (canvas_width, canvas_height), '#f5deb3')
    draw = ImageDraw.Draw(img)
    
    # タイトル
    draw.text((canvas_width // 2 - 100, 10), 
              "将棋駒一覧（全15種類）", 
              fill='black', 
              font=None)
    
    # 駒を配置
    y_offset = 50
    for i, (filename, name) in enumerate(pieces):
        row = i // cols
        col = i % cols
        
        x = padding + col * CELL_SIZE + CELL_SIZE // 2
        y = y_offset + row * CELL_SIZE + CELL_SIZE // 2
        
        # マスの枠
        x_cell = padding + col * CELL_SIZE
        y_cell = y_offset + row * CELL_SIZE
        draw.rectangle(
            [x_cell, y_cell, x_cell + CELL_SIZE, y_cell + CELL_SIZE],
            outline='#8b4513',
            width=1
        )
        
        # 駒画像を配置
        piece_path = os.path.join('assets', 'pieces', filename)
        if os.path.exists(piece_path):
            piece_img = Image.open(piece_path)
            piece_img_resized = piece_img.resize((piece_size, piece_size), Image.Resampling.LANCZOS)
            
            x_img = x - piece_size // 2
            y_img = y - piece_size // 2
            
            if piece_img_resized.mode == 'RGBA':
                img.paste(piece_img_resized, (x_img, y_img), piece_img_resized)
            else:
                img.paste(piece_img_resized, (x_img, y_img))
            
            # 駒の名前を下に表示
            draw.text((x - 10, y_cell + CELL_SIZE + 2), name, fill='black')
        else:
            # ファイルがない場合
            draw.text((x - 10, y), "?", fill='red', font=None)
    
    # 保存
    output_path = 'test_all_pieces.png'
    img.save(output_path)
    print(f"✓ すべての駒の表示テスト画像を生成しました: {output_path}")
    
    # 統計
    existing = sum(1 for filename, _ in pieces if os.path.exists(os.path.join('assets', 'pieces', filename)))
    print(f"\n統計:")
    print(f"  - 全駒数: {len(pieces)}種類")
    print(f"  - 基本駒: 9種類")
    print(f"  - 成駒: 6種類")
    print(f"  - 画像ファイル: {existing}/{len(pieces)}")
    
    if existing == len(pieces):
        print(f"\n✅ すべての駒画像が揃っています！")
    else:
        print(f"\n⚠️ {len(pieces) - existing}個の駒画像が不足しています")

if __name__ == "__main__":
    print("すべての駒の表示テスト\n")
    create_all_pieces_test()
