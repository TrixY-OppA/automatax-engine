"""
DFA implementation and Subset Construction (NFA -> DFA).
"""
from typing import Dict, Set, FrozenSet, List
from collections import deque
from src.automata.nfa import State as NFAState, NFA


class DFAState:
    _id_counter = 0

    def __init__(self, nfa_states: FrozenSet[NFAState], is_end: bool = False):
        self.id = DFAState._id_counter
        DFAState._id_counter += 1
        self.nfa_states = nfa_states
        self.is_end = is_end
        self.transitions: Dict[str, 'DFAState'] = {}

    def add_transition(self, symbol: str, to_state: 'DFAState'):
        self.transitions[symbol] = to_state

    def __repr__(self):
        return f"DFAState(q{self.id}, is_end={self.is_end})"


class DFA:
    def __init__(self, start: DFAState, alphabet: Set[str], states: List[DFAState]):
        self.start = start
        self.alphabet = alphabet
        self.states = states

    def get_end_states(self) -> List[DFAState]:
        return [s for s in self.states if s.is_end]


def epsilon_closure(states: Set[NFAState]) -> FrozenSet[NFAState]:
    closure = set(states)
    queue = deque(states)

    while queue:
        current = queue.popleft()
        for next_state in current.epsilon_transitions:
            if next_state not in closure:
                closure.add(next_state)
                queue.append(next_state)

    return frozenset(closure)


def get_alphabet(nfa: NFA) -> Set[str]:
    alphabet = set()
    visited = set()
    queue = deque([nfa.start])

    while queue:
        curr = queue.popleft()
        if curr.id in visited:
            continue
        visited.add(curr.id)

        for sym, next_states in curr.transitions.items():
            alphabet.add(sym)
            for ns in next_states:
                queue.append(ns)

        for ns in curr.epsilon_transitions:
            queue.append(ns)

    return alphabet


def nfa_to_dfa(nfa: NFA) -> DFA:
    DFAState._id_counter = 0

    alphabet = get_alphabet(nfa)
    start_closure = epsilon_closure({nfa.start})

    is_start_end = any(s.is_end for s in start_closure)
    start_dfa_state = DFAState(start_closure, is_end=is_start_end)

    dfa_states_map: Dict[FrozenSet[NFAState], DFAState] = {
        start_closure: start_dfa_state
    }
    unmarked_states = deque([start_closure])
    all_dfa_states = [start_dfa_state]

    while unmarked_states:
        current_set = unmarked_states.popleft()
        current_dfa_state = dfa_states_map[current_set]

        for symbol in alphabet:
            move_set = set()
            for state in current_set:
                if symbol in state.transitions:
                    move_set.update(state.transitions[symbol])

            if not move_set:
                continue

            target_closure = epsilon_closure(move_set)

            if target_closure not in dfa_states_map:
                is_target_end = any(s.is_end for s in target_closure)
                new_dfa_state = DFAState(target_closure, is_end=is_target_end)
                dfa_states_map[target_closure] = new_dfa_state
                all_dfa_states.append(new_dfa_state)
                unmarked_states.append(target_closure)

            current_dfa_state.add_transition(symbol, dfa_states_map[target_closure])

    return DFA(start=start_dfa_state, alphabet=alphabet, states=all_dfa_states)