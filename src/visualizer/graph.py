"""
State Machine Graphviz Generator.
Renders NFA and DFA state transition graphs to SVG/PNG.
"""
from typing import Optional, List
import graphviz
from src.automata.dfa import DFA, DFAState
from src.automata.nfa import NFA, State as NFAState


class AutomataVisualizer:
    @staticmethod
    def render_dfa(dfa: DFA, output_filename: str = "dfa_graph", active_path: Optional[List[int]] = None) -> str:
        """
        Renders a DFA to an SVG/PNG graph.
        If active_path is provided, highlights traversed states and edges.
        """
        dot = graphviz.Digraph(name="DFA", format="svg")
        dot.attr(rankdir="LR")

        # Fake initial state arrow
        dot.node("start_fake", shape="none", label="")
        dot.edge("start_fake", f"q{dfa.start.id}")

        for state in dfa.states:
            state_name = f"q{state.id}"
            
            # Formatting: doublecircle for accepting states
            shape = "doublecircle" if state.is_end else "circle"
            color = "black"
            fillcolor = "white"
            style = "solid"

            # Highlight if in active path
            if active_path and state.id in active_path:
                color = "#10B981"  # Emerald green
                fillcolor = "#D1FAE5"
                style = "filled"

            dot.node(state_name, shape=shape, color=color, fillcolor=fillcolor, style=style)

            for symbol, target_state in state.transitions.items():
                target_name = f"q{target_state.id}"
                edge_color = "#10B981" if (active_path and state.id in active_path and target_state.id in active_path) else "#6B7280"
                dot.edge(state_name, target_name, label=f" {symbol} ", color=edge_color)

        return dot.render(output_filename, cleanup=True)

    @staticmethod
    def render_nfa(nfa: NFA, output_filename: str = "nfa_graph") -> str:
        """
        Renders an NFA with epsilon transitions to SVG/PNG.
        """
        dot = graphviz.Digraph(name="NFA", format="svg")
        dot.attr(rankdir="LR")

        dot.node("start_fake", shape="none", label="")
        dot.edge("start_fake", f"s{nfa.start.id}")

        visited = set()
        stack = [nfa.start]

        while stack:
            curr = stack.pop()
            if curr.id in visited:
                continue
            visited.add(curr.id)

            shape = "doublecircle" if curr.is_end else "circle"
            dot.node(f"s{curr.id}", shape=shape)

            for sym, targets in curr.transitions.items():
                for target in targets:
                    dot.edge(f"s{curr.id}", f"s{target.id}", label=f" {sym} ")
                    stack.append(target)

            for target in curr.epsilon_transitions:
                dot.edge(f"s{curr.id}", f"s{target.id}", label=" ε ", style="dashed", color="#9CA3AF")
                stack.append(target)

        return dot.render(output_filename, cleanup=True)