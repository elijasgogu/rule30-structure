"""
2D Outer Totalistic Rule Space Analysis
=========================================
Scans all structurally valid outer totalistic 2D rules and classifies their
single-cell behaviour. Establishes what fraction of the theoretical rule space
is structurally bounded — analogous to the reduction from 256 to 32 rules
in 1D elementary cellular automata.

Outer totalistic rules: the next state of a cell depends only on its current
state (0 or 1) and the sum of its 8 Moore neighbours (0–8). This gives
2 × 9 = 18 binary decisions → 2^18 = 262,144 possible rules.

Structural constraints applied:
  1. 0 ∉ birth_set: dead cells with 0 live neighbours stay dead
     (no spontaneous generation from empty space)
     → reduces to 2^16 = 65,536 candidate rules

Classification of single-cell start condition over 25 generations:
  dies       → pattern reaches 0 active cells
  stable     → constant active cell count (period 1)
  period-N   → oscillating with period N
  growing    → cell count increasing at gen 25
  exploding  → cell count exceeds 60% of grid area
  other      → none of the above

Requires: numpy
Install:  pip install -r requirements.txt
"""

import numpy as np
from collections import defaultdict
import time

# --- Configuration ---
SIZE = 35   # grid size — increase for more accurate growing/exploding distinction
GENS = 25   # generations per rule test


def scan_all_rules(size, gens):
    counts   = defaultdict(int)
    gol_info = None

    for rule_id in range(2**16):
        b_mask = rule_id & 0xFF
        s_mask = (rule_id >> 8) & 0xFF

        birth_arr    = np.array(
            [(b_mask >> (s-1)) & 1 if s > 0 else 0 for s in range(9)], dtype=bool
        )
        survival_arr = np.array(
            [(s_mask >> (s-1)) & 1 if s > 0 else 0 for s in range(9)], dtype=bool
        )

        grid = np.zeros((size, size), dtype=np.int8)
        mid  = size // 2
        grid[mid][mid] = 1

        counts_ac = []
        exploded  = False

        for _ in range(gens):
            nb = (
                np.roll(np.roll(grid,-1,0),-1,1) + np.roll(grid,-1,0) +
                np.roll(np.roll(grid,-1,0), 1,1) + np.roll(grid,-1,1) +
                np.roll(grid, 1,1) +
                np.roll(np.roll(grid, 1,0),-1,1) + np.roll(grid, 1,0) +
                np.roll(np.roll(grid, 1,0), 1,1)
            )
            grid = (
                ((grid == 0) & birth_arr[nb]) |
                ((grid == 1) & survival_arr[nb])
            ).astype(np.int8)
            ac = int(grid.sum())
            counts_ac.append(ac)
            if ac > size * size * 0.6:
                exploded = True
                break

        if exploded:
            label = "exploding"
        elif counts_ac[-1] == 0:
            label = "dies"
        else:
            found = False
            for p in range(1, 5):
                if (len(counts_ac) >= p * 2 and
                        counts_ac[-p*2:-p] == counts_ac[-p:]):
                    label = "stable" if p == 1 else f"period-{p}"
                    found = True
                    break
            if not found:
                label = "growing" if counts_ac[-1] > counts_ac[gens//2] else "other"

        counts[label] += 1

        # identify Game of Life B3/S23
        birth_set    = {s for s in range(1, 9) if (b_mask >> (s-1)) & 1}
        survival_set = {s for s in range(1, 9) if (s_mask >> (s-1)) & 1}
        if birth_set == {3} and survival_set == {2, 3}:
            gol_info = label

    return counts, gol_info


# --- Main ---
print(f"2D Outer Totalistic Rule Space Analysis")
print(f"Grid: {SIZE}×{SIZE}  ·  {GENS} generations  ·  start: single active cell")
print(f"System boundary: 511 = 2⁹ − 1 = 7 × 73")
print()

start  = time.time()
counts, gol_info = scan_all_rules(SIZE, GENS)
elapsed = time.time() - start

total = sum(counts.values())

print(f"Scan complete in {elapsed:.1f}s")
print()
print("=" * 65)
print("CLASSIFICATION OF SINGLE-CELL BEHAVIOUR")
print("=" * 65)
for label, n in sorted(counts.items(), key=lambda x: -x[1]):
    pct = 100 * n / total
    bar = "█" * (n // 500)
    print(f"  {label:<14}  {n:>6}  ({pct:5.1f}%)  {bar}")

structured = sum(
    counts[k] for k in ["dies", "stable", "period-2", "period-3", "period-4"]
)
unbounded = counts["exploding"] + counts["growing"]

print()
print(f"  Structurally bounded (dies + stable + periodic):  {structured:>6}  ({100*structured/total:.1f}%)")
print(f"  Unbounded (exploding + growing):                  {unbounded:>6}  ({100*unbounded/total:.1f}%)")
print()
print("=" * 65)
print("REDUCTION THROUGH THE RULE SPACE")
print("=" * 65)
print()
print(f"  2^18 = {2**18:>8,}   all outer totalistic rules")
print(f"  2^16 = {2**16:>8,}   after constraint: 0 ∉ birth_set")
print(f"         {structured:>8,}   structurally bounded (single cell)")
print()
print(f"  Reduction factor (2^18 → bounded): {2**18 // max(structured,1):,}×")
print(f"  Reduction factor (2^16 → bounded): {2**16 // max(structured,1):,}×")
print()
print(f"  Compare 1D: 256 → 32  (reduction factor: 8×)")
print()
print("=" * 65)
print("GAME OF LIFE B3/S23")
print("=" * 65)
print()
print(f"  Single-cell behaviour:  {gol_info}")
print(f"  Root path number:       511 = 7 × 73 = 2⁹ − 1")
print(f"  Position in rule space: structurally bounded = {'yes' if gol_info in ['dies','stable','period-2','period-3','period-4'] else 'no'}")
