COLORS = ["red", "green", "blue"]

def get_game_id(line):
    """Returns game id as integer"""
    # second word before colon is game id
    return int(line.split(":")[0].split(" ")[1])

def get_draws(line):
    """ Returns list of draws as list of list of integers,
        in order of colors in COLORS
    """
    # select all text after colon, split on semicolon
    draws_text = line.split(":")[1].split(";")
    draws_int = []
    # for each draw
    for draw_text in draws_text:
        # split draw on comma
        draw_percolor = draw_text.strip().split(",")
        draw_int = [0, 0, 0]
        for color_draw in draw_percolor:
            # Get color and number, convert to integer
            color = color_draw.strip().split(" ")[1]
            number = int(color_draw.strip().split(" ")[0])
            # put the number in the right place in the list            
            color_index = COLORS.index(color)
            draw_int[color_index] = number
        # add draw to list of draws
        draws_int.append(draw_int)
    return draws_int

def valid_draws(draws, bag_contents):
    for draw in draws:
        for i in range(len(bag_contents)):
            if draw[i] > bag_contents[i]:
                return False
    return True

if __name__ == "__main__":
    bag_contents = [13, 14, 15]
    # file_path = "Wouter/day_2_input_1.txt"
    file_path = "Wouter/day_2_input_final.txt"

    print(f"bag_contents : {bag_contents}")
    print(f"color order : {COLORS}")
    # Open file
    with open(file_path, "r") as f:
        sum = 0
        # for each line
        while(line:=f.readline().strip()):
            print(line)
            game_id = get_game_id(line)
            draws = get_draws(line)
            print(draws)
            if valid_draws(draws, bag_contents):
                sum += game_id
                print("valid")
            else:
                print("invalid")
        print(f"sum of valid game ids : {sum}")


            