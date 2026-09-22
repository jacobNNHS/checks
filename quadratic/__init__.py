"""
check50 checks for quadratic.c

Problem: prompt for doubles a, b, c representing ax^2 + bx + c = 0,
and classify the number/type of real solutions using only conditionals.

NOTE: Adjust the EXPECTED_* strings below to match your exact wording.
Checks use substring matching (in the student's output) rather than exact
equality, so minor formatting differences (extra spaces, punctuation)
around the required phrase won't cause false failures -- but the KEY
PHRASES themselves must match what you tell students to print.
"""

import check50
import check50.c

# ---- Required wording (confirmed) ----
NO_SOLUTION = "No real solutions"
ONE_REPEATED = "One repeated real solution"
TWO_DISTINCT = "Two distinct real solutions"
INFINITE = "Infinite solutions"
LINEAR_PREFIX = "Linear equation, one solution: x ="
# -------------------------------------------------------------


@check50.check()
def exists():
    """quadratic.c exists"""
    check50.exists("quadratic.c")


@check50.check(exists)
def compiles():
    """quadratic.c compiles"""
    check50.c.compile("quadratic.c", exe_name="quadratic", lcs50=True)


@check50.check(compiles)
def two_distinct_solutions():
    """identifies two distinct real solutions (a=1, b=-3, c=2)"""
    check50.run("./quadratic") \
        .stdin("1\n-3\n2\n", prompt=False) \
        .stdout(f"(?i).*{TWO_DISTINCT}.*", regex=True) \
        .exit()


@check50.check(compiles)
def one_repeated_solution():
    """identifies one repeated real solution (a=1, b=2, c=1)"""
    check50.run("./quadratic") \
        .stdin("1\n2\n1\n", prompt=False) \
        .stdout(f"(?i).*{ONE_REPEATED}.*", regex=True) \
        .exit()


@check50.check(compiles)
def no_real_solutions():
    """identifies no real solutions when discriminant is negative (a=1, b=0, c=1)"""
    check50.run("./quadratic") \
        .stdin("1\n0\n1\n", prompt=False) \
        .stdout(f"(?i).*{NO_SOLUTION}.*", regex=True) \
        .exit()


@check50.check(compiles)
def linear_equation():
    """identifies a linear equation and computes correct root (a=0, b=4, c=-8)"""
    check50.run("./quadratic") \
        .stdin("0\n4\n-8\n", prompt=False) \
        .stdout(r"(?i).*Linear equation.*x\s*=\s*2\.00.*", regex=True) \
        .exit()


@check50.check(compiles)
def infinite_solutions():
    """identifies infinite solutions when a=0, b=0, c=0"""
    check50.run("./quadratic") \
        .stdin("0\n0\n0\n", prompt=False) \
        .stdout(f"(?i).*{INFINITE}.*", regex=True) \
        .exit()


@check50.check(compiles)
def no_solution_degenerate():
    """identifies no solution when a=0, b=0, c=5 (0 = -5 is never true)"""
    check50.run("./quadratic") \
        .stdin("0\n0\n5\n", prompt=False) \
        .stdout(f"(?i).*{NO_SOLUTION}.*", regex=True) \
        .exit()


@check50.check(compiles)
def linear_negative_root():
    """handles a linear equation with a negative root (a=0, b=2, c=6 -> x = -3.00)"""
    check50.run("./quadratic") \
        .stdin("0\n2\n6\n", prompt=False) \
        .stdout(r"(?i).*Linear equation.*x\s*=\s*-3\.00.*", regex=True) \
        .exit()


@check50.check(compiles)
def two_distinct_negative_a():
    """correctly handles negative leading coefficient (a=-1, b=0, c=4 -> two distinct)"""
    # x^2 = 4 style case via -x^2 + 4 = 0 -> x = ±2, discriminant = 0 - 4(-1)(4) = 16 > 0
    check50.run("./quadratic") \
        .stdin("-1\n0\n4\n", prompt=False) \
        .stdout(f"(?i).*{TWO_DISTINCT}.*", regex=True) \
        .exit()
