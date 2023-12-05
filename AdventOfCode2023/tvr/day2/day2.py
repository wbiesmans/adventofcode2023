import argparse
import math
import typing

_COLOURS = ['red', 'green', 'blue']


def _max_values(game_pulls: dict) -> dict:
    max_values = {}
    for colour in _COLOURS:
        max_values[colour] = max((map(lambda x: x[colour] if colour in x.keys() else 0, game_pulls)))
    return max_values

def _power(input_dict: dict) -> typing.Generator[int, None, None]:
    for _, game_pulls in input_dict.items():
        yield math.prod(_max_values(game_pulls).values())
    
def _possible_ids(input_dict: dict, max_dict: dict) -> typing.Generator[int, None, None]:
    for game_id, game_pulls in input_dict.items():
        failed = False
        max_values = _max_values(game_pulls)
        for colour, max_value in max_values.items():
            if max_value > max_dict[colour]:
                failed = True
                break
        if failed:
            continue
        yield game_id

def _process_input_file(input_file: str) -> dict:
    input_dict = {}
    with open(input_file, 'r') as input_fh:
        for line in input_fh:
            game = line.split(':')
            game_id = int(game[0].split(' ')[1])
            game_pulls = []
            for game_pulls_string in game[1].split(';'):
                game_pull = {}
                for colours in game_pulls_string.split(','):
                    colour_split = colours.strip().split(' ')
                    game_pull[colour_split[1]] = int(colour_split[0])
                game_pulls.append(game_pull)
            input_dict[game_id] = game_pulls
    return input_dict

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Tool to solve advent of code day 2 challenge")
    parser.add_argument('-i', '--input_file', help='The input file.')
    parser.add_argument('-r', '--red', help='Max red blocks', type=int, default=0)
    parser.add_argument('-g', '--green', help='Max green blocks', type=int, default=0)
    parser.add_argument('-b', '--blue', help='Max blue blocks', type=int, default=0)
    args = parser.parse_args()
    
    max_dict = {'red': args.red, 'green': args.green, 'blue': args.blue}
    input_dict = _process_input_file(args.input_file)
    print(sum(_possible_ids(input_dict, max_dict)))
    print(sum(_power(input_dict)))


