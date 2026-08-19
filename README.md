# AutomataX ⚡

> **Deterministic Finite Automaton (DFA) Regex Engine & Visual Security Verifier** built from first principles in Python.

AutomataX parses regular expressions, compiles them via Thompson's Construction to $\varepsilon$-NFAs, and transforms them into deterministic finite state machines via Subset Construction. It provides guaranteed linear-time matching ($O(n)$) immune to **Regular Expression Denial of Service (ReDoS)** catastrophic backtracking attacks.

---

## 📌 Architecture & Theoretical Pipeline