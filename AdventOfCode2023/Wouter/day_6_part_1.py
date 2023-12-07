with open("Wouter/day_6_input_final.txt", "r") as f:
    input_lines = f.readlines()

    times = [int(x) for x in input_lines[0].split(": ")[1].split()]
    record_distances = [int(x) for x in input_lines[1].split(": ")[1].split()]

    total_count = 1
    for time, record_distance in zip(times, record_distances):
        print(f"{time=} {record_distance=}")
        my_distances = []
        for i in range(1, time):
            # Hold button for i seconds.
            # # Travel for time-i seconds at speed i
            my_distances.append((time - i)*i)
        print(f"{my_distances=}")
        num_records_beaten = len([d for d in my_distances if d > record_distance])
        total_count *= num_records_beaten
        print(f"{num_records_beaten=}")
    print(f"{total_count=}")