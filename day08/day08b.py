import io
from typing import List, NamedTuple, Optional, TextIO


class Instruction(NamedTuple):
    op: str
    arg: int


Program = List[Instruction]


def run(program: Program) -> Optional[int]:
    seen = set()
    pc = 0
    acc = 0
    while pc < len(program):
        if pc in seen:
            return None
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
    if pc == len(program):
        return acc
    return None


def solve(program: Program) -> int:
    seq = []
    pc = 0
    while True:
        if pc in seq:
            break
        seq.append(pc)
        op, arg = program[pc]
        if op in ('nop', 'acc'):
            pc += 1
        elif op == 'jmp':
            pc += arg
        else:
            raise Exception('Unknown instruction: %s %d' % (op, arg))

    for pc in seq:
        op, arg = program[pc]
        if op == 'nop':
            fixed_program = program[:pc] + [Instruction('jmp', arg)] + program[pc+1:]
            acc = run(fixed_program)
            if acc is not None:
                # print('%d: %s -> %d' % (pc, 'jmp', acc))
                return acc
        elif op == 'jmp':
            fixed_program = program[:pc] + [Instruction('nop', arg)] + program[pc+1:]
            acc = run(fixed_program)
            if acc is not None:
                # print('%d: %s -> %d' % (pc, 'nop', acc))
                return acc

    raise Exception('Solution not found')


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
    assert solve(program) == 8


def main():
    with open('day08.txt') as f:
        program = parse(f)
    print(solve(program))


if __name__ == '__main__':
    main()
