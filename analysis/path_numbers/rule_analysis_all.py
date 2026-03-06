"""
Path number analysis of all 32 structurally independent cellular automaton rules.

Start condition: always 00100 (fixed for all rules)
Root:           path number gen 0 = 7 (always)
Valid rules:    4, 12, 20 ... 252 (step size 8, 32 rules)
Path number:    sum of all triplet decimal values across the recursion

Note: Wolfram's Rule 30 = rule 60 in structural notation
"""

def make_rule(n):
    rule = {}
    for i in range(8):
        l=(i>>2)&1; m=(i>>1)&1; r=i&1
        rule[(l,m,r)] = (n>>i)&1
    return rule

def next_gen(cells, rule):
    p = [0,0] + cells + [0,0]
    return [rule[(p[i],p[i+1],p[i+2])] for i in range(len(p)-2)]

def path_number(cells):
    p = [0,0] + cells + [0,0]
    return sum(p[i]*4 + p[i+1]*2 + p[i+2] for i in range(len(p)-2))

def factorize(n):
    if n <= 1: return []
    factors, d = [], 2
    while d * d <= n:
        while n % d == 0:
            factors.append(d); n //= d
        d += 1
    if n > 1: factors.append(n)
    return sorted(set(factors))

START = [1, 0, 0]  # 00100
GENS  = 17   # gen 0 through gen 16

print(f"Start condition: 00100  |  Root = {path_number(START)}")
print()
print(f"{'Rule':<6} | {'Root':>6} | {'Factors':<18} | Path numbers gen 0–16")
print("-" * 110)

for n in range(4, 257, 8):
    rule   = make_rule(n)
    cells  = START[:]
    pns    = []
    for _ in range(GENS):
        pns.append(path_number(cells))
        cells = next_gen(cells, rule)

    root    = pns[0]
    factors = factorize(n)
    fstr    = " x ".join(map(str, factors)) if factors else "-"
    pstr    = " ".join(f"{p:>5}" for p in pns)
    note    = "  <- Wolfram Rule 30" if n == 60 else ""
    print(f"{n:<6} | {root:>6} | {fstr:<18} | {pstr}{note}")