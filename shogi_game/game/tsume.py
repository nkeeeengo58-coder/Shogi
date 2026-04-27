"""
詰将棋モジュール
"""
import json
import os
from game.board import Board
from game.piece import Piece
from game.rules import Rules

class TsumeProblem:
    """詰将棋問題クラス"""
    
    def __init__(self, problem_id, difficulty, board_data, solution, description=""):
        """
        Args:
            problem_id: 問題ID
            difficulty: 難易度 ('beginner', 'intermediate', 'advanced', 'expert')
            board_data: 盤面データ（辞書形式）
            solution: 正解手順（Moveのリスト）
            description: 問題の説明
        """
        self.problem_id = problem_id
        self.difficulty = difficulty
        self.board_data = board_data
        self.solution = solution
        self.description = description
    
    def get_board(self):
        """盤面を取得"""
        return Board.from_dict(self.board_data)
    
    def check_solution(self, moves):
        """解答をチェック"""
        # 簡易実装：詰みに至ったかをチェック
        board = self.get_board()
        
        for move in moves:
            # 手が合法かチェック
            legal_moves = []
            if move.is_drop:
                legal_moves = Rules.get_drop_moves(board, move.piece.get_base_type())
            else:
                legal_moves = Rules.get_piece_moves(board, move.from_pos[0], move.from_pos[1])
            
            # 同じ手があるかチェック
            move_found = False
            for legal_move in legal_moves:
                if (legal_move.to_pos == move.to_pos and
                    legal_move.is_promotion == move.is_promotion):
                    board.move_piece(legal_move)
                    move_found = True
                    break
            
            if not move_found:
                return False, "不正な手です"
        
        # 相手（後手）が詰んでいるかチェック
        opponent = 'white' if board.turn == 'black' else 'black'
        if Rules.is_checkmate(board, opponent):
            return True, "正解です！"
        else:
            return False, "詰みに至っていません"
    
    def is_mate_in_n(self, n):
        """n手詰めかどうか（簡易判定）"""
        board = self.get_board()
        return self._search_mate(board, n, True)
    
    def _search_mate(self, board, depth, is_attacker_turn):
        """詰み探索（簡易版）"""
        if depth == 0:
            opponent = 'white' if board.turn == 'black' else 'black'
            return Rules.is_checkmate(board, opponent)
        
        if is_attacker_turn:
            # 攻め方の手番：詰ます手を探す
            all_moves = self._get_all_moves(board)
            for move in all_moves:
                test_board = board.copy()
                test_board.move_piece(move)
                if self._search_mate(test_board, depth - 1, False):
                    return True
            return False
        else:
            # 受け方の手番：全ての手で詰まないかチェック
            all_moves = self._get_all_moves(board)
            if not all_moves:
                # 手がなければ詰み
                return True
            for move in all_moves:
                test_board = board.copy()
                test_board.move_piece(move)
                if not self._search_mate(test_board, depth - 1, True):
                    return False
            return True
    
    def _get_all_moves(self, board):
        """全ての合法手を取得"""
        moves = []
        for row in range(9):
            for col in range(9):
                piece = board.get_piece(row, col)
                if piece and piece.owner == board.turn:
                    moves.extend(Rules.get_piece_moves(board, row, col))
        
        captured_types = set()
        for piece in board.captured_pieces[board.turn]:
            captured_types.add(piece.get_base_type())
        
        for piece_type in captured_types:
            moves.extend(Rules.get_drop_moves(board, piece_type))
        
        return moves


class TsumeManager:
    """詰将棋問題管理クラス"""
    
    def __init__(self):
        self.problems = {}
        self.load_problems()
    
    def load_problems(self):
        """問題を読み込む"""
        problems_file = os.path.join(os.path.dirname(__file__), '../data/tsume_problems.json')
        
        if os.path.exists(problems_file):
            try:
                with open(problems_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for difficulty, problems in data.items():
                        self.problems[difficulty] = []
                        for p in problems:
                            problem = TsumeProblem(
                                p['id'],
                                difficulty,
                                p['board'],
                                p.get('solution', []),
                                p.get('description', '')
                            )
                            self.problems[difficulty].append(problem)
            except Exception as e:
                print(f"問題読み込みエラー: {e}")
    
    def get_problem(self, difficulty, index=0):
        """指定難易度の問題を取得"""
        if difficulty in self.problems and index < len(self.problems[difficulty]):
            return self.problems[difficulty][index]
        return None
    
    def get_problem_count(self, difficulty):
        """指定難易度の問題数を取得"""
        return len(self.problems.get(difficulty, []))
