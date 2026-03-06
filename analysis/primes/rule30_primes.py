"""
Prime factors beyond the system boundary in Rule 30 path numbers.

Collects all prime factors > 7 from path number values over a configurable
number of generations. The 3-bit system's structural primes are {2, 3, 5, 7} —
any prime factor larger than 7 emerges from the recursion itself, not from the
system's building blocks.

Adjust GENS at the top to control the analysis window.
"""

from collections import Counter

RULE30 = {
    (1,1,1): 0, (1,1,0): 0, (1,0,1): 0, (1,0,0): 1,
    (0,1,1): 1, (0,1,0): 1, (0,0,1): 1, (0,0,0): 0,
}

SYSTEM_PRIMES = {2, 3, 5, 7}
GENS = 1024   # adjust to change analysis window

def next_gen(cells):
    p = [0,0] + cells + [0,0]
    return [RULE30[(p[i],p[i+1],p[i+2])] for i in range(len(p)-2)]

def path_number(cells):
    total = 0
    for i in range(len(cells)-2):
        l, m, r = cells[i], cells[i+1], cells[i+2]
        total += l*4 + m*2 + r
    return total

def factorize(n):
    if n <= 1: return []
    factors, d = [], 2
    while d * d <= n:
        while n % d == 0:
            factors.append(d); n //= d
        d += 1
    if n > 1: factors.append(n)
    return factors

# --- Main ---

cells = [0,0,1,0,0]

outside_raw  = []   # all occurrences in order of appearance
outside_seen = []   # first occurrence only, order preserved
outside_set  = set()

for gen in range(GENS):
    pn = path_number(cells)
    for p in factorize(pn):
        if p not in SYSTEM_PRIMES:
            outside_raw.append(p)
            if p not in outside_set:
                outside_seen.append(p)
                outside_set.add(p)
    cells = next_gen(cells)

outside_sorted = sorted(outside_set)

# check which primes below the maximum found are absent
max_p = max(outside_sorted) if outside_sorted else 0

#from sympy import isprime
#all_primes_to_max = [p for p in range(8, max_p+1) if isprime(p)]

#missing = [p for p in all_primes_to_max if p not in outside_set]

print(f"Analysis window: {GENS} generations")
print(f"System primes:   {{2, 3, 5, 7}}")
print()
print(f"All prime factors > 7 (with repetition, in order of appearance):")
print(outside_raw)
print()
print(f"Unique prime factors > 7 (in order of first appearance):")
print(outside_seen)
print()
print(f"Unique prime factors > 7 (sorted):")
print(outside_sorted)
print()
print(f"Count of unique prime factors > 7: {len(outside_sorted)}")
print(f"Largest prime factor found:        {max_p}")
print()
'''if missing:
    print(f"Primes between 7 and {max_p} not yet observed:")
    print(missing)
else:
    print(f"No primes between 7 and {max_p} are missing — all appear within {GENS} generations.")'''