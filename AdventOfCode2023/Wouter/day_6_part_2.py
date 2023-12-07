import math
with open("Wouter/day_6_input_test.txt", "r") as f:
    input_lines = f.readlines()

    # test
    # time = 71530
    # record_distance = 940200
    # final
    time = 60808676
    record_distance = 601116315591300

    # quadtratic equation : -x^2 + time - distance = 0
    # two solutions :
    time_1 = (time - math.sqrt(time**2 - 4*record_distance))/2
    time_2 = (time + math.sqrt(time**2 - 4*record_distance))/2
    time_1 = math.ceil(time_1)
    time_2 = math.floor(time_2)
    print(f"{time_1=} {time_2=}")
    num_solutions = len(range(time_1, time_2+1))
    print(f"{num_solutions=}")
