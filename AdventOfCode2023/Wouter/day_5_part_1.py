import numpy as np

class Mapping():
    def __init__(self, input_lines):
        self.input = input_lines
        self._from, self._to = self._determine_from_to(input_lines[0])
        self.mapping = self._create_mapping(input_lines[1:])

    def _determine_from_to(self, line):
        line = line.split()[0]
        origin, destination = line.split("-to-")
        return origin, destination

    def _create_mapping(self, input_lines):
        # TODO : if numbers get large, mapping as a list won't work anymore
        # Store mappings separately, and rework map function
        mapping = []
        for line in input_lines:
            _to, _from, _range = line.split()
            _from = int(_from)
            _to = int(_to)
            _range = int(_range)
            mapping.append((_from, _to, _range))
        return mapping

    def map(self, input):
        output = input
        for _from, _to, _range in self.mapping:
            if input in range(_from, _from + _range):
                output = _to + (input - _from)
                break
        return output

    def __repr__(self):
        return f"Mapping from {self._from} to {self._to}"

class ChainOfMappings():
    def __init__(self):
        self.mappings = []

    def add_mapping(self, mapping):
        self.mappings.append(mapping)

    def map(self, input):
        map_str = str(input)
        for mapping in self.mappings:
            input = mapping.map(input)
            map_str += f" -> {input}"
        print(map_str)
        return input

    def __repr__(self):
        return f"Chain of mappings: {self.mappings}"

if __name__ == "__main__":
    with open("Wouter/day_5_input_final.txt", "r") as f:
        input_lines = f.readlines()

    seeds = input_lines[0].split(": ")[1].split(" ")
    seeds_int = [int(seed) for seed in seeds]

    chain_of_mappings = ChainOfMappings()
    mapping_lines = []
    for line in input_lines[2:]:
        if line.strip():
            mapping_lines.append(line)
        else:
            mapping = Mapping(mapping_lines)
            chain_of_mappings.add_mapping(mapping)
            mapping_lines = []

    # Add last mapping (file ends without empty line...)
    mapping = Mapping(mapping_lines)
    chain_of_mappings.add_mapping(mapping)

    minimum = None
    minimum_seed = None
    for seed in seeds_int:
        map_output = chain_of_mappings.map(seed)
        if minimum is None or map_output < minimum:
            minimum = map_output
            minimum_seed = seed
        print(f"seed: {seed}, output: {map_output}")

    print(f"minimum: {minimum}, for seed: {minimum_seed}")