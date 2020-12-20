import fileinput

valid_passwords = 0
for line in fileinput.input():
    policy, password = line.strip().split(sep=': ', maxsplit=1)
    minmax, char = policy.split(sep=' ')
    min, max = map(int, minmax.split(sep='-'))
    if password[min - 1] == char and password[max - 1] != char:
        valid_passwords += 1
    if password[min - 1] != char and password[max - 1] == char:
        valid_passwords += 1

print(valid_passwords)
