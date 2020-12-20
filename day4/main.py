import re
import fileinput

hair_color_re = re.compile(r"\A#[0-9a-f]{6}\Z")
pid_format_re = re.compile(r"\A[0-9]{9}\Z")
eye_colors = {'amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'}

def is_valid_hgt(hgt):
    unit = hgt[-2:]
    if unit == 'cm':
        return 150 <= int(hgt[:-2]) <= 193
    elif unit == 'in':
        return 59 <= int(hgt[:-2]) <= 76
    else:
        return False


class Passport:
    def __init__(self, byr = None, iyr = None, eyr = None, hgt = None, hcl = None, ecl = None, pid = None, cid = None):
        self.byr = byr
        self.iyr = iyr
        self.eyr = eyr
        self.hgt = hgt
        self.hcl = hcl
        self.ecl = ecl
        self.pid = pid
        self.cid = cid

    def is_valid(self):
        try:
            return (
                self.byr and 1920 <= int(self.byr) <= 2002 and
                self.iyr and 2010 <= int(self.iyr) <= 2020 and
                self.eyr and 2020 <= int(self.eyr) <= 2030 and
                self.hgt and is_valid_hgt(self.hgt) and
                self.hcl and hair_color_re.match(self.hcl) and
                self.ecl in eye_colors and
                self.pid and pid_format_re.match(self.pid)
            )
        except Exception as e:
            print(e)
            return False

passports = []
current_passport_fields = []
for i, line in enumerate(fileinput.input()):
    try:
        if line == "\n":
            passports.append(Passport(**{ name: value for name, value in current_passport_fields }))
            current_passport_fields = []
        else:
            current_passport_fields += [field.split(":") for field in line.strip().split()]
    except Exception as e:
        raise e

if current_passport_fields:
    passports.append(Passport(**{ name: value for name, value in current_passport_fields }))

print(sum(1 if p.is_valid() else 0 for p in passports))
