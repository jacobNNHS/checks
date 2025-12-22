import check50
import re


@check50.check()
def exists():
    """text_analysis.c exists"""
    check50.exists("text_analysis.c")


@check50.check(exists)
def compiles():
    """text_analysis.c compiles"""
    check50.c.compile("text_analysis.c", lcs50=True)


@check50.check(compiles)
def test_simple():
    """handles simple input: 'Hello world'"""
    output = check50.run("./text_analysis").stdin("Hello world").stdout()
    
    # Check for basic statistics
    check_contains(output, r"Characters:\s*11", "character count")
    check_contains(output, r"Words:\s*2", "word count")
    check_contains(output, r"Sentences:\s*0", "sentence count (no punctuation)")


@check50.check(compiles)
def test_single_sentence():
    """handles single sentence: 'The cat sat.'"""
    output = check50.run("./text_analysis").stdin("The cat sat.").stdout()
    
    check_contains(output, r"Characters:\s*13", "character count")
    check_contains(output, r"Words:\s*3", "word count")
    check_contains(output, r"Sentences:\s*1", "sentence count")


@check50.check(compiles)
def test_repeated_words():
    """detects repeated words in 'The cat and the dog'"""
    output = check50.run("./text_analysis").stdin("The cat and the dog").stdout()
    
    # Should detect "the" appears twice (case-insensitive)
    if not re.search(r"the.*2\s*time", output.lower()):
        raise check50.Failure("should identify 'the' appears 2 times")


@check50.check(compiles)
def test_multiple_sentences():
    """handles multiple sentences with different punctuation"""
    text = "Hello! How are you? I am fine."
    output = check50.run("./text_analysis").stdin(text).stdout()
    
    check_contains(output, r"Sentences:\s*3", "sentence count")


@check50.check(compiles)
def test_character_frequency():
    """tracks character frequency for 'aaa bbb ccc'"""
    output = check50.run("./text_analysis").stdin("aaa bbb ccc").stdout()
    
    # Each letter appears 3 times
    lower_output = output.lower()
    if "a" not in lower_output or "3" not in output:
        raise check50.Failure("should show character frequencies")


@check50.check(compiles)
def test_average_word_length():
    """calculates average word length for 'I am good'"""
    # Words: "I" (1), "am" (2), "good" (4) -> average = 2.33
    output = check50.run("./text_analysis").stdin("I am good").stdout()
    
    # Look for average between 2.0 and 2.5
    if not re.search(r"[Aa]verage.*2\.[0-9]", output):
        raise check50.Failure("should calculate average word length (expected ~2.3)")


@check50.check(compiles)
def test_longest_word():
    """identifies longest word in 'The quick brown fox'"""
    output = check50.run("./text_analysis").stdin("The quick brown fox").stdout()
    
    # "quick" and "brown" are both 5 letters (either is acceptable)
    if not re.search(r"[Ll]ongest.*5", output):
        raise check50.Failure("should identify longest word length (5 letters)")


@check50.check(compiles)
def test_readability():
    """calculates readability index"""
    text = "The cat sat on the mat. The dog ran fast."
    output = check50.run("./text_analysis").stdin(text).stdout()
    
    # Should have some readability calculation
    if not re.search(r"[Rr]eadability|[Ii]ndex|[Gg]rade", output):
        raise check50.Failure("should calculate readability index")


@check50.check(compiles)
def test_case_insensitive():
    """treats words case-insensitively: 'The THE the'"""
    output = check50.run("./text_analysis").stdin("The THE the").stdout()
    
    # Should detect "the" appears 3 times
    if not re.search(r"the.*3\s*time", output.lower()):
        raise check50.Failure("should count 'The', 'THE', and 'the' as same word (3 times)")


@check50.check(compiles)
def test_no_repeated_words():
    """handles text with no repeated words: 'Each word is unique'"""
    output = check50.run("./text_analysis").stdin("Each word is unique").stdout()
    
    # Should handle gracefully - either show nothing or explicitly state no repeats
    # Just verify it runs without error and produces output
    if len(output) < 20:
        raise check50.Failure("should produce meaningful output even with no repeated words")


@check50.check(compiles)
def test_complex_text():
    """handles complex text with all features"""
    text = "The quick brown fox jumps over the lazy dog! The fox was very quick."
    output = check50.run("./text_analysis").stdin(text).stdout()
    
    # Verify key statistics are present
    check_contains(output, r"Characters:\s*7[0-9]", "character count")
    check_contains(output, r"Words:\s*1[34]", "word count")
    check_contains(output, r"Sentences:\s*2", "sentence count")
    
    # Should detect repeated words: "the", "fox", "quick"
    lower_output = output.lower()
    repeated_count = 0
    if "the" in lower_output and "2" in output:
        repeated_count += 1
    if "fox" in lower_output and "2" in output:
        repeated_count += 1
    if "quick" in lower_output and "2" in output:
        repeated_count += 1
    
    if repeated_count < 2:
        raise check50.Failure("should detect multiple repeated words")


def check_contains(output, pattern, description):
    """Helper function to check if output contains pattern"""
    if not re.search(pattern, output):
        raise check50.Failure(f"output should contain {description}")
