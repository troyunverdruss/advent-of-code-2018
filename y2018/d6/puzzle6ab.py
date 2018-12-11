from helpers.helpers import read_raw_entries, manhattan_distance, Point
from typing import List


class GridCell:
    def __init__(self, x, y):
        self.point_id = None
        p = Point()
        p.x, p.y = x, y
        self.location = p
        self.distances = {}

    def compute_distances(self, points: List[Point]) -> None:
        for point in points:
            self.distances[point.id] = manhattan_distance(self.location, point)

    def closest_to(self):
        if len(self.distances) == 0:
            raise Exception('Call compute_distances first!')

        s = sorted(self.distances.items(), key=lambda k: k[1])
        if s[0][1] == s[1][1]:
            return None
        else:
            return s[0][0]

    def closest_to_tied_list(self):
        if len(self.distances) == 0:
            raise Exception('Call compute_distances first!')

        sorted_distances = sorted(self.distances.items(), key=lambda kv: kv[1])

        tied = []
        first_distance = sorted_distances[0][1]
        for i in sorted_distances:
            if i[1] == first_distance:
                tied.append(i[0])
            else:
                break

        return tied

    def is_within_threshold(self, threshold):
        if sum(map(lambda kv: kv[1], self.distances.items())) < threshold:
            return True

        return False


def convert_points(entries: List[str]) -> List[Point]:
    points = []
    i = 0
    for entry in entries:
        p = Point()
        p.x, p.y = map(lambda v: int(v), entry.split(','))
        p.id = i
        points.append(p)
        i += 1

    return points


def setup_grid(points):
    buffer = 0
    min_x = min(points, key=lambda p: p.x).x - buffer
    max_x = max(points, key=lambda p: p.x).x + buffer
    min_y = min(points, key=lambda p: p.y).y - buffer
    max_y = max(points, key=lambda p: p.y).y + buffer
    grid = {}
    for i in range(min_x, max_x + 1):
        for j in range(min_y, max_y + 1):
            if i not in grid:
                grid[i] = {}

            grid[i][j] = GridCell(i, j)
    for point in points:
        grid[point.x][point.y].point_id = point.id
    for i in range(min_x, max_x + 1):
        for j in range(min_y, max_y + 1):
            grid[i][j].compute_distances(points)
    return grid, max_x, max_y, min_x, min_y


def solve_6a(points: List[Point]) -> int:
    grid, max_x, max_y, min_x, min_y = setup_grid(points)

    # Remove edge represented points
    points_to_consider = list(map(lambda x: x.id, points))

    for i in range(min_x, max_x + 1):
        for j in range(min_y, max_y + 1):
            if i == min_x or i == max_x or j == min_y or j == max_y:
                closest_to = grid[i][j].closest_to()

                if closest_to is not None and closest_to in points_to_consider:
                    points_to_consider.remove(closest_to)

    point_influence_count = {}
    for p in points_to_consider:
        point_influence_count[p] = 0

    for i in range(min_x, max_x + 1):
        for j in range(min_y, max_y + 1):
            closest_to = grid[i][j].closest_to()
            if closest_to in point_influence_count.keys():
                point_influence_count[closest_to] += 1

    sorted_influence_list = sorted(point_influence_count.items(), key=lambda kv: kv[1])
    return sorted_influence_list[len(sorted_influence_list) - 1][1]


def solve_6b(points, threshold):
    grid, max_x, max_y, min_x, min_y = setup_grid(points)

    total_size = 0
    for i in range(min_x, max_x + 1):
        for j in range(min_y, max_y + 1):
            if grid[i][j].is_within_threshold(threshold):
                total_size += 1

    return total_size


if __name__ == '__main__':
    entries = read_raw_entries('input.txt')
    points = convert_points(entries)

    r = solve_6a(points)

    print('Largest size: {}'.format(r))

    entries = read_raw_entries('input.txt')
    points = convert_points(entries)

    r = solve_6b(points, 10000)

    print('Largest size: {}'.format(r))
