import numpy as np
# Load input file into a 2D numpy array of single characters
file_path = "Wouter/day_10_input_final.txt"
grid = np.genfromtxt(file_path, dtype=str, comments=None, delimiter=1, autostrip=True).transpose()
grid_mask = np.zeros_like(grid, dtype=bool)
# grid = np.flipud(grid)
grid_height = grid.shape[1]
grid_width = grid.shape[0]

# Find coordinates of character 'S'
# Returns a tuple of two arrays, one for each dimension
S = np.where(grid == "S")

x = S[0][0]
y = S[1][0]
grid_mask[x, y] = True
print(f"Starting position: {x, y}")

current_positions = []
previous_positions = []
# First iteration manually, as we don't know the shape of the starting pipe
up, down, left, right = False, False, False, False
# Check up
if grid[x, y - 1] in ["|", "F", "7"]:
    previous_positions.append((x, y))
    current_positions.append((x, y - 1))
    up = True
# Check down
if grid[x, y + 1] in ["|", "L", "J"]:
    previous_positions.append((x, y))
    current_positions.append((x, y + 1))
    down = True
# Check left
if grid[x - 1, y] in ["-", "F", "L"]:
    previous_positions.append((x, y))
    current_positions.append((x - 1, y))
    left = True
# Check right
if grid[x + 1, y] in ["-", "7", "J"]:
    previous_positions.append((x, y))
    current_positions.append((x + 1, y))
    right = True
print(f"Valid follow-up positions: {current_positions}")

distance_from_S = 1
# TODO: add checks for out of bound
# TODO : add stop criterium
loops = ['S'] * len(current_positions)
loop_round = False
while not loop_round:
    next_positions = []
    # print(f"Distance from S: {distance_from_S}")
    for i, ((x, y), (x_prev, y_prev)) in enumerate(zip(current_positions, previous_positions)):
        grid_mask[x, y] = True
        loops[i] += grid[x, y]
        # print(f"Loop {i}: {loops[i]}")
        # print(f"Current position: {x, y} : {grid[x,y]}, previous position: {x_prev, y_prev} : {grid[x_prev, y_prev]}")
        # print(f"Current character: {grid[x, y]}")
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
        # print(f"Next position: {next_positions[-1]}")

    previous_positions = current_positions
    current_positions = next_positions
    distance_from_S += 1

print(f"Loop: {loops[0]}")
print(f"distance from S: {(distance_from_S - 1)/2}")

# Part 2 : when count is odd, '.' symbols are added to the count
# Replace S with a pipe
if up and down:
    grid[x, y] = "|"
elif left and right:
    grid[x, y] = "-"
elif left and up:
    grid[x, y] = "J"
elif right and down:
    grid[x, y] = "F"
elif left and down:
    grid[x, y] = "J"
elif right and up:
    grid[x, y] = "L"
else:
    raise ValueError("Invalid starting pipe")
print(f"Starting pipe: {grid[x, y]}")

def custom_print(grid):
    for y in range(grid.shape[1]):
        for x in range(grid.shape[0]):
            print(grid[x,y], end='')
        print()


inside_tiles_count = 0
# for each row
for y in range(grid_height):
    boundaries_count = 0
    # from left to right, count the number of loop parts we encounter
    src = None
    for x in range(grid_width):
        if grid_mask[x,y]:
            if grid[x,y] in ['|']:
                boundaries_count += 1
            elif grid[x,y] in ['L']:
                if not src:
                    src = 'up'
                else:
                    raise ValueError("Invalid pipe")
            elif grid[x,y] in ['F']:
                if not src:
                    src = 'down'
                else:
                    raise ValueError("Invalid pipe")
            elif grid[x,y] in ['J']:
                if not src:
                    raise ValueError("Invalid pipe")
                elif src == 'down':
                    boundaries_count += 1
                    src = None
                elif src == 'up':
                    boundaries_count += 0
                    src = None
                else:
                    raise ValueError("Invalid pipe")
            elif grid[x,y] in ['7']:
                if not src:
                    raise ValueError("Invalid pipe")
                elif src == 'down':
                    boundaries_count += 0
                    src = None
                elif src == 'up':
                    boundaries_count += 1
                    src = None
                else:
                    raise ValueError("Invalid pipe")
            elif grid[x,y] in ['-']:
                boundaries_count += 0
                if src is None:
                    raise ValueError("Invalid pipe")
            else:
                raise ValueError("Invalid pipe")
        else:
            # if we encounter a '.', and the count is odd, we add 1 to the inside tiles count
            if boundaries_count % 2 == 1:
                inside_tiles_count += 1
                grid[x,y] = 'I'
            elif boundaries_count % 2 == 0:
                grid[x,y] = 'O'
custom_print(grid)
custom_print(grid_mask)
print(f"Total count: {inside_tiles_count}")


    