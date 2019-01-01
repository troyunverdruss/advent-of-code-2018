from helpers.helpers import read_raw_entries
from typing import List
import re
import sys
import numpy


class Star:
    def __init__(self, x=None, y=None, x_vel=None, y_vel=None):
        self.x = x
        self.y = y
        self.x_vel = x_vel
        self.y_vel = y_vel

    def update(self):
        self.x += self.x_vel
        self.y += self.y_vel

    def has_neighbor(self, stars):
        x_list = [self.x + 1, self.x - 1]
        y_list = [self.y + 1, self.y - 1]

        for star in stars:
            if star == self:
                continue

            if (star.x == self.x and (star.y in y_list)) or (star.y == self.y and (star.x in x_list)):
                return True

        return False

    def __repr__(self):
        return repr('Pos: ({}, {}), Vel: ({}, {})'.format(self.x, self.y, self.x_vel, self.y_vel))


def read_stars(input: str):
    entries = read_raw_entries(__file__, input)

    stars = []
    for entry in entries:
        # position = < -3, 11 > velocity = < 1, -2 >
        p = re.compile(r'.*<(.*)>.*<(.*)>.*')
        matcher = p.match(entry)

        x, y = matcher.group(1).split(',')
        x_vel, y_vel = matcher.group(2).split(',')

        stars.append(Star(x=int(x), y=int(y), x_vel=int(x_vel), y_vel=int(y_vel)))

    return stars


def print_sky(stars: List[Star]):
    max_x, max_y, min_x, min_y = get_sky_range(stars)

    sky = []
    for x in range(0, max_x - min_x + 1):
        sky.append([])
        for y in range(0, max_y - min_y + 1):
            sky[x].append(' ')

    for star in stars:
        sky[star.x - min_x][star.y - min_y] = '#'

    for y in range(0, max_y - min_y + 1):
        for x in range(0, max_x - min_x + 1):
            print(sky[x][y], end='')

        print('')

    sys.stdout.flush()


def solve_10(stars: List[Star]):
    max_x, max_y, min_x, min_y = get_sky_range(stars)

    run = True
    time = 0
    lone_star_threshold = 20
    while run:
        if time % 10000 == 0:
            print(time)

        neighbor_count = 0
        lone_stars = 0

        # Quitting condition
        for star in stars:
            if star.x < min_x or star.x > max_x or star.y < min_y or star.y > max_y:
                run = False
                break

            if star.has_neighbor(stars):
                neighbor_count += 1
            else:
                lone_stars += 1
                if lone_stars > lone_star_threshold:
                    break

        if run and (neighbor_count / len(stars) > 0.5):
            print(time)
            print_sky(stars)

        for star in stars:
            star.update()

        time += 1


def get_sky_range(stars):
    min_x = min(stars, key=lambda s: s.x).x
    max_x = max(stars, key=lambda s: s.x).x
    min_y = min(stars, key=lambda s: s.y).y
    max_y = max(stars, key=lambda s: s.y).y
    return max_x, max_y, min_x, min_y


if __name__ == '__main__':
    stars = read_stars('input.txt')
    solve_10(stars)
