import numpy as np
# Load input file into a 2D numpy array of single characters
file_path = "Wouter/day_10_input_test3.txt"
grid = np.genfromtxt(file_path, dtype=str, comments=None, delimiter=1, autostrip=True).transpose()
# grid = np.flipud(grid)
grid_height = grid.shape[0]
grid_width = grid.shape[1]

# Find coordinates of character 'S'
# Returns a tuple of two arrays, one for each dimension
S = np.where(grid == "S")

x = S[0][0]
y = S[1][0]
print(f"Starting position: {x, y}")

current_positions = []
previous_positions = []
# First iteration manually, as we don't know the shape of the starting pipe
# Check up
if grid[x, y - 1] in ["|", "F", "7"]:
    previous_positions.append((x, y))
    current_positions.append((x, y - 1))
# Check down
if grid[x, y + 1] in ["|", "L", "J"]:
    previous_positions.append((x, y))
    current_positions.append((x, y + 1))
# Check left
if grid[x - 1, y] in ["-", "F", "L"]:
    previous_positions.append((x, y))
    current_positions.append((x - 1, y))
# Check right
if grid[x + 1, y] in ["-", "7", "J"]:
    previous_positions.append((x, y))
    current_positions.append((x + 1, y))
print(f"Valid follow-up positions: {current_positions}")

distance_from_S = 1
# TODO: add checks for out of bound
# TODO : add stop criterium
loops = ['S'] * len(current_positions)
loop_round = False
while not loop_round:
    next_positions = []
    print(f"Distance from S: {distance_from_S}")
    for i, ((x, y), (x_prev, y_prev)) in enumerate(zip(current_positions, previous_positions)):
        loops[i] += grid[x, y]
        print(f"Loop {i}: {loops[i]}")
        print(f"Current position: {x, y} : {grid[x,y]}, previous position: {x_prev, y_prev} : {grid[x_prev, y_prev]}")
        print(f"Current character: {grid[x, y]}")
        # Based on the current character, and the previos posistion, we can determine the next position
        if grid[x, y] == "-":
            if x_prev + 1 == x:
                next_positions.append((x + 1, y))
            elif x_prev - 1 == x:
                next_positions.append((x - 1, y))
            else:
                raise ValueError("Invalid pipe")
        elif grid[x, y] == "|":
            if y_prev + 1 == y:
                next_positions.append((x, y + 1))
            elif y_prev - 1 == y:
                next_positions.append((x, y - 1))
            else:
                raise ValueError("Invalid pipe")
        elif grid[x, y] == "7":
            if y_prev - 1 == y and x_prev == x:
                next_positions.append((x - 1, y))
            elif x_prev + 1 == x and y_prev == y:
                next_positions.append((x, y + 1))
            else:
                raise ValueError("Invalid pipe")
        elif grid[x, y] == "J":
            if y_prev + 1 == y and x_prev == x:
                next_positions.append((x - 1, y))
            elif x_prev + 1 == x and y_prev == y:
                next_positions.append((x, y - 1))
            else:
                raise ValueError("Invalid pipe")
        elif grid[x, y] == "F":
            if y_prev - 1 == y and x_prev == x:
                next_positions.append((x + 1, y))
            elif x_prev - 1 == x and y_prev == y:
                next_positions.append((x, y + 1))
            else:
                raise ValueError("Invalid pipe")
        elif grid[x, y] == "L":
            if y_prev + 1 == y and x_prev == x:
                next_positions.append((x + 1, y))
            elif x_prev - 1 == x and y_prev == y:
                next_positions.append((x, y - 1))
            else:
                raise ValueError("Invalid pipe")
        elif grid[x, y] == "S":
            loop_round = True
            break
        else:
            raise ValueError("Invalid pipe")
        print(f"Next position: {next_positions[-1]}")

    previous_positions = current_positions
    current_positions = next_positions
    distance_from_S += 1

print(f"Loop: {loops[0]}")
print(f"distance from S: {(distance_from_S - 1)/2}")
    