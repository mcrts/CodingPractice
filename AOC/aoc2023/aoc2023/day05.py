from collections import namedtuple
import sys
import re

import itertools as I
import functools as F

RE_SEED = r"^seeds: (?P<seeds>.*)$"
RE_MAP = r"^(?P<dst>\d+) (?P<src>\d+) (?P<map_range>\d+)$"

Range = namedtuple("Range", ['source' ,'target', 'size'])
class Range(Range):
    def isin(self, key):
        return self.source <= key < self.source + self.size

    def get(self, key, default=None):
        if self.isin(key):
            return (key - self.source) + self.target
        elif default:
            return default
        else:
            raise KeyError(key)
    
    def reverse_isin(self, key):
        return self.target <= key < self.target + self.size

    def reverse_get(self, key, default=None):
        if self.reverse_isin(key):
            return (key - self.target) + self.source
        elif default:
            return default
        else:
            raise KeyError(key)

RangeMap = namedtuple("RangeMap", ['ranges'])
class RangeMap(RangeMap):
    def reverse_get(self, key):
        select = None
        for r in self.ranges:
            if r.reverse_isin(key):
                select = r
                break
        
        if select:
            value = select.reverse_get(key)
        else:
            value = key
        return value

    def get(self, key):
        select = None
        for r in self.ranges:
            if r.isin(key):
                select = r
                break
        
        if select:
            value = select.get(key)
        else:
            value = key
        return value

    @classmethod
    def merge(cls, lhs, rhs):
        left_indices = I.chain.from_iterable((r.target, r.target + r.size) for r in lhs.ranges)
        right_indices = I.chain.from_iterable((r.source, r.source + r.size) for r in rhs.ranges)
        indices = sorted(list(set(I.chain(left_indices, right_indices))))
        intervalles = zip(indices[0::], indices[1::])
        ranges = []
        for i0, i1 in intervalles:
            d = i1 - i0
            source = lhs.reverse_get(i0)
            target = rhs.get(i0)
            r = Range(source, target, d)
            ranges.append(r)
        return cls(tuple(ranges))
        

def parse_range(line):
    m = re.match(RE_MAP, line)
    dst, src, r = m.groups()
    dst = int(dst)
    src = int(src)
    r = int(r)
    return Range(src, dst, r)

def parse_map(buffer):
    d = []
    for l in buffer:
        l = l.strip()
        match l:
            case "":
                break
            case _:
                d.append(parse_range(l))
    return RangeMap(tuple(d))

def parser_part1(buffer):
    seed_line = buffer.readline()
    m = re.match(RE_SEED, seed_line)
    seeds = set(map(int, filter(bool, m['seeds'].split(' '))))
    
    for l in buffer:
        l = l.strip()
        match l:
            case "seed-to-soil map:":
                seed_soil_map = parse_map(buffer)
            case "soil-to-fertilizer map:":
                soil_fertilizer_map = parse_map(buffer)
            case "fertilizer-to-water map:":
                fertilizer_water_map = parse_map(buffer)
            case "water-to-light map:":
                water_light_map = parse_map(buffer)
            case "light-to-temperature map:":
                light_temperature_map = parse_map(buffer)
            case "temperature-to-humidity map:":
                temperature_humidity_map = parse_map(buffer)
            case "humidity-to-location map:":
                humidity_location_map = parse_map(buffer)
            case _:
                pass

    maps = [
        seed_soil_map,
        soil_fertilizer_map,
        fertilizer_water_map,
        water_light_map,
        light_temperature_map,
        temperature_humidity_map,
        humidity_location_map
    ]
    rmap = F.reduce(RangeMap.merge, maps)
    return seeds, rmap

def part1():
    seeds, rmap = parser_part1(sys.stdin)
    locations = []
    for seed in seeds:
        locations.append(rmap.get(seed))
    return min(locations)

def parser_part2(buffer):
    seed_line = buffer.readline()
    m = re.match(RE_SEED, seed_line)

    seed_idx = list(map(int, filter(bool, m['seeds'].split(' '))))
    ranges = [Range(src, src, d) for src, d in zip(seed_idx[0::2], seed_idx[1::2])]
    seed_range = RangeMap(tuple(ranges))
    
    for l in buffer:
        l = l.strip()
        match l:
            case "seed-to-soil map:":
                seed_soil_map = parse_map(buffer)
            case "soil-to-fertilizer map:":
                soil_fertilizer_map = parse_map(buffer)
            case "fertilizer-to-water map:":
                fertilizer_water_map = parse_map(buffer)
            case "water-to-light map:":
                water_light_map = parse_map(buffer)
            case "light-to-temperature map:":
                light_temperature_map = parse_map(buffer)
            case "temperature-to-humidity map:":
                temperature_humidity_map = parse_map(buffer)
            case "humidity-to-location map:":
                humidity_location_map = parse_map(buffer)
            case _:
                pass

    maps = [
        seed_range,
        seed_soil_map,
        soil_fertilizer_map,
        fertilizer_water_map,
        water_light_map,
        light_temperature_map,
        temperature_humidity_map,
        humidity_location_map
    ]
    rmap = F.reduce(RangeMap.merge, maps)
    return seed_range, rmap

def part2():
    seed_range, rmap = parser_part2(sys.stdin)
    targets = sorted(rmap.ranges, key=lambda x: x.target)

    for t in targets:
        for r in seed_range.ranges:
            a = max(r.source, t.source)
            b = min(r.source + r.size, t.source + t.size) 
            if a <= b:
                return t.get(a)

def main():
    v = part2()
    print(v)