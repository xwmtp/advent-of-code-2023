import requests
import sys
import os
import datetime

# Command line arg 1: Advent of Code session cookie
# Command line arg 2 (optional): Day number

YEAR = 2023


class Downloader:

    def __init__(self):
        self.day = get_current_day()
        self.formatted_day = formatted_day(self.day)
        print(self.formatted_day)

    def fetch_input(self):
        url = f"https://adventofcode.com/{YEAR}/day/{self.day}/input"
        print(f"Fetching url {url}")
        response = requests.post(url, cookies={'session': get_session_cookie()})
        if response.status_code != 200:
            raise Exception(f"Error code {response.status_code} while fetching {url}: {response.text}")
        print(repr(response.text))
        return response.text

    def save_input(self, input_string):
        folder_path = f'../day{formatted_day(self.day)}'
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        input_path = f'../day{formatted_day(self.day)}/input.txt'
        if os.path.exists(input_path):
            raise Exception(f'File {input_path} already exists!')

        with open(input_path, 'w') as file:
            file.write(input_string)

    def save_template(self, template_string):
        folder_path = f'../day{formatted_day(self.day)}'
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        template_path = f'../day{formatted_day(self.day)}/day{formatted_day(self.day)}.py'

        if os.path.exists(template_path):
            raise Exception(f'File {template_path} already exists!')

        with open(template_path, 'w') as file:
            file.write(template_string)

    def get_solution_template(self):
        return f"""# https://adventofcode.com/{YEAR}/day/{self.day}

with open('input.txt', 'r') as file:
    raw_input = file.read()
    lines = raw_input.splitlines()

# --- Part 1 --- #

print(lines)
"""


def get_session_cookie():
    if sys.argv[1] is None:
        raise Exception('Missing session cookie, please provide it as a command line argument')
    session_cookie = sys.argv[1]
    return session_cookie


def get_current_day():
    month = datetime.datetime.now().month
    if len(sys.argv) >= 3:
        print(f'Read day {sys.argv[2]} from command line')
        return int(sys.argv[2])
    if month == 12:
        return datetime.datetime.now().day
    if len(sys.argv) < 3:
        raise Exception('Missing day, and its not December. Put the day number as the 2nd command line argument')
    return int(sys.argv[2])


def formatted_day(day):
    return f"0{day}" if day < 10 else str(day)


if __name__ == '__main__':
    downloader = Downloader()

    input_string = downloader.fetch_input()
    template = downloader.get_solution_template()

    downloader.save_input(input_string)
    downloader.save_template(template)
