
# opening and reading the lines from the input
with open('./input.txt', 'r') as f:
    lines = f.readlines()

bag = {
    'red': 12,
    'green': 13,
    'blue': 14,
}
count = 0
for line in lines:
    idx = int(line.split(': ')[0].split(' ')[-1])
    games = line.split(': ')[-1].split('; ')
    valid = True
    for game in games:
        draws = game.split(', ')
        for color, amount in bag.items():
            if sum([int(x.split(' ')[0]) for x in draws if color in x]) > amount:
                valid = False

    if valid:
        count+=idx

print(count)

