import re
from collections import namedtuple

RE_STATEMENT = r"^(?P<key>[A-Z]+)\[(?P<i0>\-{0,1}\d+)\.\.(?P<i1>\-{0,1}\d+)\]\s=\s(?P<values>.*)$"
RE_INSTRUCTION = r"^(?P<key>[A-Z]+)\[((?P<i>\-{0,1}\d+)|(?P<sub>.*))\]$"


class Array(namedtuple("Array", ["key", "offset", "values"])):
    def get(self, i):
        return self.values[i - self.offset]


class Instruction(namedtuple("Instruction", ["key", "index", "subinstr"])):
    def run(self, memory):
        if self.index is not None:
            return memory[self.key].get(self.index)
        else:
            index = self.subinstr.run(memory)
            return memory[self.key].get(index)


def parse_statement(s):
    m = re.match(RE_STATEMENT, s)
    key = m.group("key")
    offset = int(m.group("i0"))
    values = list(map(int, m.group("values").split(" ")))
    return Array(key, offset, values)


def parse_instruction(s):
    m = re.match(RE_INSTRUCTION, s)
    key = m.group("key")
    if m.group("i"):
        index = int(m.group("i"))
        subinstr = None
    else:
        index = None
        subinstr = parse_instruction(m.group("sub"))
    return Instruction(key, index, subinstr)


def parse():
    n = int(input())
    statements = [parse_statement(input()) for _ in range(n)]
    memory = {a.key: a for a in statements}
    instruction = parse_instruction(input())
    return n, memory, instruction


n, memory, instruction = parse()
print(instruction.run(memory))
