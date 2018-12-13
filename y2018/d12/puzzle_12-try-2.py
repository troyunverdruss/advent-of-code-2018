from collections import deque
from helpers.helpers import read_raw_entries
from typing import List, Dict, Tuple
import re
import sys

def solve_12(entries):
    curr = entries[0].strip()

    rules = {}
    p = re.compile(r'(.*)=>(.*)')
    for entry in entries:
        m = p.match(entry)
        if m:
            rules[m.group(1).strip()] = m.group(2).strip()

    for k, v in rules.items():
        print (k, v)

    for i in range(20):


if __name__ == '__main__':
    entries = read_raw_entries('input.txt')
    solve_12(entries)