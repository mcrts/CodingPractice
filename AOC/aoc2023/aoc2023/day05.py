from collections import namedtuple
import sys
import re

RE_SEED = r"^seeds: (?P<seeds>.*)$"
RE_MAP = r"^(?P<dst>\d+) (?P<src>\d+) (?P<map_range>\d+)$"

Almanach = namedtuple("Almanach", [
    'seeds',
    'seed_soil_map',
    'soil_fertilizer_map',
    'fertilizer_water_map',
    'water_light_map',
    'light_temperature_map',
    'temperature_humidity_map',
    'humidity_location_map',

])
class Almanach(Almanach):
    def get_locations(self):
        locations = []
        for seed in self.seeds:
            soil = self.seed_soil_map.get(seed, seed)
            fertilizer = self.soil_fertilizer_map.get(soil, soil)
            water = self.fertilizer_water_map.get(fertilizer, fertilizer)
            
            light = self.water_light_map.get(water, water)
            temperature = self.light_temperature_map.get(light, light)
            humidity = self.temperature_humidity_map.get(temperature, temperature)
            location = self.humidity_location_map.get(humidity, humidity)
            locations.append(location)
        return locations

def parse_range(line):
    m = re.match(RE_MAP, line)
    dst, src, r = m.groups()
    dst = int(dst)
    src = int(src)
    r = int(r)
    d = dict((k, v) for k, v in zip(range(src, src+r), range(dst, dst+r)))
    return d

def parse_map(buffer):
    d = dict()
    for l in buffer:
        l = l.strip()
        match l:
            case "":
                break
            case _:
                d.update(parse_range(l))
    return d

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
                print("SKIP >>", l)
    almanach = Almanach(
        seeds=seeds,
        seed_soil_map=seed_soil_map,
        soil_fertilizer_map=soil_fertilizer_map,
        fertilizer_water_map=fertilizer_water_map,
        water_light_map=water_light_map,
        light_temperature_map=light_temperature_map,
        temperature_humidity_map=temperature_humidity_map,
        humidity_location_map=humidity_location_map,
    )
    return almanach

def part1():
    almanach = parser_part1(sys.stdin)
    return min(almanach.get_locations())

def part2():
    return 0

def main():
    v = part1()
    print(v)