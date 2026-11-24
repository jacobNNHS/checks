import re

import check50
import check50.c

# Flexible checks: wording, capitalization, spacing, and punctuation can vary.
# What's checked is the content: the right numbers, names, counts, and winners.

GUESTS = ["3", "Grandma", "Leo", "Aunt Rosa"]
VOTES = ["1", "3", "1"]
MESSAGE = ["I love pie"]
PIES = ["Pumpkin", "Apple", "Pecan"]


def output_of(inputs):
    """Run ./feast with these inputs and return everything it printed."""
    process = check50.run("./feast")
    for line in inputs:
        process.stdin(line, prompt=False)
    out = process.stdout()  # waits for the program to finish
    # Collapse runs of spaces and tabs so spacing doesn't matter
    return re.sub(r"[ \t]+", " ", out)


def count_prompts(out, name):
    """How many times '<name>... vote' was printed as a prompt."""
    return len(re.findall(re.escape(name.lower()) + r"[^\n]{0,15}?vote", out.lower()))


def star_counts(out):
    """Find each pie's results line and count its stars."""
    counts = {}
    for line in out.splitlines():
        lower = line.lower()
        found = [pie for pie in PIES if pie.lower() in lower]
        # A results line names exactly one pie and isn't a vote prompt or the winner line
        if len(found) == 1 and "vote" not in lower and "win" not in lower:
            counts[found[0]] = line.count("*")
    return counts


def find_line(out, *keywords):
    """First line containing any of the keywords (case-insensitive)."""
    for line in out.splitlines():
        if any(k in line.lower() for k in keywords):
            return line
    return None


def check_stars(out, expected):
    counts = star_counts(out)
    for pie in PIES:
        if pie not in counts:
            raise check50.Failure(f"couldn't find a results line for {pie}")
    if counts != expected:
        raise check50.Mismatch(
            "\n".join(f"{p}: {'*' * expected[p]}" for p in PIES),
            "\n".join(f"{p}: {'*' * counts[p]}" for p in PIES),
        )


def check_winner(out, *accepted):
    line = find_line(out, "win", "tie")
    if line is None:
        raise check50.Failure("couldn't find a line announcing the winner")
    lower = line.lower()
    named = [pie for pie in PIES if pie.lower() in lower]
    ok = (len(named) == 1 and named[0] in accepted) or ("tie" in accepted and "tie" in lower and not named)
    if not ok:
        raise check50.Mismatch(f"winner: {' or '.join(accepted)}", line.strip())


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
    out = output_of(["0", "9"] + GUESTS + VOTES + MESSAGE)
    asked = out.lower().count("how many")
    if asked != 3:
        raise check50.Failure(
            f"expected to be asked for the number of guests 3 times, but was asked {asked}")


@check50.check(compiles)
def accepts_eight_guests():
    """accepts 8 guests"""
    names = ["Ann", "Ben", "Cal", "Dee", "Eli", "Fay", "Gus", "Hal"]
    out = output_of(["8"] + names + ["1"] * 8 + MESSAGE)
    if out.lower().count("how many") != 1:
        raise check50.Failure("8 guests should be accepted without re-prompting")
    if not re.search(r"8\W*hal", out.lower()):
        raise check50.Failure("expected guest list to include \"8. Hal\"")


@check50.check(compiles)
def guest_list():
    """prints the numbered guest list"""
    out = output_of(GUESTS + VOTES + MESSAGE).lower()
    for number, name in [(1, "Grandma"), (2, "Leo"), (3, "Aunt Rosa")]:
        if not re.search(rf"{number}\W*{name.lower()}", out):
            raise check50.Failure(f"expected guest list to include \"{number}. {name}\"")


@check50.check(compiles)
def vote_prompts():
    """asks each guest for a vote by name"""
    out = output_of(GUESTS + VOTES + MESSAGE)
    for name in ["Grandma", "Leo", "Aunt Rosa"]:
        if count_prompts(out, name) != 1:
            raise check50.Failure(f"expected one vote prompt that includes \"{name}\"")


@check50.check(compiles)
def rejects_bad_vote():
    """re-prompts when a vote is not 1, 2, or 3"""
    out = output_of(GUESTS + ["1", "5", "0", "3", "1"] + MESSAGE)
    asked = count_prompts(out, "Leo")
    if asked != 3:
        raise check50.Failure(
            f"Leo entered 5, then 0, then 3, so should be asked 3 times, but was asked {asked}")


@check50.check(compiles)
def results():
    """prints one * per vote for each pie"""
    out = output_of(GUESTS + VOTES + MESSAGE)
    check_stars(out, {"Pumpkin": 2, "Apple": 0, "Pecan": 1})


@check50.check(results)
def winner_first():
    """picks Pumpkin as the winner"""
    out = output_of(GUESTS + VOTES + MESSAGE)
    check_winner(out, "Pumpkin")


@check50.check(results)
def winner_not_first():
    """picks Apple as the winner"""
    out = output_of(GUESTS + ["2", "2", "3"] + MESSAGE)
    check_stars(out, {"Pumpkin": 0, "Apple": 2, "Pecan": 1})
    check_winner(out, "Apple")


@check50.check(results)
def winner_tie():
    """handles a tie (first pie listed wins, or bonus tie message)"""
    out = output_of(["2", "Ann", "Bo", "3", "2"] + MESSAGE)
    check_winner(out, "Apple", "tie")


# ===== LEVEL 2 =====

@check50.check(compiles)
def carver():
    """(Level 2) longest name carves the turkey"""
    out = output_of(GUESTS + VOTES + MESSAGE)
    line = find_line(out, "carve")
    if line is None or "aunt rosa" not in line.lower():
        raise check50.Mismatch("Aunt Rosa carves the turkey!", (line or "").strip())


@check50.check(carver)
def carver_tie():
    """(Level 2) first guest wins a tie for longest name"""
    out = output_of(["2", "Ann", "Bob", "1", "1"] + MESSAGE)
    line = find_line(out, "carve")
    if line is None or "ann" not in line.lower():
        raise check50.Mismatch("Ann carves the turkey!", (line or "").strip())


@check50.check(compiles)
def translator():
    """(Level 2) translates "I love pie" """
    out = output_of(GUESTS + VOTES + MESSAGE)
    if "O lovo poo" not in out or "gobble" not in out.lower():
        raise check50.Mismatch("Turkey says: O lovo poo Gobble gobble!",
                               (find_line(out, "turkey says", "gobble") or "").strip())


@check50.check(translator)
def translator_case():
    """(Level 2) keeps uppercase vowels uppercase"""
    out = output_of(GUESTS + VOTES + ["HAPPY Thanksgiving"])
    if "HOPPY Thonksgovong" not in out:
        raise check50.Mismatch("Turkey says: HOPPY Thonksgovong Gobble gobble!",
                               (find_line(out, "turkey says", "gobble") or "").strip())
