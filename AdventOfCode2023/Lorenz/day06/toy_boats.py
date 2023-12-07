
# opening and reading the lines from the input
with open('./input.txt', 'r') as f:
    lines = f.readlines()

times = [int(x) for x in lines[0].split(':')[-1][:-1].split(' ') if x != '']
distances = [int(x) for x in lines[1].split(':')[-1][:-1].split(' ') if x != '']
num_solutions = 1
for time, distance in zip(times, distances):

    time_holding = [time - x for x in range(time+1)]
    time_left = [time-x for x in time_holding]
    distance_traveled = [x*y for x, y in zip(time_holding, time_left)]

    num_solutions *= sum([x>distance for x in distance_traveled])

print(num_solutions)