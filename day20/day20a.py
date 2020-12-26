from typing import Dict, List


NORTH, EAST, SOUTH, WEST = 0, 1, 2, 3


def normalize_dir(i: int) -> int:
    i %= 4
    if i < 0:
        i += 4
    return i


class Tile:
    id: int
    pattern: List[str]

    def __init__(self, id: int, pattern: List[str]):
        self.id = id
        self.pattern = pattern

    def edge(self, i: int) -> str:
        i = normalize_dir(i)
        if i == 0:
            return self.pattern[0]
        if i == 1:
            return ''.join(line[-1] for line in self.pattern)
        if i == 2:
            return ''.join(reversed(self.pattern[-1]))
        if i == 3:
            return ''.join(line[0] for line in reversed(self.pattern))
        assert False, i

    def __str__(self) -> str:
        return '[%d]\n%s' % (self.id, '\n'.join(self.pattern))

    # Rotates counterclockwise.
    def rotate(self, times) -> 'Tile':
        n = len(self.pattern)
        tile = self
        for _ in range(normalize_dir(times)):
            new_pattern = [''.join(tile.pattern[j][n-1-i] for j in range(n)) for i in range(n)]
            tile = Tile(id=tile.id, pattern=new_pattern)
        return tile

    # Flips horizontally.
    def flip(self) -> 'Tile':
        return Tile(id=self.id, pattern=[''.join(reversed(row)) for row in self.pattern])


class TileNotFound(Exception):
    pass


class TileSet:
    _tiles: Dict[int, Tile]

    def __init__(self, tiles: List[Tile]):
        self._tiles = {tile.id: tile for tile in tiles}

    def __len__(self) -> int:
        return len(self._tiles)

    def __getitem__(self, id: int) -> Tile:
        return self._tiles[id]

    def push(self, tile: Tile) -> None:
        assert tile.id not in self._tiles
        self._tiles[tile.id] = tile

    def pop(self, id: int) -> Tile:
        if id not in self._tiles:
            raise TileNotFound()
        return self._tiles.pop(id)

    def pop_corner(self) -> Tile:
        for corner in list(self._tiles.values()):
            self.pop(corner.id)
            adjs = []
            for i in range(4):
                try:
                    tile = self.pop_match(corner.edge(i))
                except TileNotFound:
                    pass
                else:
                    self.push(tile)
                    adjs.append(i)
            assert len(adjs) >= 2
            if len(adjs) == 2:
                if adjs == [0, 3]:
                    adjs.reverse()
                return corner.rotate(adjs[0] - 1)
            self.push(corner)
        raise TileNotFound()

    def pop_match(self, edge: str) -> Tile:
        flip_edge = ''.join(reversed(edge))
        # print('pop_match: looking for %s or %s' % (edge, flip_edge))
        for tile in self._tiles.values():
            for i in range(4):
                if tile.edge(i) == flip_edge:
                    self._tiles.pop(tile.id)
                    return tile.rotate(i)
                if tile.edge(i) == edge:
                    self._tiles.pop(tile.id)
                    return tile.rotate(i).flip()
        raise TileNotFound()


def solve(tileset: TileSet) -> int:
    start = tileset.pop_corner()
    layout = [[start]]
    # print(start)
    while True:
        try:
            tile = tileset.pop_match(layout[0][-1].edge(EAST)).rotate(1)
        except TileNotFound:
            break
        # print(tile)
        layout[0].append(tile)
    while len(tileset) > 0:
        # print('------------------------------')
        row = []
        for tile in layout[-1]:
            try:
                tile = tileset.pop_match(tile.edge(SOUTH))
            except TileNotFound:
                assert False, tile.edge(SOUTH)
            # print(tile)
            row.append(tile)
        layout.append(row)
    return layout[0][0].id * layout[0][-1].id * layout[-1][0].id * layout[-1][-1].id


def parse(input: str) -> TileSet:
    tiles = []
    for section in input.strip().split('\n\n'):
        lines = section.splitlines()
        id = int(lines[0].split()[1].rstrip(':'))
        tiles.append(Tile(id=id, pattern=lines[1:]))
    return TileSet(tiles)


def test_solve():
    tileset = parse("""Tile 2311:
..##.#..#.
##..#.....
#...##..#.
####.#...#
##.##.###.
##...#.###
.#.#.#..##
..#....#..
###...#.#.
..###..###

Tile 1951:
#.##...##.
#.####...#
.....#..##
#...######
.##.#....#
.###.#####
###.##.##.
.###....#.
..#.#..#.#
#...##.#..

Tile 1171:
####...##.
#..##.#..#
##.#..#.#.
.###.####.
..###.####
.##....##.
.#...####.
#.##.####.
####..#...
.....##...

Tile 1427:
###.##.#..
.#..#.##..
.#.##.#..#
#.#.#.##.#
....#...##
...##..##.
...#.#####
.#.####.#.
..#..###.#
..##.#..#.

Tile 1489:
##.#.#....
..##...#..
.##..##...
..#...#...
#####...#.
#..#.#.#.#
...#.#.#..
##.#...##.
..##.##.##
###.##.#..

Tile 2473:
#....####.
#..#.##...
#.##..#...
######.#.#
.#...#.#.#
.#########
.###.#..#.
########.#
##...##.#.
..###.#.#.

Tile 2971:
..#.#....#
#...###...
#.#.###...
##.##..#..
.#####..##
.#..####.#
#..#.#..#.
..####.###
..#.#.###.
...#.#.#.#

Tile 2729:
...#.#.#.#
####.#....
..#.#.....
....#..#.#
.##..##.#.
.#.####...
####.#.#..
##.####...
##..#.##..
#.##...##.

Tile 3079:
#.#.#####.
.#..######
..#.......
######....
####.#..#.
.#...#.##.
#.#####.##
..#.###...
..#.......
..#.###...
""")
    assert solve(tileset) == 20899048083289


def main():
    with open('day20.txt') as f:
        tileset = parse(f.read())
    print(solve(tileset))


if __name__ == '__main__':
    main()
