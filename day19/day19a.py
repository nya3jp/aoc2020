import functools
from typing import Dict, List, NamedTuple, Tuple, Union


class CharMatch(NamedTuple):
    char: str


class RefMatch(NamedTuple):
    rule_id: int


class OrMatch(NamedTuple):
    left: 'Match'
    right: 'Match'


class SeqMatch(NamedTuple):
    left: 'Match'
    right: 'Match'


Match = Union[CharMatch, RefMatch, OrMatch, SeqMatch]


def solve_one(rules: Dict[int, Match], text: str) -> int:
    @functools.cache
    def solve_rule(i: int, j: int, rule_id: int) -> bool:
        return solve_match(i, j, rules[rule_id])

    def solve_match(i: int, j: int, m: Match) -> bool:
        if isinstance(m, CharMatch):
            return j - i == 1 and text[i] == m.char
        if isinstance(m, RefMatch):
            return solve_rule(i, j, m.rule_id)
        if isinstance(m, OrMatch):
            return solve_match(i, j, m.left) or solve_match(i, j, m.right)
        if isinstance(m, SeqMatch):
            for k in range(i + 1, j):
                if solve_match(i, k, m.left) and solve_match(k, j, m.right):
                    return True
            return False
        assert False, m

    return solve_rule(0, len(text), 0)


def solve(rules: Dict[int, Match], texts: List[str]) -> int:
    return sum(1 for text in texts if solve_one(rules, text))


def parse_match(expr: str) -> Match:
    if '|' in expr:
        return functools.reduce(OrMatch, (parse_match(subexpr) for subexpr in expr.split(' | ')))
    if ' ' in expr:
        return functools.reduce(SeqMatch, (parse_match(subexpr) for subexpr in expr.split()))
    if '"' in expr:
        return CharMatch(expr.strip('"'))
    return RefMatch(int(expr))


def parse(input: str) -> Tuple[Dict[int, Match], List[str]]:
    rules_section, texts_section = input.strip().split('\n\n')
    rules = {}
    for line in rules_section.splitlines():
        lhs, rhs = line.split(': ')
        rules[int(lhs)] = parse_match(rhs)
    return rules, texts_section.splitlines()


def test_solve():
    assert solve(*parse("""0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"

ababbb
bababa
abbbab
aaabbb
aaaabbb
""")) == 2


def main():
    with open('day19.txt') as f:
        rules, texts = parse(f.read())
    print(solve(rules, texts))


if __name__ == '__main__':
    main()
