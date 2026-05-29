"""
将棋ゲーム - アプリケーションメインクラス
"""
import json
import os
import sys

from PySide6.QtWidgets import QApplication, QMainWindow, QWidget

from game.save_load import SaveLoad
from ui.customize import CustomizeDialog
from ui.menu import MenuBar
from ui.screens import (
    ConfirmScreen,
    DifficultySelectScreen,
    GameScreen,
    ModeSelectScreen,
    ResultScreen,
)


class ShogiApp:
    """将棋ゲームのメインアプリケーションクラス"""

    def __init__(self):
        self.qt_app = QApplication.instance() or QApplication(sys.argv)
        self.root = QMainWindow()
        self.root.setWindowTitle("将棋ゲーム")
        self.root.resize(1024, 768)

        self.config = self.load_config()
        self.current_screen = None
        self.game_mode = None
        self.difficulty = None

        self.menu_bar = MenuBar(self.root, self)
        self.show_mode_select()

    def load_config(self):
        config_path = os.path.join(os.path.expanduser("~"), ".shogi_game", "config.json")
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                pass
        return {
            'board_theme': 'default',
            'piece_set': 'default',
            'font_size': 12,
            'sound_enabled': True,
            'highlight_opacity': 0.5,
        }

    def save_config(self):
        config_dir = os.path.join(os.path.expanduser("~"), ".shogi_game")
        os.makedirs(config_dir, exist_ok=True)
        config_path = os.path.join(config_dir, "config.json")
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, ensure_ascii=False, indent=2)

    def clear_screen(self):
        if self.current_screen:
            self.current_screen.deleteLater()
            self.current_screen = None

    def _set_screen(self, screen: QWidget):
        self.clear_screen()
        self.current_screen = screen
        self.root.setCentralWidget(screen)

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
        self._set_screen(GameScreen(self, self.game_mode, self.difficulty))

    def show_result_screen(self, result_type, game_mode=None, difficulty=None):
        if game_mode is not None:
            self.game_mode = game_mode
        if difficulty is not None:
            self.difficulty = difficulty
        self._set_screen(ResultScreen(self, result_type, self.game_mode, self.difficulty))

    def new_game(self):
        self.show_mode_select()

    def save_game(self):
        if self.current_screen and hasattr(self.current_screen, 'get_save_data'):
            save_data = self.current_screen.get_save_data()
            SaveLoad.save_game(save_data)
            self.menu_bar.show_info("保存", "ゲームを保存しました")
        else:
            self.menu_bar.show_warning("保存", "保存できるゲームがありません")

    def load_game(self):
        save_data = SaveLoad.load_game(parent=self.root)
        if save_data:
            self.game_mode = save_data.get('game_mode')
            self.difficulty = save_data.get('difficulty')
            self._set_screen(GameScreen(self, self.game_mode, self.difficulty, save_data))
        else:
            self.menu_bar.show_warning("読み込み", "保存データが見つかりません")

    def show_customize(self):
        CustomizeDialog(self.root, self).exec()

    def run(self):
        self.root.show()
        return self.qt_app.exec()
