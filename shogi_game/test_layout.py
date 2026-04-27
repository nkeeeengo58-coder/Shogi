"""
駒画像のサイズとレイアウトの検証スクリプト
"""
import os
from PIL import Image, ImageDraw


BOARD_PADDING = 40
BOARD_IMAGE_WIDTH = 1306
BOARD_IMAGE_HEIGHT = 1204
BOARD_RENDER_WIDTH = 540
BOARD_GRID_LEFT = 133
BOARD_GRID_TOP = 58
BOARD_GRID_RIGHT = 1141
BOARD_GRID_BOTTOM = 1142


def get_layout_metrics():
    """盤面画像から実際のマス配置情報を計算"""
    board_width = BOARD_RENDER_WIDTH
    board_height = round(BOARD_IMAGE_HEIGHT * board_width / BOARD_IMAGE_WIDTH)
    scale_x = board_width / BOARD_IMAGE_WIDTH
    scale_y = board_height / BOARD_IMAGE_HEIGHT

    grid_left = BOARD_PADDING + BOARD_GRID_LEFT * scale_x
    grid_top = BOARD_PADDING + BOARD_GRID_TOP * scale_y
    grid_right = BOARD_PADDING + BOARD_GRID_RIGHT * scale_x
    grid_bottom = BOARD_PADDING + BOARD_GRID_BOTTOM * scale_y
    cell_width = (grid_right - grid_left) / 9
    cell_height = (grid_bottom - grid_top) / 9
    piece_size = max(24, int(min(cell_width, cell_height)) - 6)

    return {
        'board_width': board_width,
        'board_height': board_height,
        'grid_left': grid_left,
        'grid_top': grid_top,
        'grid_right': grid_right,
        'grid_bottom': grid_bottom,
        'cell_width': cell_width,
        'cell_height': cell_height,
        'piece_size': piece_size,
    }


def get_cell_rect(metrics, row, col):
    """マスの矩形を返す"""
    x1 = metrics['grid_left'] + col * metrics['cell_width']
    y1 = metrics['grid_top'] + row * metrics['cell_height']
    x2 = x1 + metrics['cell_width']
    y2 = y1 + metrics['cell_height']
    return x1, y1, x2, y2

