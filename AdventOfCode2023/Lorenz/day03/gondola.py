import re

import numpy as np

# opening and reading the lines from the input
with open('./input.txt', 'r') as f:
    lines = f.readlines()

data = np.array([[x for x in line] for line in lines])
data = data[:, :-1]
not_symbols = ['.', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
count = 0

for idx, line in enumerate(lines):
    line_length = len(line)

    remainder = line.lstrip('.')
    while remainder != '\n':
        if remainder[0].isdigit():
            number = remainder.split('.')[0]
            try:
                last_digit = [x.isdigit() for x in number].index(False)
                number = number[:last_digit]
            except ValueError:
                pass

            pos = line_length - len(remainder)
            str_size = len(number)
            neighbours = []

            left_bound = max(0, pos-1)
            right_bound = min(data.shape[1], pos+str_size+1)
            top_bound = max(0, idx-1)
            bottom_bound = min(data.shape[0], idx+1)

            neighbours = data[top_bound:bottom_bound+1, left_bound:right_bound].flatten()

            symbols = [x for x in neighbours if x not in not_symbols]
            if len(symbols)>0:
                count+=int(number)

            remainder = remainder[str_size:].lstrip('.')
        else:
            remainder = remainder[1:].lstrip('.')

print(count)