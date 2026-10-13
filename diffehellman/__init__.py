import re

import check50
import check50.c


def numbers_in(output):
    """Return every whole number printed, in order."""
    return [int(n) for n in re.findall(r"-?\d+", output)]


def in_order(found, expected):
    """True if the expected numbers appear in found, in this order (other numbers may sit between them)."""
    it = iter(found)
    return all(any(n == e for n in it) for e in expected)


def run_with(*inputs):
    """Run the program, send each input, and return everything it printed."""
    run = check50.run("./secret_handshake")
    for value in inputs:
        run.stdin(str(value))
    return run.stdout()


def expected_values(p, g, a, b):
    A = pow(g, a, p)
    B = pow(g, b, p)
    return A, B, pow(B, a, p), pow(A, b, p)


def expect_exchange(inputs, p, g, a, b):
    A, B, alice, bob = expected_values(p, g, a, b)
    output = run_with(*inputs)
    if not in_order(numbers_in(output), [A, B, alice, bob]):
        raise check50.Failure(
            f"expected Alice to send {A}, Bob to send {B}, "
            f"and both shared secrets to be {alice}",
            help="print what Alice sends, what Bob sends, then Alice's and Bob's shared secrets, in that order")


def source_without_comments_or_strings():
    with open("secret_handshake.c") as f:
        code = f.read()
    code = re.sub(r"/\*.*?\*/", "", code, flags=re.S)
    code = re.sub(r"//[^\n]*", "", code)
    code = re.sub(r'"(?:\\.|[^"\\])*"', '""', code)
    return code


@check50.check()
def exists():
    """secret_handshake.c exists"""
    check50.exists("secret_handshake.c")


@check50.check(exists)
def compiles():
    """secret_handshake.c compiles"""
    check50.c.compile("secret_handshake.c", lcs50=True)


@check50.check(compiles)
def sample_23_5():
    """p = 23, g = 5, a = 6, b = 15"""
    expect_exchange([23, 5, 6, 15], 23, 5, 6, 15)


@check50.check(compiles)
def sample_17_3():
    """p = 17, g = 3, a = 5, b = 7"""
    expect_exchange([17, 3, 5, 7], 17, 3, 5, 7)


@check50.check(compiles)
def sample_97_5():
    """p = 97, g = 5, a = 36, b = 58"""
    expect_exchange([97, 5, 36, 58], 97, 5, 36, 58)


@check50.check(compiles)
def smallest_secrets():
    """handles secrets of 1 (p = 23, g = 5, a = 1, b = 1)"""
    expect_exchange([23, 5, 1, 1], 23, 5, 1, 1)


@check50.check(compiles)
def largest_secrets():
    """handles the largest secrets, p - 1 (p = 23, g = 5, a = 22, b = 22)"""
    expect_exchange([23, 5, 22, 22], 23, 5, 22, 22)


@check50.check(compiles)
def smallest_prime():
    """handles the smallest allowed prime (p = 3, g = 2, a = 1, b = 2)"""
    expect_exchange([3, 2, 1, 2], 3, 2, 1, 2)


@check50.check(compiles)
def large_exponents():
    """handles large exponents (p = 997, g = 5, a = 996, b = 900)"""
    expect_exchange([997, 5, 996, 900], 997, 5, 996, 900)


@check50.check(compiles)
def rejects_bad_p():
    """rejects p below 3 or at least 1000"""
    expect_exchange([2, 1000, -5, 23, 5, 6, 15], 23, 5, 6, 15)


@check50.check(compiles)
def rejects_bad_g():
    """rejects g below 2 or at least p"""
    expect_exchange([23, 1, 23, 40, 5, 6, 15], 23, 5, 6, 15)


@check50.check(compiles)
def rejects_bad_secrets():
    """rejects secrets below 1 or at least p"""
    expect_exchange([23, 5, 0, 23, 6, -4, 15], 23, 5, 6, 15)


@check50.check(exists)
def no_pow():
    """does not use pow"""
    if re.search(r"\bpow\s*\(", source_without_comments_or_strings()):
        raise check50.Failure("found pow in your code",
                              help="build the powers with loops instead")


@check50.check(exists)
def no_arrays_or_strings():
    """does not use arrays or strings"""
    code = source_without_comments_or_strings()
    if re.search(r"\[|\bstring\b|\bchar\b|\bget_string\b", code):
        raise check50.Failure("found an array or string in your code")


@check50.check(exists)
def only_main():
    """has everything in main (no other functions)"""
    code = source_without_comments_or_strings()
    names = re.findall(
        r"^[ \t]*(?:static\s+)?(?:unsigned\s+)?(?:int|long|void|double|float|bool|char)\s+(\w+)\s*\([^;{)]*\)\s*\{?\s*$",
        code, flags=re.M)
    extra = [n for n in names if n != "main"]
    if extra:
        raise check50.Failure(f"found extra function(s): {', '.join(extra)}",
                              help="write all of your code inside main")
