from helpers.helpers import Point

GRID_SIZE = 3

def compute_cell(point, serial_number):
    rack_id = point.x + 10

    power = rack_id * point.y
    power += serial_number
    power *= rack_id
    power = power // 100 % 10

    return power - 5


def fill_grid(serial_number):
    grid = []

    for x in range(0, GRID_SIZE):
        grid.append([])
        for y in range(0, GRID_SIZE):
            grid[x].append(compute_cell(Point(x, y), serial_number))

    return grid


def fill_prefix_sum_grid(grid):
    prefix_sum_grid = [[0 for x in range(GRID_SIZE + 1)] for y in range(GRID_SIZE + 1)]

    for x in range(1, GRID_SIZE + 1):
        for y in range(1, GRID_SIZE + 1):
            prefix_sum_grid[x][y] = prefix_sum_grid[x][y-1] + prefix_sum_grid[x-1][y] - prefix_sum_grid[x-1][y-1] + grid[x-1][y-1]

    return prefix_sum_grid


def compute_value_from_point(grid, point, dimension):
    value = 0
    for x in range(0, dimension):
        for y in range(0, dimension):
            value += grid[point.x + x][point.y + y]

    return value


def solve_11(serial_number, min_dimension=3, max_dimension=3):
    max_dimension += 1

    grid = fill_grid(serial_number)
    prefix_sum_grid = fill_prefix_sum_grid(grid)

    max_value_found = 0
    coord = Point(0, 0)
    dimension = 0

    for dimension in range(min_dimension, max_dimension):
        print('dim: {}'.format(dimension))
        for x in range(1, GRID_SIZE + 1 - dimension):
            for y in range(1, GRID_SIZE + 1 - dimension):
                value = compute_value_from_point(grid, Point(x, y), dimension)

                if value > max_value_found:
                    max_value_found = value
                    coord = Point(x, y)
                    dimension = dimension
                    print('{},{},{}'.format(x, y, dimension))

    return coord, dimension

if __name__ == '__main__':
    r, dim = solve_11(1788, 3, 3)
    print('{}, {}'.format(r.x, r.y))

    # r, d = solve_11(1788, 1, GRID_SIZE)
    # print('{},{},{}'.format(r.x, r.y, d))
