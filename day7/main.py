import fileinput

# Holds name: [(count, other_name)]
bags = {}

def parse(line):
    name, rest = line.split(' bags contain ', maxsplit=1)
    bags[name] = []
    if rest != 'no other bags.':
        for content in rest.split(', '):
            count, rest = content.split(' ', maxsplit=1)
            other_name, _ = rest.split(' bag', maxsplit=1)
            bags[name].append((int(count), other_name))

for line in fileinput.input():
    parse(line.strip())

def contains_shiny_gold(name):
    return (
        any(
            inner_bag
            for _count, inner_bag in bags[name]
            if inner_bag == 'shiny gold'
        ) or any(
            inner_bag
            for _count, inner_bag in bags[name]
            if contains_shiny_gold(inner_bag)
        )
    )

def count_contained_bags(bag_name, count=1):
    return count + sum(
        count * count_contained_bags(inner_bag, inner_count)
        for inner_count, inner_bag in bags[bag_name]
    )

print(sum(1 for bag_name in bags.keys() if contains_shiny_gold(bag_name)))
print(count_contained_bags('shiny gold') - 1)
