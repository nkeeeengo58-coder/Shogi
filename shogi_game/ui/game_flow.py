"""UI非依存の対局進行制御"""

from dataclasses import dataclass

from game.rules import Rules


@dataclass
class GameFlowUpdate:
    turn_text: str | None = None
    turn_color: str = 'black'
    result_type: str | None = None
    status_level: str | None = None
    status_title: str | None = None
    status_message: str | None = None
    input_enabled: bool | None = None
    refresh_board: bool = False
    replace_board: bool = False
    schedule_cpu_move: bool = False


class GameFlowController:
    """GameScreenから切り出した対局進行ロジック"""

    def __init__(
        self,
        game_mode,
        difficulty,
        board,
        engine=None,
        tsume_manager=None,
        current_problem=None,
        current_problem_index=0,
        rules=Rules,
    ):
        self.game_mode = game_mode
        self.difficulty = difficulty
        self.board = board
        self.engine = engine
        self.tsume_manager = tsume_manager
        self.current_problem = current_problem
        self.current_problem_index = current_problem_index
        self.rules = rules

    def get_turn_text(self):
        """現在の手番文言を返す"""
        if self.game_mode == 'tsume':
            return '先手（あなた）の手番'
        if self.board.turn == 'black':
            return '先手（あなた）の手番'
        return '後手（CPU）の手番'

    def get_initial_update(self):
        """画面初期表示時の更新内容を返す"""
        update = GameFlowUpdate(turn_text=self.get_turn_text())
        if self.game_mode == 'normal' and self.board.turn == 'white':
            update.input_enabled = False
            update.schedule_cpu_move = True
        return update

    def handle_player_move(self):
        """プレイヤー手の後処理"""
        if self.game_mode == 'normal':
            return self._handle_normal_player_move()
        return self._handle_tsume_player_move()

    def _handle_normal_player_move(self):
        opponent = 'white' if self.board.turn == 'black' else 'black'
        if self.rules.is_checkmate(self.board, opponent):
            result_type = 'win' if self.board.turn == 'white' else 'lose'
            return GameFlowUpdate(result_type=result_type)

        if self.rules.is_stalemate(self.board):
            return GameFlowUpdate(
                status_level='info',
                status_title='ゲーム終了',
                status_message='千日手により引き分けです',
            )

        in_check = self.rules.is_in_check(self.board, self.board.turn)
        update = GameFlowUpdate(
            turn_text=self.get_turn_text() + (' - 王手！' if in_check else ''),
            turn_color='red' if in_check else 'black',
        )
        if self.board.turn == 'white':
            update.input_enabled = False
            update.schedule_cpu_move = True
        return update

    def _handle_tsume_player_move(self):
        opponent = 'white'
        if self.rules.is_checkmate(self.board, opponent):
            update = self.next_problem()
            return self._merge_updates(
                GameFlowUpdate(
                    status_level='info',
                    status_title='正解',
                    status_message='詰みです！正解です！',
                ),
                update,
            )

        if self.board.turn == 'white':
            if not self._player_has_any_move('white'):
                update = self.next_problem()
                return self._merge_updates(
                    GameFlowUpdate(
                        status_level='info',
                        status_title='正解',
                        status_message='正解です！',
                    ),
                    update,
                )

            self.board.undo_move()
            return GameFlowUpdate(
                status_level='warning',
                status_title='不正解',
                status_message='まだ詰んでいません',
                refresh_board=True,
            )

        return GameFlowUpdate(turn_text=self.get_turn_text())

    def handle_cpu_move(self):
        """CPU手の後処理"""
        if self.engine is None:
            return GameFlowUpdate()

        move = self.engine.get_best_move(self.board)
        if move is None:
            return GameFlowUpdate(result_type='win', input_enabled=True)

        self.board.move_piece(move)
        in_check = self.rules.is_in_check(self.board, 'black')
        update = GameFlowUpdate(
            turn_text=self.get_turn_text() + (' - 王手！' if in_check else ''),
            turn_color='red' if in_check else 'black',
            refresh_board=True,
            input_enabled=True,
        )

        if self.rules.is_checkmate(self.board, 'black'):
            update.result_type = 'lose'

        return update

    def next_problem(self):
        """次の詰将棋問題へ進む"""
        if self.tsume_manager is None:
            return GameFlowUpdate()

        self.current_problem_index += 1
        problem = self.tsume_manager.get_problem(self.difficulty, self.current_problem_index)
        if problem is None:
            return GameFlowUpdate(result_type='win')

        self.current_problem = problem
        self.board = problem.get_board()
        return GameFlowUpdate(
            turn_text=self.get_turn_text(),
            replace_board=True,
            refresh_board=True,
        )

    def get_save_data(self):
        """保存用データを返す"""
        data = {
            'game_mode': self.game_mode,
            'difficulty': self.difficulty,
            'board': self.board.to_dict(),
        }
        if self.game_mode == 'tsume':
            data['current_problem_index'] = self.current_problem_index
        return data

    def _player_has_any_move(self, owner):
        for row in range(9):
            for col in range(9):
                piece = self.board.get_piece(row, col)
                if piece and piece.owner == owner and self.rules.get_piece_moves(self.board, row, col):
                    return True
        return False

    @staticmethod
    def _merge_updates(base, overlay):
        return GameFlowUpdate(
            turn_text=overlay.turn_text if overlay.turn_text is not None else base.turn_text,
            turn_color=overlay.turn_color if overlay.turn_text is not None else base.turn_color,
            result_type=overlay.result_type or base.result_type,
            status_level=base.status_level,
            status_title=base.status_title,
            status_message=base.status_message,
            input_enabled=overlay.input_enabled if overlay.input_enabled is not None else base.input_enabled,
            refresh_board=base.refresh_board or overlay.refresh_board,
            replace_board=base.replace_board or overlay.replace_board,
            schedule_cpu_move=base.schedule_cpu_move or overlay.schedule_cpu_move,
        )
