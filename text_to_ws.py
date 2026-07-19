"""
text_to_ws.py - Converts arbitrary text into a Whitespace program.

Each character is pushed as its ASCII value, then output as a character.
This produces the most compact Whitespace representation for text output.
"""

import sys

S = ' '    # Space
T = '\t'   # Tab
LF = '\n'  # Linefeed


def encode_number(n):
    """Encode a positive integer as a Whitespace number."""
    result = S  # positive sign
    bits = bin(n)[2:]
    for b in bits:
        result += T if b == '1' else S
    result += LF
    return result


def push(n):
    """Push instruction: SS followed by number."""
    return S + S + encode_number(n)


def output_char():
    """Output top of stack as character: TLSS."""
    return T + LF + S + S


def end():
    """End program: LLL."""
    return LF + LF + LF


def text_to_whitespace(text):
    """Convert a text string to a Whitespace program."""
    program = ''
    for ch in text:
        program += push(ord(ch))
        program += output_char()
    program += end()
    return program


def text_file_to_ws(input_path, output_path):
    """Read a text file and write its Whitespace equivalent."""
    with open(input_path, 'r', encoding='utf-8') as f:
        text = f.read()

    ws_program = text_to_whitespace(text)

    with open(output_path, 'w', encoding='utf-8', newline='') as f:
        f.write(ws_program)

    print(f"Converted {len(text)} characters -> {len(ws_program)} whitespace bytes")
    print(f"Written to {output_path}")
    return ws_program


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python text_to_ws.py <input.txt> <output.ws>")
        sys.exit(1)

    text_file_to_ws(sys.argv[1], sys.argv[2])
