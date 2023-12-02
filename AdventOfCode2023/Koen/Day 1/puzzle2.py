out = 0
numbs = {'zero':'0', 'one':'1', 'two':'2', 'three':'3', 'four':'4', 'five':'5', 'six':'6', 'seven':'7', 'eight':'8', 'nine':'9', '0':'0', '1':'1', '2':'2', '3':'3', '4':'4', '5':'5', '6':'6', '7':'7', '8':'8', '9':'9'}
with open('../Data/input1.txt') as calibration:
    for line in calibration.readlines():
        numbers_input = {index:v for k, v in numbs.items() if (index := line.find(k)) != -1}
        numbers_input.update({index:v for k, v in numbs.items() if (index := line.rfind(k)) != -1})
        sorted_in = sorted(numbers_input)
        out += int(numbers_input[sorted_in[0]]+numbers_input[sorted_in[-1]])
print(out)