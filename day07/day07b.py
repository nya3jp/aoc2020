import re
from typing import Dict, List, NamedTuple, Tuple


ForwardGraph = Dict[str, List[Tuple[int, str]]]
BackwardGraph = Dict[str, List[str]]


RULE_RE = re.compile(
    r'^(?P<outer>\S+ \S+ bags) contain '
    r'(?:no other bags|(?P<inners>(?:\d+ \S+ \S+ bags?(?:, )?)+))\.$')


def parse_bag(s: str) -> (int, str):
    v = s.split()
    assert len(v) == 4
    return int(v[0]), ' '.join(v[1:3])


def parse(input: str) -> ForwardGraph:
    graph = {}
    for line in input.strip().splitlines():
        m = RULE_RE.match(line)
        assert m, line
        outer = parse_bag('0 ' + m.group('outer'))[1]
        inners_str = m.group('inners')
        inners = [parse_bag(s) for s in inners_str.split(', ')] if inners_str else []
        graph[outer] = inners
    return graph


def solve(graph: ForwardGraph) -> int:
    memo = {}

    def count(outer: str) -> int:
        if outer in memo:
            return memo[outer]
        cnt = 0
        for mul, inner in graph[outer]:
            cnt += mul * (1 + count(inner))
        memo[outer] = cnt
        return cnt

    return count('shiny gold')


def test_parse():
    assert parse("""light red bags contain 1 bright white bag, 2 muted yellow bags.
bright white bags contain 1 shiny gold bag.
faded blue bags contain no other bags.
""") == {
        'light red': [(1, 'bright white'), (2, 'muted yellow')],
        'bright white': [(1, 'shiny gold')],
        'faded blue': [],
    }


def test_solve():
    assert solve(parse("""light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags.
""")) == 32
    assert solve(parse("""shiny gold bags contain 2 dark red bags.
dark red bags contain 2 dark orange bags.
dark orange bags contain 2 dark yellow bags.
dark yellow bags contain 2 dark green bags.
dark green bags contain 2 dark blue bags.
dark blue bags contain 2 dark violet bags.
dark violet bags contain no other bags.
""")) == 126


def main():
    with open('day07.txt') as f:
        input = f.read()
    print(solve(parse(input)))


if __name__ == '__main__':
    main()
