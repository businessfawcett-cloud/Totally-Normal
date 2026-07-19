import sys
import os

def load_program(filename):
    with open(filename, 'rb') as f:
        return f.read().decode('utf-8')

def tokenize(program):
    tokens = []
    i = 0
    while i < len(program):
        c = program[i]
        if c == ' ':
            tokens.append('S')
        elif c == '\t':
            tokens.append('T')
        elif c == '\n':
            tokens.append('L')
        i += 1
    return tokens

def parse_number(tokens, pos):
    if tokens[pos] == 'S':
        sign = 1
    else:
        sign = -1
    pos += 1
    value = 0
    while tokens[pos] != 'L':
        value = value * 2 + (1 if tokens[pos] == 'T' else 0)
        pos += 1
    return sign * value, pos + 1

def run(tokens):
    stack = []
    heap = {}
    call_stack = []
    labels = {}
    output = []
    pos = 0

    # First pass: find labels
    i = 0
    while i < len(tokens):
        if tokens[i] == 'L':
            if i + 1 < len(tokens) and tokens[i+1] == 'S':
                if i + 2 < len(tokens) and tokens[i+2] == 'S':
                    # Label definition: LSS<number>
                    num, i = parse_number(tokens, i + 3)
                    labels[num] = i
                    continue
        i += 1

    # Second pass: execute
    pos = 0
    while pos < len(tokens):
        if tokens[pos] == 'S':
            if pos + 1 < len(tokens) and tokens[pos+1] == 'S':
                # Push number
                num, pos = parse_number(tokens, pos + 2)
                stack.append(num)
            elif pos + 1 < len(tokens) and tokens[pos+1] == 'L':
                # Duplicate top
                stack.append(stack[-1])
                pos += 2
            elif pos + 1 < len(tokens) and tokens[pos+1] == 'T':
                if pos + 2 < len(tokens) and tokens[pos+2] == 'S':
                    # Swap top two
                    stack[-1], stack[-2] = stack[-2], stack[-1]
                    pos += 3
                elif pos + 2 < len(tokens) and tokens[pos+2] == 'L':
                    # Pop and discard
                    stack.pop()
                    pos += 3
        elif tokens[pos] == 'T':
            if pos + 1 < len(tokens) and tokens[pos+1] == 'S':
                if pos + 2 < len(tokens) and tokens[pos+2] == 'S':
                    if pos + 3 < len(tokens) and tokens[pos+3] == 'S':
                        # Add
                        b, a = stack.pop(), stack.pop()
                        stack.append(a + b)
                        pos += 4
                    elif pos + 3 < len(tokens) and tokens[pos+3] == 'T':
                        # Subtract
                        b, a = stack.pop(), stack.pop()
                        stack.append(a - b)
                        pos += 4
                    elif pos + 3 < len(tokens) and tokens[pos+3] == 'L':
                        # Multiply
                        b, a = stack.pop(), stack.pop()
                        stack.append(a * b)
                        pos += 4
                elif pos + 2 < len(tokens) and tokens[pos+2] == 'T':
                    if pos + 3 < len(tokens) and tokens[pos+3] == 'S':
                        # Divide
                        b, a = stack.pop(), stack.pop()
                        stack.append(int(a / b))
                        pos += 4
                    elif pos + 3 < len(tokens) and tokens[pos+3] == 'T':
                        # Modulo
                        b, a = stack.pop(), stack.pop()
                        stack.append(a % b)
                        pos += 4
            elif pos + 1 < len(tokens) and tokens[pos+1] == 'T':
                if pos + 2 < len(tokens) and tokens[pos+2] == 'S':
                    # Store
                    val = stack.pop()
                    addr = stack.pop()
                    heap[addr] = val
                    pos += 3
                elif pos + 2 < len(tokens) and tokens[pos+2] == 'T':
                    # Retrieve
                    addr = stack.pop()
                    stack.append(heap.get(addr, 0))
                    pos += 3
            elif pos + 1 < len(tokens) and tokens[pos+1] == 'L':
                if pos + 2 < len(tokens) and tokens[pos+2] == 'S':
                    if pos + 3 < len(tokens) and tokens[pos+3] == 'S':
                        # Output character
                        val = stack.pop()
                        output.append(chr(val))
                        pos += 4
                    elif pos + 3 < len(tokens) and tokens[pos+3] == 'T':
                        # Output number
                        val = stack.pop()
                        output.append(str(val))
                        pos += 4
        elif tokens[pos] == 'L':
            if pos + 1 < len(tokens) and tokens[pos+1] == 'S':
                if pos + 2 < len(tokens) and tokens[pos+2] == 'S':
                    # Label definition - skip
                    _, pos = parse_number(tokens, pos + 3)
                elif pos + 2 < len(tokens) and tokens[pos+2] == 'T':
                    # Call subroutine
                    num, pos = parse_number(tokens, pos + 3)
                    call_stack.append(pos)
                    pos = labels[num]
                elif pos + 2 < len(tokens) and tokens[pos+2] == 'L':
                    # Jump
                    num, pos = parse_number(tokens, pos + 3)
                    pos = labels[num]
            elif pos + 1 < len(tokens) and tokens[pos+1] == 'T':
                if pos + 2 < len(tokens) and tokens[pos+2] == 'S':
                    # Jump if zero
                    num, pos = parse_number(tokens, pos + 3)
                    if stack.pop() == 0:
                        pos = labels[num]
                elif pos + 2 < len(tokens) and tokens[pos+2] == 'T':
                    # Jump if negative
                    num, pos = parse_number(tokens, pos + 3)
                    if stack.pop() < 0:
                        pos = labels[num]
                elif pos + 2 < len(tokens) and tokens[pos+2] == 'L':
                    # Return
                    pos = call_stack.pop()
            elif pos + 1 < len(tokens) and tokens[pos+1] == 'L':
                if pos + 2 < len(tokens) and tokens[pos+2] == 'L':
                    # End
                    break
                else:
                    pos += 1
            else:
                pos += 1
        else:
            pos += 1

    return ''.join(output)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python run_ws.py <program.ws>')
        sys.exit(1)
    
    program = load_program(sys.argv[1])
    tokens = tokenize(program)
    result = run(tokens)
    sys.stdout.buffer.write(result.encode('utf-8'))
