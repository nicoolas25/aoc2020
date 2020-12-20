import fileinput

inputs = []
for line in fileinput.input():
    inputs.append(int(line.strip()))

# Part 1

# inputs = sorted(inputs + [0])
# counters = { 0: 0, 1: 0, 2: 0, 3: 0}
# for i, adapter_rate in enumerate(inputs):
#     if i + 1 == len(inputs):
#         # Last adapter
#         counters[3] += 1
#     else:
#         diff = inputs[i+1] - adapter_rate
#         counters[diff] += 1
# print(counters[1] * counters[3])

_cache = {}
def arrangements(sorted_adapters, last_jolt=0):
    adapters_count = len(sorted_adapters)

    if adapters_count <= 1:
        return 1

    cache_key = (adapters_count, sorted_adapters[0], last_jolt)
    cached_result = _cache.get(cache_key, None)
    if cached_result is not None:
        return cached_result

    arrangements_count = 0
    for i, adapter_rate in enumerate(sorted_adapters):
        if adapter_rate - last_jolt > 3:
            break

        arrangements_count += arrangements(
            sorted_adapters[i+1:],
            last_jolt=adapter_rate,
        )

    _cache[cache_key] = arrangements_count
    return arrangements_count

print(arrangements(sorted(inputs), last_jolt=0))
