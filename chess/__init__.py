"""
check50 checks for the "Legal Chess Move Checker" problem.

Expected program: chess.c, compiling to an executable named "chess".

Expected input order (one value per line; prompt text can be anything):
    1. Piece letter: P, R, B, N, Q, or K
    2. Start column (0-7)
    3. Start row    (0-7)
    4. End column   (0-7)
    5. End row      (0-7)

Expected output: stdout must contain "Legal move" or "Illegal move".

To run locally:
    check50 dir:chess
(assuming this folder is named "chess" and sits next to the student's chess.c,
or point check50 at wherever you've placed this checks folder)
"""

import check50


@check50.check()
def exists():
    """chess.c exists"""
    check50.exists("chess.c")


@check50.check(exists)
def compiles():
    """chess.c compiles"""
    check50.c.compile("chess.c", exe_name="chess")


def _run(piece, start_col, start_row, end_col, end_row):
    """Helper: run ./chess with the five inputs, in order, prompts ignored."""
    return (
        check50.run("./chess")
        .stdin(str(piece), prompt=False)
        .stdin(str(start_col), prompt=False)
        .stdin(str(start_row), prompt=False)
        .stdin(str(end_col), prompt=False)
        .stdin(str(end_row), prompt=False)
    )


# ---------- Rook ----------

@check50.check(compiles)
def rook_legal_horizontal():
    """rook: horizontal move is legal"""
    _run("R", 0, 0, 5, 0).stdout("Legal move").exit(0)


@check50.check(compiles)
def rook_legal_vertical():
    """rook: vertical move is legal"""
    _run("R", 3, 0, 3, 7).stdout("Legal move").exit(0)


@check50.check(compiles)
def rook_illegal_diagonal():
    """rook: diagonal move is illegal"""
    _run("R", 0, 0, 3, 3).stdout("Illegal move").exit(0)


# ---------- Bishop ----------

@check50.check(compiles)
def bishop_legal_diagonal():
    """bishop: diagonal move is legal"""
    _run("B", 0, 0, 3, 3).stdout("Legal move").exit(0)


@check50.check(compiles)
def bishop_illegal_straight():
    """bishop: straight move is illegal"""
    _run("B", 0, 0, 0, 5).stdout("Illegal move").exit(0)


# ---------- Knight ----------

@check50.check(compiles)
def knight_legal_L_shape_a():
    """knight: 2-1 L-shaped move is legal"""
    _run("N", 1, 0, 2, 2).stdout("Legal move").exit(0)


@check50.check(compiles)
def knight_legal_L_shape_b():
    """knight: 1-2 L-shaped move is legal"""
    _run("N", 1, 0, 0, 2).stdout("Legal move").exit(0)


@check50.check(compiles)
def knight_illegal_straight():
    """knight: straight move is illegal"""
    _run("N", 1, 0, 1, 2).stdout("Illegal move").exit(0)


@check50.check(compiles)
def knight_illegal_diagonal():
    """knight: diagonal move is illegal"""
    _run("N", 1, 0, 3, 2).stdout("Illegal move").exit(0)


# ---------- King ----------

@check50.check(compiles)
def king_legal_one_square_orthogonal():
    """king: one square orthogonal move is legal"""
    _run("K", 4, 4, 4, 5).stdout("Legal move").exit(0)


@check50.check(compiles)
def king_legal_one_square_diagonal():
    """king: one square diagonal move is legal"""
    _run("K", 4, 4, 5, 5).stdout("Legal move").exit(0)


@check50.check(compiles)
def king_illegal_two_squares():
    """king: two square move is illegal"""
    _run("K", 4, 4, 4, 6).stdout("Illegal move").exit(0)


# ---------- Queen ----------

@check50.check(compiles)
def queen_legal_diagonal():
    """queen: diagonal move is legal"""
    _run("Q", 0, 0, 4, 4).stdout("Legal move").exit(0)


@check50.check(compiles)
def queen_legal_straight():
    """queen: straight move is legal"""
    _run("Q", 0, 0, 0, 7).stdout("Legal move").exit(0)


@check50.check(compiles)
def queen_illegal_knight_shape():
    """queen: knight-shaped move is illegal"""
    _run("Q", 0, 0, 1, 2).stdout("Illegal move").exit(0)


# ---------- Pawn ----------

@check50.check(compiles)
def pawn_legal_one_forward():
    """pawn: one square forward is legal"""
    _run("P", 4, 1, 4, 2).stdout("Legal move").exit(0)


@check50.check(compiles)
def pawn_legal_two_forward_from_start_row():
    """pawn: two squares forward from starting row (row 1) is legal"""
    _run("P", 4, 1, 4, 3).stdout("Legal move").exit(0)


@check50.check(compiles)
def pawn_illegal_two_forward_not_from_start_row():
    """pawn: two squares forward from a non-starting row is illegal"""
    _run("P", 4, 2, 4, 4).stdout("Illegal move").exit(0)


@check50.check(compiles)
def pawn_illegal_sideways():
    """pawn: sideways move is illegal"""
    _run("P", 4, 1, 5, 1).stdout("Illegal move").exit(0)


@check50.check(compiles)
def pawn_illegal_backward():
    """pawn: backward move is illegal"""
    _run("P", 4, 3, 4, 2).stdout("Illegal move").exit(0)


# ---------- Edge case ----------

@check50.check(compiles)
def no_move_is_illegal():
    """staying on the same square is illegal"""
    _run("R", 3, 3, 3, 3).stdout("Illegal move").exit(0)
