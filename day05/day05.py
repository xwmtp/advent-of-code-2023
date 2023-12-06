# https://adventofcode.com/2023/day/5
import sys

with open('input.txt', 'r') as file:
    raw_input = file.read()
    lines = raw_input.splitlines()

# --- Part 1 --- #

lines.append('')
seeds = [int(c) for c in lines[0].split(': ')[1].split(' ')]


class Map:

    def __init__(self, from_name, to_name, raw_numbers):
        self.from_name = from_name
        self.to_name = to_name
        self.raw_numbers = raw_numbers
        self.ranges = [MapRange(d, s, l) for d, s, l in raw_numbers]

    def map_value(self, val):
        for map_range in self.ranges:
            result_value = map_range.map_value(val)
            if result_value is not None:
                return result_value
        return val

    def map_value_reverse(self, val):
        for map_range in self.ranges:
            result_value = map_range.map_value_reverse(val)
            if result_value is not None:
                return result_value
        return val

    def map_value_reverse_2(self, val):
        for map_range in self.ranges:
            result = map_range.map_value_reverse_2(val)
            if result is not None:
                result_val, mapped_diff, dist_to_next = result
                # print(f'{val} +{mapped_diff} = {result_val} (dist: {dist_to_next})')
                return result_val
        return val

    def map_value_reverse_3(self, val):
        max_skip = None
        for ra in self.ranges:
            if ra.is_in(val):
                max_skip = ra.bounds[1] - val
                # print('within maxskip', max_skip)
        if max_skip is None:
            diffs = [ra.bounds[0] - val for ra in self.ranges if ra.bounds[0] - val >= 0]
            max_skip = min(diffs) - 1 if len(diffs) > 0 else None
            # print('outside maxskip', max_skip)

        return self.map_value_reverse_2(val), max_skip

    def __str__(self):
        return f'{self.from_name} to {self.to_name}: {self.raw_numbers}'


class MapRange:
    def __init__(self, destination_start, source_start, length):
        self.destination_start = destination_start
        self.source_start = source_start
        self.length = length
        self.bounds = (self.source_start, self.source_start + self.length)

    def map_value(self, value):
        if value < self.source_start or value >= self.source_start + self.length:
            return None
        start_offset = value - self.source_start
        return self.destination_start + start_offset

    def map_value_reverse(self, val):
        if val < self.destination_start or val >= self.destination_start + self.length:
            return None
        start_offset = val - self.destination_start
        return self.source_start + start_offset

    def map_value_reverse_2(self, val):
        if val < self.destination_start or val >= self.destination_start + self.length:
            return None
        start_offset = val - self.destination_start
        mapped = self.source_start + start_offset
        # mapped, diff, dist to next value
        return mapped, mapped - val, (self.destination_start + self.length - 1) - val

    def is_in(self, val):
        return val >= self.destination_start and val < self.destination_start + self.length

    def __str__(self):
        return f'dest: {self.destination_start}, source: {self.source_start}, length: {self.length}'


def get_map_names(string):
    splt_string = string.split(' ')[0].split('-')
    return splt_string[0], splt_string[2]


maps_dct = dict()
maps_rev_dict = dict()

map_names = []
map_numbers = []
for line in lines[2:]:
    if len(line) == 0:
        maps_dct[map_names[0]] = Map(map_names[0], map_names[1], map_numbers)
        maps_rev_dict[map_names[1]] = Map(map_names[0], map_names[1], map_numbers)
        map_numbers = []
        continue
    if line[0].isalpha():
        map_names = get_map_names(line)
    if line[0].isdigit():
        numbers = [int(c) for c in line.split()]
        map_numbers.append(numbers)

location_numbers = []
for seed in seeds:
    from_name = 'seed'
    mapped_value = seed
    while (True):
        if from_name not in maps_dct:
            break
        map = maps_dct[from_name]
        # print(f'{from_name} {mapped_value}')
        mapped_value = map.map_value(mapped_value)
        from_name = map.to_name
    location_numbers.append(mapped_value)

print(min(location_numbers))

# --- Part 2 --- #

pairs = list(zip(seeds[::2], seeds[1::2]))

pair_bounds = [(see, see + le - 1) for see, le in pairs]

min_value = sys.maxsize
for seed, length in pairs:
    start = seed
    end = seed + length - 1


def within_pair(value, seed, length):
    # print(f'is {seed} <= {value} <= {seed + length - 1}?', value >= seed or value <= (seed + length -1))
    return value >= seed and value <= (seed + length - 1)


def is_pair(value, skip, seed):
    return seed >= value and value + skip >= seed


min_loc = 0
min_dist = 0
while (True):
    to_name = 'location'
    if min_loc % 100000 == 0:
        print(min_loc, mapped_value)
    if min_dist > 0:
        # print(f'     SKIP {min_dist}')
        for pair in pairs:
            if is_pair(mapped_value, min_dist, pair[0]):
                print('        IS SKIPPING SEED PAIR START', min_loc, min_dist, pair[0] - mapped_value)
    min_loc += min_dist
    mapped_value = min_loc
    # print('\ntrying mapped val', mapped_value)

    min_dists = []

    while (True):
        if to_name not in maps_rev_dict:
            break
        map = maps_rev_dict[to_name]
        mapped_value, min_dist = map.map_value_reverse_3(mapped_value)
        min_dists.append(min_dist)
        # print(f'{map.from_name}-{map.to_name} {mapped_value}')
        to_name = map.from_name
    valid_dists = [c for c in min_dists if c is not None and c >= 0]
    min_dist = min(valid_dists) if len(valid_dists) > 0 else 0
    print(f'min_dist {min_dist} min dists ', min_dists, f'mapped value {mapped_value}')
    if any(within_pair(mapped_value, p, l) for p, l in pairs):
        print('FOUND IT', min_loc)
        break
    min_loc += 1
