# https://adventofcode.com/2023/day/3
from Grid2D import Grid2D

with open('input.txt', 'r') as file:
    raw_input = file.read()
    lines = raw_input.splitlines()


# --- Part 1 --- #

def is_symbol(char):
    return not char.isdigit() and char != '.'


grid = Grid2D(lines)
grid_size = grid.size()

parts_sum = 0

number_string = ''
adjacent_symbol_coords = set()
symbol_numbers_dict = dict()

for y in range(grid_size[0]):
    for x in range(grid_size[1]):
        char = grid.get(x, y)
        if char.isdigit():
            number_string += char
            adjacent_coords = grid.adjacent_coords(x, y)

            for coord in adjacent_coords:
                if is_symbol(grid.get(coord[0], coord[1])):
                    adjacent_symbol_coords.add(coord)
            continue

        if len(adjacent_symbol_coords) and len(number_string) > 0:
            parts_sum += int(number_string)

        for coord in adjacent_symbol_coords:
            if coord not in symbol_numbers_dict:
                symbol_numbers_dict[coord] = []
            symbol_numbers_dict[coord].append(int(number_string))

        number_string = ''
        adjacent_symbol_coords = set()

print(parts_sum)

# --- Part 2 --- #

symbol_and_numbers = []

for y in range(grid_size[0]):
    for x in range(grid_size[1]):
        char = grid.get(x, y)
        if is_symbol(char):
            adjacent_numbers = symbol_numbers_dict[(x, y)]
            symbol_and_numbers.append((char, adjacent_numbers))

gear_ratios_sum = 0

for symbol, numbers in symbol_and_numbers:
    if symbol == '*':
        if len(numbers) > 1:
            gear_ratio = numbers[0] * numbers[1]
            gear_ratios_sum += gear_ratio

print(gear_ratios_sum)
