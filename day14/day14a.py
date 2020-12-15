import re
from typing import List


SET_RE = re.compile(r'^mem\[(\d+)\] = (\d+)$')


def solve(program: str) -> int:
    mask = '0' * 36
    mem = {}
    for line in program.strip().splitlines():
        if line.startswith('mask = '):
            mask = line.split()[2]
            continue
        m = SET_RE.match(line)
        assert m, line
        addr = int(m.group(1))
        value_bin = bin(int(m.group(2)))[2:].rjust(36, '0')
        for i, m in enumerate(mask):
            if m != 'X':
                value_bin = value_bin[:i] + m + value_bin[i+1:]
        value = int(value_bin, 2)
        mem[addr] = value
    return sum(mem.values())


def test_solve():
    assert solve("""mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0
""") == 165


def main():
    with open('day14.txt') as f:
        program = f.read()
    print(solve(program))


if __name__ == '__main__':
    main()
