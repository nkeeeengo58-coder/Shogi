"""PySide6向け盤面ビュー（プレースホルダー）"""
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QWidget


class BoardView(QWidget):
    def __init__(self, parent=None, board=None, config=None, on_move_callback=None):
        super().__init__(parent)
        self.board = board
        self.config = config or {}
        self.on_move_callback = on_move_callback
        self.enabled = True

    def set_board(self, board):
        self.board = board
        self.update()

    def set_enabled(self, enabled):
        self.enabled = enabled

    def paintEvent(self, _event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), Qt.lightGray)
        painter.drawText(self.rect(), Qt.AlignCenter, "BoardView (PySide6)")
