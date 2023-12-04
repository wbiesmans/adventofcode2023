import regex as re

if __name__ == "__main__":
    # open file
    with open("Wouter/day_4_input_final.txt", "r") as f:
        sum = 0
        # loop over lines in file
        while (line := f.readline()):
            card_id = re.findall(r'\d+', line.split(": ")[0])[0]
            # split on :
            scratchcards = line.split(": ")[1]
            game_split = scratchcards.split(" | ")

            set_of_winning_numbers = set(re.findall(r'\d+', game_split[0]))
            set_of_actual_numbers = set(re.findall(r'\d+', game_split[1]))
            num_winning_numbers = len(set_of_winning_numbers.intersection(set_of_actual_numbers))
            num_points = 0
            if num_winning_numbers >= 1:
                num_points = 2**(num_winning_numbers -1)
            sum += num_points
            print(f"scratchcard {card_id}: {num_winning_numbers} numbers, {num_points} points")
        # print final sum
        print(sum)
            
