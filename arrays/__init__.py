import re
import check50
import check50.c

NUMS = [41, -17, 93, 8, 60, 25, -4, 77, 12, 36]   # max 93, min -17, 2nd 77
NUMS_DUP_MAX = [50, 93, 93, 20, 77, 5, 61, 33, 18, 2]  # max 93, min 2, 2nd 77
UNIQ = (4, [31, 22, 22, 55])
PAL = (5, [1, 2, 3, 2, 1])
NOT_PAL = (5, [1, 2, 3, 4, 5])


def ints(text):
    return [int(t) for t in re.findall(r"-?\d+", text)]


def build_input(nums=NUMS, uniq=UNIQ, pal=PAL):
    parts = [str(n) for n in nums]
    parts += [str(uniq[0])] + [str(n) for n in uniq[1]]
    parts += [str(pal[0])] + [str(n) for n in pal[1]]
    return parts


def run_program(**kwargs):
    proc = check50.run("./arrays")
    for token in build_input(**kwargs):
        proc.stdin(token, prompt=False)
    return proc.stdout()


def after_echo(out, nums):
    """Return numeric tokens that appear after the echoed list of nums."""
    tokens = ints(out)
    i = 5  # skip the 1..5 printed at the start
    for n in nums:
        try:
            i = tokens.index(n, i) + 1
        except ValueError:
            raise check50.Failure(
                "did not print the 10 integers back in the same order"
            )
    return tokens, tokens[i:]


@check50.check()
def exists():
    """arrays.c exists"""
    check50.exists("arrays.c")


@check50.check(exists)
def compiles():
    """arrays.c compiles"""
    check50.c.compile("arrays.c", lcs50=True)


@check50.check(compiles)
def declaration():
    """prints 1 2 3 4 5 from an initialized array"""
    out = run_program()
    if ints(out)[:5] != [1, 2, 3, 4, 5]:
        raise check50.Failure("expected output to begin with 1 2 3 4 5")


@check50.check(compiles)
def input_output():
    """reads 10 integers and prints them in the same order"""
    out = run_program()
    after_echo(out, NUMS)


@check50.check(compiles)
def maximum():
    """finds the largest of 10 integers"""
    out = run_program()
    _, rest = after_echo(out, NUMS)
    if 93 not in rest:
        raise check50.Failure("expected the maximum, 93, to be printed")


@check50.check(compiles)
def minimum():
    """finds the smallest of 10 integers (including negatives)"""
    out = run_program()
    _, rest = after_echo(out, NUMS)
    if -17 not in rest:
        raise check50.Failure("expected the minimum, -17, to be printed")


@check50.check(compiles)
def second_largest():
    """finds the second largest integer"""
    out = run_program()
    _, rest = after_echo(out, NUMS)
    if 77 not in rest:
        raise check50.Failure("expected the second largest, 77, to be printed")


@check50.check(compiles)
def second_largest_duplicate_max():
    """second largest ignores a repeated maximum"""
    out = run_program(nums=NUMS_DUP_MAX)
    _, rest = after_echo(out, NUMS_DUP_MAX)
    if 77 not in rest:
        raise check50.Failure(
            "with 93 appearing twice, the second largest should be 77"
        )


@check50.check(compiles)
def unique_elements():
    """prints only elements that appear exactly once"""
    out = run_program()
    matches = list(re.finditer(r"unique", out, re.I))
    if not matches:
        raise check50.Failure('output should include the word "unique"')
    section = out[matches[-1].end():]
    section = re.split(r"palindrom", section, flags=re.I)[0]
    tokens = ints(section)
    if 31 not in tokens or 55 not in tokens:
        raise check50.Failure("expected unique elements 31 and 55")
    if 22 in tokens:
        raise check50.Failure("22 appears twice and should not be printed")
    if tokens.index(31) > tokens.index(55):
        raise check50.Failure("unique elements should keep original order")


def last_line(out):
    lines = [l for l in out.strip().splitlines() if l.strip()]
    return lines[-1].lower() if lines else ""


@check50.check(compiles)
def palindrome_yes():
    """identifies a palindromic array"""
    out = run_program(pal=PAL)
    line = last_line(out)
    if re.search(r"\bnot\b|n't", line) or not re.search(r"palindrom|yes", line):
        raise check50.Failure("expected last line to say the array IS a palindrome")


@check50.check(compiles)
def palindrome_no():
    """identifies a non-palindromic array"""
    out = run_program(pal=NOT_PAL)
    line = last_line(out)
    if not re.search(r"\bnot\b|n't|\bno\b", line):
        raise check50.Failure("expected last line to say the array is NOT a palindrome")
