import re

import check50
import check50.c

# Standard input for most checks (matches the sample run, minus the bad inputs)
GUESTS = ["3", "Grandma", "Leo", "Aunt Rosa"]
VOTES = ["1", "3", "1"]
MESSAGE = ["I love pie"]


def lines(*text):
    """Regex that matches these lines in order, one after another."""
    return r"\r?\n".join(re.escape(t) for t in text)


def run_feast(inputs):
    """Run ./feast and send every line of input up front."""
    process = check50.run("./feast")
    for line in inputs:
        process.stdin(line, prompt=False)
    return process


@check50.check()
def exists():
    """feast.c exists"""
    check50.exists("feast.c")


@check50.check(exists)
def compiles():
    """feast.c compiles"""
    check50.c.compile("feast.c", lcs50=True)


# ===== LEVEL 1 =====

@check50.check(compiles)
def rejects_bad_guest_count():
    """re-prompts when number of guests is 0 or 9"""
    run_feast(["0", "9"] + GUESTS + VOTES + MESSAGE) \
        .stdout(r"(How many guests\? ?){3}Guest 1 name: ") \
        .exit(0)


@check50.check(compiles)
def accepts_eight_guests():
    """accepts 8 guests"""
    names = ["A", "B", "C", "D", "E", "F", "G", "H"]
    run_feast(["8"] + names + ["1"] * 8 + MESSAGE) \
        .stdout(lines("8. H")) \
        .exit(0)


@check50.check(compiles)
def guest_list():
    """prints the numbered guest list"""
    run_feast(GUESTS + VOTES + MESSAGE) \
        .stdout(lines("Guest List", "1. Grandma", "2. Leo", "3. Aunt Rosa")) \
        .exit(0)


@check50.check(compiles)
def vote_prompts():
    """asks each guest for a vote by name"""
    run_feast(GUESTS + VOTES + MESSAGE) \
        .stdout(lines("Pie Poll: 1 = Pumpkin, 2 = Apple, 3 = Pecan")) \
        .stdout(r"Grandma's vote: ?Leo's vote: ?Aunt Rosa's vote: ") \
        .exit(0)


@check50.check(compiles)
def rejects_bad_vote():
    """re-prompts when a vote is not 1, 2, or 3"""
    run_feast(GUESTS + ["1", "5", "0", "3", "1"] + MESSAGE) \
        .stdout(r"(Leo's vote: ?){3}Aunt Rosa's vote: ") \
        .exit(0)


@check50.check(compiles)
def results():
    """prints one * per vote for each pie"""
    run_feast(GUESTS + VOTES + MESSAGE) \
        .stdout(lines("Results", "Pumpkin: **", "Apple: ", "Pecan: *")) \
        .exit(0)


@check50.check(results)
def winner_first():
    """picks Pumpkin as the winner"""
    run_feast(GUESTS + VOTES + MESSAGE) \
        .stdout(lines("Winner: Pumpkin pie!")) \
        .exit(0)


@check50.check(results)
def winner_not_first():
    """picks Apple as the winner"""
    run_feast(GUESTS + ["2", "2", "3"] + MESSAGE) \
        .stdout(lines("Apple: **", "Pecan: *", "Winner: Apple pie!")) \
        .exit(0)


@check50.check(results)
def winner_tie():
    """handles a tie (first pie listed wins, or bonus tie message)"""
    run_feast(["2", "Ann", "Bo", "3", "2"] + MESSAGE) \
        .stdout(r"Winner: Apple pie!|It's a tie!") \
        .exit(0)


# ===== LEVEL 2 =====

@check50.check(compiles)
def carver():
    """(Level 2) longest name carves the turkey"""
    run_feast(GUESTS + VOTES + MESSAGE) \
        .stdout(lines("Aunt Rosa carves the turkey!")) \
        .exit(0)


@check50.check(carver)
def carver_tie():
    """(Level 2) first guest wins a tie for longest name"""
    run_feast(["2", "Ann", "Bob", "1", "1"] + MESSAGE) \
        .stdout(lines("Ann carves the turkey!")) \
        .exit(0)


@check50.check(compiles)
def translator():
    """(Level 2) translates "I love pie" """
    run_feast(GUESTS + VOTES + MESSAGE) \
        .stdout(lines("Turkey says: O lovo poo Gobble gobble!")) \
        .exit(0)


@check50.check(translator)
def translator_case():
    """(Level 2) keeps uppercase vowels uppercase"""
    run_feast(GUESTS + VOTES + ["HAPPY Thanksgiving"]) \
        .stdout(lines("Turkey says: HOPPY Thonksgovong Gobble gobble!")) \
        .exit(0)
