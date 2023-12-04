if __name__ == "__main__":
    # open file
    with open("Wouter/day_1_input_final.txt", "r") as f:
        sum = 0
        digits = [str(i) for i in range(10)]
        # loop over lines in file
        while (line := f.readline()):
            print(line)
            digits_list = []
            # loop over characters in line
            for char in line:
                # check if character is a digit, if so, add to list
                if char in digits:
                    digits_list.append(int(char))
            # Use first and last digit to create number
            number = 10*digits_list[0] + digits_list[-1]
            print(number)
            # add number to sum
            sum += number
        # print final sum
        print(sum)
            


