<div align="center">

# AutomataX Engine

**High-Performance Regex-to-DFA Compiler & State Visualizer**
*Guaranteed O(n) Linear-Time Matching | ReDoS Immune | Theoretical Automata from Scratch*

[![CI Pipeline](https://github.com/TrixY-OppA/automatx-engine/actions/workflows/ci.yml/badge.svg)](https://github.com/TrixY-OppA/automatx-engine/actions)
![Python Version](https://img.shields.io/badge/Python-3.9%20%7C%203.11%20%7C%203.14-blue?logo=python&logoColor=white)
![Security Focus](https://img.shields.io/badge/Security-ReDoS%20Immune-success?style=flat&logo=shield)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

</div>

---

## Overview

Standard backtracking regex engines (like standard Python `re`, JavaScript RegExp, PCRE) suffer from exponential time complexity $\mathcal{O}(2^n)$ on non-deterministic ambiguous patterns—making them vulnerable to **Catastrophic Backtracking / Regular Expression Denial of Service (ReDoS)**.

**AutomataX** compiles regular expressions into deterministic finite state machines via first-principles automata theory:

1. **Dijkstra's Shunting-Yard Algorithm** with explicit concatenation insertion.
2. **Thompson's Construction** to build composable $\varepsilon$-NFAs.
3. **Subset (Powerset) Construction** with $\varepsilon$-closure resolution to compile pure, deterministic DFAs.
4. **Zero-Backtracking Engine** that validates streaming payloads in strict $\mathcal{O}(n)$ time.

---

## Architecture Pipeline

```
Infix Regex: (a|b)*c
        │
        ▼   [Shunting-Yard Parser + Implicit Concat Detection]
Postfix Tokens: ab|*c.
        │
        ▼   [Thompson's Construction via State Graph Stack]
Composable ε-NFA
        │
        ▼   [Subset Construction + BFS ε-Closure Computation]
Deterministic Finite Automaton (DFA)
        │
        ├──────────────────────┬──────────────────────┐
        ▼                                      ▼
Linear O(n) Engine                    Graphviz Engine
[ReDoS Immune Matching]            [Render SVG/PNG State Diagrams]
```

---

## Performance: ReDoS Immunity Benchmark

Testing against the classic evil catastrophic backtracking regex pattern `(a+)+b` evaluated against non-matching repetitive payload `a^30 + 'X'`:

| Engine | Evaluation Algorithm | Time Complexity | Execution Time |
| :--- | :--- | :--- | :--- |
| **Standard Backtracking Engine** | Recursive Backtracking | $\mathcal{O}(2^n)$ (Exponential) | **Freezes / Timeout (>10s)** |
| **AutomataX DFA Engine** | Deterministic Graph Walk | $\mathcal{O}(n)$ (Strict Linear) | **~0.000005s (< 0.01ms)** |

---

## CLI Usage & Real-time Trace

### 1. Match Payload with Live State Traversal

```bash
python -m src.main -p "(a|b)*c" -t "ababc" -v
```

**Terminal Output Preview:**

```
AutomataX Security & Automata Engine        You, 3 minutes ago • Uncommitted changes

Compilation Summary
 _________________________________________
| Property           | Value              |
|--------------------|--------------------|
| Infix Regex        | (a|b)*c            |
| Postfix Expression | ab|*c.             |
| DFA State Count    | 4                  |
| Accepting States   | ['q1']             |
| Alphabet           | ['c', 'a', 'b']    |

── Execution Trace ──────────────────────────
Result: ACCEPTED (Match Found)
Input: 'ababc'
State Traversal Path: q0 -> q2 -> q3 -> q2 -> q3 -> q1
──────────────────────────────────────────────

✓ DFA graph exported to: dfa_output.svg
✓ NFA graph exported to: nfa_output.svg
```

---

## Installation & Setup

### Prerequisites

- Python 3.9+

### Graphviz Binary

**macOS:**
```bash
brew install graphviz
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install graphviz
```

**Windows:**
```bash
winget install graphviz
```

### Quickstart

```bash
# Clone the repository
git clone https://github.com/TrixY-OppA/automatx-engine.git
cd automatx-engine

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

## Test Suite

Run the full unit test suite, parser verification, and ReDoS benchmarks:

```bash
pytest -v -s
```

---

## License

Distributed under the MIT License. See `LICENSE` for more information.