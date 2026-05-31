from ui.board_layout import BOARD_PADDING, get_cell_center, get_cell_rect, get_layout_metrics


def test_layout_metrics_match_existing_board_dimensions():
    metrics = get_layout_metrics()

    assert metrics.board_width == 540
    assert metrics.board_height == 498
    assert round(metrics.cell_width, 2) == 46.31
    assert round(metrics.cell_height, 2) == 49.82
    assert metrics.piece_size == 40
    assert metrics.canvas_width == metrics.board_width + BOARD_PADDING * 2 + 200
    assert metrics.canvas_height == metrics.board_height + BOARD_PADDING * 2


def test_cell_helpers_return_expected_positions():
    metrics = get_layout_metrics()

    top_left = get_cell_rect(metrics, 0, 0)
    bottom_right = get_cell_rect(metrics, 8, 8)
    center = get_cell_center(metrics, 4, 4)

    assert tuple(round(value, 2) for value in top_left) == (94.99, 63.99, 141.3, 113.81)
    assert tuple(round(value, 2) for value in bottom_right) == (465.47, 462.54, 511.78, 512.36)
    assert tuple(round(value, 2) for value in center) == (303.38, 288.17)