from PySide6.QtCore import Qt

from qt_app import ShogiQtWindow
from ui.qt.screens import ConfirmScreen, DifficultySelectScreen, GameScreen, ModeSelectScreen, ResultScreen


def test_qt_shell_transitions_from_mode_to_game(qtbot):
    window = ShogiQtWindow()
    qtbot.addWidget(window)

    assert isinstance(window.current_screen, ModeSelectScreen)

    qtbot.mouseClick(window.current_screen.normal_button, Qt.MouseButton.LeftButton)
    assert isinstance(window.current_screen, DifficultySelectScreen)

    qtbot.mouseClick(window.current_screen.difficulty_buttons['beginner'], Qt.MouseButton.LeftButton)
    assert isinstance(window.current_screen, ConfirmScreen)

    qtbot.mouseClick(window.current_screen.confirm_button, Qt.MouseButton.LeftButton)
    assert isinstance(window.current_screen, GameScreen)
    assert window.current_screen.info_label.text() == '通常将棋 - 初級'
    assert window.current_screen.turn_label.text() == '先手（あなた）の手番'


def test_qt_result_screen_restart_returns_to_same_mode(qtbot):
    window = ShogiQtWindow()
    qtbot.addWidget(window)

    window.show_result_screen('win', 'tsume', 'expert')
    assert isinstance(window.current_screen, ResultScreen)

    qtbot.mouseClick(window.current_screen.restart_button, Qt.MouseButton.LeftButton)

    assert isinstance(window.current_screen, GameScreen)
    assert window.current_screen.info_label.text() == '詰将棋 - 超上級'
    assert window.current_screen.turn_label.text() == '先手（あなた）の手番'