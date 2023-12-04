import regex as re
import math

if __name__ == "__main__":
    # open file
    with open("Wouter/day_4_input_final.txt", "r") as f:
        line_number = -1
        card_instances = [1]*250
        # loop over lines in file
        while (line := f.readline()):
            line_number += 1
            card_id = re.findall(r'\d+', line.split(": ")[0])[0]
            # split on :
            scratchcards = line.split(": ")[1]
            game_split = scratchcards.split(" | ")

            set_of_winning_numbers = set(re.findall(r'\d+', game_split[0]))
            set_of_actual_numbers = set(re.findall(r'\d+', game_split[1]))
            num_winning_numbers = len(set_of_winning_numbers.intersection(set_of_actual_numbers))

            # Add appropriate number of card instances
            for i in range(num_winning_numbers):
                card_instances[line_number+1 + i] = card_instances[(line_number+1 + i)]  + card_instances[line_number]
            # print(card_instances)
            
        # print final sum
        print(sum(card_instances[0:line_number + 1]))
        
        