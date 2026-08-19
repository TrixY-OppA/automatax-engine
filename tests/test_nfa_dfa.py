from src.automata.parser import parse_regex_to_postfix
from src.automata.nfa import build_nfa_from_postfix
from src.automata.dfa import nfa_to_dfa

def test_full_nfa_to_dfa_pipeline():
    # Regex: (a|b)*c
    postfix = parse_regex_to_postfix("(a|b)*c")
    nfa = build_nfa_from_postfix(postfix)
    dfa = nfa_to_dfa(nfa)

    assert dfa.start is not None
    assert len(dfa.states) >= 2
    assert "a" in dfa.alphabet
    assert "b" in dfa.alphabet
    assert "c" in dfa.alphabet
    
    end_states = dfa.get_end_states()
    assert len(end_states) >= 1