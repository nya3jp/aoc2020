from typing import List, Tuple


def score(deck: List[int]):
    n = len(deck)
    return sum(card * (n - i) for i, card in enumerate(deck))


def solve(decks: Tuple[List[int], List[int]]) -> int:
    while decks[0] and decks[1]:
        card0 = decks[0].pop(0)
        card1 = decks[1].pop(0)
        if card0 > card1:
            decks[0].extend([card0, card1])
        else:
            decks[1].extend([card1, card0])
    return score(decks[0] or decks[1])


def parse(input: str) -> Tuple[List[int], List[int]]:
    section0, section1 = input.strip().split('\n\n')
    return [int(s) for s in section0.splitlines()[1:]], [int(s) for s in section1.splitlines()[1:]]


def test_solve():
    assert solve(parse("""Player 1:
9
2
6
3
1

Player 2:
5
8
4
7
10
""")) == 306


def main():
    with open('day22.txt') as f:
        decks = parse(f.read())
    print(solve(decks))


if __name__ == '__main__':
    main()
