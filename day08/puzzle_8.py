from helpers.helpers import read_raw_entries
from typing import List, Dict
import re
import string


class Node:
    def __init__(self, child_count, metadata_count):
        self.child_count = child_count
        self.metadata_count = metadata_count
        self.metadata = []


def process_input(data: List[int], nodes: List[Node]):
    my_data = data
    child_count = int(my_data.pop(0))
    metadata_count = int(my_data.pop(0))

    node = Node(child_count, metadata_count)
    nodes.append(node)

    for i in range(0, child_count):
        process_input(my_data, nodes)

    for i in range(0, metadata_count):
        node.metadata.append(int(my_data.pop(0)))




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


if __name__ == '__main__':
    entries = read_raw_entries('input.txt')
    r = solve_8a(entries[0])
    print('Sum of metadata count: {}'.format(r))
