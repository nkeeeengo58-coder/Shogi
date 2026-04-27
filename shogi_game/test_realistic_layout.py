"""
実際の盤面画像と駒画像を組み合わせたレイアウトテスト
"""
import os
from PIL import Image, ImageDraw

def create_realistic_layout():
    """実際の盤面画像と駒画像を使ったテスト"""
    
    # 設定
    CELL_SIZE = 60
    BOARD_PADDING = 40
    piece_size = CELL_SIZE - 8  # 52
    
    # 盤面画像を読み込み
    board_path = os.path.join('assets', 'board', '盤面_雅.png')
    
    if not os.path.exists(board_path):
        print(f"✗ 盤面画像が見つかりません: {board_path}")
        return
    
    # 元の盤面画像を開く
    board_img = Image.open(board_path)
    print(f"元の盤面画像サイズ: {board_img.size}")
    
    # 9マス×9マスにリサイズ
    board_size = CELL_SIZE * 9
    board_img_resized = board_img.resize((board_size, board_size), Image.Resampling.LANCZOS)
    print(f"リサイズ後: {board_img_resized.size}")
    
    # キャンバスを作成
    canvas_width = board_size + BOARD_PADDING * 2
    canvas_height = board_size + BOARD_PADDING * 2
    canvas = Image.new('RGB', (canvas_width, canvas_height), '#f5deb3')
    
    # 盤面画像を貼り付け
    canvas.paste(board_img_resized, (BOARD_PADDING, BOARD_PADDING))
    
    # 駒画像をいくつか配置
    piece_files = [
        ('駒_玉将.png', 4, 4, 'black'),  # 中央に先手玉
        ('駒_王将.png', 0, 4, 'white'),  # 上部に後手王
        ('駒_飛車.png', 7, 1, 'black'),  # 先手飛車
        ('駒_角行.png', 7, 7, 'black'),  # 先手角
        ('駒_成_竜王.png', 2, 4, 'white'),  # 後手龍
        ('駒_成_龍馬.png', 6, 4, 'black'),  # 先手馬
        ('駒_金将.png', 8, 3, 'black'),   # 先手金
        ('駒_金将.png', 8, 5, 'black'),   # 先手金
        ('駒_銀将.png', 8, 2, 'black'),   # 先手銀
        ('駒_銀将.png', 8, 6, 'black'),   # 先手銀
        ('駒_桂馬.png', 8, 1, 'black'),   # 先手桂
        ('駒_桂馬.png', 8, 7, 'black'),   # 先手桂
        ('駒_香車.png', 8, 0, 'black'),   # 先手香
        ('駒_香車.png', 8, 8, 'black'),   # 先手香
        ('駒_歩兵.png', 6, 0, 'black'),   # 先手歩
        ('駒_歩兵.png', 6, 2, 'black'),
        ('駒_歩兵.png', 6, 6, 'black'),
        ('駒_歩兵.png', 6, 8, 'black'),
    ]
    
    for filename, row, col, owner in piece_files:
        piece_path = os.path.join('assets', 'pieces', filename)
        if os.path.exists(piece_path):
            piece_img = Image.open(piece_path)
            piece_img_resized = piece_img.resize((piece_size, piece_size), Image.Resampling.LANCZOS)
            
            # 後手の駒は180度回転
            if owner == 'white':
                piece_img_resized = piece_img_resized.rotate(180)
            
            # マスの中心座標
            x_center = BOARD_PADDING + col * CELL_SIZE + CELL_SIZE // 2
            y_center = BOARD_PADDING + row * CELL_SIZE + CELL_SIZE // 2
            
            # 画像の左上座標
            x_img = x_center - piece_size // 2
            y_img = y_center - piece_size // 2
            
            # 駒画像を貼り付け
            if piece_img_resized.mode == 'RGBA':
                canvas.paste(piece_img_resized, (x_img, y_img), piece_img_resized)
            else:
                canvas.paste(piece_img_resized, (x_img, y_img))
    
    # デバッグ用：いくつかのマスに枠線を描画
    draw = ImageDraw.Draw(canvas)
    debug_positions = [(4, 4), (0, 4), (7, 1), (7, 7)]
    for row, col in debug_positions:
        x = BOARD_PADDING + col * CELL_SIZE
        y = BOARD_PADDING + row * CELL_SIZE
        draw.rectangle(
            [x, y, x + CELL_SIZE, y + CELL_SIZE],
            outline='red',
            width=2
        )
    
    # 情報テキスト
    info_text = [
        "実際の盤面と駒の組み合わせテスト",
        "赤枠: マスの範囲（デバッグ用）",
        "駒が赤枠内に収まっていればOK"
    ]
    
    y_text = 5
    for text in info_text:
        draw.text((5, y_text), text, fill='black')
        y_text += 15
    
    # 保存
    output_path = 'test_realistic_layout.png'
    canvas.save(output_path)
    print(f"\n✓ 実際の盤面レイアウトテスト画像を生成しました: {output_path}")
    
    print(f"\n=== 確認事項 ===")
    print("1. 駒がマス（赤枠）内に収まっているか")
    print("2. 駒が盤面の罫線からはみ出していないか")
    print("3. 駒同士が重なっていないか")
    print("4. 後手の駒が正しく180度回転しているか")
    print("5. 駒の視認性は十分か")

if __name__ == "__main__":
    print("実際の盤面画像と駒画像のレイアウトテスト\n")
    create_realistic_layout()
