def check_game(game):
    max_values = {
        'red' : 12,
        'green' : 13,
        'blue' : 14
    }
    valid = True
    for round in game:
        cubes = round.split(', ')
        for c in cubes:
            sum = int(c.split(' ')[0])
            color = c.split(' ')[1]
            if sum > max_values[color]:
                valid = False
        
    return valid

def main():

    with open('../Data/data.txt') as data:
        df = data.read().splitlines()
    sum = 0

    for line in df:
        id = int(line.split(': ')[0].split(" ")[1])
        game = line.split(': ')[1].split('; ')
        if check_game(game):
            sum += id
    print(sum)
    
if __name__ == '__main__':
    main()