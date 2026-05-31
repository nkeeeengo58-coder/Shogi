"""PySide6ベースの画面群"""

from PySide6.QtCore import QTimer, Qt
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from ui.qt.board_widget import QtBoardWidget


DIFFICULTY_LABELS = {
    'beginner': '初級',
    'intermediate': '中級',
    'advanced': '上級',
    'expert': '超上級',
}


DIFFICULTY_DESCRIPTIONS = {
    'normal': {
        'beginner': '合法手からランダムに選択',
        'intermediate': '1〜2手読み',
        'advanced': '3〜4手読み（ミニマックス）',
        'expert': '4手以上の探索',
    },
    'tsume': {
        'beginner': '1手詰め',
        'intermediate': '3手詰め',
        'advanced': '5手詰め',
        'expert': '7手詰め以上',
    },
}


def _set_screen_style(widget):
    widget.setStyleSheet(
        'QWidget { background: #f0f0f0; }'
        'QLabel[role="title"] { font-size: 28px; font-weight: 700; }'
        'QPushButton { font-size: 16px; padding: 12px 18px; min-width: 180px; }'
    )


class ModeSelectScreen(QWidget):
    def __init__(self, app_window):
        super().__init__()
        self.app_window = app_window
        self.normal_button = QPushButton('通常将棋モード')
        self.tsume_button = QPushButton('詰将棋モード')
        self._build_ui()

    def _build_ui(self):
        _set_screen_style(self)
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(24)

        title = QLabel('将棋ゲーム')
        title.setProperty('role', 'title')
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        self.normal_button.clicked.connect(lambda: self.app_window.show_difficulty_select('normal'))
        self.tsume_button.clicked.connect(lambda: self.app_window.show_difficulty_select('tsume'))
        layout.addWidget(self.normal_button, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.tsume_button, alignment=Qt.AlignmentFlag.AlignCenter)


class DifficultySelectScreen(QWidget):
    def __init__(self, app_window, mode):
        super().__init__()
        self.app_window = app_window
        self.mode = mode
        self.difficulty_buttons = {}
        self.back_button = QPushButton('戻る')
        self._build_ui()

    def _build_ui(self):
        _set_screen_style(self)
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setSpacing(18)

        mode_text = '通常将棋' if self.mode == 'normal' else '詰将棋'
        title = QLabel(f'{mode_text} - 難易度選択')
        title.setProperty('role', 'title')
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        for difficulty in ['beginner', 'intermediate', 'advanced', 'expert']:
            row = QVBoxLayout()
            button = QPushButton(DIFFICULTY_LABELS[difficulty])
            description = QLabel(DIFFICULTY_DESCRIPTIONS[self.mode][difficulty])
            description.setAlignment(Qt.AlignmentFlag.AlignCenter)
            button.clicked.connect(lambda checked=False, value=difficulty: self.app_window.show_confirm(self.mode, value))
            row.addWidget(button, alignment=Qt.AlignmentFlag.AlignCenter)
            row.addWidget(description)
            layout.addLayout(row)
            self.difficulty_buttons[difficulty] = button

        self.back_button.clicked.connect(self.app_window.show_mode_select)
        layout.addWidget(self.back_button, alignment=Qt.AlignmentFlag.AlignCenter)


