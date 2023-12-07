import argparse
import math
import typing
import re
import math
import operator
import itertools
import copy

_REGEX_DIGITS = re.compile('\d+')
_REGEX_SYMBOL = re.compile('[^\d\.\n]')
_DUMMY = {'numbers': [], 'symbols': [], 'gears': []}

def find_gears(queue: list) -> typing.Generator[int, None, None]:
    gears = queue[1]['gears']
    for gear in gears:
        matches = []
        for queued_item in queue:
            for number in queued_item['numbers']:
                if gear in number['span']:
                    matches.append(number['part_number'])
        if len(matches) > 1:
            yield math.prod(matches)

def find_part_numbers(queue: list) -> typing.Generator[int, None, None]:
    symbols = set(itertools.chain.from_iterable(map(operator.itemgetter('symbols'), queue)))
    for number in queue[1]['numbers']:
        if any([symbol in number['span'] for symbol in symbols]):
            yield number['part_number']

def parse_line(line: str) -> dict:
    output = copy.deepcopy(_DUMMY)
    numbers = _REGEX_DIGITS.finditer(line)
    if numbers:
        for match in numbers:
            span = match.span()
            span = range(span[0]-1, span[1]+1)
            number = int(match.group())
            output['numbers'].append({'part_number': number, 'span': span})
    symbols = _REGEX_SYMBOL.finditer(line)
    if symbols:
        for match in symbols:
            loc = match.start()
            if match.group() == '*':
                output['gears'].append(loc)
            output['symbols'].append(loc)
    return output        

def _process_input_file(input_file: str, func: typing.Callable) -> typing.Generator[int, None, None]:
    with open(input_file, 'r') as input_fh:
        queue = [_DUMMY, _DUMMY, _DUMMY]
        for line in input_fh:
            queue.pop(0)
            parsed_line = parse_line(line)
            queue.append(parsed_line)
            for part_number in func(queue):
                yield part_number
        queue.pop(0)
        queue.append(_DUMMY)
        for part_number in func(queue):
            yield part_number

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Tool to solve advent of code day 3 challenge")
    parser.add_argument('-i', '--input_file', help='The input file.')
    parser.add_argument('-g', '--gears', help='Process gears.', action='store_true', default=False)

    args = parser.parse_args()
    
    func = find_part_numbers
    if args.gears:
        func = find_gears
    print(sum(_process_input_file(args.input_file, func)))

