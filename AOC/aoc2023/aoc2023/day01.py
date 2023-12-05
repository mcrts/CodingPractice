import sys
import re

RE_DIGIT = r"(\d)"

SUB_PAIR = [
    ('one', 'o1e'),
    ('two', 't2'),           
    ('three', '3e'),            
    ('four', '4'),    
    ('five', '5e'),      
    ('six', '6'),           
    ('seven', '7n'),       
    ('eight', 'e8t'),     
    ('nine', 'n9e'),
]

def part1():
    res = 0
    for l in sys.stdin:
        m = re.findall(RE_DIGIT, l)
        res += int(m[0] + m[-1])
    return res

def part2():
    res = 0
    for l in sys.stdin:
        for k, v in SUB_PAIR:
           l = re.sub(k, v, l)
        m = re.findall(RE_DIGIT, l)
        res += int(m[0] + m[-1])
    return res

def main():
    r = part2()
    print(r)