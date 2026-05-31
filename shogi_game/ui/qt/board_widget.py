"""PySide6ベースの盤面ウィジェット"""

import os

from PySide6.QtCore import QPointF, QRectF, Qt, Signal
from PySide6.QtGui import QColor, QFont, QPainter, QPen, QPixmap
from PySide6.QtWidgets import QMessageBox, QSizePolicy, QWidget

from game.piece import Piece
from game.rules import Rules
from ui.board_layout import BOARD_PADDING, get_cell_center, get_cell_rect, get_layout_metrics


PIECE_FILE_MAP = {
    'pawn': '駒_歩兵.png',
    'lance': '駒_香車.png',
    'knight': '駒_桂馬.png',
    'silver': '駒_銀将.png',
    'gold': '駒_金将.png',
    'bishop': '駒_角行.png',
    'rook': '駒_飛車.png',
    'king': '駒_玉将.png',
    'promoted_pawn': '駒_成_と金.png',
    'promoted_lance': '駒_成_成香.png',
    'promoted_knight': '駒_成_成桂.png',
    'promoted_silver': '駒_成_成銀.png',
    'promoted_bishop': '駒_成_龍馬.png',
    'promoted_rook': '駒_成_竜王.png',
}


class QtBoardWidget(QWidget):
    movePlayed = Signal(object)

    def __init__(self, board, config, parent=None):
        super().__init__(parent)
        self.board = board
        self.config = config
        self.enabled = True
        self.selected_pos = None
        self.selected_piece_type = None
        self.legal_moves = []

        self.layout_metrics = get_layout_metrics()
        self.board_width = self.layout_metrics.board_width
        self.board_height = self.layout_metrics.board_height
        self.grid_left = self.layout_metrics.grid_left
        self.grid_top = self.layout_metrics.grid_top
        self.grid_right = self.layout_metrics.grid_right
        self.grid_bottom = self.layout_metrics.grid_bottom
        self.cell_width = self.layout_metrics.cell_width
        self.cell_height = self.layout_metrics.cell_height

        self.theme_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'assets', 'pieces')
        self.board_theme_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'assets', 'board')
        self.board_pixmap = QPixmap()
        self.piece_pixmaps = {}
        self._load_images()

        self.setMinimumSize(self.layout_metrics.canvas_width, self.layout_metrics.canvas_height)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

    def _load_images(self):
        board_path = os.path.join(self.board_theme_path, '盤面_雅.png')
        if os.path.exists(board_path):
            self.board_pixmap = QPixmap(board_path).scaled(
                self.board_width,
                self.board_height,
                Qt.AspectRatioMode.IgnoreAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )

        piece_size = self.layout_metrics.piece_size
        captured_piece_size = 40

        for piece_type, filename in PIECE_FILE_MAP.items():
            path = os.path.join(self.theme_path, filename)
            if not os.path.exists(path):
                self.piece_pixmaps[f'{piece_type}_black'] = QPixmap()
                self.piece_pixmaps[f'{piece_type}_white'] = QPixmap()
                self.piece_pixmaps[f'{piece_type}_captured'] = QPixmap()
                continue

            pixmap = QPixmap(path)
            self.piece_pixmaps[f'{piece_type}_black'] = pixmap.scaled(
                piece_size,
                piece_size,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
            self.piece_pixmaps[f'{piece_type}_white'] = pixmap.transformed(
                self._rotation_transform()
            ).scaled(
                piece_size,
                piece_size,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
            self.piece_pixmaps[f'{piece_type}_captured'] = pixmap.scaled(
                captured_piece_size,
                captured_piece_size,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )

    @staticmethod
    def _rotation_transform():
        from PySide6.QtGui import QTransform

        transform = QTransform()
        transform.rotate(180)
        return transform

    def set_board(self, board):
        self.board = board
        self.selected_pos = None
        self.selected_piece_type = None
        self.legal_moves = []
        self.update()

    def set_enabled(self, enabled):
        self.enabled = enabled
        if not enabled:
            self.selected_pos = None
            self.selected_piece_type = None
            self.legal_moves = []
        self.update()

    def refresh(self):
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.fillRect(self.rect(), QColor('#f5deb3'))

        self._draw_board(painter)
        self._draw_pieces(painter)
        self._draw_captured_pieces(painter)
        if self.legal_moves:
            self._draw_legal_moves(painter)
        if self.board.last_move:
            self._draw_last_move(painter)

    def _draw_board(self, painter):
        if not self.board_pixmap.isNull():
            painter.drawPixmap(BOARD_PADDING, BOARD_PADDING, self.board_pixmap)
        else:
            painter.setPen(QPen(QColor('#8b4513'), 3))
            painter.setBrush(QColor('#daa520'))
            painter.drawRect(QRectF(self.grid_left, self.grid_top, self.grid_right - self.grid_left, self.grid_bottom - self.grid_top))
            painter.setPen(QPen(QColor('#8b4513'), 1))
            for index in range(10):
                x = self.grid_left + index * self.cell_width
                y = self.grid_top + index * self.cell_height
                painter.drawLine(QPointF(x, self.grid_top), QPointF(x, self.grid_bottom))
                painter.drawLine(QPointF(self.grid_left, y), QPointF(self.grid_right, y))

        font = QFont()
        font.setPointSize(12)
        painter.setFont(font)
        row_labels = ['一', '二', '三', '四', '五', '六', '七', '八', '九']
        for index in range(9):
            x, _ = get_cell_center(self.layout_metrics, 0, index)
            painter.drawText(QRectF(x - 10, self.grid_top - 28, 20, 20), Qt.AlignmentFlag.AlignCenter, str(9 - index))
            _, y = get_cell_center(self.layout_metrics, index, 0)
            painter.drawText(QRectF(self.grid_right + 8, y - 10, 20, 20), Qt.AlignmentFlag.AlignCenter, row_labels[index])

    def _draw_pieces(self, painter):
        for row in range(9):
            for col in range(9):
                piece = self.board.get_piece(row, col)
                if piece:
                    self._draw_piece(painter, row, col, piece)

        if self.selected_pos:
            row, col = self.selected_pos
            x1, y1, x2, y2 = get_cell_rect(self.layout_metrics, row, col)
            painter.setPen(QPen(QColor('blue'), 3))
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.drawRect(QRectF(x1 + 2, y1 + 2, x2 - x1 - 4, y2 - y1 - 4))

    def _draw_piece(self, painter, row, col, piece, x_offset=0, y_offset=0):
        x, y = get_cell_center(self.layout_metrics, row, col)
        x += x_offset
        y += y_offset

        pixmap = self.piece_pixmaps.get(f'{piece.piece_type}_{piece.owner}')
        if pixmap and not pixmap.isNull():
            painter.drawPixmap(int(x - pixmap.width() / 2), int(y - pixmap.height() / 2), pixmap)
            return

        size = 22
        points = [
            QPointF(x, y - size),
            QPointF(x + size, y - size // 2),
            QPointF(x + size, y + size),
            QPointF(x - size, y + size),
            QPointF(x - size, y - size // 2),
        ]
        painter.setPen(QPen(Qt.GlobalColor.black, 1))
        painter.setBrush(QColor('#f5f5dc' if piece.owner == 'black' else '#696969'))
        painter.drawPolygon(points)
        painter.setPen(QColor('black' if piece.owner == 'black' else 'white'))
        font = QFont()
        font.setPointSize(18)
        font.setBold(True)
        painter.setFont(font)
        painter.drawText(QRectF(x - 18, y - 18, 36, 36), Qt.AlignmentFlag.AlignCenter, piece.get_name())

    def _draw_captured_pieces(self, painter):
        x_base = BOARD_PADDING + self.board_width + 30
        y_black = self.grid_top + self.cell_height * 7
        y_white = self.grid_top + self.cell_height
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        painter.setFont(font)
        painter.setPen(QColor('black'))
        painter.drawText(QRectF(x_base - 20, y_black - 45, 110, 20), Qt.AlignmentFlag.AlignLeft, '先手の持ち駒')
        painter.drawText(QRectF(x_base - 20, y_white - 45, 110, 20), Qt.AlignmentFlag.AlignLeft, '後手の持ち駒')
        self._draw_captured_pieces_for_player(painter, 'black', x_base, y_black)
        self._draw_captured_pieces_for_player(painter, 'white', x_base, y_white)

    def _draw_captured_pieces_for_player(self, painter, player, x_base, y_base):
        piece_counts = {}
        for piece in self.board.captured_pieces[player]:
            base_type = piece.get_base_type()
            piece_counts[base_type] = piece_counts.get(base_type, 0) + 1

        y_offset = 0
        for piece_type, count in piece_counts.items():
            piece = Piece(piece_type, player)
            x = x_base + 20
            y = y_base + y_offset
            if self.selected_piece_type == piece_type and player == self.board.turn:
                painter.setPen(QPen(QColor('blue'), 3))
                painter.setBrush(Qt.BrushStyle.NoBrush)
                painter.drawRect(QRectF(x - 25, y - 25, 50, 50))

            pixmap = self.piece_pixmaps.get(f'{piece_type}_captured')
            if pixmap and not pixmap.isNull():
                painter.drawPixmap(int(x - pixmap.width() / 2), int(y - pixmap.height() / 2), pixmap)
            else:
                self._draw_piece(painter, 0, 0, piece, x - get_cell_center(self.layout_metrics, 0, 0)[0], y - get_cell_center(self.layout_metrics, 0, 0)[1])

            if count > 1:
                painter.setPen(QColor('black'))
                font = QFont()
                font.setPointSize(12)
                painter.setFont(font)
                painter.drawText(QRectF(x + 25, y - 12, 40, 24), Qt.AlignmentFlag.AlignLeft, f'×{count}')
            y_offset += 45

    def _draw_legal_moves(self, painter):
        alpha = int(255 * self.config.get('highlight_opacity', 0.5))
        pen = QPen(QColor(0, 128, 0), 2)
        painter.setPen(pen)
        painter.setBrush(QColor(0, 128, 0, alpha // 3))
        for move in self.legal_moves:
            row, col = move.to_pos
            x1, y1, x2, y2 = get_cell_rect(self.layout_metrics, row, col)
            painter.drawRect(QRectF(x1 + 5, y1 + 5, x2 - x1 - 10, y2 - y1 - 10))

    def _draw_last_move(self, painter):
        pen = QPen(QColor('orange'), 2)
        painter.setPen(pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        move = self.board.last_move
        if move and not move.is_drop:
            from_row, from_col = move.from_pos
            x1, y1, x2, y2 = get_cell_rect(self.layout_metrics, from_row, from_col)
            painter.drawRect(QRectF(x1 + 5, y1 + 5, x2 - x1 - 10, y2 - y1 - 10))
        to_row, to_col = move.to_pos
        x1, y1, x2, y2 = get_cell_rect(self.layout_metrics, to_row, to_col)
        painter.drawRect(QRectF(x1 + 5, y1 + 5, x2 - x1 - 10, y2 - y1 - 10))

    def mousePressEvent(self, event):
        if not self.enabled or event.button() != Qt.MouseButton.LeftButton:
            return

        x = event.position().x()
        y = event.position().y()
        if self.grid_left <= x <= self.grid_right and self.grid_top <= y <= self.grid_bottom:
            col = min(8, int((x - self.grid_left) // self.cell_width))
            row = min(8, int((y - self.grid_top) // self.cell_height))
            self._on_board_click(row, col)
        else:
            self._on_captured_click(x, y)

    def _on_board_click(self, row, col):
        if self.selected_piece_type:
            for move in self.legal_moves:
                if move.to_pos == (row, col):
                    self._execute_move(move)
                    self.selected_piece_type = None
                    self.legal_moves = []
                    self.update()
                    return
            self.selected_piece_type = None
            self.legal_moves = []
            self.update()
            return

        if self.selected_pos:
            for move in self.legal_moves:
                if move.to_pos == (row, col):
                    move = self._choose_promotion_if_needed(row, col, move)
                    self._execute_move(move)
                    self.selected_pos = None
                    self.legal_moves = []
                    self.update()
                    return

            piece = self.board.get_piece(row, col)
            if piece and piece.owner == self.board.turn:
                self.selected_pos = (row, col)
                self.legal_moves = Rules.get_piece_moves(self.board, row, col)
            else:
                self.selected_pos = None
                self.legal_moves = []
            self.update()
            return

        piece = self.board.get_piece(row, col)
        if piece and piece.owner == self.board.turn:
            self.selected_pos = (row, col)
            self.legal_moves = Rules.get_piece_moves(self.board, row, col)
            self.update()

    def _choose_promotion_if_needed(self, row, col, default_move):
        if not default_move.piece.can_promote():
            return default_move
        promote_moves = [move for move in self.legal_moves if move.to_pos == (row, col) and move.is_promotion]
        normal_moves = [move for move in self.legal_moves if move.to_pos == (row, col) and not move.is_promotion]
        if not (promote_moves and normal_moves):
            return default_move

        result = QMessageBox.question(
            self,
            '成り',
            '成りますか？',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.Yes,
        )
        return promote_moves[0] if result == QMessageBox.StandardButton.Yes else normal_moves[0]

    def _on_captured_click(self, x, y):
        x_base = BOARD_PADDING + self.board_width + 30
        y_black = self.grid_top + self.cell_height * 7
        y_white = self.grid_top + self.cell_height

        if self.board.turn == 'black':
            y_base = y_black
            player = 'black'
        else:
            y_base = y_white
            player = 'white'

        piece_counts = {}
        for piece in self.board.captured_pieces[player]:
            base_type = piece.get_base_type()
            piece_counts[base_type] = piece_counts.get(base_type, 0) + 1

        piece_x = x_base + 20
        y_offset = 0
        for piece_type in piece_counts.keys():
            piece_y = y_base + y_offset
            if piece_x - 25 <= x <= piece_x + 25 and piece_y - 25 <= y <= piece_y + 25:
                self.selected_piece_type = piece_type
                self.selected_pos = None
                self.legal_moves = Rules.get_drop_moves(self.board, piece_type)
                self.update()
                return
            y_offset += 45

    def _execute_move(self, move):
        self.board.move_piece(move)
        self.movePlayed.emit(move)
