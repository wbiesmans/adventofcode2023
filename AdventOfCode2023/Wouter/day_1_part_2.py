# note that written digits can overlap, so we can't just replace them with digits
def find_digits(line):
    """Find digits in line and add them to found_digits list."""
    digits = [str(i) for i in range(10)]
    digits_written = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']

    found_digits = []
    found_indices = []
    # find indices of written digits.
    # Note that written digits can occur multiple times in a line
    for digit_written, digit in zip(digits_written, digits):
        start_index = -1
        while((start_index := line.find(digit_written, start_index + 1)) != -1):
            found_indices.append(start_index)
            found_digits.append(int(digit))
    
    # find indices of digits
    for i, c in enumerate(line):
        # check if character is a digit
        if c in digits:
            # add digit to digits_list
            found_indices.append(i)
            found_digits.append(int(c))

    # sort digits according to their index in line
    found_digits = [x for _,x in sorted(zip(found_indices, found_digits))]
    print(found_digits)
    return found_digits


if __name__ == "__main__":
    # open file
    with open("input.txt", "r") as f:
        sum = 0
        # loop over lines in file
        while (line := f.readline()):
            print(line)
            # loop over characters in line
            found_digits = find_digits(line)
            # Use first and last digit to create number
            number = 10*found_digits[0] + found_digits[-1]
            print(number)
            # add number to sum
            sum += number
        # print final sum
        print(sum)