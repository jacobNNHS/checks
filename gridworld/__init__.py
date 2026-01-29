import check50
import check50.c

@check50.check()
def exists():
    """gridworld.c exists"""
    check50.exists("gridworld.c")

@check50.check(exists)
def compiles():
    """gridworld.c compiles"""
    check50.c.compile("gridworld.c")

@check50.check(compiles)
def test_init_display():
    """initializes and displays empty grid"""
    check50.run("./gridworld").stdin("display\nquit").stdout(
        r"\. \. \. \. \. \. \. \. \. \.\n"
        r"\. \. \. \. \. \. \. \. \. \.\n"
        r"\. \. \. \. \. \. \. \. \. \.\n"
        r"\. \. \. \. \. \. \. \. \. \.\n"
        r"\. \. \. \. \. \. \. \. \. \.\n"
        r"\. \. \. \. \. \. \. \. \. \.\n"
        r"\. \. \. \. \. \. \. \. \. \.\n"
        r"\. \. \. \. \. \. \. \. \. \.\n"
        r"\. \. \. \. \. \. \. \. \. \.\n"
        r"\. \. \. \. \. \. \. \. \. \.",
        regex=True
    ).exit(0)

@check50.check(compiles)
def test_place_single():
    """places a single entity"""
    check50.run("./gridworld").stdin("place P 5 5\ndisplay\nquit").stdout(
        r"Placed P at \(5, 5\)",
        regex=True
    ).stdout(
        r"\. \. \. \. \. \. \. \. \. \.\n"
        r"\. \. \. \. \. \. \. \. \. \.\n"
        r"\. \. \. \. \. \. \. \. \. \.\n"
        r"\. \. \. \. \. \. \. \. \. \.\n"
        r"\. \. \. \. \. \. \. \. \. \.\n"
        r"\. \. \. \. \. P \. \. \. \.\n"
        r"\. \. \. \. \. \. \. \. \. \.\n"
        r"\. \. \. \. \. \. \. \. \. \.\n"
        r"\. \. \. \. \. \. \. \. \. \.\n"
        r"\. \. \. \. \. \. \. \. \. \.",
        regex=True
    ).exit(0)

@check50.check(compiles)
def test_place_multiple():
    """places multiple entities"""
    check50.run("./gridworld").stdin(
        "place P 2 3\nplace T 2 4\nplace R 5 5\nplace W 8 1\ndisplay\nquit"
    ).stdout(
        r"\. \. \. \. \. \. \. \. \. \.\n"
        r"\. \. \. \. \. \. \. \. \. \.\n"
        r"\. \. \. P T \. \. \. \. \.\n"
        r"\. \. \. \. \. \. \. \. \. \.\n"
        r"\. \. \. \. \. \. \. \. \. \.\n"
        r"\. \. \. \. \. R \. \. \. \.\n"
        r"\. \. \. \. \. \. \. \. \. \.\n"
        r"\. \. \. \. \. \. \. \. \. \.\n"
        r"\. W \. \. \. \. \. \. \. \.\n"
        r"\. \. \. \. \. \. \. \. \. \.",
        regex=True
    ).exit(0)

@check50.check(compiles)
def test_place_out_of_bounds():
    """rejects out of bounds placement"""
    check50.run("./gridworld").stdin(
        "place P 10 5\nplace T 5 10\nplace R -1 5\ndisplay\nquit"
    ).stdout(
        r"Could not place",
        regex=True
    ).stdout(
        r"\. \. \. \. \. \. \. \. \. \.\n"
        r"\. \. \. \. \. \. \. \. \. \.\n"
        r"\. \. \. \. \. \. \. \. \. \.\n"
        r"\. \. \. \. \. \. \. \. \. \.\n"
        r"\. \. \. \. \. \. \. \. \. \.\n"
        r"\. \. \. \. \. \. \. \. \. \.\n"
        r"\. \. \. \. \. \. \. \. \. \.\n"
        r"\. \. \. \. \. \. \. \. \. \.\n"
        r"\. \. \. \. \. \. \. \. \. \.\n"
        r"\. \. \. \. \. \. \. \. \. \.",
        regex=True
    ).exit(0)

@check50.check(compiles)
def test_place_occupied():
    """rejects placement on occupied space"""
    check50.run("./gridworld").stdin(
        "place P 5 5\nplace T 5 5\ndisplay\nquit"
    ).stdout(
        r"Placed P at \(5, 5\)",
        regex=True
    ).stdout(
        r"Could not place",
        regex=True
    ).stdout(
        r"\. \. \. \. \. P \. \. \. \.",
        regex=True
    ).exit(0)

@check50.check(compiles)
def test_move_right():
    """moves entity right"""
    check50.run("./gridworld").stdin(
        "place P 5 5\nmove 5 5 right\ndisplay\nquit"
    ).stdout(
        r"\. \. \. \. \. \. P \. \. \.",
        regex=True
    ).exit(0)

