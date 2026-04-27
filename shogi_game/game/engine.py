"""
CPU思考エンジン
"""
import random
from game.rules import Rules
from game.piece import PieceType

class Engine:
    """CPU思考エンジンクラス"""
    
    # 駒の基本価値
    PIECE_VALUES = {
        PieceType.KING: 10000,
        PieceType.ROOK: 900,
        PieceType.BISHOP: 800,
        PieceType.GOLD: 600,
        PieceType.SILVER: 500,
        PieceType.KNIGHT: 400,
        PieceType.LANCE: 400,
        PieceType.PAWN: 100,
        PieceType.PROMOTED_ROOK: 1100,
        PieceType.PROMOTED_BISHOP: 1000,
        PieceType.PROMOTED_SILVER: 600,
        PieceType.PROMOTED_KNIGHT: 600,
        PieceType.PROMOTED_LANCE: 600,
        PieceType.PROMOTED_PAWN: 600,
    }
    
    def __init__(self, difficulty='beginner'):
        """
        Args:
            difficulty: 難易度 ('beginner', 'intermediate', 'advanced', 'expert')
        """
        self.difficulty = difficulty
    
    def get_best_move(self, board):
        """最善手を取得"""
        if self.difficulty == 'beginner':
            return self._get_beginner_move(board)
        elif self.difficulty == 'intermediate':
            return self._get_intermediate_move(board)
        elif self.difficulty == 'advanced':
            return self._get_advanced_move(board)
        elif self.difficulty == 'expert':
            return self._get_expert_move(board)
        else:
            return self._get_beginner_move(board)
    
    def _get_all_legal_moves(self, board):
        """全ての合法手を取得"""
        moves = []
        
        # 盤上の駒の移動
        for row in range(9):
            for col in range(9):
                piece = board.get_piece(row, col)
                if piece and piece.owner == board.turn:
                    moves.extend(Rules.get_piece_moves(board, row, col))
        
        # 持ち駒を打つ手
        captured_types = set()
        for piece in board.captured_pieces[board.turn]:
            captured_types.add(piece.get_base_type())
        
        for piece_type in captured_types:
            moves.extend(Rules.get_drop_moves(board, piece_type))
        
        return moves
    
    def _get_beginner_move(self, board):
        """初級：ランダム寄りの選択"""
        all_moves = self._get_all_legal_moves(board)
        
        if not all_moves:
            return None
        
        # 明らかに悪い手を除外
        good_moves = []
        for move in all_moves:
            test_board = board.copy()
            test_board.move_piece(move)
            
            # 王手放置になる手は除外済み（Rules.get_piece_movesで）
            # 駒損になる手を避ける
            opponent = 'white' if board.turn == 'black' else 'black'
            
            # 移動先が攻撃されていないかチェック
            if not move.is_drop:
                is_attacked = False
                for r in range(9):
                    for c in range(9):
                        p = test_board.get_piece(r, c)
                        if p and p.owner == opponent:
                            opp_moves = Rules._get_piece_moves_simple(test_board, r, c)
                            for om in opp_moves:
                                if om.to_pos == move.to_pos:
                                    # 価値の低い駒で取られる場合は除外
                                    if move.piece:
                                        piece_value = self.PIECE_VALUES.get(move.piece.piece_type, 0)
                                        attacker_value = self.PIECE_VALUES.get(p.piece_type, 0)
                                        if piece_value > attacker_value + 200:
                                            is_attacked = True
                                            break
                    if is_attacked:
                        break
                
                if not is_attacked:
                    good_moves.append(move)
            else:
                good_moves.append(move)
        
        if good_moves:
            return random.choice(good_moves)
        else:
            return random.choice(all_moves)
    
    def _get_intermediate_move(self, board):
        """中級：1-2手読み"""
        all_moves = self._get_all_legal_moves(board)
        
        if not all_moves:
            return None
        
        best_move = None
        best_score = float('-inf')
        
        for move in all_moves:
            test_board = board.copy()
            test_board.move_piece(move)
            
            # 1手先の評価
            score = self._evaluate_board(test_board, board.turn)
            
            # 相手の応手を考慮（簡易）
            opponent_moves = self._get_all_legal_moves(test_board)
            if opponent_moves:
                worst_response_score = float('inf')
                for opp_move in opponent_moves[:10]:  # 最初の10手のみ
                    test_board2 = test_board.copy()
                    test_board2.move_piece(opp_move)
                    response_score = self._evaluate_board(test_board2, board.turn)
                    worst_response_score = min(worst_response_score, response_score)
                score = worst_response_score
            
            if score > best_score:
                best_score = score
                best_move = move
        
        return best_move if best_move else random.choice(all_moves)
    
    def _get_advanced_move(self, board):
        """上級：3-4手読み（ミニマックス + αβ枝刈り）"""
        all_moves = self._get_all_legal_moves(board)
        
        if not all_moves:
            return None
        
        best_move = None
        best_score = float('-inf')
        alpha = float('-inf')
        beta = float('inf')
        
        for move in all_moves:
            test_board = board.copy()
            test_board.move_piece(move)
            
            score = self._minimax(test_board, 3, alpha, beta, False, board.turn)
            
            if score > best_score:
                best_score = score
                best_move = move
            
            alpha = max(alpha, score)
        
        return best_move if best_move else random.choice(all_moves)
    
    def _get_expert_move(self, board):
        """超上級：4手以上の探索"""
        all_moves = self._get_all_legal_moves(board)
        
        if not all_moves:
            return None
        
        best_move = None
        best_score = float('-inf')
        alpha = float('-inf')
        beta = float('inf')
        
        for move in all_moves:
            test_board = board.copy()
            test_board.move_piece(move)
            
            score = self._minimax(test_board, 4, alpha, beta, False, board.turn)
            
            if score > best_score:
                best_score = score
                best_move = move
            
            alpha = max(alpha, score)
        
        return best_move if best_move else random.choice(all_moves)
    
    def _minimax(self, board, depth, alpha, beta, is_maximizing, original_player):
        """ミニマックス法 with αβ枝刈り"""
        # 深さ0または詰みの場合
        current_player = board.turn if not is_maximizing else ('white' if board.turn == 'black' else 'black')
        
        if depth == 0:
            return self._evaluate_board(board, original_player)
        
        # 詰みチェック
        if Rules.is_checkmate(board, board.turn):
            return -100000 if is_maximizing else 100000
        
        all_moves = self._get_all_legal_moves(board)
        if not all_moves:
            return self._evaluate_board(board, original_player)
        
        # 手を制限（計算量削減）
        if len(all_moves) > 20:
            all_moves = all_moves[:20]
        
        if is_maximizing:
            max_eval = float('-inf')
            for move in all_moves:
                test_board = board.copy()
                test_board.move_piece(move)
                eval_score = self._minimax(test_board, depth - 1, alpha, beta, False, original_player)
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for move in all_moves:
                test_board = board.copy()
                test_board.move_piece(move)
                eval_score = self._minimax(test_board, depth - 1, alpha, beta, True, original_player)
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break
            return min_eval
    
    def _evaluate_board(self, board, player):
        """盤面評価"""
        score = 0
        opponent = 'white' if player == 'black' else 'black'
        
        # 駒の価値
        for row in range(9):
            for col in range(9):
                piece = board.get_piece(row, col)
                if piece:
                    piece_value = self.PIECE_VALUES.get(piece.piece_type, 0)
                    if piece.owner == player:
                        score += piece_value
                    else:
                        score -= piece_value
        
        # 持ち駒の価値
        for piece in board.captured_pieces[player]:
            score += self.PIECE_VALUES.get(piece.get_base_type(), 0) * 0.8
        
        for piece in board.captured_pieces[opponent]:
            score -= self.PIECE_VALUES.get(piece.get_base_type(), 0) * 0.8
        
        # 王手ボーナス
        if Rules.is_in_check(board, opponent):
            score += 500
        if Rules.is_in_check(board, player):
            score -= 500
        
        # 詰みチェック
        if Rules.is_checkmate(board, opponent):
            score += 100000
        if Rules.is_checkmate(board, player):
            score -= 100000
        
        # 王の安全性
        king_safety_score = self._evaluate_king_safety(board, player)
        score += king_safety_score
        score -= self._evaluate_king_safety(board, opponent)
        
        return score
    
    def _evaluate_king_safety(self, board, player):
        """王の安全性評価"""
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
            return 0
        
        safety_score = 0
        king_row, king_col = king_pos
        
        # 周囲の味方駒（守り駒）
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                r, c = king_row + dr, king_col + dc
                if 0 <= r < 9 and 0 <= c < 9:
                    piece = board.get_piece(r, c)
                    if piece and piece.owner == player:
                        if piece.piece_type == PieceType.GOLD:
                            safety_score += 50
                        elif piece.piece_type == PieceType.SILVER:
                            safety_score += 30
                        else:
                            safety_score += 20
        
        return safety_score
