import fileinput
from functools import reduce

class Group:
    def __init__(self):
        self.persons = []

    def __len__(self):
        return len(self.persons)

    def receive_answers(self, answers):
        self.persons.append({answer for answer in answers})

    @property
    def unanimous_answers_count(self):
        return len(
            reduce(
                lambda common_answers, answers: common_answers.intersection(answers),
                self.persons
            )
        )

groups = []
current_group = Group()
for line in fileinput.input():
    if line == '\n':
        groups.append(current_group)
        current_group = Group()
    else:
        current_group.receive_answers(line.strip())

if len(current_group):
    groups.append(current_group)

print(sum(group.unanimous_answers_count for group in groups))
