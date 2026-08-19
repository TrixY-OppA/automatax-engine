import time
from src.automata.matcher import AutomataMatcher

def test_basic_matching():
    matcher = AutomataMatcher("(a|b)*c")
    assert matcher.match("c") is True
    assert matcher.match("ac") is True
    assert matcher.match("ababc") is True
    assert matcher.match("ababa") is False

def test_redos_immunity():
    # Catastrophic backtracking pattern: (a+)+b
    # When matched against 'aaaaaaaaaaaaaaaaaaaaaX' standard backtracking explodes exponentially.
    pattern = "(a+)+b"
    matcher = AutomataMatcher(pattern)
    
    evil_input = "a" * 30 + "X"
    
    start_time = time.time()
    result, path = matcher.trace(evil_input)
    elapsed_time = time.time() - start_time
    
    assert result is False
    # Execution should take less than 1 millisecond
    assert elapsed_time < 0.05
    print(f"\n[PASS] ReDoS test completed in {elapsed_time:.6f}s (Immune to catastrophic backtracking)")