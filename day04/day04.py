# https://adventofcode.com/2023/day/4

with open('input.txt', 'r') as file:
    raw_input = file.read()
    lines = raw_input.splitlines()


# --- Part 1 --- #

class Card:

    def __init__(self, card_id, winning_numbers, own_numbers):
        self.card_id = card_id
        self.winning_numbers = winning_numbers
        self.own_numbers = own_numbers
        self.is_copied = False

    def __str__(self):
        return f"Card {str(self.card_id)}: {' '.join(str(n) for n in self.winning_numbers)} | {' '.join(str(n) for n in self.own_numbers)}"

    def points(self):
        points = 0
        for number in self.own_numbers:
            if number in self.winning_numbers:
                if points == 0:
                    points = 1
                else:
                    points *= 2
        return points

    def copy_card_ids(self):
        wins = 0
        for number in self.own_numbers:
            if number in self.winning_numbers:
                wins += 1

        copies_ids = [self.card_id + i for i in range(1, wins + 1)]
        self.is_copied = True
        return copies_ids


def parse_to_card(line):
    card_string = line.split(': ')[0]
    card_id = int(card_string.split()[1])
    numbers_string = line.split(': ')[1]
    winning_numbers = [int(num_string) for num_string in numbers_string.split('|')[0].split()]
    own_numbers = [int(num_string) for num_string in numbers_string.split('|')[1].split()]
    return Card(card_id, winning_numbers, own_numbers)


cards = [parse_to_card(line) for line in lines]

total_points = sum(card.points() for card in cards)
print(total_points)

# --- Part 2 --- #

orig_cards = [c for c in cards]
all_cards = cards

total = 0
made_copies = True

# This is quite jank, but it gives the result... eventually

while (True):
    if not made_copies:
        break
    made_copies = False
    for i, card in enumerate(all_cards):
        if card.is_copied:
            total += 1
            continue
        copies_ids = card.copy_card_ids()
        for c in copies_ids:
            made_copies = True
            matching_card = next(ca for ca in orig_cards if ca.card_id == c)
            all_cards.append(Card(matching_card.card_id, matching_card.winning_numbers, matching_card.own_numbers))

print(len(all_cards))
