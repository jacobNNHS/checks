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


def check_word(word, letter):
    check50.run("./last_letter").stdin(word, prompt=True) \
        .stdout(f"Last letter: {letter}\n", regex=False) \
        .exit(0)


@check50.check(compiles)
def hello():
    """handles "hello" as input"""
    check_word("hello", "o")


@check50.check(compiles)
def single_letter():
    """handles a one-letter word, "a", as input"""
    check_word("a", "a")


@check50.check(compiles)
def long_word():
    """handles "Massachusetts" as input"""
    check_word("Massachusetts", "s")


@check50.check(compiles)
def capital_last():
    """handles "chatGPT" as input"""
    check_word("chatGPT", "T")


@check50.check(compiles)
def function_works():
    """get_last_letter() returns the correct letter when called directly"""
    check50.c.compile("test_get_last_letter.c", lcs50=True)
    check50.run("./test_get_last_letter") \
        .stdout("z\nk\nx\n", regex=False) \
        .exit(0)
