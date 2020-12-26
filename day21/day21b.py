import functools
from typing import Dict, List, NamedTuple, Optional, Set


class Food(NamedTuple):
    ingredients: Set[str]
    allergens: Set[str]


def bipartite_match(graph: Dict[str, List[str]]) -> Dict[str, List[str]]:
    matching = {}

    def augment(left: Optional[str], visited: Set[str]) -> bool:
        if left is None:
            return True
        if left in visited:
            return False
        visited.add(left)
        for right in graph[left]:
            if augment(matching.get(right), visited):
                matching[right] = left
                return True
        return False

    for left in graph:
        augment(left, set())

    return matching


def solve(foods: List[Food]) -> str:
    all_allergens = functools.reduce(lambda a, b: a | b, (food.allergens for food in foods))
    all_ingredients = functools.reduce(lambda a, b: a | b, (food.ingredients for food in foods))
    graph = {
        allergen: functools.reduce(lambda a, b: a & b, (food.ingredients for food in foods if allergen in food.allergens))
        for allergen in all_allergens
    }

    matching = bipartite_match(graph)

    return ','.join(sorted(matching.keys(), key=lambda ingredient: matching[ingredient]))


def parse(input: str) -> List[Food]:
    foods = []
    for line in input.strip().splitlines():
        lhs, rhs = line.rstrip(')').split(' (contains ')
        foods.append(Food(ingredients=set(lhs.split()), allergens=set(rhs.split(', '))))
    return foods


def test_solve():
    assert solve(parse("""mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)
""")) == 'mxmxvkd,sqjhc,fvjkl'


def main():
    with open('day21.txt') as f:
        foods = parse(f.read())
    print(solve(foods))


if __name__ == '__main__':
    main()
