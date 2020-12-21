from typing import List, NamedTuple

Ticket = List[int]


class Range(NamedTuple):
    min: int
    max: int

    def __contains__(self, i: int) -> bool:
        return self.min <= i <= self.max


class Field(NamedTuple):
    name: str
    ranges: List[Range]

    def __contains__(self, i: int) -> bool:
        return any(i in r for r in self.ranges)


class Problem(NamedTuple):
    fields: List[Field]
    mine: Ticket
    theirs: List[Ticket]


def solve(fields: List[Field], mine: Ticket, theirs: List[Ticket]) -> int:
    error = 0
    for ticket in theirs:
        for value in ticket:
            for field in fields:
                if value in field:
                    break
            else:
                error += value
    return error


def parse(text: str) -> Problem:
    parts = text.rstrip().split('\n\n')
    fields = []
    for line in parts[0].splitlines():
        name, spec = line.split(': ')
        range1, range2 = spec.split(' or ')
        fields.append(Field(
            name=name,
            ranges=[
                Range(*map(int, range1.split('-'))),
                Range(*map(int, range2.split('-'))),
            ]))
    line = parts[1].splitlines()[1]
    mine = [int(s) for s in line.split(',')]
    theirs = []
    for line in parts[2].splitlines()[1:]:
        theirs.append([int(s) for s in line.split(',')])
    return Problem(fields=fields, mine=mine, theirs=theirs)


def test_solve():
    assert solve(*parse("""class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12
""")) == 71


def main():
    with open('day16.txt') as f:
        problem = parse(f.read())
    print(solve(*problem))


if __name__ == '__main__':
    main()
