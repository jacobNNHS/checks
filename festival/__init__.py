import re

import check50
import check50.c

# Inputs, in the order the program asks for them:
# width, height, starting balance, goal, cupcakes, wristband code, voucher number
DEFAULTS = {
    "width": "6",
    "height": "4",
    "start": "100",
    "goal": "500",
    "cupcakes": "47",
    "wristband": "4006381333931",
    "voucher": "10000001",
}
ORDER = ["width", "height", "start", "goal", "cupcakes", "wristband", "voucher"]

# Signatures students were given for Stages 1 to 3
SIGNATURES = {
    "get_int_in_range": r"int\s+get_int_in_range\s*\(\s*int\s+\w+\s*,\s*int\s+\w+\s*\)",
    "print_banner": r"void\s+print_banner\s*\(\s*int\s+\w+\s*,\s*int\s+\w+\s*\)",
    "next_balance": r"int\s+next_balance\s*\(\s*int\s+\w+\s*\)",
    "months_to_goal": r"int\s+months_to_goal\s*\(\s*int\s+\w+\s*,\s*int\s+\w+\s*\)",
    "total_interest": r"int\s+total_interest\s*\(\s*int\s+\w+\s*,\s*int\s+\w+\s*\)",
    "boxes": r"int\s+boxes\s*\(\s*int\s+\w+\s*,\s*int\s+\w+\s*\)",
    "remaining": r"int\s+remaining\s*\(\s*int\s+\w+\s*,\s*int\s+\w+\s*\)",
}


# ----------------------------------------------------------------- helpers

def build_inputs(**overrides):
    """Return the stdin lines for one run. A value can be a string or a list of
    strings (use a list to type invalid values before the valid one)."""
    values = dict(DEFAULTS)
    values.update(overrides)
    lines = []
    for key in ORDER:
        value = values[key]
        lines.extend(value if isinstance(value, list) else [value])
    return lines


def run_program(**overrides):
    """Run ./festival with the given inputs and return everything it printed."""
    proc = check50.run("./festival")
    for line in build_inputs(**overrides):
        proc.stdin(line, prompt=False)
    try:
        output = proc.stdout()
    except check50.Failure:
        proc.kill()
        raise check50.Failure(
            "your program did not finish; it may be waiting for more input than expected, "
            "or stuck in a loop",
            help="check50 typed the inputs in the order: width, height, starting balance, "
                 "goal, cupcakes, wristband code, voucher number")
    return output.replace("\r", "")


def stage5_started():
    """Stage 5 counts as started if the program is still waiting for input after
    the wristband code has been entered."""
    proc = check50.run("./festival")
    for line in build_inputs()[:6]:
        proc.stdin(line, prompt=False)
    try:
        proc.reject(timeout=1)
        started = True
    except check50.Failure:
        started = False
    proc.kill()
    return started


def skip_optional():
    """True (and logs why) if Stage 5 has not been started."""
    if stage5_started():
        return False
    check50.log("Stage 5 is optional and your program does not ask for a voucher, "
                "so this check passes automatically.")
    return True


def expect_numbers(output, expected):
    """expected maps a label such as 'Months' to the number printed after it."""
    for label, want in expected.items():
        match = re.search(rf"(?<!\d){re.escape(label)}:?\s*(-?\d+)", output)
        if not match:
            raise check50.Failure(f'could not find "{label}: <number>" in your output')
        got = int(match.group(1))
        if got != want:
            raise check50.Mismatch(f"{label}: {want}", f"{label}: {got}")


def banner_pattern(width, height):
    top = r"\*{%d}" % width
    middle = r"\*[ ]{%d}\*\n" % (width - 2)
    return r"(?<!\*)" + top + r"\n(?:" + middle + r"){%d}" % (height - 2) + top + r"(?!\*)"


def expect_banner(output, width, height):
    cleaned = "\n".join(line.rstrip() for line in output.split("\n"))
    if not re.search(banner_pattern(width, height), cleaned):
        top = "*" * width
        middle = "*" + " " * (width - 2) + "*"
        expected = "\n".join([top] + [middle] * (height - 2) + [top])
        raise check50.Mismatch(expected, output)


def word_present(word, output):
    return re.search(rf"\b{word}\b", output) is not None


def expect_wristband(output, valid):
    """Inputs always use a valid voucher, so INVALID can only come from the wristband."""
    has_invalid = word_present("INVALID", output)
    has_valid = word_present("VALID", output)
    if valid and (has_invalid or not has_valid):
        raise check50.Failure("expected VALID for this wristband code",
                              help="your output was:\n" + output)
    if not valid and not has_invalid:
        raise check50.Failure("expected INVALID for this wristband code",
                              help="your output was:\n" + output)


def expect_voucher(output, expected):
    """Inputs always use a valid wristband, so INVALID can only come from the voucher."""
    categories = ["STUDENT", "STAFF", "GUEST"]
    if expected == "INVALID":
        if not word_present("INVALID", output) or any(word_present(c, output) for c in categories):
            raise check50.Failure("expected INVALID for this voucher number",
                                  help="your output was:\n" + output)
        return
    others = [c for c in categories if c != expected]
    if not word_present(expected, output) or word_present("INVALID", output) \
            or any(word_present(c, output) for c in others):
        raise check50.Failure(f"expected {expected} for this voucher number",
                              help="your output was:\n" + output)


