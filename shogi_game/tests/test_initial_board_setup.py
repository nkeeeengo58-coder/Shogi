from game.board import Board
from game.piece import PieceType


def test_initial_rook_bishop_positions():
    """飛車と角の初期配置が入れ替わっていないことを検証する。"""
    board = Board()
    board.initialize_normal_game()

    # 後手（white）
    white_rook = board.get_piece(1, 1)
    white_bishop = board.get_piece(1, 7)

    assert white_rook is not None
    assert white_rook.piece_type == PieceType.ROOK
    assert white_rook.owner == 'white'

    assert white_bishop is not None
    assert white_bishop.piece_type == PieceType.BISHOP
    assert white_bishop.owner == 'white'

    # 先手（black）
    black_bishop = board.get_piece(7, 1)
    black_rook = board.get_piece(7, 7)

    assert black_bishop is not None
    assert black_bishop.piece_type == PieceType.BISHOP
    assert black_bishop.owner == 'black'

    assert black_rook is not None
    assert black_rook.piece_type == PieceType.ROOK
    assert black_rook.owner == 'black'

    # 逆配置になっていないことを明示チェック
    assert board.get_piece(1, 1).piece_type != PieceType.BISHOP
    assert board.get_piece(1, 7).piece_type != PieceType.ROOK
    assert board.get_piece(7, 1).piece_type != PieceType.ROOK
    assert board.get_piece(7, 7).piece_type != PieceType.BISHOP
