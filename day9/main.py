import fileinput

# Part 1

# inputs = []
# for i, line in enumerate(fileinput.input()):
#     number = int(line.strip())
#     inputs.append(number)
#     if i < 25:
#         continue
# 
#     if not any(
#         1
#         for a in inputs[-26:-1]
#         for b in inputs[-26:-1]
#         if a != b and (a + b) == number
#     ):
#         print(number)
#         break

# Part 2

target = 556543474
inputs = []
for line in fileinput.input():
    number = int(line.strip())
    inputs.append(number)
    range_numbers = []
    for n in inputs[::-1]:
        range_numbers.append(n)
        range_sum = sum(range_numbers)
        if range_sum == target:
            print(min(range_numbers) + max(range_numbers))
            break
        elif range_sum > target:
            break