def source_code():
    """festival.c with comments and string contents removed."""
    with open("festival.c") as f:
        text = f.read()
    token = re.compile(r"//[^\n]*|/\*.*?\*/|\"(?:\\.|[^\"\\\n])*\"|'(?:\\.|[^'\\\n])*'", re.S)
    return token.sub(lambda m: " " if m.group(0).startswith("/") else m.group(0)[0] * 2, text)


def call(*args, stdin=()):
    """Run the harness and return the RESULT number."""
    proc = check50.run("./harness " + " ".join(str(a) for a in args))
    for line in stdin:
        proc.stdin(line, prompt=False)
    output = proc.stdout()
    match = re.search(r"RESULT:(-?\d+)", output)
    if not match:
        raise check50.Failure("your function did not return normally", help=output)
    return int(match.group(1))


def expect_call(want, label, *args, stdin=()):
    got = call(*args, stdin=stdin)
    if got != want:
        raise check50.Mismatch(f"{label} = {want}", f"{label} = {got}")


# -------------------------------------------------------------- basic checks

@check50.check()
def exists():
    """festival.c exists"""
    check50.exists("festival.c")


@check50.check(exists)
def compiles():
    """festival.c compiles with -Wall -Werror"""
    check50.c.compile("festival.c", lcs50=True, Wall=True, Werror=True)


@check50.check(exists)
def prototypes():
    """prototypes for the given functions are above main, definitions below"""
    code = source_code()
    main = re.search(r"\bint\s+main\s*\(", code)
    if not main:
        raise check50.Failure("could not find int main(void)")
    before, after = code[:main.start()], code[main.start():]
    for name, signature in SIGNATURES.items():
        if not re.search(signature + r"\s*;", before):
            raise check50.Failure(f"missing the prototype for {name} above main",
                                  help="copy it from the starter prototypes")
        if not re.search(signature + r"\s*\{", after):
            raise check50.Failure(f"missing the definition of {name} below main",
                                  help="the definition must match the prototype")


@check50.check(compiles)
def harness_builds():
    """functions can be called on their own"""
    check50.include("harness.c")
    check50.c.compile("festival.c", "harness.c", exe_name="harness",
                      cc="clang -Dmain=student_main", lcs50=True)


# ------------------------------------------------------- function-level checks

@check50.check(harness_builds)
def unit_get_int_in_range():
    """get_int_in_range keeps asking until the number is in range"""
    expect_call(7, "get_int_in_range(4, 20)", "range", 4, 20, stdin=["3", "21", "7"])
    expect_call(4, "get_int_in_range(4, 20)", "range", 4, 20, stdin=["3", "4"])
    expect_call(20, "get_int_in_range(4, 20)", "range", 4, 20, stdin=["21", "20"])


@check50.check(harness_builds)
def unit_print_banner():
    """print_banner prints a hollow rectangle"""
    output = check50.run("./harness banner 6 4").stdout().replace("\r", "")
    expect_banner(output, 6, 4)
    output = check50.run("./harness banner 4 3").stdout().replace("\r", "")
    expect_banner(output, 4, 3)


@check50.check(harness_builds)
def unit_stage2_functions():
    """next_balance, months_to_goal and total_interest return the right values"""
    expect_call(130, "next_balance(100)", "next", 100)
    expect_call(1075, "next_balance(1000)", "next", 1000)
    for start, goal, months, interest in [(100, 500, 11, 147), (100, 130, 1, 5),
                                          (500, 600, 2, 52), (1000, 2000, 11, 784)]:
        expect_call(months, f"months_to_goal({start}, {goal})", "months", start, goal)
        expect_call(interest, f"total_interest({start}, {goal})", "interest", start, goal)


@check50.check(harness_builds)
def unit_stage3_functions():
    """boxes and remaining return the right values"""
    for cupcakes, size, full, left in [(47, 12, 3, 11), (11, 6, 1, 5), (5, 3, 1, 2), (2, 3, 0, 2)]:
        expect_call(full, f"boxes({cupcakes}, {size})", "boxes", cupcakes, size)
        expect_call(left, f"remaining({cupcakes}, {size})", "remaining", cupcakes, size)


# ------------------------------------------------------------ whole-program checks

@check50.check(compiles)
def stage1_banner():
    """stage 1: banner width and height are validated and the banner is printed"""
    output = run_program(width=["3", "21", "6"], height=["2", "11", "4"])
    expect_banner(output, 6, 4)
    for width, height in [(4, 3), (20, 10), (9, 5)]:
        output = run_program(width=str(width), height=str(height))
        expect_banner(output, width, height)


@check50.check(compiles)
def stage2_fundraiser():
    """stage 2: 100 to 500 takes 11 months and earns 147 in interest"""
    output = run_program(start=["99", "100"], goal=["100", "500"])
    expect_numbers(output, {"Months": 11, "Interest": 147})


