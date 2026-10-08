import re

import check50
import check50.c


def pins_in(output):
    """Return the set of standalone 4-digit numbers in the output."""
    return set(re.findall(r"(?<!\d)\d{4}(?!\d)", output))


def run_with_hash(hash_value):
    """Run the program, give it a hash, and return everything it printed."""
    run = check50.run("./pin_cracker")
    run.stdin(str(hash_value))
    return run.stdout()


def expect_pin(hash_value, pin):
    output = run_with_hash(hash_value)
    found = pins_in(output)
    if pin not in found:
        raise check50.Failure(f"expected the PIN {pin} to be printed",
                              help="remember to print all 4 digits, including leading zeros")
    if found != {pin}:
        raise check50.Failure(f"expected only the PIN {pin}, but found other 4-digit numbers: {sorted(found - {pin})}")


@check50.check()
def exists():
    """pin_cracker.c exists"""
    check50.exists("pin_cracker.c")


@check50.check(exists)
def compiles():
    """pin_cracker.c compiles"""
    check50.c.compile("pin_cracker.c", lcs50=True)


@check50.check(compiles)
def finds_1234():
    """finds PIN 1234"""
    expect_pin(496439, "1234")


@check50.check(compiles)
def finds_7391():
    """finds PIN 7391"""
    expect_pin(676329, "7391")


@check50.check(compiles)
def finds_leading_zeros():
    """prints leading zeros (0042)"""
    expect_pin(464755, "0042")


@check50.check(compiles)
def finds_0007():
    """prints leading zeros (0007)"""
    expect_pin(464636, "0007")


@check50.check(compiles)
def finds_first_pin():
    """finds the first PIN, 0000"""
    expect_pin(464629, "0000")


@check50.check(compiles)
def finds_last_pin():
    """finds the last PIN, 9999"""
    expect_pin(741685, "9999")


@check50.check(compiles)
def no_match():
    """reports when no PIN matches"""
    output = run_with_hash(5)
    if pins_in(output):
        raise check50.Failure(f"printed a PIN even though none should match: {sorted(pins_in(output))}")
    if not output.strip():
        raise check50.Failure("printed nothing when no PIN matched",
                              help="print a message saying no PIN was found")
