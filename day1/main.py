import fileinput

inputs = [
    int(line.strip())
    for line in fileinput.input()
]

for i in inputs:
    for j in inputs:
        for k in inputs:
            if i + j + k == 2020:
                print(i * j * k)
