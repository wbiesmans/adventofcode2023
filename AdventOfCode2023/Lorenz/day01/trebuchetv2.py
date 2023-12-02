import re

# create an empty list where we store the calibration values
outcome = []

# opening and reading the lines from the input
with open('./input.txt', 'r') as f:
    lines = f.readlines()

# this is very hacky, because twone can be 21 we need to add the original ones hehe
numbers = {
    'zero': 'ze0ro', 'one': 'o1ne', 'two': 'tw2o',
    'three': 'thr3ee', 'four': 'fo4ur', 'five': 'fi5ve',
    'six': 'si6x', 'seven': 'sev7en', 'eight': 'eig8th',    'nine': 'ni9ne',
}
# iterate over the lines
for line in lines:
    # iterate over the numbers
    for num, value in numbers.items():
        # sub number if found, we keep the original as it might be
        line = re.sub(num, num+value, line)
    # find all decimals inside string
    decimals = re.findall("[0-9]", line)
    # assert that at least 1 decimal is found
    assert len(decimals)>=1, f'did not find a number for line {line}'
    # append first and last (can be same), convert to int
    number = int(f'{decimals[0]}{decimals[-1]}')
    # append to list
    outcome.append(number)

# take the sum of the list
print(sum(outcome))

