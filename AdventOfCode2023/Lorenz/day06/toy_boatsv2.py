import math

import numpy as np

# opening and reading the lines from the input
with open('./input.txt', 'r') as f:
    lines = f.readlines()

time = int(lines[0].split(':')[-1].replace(' ', '')[:-1])
distance = int(lines[1].split(':')[-1].replace(' ', '')[:-1])
num_solutions = 0

time_holding = [time - x for x in range(time + 1)]

# we have to use a second degree equation to solve this
# given that t_holding*t_racing > distance, we can make the equation
# -t_racing^2 + time*t_racing - distance > 0, to know where this is equal to 0
# we take the discriminant which is (-b +- sqrt(b^2 - 4ac))/2a

first_point = (-time + np.sqrt(time*time - 4*(-1)*(-distance)))/2*(-1)
second_point = (-time - np.sqrt(time*time - 4*(-1)*(-distance)))/2*(-1)

print(math.floor(second_point) - math.ceil(first_point) + 1) # NGL had to fiddle with the exact number