@check50.check(stage2_fundraiser)
def stage2_other_goals():
    """stage 2: other starting balances and goals"""
    for start, goal, months, interest in [(100, 130, 1, 5), (500, 600, 2, 52), (1000, 2000, 11, 784)]:
        output = run_program(start=str(start), goal=str(goal))
        expect_numbers(output, {"Months": months, "Interest": interest})


@check50.check(compiles)
def stage3_cupcakes():
    """stage 3: 47 cupcakes use 3, 1, 1 and 2 singles"""
    output = run_program(cupcakes=["0", "1001", "47"])
    expect_numbers(output, {"12-packs": 3, "6-packs": 1, "3-packs": 1, "Singles": 2})


@check50.check(stage3_cupcakes)
def stage3_other_counts():
    """stage 3: other numbers of cupcakes"""
    for cupcakes, big, medium, small, singles in [(1, 0, 0, 0, 1), (11, 0, 1, 1, 2), (12, 1, 0, 0, 0),
                                                  (29, 2, 0, 1, 2), (100, 8, 0, 1, 1)]:
        output = run_program(cupcakes=str(cupcakes))
        expect_numbers(output, {"12-packs": big, "6-packs": medium, "3-packs": small, "Singles": singles})


@check50.check(compiles)
def stage4_valid_wristbands():
    """stage 4: valid wristband codes are VALID"""
    for code in ["4006381333931", "9780306406157", "5012345678900"]:
        expect_wristband(run_program(wristband=code), True)


@check50.check(compiles)
def stage4_invalid_wristbands():
    """stage 4: invalid wristband codes are INVALID"""
    for code in ["4006381333932", "4006381333913", "9780306406158"]:
        expect_wristband(run_program(wristband=code), False)


@check50.check(stage4_valid_wristbands)
def stage4_reprompts():
    """stage 4: codes without exactly 13 digits (or negative) are asked for again"""
    output = run_program(wristband=["400638133393", "40063813339310", "-4006381333931", "4006381333931"])
    expect_wristband(output, True)


# ---------------------------------------------- stage 5 (optional) and final report

@check50.check(stage4_valid_wristbands)
def stage5_categories():
    """optional stage 5: STUDENT, STAFF and GUEST vouchers (passes if you have not started stage 5)"""
    if skip_optional():
        return
    for voucher, category in [("10000001", "STUDENT"), ("45210330", "STAFF"), ("7312345678", "GUEST"),
                              ("1000000001", "STUDENT")]:
        expect_voucher(run_program(voucher=voucher), category)


@check50.check(stage4_valid_wristbands)
def stage5_boundaries():
    """optional stage 5: category boundaries and an alternating sum of 11"""
    if skip_optional():
        return
    for voucher, category in [("39000060", "STUDENT"), ("40000004", "STAFF"), ("69000030", "STAFF"),
                              ("70000007", "GUEST"), ("99000000", "GUEST"), ("19030000", "STUDENT")]:
        expect_voucher(run_program(voucher=voucher), category)


@check50.check(stage4_valid_wristbands)
def stage5_invalid():
    """optional stage 5: bad length, bad alternating sum, zero and negative are INVALID"""
    if skip_optional():
        return
    for voucher in ["45210331", "12345678", "123456789", "12345678901", "0", "-10000001"]:
        expect_voucher(run_program(voucher=voucher), "INVALID")


REPORT_LINES = 5


@check50.check(stage4_valid_wristbands)
def final_report():
    """final report shows the right values (the voucher result is required only if you did stage 5)"""
    with_stage5 = stage5_started()
    cases = [
        (dict(), [6, 4, 11, 47, 7], ["VALID", "STUDENT"]),
        (dict(width="4", height="3", start="1000", goal="2000", cupcakes="29",
              wristband="9780306406158", voucher="45210331"),
         [4, 3, 11, 29, 5], ["INVALID", "INVALID"]),
    ]
    for overrides, numbers, words in cases:
        output = run_program(**overrides)
        lines = [line.strip() for line in output.split("\n") if line.strip()]
        report = lines[-REPORT_LINES:]
        # Only the values matter, not the wording or the number of lines (up to five):
        # banner width, banner height, months, cupcakes, containers, then the
        # wristband result and the voucher result, in that order.
        want_words = words if with_stage5 else words[:1]
        wanted = [str(n) for n in numbers] + want_words
        tokens = re.findall(r"\d+|\b(?:INVALID|VALID|STUDENT|STAFF|GUEST)\b", "\n".join(report))
        matched = 0
        for token in tokens:
            if matched < len(wanted) and token == wanted[matched]:
                matched += 1
        if matched < len(wanted):
            raise check50.Failure(
                "the final report is missing or has a wrong value: " + wanted[matched],
                help="check50 reads the last %d lines your program prints and looks for these "
                     "values in order: banner width, banner height, months, cupcakes, containers, "
                     "wristband result%s. Expected: %s. Your last lines were:\n%s"
                     % (REPORT_LINES, ", voucher result" if with_stage5 else "",
                        ", ".join(wanted), "\n".join(report)))
