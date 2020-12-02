import re
from typing import List, NamedTuple, Optional, Tuple


class Policy(NamedTuple):
    char: str
    min: int
    max: int


class Case(NamedTuple):
    policy: Policy
    password: str


_CASE_RE = re.compile(r'^(?P<min>\d+)-(?P<max>\d+) (?P<char>.): (?P<password>.*)$')


def parse(input: str) -> List[Case]:
    cases = []
    for line in input.splitlines():
        m = _CASE_RE.match(line)
        assert m, line
        cases.append(Case(
            policy=Policy(
                char=m.group('char'),
                min=int(m.group('min')),
                max=int(m.group('max'))),
            password=m.group('password')))
    return cases


def valid(case: Case) -> bool:
    p = case.policy
    return p.min <= case.password.count(p.char) <= p.max


def solve(cases: List[Case]) -> int:
    return sum(1 for case in cases if valid(case))


def test_solve():
    input = """1-3 a: abcde
1-3 b: cdefg
2-9 c: ccccccccc
"""
    assert solve(parse(input)) == 2


def main():
    with open('day02.txt') as f:
        input = f.read()
    print(solve(parse(input)))


if __name__ == '__main__':
    main()
