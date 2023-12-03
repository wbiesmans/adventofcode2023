import numpy as np
import regex as re


def get_surrounding_submatrix(matrix, line_number, span):
    # Get the submatrix surrounding the number
    nrows = matrix.shape[0]
    ncols = matrix.shape[1]
    submatrix = matrix[max(0, line_number - 1): (min(line_number + 1, nrows) + 1), \
                     max(0, span[0] - 1): min(span[1] + 1, ncols)]
    return submatrix


if __name__ == "__main__":
    # file_path = "Wouter/day_3_input_test.txt"
    file_path = "Wouter/day_3_input_final.txt"

    # With numpy, parse file into 2d array of single characters
    # each line is a row, each character is a column
    matrix = np.genfromtxt(file_path, dtype=str, comments=None, delimiter=1, autostrip=True)


    sum = 0
    # Line by line, search for numbers, and their corresponding indices
    for line_number, line in enumerate(matrix):
        line = "".join(line)
        for match in re.finditer(r"\d+", line):
            number = int(match.group())
            span = match.span()
            submatrix = get_surrounding_submatrix(matrix, line_number, span)
            # If submatrix contains a symbol, add number to sum
            # regex that matches any character that is not a digit or a point
            if re.search(r"[^0-9.]", "".join(submatrix.flatten())):
                print(number)
                print(submatrix)
                sum += number
    print(f"sum: {sum}")
