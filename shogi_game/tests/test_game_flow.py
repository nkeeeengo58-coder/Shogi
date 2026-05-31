from types import SimpleNamespace

from ui.game_flow import GameFlowController


class FakeBoard:
    def __init__(self, turn='black', pieces=None):
        self.turn = turn
        self.undo_called = False
        self.moved = []
        self._pieces = pieces or {}

    def move_piece(self, move):
        self.moved.append(move)
        self.turn = 'white' if self.turn == 'black' else 'black'

    def undo_move(self):
        self.undo_called = True

    def to_dict(self):
        return {'turn': self.turn}

    def get_piece(self, row, col):
        return self._pieces.get((row, col))


class FakeProblem:
    def __init__(self, board):
        self._board = board

    def get_board(self):
        return self._board


class FakeTsumeManager:
    def __init__(self, mapping):
        self.mapping = mapping

    def get_problem(self, difficulty, index):
        return self.mapping.get((difficulty, index))


class FakeEngine:
    def __init__(self, move=None):
        self.move = move
        self.calls = []

    def get_best_move(self, board):
        self.calls.append(board)
        return self.move


class FakeRules:
    checkmate = False
    stalemate = False
    in_check = False
    moves = {}

    @classmethod
    def is_checkmate(cls, board, owner):
        return cls.checkmate

    @classmethod
    def is_stalemate(cls, board):
        return cls.stalemate

    @classmethod
    def is_in_check(cls, board, owner):
        return cls.in_check

    @classmethod
    def get_piece_moves(cls, board, row, col):
        return cls.moves.get((row, col), [])


def reset_rules():
    FakeRules.checkmate = False
    FakeRules.stalemate = False
    FakeRules.in_check = False
    FakeRules.moves = {}


def test_initial_update_schedules_cpu_when_white_turn():
    controller = GameFlowController('normal', 'beginner', FakeBoard(turn='white'), rules=FakeRules)

    update = controller.get_initial_update()

    assert update.turn_text == '後手（CPU）の手番'
    assert update.input_enabled is False
    assert update.schedule_cpu_move is True


def test_normal_player_move_reports_stalemate():
    reset_rules()
    FakeRules.stalemate = True
    controller = GameFlowController('normal', 'beginner', FakeBoard(turn='black'), rules=FakeRules)

    update = controller.handle_player_move()

    assert update.status_level == 'info'
    assert update.status_title == 'ゲーム終了'
    assert update.status_message == '千日手により引き分けです'


def test_normal_player_move_disables_input_and_marks_check_before_cpu():
    reset_rules()
    FakeRules.in_check = True
    controller = GameFlowController('normal', 'beginner', FakeBoard(turn='white'), rules=FakeRules)

    update = controller.handle_player_move()

    assert update.turn_text == '後手（CPU）の手番 - 王手！'
    assert update.turn_color == 'red'
    assert update.input_enabled is False
    assert update.schedule_cpu_move is True


def test_cpu_move_refreshes_board_and_reenables_input():
    reset_rules()
    board = FakeBoard(turn='white')
    controller = GameFlowController(
        'normal',
        'advanced',
        board,
        engine=FakeEngine(move='best-move'),
        rules=FakeRules,
    )

    update = controller.handle_cpu_move()

    assert board.moved == ['best-move']
    assert update.refresh_board is True
    assert update.input_enabled is True
    assert update.turn_text == '先手（あなた）の手番'


def test_tsume_player_move_undoes_when_not_mate():
    reset_rules()
    piece = SimpleNamespace(owner='white')
    board = FakeBoard(turn='white', pieces={(0, 0): piece})
    FakeRules.moves = {(0, 0): ['legal']}
    controller = GameFlowController('tsume', 'beginner', board, rules=FakeRules)

    update = controller.handle_player_move()

    assert board.undo_called is True
    assert update.status_level == 'warning'
    assert update.status_title == '不正解'
    assert update.status_message == 'まだ詰んでいません'
    assert update.refresh_board is True


def test_next_problem_replaces_board_and_advances_index():
    reset_rules()
    next_board = FakeBoard(turn='black')
    manager = FakeTsumeManager({('expert', 1): FakeProblem(next_board)})
    controller = GameFlowController(
        'tsume',
        'expert',
        FakeBoard(turn='white'),
        tsume_manager=manager,
        current_problem_index=0,
        rules=FakeRules,
    )

    update = controller.next_problem()

    assert controller.board is next_board
    assert controller.current_problem_index == 1
    assert update.replace_board is True
    assert update.refresh_board is True
    assert update.turn_text == '先手（あなた）の手番'


def test_get_save_data_includes_tsume_problem_index():
    reset_rules()
    controller = GameFlowController(
        'tsume',
        'intermediate',
        FakeBoard(turn='black'),
        current_problem_index=3,
        rules=FakeRules,
    )

    data = controller.get_save_data()

    assert data == {
        'game_mode': 'tsume',
        'difficulty': 'intermediate',
        'board': {'turn': 'black'},
        'current_problem_index': 3,
    }