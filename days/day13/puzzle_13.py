from collections import deque
from helpers import read_raw_entries, Point, path
import copy

class Cell:
    def __init__(self, value):
        self.value = value


class Cart:
    def __init__(self, orientation, loc):
        self.orientation = orientation
        self.turns = deque(['L', 'S', 'R'])
        self.loc = loc

    def move(self):
        if self.orientation == '<':
            self.loc.x -= 1
        elif self.orientation == '>':
            self.loc.x += 1
        elif self.orientation == '^':
            self.loc.y -= 1
        else:
            self.loc.y += 1

    def rotate(self, grid_cell):
        if grid_cell == '+':
            if self.turns[0] == 'L':
                if self.orientation == '<':
                    self.orientation = 'v'
                elif self.orientation == '>':
                    self.orientation = '^'
                elif self.orientation == '^':
                    self.orientation = '<'
                else:
                    self.orientation = '>'
            elif self.turns[0] == 'R':
                if self.orientation == '<':
                    self.orientation = '^'
                elif self.orientation == '>':
                    self.orientation = 'v'
                elif self.orientation == '^':
                    self.orientation = '>'
                else:
                    self.orientation = '<'
            self.turns.rotate(-1)
        elif grid_cell == '/':
            if self.orientation == '<':
                self.orientation = 'v'
            elif self.orientation == '>':
                self.orientation = '^'
            elif self.orientation == '^':
                self.orientation = '>'
            else:
                self.orientation = '<'
        elif grid_cell == '\\':
            if self.orientation == '<':
                self.orientation = '^'
            elif self.orientation == '>':
                self.orientation = 'v'
            elif self.orientation == '^':
                self.orientation = '<'
            else:
                self.orientation = '>'

    def collision(self, carts, remove_crashed_carts):
        for other in carts:
            if other == self:
                continue
            else:
                if self.loc.x == other.loc.x and self.loc.y == other.loc.y:
                    if remove_crashed_carts:
                        carts.remove(self)
                        carts.remove(other)
                    return True
        return False


def parse_map(input_path):
    grid = []
    lines = read_raw_entries(input_path, strip=False)

    for line in lines:
        grid.append(list(line))

    return grid


def print_map(map_grid, carts):
    temp_grid = copy.deepcopy(map_grid)

    for cart in carts:
        temp_grid[cart.loc.y][cart.loc.x] = cart.orientation

    for y in range(len(map_grid)):
        for x in range(len(map_grid[y])):
            print(temp_grid[y][x], end='')
        print('')


def solve_13(input_path, remove_crashed_carts=False):
    map_grid = parse_map(input_path)
    carts = []

    for y in range(0, len(map_grid)):
        for x in range(0, len(map_grid[0])):
            if map_grid[y][x] == '<' or map_grid[y][x] == '>':
                carts.append(Cart(map_grid[y][x], Point(x, y)))
                map_grid[y][x] = '-'
            elif map_grid[y][x] == '^' or map_grid[y][x] == 'v':
                carts.append(Cart(map_grid[y][x], Point(x, y)))
                map_grid[y][x] = '|'

    run = True
    result_loc = None
    while run:
        for cart in sorted(carts, key=lambda c: (c.loc.y, c.loc.x)):
            cart.move()
            if cart.collision(carts, remove_crashed_carts):
                if not remove_crashed_carts:
                    run = False
                    result_loc = Point(cart.loc.x, cart.loc.y)
                    # print_map(map_grid, carts)
                if len(carts) == 1:
                    run = False

            cart.rotate(map_grid[cart.loc.y][cart.loc.x])
        # print_map(map_grid, carts)
        if not run and remove_crashed_carts:
            result_loc = Point(carts[0].loc.x, carts[0].loc.y)
            # print_map(map_grid, carts)

    return result_loc


if __name__ == '__main__':
    r = solve_13(path(__file__, 'input.txt'))
    print('Collision: {},{}'.format(r.x, r.y))

    r = solve_13(path(__file__, 'input.txt'), True)
    print('Collision: {},{}'.format(r.x, r.y))
    # wrong: 61,48
