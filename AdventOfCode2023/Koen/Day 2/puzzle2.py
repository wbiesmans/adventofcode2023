
import math

def check_game(game):
    colors = {
        'green' : 0,
        'blue' : 0,
        'red' : 0
    }
    for round in game:
        cubes = round.split(', ')
        for c in cubes:
            amount = int(c.split(' ')[0])
            color = c.split(' ')[1]
            if amount > colors[color]:
                colors[color] = amount
                
    power = math.prod(colors.values())
    return power


def main():

    with open('../Data/data.txt') as data:
        df = data.read().splitlines()

    sum = 0

    for line in df:
        game = line.split(': ')[1].split('; ')
        sum += check_game(game)

    print(sum)
if __name__ == '__main__':
    main()