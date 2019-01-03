from helpers import read_raw_entries
from typing import List


class Node:
    def __init__(self, child_count, metadata_count):
        self.child_count = child_count
        self.metadata_count = metadata_count
        self.children = []
        self.metadata = []

    def value(self):
        value = 0
        if self.child_count == 0:
            for m in self.metadata:
                value += m
        else:
            value = 0
            for m in self.metadata:
                if m <= len(self.children):
                    value += self.children[m - 1].value()

        return value


def process_input(data: List[int], nodes: List[Node]):
    child_count = int(data.pop(0))
    metadata_count = int(data.pop(0))

    node = Node(child_count, metadata_count)
    nodes.append(node)

    for i in range(0, child_count):
        node.children.append(process_input(data, nodes))

    for i in range(0, metadata_count):
        node.metadata.append(int(data.pop(0)))

    return node


def solve_8a(input: str):
    data = input.split(' ')
    for d in data:
        d = int(d)

    nodes = []
    process_input(data, nodes)

    metadata_total = 0
    for node in nodes:
        for metadata in node.metadata:
            metadata_total += metadata

    return metadata_total


def solve_8b(input: str):
    data = input.split(' ')
    for d in data:
        d = int(d)

    nodes = []
    process_input(data, nodes)

    return nodes[0].value()


if __name__ == '__main__':
    entries = read_raw_entries('input.txt')
    r = solve_8a(entries[0])
    print('Sum of metadata count: {}'.format(r))

    entries = read_raw_entries('input.txt')
    r = solve_8b(entries[0])
    print('Root node value: {}'.format(r))
