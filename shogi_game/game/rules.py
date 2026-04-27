"""
将棋のルール判定
"""
from game.piece import PieceType
from game.move import Move

class Rules:
    """将棋のルール判定クラス"""
    
    @staticmethod
    def get_piece_moves(board, row, col):
        """
        指定位置の駒が移動できるマスのリストを返す
        
        Returns:
            list of Move: 可能な手のリスト
        """
        piece = board.get_piece(row, col)
        if not piece or piece.owner != board.turn:
            return []
        
        moves = []
        piece_type = piece.piece_type
        owner = piece.owner
        
        # 方向: (row_delta, col_delta)
        # 先手（black）は上方向がマイナス、後手（white）は下方向がプラス
        direction = -1 if owner == 'black' else 1
        
        if piece_type == PieceType.KING:
            # 王：全方向1マス
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr == 0 and dc == 0:
                        continue
                    moves.extend(Rules._try_move(board, row, col, row + dr, col + dc))
        
        elif piece_type == PieceType.ROOK:
            # 飛車：縦横
            for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                moves.extend(Rules._try_line_move(board, row, col, dr, dc))
        
        elif piece_type == PieceType.BISHOP:
            # 角：斜め
            for dr, dc in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
                moves.extend(Rules._try_line_move(board, row, col, dr, dc))
        
        elif piece_type == PieceType.GOLD or piece_type in [
            PieceType.PROMOTED_SILVER, PieceType.PROMOTED_KNIGHT,
            PieceType.PROMOTED_LANCE, PieceType.PROMOTED_PAWN
        ]:
            # 金、成り駒（金と同じ動き）
            for dr, dc in [(direction, 0), (direction, -1), (direction, 1),
                          (0, -1), (0, 1), (-direction, 0)]:
                moves.extend(Rules._try_move(board, row, col, row + dr, col + dc))
        
        elif piece_type == PieceType.SILVER:
            # 銀：前方3方向と斜め後ろ
            for dr, dc in [(direction, 0), (direction, -1), (direction, 1),
                          (-direction, -1), (-direction, 1)]:
                moves.extend(Rules._try_move(board, row, col, row + dr, col + dc))
        
        elif piece_type == PieceType.KNIGHT:
            # 桂馬：前方の桂馬飛び
            for dc in [-1, 1]:
                moves.extend(Rules._try_move(board, row, col, row + direction * 2, col + dc))
        
        elif piece_type == PieceType.LANCE:
            # 香車：前方直線
            moves.extend(Rules._try_line_move(board, row, col, direction, 0))
        
        elif piece_type == PieceType.PAWN:
            # 歩：前方1マス
            moves.extend(Rules._try_move(board, row, col, row + direction, col))
        
        elif piece_type == PieceType.PROMOTED_ROOK:
            # 竜王：飛車+王の斜め
            for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                moves.extend(Rules._try_line_move(board, row, col, dr, dc))
            for dr, dc in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
                moves.extend(Rules._try_move(board, row, col, row + dr, col + dc))
        
        elif piece_type == PieceType.PROMOTED_BISHOP:
            # 竜馬：角+王の縦横
            for dr, dc in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
                moves.extend(Rules._try_line_move(board, row, col, dr, dc))
            for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                moves.extend(Rules._try_move(board, row, col, row + dr, col + dc))
        
        # 王手放置チェック
        legal_moves = []
        for move in moves:
            test_board = board.copy()
            test_board.move_piece(move)
            # 手番が変わっているので、元の手番をチェック
            if not Rules.is_in_check(test_board, owner):
                legal_moves.append(move)
        
        return legal_moves
    
    @staticmethod
    def _try_move(board, from_row, from_col, to_row, to_col):
        """1マスの移動を試行"""
        if not (0 <= to_row < 9 and 0 <= to_col < 9):
            return []
        
        piece = board.get_piece(from_row, from_col)
        target = board.get_piece(to_row, to_col)
        
        # 自分の駒がある場合は移動不可
        if target and target.owner == piece.owner:
            return []
        
        moves = []
        move = Move((from_row, from_col), (to_row, to_col), piece, False, False)
        moves.append(move)
        
        # 成れる条件をチェック
        if Rules._can_promote(piece, from_row, to_row):
            promo_move = Move((from_row, from_col), (to_row, to_col), piece, False, True)
            moves.append(promo_move)
        
        # 行き所のない駒チェック
        valid_moves = []
        for m in moves:
            if not Rules._is_no_retreat_position(piece, to_row, m.is_promotion):
                valid_moves.append(m)
        
        return valid_moves
    
    @staticmethod
    def _try_line_move(board, from_row, from_col, dr, dc):
        """直線上の移動を試行"""
        moves = []
        piece = board.get_piece(from_row, from_col)
        
        r, c = from_row + dr, from_col + dc
        while 0 <= r < 9 and 0 <= c < 9:
            target = board.get_piece(r, c)
            
            if target:
                # 相手の駒なら取れる
                if target.owner != piece.owner:
                    move = Move((from_row, from_col), (r, c), piece, False, False)
                    moves.append(move)
                    
                    # 成れる条件をチェック
                    if Rules._can_promote(piece, from_row, r):
                        promo_move = Move((from_row, from_col), (r, c), piece, False, True)
                        moves.append(promo_move)
                break
            else:
                # 空きマスなら移動可能
                move = Move((from_row, from_col), (r, c), piece, False, False)
                moves.append(move)
                
                # 成れる条件をチェック
                if Rules._can_promote(piece, from_row, r):
                    promo_move = Move((from_row, from_col), (r, c), piece, False, True)
                    moves.append(promo_move)
            
            r += dr
            c += dc
        
        return moves
    
    @staticmethod
    def _can_promote(piece, from_row, to_row):
        """成れるかどうか"""
        if not piece.can_promote():
            return False
        
        # 敵陣（先手は0-2段目、後手は6-8段目）に入るか、敵陣から出るか
        if piece.owner == 'black':
            return from_row <= 2 or to_row <= 2
        else:
            return from_row >= 6 or to_row >= 6
    
    @staticmethod
    def _is_no_retreat_position(piece, to_row, is_promotion):
        """行き所のない位置かどうか"""
        if is_promotion:
            return False
        
        piece_type = piece.piece_type
        owner = piece.owner
        
        # 先手の場合
        if owner == 'black':
            if piece_type == PieceType.PAWN or piece_type == PieceType.LANCE:
                return to_row == 0  # 1段目に歩・香は置けない
            elif piece_type == PieceType.KNIGHT:
                return to_row <= 1  # 1-2段目に桂馬は置けない
        else:
            # 後手の場合
            if piece_type == PieceType.PAWN or piece_type == PieceType.LANCE:
                return to_row == 8  # 9段目に歩・香は置けない
            elif piece_type == PieceType.KNIGHT:
                return to_row >= 7  # 8-9段目に桂馬は置けない
        
        return False
    
    @staticmethod
    def get_drop_moves(board, piece_type):
        """
        持ち駒を打てる位置のリストを返す
        
        Args:
            board: 盤面
            piece_type: 駒の種類（基本形）
        
        Returns:
            list of Move: 可能な打つ手のリスト
        """
        moves = []
        owner = board.turn
        
        # 二歩チェック用：各列の歩の有無
        pawn_columns = set()
        if piece_type == PieceType.PAWN:
            for row in range(9):
                for col in range(9):
                    piece = board.get_piece(row, col)
                    if piece and piece.owner == owner and piece.piece_type == PieceType.PAWN:
                        pawn_columns.add(col)
        
        for row in range(9):
            for col in range(9):
                # 空きマスのみ
                if board.get_piece(row, col) is not None:
                    continue
                
                # 二歩チェック
                if piece_type == PieceType.PAWN and col in pawn_columns:
                    continue
                
                # 行き所のない位置チェック
                piece = Piece(piece_type, owner)
                if Rules._is_no_retreat_position(piece, row, False):
                    continue
                
                # 打ち歩詰めチェック
                if piece_type == PieceType.PAWN:
                    if Rules._is_pawn_drop_mate(board, row, col):
                        continue
                
                move = Move(None, (row, col), piece, True, False)
                moves.append(move)
        
        return moves
    
    @staticmethod
    def _is_pawn_drop_mate(board, row, col):
        """打ち歩詰めかどうか"""
        # 簡易実装：歩を打って王手になり、かつ詰みの場合
        test_board = board.copy()
        from game.piece import Piece
        pawn = Piece(PieceType.PAWN, test_board.turn)
        move = Move(None, (row, col), pawn, True, False)
        test_board.move_piece(move)
        
        # 相手が詰んでいるかチェック
        opponent = 'white' if test_board.turn == 'black' else 'black'
        
        # 王手かどうか
        if not Rules.is_in_check(test_board, opponent):
            return False
        
        # 詰みかどうか（相手に合法手がないか）
        has_legal_move = False
        for r in range(9):
            for c in range(9):
                piece = test_board.get_piece(r, c)
                if piece and piece.owner == opponent:
                    if Rules.get_piece_moves(test_board, r, c):
                        has_legal_move = True
                        break
            if has_legal_move:
                break
        
        # 持ち駒を打つ手もチェック
        if not has_legal_move:
            for captured_piece in test_board.captured_pieces[opponent]:
                if Rules.get_drop_moves(test_board, captured_piece.get_base_type()):
                    has_legal_move = True
                    break
        
        # 詰んでいれば打ち歩詰め
        return not has_legal_move
    
    @staticmethod
    def is_in_check(board, player):
        """
        指定プレイヤーの王が王手されているか
        
        Args:
            player: チェックするプレイヤー ('black' or 'white')
        
        Returns:
            bool: 王手されていればTrue
        """
        # 王の位置を探す
        king_pos = None
        for row in range(9):
            for col in range(9):
                piece = board.get_piece(row, col)
                if piece and piece.owner == player and piece.piece_type == PieceType.KING:
                    king_pos = (row, col)
                    break
            if king_pos:
                break
        
        if not king_pos:
            return False
        
        # 相手の駒が王を取れるかチェック
        opponent = 'white' if player == 'black' else 'black'
        for row in range(9):
            for col in range(9):
                piece = board.get_piece(row, col)
                if piece and piece.owner == opponent:
                    # 簡易的に移動可能位置を取得（王手放置チェックなし）
                    moves = Rules._get_piece_moves_simple(board, row, col)
                    for move in moves:
                        if move.to_pos == king_pos:
                            return True
        
        return False
    
    @staticmethod
    def _get_piece_moves_simple(board, row, col):
        """王手放置チェックなしで移動可能位置を取得"""
        piece = board.get_piece(row, col)
        if not piece:
            return []
        
        moves = []
        piece_type = piece.piece_type
        owner = piece.owner
        direction = -1 if owner == 'black' else 1
        
        if piece_type == PieceType.KING:
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr == 0 and dc == 0:
                        continue
                    moves.extend(Rules._try_move_simple(board, row, col, row + dr, col + dc))
        
        elif piece_type == PieceType.ROOK:
            for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                moves.extend(Rules._try_line_move_simple(board, row, col, dr, dc))
        
        elif piece_type == PieceType.BISHOP:
            for dr, dc in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
                moves.extend(Rules._try_line_move_simple(board, row, col, dr, dc))
        
        elif piece_type == PieceType.GOLD or piece_type in [
            PieceType.PROMOTED_SILVER, PieceType.PROMOTED_KNIGHT,
            PieceType.PROMOTED_LANCE, PieceType.PROMOTED_PAWN
        ]:
            for dr, dc in [(direction, 0), (direction, -1), (direction, 1),
                          (0, -1), (0, 1), (-direction, 0)]:
                moves.extend(Rules._try_move_simple(board, row, col, row + dr, col + dc))
        
        elif piece_type == PieceType.SILVER:
            for dr, dc in [(direction, 0), (direction, -1), (direction, 1),
                          (-direction, -1), (-direction, 1)]:
                moves.extend(Rules._try_move_simple(board, row, col, row + dr, col + dc))
        
        elif piece_type == PieceType.KNIGHT:
            for dc in [-1, 1]:
                moves.extend(Rules._try_move_simple(board, row, col, row + direction * 2, col + dc))
        
        elif piece_type == PieceType.LANCE:
            moves.extend(Rules._try_line_move_simple(board, row, col, direction, 0))
        
        elif piece_type == PieceType.PAWN:
            moves.extend(Rules._try_move_simple(board, row, col, row + direction, col))
        
        elif piece_type == PieceType.PROMOTED_ROOK:
            for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                moves.extend(Rules._try_line_move_simple(board, row, col, dr, dc))
            for dr, dc in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
                moves.extend(Rules._try_move_simple(board, row, col, row + dr, col + dc))
        
        elif piece_type == PieceType.PROMOTED_BISHOP:
            for dr, dc in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
                moves.extend(Rules._try_line_move_simple(board, row, col, dr, dc))
            for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                moves.extend(Rules._try_move_simple(board, row, col, row + dr, col + dc))
        
        return moves
    
    @staticmethod
    def _try_move_simple(board, from_row, from_col, to_row, to_col):
        """1マスの移動を試行（簡易版）"""
        if not (0 <= to_row < 9 and 0 <= to_col < 9):
            return []
        
        piece = board.get_piece(from_row, from_col)
        target = board.get_piece(to_row, to_col)
        
        if target and target.owner == piece.owner:
            return []
        
        move = Move((from_row, from_col), (to_row, to_col), piece, False, False)
        return [move]
    
    @staticmethod
    def _try_line_move_simple(board, from_row, from_col, dr, dc):
        """直線上の移動を試行（簡易版）"""
        moves = []
        piece = board.get_piece(from_row, from_col)
        
        r, c = from_row + dr, from_col + dc
        while 0 <= r < 9 and 0 <= c < 9:
            target = board.get_piece(r, c)
            
            if target:
                if target.owner != piece.owner:
                    move = Move((from_row, from_col), (r, c), piece, False, False)
                    moves.append(move)
                break
            else:
                move = Move((from_row, from_col), (r, c), piece, False, False)
                moves.append(move)
            
            r += dr
            c += dc
        
        return moves
    
    @staticmethod
    def is_checkmate(board, player):
        """
        指定プレイヤーが詰んでいるか
        
        Args:
            player: チェックするプレイヤー
        
        Returns:
            bool: 詰んでいればTrue
        """
        # 王手されていなければ詰みではない
        if not Rules.is_in_check(board, player):
            return False
        
        # 合法手があるかチェック
        for row in range(9):
            for col in range(9):
                piece = board.get_piece(row, col)
                if piece and piece.owner == player:
                    if Rules.get_piece_moves(board, row, col):
                        return False
        
        # 持ち駒を打つ手もチェック
        for captured_piece in board.captured_pieces[player]:
            if Rules.get_drop_moves(board, captured_piece.get_base_type()):
                return False
        
        return True
    
    @staticmethod
    def is_stalemate(board):
        """千日手（同一局面が4回）の簡易チェック"""
        # 簡易実装：履歴から同じ盤面を探す
        if len(board.move_history) < 8:
            return False
        
        # 実際の千日手判定は複雑なので、ここでは簡易的に
        # 同じ位置への往復が続いているかをチェック
        recent_moves = board.move_history[-8:]
        if len(recent_moves) >= 8:
            # 4往復（8手）で同じパターンが繰り返されているか
            pattern1 = recent_moves[0:2]
            pattern2 = recent_moves[2:4]
            pattern3 = recent_moves[4:6]
            pattern4 = recent_moves[6:8]
            
            # 簡易的なチェック
            if (pattern1[0].to_pos == pattern2[1].from_pos and
                pattern1[1].to_pos == pattern2[0].from_pos and
                pattern2[0].to_pos == pattern3[1].from_pos and
                pattern2[1].to_pos == pattern3[0].from_pos and
                pattern3[0].to_pos == pattern4[1].from_pos and
                pattern3[1].to_pos == pattern4[0].from_pos):
                return True
        
        return False
