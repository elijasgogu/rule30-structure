"""
Path number analysis of Rule 30 (structurally Rule 60).

Start condition: 00100
Rule 30 = structural Rule 60 (two trailing zeros belong to the active cell's
necessary state space and are not output bits)

Path number: sum of all triplet decimal values across one generation.
System primes: the four primes within the 3-bit value range {0..7}: 2, 3, 5, 7
Prime factors outside the system boundary are marked with [!p].
"""

from collections import Counter

RULE30 = {
    (1,1,1): 0, (1,1,0): 0, (1,0,1): 0, (1,0,0): 1,
    (0,1,1): 1, (0,1,0): 1, (0,0,1): 1, (0,0,0): 0,
}

SYSTEM_PRIMES = {2, 3, 5, 7}

def next_gen(cells):
    p = [0,0] + cells + [0,0]
    return [RULE30[(p[i],p[i+1],p[i+2])] for i in range(len(p)-2)]

def path_number(cells):
    total = 0
    for i in range(len(cells)-2):
        l, m, r = cells[i], cells[i+1], cells[i+2]
        total += l*4 + m*2 + r
    return total

def binary_value(cells):
    return int(''.join(map(str, cells)), 2)

def pattern_str(cells):
    return ''.join(map(str, cells))

def factorize(n):
    """Prime factorization with repetition, e.g. 28 -> [2, 2, 7]"""
    if n <= 1: return []
    factors, d = [], 2
    while d * d <= n:
        while n % d == 0:
            factors.append(d); n //= d
        d += 1
    if n > 1: factors.append(n)
    return factors

def factor_str(n):
    """
    Formats prime factorization.
    Factors within {2,3,5,7} shown normally; factors outside marked with [!p].
    """
    f = factorize(n)
    if not f: return "-"
    c = Counter(f)
    inside, outside = [], []
    for p in sorted(c):
        exp = c[p]
        s = f"{p}^{exp}" if exp > 1 else str(p)
        if p in SYSTEM_PRIMES:
            inside.append(s)
        else:
            outside.append(s)
    result = " × ".join(inside)
    if outside:
        result += "  [!" + " × ".join(outside) + "]"
    return result

# --- Main ---

cells = [0,0,1,0,0]

print(f"{'Gen':>4} | {'Pattern':<35} | {'Binary dec':>12} | {'Path num':>8} | Prime factors")
print(f"{'':>4}   {'':35}   {'':12}   {'':8}   (system: {{2,3,5,7}}  outside boundary: [!p])")
print("-" * 105)

for gen in range(128):
    pat     = pattern_str(cells)
    bin_val = binary_value(cells)
    pn      = path_number(cells)
    fs      = factor_str(pn)

    print(f"{gen:>4} | {pat:<35} | {bin_val:>12} | {pn:>8} | {fs}")

    cells = next_gen(cells)