def create_test_layout():
    """盤面のレイアウトをテスト画像として生成"""
    metrics = get_layout_metrics()

    canvas_width = metrics['board_width'] + BOARD_PADDING * 2
    canvas_height = metrics['board_height'] + BOARD_PADDING * 2

    board_path = os.path.join('assets', 'board', '盤面_雅.png')
    if not os.path.exists(board_path):
        print(f"✗ 盤面画像が見つかりません: {board_path}")
        return

    board_img = Image.open(board_path)
    board_img_resized = board_img.resize(
        (metrics['board_width'], metrics['board_height']),
        Image.Resampling.LANCZOS,
    )

    img = Image.new('RGB', (canvas_width, canvas_height), '#f5deb3')
    img.paste(board_img_resized, (BOARD_PADDING, BOARD_PADDING))
    draw = ImageDraw.Draw(img)
    
    # サンプルの駒画像を配置（実際の駒画像があればそれを使用）
    piece_path = os.path.join('assets', 'pieces', '駒_歩兵.png')
    
    if os.path.exists(piece_path):
        piece_img = Image.open(piece_path)
        piece_size = metrics['piece_size']
        piece_img_resized = piece_img.resize((piece_size, piece_size), Image.Resampling.LANCZOS)
        
        # いくつかのマスに駒を配置してテスト
        test_positions = [
            (0, 0), (0, 8),  # 上の角
            (4, 4),          # 中央
            (8, 0), (8, 8)   # 下の角
        ]
        
        for row, col in test_positions:
            x1, y1, x2, y2 = get_cell_rect(metrics, row, col)
            x_center = (x1 + x2) / 2
            y_center = (y1 + y2) / 2
            x_img = int(round(x_center - piece_size / 2))
            y_img = int(round(y_center - piece_size / 2))
            
            # 駒画像を貼り付け
            img.paste(piece_img_resized, (x_img, y_img), piece_img_resized if piece_img_resized.mode == 'RGBA' else None)
            
            # マスの範囲を赤枠で示す（デバッグ用）
            draw.rectangle(
                [x1, y1, x2, y2],
                outline='red',
                width=2
            )
    
    # 情報を描画
    info_text = [
        f"cell_width: {metrics['cell_width']:.2f}px",
        f"cell_height: {metrics['cell_height']:.2f}px",
        f"駒画像サイズ: {piece_size}x{piece_size}px",
        f"横余白: {(metrics['cell_width'] - piece_size) / 2:.2f}px",
        f"縦余白: {(metrics['cell_height'] - piece_size) / 2:.2f}px",
        "",
        "赤枠: マスの範囲",
        "駒画像が赤枠内に収まっていればOK"
    ]
    
    y_text = 10
    for text in info_text:
        draw.text((10, y_text), text, fill='black')
        y_text += 20
    
    # 画像を保存
    output_path = 'test_layout.png'
    img.save(output_path)
    print(f"✓ レイアウトテスト画像を生成しました: {output_path}")
    
    # 分析結果を出力
    print(f"\n=== サイズ分析 ===")
    print(f"マスのサイズ: {metrics['cell_width']:.2f}x{metrics['cell_height']:.2f}px")
    print(f"駒画像のサイズ: {piece_size}x{piece_size}px")
    print(f"横余白（各辺）: {(metrics['cell_width'] - piece_size) / 2:.2f}px")
    print(f"縦余白（各辺）: {(metrics['cell_height'] - piece_size) / 2:.2f}px")
    
    if piece_size <= metrics['cell_width'] and piece_size <= metrics['cell_height']:
        print(f"✓ 駒画像はマスに収まります")
        余白率 = ((metrics['cell_width'] - piece_size) / metrics['cell_width']) * 100
        print(f"  横方向の余白率: {余白率:.1f}%")
        if 余白率 < 5:
            print(f"  ⚠️ 余白が少なすぎる可能性があります")
        elif 余白率 > 30:
            print(f"  ⚠️ 駒が小さすぎる可能性があります")
        else:
            print(f"  ✓ 適切なサイズです")
    else:
        print(f"✗ 駒画像がマスからはみ出します！")
        はみ出し_x = max(0, piece_size - metrics['cell_width'])
        はみ出し_y = max(0, piece_size - metrics['cell_height'])
        print(f"  横はみ出し量: {はみ出し_x:.2f}px")
        print(f"  縦はみ出し量: {はみ出し_y:.2f}px")
    
    # 実際の駒画像のサイズを確認
    if os.path.exists(piece_path):
        original_img = Image.open(piece_path)
        print(f"\n元画像のサイズ: {original_img.size}")
        print(f"リサイズ後: {piece_size}x{piece_size}")
        縮小率 = (piece_size / original_img.width) * 100
        print(f"縮小率: {縮小率:.2f}%")

def check_all_piece_sizes():
    """すべての駒画像のサイズを確認"""
    print("\n=== 駒画像ファイルの確認 ===")
    
    pieces_dir = os.path.join('assets', 'pieces')
    
    if not os.path.exists(pieces_dir):
        print(f"✗ ディレクトリが見つかりません: {pieces_dir}")
        return
    
    piece_files = [f for f in os.listdir(pieces_dir) if f.endswith('.png')]
    
    for filename in sorted(piece_files):
        path = os.path.join(pieces_dir, filename)
        try:
            img = Image.open(path)
            width, height = img.size
            
            # 正方形かどうか
            if width == height:
                shape = "正方形"
            else:
                aspect = width / height
                if aspect > 1:
                    shape = f"横長 ({aspect:.2f}:1)"
                else:
                    shape = f"縦長 (1:{1/aspect:.2f})"
            
            print(f"  {filename}: {width}x{height} ({shape})")
            
            # 警告
            if width != height:
                print(f"    ⚠️ 正方形ではありません。リサイズ時に歪む可能性があります")
                
        except Exception as e:
            print(f"  ✗ {filename}: エラー - {e}")

if __name__ == "__main__":
    print("駒画像サイズとレイアウトの検証\n")
    create_test_layout()
    check_all_piece_sizes()
