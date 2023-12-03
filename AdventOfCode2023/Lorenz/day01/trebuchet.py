import re

# create an empty list where we store the calibration values
outcome = []

# opening and reading the lines from the input
with open('./input.txt', 'r') as f:
    lines = f.readlines()

# iterate over the lines
for line in lines:
    # find all decimals inside string
    decimals = re.findall("[0-9]", line)
    # assert that at least 1 decimal is found
    assert len(decimals)>=1, f'did not find a number for line {line}'
    # append first and last (can be same), convert to int and append to our list
    outcome.append(int(f'{decimals[0]}{decimals[-1]}'))

# take the sum of the list
print(sum(outcome))

