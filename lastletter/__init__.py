import check50
import check50.c

# Small C program that calls the student's get_last_letter() directly,
# bypassing their main. Written to disk by the exists check below.
HARNESS = r"""
// Calls the student's get_last_letter() directly, bypassing their main.
#define main student_main
#include "last_letter.c"
#undef main

void show(char c)
{
    if (c == '\0')
    {
        printf("none\n");
    }
    else
    {
        printf("%c\n", c);
    }
}

int main(int argc, char *argv[])
{
    if (argc == 2 && argv[1][0] == '1')
    {
        // Level 1: words made only of letters
        show(get_last_letter("quiz"));
        show(get_last_letter("k"));
        show(get_last_letter("toolbox"));
    }
    else
    {
        // Level 2: non-letters and words with no letters
        show(get_last_letter("wow!!"));
        show(get_last_letter("R2D2"));
        show(get_last_letter("404"));
        show(get_last_letter(""));
    }
    return 0;
}
"""


@check50.check()
def exists():
    """last_letter.c exists"""
    check50.exists("last_letter.c")
    with open("test_get_last_letter.c", "w") as f:
        f.write(HARNESS)


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