class ConfirmScreen(QWidget):
    def __init__(self, app_window, mode, difficulty):
        super().__init__()
        self.app_window = app_window
        self.mode = mode
        self.difficulty = difficulty
        self.confirm_button = QPushButton('はい')
        self.cancel_button = QPushButton('いいえ')
        self._build_ui()

    def _build_ui(self):
        _set_screen_style(self)
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(18)

        mode_text = '通常将棋' if self.mode == 'normal' else '詰将棋'
        title = QLabel('ゲーム設定')
        title.setProperty('role', 'title')
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        layout.addWidget(QLabel(f'モード: {mode_text}'), alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(QLabel(f'難易度: {DIFFICULTY_LABELS[self.difficulty]}'), alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(QLabel('ゲームを開始しますか？'), alignment=Qt.AlignmentFlag.AlignCenter)

        buttons = QHBoxLayout()
        self.confirm_button.clicked.connect(self.app_window.start_game)
        self.cancel_button.clicked.connect(lambda: self.app_window.show_difficulty_select(self.mode))
        buttons.addWidget(self.confirm_button)
        buttons.addWidget(self.cancel_button)
        layout.addLayout(buttons)


class GameScreen(QWidget):
    def __init__(self, app_window, controller):
        super().__init__()
        self.app_window = app_window
        self.controller = controller
        self.info_label = QLabel()
        self.turn_label = QLabel()
        self.board_widget = QtBoardWidget(controller.board, app_window.config, self)
        self.action_button = QPushButton()
        self.menu_button = QPushButton('メニューに戻る')
        self._build_ui()

    def _build_ui(self):
        _set_screen_style(self)
        layout = QVBoxLayout(self)
        layout.setSpacing(18)

        mode_text = '通常将棋' if self.controller.game_mode == 'normal' else '詰将棋'
        difficulty_text = DIFFICULTY_LABELS[self.controller.difficulty]
        self.info_label.setText(f'{mode_text} - {difficulty_text}')
        self.turn_label.setText(self.controller.get_turn_text())
        self.info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.turn_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title = QLabel('対局中')
        title.setProperty('role', 'title')
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        header = QVBoxLayout()
        header.addWidget(title)
        header.addWidget(self.info_label)
        header.addWidget(self.turn_label)
        layout.addLayout(header)

        self.board_widget.movePlayed.connect(self.on_move)
        layout.addWidget(self.board_widget, alignment=Qt.AlignmentFlag.AlignCenter)

        button_row = QHBoxLayout()
        if self.controller.game_mode == 'normal':
            self.action_button.setText('投了')
            self.action_button.clicked.connect(self.resign)
        else:
            self.action_button.setText('次の問題')
            self.action_button.clicked.connect(self.next_problem)
        self.menu_button.clicked.connect(self.back_to_menu)
        button_row.addWidget(self.action_button)
        button_row.addWidget(self.menu_button)
        layout.addLayout(button_row)

        self._apply_update(self.controller.get_initial_update())

    def _apply_update(self, update):
        self.board_widget.set_board(self.controller.board)

        if update.replace_board:
            self.board_widget.set_board(self.controller.board)

        if update.refresh_board:
            self.board_widget.refresh()

        if update.turn_text is not None:
            self.turn_label.setText(update.turn_text)
            self.turn_label.setStyleSheet(f'color: {update.turn_color};')

        if update.input_enabled is not None:
            self.board_widget.set_enabled(update.input_enabled)

        if update.status_level:
            if update.status_level == 'info':
                QMessageBox.information(self, update.status_title, update.status_message)
            elif update.status_level == 'warning':
                QMessageBox.warning(self, update.status_title, update.status_message)
            elif update.status_level == 'error':
                QMessageBox.critical(self, update.status_title, update.status_message)

        if update.result_type:
            self.app_window.show_result_screen(update.result_type, self.controller.game_mode, self.controller.difficulty)
            return

        if update.schedule_cpu_move:
            QTimer.singleShot(500, self.cpu_move)

    def on_move(self, move):
        self._apply_update(self.controller.handle_player_move())

    def cpu_move(self):
        try:
            self._apply_update(self.controller.handle_cpu_move())
        except Exception as error:
            QMessageBox.critical(self, 'エラー', f'CPU処理中にエラーが発生しました:\n{error}')
            self.board_widget.set_enabled(True)

    def resign(self):
        result = QMessageBox.question(
            self,
            '投了',
            '投了しますか？',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if result == QMessageBox.StandardButton.Yes:
            self.app_window.show_result_screen('lose', self.controller.game_mode, self.controller.difficulty)

    def next_problem(self):
        self._apply_update(self.controller.next_problem())

    def back_to_menu(self):
        result = QMessageBox.question(
            self,
            '確認',
            'ゲームを終了してメニューに戻りますか？',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if result == QMessageBox.StandardButton.Yes:
            self.app_window.show_mode_select()


class ResultScreen(QWidget):
    def __init__(self, app_window, result_type, game_mode, difficulty):
        super().__init__()
        self.app_window = app_window
        self.result_type = result_type
        self.game_mode = game_mode
        self.difficulty = difficulty
        self.restart_button = QPushButton('もう一度同じモードでゲームする')
        self.mode_select_button = QPushButton('他のモードでゲームする')
        self._build_ui()

    def _build_ui(self):
        _set_screen_style(self)
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(18)

        title = QLabel('勝利' if self.result_type == 'win' else '敗北')
        title.setProperty('role', 'title')
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        message = QLabel('対局が終了しました。次の操作を選択してください。')
        message.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.restart_button.clicked.connect(self._restart_same_mode)
        self.mode_select_button.clicked.connect(self.app_window.show_mode_select)

        layout.addWidget(title)
        layout.addWidget(message)
        layout.addWidget(self.restart_button, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.mode_select_button, alignment=Qt.AlignmentFlag.AlignCenter)

    def _restart_same_mode(self):
        self.app_window.game_mode = self.game_mode
        self.app_window.difficulty = self.difficulty
        self.app_window.start_game()
