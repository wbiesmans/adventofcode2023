import numpy as np
import regex as re

# python indexing : up to and not including the last index
# This means that the last index can be equal to the length of the array
def get_surrounding_submatrix(matrix, line_number, span):
    # Get the submatrix surrounding the number
    nrows = matrix.shape[0]
    ncols = matrix.shape[1]
    submatrix = matrix[max(0, line_number - 1): (min(line_number + 1 + 1, nrows)), \
                     max(0, span[0] - 1): min(span[1] + 1, ncols)]
    return submatrix

def adjacent_number_count(submatrix):
    num_numbers = 0
    for line in submatrix:
        incomplete_number_matches = re.findall(r"\d+", "".join(line.flatten()))
        num_numbers += len(incomplete_number_matches)
    return num_numbers

def get_full_numbers(matrix, line_number, span_asterisk):
    nrows = matrix.shape[0]
    ncols = matrix.shape[1]
    line_indices = (max(0, line_number - 1), min(line_number + 1 + 1, nrows))
    column_indices = (max(0, span_asterisk[0] - 1), min(span_asterisk[1] + 1, ncols))
    print(matrix[line_indices[0]:(line_indices[1]), column_indices[0]:(column_indices[1])])
    numbers = []
    for line_index in range(line_indices[0], line_indices[1]):
        match_index = -1
        for match in re.finditer(r"\d+", "".join(matrix[line_index, column_indices[0]:column_indices[1]])):
            match_index += 1
            number = int(match.group())
            print(f"partial number: ", number)
            span_number = match.span()
            col_indices_temp = column_indices
            line_extended = line
            # Extend the span of the number to the left (if possible) until it is a full number
            while(span_number[0] == 0 and col_indices_temp[0] > 0):
                col_indices_temp = (col_indices_temp[0] - 1, col_indices_temp[1])
                line_extended = matrix[line_index, col_indices_temp[0]:col_indices_temp[1]]
                # search again and update span
                temp_matches = re.finditer(r"\d+", "".join(line_extended))
                temp_match = next(x for i,x in enumerate(temp_matches) if i==match_index)
                span_number = temp_match.span()
                number = int(temp_match.group())
            # Extend the span of the number to the right (if possible) until it is a full number
            while(span_number[1] == (col_indices_temp[1] - col_indices_temp[0]) and col_indices_temp[1] < matrix.shape[1]):
                col_indices_temp = (col_indices_temp[0], col_indices_temp[1] + 1)
                line_extended = matrix[line_index, col_indices_temp[0]:col_indices_temp[1]]
                # search again and update span
                temp_matches = re.finditer(r"\d+", "".join(line_extended))
                temp_match = next(x for i,x in enumerate(temp_matches) if i==match_index)
                span_number = temp_match.span()
                number = int(temp_match.group())
            print(f"{col_indices_temp} : {line_extended}")
            print("full number: ", number)
            numbers.append(int(number))
    print("found numbers: ", numbers)
    return numbers


if __name__ == "__main__":
    # file_path = "Wouter/day_3_input_test.txt"
    file_path = "Wouter/day_3_input_final.txt"

    # With numpy, parse file into 2d array of single characters
    # each line is a row, each character is a column
    matrix = np.genfromtxt(file_path, dtype=str, comments=None, delimiter=1, autostrip=True)
    print(f"matrix size: {matrix.shape}")

    sum = 0
    # Line by line, search for numbers, and their corresponding indices
    for line_number, line in enumerate(matrix):
        line = "".join(line)
        for match in re.finditer(r"\*", line):
            span = match.span()
            submatrix = get_surrounding_submatrix(matrix, line_number, span)
            # Check how many numbers are adjacent to the asterisk
            if adjacent_number_count(submatrix) != 2:
                continue
            print(submatrix)
            # For each of the number matches, check if it is a complete number
            full_numbers = get_full_numbers(matrix, line_number, span)
            # product of the full numbers
            product = np.prod(full_numbers)
            sum += product

    print(f"sum: {sum}")
