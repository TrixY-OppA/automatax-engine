"""
Regex Infix to Postfix Converter
Handles explicit insertion of concatenation operator ('.') and Shunting-Yard parsing.
"""

OPERATORS = {'*', '+', '?', '|', '.'}
PRECEDENCE = {
    '*': 3,
    '+': 3,
    '?': 3,
    '.': 2,
    '|': 1
}

def insert_explicit_concat(regex: str) -> str:
    """
    Inserts explicit '.' for concatenation:
    - Between literal & literal: 'ab' -> 'a.b'
    - Between literal & '(': 'a(' -> 'a.('
    - Between ')' & literal: ')a' -> ').a'
    - Between '*', '+', '?' & literal/'(': 'a*b' -> 'a*.b'
    """
    output = []
    for i in range(len(regex)):
        c1 = regex[i]
        output.append(c1)
        if i + 1 < len(regex):
            c2 = regex[i + 1]
            if c1 not in '(|' and c2 not in '|)*+?':
                output.append('.')
    return "".join(output)

def parse_regex_to_postfix(regex: str) -> str:
    """
    Converts infix regex to postfix using Dijkstra's Shunting-Yard algorithm.
    """
    if not regex:
        return ""
    
    formatted = insert_explicit_concat(regex)
    postfix = []
    operator_stack = []

    for char in formatted:
        if char == '(':
            operator_stack.append(char)
        elif char == ')':
            while operator_stack and operator_stack[-1] != '(':
                postfix.append(operator_stack.pop())
            if operator_stack and operator_stack[-1] == '(':
                operator_stack.pop()  # Pop '('
            else:
                raise ValueError("Mismatched parentheses in regex")
        elif char in OPERATORS:
            # Unary operators (*, +, ?) have right-to-left associativity, binary left-to-right
            while (operator_stack and operator_stack[-1] != '(' and
                   PRECEDENCE.get(operator_stack[-1], 0) >= PRECEDENCE.get(char, 0)):
                postfix.append(operator_stack.pop())
            operator_stack.append(char)
        else:
            # Literal character
            postfix.append(char)

    while operator_stack:
        op = operator_stack.pop()
        if op == '(':
            raise ValueError("Mismatched parentheses in regex")
        postfix.append(op)

    return "".join(postfix)