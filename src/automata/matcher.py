"""
O(n) Linear Execution Matcher for Compiled DFAs.
Immune to ReDoS (Regular Expression Denial of Service).
"""
from typing import Tuple, List
from src.automata.parser import parse_regex_to_postfix
from src.automata.nfa import build_nfa_from_postfix
from src.automata.dfa import nfa_to_dfa, DFA, DFAState


class AutomataMatcher:
    def __init__(self, pattern: str):
        self.pattern = pattern
        self.postfix = parse_regex_to_postfix(pattern)
        self.nfa = build_nfa_from_postfix(self.postfix)
        self.dfa = nfa_to_dfa(self.nfa)

    def match(self, text: str) -> bool:
        """
        Tests if the exact text is accepted by the DFA.
        Time Complexity: O(len(text))
        """
        current_state = self.dfa.start
        for char in text:
            if char not in current_state.transitions:
                return False
            current_state = current_state.transitions[char]
        return current_state.is_end

    def trace(self, text: str) -> Tuple[bool, List[int]]:
        """
        Matches text while recording the state transition path (q0 -> q1 -> ...).
        Useful for visualization and debugging.
        """
        current_state = self.dfa.start
        path = [current_state.id]

        for char in text:
            if char not in current_state.transitions:
                return False, path
            current_state = current_state.transitions[char]
            path.append(current_state.id)

        return current_state.is_end, path