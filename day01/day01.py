# https://adventofcode.com/2023/day/1

with open('input.txt', 'r') as file:
    raw_input = file.read()
    lines = raw_input.splitlines()

# --- Part 1 --- #

values_sum = 0

for line in lines:
    digits_string = [c for c in line if c.isdigit()]
    calibration_value = int(digits_string[0] + digits_string[-1])
    values_sum += calibration_value

print(values_sum)

# --- Part 2 --- #
word_to_num_dict = {
    'one': '1',
    'two': '2',
    'three': '3',
    'four': '4',
    'five': '5',
    'six': '6',
    'seven': '7',
    'eight': '8',
    'nine': '9'
}

values_sum_2 = 0

for line in lines:
    digits_string = []
    for i in range(len(line)):
        line_remainder = line[i:]
        if line_remainder[0].isdigit():
            digits_string.append(line_remainder[0])
        for num_word in word_to_num_dict.keys():
            if line_remainder.lower().startswith(num_word):
                digits_string.append(word_to_num_dict[num_word])

    calibration_value = int(digits_string[0] + digits_string[-1])
    values_sum_2 += calibration_value

print(values_sum_2)
