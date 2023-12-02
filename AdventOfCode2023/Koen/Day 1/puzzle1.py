numbs = [str(i) for i in range(10)]
out = 0
with open("../Data/input1.txt") as calibration:
    for line in calibration.readlines():
        numbers_input = [character for character in line if character in numbs]
        out += int(numbers_input[0]+numbers_input[-1])
print(out)
