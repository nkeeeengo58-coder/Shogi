"""PySide6ベースの並行UIシェル"""

import json
import os
import sys

from PySide6.QtWidgets import QApplication, QMainWindow

from game.board import Board
from game.engine import Engine
from game.tsume import TsumeManager
from ui.game_flow import GameFlowController
from ui.qt.screens import ConfirmScreen, DifficultySelectScreen, GameScreen, ModeSelectScreen, ResultScreen


class ShogiQtWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.config = self.load_config()
        self.current_screen = None
        self.current_controller = None
        self.game_mode = None
        self.difficulty = None

        self.setWindowTitle('将棋ゲーム')
        self.resize(1024, 768)
        self.show_mode_select()

    def load_config(self):
        config_path = os.path.join(os.path.expanduser('~'), '.shogi_game', 'config.json')
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r', encoding='utf-8') as handle:
                    return json.load(handle)
            except Exception:
                pass

        return {
            'board_theme': 'default',
            'piece_set': 'default',
            'font_size': 12,
            'sound_enabled': True,
            'highlight_opacity': 0.5,
        }

    def _set_screen(self, widget):
        self.current_screen = widget
        self.setCentralWidget(widget)

    def show_mode_select(self):
        self._set_screen(ModeSelectScreen(self))

    def show_difficulty_select(self, mode):
        self.game_mode = mode
        self._set_screen(DifficultySelectScreen(self, mode))

    def show_confirm(self, mode, difficulty):
        self.game_mode = mode
        self.difficulty = difficulty
        self._set_screen(ConfirmScreen(self, mode, difficulty))

    def start_game(self):
        controller = self._build_controller()
        self.current_controller = controller
        self._set_screen(GameScreen(self, controller))

    def show_result_screen(self, result_type, game_mode=None, difficulty=None):
        if game_mode is not None:
            self.game_mode = game_mode
        if difficulty is not None:
            self.difficulty = difficulty
        self._set_screen(ResultScreen(self, result_type, self.game_mode, self.difficulty))

    def _build_controller(self):
        board = Board()
        engine = None
        tsume_manager = None
        current_problem = None

        if self.game_mode == 'normal':
            board.initialize_normal_game()
            engine = Engine(self.difficulty)
        elif self.game_mode == 'tsume':
            tsume_manager = TsumeManager()
            current_problem = tsume_manager.get_problem(self.difficulty, 0)
            if current_problem is not None:
                board = current_problem.get_board()

        return GameFlowController(
            game_mode=self.game_mode,
            difficulty=self.difficulty,
            board=board,
            engine=engine,
            tsume_manager=tsume_manager,
            current_problem=current_problem,
            current_problem_index=0,
        )


def main():
    application = QApplication.instance() or QApplication(sys.argv)
    window = ShogiQtWindow()
    window.show()
    return application.exec()


if __name__ == '__main__':
    raise SystemExit(main())
