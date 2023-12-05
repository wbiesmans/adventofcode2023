import argparse
import typing

_NUMBERS_STRING = "0123456789"
_WRITTEN_NUMBERS = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
_NUMBERS_DICT = dict(zip(_WRITTEN_NUMBERS + list(_NUMBERS_STRING), _NUMBERS_STRING + _NUMBERS_STRING))


def _find_all_offsets(string, substring) -> typing.Generator[int, None, None]:
    offset = -1
    while (offset := string.find(substring, offset+1)) != -1:
        yield offset

def _process_written_numbers(line: str) -> str:
    offsets = {}
    for number_to_find, number in _NUMBERS_DICT.items():
        for offset in _find_all_offsets(line, number_to_find):
            offsets[offset] = number
    return "".join(dict(sorted(offsets.items())).values())

def _process_input_file(input_file: str, process_written_numbers: bool) -> typing.Generator[int, None, None]:
    with open(input_file, 'r') as input_fh:
        for line in input_fh:
            if process_written_numbers:
                line = _process_written_numbers(line)
            else:
                line = [elem for elem in line if elem in _NUMBERS_STRING]
            yield int(line[0] + line[-1])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Tool to solve advent of code day 1 challenge")
    parser.add_argument('-i', '--input_file', help='The input file.')
    parser.add_argument('-p', '--process_written_numbers', help='Process written numbers.', action='store_true', default=False)
    args = parser.parse_args()
    
    print(sum(_process_input_file(args.input_file, args.process_written_numbers)))

