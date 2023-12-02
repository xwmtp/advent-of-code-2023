# https://adventofcode.com/2023/day/2

with open('input.txt', 'r') as file:
    raw_input = file.read()
    lines = raw_input.splitlines()

# --- Part 1 --- #

colors = ['red', 'green', 'blue']


def parse_game(game_string):
    sets_string = game_string.split(': ')[1]
    set_strings = sets_string.split('; ')
    split_set_strings = [set_string.split(', ') for set_string in set_strings]
    return [parse_split_set(split_set) for split_set in split_set_strings]


def parse_split_set(split_set):
    set = dict([(subset.split(' ')[1], int(subset.split(' ')[0])) for subset in split_set])
    for color in ['red', 'green', 'blue']:
        if color not in set:
            set[color] = 0
    return set


num_red_cubes = 12
num_green_cubes = 13
num_blue_cubes = 14

valid_game_indices = []

for i, line in enumerate(lines):
    game = parse_game(line)
    is_valid = True
    for set in game:
        if set['red'] > num_red_cubes or set['green'] > num_green_cubes or set['blue'] > num_blue_cubes:
            is_valid = False
            break
    if is_valid:
        valid_game_indices.append(i + 1)

print(sum(valid_game_indices))

# --- Part 2 --- #

power_sum = 0

for i, line in enumerate(lines):
    game = parse_game(line)

    min_num_squares = {
        'red': 0,
        'green': 0,
        'blue': 0,
    }

    for set in game:
        for color in colors:
            if set[color] > min_num_squares[color]:
                min_num_squares[color] = set[color]
    power = min_num_squares['red'] * min_num_squares['blue'] * min_num_squares['green']
    power_sum += power

print(power_sum)
