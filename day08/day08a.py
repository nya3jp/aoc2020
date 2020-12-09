import io
from typing import List, NamedTuple, TextIO


class Instruction(NamedTuple):
    op: str
    arg: int


Program = List[Instruction]


def solve(program: Program) -> int:
    seen = set()
    pc = 0
    acc = 0
    while True:
        if pc in seen:
            return acc
        seen.add(pc)
        op, arg = program[pc]
        if op == 'nop':
            pc += 1
        elif op == 'jmp':
            pc += arg
        elif op == 'acc':
            acc += arg
            pc += 1
        else:
            raise Exception('Unknown instruction: %s %d' % (op, arg))


def parse(f: TextIO) -> Program:
    program = []
    for line in f:
        op, arg_str = line.split()
        program.append(Instruction(op, int(arg_str)))
    return program


def test_solve():
    program = parse(io.StringIO("""nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6
"""))
    assert solve(program) == 5


def main():
    with open('day08.txt') as f:
        program = parse(f)
    print(solve(program))


if __name__ == '__main__':
    main()
