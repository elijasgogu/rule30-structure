"""
Rule 30 – Interior Analysis: Search for Additional Invariants

Starting from Gen 2, the known invariants are:
    Left boundary:  1, 3, 6  (first 3 active triplets)
    Right boundary: 4        (last active triplet)

This script strips these known invariants and displays the raw interior
for each generation, making it possible to identify any additional
invariant values that may emerge at fixed positions after Gen 2.

Isolated values  {1, 2, 4}: echo of initial condition, single 1 in zero space
Collision values {3, 5, 6, 7}: contact points between active regions
"""

RULE30 = {
    (1,1,1): 0, (1,1,0): 0, (1,0,1): 0, (1,0,0): 1,
    (0,1,1): 1, (0,1,0): 1, (0,0,1): 1, (0,0,0): 0,
}

def next_gen(cells):
    p = [0,0] + cells + [0,0]
    return [RULE30[(p[i],p[i+1],p[i+2])] for i in range(len(p)-2)]

def active_triplet_values(cells):
    p = [0,0] + cells + [0,0]
    vals = []
    for i in range(len(p)-2):
        l,m,r = p[i],p[i+1],p[i+2]
        if any(x!=0 for x in (l,m,r)):
            vals.append(l*4 + m*2 + r)
    return vals

def split(vals, gen):
    if gen == 0:
        return [], vals, []
    elif gen == 1:
        return vals[:1], vals[1:-1], vals[-1:]
    else:
        return vals[:3], vals[3:-1], vals[-1:]

def fmt(lst):
    return " ".join(map(str, lst)) if lst else "–"

# --- Main ---

GENS = 128
cells = [0,0,1,0,0]
rows  = []

for gen in range(GENS):
    vals = active_triplet_values(cells)
    left, interior, right = split(vals, gen)
    rows.append((gen, left, interior, right))
    cells = next_gen(cells)

GEN_W   = 4
LEFT_W  = 7    # "1 3 6"
RIGHT_W = 5    # "4"

header_interior = "Interior  [Left(1,3,6) ··· Right(4)]"

print("Rule 30 – Interior Analysis (known invariants stripped)")
print()
print("Left boundary  (Gen 2+): 1  3  6    invariant forced collision with zero space")
print("Right boundary (Gen 1+): 4          invariant forced collision with zero space")
print("Interior: isolated {1,2,4}  |  collision {3,5,6,7}")
print()
print(f"{'Gen':>{GEN_W}}  {'Left':<{LEFT_W}}  {'Right':<{RIGHT_W}}  {header_interior}")
print("-" * 80)

for gen, left, interior, right in rows:
    l = fmt(left).ljust(LEFT_W)
    r = fmt(right).ljust(RIGHT_W)
    i = fmt(interior)
    print(f"{gen:>{GEN_W}}  {l}  {r}  {i}")

print()

# --- Positional invariant check ---
print("Positional invariant check (Gen 2+, first 6 positions from each side):")
print()

gen2 = [(gen, interior) for gen, _, interior, _ in rows if gen >= 2]

for pos in range(6):
    vals = [interior[pos] for _, interior in gen2 if len(interior) > pos]
    unique = set(vals)
    status = f"INVARIANT = {unique.pop()}" if len(unique) == 1 else f"variable  {sorted(unique)}"
    print(f"  Left  +{pos}: {status}")

print()

for pos in range(1, 7):
    vals = [interior[-pos] for _, interior in gen2 if len(interior) >= pos]
    unique = set(vals)
    status = f"INVARIANT = {unique.pop()}" if len(unique) == 1 else f"variable  {sorted(unique)}"
    print(f"  Right -{pos}: {status}")
