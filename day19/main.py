import fileinput

lines = [line.strip() for line in fileinput.input()]

rules = {}
while (line := lines.pop(0)):
    rule_index, rule_body = line.split(': ')
    if rule_body[0] == '"':
        rules[rule_index] = rule_body[1]
    else:
        rules[rule_index] = [ # disjunction of allowed sequences
            disjunction.split(' ')
            for disjunction in rule_body.split(' | ')
        ]

class Validator:
    def __init__(self, string):
        self.string = string

    def match(self):
        final_positions = self._match(positions=[0], rule_index='0')
        return any(p == len(self.string) for p in final_positions)

    def _match(self, positions, rule_index):
        rule = rules[rule_index]
        if isinstance(rule, str):
            return [
                p + 1
                for p in positions
                if len(self.string) > p
                and rule == self.string[p]
            ]
        else:
            valid_positions = []
            for position in positions:
                for sequence in rule:
                    current_positions = [position]
                    for current_rule_index in sequence:
                        current_positions = self._match(
                            positions=current_positions,
                            rule_index=current_rule_index,
                        )
                        if not current_positions:
                            break
                    else:
                        valid_positions += current_positions
            return valid_positions

print(sum(1 for line in lines if Validator(line).match()))
