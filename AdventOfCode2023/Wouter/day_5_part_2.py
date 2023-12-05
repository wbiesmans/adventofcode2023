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

        # Sort mapping by _from
        mapping.sort(key=lambda x: x[0])

        return mapping

    def map(self, input):
        output = input
        for _from, _to, _range in self.mapping:
            if input in range(_from, _from + _range):
                output = _to + (input - _from)
                break
        return output

    # Helper/debug function
    def count_total_range(self, ranges):
        total_range = 0
        for start, range in ranges:
            total_range += range
        return total_range


    def map_ranges(self, input_ranges):
        """ranges = list of (start, length) tuples"""
        sum_input_ranges = self.count_total_range(input_ranges)
        total_output_ranges = []
        for start_input, range_input in input_ranges:
            stop_input = start_input + range_input

            output_ranges = []
            for start_map, dest_map, range_map in self.mapping:
                stop_map = start_map + range_map

                # Case 1 : map_range starts after input start
                # Add (linear map) to output range, and shift start
                if start_map > start_input and start_map < stop_input:
                    output_ranges.append((start_input, (start_map - start_input)))
                    start_input = start_map

                # # Case 2 : map_range ends before input start
                # if _from_map + _range > start:
                #     continue

                # Case 3: map_range starts at, or before input start
                if start_input in range(start_map, start_map + range_map):
                    # Case 3a : map ends after 'stop'
                    if stop_map > stop_input:
                        stop_map = stop_input

                    # Case 3b : map ends before or at 'stop'
                    if stop_map <= stop_input:
                        _from_out = dest_map + (start_input - start_map)
                        _range_out = min(stop_input-start_input, stop_map-start_input)
                        total_output_ranges.append((_from_out, _range_out))
                        start_input += _range_out

                # If full input range is covered, stop
                if start_input >= stop_input:
                    break

            # Check at the end of the mappings, if full input range is covered
            if start_input < stop_input:
                output_ranges.append((start_input, stop_input - start_input))
            total_output_ranges = total_output_ranges + output_ranges

        sum_output_range = self.count_total_range(total_output_ranges)
        assert sum_output_range == sum_input_ranges, f"sum_output_range ({sum_output_range}) != sum_range ({sum_range})"
        return total_output_ranges

    def __repr__(self):
        return f"Mapping from {self._from} to {self._to}"


class ChainOfMappings():
    def __init__(self):
        self.mappings = []

    def add_mapping(self, mapping):
        self.mappings.append(mapping)

    def map(self, input):
        # map_str = str(input)
        for mapping in self.mappings:
            input = mapping.map(input)
            # map_str += f" -> {input}"
        # print(map_str)
        return input

    def map_ranges(self, input_ranges):
        for mapping in self.mappings:
            print(f"mapping: {mapping}")
            input_ranges = mapping.map_ranges(input_ranges)
        return input_ranges

    def __repr__(self):
        return f"Chain of mappings: {self.mappings}"


def find_minimum(output_ranges):
    minimum = None
    for start, range in output_ranges:
        if minimum is None or start < minimum:
            minimum = start
    return minimum


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

    # split seeds into even and odd indices
    seed_ranges = list(zip(seeds_int[::2], seeds_int[1::2]))
    output_ranges = chain_of_mappings.map_ranges(seed_ranges)

    minimum = find_minimum(output_ranges)

    print(f"minimum: {minimum}")
