import re

import check50
import check50.c


@check50.check()
def exists():
    """average.c exists"""
    check50.exists("average.c")


@check50.check(exists)
def compiles():
    """average.c compiles"""
    check50.c.compile("average.c", lcs50=True)


@check50.check(compiles)
def has_function():
    """defines an average function that takes an array"""
    with open("average.c") as f:
        code = f.read()
    # Looks for a function definition like: float average(int length, int array[]) {
    pattern = r"\baverage\s*\([^)]*\[\s*\][^)]*\)\s*\{"
    if not re.search(pattern, code):
        raise check50.Failure(
            "Couldn't find a function named average with an array parameter, "
            "like average(..., int array[])"
        )


@check50.check(compiles)
def rejects_zero():
    """rejects 0 as the number of scores"""
    check50.run("./average").stdin("0").reject()


@check50.check(compiles)
def rejects_negative():
    """rejects a negative number of scores"""
    check50.run("./average").stdin("-3").reject()


def check_average(scores, expected):
    """Run ./average with the given scores and look for the expected average."""
    run = check50.run("./average").stdin(str(len(scores)))
    for score in scores:
        run.stdin(str(score))
    # (?!\d) makes sure output like 82.333336 doesn't count as 82.3
    run.stdout(rf"{re.escape(expected)}(?!\d)", f"Average: {expected}\n", regex=True)
    run.exit(0)


@check50.check(has_function)
def three_scores():
    """90, 85, 72 averages to 82.3"""
    check_average([90, 85, 72], "82.3")


@check50.check(has_function)
def one_score():
    """a single score of 100 averages to 100.0"""
    check_average([100], "100.0")


@check50.check(has_function)
def five_scores():
    """72, 73, 33, 95, 61 averages to 66.8"""
    check_average([72, 73, 33, 95, 61], "66.8")


@check50.check(has_function)
def not_integer_division():
    """1 and 2 average to 1.5 (not 1.0)"""
    check_average([1, 2], "1.5")
