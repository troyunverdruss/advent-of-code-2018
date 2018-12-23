import re
from unittest import TestCase, skip
import networkx as nx

from helpers.helpers import Point
from y2018.d20.puzzle_20 import solve_20


class TestSolve_20(TestCase):
    def test_sample_1(self):
        d = solve_20('^WNE$')
        self.assertEqual(3, d)

    def test_sample_2(self):
        d = solve_20('^ENWWW(NEEE|SSE(EE|N))$')
        self.assertEqual(10, d)

    def test_sample_3(self):
        d = solve_20('^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$')
        self.assertEqual(18, d)

    def test_mine_1(self):
        d = solve_20('^N(NES|)SS$')
        self.assertEqual(6, d)

    def test_mine_2(self):
        d = solve_20('^NNN(E|NN(E|W))SSS$')
        self.assertEqual(9, d)

    def test_mine_3(self):
        d = solve_20('^N(E|N(E|W))S$')
        self.assertEqual(4, d)

    def test_mine_4(self):
        d = solve_20('^N(W(N|E(E|S)E)E)$')

    def test_more_examples_1(self):
        d = solve_20('^ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))$')
        self.assertEqual(23, d)

    def test_more_examples_2(self):
        d = solve_20('^WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))$')
        self.assertEqual(31, d)

    @skip
    def test_load_gml(self):
        g = nx.DiGraph()

        g: nx.DiGraph = nx.read_gml('real-nodes.gml', destringizer=self.make_points)

        max_distance = 0
        nodes = len(g.nodes)
        i = 0

        all_paths = nx.single_source_shortest_path(g, source=Point(0,0))

        for k in all_paths.keys():
            i += 1
            # if p == Point(0,0):
            #     continue

            if len(all_paths[k]) > max_distance:
                max_distance = len(all_paths[k])
            print('{}/{}'.format(i, nodes))
        print('max: {}'.format(max_distance - 1))

        for node in g.nodes:
            i += 1
            distance = nx.shortest_path_length(g, source=Point(0, 0), target=node)
            if distance > max_distance:
                max_distance = distance
        print(max_distance)

    def make_points(self, string):
        # print(string)
        p = re.compile(r'\((-?\d+),\s*(-?\d+)\)')
        m = p.match(string)
        return Point(m.group(1), m.group(2))
