import check50
import check50.c


@check50.check()
def exists():
    """last_letter.c exists"""
    check50.exists("last_letter.c")
    check50.include("test_get_last_letter.c")


@check50.check(exists)
def compiles():
    """last_letter.c compiles"""
    check50.c.compile("last_letter.c", lcs50=True)


def check_word(word, expected):
    check50.run("./last_letter").stdin(word, prompt=True) \
        .stdout(expected + "\n", regex=False) \
        .exit(0)


# ---------- Level 1: words made only of letters ----------

@check50.check(compiles)
def hello():
    """Level 1: handles "hello" as input"""
    check_word("hello", "Last letter: o")


@check50.check(compiles)
def single_letter():
    """Level 1: handles a one-letter word, "a", as input"""
    check_word("a", "Last letter: a")


@check50.check(compiles)
def long_word():
    """Level 1: handles "Massachusetts" as input"""
    check_word("Massachusetts", "Last letter: s")


@check50.check(compiles)
def capital_last():
    """Level 1: handles "chatGPT" as input"""
    check_word("chatGPT", "Last letter: T")


@check50.check(compiles)
def function_level1():
    """Level 1: get_last_letter() returns the correct letter when called directly"""
    check50.c.compile("test_get_last_letter.c", lcs50=True)
    check50.run("./test_get_last_letter 1") \
        .stdout("z\nk\nx\n", regex=False) \
        .exit(0)


# ---------- Level 2: skip non-letters, handle no letters ----------

@check50.check(compiles)
def punctuation():
    """Level 2: handles "hello!" as input"""
    check_word("hello!", "Last letter: o")


@check50.check(compiles)
def digits():
    """Level 2: handles "CS50" as input"""
    check_word("CS50", "Last letter: S")


@check50.check(compiles)
def mixed():
    """Level 2: handles "R2-D2 :)" as input"""
    check_word("R2-D2 :)", "Last letter: D")


@check50.check(compiles)
def no_letters():
    """Level 2: handles "?!" (no letters) as input"""
    check_word("?!", "No letters")


@check50.check(compiles)
def empty():
    """Level 2: handles empty input"""
    check_word("", "No letters")


@check50.check(compiles)
def function_level2():
    """Level 2: get_last_letter() skips non-letters and returns '\\0' when there are none"""
    check50.c.compile("test_get_last_letter.c", lcs50=True)
    check50.run("./test_get_last_letter 2") \
        .stdout("w\nD\nnone\nnone\n", regex=False) \
        .exit(0)
