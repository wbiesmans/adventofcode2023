import pandas as pd

# opening and reading the lines from the input
with open('./input.txt', 'r') as f:
    lines = f.readlines()

instructions = [*lines[0][:-1]]

data = [[line[:3], line[7:10], line[12:15]] for line in lines[2:]]
df = pd.DataFrame(data, columns=['pos', 'left', 'right'])


class Element(object):
    def __init__(self, pos, left=None, right=None):
        self.pos = pos
        self.left = left
        self.right = right

    def add_left(self, left):
        self.left = left
        return self

    def add_right(self, right):
        self.right = right
        return self

    def turn(self, direction):
        assert direction in ['L', 'R'], 'wrong turn'
        if direction=='L':
            return self.left
        if direction=='R':
            return self.right

    def __repr__(self):
        return f'node: {self.pos}'
        # return f'{self.pos} = ({str(self.left)}, {str(self.right)})'

df['element'] = df.apply(lambda x: Element(x.pos), axis='columns')

nodes_dict = df['element'].to_dict()

df['left'] = df.set_index('pos')['element'][df['left']].reset_index(drop=True)
df['right'] = df.set_index('pos')['element'][df['right']].reset_index(drop=True)

df.apply(lambda x: x.element.add_left(x.left).add_right(x.right), axis='columns')

location = df[df.pos == 'AAA'].iloc[0].element
steps = 0
directions = []
while location.pos != 'ZZZ':
    if len(directions)==0:
        directions = instructions.copy()
    direction = directions.pop(0)
    location = location.turn(direction)
    steps += 1

print(steps)