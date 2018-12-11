from helpers.helpers import Point


def compute_cell(point, serial_number):
    rack_id = point.x + 10

    value = rack_id * point.y

    value += serial_number

    value *= rack_id

    digits = list(str(value))

    if len(digits) < 3:
        value = 0
    else:
        value = int(digits[-3])

    return value - 5


def fill_grid(serial_number):
    grid = []

    for x in range(0, 300):
        grid.append([])
        for y in range(0, 300):
            grid[x].append(compute_cell(Point(x + 1, y + 1), serial_number))

    return grid


def compute_value_from_point(grid, point, dimension):
    value = 0
    for x in range(0, dimension):
        for y in range(0, dimension):
            value += grid[point.x + x][point.y + y]

    return value


def solve_11(serial_number, min_dimension=3, max_dimension=3):
    max_dimension += 1

    grid = fill_grid(serial_number)

    max_value_found = 0
    coord = Point(0, 0)
    dimension = 0

    for dimension in range(min_dimension, max_dimension):
        print('dim: {}'.format(dimension))
        for x in range(0, 300 - dimension):
            for y in range(0, 300 - dimension):
                value = compute_value_from_point(grid, Point(x, y), dimension)

                if value > max_value_found:
                    max_value_found = value
                    coord = Point(x+ 1, y+1)
                    dimension = dimension
                    print('{},{},{}'.format(x+1, y+1, dimension))

    return coord, dimension

if __name__ == '__main__':
    # r = solve_11(1788, 3, 3)
    # print('{}, {}'.format(r.x, r.y))

    r, d = solve_11(1788, 1, 300)
    print('{},{},{}'.format(r.x, r.y, d))
