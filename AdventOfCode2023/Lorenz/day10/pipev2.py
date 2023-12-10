import numpy as np


class Segment(object):

    def __init__(self, x, y, start, mask):
        self.x = x
        self.y = y
        self.x_p = start[0]
        self.y_p = start[1]
        self.mask = mask
        self.bend = self.mask[self.y, self.x]
        self.n_steps = 1

    def step(self):

        if self.bend == '-':
            delta_x = self.x - self.x_p
            delta = (delta_x * 2, 0)

        elif self.bend == '|':
            delta_y = self.y - self.y_p
            delta = (0, delta_y * 2)

        elif self.bend == 'L':
            if self.x - self.x_p == 0:
                delta = (1, 1)
            else:
                delta = (-1, -1)

        elif self.bend == 'F':
            if self.x - self.x_p == 0:
                delta = (1, -1)
            else:
                delta = (-1, 1)

        elif self.bend == '7':
            if self.x - self.x_p == 0:
                delta = (-1, -1)
            else:
                delta = (1, 1)

        elif self.bend == 'J':
            if self.x - self.x_p == 0:
                delta = (-1, 1)
            else:
                delta = (1, -1)

        # settle new location
        curr = (self.x, self.y)
        self.mask[curr[1], curr[0]] = 'X'
        self.x = self.x_p + delta[0]
        self.y = self.y_p + delta[1]
        self.x_p, self.y_p = curr
        self.bend = self.mask[self.y, self.x]
        self.n_steps += 1


# opening and reading the lines from the input
with open('./input.txt', 'r') as f:
    lines = f.readlines()

maze = np.array([[x for x in line[:-1]] for line in lines])
mask = maze.copy()

y, x = [x[0] for x in np.where(maze == 'S')]
region = maze[(y - 1):(y + 2), (x - 1):(x + 2)]
print('\n'.join([''.join(x) for x in region.tolist()]))

sides = [Segment(x - 1, y, (x, y), mask), Segment(x, y - 1, (x, y), mask)]

i = 0
while (sides[0].x, sides[0].y) != (sides[1].x, sides[1].y):

    sides[i].step()
    i = (i + 1) % 2

# closing the loop
mask[sides[0].y, sides[0].x] = 'X'
# our S is a J
mask[mask == 'S'] = 'X'
maze[maze == 'S'] = 'J'

# removing redundant pieces
maze[mask != 'X'] = '.'

dots = np.where(maze == '.')
count = 0

for dot_y, dot_x in zip(*dots):

    line = ''.join([x for x in maze[dot_y, dot_x:] if x in ['|', 'F', '7', 'J', 'L']])
    crosses = line.count('|') + line.count('L7') + line.count('FJ')

    if crosses%2 == 1: # odd is inside
        count += 1
        maze[dot_y, dot_x] = 'I'
    else:
        maze[dot_y, dot_x] = 'O'

with open('./output.txt', 'w') as f:
    f.write('\n'.join([''.join(x) for x in maze.tolist()]))

print([side.n_steps for side in sides])
print(count)