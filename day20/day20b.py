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


def join_rows(rows: List[str]) -> str:
    return ''.join([rows[0][0]] + [row[1:] for row in rows])


def make_image(tileset: TileSet) -> Tile:
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

    image = []
    for tile_row in layout:
        for i in range(1, len(tile_row[0].pattern)-1):
            image.append(''.join(tile.pattern[i][1:-1] for tile in tile_row))
    #print(Tile(id=0, pattern=image))
    return Tile(id=0, pattern=image)


def parse(input: str) -> TileSet:
    tiles = []
    for section in input.strip().split('\n\n'):
        lines = section.splitlines()
        id = int(lines[0].split()[1].rstrip(':'))
        tiles.append(Tile(id=id, pattern=lines[1:]))
    return TileSet(tiles)


def test_make_image():
    assert make_image(parse("""Tile 2311:
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
""")).flip().rotate(1).pattern == """.#.#..#.##...#.##..#####
###....#.#....#..#......
##.##.###.#.#..######...
###.#####...#.#####.#..#
##.#....#.##.####...#.##
...########.#....#####.#
....#..#...##..#.#.###..
.####...#..#.....#......
#..#.##..#..###.#.##....
#.####..#.####.#.#.###..
###.#.#...#.######.#..##
#.####....##..########.#
##..##.#...#...#.#.#.#..
...#..#..#.#.##..###.###
.#.#....#.##.#...###.##.
###.#...#..#.##.######..
.#.#.###.##.##.#..#.##..
.####.###.#...###.#..#.#
..#.#..#..#.#.#.####.###
#..####...#.#.#.###.###.
#####..#####...###....##
#.##..#..#...#..####...#
.#.###..##..##..####.##.
...###...##...#...#..###""".splitlines()


SEA_MONSTER = """\
..................#.
#....##....##....###
.#..#..#..#..#..#...""".splitlines()


def fill_sea_monsters(image: Tile) -> None:
    h = len(SEA_MONSTER)
    w = len(SEA_MONSTER[0])
    for bi in range(len(image.pattern) - h + 1):
        for bj in range(len(image.pattern[0]) - w + 1):
            found = True
            for i in range(h):
                if not found:
                    break
                for j in range(w):
                    if SEA_MONSTER[i][j] == '#' and image.pattern[bi+i][bj+j] == '.':
                        found = False
                        break
            if found:
                for i in range(h):
                    for j in range(w):
                        if SEA_MONSTER[i][j] == '#':
                            image.pattern[bi+i] = image.pattern[bi+i][:bj+j] + 'O' + image.pattern[bi+i][bj+j+1:]


def solve(tileset: TileSet) -> int:
    image = make_image(tileset)
    for _ in range(2):
        for _ in range(4):
            fill_sea_monsters(image)
            image = image.rotate(1)
        image = image.flip()
    #print(image)
    return ''.join(image.pattern).count('#')


def test_solve():
    assert solve(parse("""Tile 2311:
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
..#.###...""")) == 273


def main():
    with open('day20.txt') as f:
        tileset = parse(f.read())
    print(solve(tileset))


if __name__ == '__main__':
    main()
