import re

import numpy as np

# opening and reading the lines from the input
with open('./input.txt', 'r') as f:
    lines = f.readlines()

data = np.array([[x for x in line] for line in lines])
data = data[:, :-1]

rows, cols = np.where(data == '*')

def find_first_number(seq):
    try:
        str_len = [x.isdigit() for x in seq].index(False)
        return ''.join(seq[:str_len])
    except ValueError:
        return ''.join(seq)

count = 0
for row, col in zip(rows, cols):

    # this part is only used for debugging purposes
    left_bound = max(0, col - 1)
    right_bound = min(data.shape[1], col + 1)
    top_bound = max(0, row - 1)
    bottom_bound = min(data.shape[0], row + 1)
    box = data[top_bound:bottom_bound+1, left_bound:right_bound+1]

    part_numbers = []

    # left part number
    digit = data[row, col-1]
    if digit.isdigit():
        sequence = data[row, :col]
        part_numbers.append(
            int(find_first_number(sequence[::-1])[::-1])
        )

    # right part number
    digit = data[row, col+1]
    if digit.isdigit():
        sequence = data[row, col+1:]
        part_numbers.append(
            int(find_first_number(sequence))
        )

    # top part number
    digit = data[row-1, col]
    if digit.isdigit():
        left_seq = data[row-1, :col+1][::-1]
        right_seq = data[row-1, col:]
        part_numbers.append(
            int(find_first_number(left_seq)[::-1][:-1] + find_first_number(right_seq))
        )
    else:
        # top left part number
        digit = data[row-1, col-1]
        if digit.isdigit():
            left_seq = data[row-1, :col]
            part_numbers.append(
                int(find_first_number(left_seq[::-1])[::-1])
            )

        # top right part number
        digit = data[row-1, col+1]
        if digit.isdigit():
            right_seq = data[row-1, col+1:]
            part_numbers.append(
                int(find_first_number(right_seq))
            )

    # bottom part number
    digit = data[row + 1, col]
    if digit.isdigit():
        left_seq = data[row + 1, :col + 1][::-1]
        right_seq = data[row + 1, col:]
        part_numbers.append(
            int(find_first_number(left_seq)[::-1][:-1] + find_first_number(right_seq))
        )
    else:
        # bottom left part number
        digit = data[row + 1, col - 1]
        if digit.isdigit():
            left_seq = data[row + 1, :col]
            part_numbers.append(
                int(find_first_number(left_seq[::-1])[::-1])
            )

        # bottom right part number
        digit = data[row + 1, col + 1]
        if digit.isdigit():
            right_seq = data[row + 1, col + 1:]
            part_numbers.append(
                int(find_first_number(right_seq))
            )

    if len(part_numbers) == 2:
        count += part_numbers[0]*part_numbers[1]

print(count)