@check50.check(compiles)
def test_move_left():
    """moves entity left"""
    check50.run("./gridworld").stdin(
        "place P 5 5\nmove 5 5 left\ndisplay\nquit"
    ).stdout(
        r"\. \. \. \. P \. \. \. \. \.",
        regex=True
    ).exit(0)

@check50.check(compiles)
def test_move_up():
    """moves entity up"""
    check50.run("./gridworld").stdin(
        "place P 5 5\nmove 5 5 up\ndisplay\nquit"
    ).stdout(
        r"\. \. \. \. \. P \. \. \. \.",
        regex=True
    ).exit(0)

@check50.check(compiles)
def test_move_down():
    """moves entity down"""
    check50.run("./gridworld").stdin(
        "place P 5 5\nmove 5 5 down\ndisplay\nquit"
    ).stdout(
        r"\. \. \. \. \. P \. \. \. \.",
        regex=True
    ).exit(0)

@check50.check(compiles)
def test_move_out_of_bounds():
    """rejects out of bounds movement"""
    check50.run("./gridworld").stdin(
        "place P 0 0\nmove 0 0 up\nmove 0 0 left\ndisplay\nquit"
    ).stdout(
        r"Could not move",
        regex=True
    ).stdout(
        r"P \. \. \. \. \. \. \. \. \.",
        regex=True
    ).exit(0)

@check50.check(compiles)
def test_move_collision():
    """rejects movement into occupied space"""
    check50.run("./gridworld").stdin(
        "place P 5 5\nplace T 5 6\nmove 5 5 right\ndisplay\nquit"
    ).stdout(
        r"Could not move",
        regex=True
    ).stdout(
        r"\. \. \. \. \. P T \. \. \.",
        regex=True
    ).exit(0)

@check50.check(compiles)
def test_list_entities():
    """lists all entities"""
    check50.run("./gridworld").stdin(
        "place P 2 3\nplace T 5 5\nplace R 8 1\nlist\nquit"
    ).stdout(
        r"P at \(2, 3\)",
        regex=True
    ).stdout(
        r"T at \(5, 5\)",
        regex=True
    ).stdout(
        r"R at \(8, 1\)",
        regex=True
    ).exit(0)

@check50.check(compiles)
def test_remove():
    """removes entity"""
    check50.run("./gridworld").stdin(
        "place P 5 5\nplace T 5 6\nremove 5 5\ndisplay\nquit"
    ).stdout(
        r"\. \. \. \. \. \. T \. \. \.",
        regex=True
    ).exit(0)

@check50.check(compiles)
def test_neighbors_none():
    """counts zero neighbors"""
    check50.run("./gridworld").stdin(
        "place P 5 5\nneighbors 5 5 T\nquit"
    ).stdout(
        r"Found 0 neighbor",
        regex=True
    ).exit(0)

@check50.check(compiles)
def test_neighbors_one():
    """counts one neighbor"""
    check50.run("./gridworld").stdin(
        "place W 5 5\nplace W 5 6\nneighbors 5 5 W\nquit"
    ).stdout(
        r"Found 1 neighbor",
        regex=True
    ).exit(0)

@check50.check(compiles)
def test_neighbors_multiple():
    """counts multiple neighbors"""
    check50.run("./gridworld").stdin(
        "place W 4 4\nplace W 4 5\nplace W 5 4\nplace W 5 5\nneighbors 4 4 W\nquit"
    ).stdout(
        r"Found 2 neighbor",
        regex=True
    ).exit(0)

@check50.check(compiles)
def test_neighbors_all_eight():
    """counts all eight neighbors"""
    check50.run("./gridworld").stdin(
        "place T 4 4\nplace T 4 5\nplace T 4 6\nplace T 5 4\nplace T 5 6\n"
        "place T 6 4\nplace T 6 5\nplace T 6 6\nneighbors 5 5 T\nquit"
    ).stdout(
        r"Found 8 neighbor",
        regex=True
    ).exit(0)

@check50.check(compiles)
def test_complex_scenario():
    """handles complex operations"""
    check50.run("./gridworld").stdin(
        "place P 0 0\nplace T 0 1\nmove 0 0 right\nmove 0 0 down\n"
        "place R 9 9\nmove 9 9 right\nlist\nneighbors 1 0 T\n"
        "remove 0 1\nlist\ndisplay\nquit"
    ).stdout(
        r"Could not move",
        regex=True
    ).stdout(
        r"Moved entity",
        regex=True
    ).stdout(
        r"P at \(1, 0\)",
        regex=True
    ).stdout(
        r"R at \(9, 9\)",
        regex=True
    ).stdout(
        r"Found 1 neighbor",
        regex=True
    ).exit(0)
