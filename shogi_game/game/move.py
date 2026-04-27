"""
手（Move）クラスの定義
"""

class Move:
    """将棋の手を表すクラス"""
    
    def __init__(self, from_pos=None, to_pos=None, piece=None, is_drop=False, is_promotion=False):
        """
        Args:
            from_pos: 移動元の位置 (row, col) または None（持ち駒を打つ場合）
            to_pos: 移動先の位置 (row, col)
            piece: 移動する駒
            is_drop: 持ち駒を打つ手かどうか
            is_promotion: 成る手かどうか
        """
        self.from_pos = from_pos
        self.to_pos = to_pos
        self.piece = piece
        self.is_drop = is_drop
        self.is_promotion = is_promotion
        self.captured_piece = None  # 取った駒
    
    def __repr__(self):
        if self.is_drop:
            return f"打: {self.piece.get_name()} -> {self.to_pos}"
        else:
            promo = "成" if self.is_promotion else ""
            return f"{self.from_pos} -> {self.to_pos} {self.piece.get_name()}{promo}"
    
    def to_dict(self):
        """辞書形式に変換"""
        return {
            'from_pos': self.from_pos,
            'to_pos': self.to_pos,
            'piece_type': self.piece.piece_type if self.piece else None,
            'piece_owner': self.piece.owner if self.piece else None,
            'is_drop': self.is_drop,
            'is_promotion': self.is_promotion,
            'captured_piece_type': self.captured_piece.piece_type if self.captured_piece else None,
            'captured_piece_owner': self.captured_piece.owner if self.captured_piece else None,
        }
