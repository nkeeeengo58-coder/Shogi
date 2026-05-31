"""盤面レイアウト計算"""

from dataclasses import dataclass


BOARD_PADDING = 40
BOARD_IMAGE_WIDTH = 1306
BOARD_IMAGE_HEIGHT = 1204
BOARD_RENDER_WIDTH = 540
BOARD_GRID_LEFT = 133
BOARD_GRID_TOP = 58
BOARD_GRID_RIGHT = 1141
BOARD_GRID_BOTTOM = 1142


@dataclass(frozen=True)
class BoardLayoutMetrics:
    board_width: int
    board_height: int
    grid_left: float
    grid_top: float
    grid_right: float
    grid_bottom: float
    cell_width: float
    cell_height: float
    piece_size: int
    canvas_width: int
    canvas_height: int


def get_layout_metrics(side_panel_width=200):
    """盤面画像から実際のマス配置情報を計算"""
    board_width = BOARD_RENDER_WIDTH
    board_height = round(BOARD_IMAGE_HEIGHT * board_width / BOARD_IMAGE_WIDTH)
    scale_x = board_width / BOARD_IMAGE_WIDTH
    scale_y = board_height / BOARD_IMAGE_HEIGHT

    grid_left = BOARD_PADDING + BOARD_GRID_LEFT * scale_x
    grid_top = BOARD_PADDING + BOARD_GRID_TOP * scale_y
    grid_right = BOARD_PADDING + BOARD_GRID_RIGHT * scale_x
    grid_bottom = BOARD_PADDING + BOARD_GRID_BOTTOM * scale_y
    cell_width = (grid_right - grid_left) / 9
    cell_height = (grid_bottom - grid_top) / 9
    piece_size = max(24, int(min(cell_width, cell_height)) - 6)

    return BoardLayoutMetrics(
        board_width=board_width,
        board_height=board_height,
        grid_left=grid_left,
        grid_top=grid_top,
        grid_right=grid_right,
        grid_bottom=grid_bottom,
        cell_width=cell_width,
        cell_height=cell_height,
        piece_size=piece_size,
        canvas_width=board_width + BOARD_PADDING * 2 + side_panel_width,
        canvas_height=board_height + BOARD_PADDING * 2,
    )


def get_cell_rect(metrics, row, col):
    """マスの矩形を返す"""
    x1 = metrics.grid_left + col * metrics.cell_width
    y1 = metrics.grid_top + row * metrics.cell_height
    x2 = x1 + metrics.cell_width
    y2 = y1 + metrics.cell_height
    return x1, y1, x2, y2


def get_cell_center(metrics, row, col):
    """マスの中心座標を返す"""
    x1, y1, x2, y2 = get_cell_rect(metrics, row, col)
    return (x1 + x2) / 2, (y1 + y2) / 2
