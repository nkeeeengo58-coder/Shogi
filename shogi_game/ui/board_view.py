"""
盤面ビュークラス
"""
import tkinter as tk
from tkinter import messagebox
from game.rules import Rules
from game.move import Move
from game.piece import Piece
import os
from PIL import Image, ImageTk

class BoardView(tk.Frame):
    """盤面表示クラス"""
    
    BOARD_PADDING = 40
    BOARD_IMAGE_WIDTH = 1306
    BOARD_IMAGE_HEIGHT = 1204
    BOARD_RENDER_WIDTH = 540
    BOARD_GRID_LEFT = 133
    BOARD_GRID_TOP = 58
    BOARD_GRID_RIGHT = 1141
    BOARD_GRID_BOTTOM = 1142
    
    def __init__(self, parent, board, config, on_move_callback):
        """
        Args:
            parent: 親ウィジェット
            board: Boardインスタンス
            config: 設定辞書
            on_move_callback: 駒が動かされた時のコールバック
        """
        super().__init__(parent)
        self.board = board
        self.config = config
        self.on_move_callback = on_move_callback
        
        # 入力可能状態（CPUの手番中は無効化）
        self.enabled = True
        
        # 選択状態
        self.selected_pos = None  # 選択中の駒の位置 (row, col)
        self.selected_piece_type = None  # 選択中の持ち駒の種類
        self.legal_moves = []  # 選択中の駒の合法手
        
        # 画像読み込み
        self.theme_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'pieces')
        self.board_theme_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'board')
        self.piece_images = {}
        self.board_photo = None
        self.board_width = self.BOARD_RENDER_WIDTH
        self.board_height = round(self.BOARD_IMAGE_HEIGHT * self.board_width / self.BOARD_IMAGE_WIDTH)
        self.scale_x = self.board_width / self.BOARD_IMAGE_WIDTH
        self.scale_y = self.board_height / self.BOARD_IMAGE_HEIGHT
        self.grid_left = self.BOARD_PADDING + self.BOARD_GRID_LEFT * self.scale_x
        self.grid_top = self.BOARD_PADDING + self.BOARD_GRID_TOP * self.scale_y
        self.grid_right = self.BOARD_PADDING + self.BOARD_GRID_RIGHT * self.scale_x
        self.grid_bottom = self.BOARD_PADDING + self.BOARD_GRID_BOTTOM * self.scale_y
        self.cell_width = (self.grid_right - self.grid_left) / 9
        self.cell_height = (self.grid_bottom - self.grid_top) / 9
        self.load_images()
        
        # キャンバスを作成
        canvas_width = self.board_width + self.BOARD_PADDING * 2 + 200  # 持ち駒エリア分を追加
        canvas_height = self.board_height + self.BOARD_PADDING * 2
        
        self.canvas = tk.Canvas(self, width=canvas_width, height=canvas_height, bg='#f5deb3')
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # クリックイベント
        self.canvas.bind('<Button-1>', self.on_click)
        
        # 描画
        self.draw()
    
    def set_board(self, board):
        """盤面を設定"""
        self.board = board
        self.selected_pos = None
        self.selected_piece_type = None
        self.legal_moves = []
    
    def set_enabled(self, enabled):
        """入力の有効/無効を設定"""
        self.enabled = enabled
        if not enabled:
            # 無効化時は選択を解除
            self.selected_pos = None
            self.selected_piece_type = None
            self.legal_moves = []
            self.draw()

    def _get_cell_rect(self, row, col):
        """指定マスの矩形を返す"""
        x1 = self.grid_left + col * self.cell_width
        y1 = self.grid_top + row * self.cell_height
        x2 = x1 + self.cell_width
        y2 = y1 + self.cell_height
        return x1, y1, x2, y2

    def _get_cell_center(self, row, col):
        """指定マスの中心座標を返す"""
        x1, y1, x2, y2 = self._get_cell_rect(row, col)
        return (x1 + x2) / 2, (y1 + y2) / 2
    
    def load_images(self):
        """画像を読み込む"""
        # 盤面画像
        board_path = os.path.join(self.board_theme_path, "盤面_雅.png")
        if os.path.exists(board_path):
            board_img = Image.open(board_path)
            board_img = board_img.resize((self.board_width, self.board_height), Image.Resampling.LANCZOS)
            self.board_photo = ImageTk.PhotoImage(board_img)
        else:
            self.board_photo = None
        
        # 駒画像のマッピング（駒種類 -> ファイル名）
        piece_files = {
            'FU': '駒_歩兵.png',
            'KY': '駒_香車.png',
            'KE': '駒_桂馬.png',
            'GI': '駒_銀将.png',
            'KI': '駒_金将.png',
            'KA': '駒_角行.png',
            'HI': '駒_飛車.png',
            'OU': '駒_玉将.png',
            'GYOKU': '駒_王将.png',
            'TO': '駒_成_と金.png',  # と金（成歩）
            'NY': '駒_成_成香.png',  # 成香
            'NK': '駒_成_成桂.png',  # 成桂
            'NG': '駒_成_成銀.png',  # 成銀
            'UM': '駒_成_龍馬.png',  # 成角（馬）
            'RY': '駒_成_竜王.png'   # 成飛（龍）
        }
        
        piece_size = max(24, int(min(self.cell_width, self.cell_height)) - 6)
        captured_piece_size = 40  # 持ち駒用のサイズ
        
        for piece_id, filename in piece_files.items():
            path = os.path.join(self.theme_path, filename)
            if os.path.exists(path):
                img_original = Image.open(path)
                
                # 通常の駒（先手用）
                img = img_original.resize((piece_size, piece_size), Image.Resampling.LANCZOS)
                self.piece_images[f'{piece_id}_black'] = ImageTk.PhotoImage(img)
                
                # 後手の駒（180度回転）
                img_rotated = img.rotate(180)
                self.piece_images[f'{piece_id}_white'] = ImageTk.PhotoImage(img_rotated)
                
                # 持ち駒用（小さめ）
                img_small = img_original.resize((captured_piece_size, captured_piece_size), Image.Resampling.LANCZOS)
                self.piece_images[f'{piece_id}_captured'] = ImageTk.PhotoImage(img_small)
            else:
                # プレースホルダー
                self.piece_images[f'{piece_id}_black'] = None
                self.piece_images[f'{piece_id}_white'] = None
                self.piece_images[f'{piece_id}_captured'] = None
    
    def draw(self):
        """盤面を描画"""
        self.canvas.delete('all')
        
        # 盤面を描画
        self._draw_board()
        
        # 駒を描画
        self._draw_pieces()
        
        # 持ち駒を描画
        self._draw_captured_pieces()
        
        # 選択中の駒があれば合法手をハイライト
        if self.legal_moves:
            self._draw_legal_moves()
        
        # 直前の手をハイライト
        if self.board.last_move:
            self._draw_last_move()
    
    def _draw_board(self):
        """盤面の枠を描画"""
        x_start = self.BOARD_PADDING
        y_start = self.BOARD_PADDING
        
        # 盤面画像を表示
        if self.board_photo:
            self.canvas.create_image(
                x_start, y_start,
                image=self.board_photo,
                anchor='nw'
            )
        else:
            # プレースホルダー（従来の描画方法）
            self.canvas.create_rectangle(
                self.grid_left, self.grid_top,
                self.grid_right,
                self.grid_bottom,
                fill='#daa520', outline='#8b4513', width=3
            )
            
            # マスの罫線
            for i in range(10):
                # 縦線
                x = self.grid_left + i * self.cell_width
                self.canvas.create_line(x, self.grid_top, x, self.grid_bottom, fill='#8b4513')
                
                # 横線
                y = self.grid_top + i * self.cell_height
                self.canvas.create_line(self.grid_left, y, self.grid_right, y, fill='#8b4513')
        
        # 座標表示
        for i in range(9):
            # 列番号（9-1）
            x, _ = self._get_cell_center(0, i)
            self.canvas.create_text(x, self.grid_top - 15, text=str(9 - i), font=("", 12))
            
            # 行番号（一-九）
            _, y = self._get_cell_center(i, 0)
            row_labels = ['一', '二', '三', '四', '五', '六', '七', '八', '九']
            self.canvas.create_text(self.grid_right + 15, y, text=row_labels[i], font=("", 12))
    
    def _draw_pieces(self):
        """駒を描画"""
        for row in range(9):
            for col in range(9):
                piece = self.board.get_piece(row, col)
                if piece:
                    self._draw_piece(row, col, piece)
        
        # 選択中の駒をハイライト
        if self.selected_pos:
            row, col = self.selected_pos
            x1, y1, x2, y2 = self._get_cell_rect(row, col)
            self.canvas.create_rectangle(
                x1 + 2, y1 + 2,
                x2 - 2, y2 - 2,
                outline='blue', width=3
            )
    
    def _draw_piece(self, row, col, piece, x_offset=0, y_offset=0):
        """1つの駒を描画"""
        x, y = self._get_cell_center(row, col)
        x += x_offset
        y += y_offset
        
        # 駒画像を取得
        image_key = f'{piece.piece_type}_{piece.owner}'
        piece_img = self.piece_images.get(image_key)
        
        if piece_img:
            # 画像で表示
            self.canvas.create_image(x, y, image=piece_img)
        else:
            # プレースホルダー（従来の描画方法）
            # 駒の背景（五角形風）
            size = 22
            points = [
                x, y - size,           # 上
                x + size, y - size//2, # 右上
                x + size, y + size,    # 右下
                x - size, y + size,    # 左下
                x - size, y - size//2  # 左上
            ]
            
            fill_color = '#f5f5dc' if piece.owner == 'black' else '#696969'
            self.canvas.create_polygon(points, fill=fill_color, outline='black', width=1)
            
            # 駒の文字
            text_color = 'black' if piece.owner == 'black' else 'white'
            
            # 後手の駒は上下逆
            if piece.owner == 'white':
                self.canvas.create_text(
                    x, y,
                    text=piece.get_name(),
                    font=("", 20, "bold"),
                    fill=text_color,
                    angle=180
                )
            else:
                self.canvas.create_text(
                    x, y,
                    text=piece.get_name(),
                    font=("", 20, "bold"),
                    fill=text_color
                )
    
    def _draw_captured_pieces(self):
        """持ち駒を描画"""
        x_base = self.BOARD_PADDING + self.board_width + 30
        
        # 先手の持ち駒（下）
        y_black = self.grid_top + self.cell_height * 7
        self.canvas.create_text(
            x_base, y_black - 30,
            text="先手の持ち駒",
            font=("", 12, "bold")
        )
        self._draw_captured_pieces_for_player('black', x_base, y_black)
        
        # 後手の持ち駒（上）
        y_white = self.grid_top + self.cell_height
        self.canvas.create_text(
            x_base, y_white - 30,
            text="後手の持ち駒",
            font=("", 12, "bold")
        )
        self._draw_captured_pieces_for_player('white', x_base, y_white)
    
    def _draw_captured_pieces_for_player(self, player, x_base, y_base):
        """指定プレイヤーの持ち駒を描画"""
        # 持ち駒を種類ごとにカウント
        piece_counts = {}
        for piece in self.board.captured_pieces[player]:
            base_type = piece.get_base_type()
            piece_counts[base_type] = piece_counts.get(base_type, 0) + 1
        
        # 描画
        y_offset = 0
        for i, (piece_type, count) in enumerate(piece_counts.items()):
            piece = Piece(piece_type, player)
            
            # 駒を描画（簡易版）
            x = x_base + 20
            y = y_base + y_offset
            
            # 選択中の持ち駒をハイライト
            if self.selected_piece_type == piece_type and player == self.board.turn:
                self.canvas.create_rectangle(
                    x - 25, y - 25,
                    x + 25, y + 25,
                    outline='blue', width=3
                )
            
            # 駒画像を取得（持ち駒用の小さい画像）
            image_key = f'{piece_type}_captured'
            piece_img = self.piece_images.get(image_key)
            
            if piece_img:
                # 画像で表示
                self.canvas.create_image(x, y, image=piece_img)
            else:
                # プレースホルダー（従来の描画方法）
                size = 18
                points = [
                    x, y - size,
                    x + size, y - size//2,
                    x + size, y + size,
                    x - size, y + size,
                    x - size, y - size//2
                ]
                self.canvas.create_polygon(points, fill='#f5f5dc', outline='black', width=1)
                
                # 駒の文字
                self.canvas.create_text(
                    x, y,
                    text=piece.get_name(),
                    font=("", 16, "bold")
                )
            
            # 枚数表示
            if count > 1:
                self.canvas.create_text(
                    x + 30, y,
                    text=f"×{count}",
                    font=("", 12)
                )
            
            y_offset += 45
    
    def _draw_legal_moves(self):
        """合法手をハイライト表示"""
        opacity = self.config.get('highlight_opacity', 0.5)
        alpha = int(255 * opacity)
        
        for move in self.legal_moves:
            row, col = move.to_pos
            x1, y1, x2, y2 = self._get_cell_rect(row, col)
            
            # 半透明の緑色でハイライト
            self.canvas.create_rectangle(
                x1 + 5, y1 + 5,
                x2 - 5, y2 - 5,
                fill='', outline='green', width=2, stipple='gray50'
            )
    
    def _draw_last_move(self):
        """直前の手をハイライト"""
        move = self.board.last_move
        if move and not move.is_drop:
            # 移動元
            from_row, from_col = move.from_pos
            x1, y1, x2, y2 = self._get_cell_rect(from_row, from_col)
            self.canvas.create_rectangle(
                x1 + 5, y1 + 5,
                x2 - 5,
                y2 - 5,
                outline='orange', width=2
            )
        
        # 移動先
        to_row, to_col = move.to_pos
        x1, y1, x2, y2 = self._get_cell_rect(to_row, to_col)
        self.canvas.create_rectangle(
            x1 + 5, y1 + 5,
            x2 - 5,
            y2 - 5,
            outline='orange', width=2
        )
    
    def on_click(self, event):
        """クリックイベント処理"""
        # CPUの手番中など、入力が無効な場合は無視
        if not self.enabled:
            return
        
        x, y = event.x, event.y
        
        # 盤面上のクリックか
        board_x_start = self.grid_left
        board_y_start = self.grid_top
        board_x_end = self.grid_right
        board_y_end = self.grid_bottom
        
        if board_x_start <= x <= board_x_end and board_y_start <= y <= board_y_end:
            col = min(8, int((x - board_x_start) // self.cell_width))
            row = min(8, int((y - board_y_start) // self.cell_height))
            self._on_board_click(row, col)
        else:
            # 持ち駒エリアのクリックか
            self._on_captured_click(x, y)
    
    def _on_board_click(self, row, col):
        """盤面クリック処理"""
        # 持ち駒を打つ場合
        if self.selected_piece_type:
            # 合法手にあるかチェック
            for move in self.legal_moves:
                if move.to_pos == (row, col):
                    self._execute_move(move)
                    self.selected_piece_type = None
                    self.legal_moves = []
                    self.draw()
                    return
            
            # 合法手でない場合はキャンセル
            self.selected_piece_type = None
            self.legal_moves = []
            self.draw()
            return
        
        # 駒を選択または移動
        if self.selected_pos:
            # 移動先として選択
            for move in self.legal_moves:
                if move.to_pos == (row, col):
                    # 成れる場合は確認
                    if move.piece.can_promote():
                        # 成る手と成らない手がある場合
                        promote_moves = [m for m in self.legal_moves if m.to_pos == (row, col) and m.is_promotion]
                        normal_moves = [m for m in self.legal_moves if m.to_pos == (row, col) and not m.is_promotion]
                        
                        if promote_moves and normal_moves:
                            # ダイアログで選択
                            promote = messagebox.askyesno("成り", "成りますか？")
                            move = promote_moves[0] if promote else normal_moves[0]
                    
                    self._execute_move(move)
                    self.selected_pos = None
                    self.legal_moves = []
                    self.draw()
                    return
            
            # 別の駒を選択
            piece = self.board.get_piece(row, col)
            if piece and piece.owner == self.board.turn:
                self.selected_pos = (row, col)
                self.legal_moves = Rules.get_piece_moves(self.board, row, col)
                self.draw()
            else:
                # 選択解除
                self.selected_pos = None
                self.legal_moves = []
                self.draw()
        else:
            # 新しく駒を選択
            piece = self.board.get_piece(row, col)
            if piece and piece.owner == self.board.turn:
                self.selected_pos = (row, col)
                self.legal_moves = Rules.get_piece_moves(self.board, row, col)
                self.draw()
    
    def _on_captured_click(self, x, y):
        """持ち駒クリック処理"""
        x_base = self.BOARD_PADDING + self.board_width + 30
        
        # 先手の持ち駒エリア
        y_black = self.grid_top + self.cell_height * 7
        
        # 後手の持ち駒エリア
        y_white = self.grid_top + self.cell_height
        
        # クリック位置から持ち駒を特定
        if self.board.turn == 'black':
            y_base = y_black
            player = 'black'
        else:
            y_base = y_white
            player = 'white'
        
        # 持ち駒を種類ごとにカウント
        piece_counts = {}
        for piece in self.board.captured_pieces[player]:
            base_type = piece.get_base_type()
            if base_type not in piece_counts:
                piece_counts[base_type] = 0
            piece_counts[base_type] += 1
        
        # クリック位置から駒を特定（描画位置は x_base + 20）
        piece_x = x_base + 20
        y_offset = 0
        for piece_type in piece_counts.keys():
            piece_y = y_base + y_offset
            if piece_x - 25 <= x <= piece_x + 25 and piece_y - 25 <= y <= piece_y + 25:
                self.selected_piece_type = piece_type
                self.selected_pos = None
                self.legal_moves = Rules.get_drop_moves(self.board, piece_type)
                self.draw()
                return
            y_offset += 45
    
    def _execute_move(self, move):
        """手を実行"""
        self.board.move_piece(move)
        
        # コールバックを呼ぶ
        if self.on_move_callback:
            self.on_move_callback(move)
    
    def refresh(self):
        """再描画"""
        self.draw()
