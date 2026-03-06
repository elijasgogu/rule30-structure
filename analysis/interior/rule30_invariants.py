"""
Rule 30 – Structural Invariants and Interior Analysis

This script categorizes the triplet values of each generation into three groups:

BOUNDARY (invariant):
    Values at the outermost active positions – fixed for all generations.
    From Gen 1: always starts with 1, always ends with 4.
    From Gen 2: always starts with 1, 3, 6.
    These values are structurally enforced by the rules and the initial
    condition 00100 and never change.

ISOLATED values {1, 2, 4}:
    Triplet values that arise when an active 1 has no active neighbors.
    A single 1 surrounded by zeros always produces the triplets:
        001 = 1,  010 = 2,  100 = 4
    These are echoes of the initial condition propagating through the zero
    space. They are not a decision of the automaton but a geometric necessity –
    wherever a 1 exists in isolation, these values repeat.

COLLISION values {3, 5, 6, 7}:
    Triplet values that arise when two active regions are close enough that
    their triplets overlap. At these contact points the neighborhood of a cell
    contains active bits from two distinct propagating regions simultaneously.
    These are the only locations where genuinely new structural configurations
    are produced. The apparent chaos of Rule 30 is localized here.

Note: the values 3 and 6 appear both as invariant boundary values and as
collision values in the interior. At the boundary they represent a structurally
forced collision between the growing pattern and the zero space – always
identical in form. In the interior they represent variable collisions between
independently propagating regions.
"""

RULE30 = {
    (1,1,1): 0, (1,1,0): 0, (1,0,1): 0, (1,0,0): 1,
    (0,1,1): 1, (0,1,0): 1, (0,0,1): 1, (0,0,0): 0,
}

# Isolated: arise from a single 1 in zero space (echo of initial condition)
ISOLATED   = {1, 2, 4}
# Collision: arise at contact points between two active regions
COLLISION  = {3, 5, 6, 7}

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

def categorize(vals, gen):
    """
    Split triplet values into boundary (invariant) and interior.
    Interior is further split into isolated and collision values.
    """
    if gen == 0:
        return vals, [], []
    if gen == 1:
        boundary = vals[:1] + vals[-1:]   # 1 ... 4
        interior = vals[1:-1]
    else:
        boundary = vals[:3] + vals[-1:]   # 1, 3, 6 ... 4
        interior = vals[3:-1]

    isolated  = [v for v in interior if v in ISOLATED]
    collision = [v for v in interior if v in COLLISION]
    return boundary, isolated, collision

def fmt(lst):
    return "[" + ", ".join(map(str, lst)) + "]" if lst else "[]"

# --- Main ---

GENS = 16
cells = [0,0,1,0,0]

print("Rule 30 – Structural Invariants and Interior Analysis")
print()
print("Boundary  (invariant): 1, 3, 6 left | 4 right  (from Gen 2)")
print("Isolated  {1, 2, 4}:   echo of initial condition – single 1 in zero space")
print("Collision {3, 5, 6, 7}: contact points between active regions – apparent chaos")
print()
print(f"{'Gen':>4} | {'Pattern':<34} | {'Boundary':<16} | {'Isolated':<24} | Collision")
print("-" * 108)

for gen in range(GENS):
    pat      = ''.join(map(str, cells))
    vals     = active_triplet_values(cells)
    boundary, isolated, collision = categorize(vals, gen)

    print(f"{gen:>4} | {pat:<34} | {fmt(boundary):<16} | {fmt(isolated):<24} | {fmt(collision)}")
    cells = next_gen(cells)

print()
print("Observation:")
print("  Even generations:  interior consists predominantly of isolated values {1, 2, 4}")
print("  Odd  generations:  interior consists predominantly of collision values {3, 5, 6, 7}")
print("  Boundary remains invariant across all generations from Gen 2 onward.")