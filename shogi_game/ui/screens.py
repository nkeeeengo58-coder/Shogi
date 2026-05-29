"""PySide6ベースの画面クラス"""
from functools import partial
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class ModeSelectScreen(QWidget):
    def __init__(self, app):
        super().__init__()
        self.app = app
        layout = QVBoxLayout(self)
        title = QLabel("将棋ゲーム")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 36px; font-weight: bold;")
        layout.addWidget(title)

        normal_btn = QPushButton("通常将棋モード")
        normal_btn.clicked.connect(lambda: self.app.show_difficulty_select('normal'))
        tsume_btn = QPushButton("詰将棋モード")
        tsume_btn.clicked.connect(lambda: self.app.show_difficulty_select('tsume'))
        layout.addWidget(normal_btn)
        layout.addWidget(tsume_btn)
        layout.addStretch()


class DifficultySelectScreen(QWidget):
    def __init__(self, app, mode):
        super().__init__()
        self.app = app
        mode_text = "通常将棋" if mode == 'normal' else "詰将棋"
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel(f"{mode_text} - 難易度選択"))

        for difficulty, text in [
            ('beginner', '初級'),
            ('intermediate', '中級'),
            ('advanced', '上級'),
            ('expert', '超上級'),
        ]:
            btn = QPushButton(text)
            btn.clicked.connect(partial(self.app.show_confirm, mode, difficulty))
            layout.addWidget(btn)

        back_btn = QPushButton("戻る")
        back_btn.clicked.connect(self.app.show_mode_select)
        layout.addWidget(back_btn)


class ConfirmScreen(QWidget):
    def __init__(self, app, mode, difficulty):
        super().__init__()
        self.app = app
        mode_text = "通常将棋" if mode == 'normal' else "詰将棋"
        difficulty_map = {
            'beginner': '初級',
            'intermediate': '中級',
            'advanced': '上級',
            'expert': '超上級',
        }
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel(f"モード: {mode_text}"))
        layout.addWidget(QLabel(f"難易度: {difficulty_map.get(difficulty, difficulty)}"))

        buttons = QHBoxLayout()
        yes_btn = QPushButton("開始")
        yes_btn.clicked.connect(self.app.start_game)
        no_btn = QPushButton("戻る")
        no_btn.clicked.connect(lambda: self.app.show_difficulty_select(mode))
        buttons.addWidget(yes_btn)
        buttons.addWidget(no_btn)
        layout.addLayout(buttons)


class GameScreen(QWidget):
    def __init__(self, app, game_mode, difficulty, save_data=None):
        super().__init__()
        self.app = app
        self.game_mode = game_mode
        self.difficulty = difficulty
        self.save_data = save_data or {}

        layout = QVBoxLayout(self)
        mode_text = "通常将棋" if game_mode == 'normal' else "詰将棋"
        layout.addWidget(QLabel(f"{mode_text} / 難易度: {difficulty}"))

        placeholder = QFrame()
        placeholder.setFrameShape(QFrame.StyledPanel)
        placeholder_layout = QVBoxLayout(placeholder)
        placeholder_label = QLabel("PySide6移行版のゲーム画面")
        placeholder_label.setAlignment(Qt.AlignCenter)
        placeholder_layout.addWidget(placeholder_label)
        layout.addWidget(placeholder)

        finish_btn = QPushButton("メニューに戻る")
        finish_btn.clicked.connect(self.app.show_mode_select)
        layout.addWidget(finish_btn)

    def get_save_data(self):
        data = dict(self.save_data)
        data['game_mode'] = self.game_mode
        data['difficulty'] = self.difficulty
        return data


class ResultScreen(QWidget):
    def __init__(self, app, result_type, game_mode, difficulty):
        super().__init__()
        self.app = app
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel(f"結果: {result_type}"))
        layout.addWidget(QLabel(f"モード: {game_mode}, 難易度: {difficulty}"))

        buttons = QHBoxLayout()
        retry_btn = QPushButton("もう一度")
        retry_btn.clicked.connect(self.app.start_game)
        menu_btn = QPushButton("メニューへ")
        menu_btn.clicked.connect(self.app.show_mode_select)
        buttons.addWidget(retry_btn)
        buttons.addWidget(menu_btn)
        layout.addLayout(buttons)
