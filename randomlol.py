import random

input_list = input().split()
for i in range(len(input_list)):
    input_list[i] = int(input_list[i])

is_sorted = False
while not is_sorted:
    rando_list = random.shuffle(input_list)
    if rando_list == sorted(input_list):
        is_sorted = True
        print("yay", rando_list)
