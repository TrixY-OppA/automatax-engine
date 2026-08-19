from src.automata.parser import parse_regex_to_postfix

def test_basic_postfix():
    assert parse_regex_to_postfix("ab") == "ab."
    assert parse_regex_to_postfix("a|b") == "ab|"
    assert parse_regex_to_postfix("a*b") == "a*b."
    assert parse_regex_to_postfix("(a|b)*c") == "ab|*c."
    print("[PASS] Parser working accurately!")

if __name__ == "__main__":
    test_basic_postfix()