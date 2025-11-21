import check50
import check50.c

@check50.check()
def exists():
    """mail.c exists"""
    check50.exists("mail.c")

@check50.check()
def compiles():
    """mail.c compiles"""
    check50.c.compile("mail.c", lcs50=True)

@check50.check(compiles)
def one_oz_letter():
    """checking price for 1(oz.) letter"""
    check50.run("./mail").stdin("1").stdout("\$1.63\n").exit(0)

@check50.check(compiles)
def two_point_five_oz_letter():
    """checking price for 2.5(oz.) letter"""
    check50.run("./mail").stdin("2.5").stdout("\$2.17\n").exit(0)

@check50.check(compiles)
def twelve_point_thirtyfour_oz_letter():
    """checking price for 12.34(oz.) letter"""
    check50.run("./mail").stdin("12.34").stdout("\$5.04\n").exit(0)

@check50.check(compiles)
def thirteen_oz_letter():
    """checking price for 13(oz.) letter"""
    check50.run("./mail").stdin("13").stdout("\$5.04\n").exit(0)

@check50.check(compiles)
def thirteen_point_zero_one_oz_letter():
    """checking price for 13.01(oz.) letter"""
    check50.run("./mail").stdin("13.01").stdout("Over allowed weight").exit(0)
