"""
将棋盤クラスの定義
"""
from game.piece import Piece, PieceType

class Board:
    """将棋盤クラス"""
    
    def __init__(self):
        """9x9の将棋盤を初期化"""
        self.board = [[None for _ in range(9)] for _ in range(9)]
        self.captured_pieces = {'black': [], 'white': []}  # 持ち駒
        self.turn = 'black'  # 'black'（先手）または 'white'（後手）
        self.move_history = []  # 手の履歴
        self.last_move = None  # 直前の手
    
    def initialize_normal_game(self):
        """通常将棋の初期配置"""
        # 後手（白）の駒配置
        self.board[0][4] = Piece(PieceType.KING, 'white')
        self.board[0][3] = Piece(PieceType.GOLD, 'white')
        self.board[0][5] = Piece(PieceType.GOLD, 'white')
        self.board[0][2] = Piece(PieceType.SILVER, 'white')
        self.board[0][6] = Piece(PieceType.SILVER, 'white')
        self.board[0][1] = Piece(PieceType.KNIGHT, 'white')
        self.board[0][7] = Piece(PieceType.KNIGHT, 'white')
        self.board[0][0] = Piece(PieceType.LANCE, 'white')
        self.board[0][8] = Piece(PieceType.LANCE, 'white')
        self.board[1][1] = Piece(PieceType.BISHOP, 'white')
        self.board[1][7] = Piece(PieceType.ROOK, 'white')
        for col in range(9):
            self.board[2][col] = Piece(PieceType.PAWN, 'white')
        
        # 先手（黒）の駒配置
        self.board[8][4] = Piece(PieceType.KING, 'black')
        self.board[8][3] = Piece(PieceType.GOLD, 'black')
        self.board[8][5] = Piece(PieceType.GOLD, 'black')
        self.board[8][2] = Piece(PieceType.SILVER, 'black')
        self.board[8][6] = Piece(PieceType.SILVER, 'black')
        self.board[8][1] = Piece(PieceType.KNIGHT, 'black')
        self.board[8][7] = Piece(PieceType.KNIGHT, 'black')
        self.board[8][0] = Piece(PieceType.LANCE, 'black')
        self.board[8][8] = Piece(PieceType.LANCE, 'black')
        self.board[7][7] = Piece(PieceType.BISHOP, 'black')
        self.board[7][1] = Piece(PieceType.ROOK, 'black')
        for col in range(9):
            self.board[6][col] = Piece(PieceType.PAWN, 'black')
    
    def get_piece(self, row, col):
        """指定位置の駒を取得"""
        if 0 <= row < 9 and 0 <= col < 9:
            return self.board[row][col]
        return None
    
    def set_piece(self, row, col, piece):
        """指定位置に駒を配置"""
        if 0 <= row < 9 and 0 <= col < 9:
            self.board[row][col] = piece
    
    def remove_piece(self, row, col):
        """指定位置の駒を削除"""
        if 0 <= row < 9 and 0 <= col < 9:
            piece = self.board[row][col]
            self.board[row][col] = None
            return piece
        return None
    
    def move_piece(self, move):
        """駒を移動"""
        if move.is_drop:
            # 持ち駒を打つ
            self.set_piece(move.to_pos[0], move.to_pos[1], move.piece.copy())
            # 持ち駒から削除
            base_type = move.piece.get_base_type()
            for i, p in enumerate(self.captured_pieces[self.turn]):
                if p.get_base_type() == base_type:
                    self.captured_pieces[self.turn].pop(i)
                    break
        else:
            # 通常の移動
            from_row, from_col = move.from_pos
            to_row, to_col = move.to_pos
            
            piece = self.get_piece(from_row, from_col)
            captured = self.get_piece(to_row, to_col)
            
            # 駒を取った場合
            if captured:
                move.captured_piece = captured
                # 成り駒は元に戻して持ち駒に
                captured_piece = Piece(captured.get_base_type(), self.turn)
                self.captured_pieces[self.turn].append(captured_piece)
            
            # 駒を移動
            self.remove_piece(from_row, from_col)
            
            # 成る場合
            if move.is_promotion and piece.can_promote():
                piece.promote()
            
            self.set_piece(to_row, to_col, piece)
        
        # 手番を交代
        self.turn = 'white' if self.turn == 'black' else 'black'
        
        # 履歴に追加
        self.move_history.append(move)
        self.last_move = move
    
    def undo_move(self):
        """手を戻す"""
        if not self.move_history:
            return False
        
        move = self.move_history.pop()
        self.turn = 'white' if self.turn == 'black' else 'black'
        
        if move.is_drop:
            # 打った駒を取り除き、持ち駒に戻す
            piece = self.remove_piece(move.to_pos[0], move.to_pos[1])
            captured_piece = Piece(piece.get_base_type(), self.turn)
            self.captured_pieces[self.turn].append(captured_piece)
        else:
            # 通常の移動を戻す
            to_row, to_col = move.to_pos
            from_row, from_col = move.from_pos
            
            piece = self.remove_piece(to_row, to_col)
            
            # 成った駒を戻す
            if move.is_promotion:
                piece.piece_type = piece.get_base_type()
            
            self.set_piece(from_row, from_col, piece)
            
            # 取った駒を戻す
            if move.captured_piece:
                self.set_piece(to_row, to_col, move.captured_piece)
                # 持ち駒から削除
                base_type = move.captured_piece.get_base_type()
                for i, p in enumerate(self.captured_pieces[self.turn]):
                    if p.get_base_type() == base_type:
                        self.captured_pieces[self.turn].pop(i)
                        break
        
        self.last_move = self.move_history[-1] if self.move_history else None
        return True
    
    def copy(self):
        """盤面のコピーを作成"""
        new_board = Board()
        new_board.board = [[piece.copy() if piece else None for piece in row] for row in self.board]
        new_board.captured_pieces = {
            'black': [p.copy() for p in self.captured_pieces['black']],
            'white': [p.copy() for p in self.captured_pieces['white']]
        }
        new_board.turn = self.turn
        new_board.move_history = self.move_history.copy()
        new_board.last_move = self.last_move
        return new_board
    
    def to_dict(self):
        """辞書形式に変換（保存用）"""
        board_data = []
        for row in range(9):
            row_data = []
            for col in range(9):
                piece = self.board[row][col]
                if piece:
                    row_data.append({
                        'type': piece.piece_type,
                        'owner': piece.owner
                    })
                else:
                    row_data.append(None)
            board_data.append(row_data)
        
        return {
            'board': board_data,
            'captured_pieces': {
                'black': [{'type': p.piece_type, 'owner': p.owner} for p in self.captured_pieces['black']],
                'white': [{'type': p.piece_type, 'owner': p.owner} for p in self.captured_pieces['white']]
            },
            'turn': self.turn,
            'move_history': [m.to_dict() for m in self.move_history]
        }
    
    @staticmethod
    def from_dict(data):
        """辞書形式から復元"""
        board = Board()
        
        # 盤面を復元
        for row in range(9):
            for col in range(9):
                piece_data = data['board'][row][col]
                if piece_data:
                    board.board[row][col] = Piece(piece_data['type'], piece_data['owner'])
        
        # 持ち駒を復元
        board.captured_pieces = {
            'black': [Piece(p['type'], p['owner']) for p in data['captured_pieces']['black']],
            'white': [Piece(p['type'], p['owner']) for p in data['captured_pieces']['white']]
        }
        
        board.turn = data['turn']
        
        return board
