"""
駒クラスの定義
"""

class PieceType:
    """駒の種類"""
    KING = 'king'          # 王
    ROOK = 'rook'          # 飛車
    BISHOP = 'bishop'      # 角
    GOLD = 'gold'          # 金
    SILVER = 'silver'      # 銀
    KNIGHT = 'knight'      # 桂馬
    LANCE = 'lance'        # 香車
    PAWN = 'pawn'          # 歩
    
    # 成り駒
    PROMOTED_ROOK = 'promoted_rook'      # 竜王
    PROMOTED_BISHOP = 'promoted_bishop'  # 竜馬
    PROMOTED_SILVER = 'promoted_silver'  # 成銀
    PROMOTED_KNIGHT = 'promoted_knight'  # 成桂
    PROMOTED_LANCE = 'promoted_lance'    # 成香
    PROMOTED_PAWN = 'promoted_pawn'      # と金

class Piece:
    """駒クラス"""
    
    # 駒の日本語名
    PIECE_NAMES = {
        PieceType.KING: '王',
        PieceType.ROOK: '飛',
        PieceType.BISHOP: '角',
        PieceType.GOLD: '金',
        PieceType.SILVER: '銀',
        PieceType.KNIGHT: '桂',
        PieceType.LANCE: '香',
        PieceType.PAWN: '歩',
        PieceType.PROMOTED_ROOK: '竜',
        PieceType.PROMOTED_BISHOP: '馬',
        PieceType.PROMOTED_SILVER: '全',
        PieceType.PROMOTED_KNIGHT: '圭',
        PieceType.PROMOTED_LANCE: '杏',
        PieceType.PROMOTED_PAWN: 'と',
    }
    
    # 成れる駒のマッピング
    PROMOTION_MAP = {
        PieceType.ROOK: PieceType.PROMOTED_ROOK,
        PieceType.BISHOP: PieceType.PROMOTED_BISHOP,
        PieceType.SILVER: PieceType.PROMOTED_SILVER,
        PieceType.KNIGHT: PieceType.PROMOTED_KNIGHT,
        PieceType.LANCE: PieceType.PROMOTED_LANCE,
        PieceType.PAWN: PieceType.PROMOTED_PAWN,
    }
    
    # 成り駒を元に戻すマッピング
    DEMOTION_MAP = {v: k for k, v in PROMOTION_MAP.items()}
    
    def __init__(self, piece_type, owner):
        """
        Args:
            piece_type: 駒の種類 (PieceType)
            owner: 駒の所有者 ('black' or 'white')
        """
        self.piece_type = piece_type
        self.owner = owner
    
    def can_promote(self):
        """成ることができるか"""
        return self.piece_type in self.PROMOTION_MAP
    
    def promote(self):
        """成る"""
        if self.can_promote():
            self.piece_type = self.PROMOTION_MAP[self.piece_type]
            return True
        return False
    
    def is_promoted(self):
        """成り駒かどうか"""
        return self.piece_type in self.DEMOTION_MAP
    
    def get_base_type(self):
        """元の駒の種類を取得（持ち駒用）"""
        if self.is_promoted():
            return self.DEMOTION_MAP[self.piece_type]
        return self.piece_type
    
    def get_name(self):
        """駒の名前を取得"""
        return self.PIECE_NAMES.get(self.piece_type, '?')
    
    def copy(self):
        """駒のコピーを作成"""
        return Piece(self.piece_type, self.owner)
    
    def __repr__(self):
        owner_str = '☗' if self.owner == 'black' else '☖'
        return f"{owner_str}{self.get_name()}"
