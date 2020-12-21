import fileinput

class Memory:
    def __init__(self):
        self.turn = 0
        self.last_number = None
        self.history = {}

    def speak(self, number):
        self.turn += 1
        count, n1, _ = self.history.get(number, (0, None, None))
        self.history[number] = (count + 1, self.turn, n1)
        self.last_number = number

    def last_spoken_number(self):
        last_count, n1, n2 = self.history.get(self.last_number, (0, None, None))
        return self.last_number, last_count, n1, n2

mem = Memory()

for number in next(fileinput.input()).split(','):
    mem.speak(int(number))

while mem.turn < 30000000:
    number, count, last_turn, turn_before_that = mem.last_spoken_number()
    mem.speak(last_turn - turn_before_that if count > 1 else 0)

print(mem.last_spoken_number()[0])
