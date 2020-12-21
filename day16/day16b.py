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
    assert len(fields) == len(mine)
    n = len(fields)

    valids = [mine]
    for ticket in theirs:
        for value in ticket:
            for field in fields:
                if value in field:
                    break
            else:
                break  # invalid ticket
        else:
            valids.append(ticket)  # valid ticket

    def field_weight(field: Field) -> int:
        return sum(1 if all(ticket[ticket_index] in field for ticket in valids) else 0 for ticket_index in range(n))

    fields.sort(key=field_weight)

    # for field_index, field in enumerate(fields):
    #     for ticket_index in range(n):
    #         print('#' if all(ticket[ticket_index] in field for ticket in valids) else '.', end=' ')
    #     print()

    field_to_ticket = []

    def search() -> bool:
        field_index = len(field_to_ticket)
        if field_index == n:
            return True
        for ticket_index in range(n):
            if ticket_index in field_to_ticket:
                continue
            for ticket in valids:
                if ticket[ticket_index] not in fields[field_index]:
                    break
            else:
                field_to_ticket.append(ticket_index)
                if search():
                    return True
                field_to_ticket.pop()
        return False

    assert search()

    prod = 1
    for field, ticket_index in zip(fields, field_to_ticket):
        # print('%s: %d (%d-%d or %d-%d)' % (field.name, mine[ticket_index], field.ranges[0].min, field.ranges[0].max, field.ranges[1].min, field.ranges[1].max))
        if field.name.startswith('departure'):
            prod *= mine[ticket_index]

    return prod


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
    assert solve(*parse("""class: 0-1 or 4-19
row: 0-5 or 8-19
seat: 0-13 or 16-19

your ticket:
11,12,13

nearby tickets:
3,9,18
15,1,5
5,14,9
""")) == 1


def main():
    with open('day16.txt') as f:
        problem = parse(f.read())
    print(solve(*problem))


if __name__ == '__main__':
    main()
