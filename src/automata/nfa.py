"""
NFA implementation using Thompson's Construction Algorithm.
"""
from typing import Dict, List, Optional


class State:
    _id_counter = 0

    def __init__(self, is_end: bool = False):
        self.id = State._id_counter
        State._id_counter += 1
        self.is_end = is_end
        self.transitions: Dict[str, List['State']] = {}
        self.epsilon_transitions: List['State'] = []

    def add_transition(self, symbol: str, to_state: 'State'):
        if symbol not in self.transitions:
            self.transitions[symbol] = []
        self.transitions[symbol].append(to_state)

    def add_epsilon_transition(self, to_state: 'State'):
        self.epsilon_transitions.append(to_state)

    def __repr__(self):
        return f"State({self.id}, is_end={self.is_end})"


class NFA:
    def __init__(self, start: State, end: State):
        self.start = start
        self.end = end

    @classmethod
    def from_literal(cls, char: str) -> 'NFA':
        start = State()
        end = State(is_end=True)
        start.add_transition(char, end)
        return cls(start, end)

    @classmethod
    def concat(cls, nfa1: 'NFA', nfa2: 'NFA') -> 'NFA':
        nfa1.end.is_end = False
        nfa1.end.add_epsilon_transition(nfa2.start)
        return cls(nfa1.start, nfa2.end)

    @classmethod
    def union(cls, nfa1: 'NFA', nfa2: 'NFA') -> 'NFA':
        start = State()
        end = State(is_end=True)

        nfa1.end.is_end = False
        nfa2.end.is_end = False

        start.add_epsilon_transition(nfa1.start)
        start.add_epsilon_transition(nfa2.start)

        nfa1.end.add_epsilon_transition(end)
        nfa2.end.add_epsilon_transition(end)

        return cls(start, end)

    @classmethod
    def kleene_star(cls, nfa: 'NFA') -> 'NFA':
        start = State()
        end = State(is_end=True)

        nfa.end.is_end = False

        start.add_epsilon_transition(nfa.start)
        start.add_epsilon_transition(end)

        nfa.end.add_epsilon_transition(nfa.start)
        nfa.end.add_epsilon_transition(end)

        return cls(start, end)

    @classmethod
    def plus(cls, nfa: 'NFA') -> 'NFA':
        start = State()
        end = State(is_end=True)

        nfa.end.is_end = False

        start.add_epsilon_transition(nfa.start)
        nfa.end.add_epsilon_transition(nfa.start)
        nfa.end.add_epsilon_transition(end)

        return cls(start, end)


def build_nfa_from_postfix(postfix_expr: str) -> Optional[NFA]:
    """
    Evaluates a postfix regular expression using a stack to build an NFA.
    """
    if not postfix_expr:
        start = State()
        end = State(is_end=True)
        start.add_epsilon_transition(end)
        return NFA(start, end)

    stack: List[NFA] = []

    for char in postfix_expr:
        if char == '.':
            nfa2 = stack.pop()
            nfa1 = stack.pop()
            stack.append(NFA.concat(nfa1, nfa2))
        elif char == '|':
            nfa2 = stack.pop()
            nfa1 = stack.pop()
            stack.append(NFA.union(nfa1, nfa2))
        elif char == '*':
            nfa = stack.pop()
            stack.append(NFA.kleene_star(nfa))
        elif char == '+':
            nfa = stack.pop()
            stack.append(NFA.plus(nfa))
        else:
            stack.append(NFA.from_literal(char))

    return stack.pop()