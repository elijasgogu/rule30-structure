"""
Center column analysis for Rule 30.

Computes both the center bit (as in Wolfram's prize problem formulation) and
the center triplet decimal value (0–7) for each generation. The triplet captures
the full local context of the center cell — observing only the bit discards two
thirds of the structural information at each step.

Shows frequency distribution of all 8 possible triplet values and checks for
periodicity in the center triplet sequence.
"""

from collections import Counter

RULE30 = {
    (1,1,1): 0, (1,1,0): 0, (1,0,1): 0, (1,0,0): 1,
    (0,1,1): 1, (0,1,0): 1, (0,0,1): 1, (0,0,0): 0,
}

def next_gen(cells):
    p = [0,0] + cells + [0,0]
    return [RULE30[(p[i],p[i+1],p[i+2])] for i in range(len(p)-2)]

def center_triplet(cells):
    """Triplet and decimal value around the center cell."""
    mid = len(cells) // 2
    p = [0,0] + cells + [0,0]
    mid_p = mid + 2
    l, m, r = p[mid_p-1], p[mid_p], p[mid_p+1]
    return l, m, r, l*4 + m*2 + r

# --- Main ---

GENS = 64

cells = [0,0,1,0,0]
center_bits = []
center_vals = []

print(f"{'Gen':>4} | {'Center bit':>10} | {'Triplet (l,m,r)':>15} | {'Decimal':>7}")
print("-" * 52)

for gen in range(GENS):
    l, m, r, val = center_triplet(cells)
    center_bits.append(m)
    center_vals.append(val)
    print(f"{gen:>4} | {m:>10} | ({l},{m},{r}){' ':>8} | {val:>7}")
    cells = next_gen(cells)

print()
print("Center bit sequence (Wolfram's prize problem formulation):")
print(center_bits)
print()
print("Center triplet sequence (decimal values 0–7):")
print(center_vals)
print()

# Frequency distribution of decimal values
c = Counter(center_vals)
print("Frequency of decimal values in center triplet:")
for v in range(8):
    bar = "█" * c.get(v, 0)
    print(f"  {v}: {c.get(v,0):>3}x  {bar}")
print()

# Periodicity check: search for recurring subsequences
print("Searching for periodicity in center triplet sequence:")
found_period = False
for length in range(2, GENS // 2):
    seq = center_vals[:length]
    if center_vals[length:length*2] == seq:
        print(f"  Possible period of length {length} found: {seq}")
        found_period = True
        break
if not found_period:
    print(f"  No period found up to length {GENS // 2}.")