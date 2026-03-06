"""
R-pentomino: Path Number Prime Analysis
========================================
Systematic collection of all prime factors appearing as multipliers k
in path numbers of the form 511 × k, over a configurable number of
generations. Tracks primes within and beyond the system boundary 511.

Analogous to analysis/primes/rule30_primes.py for Rule 30.

Requires: numpy, sympy
Install:  pip install -r requirements.txt

Set GENS and SIZE to extend the investigation window.
Note: increase SIZE proportionally with GENS to avoid boundary artefacts.
"""

import numpy as np
from collections import Counter
from sympy import isprime as sympy_isprime


def factorize(n):
    if n <= 1:
        return []
    factors, d = [], 2
    while d * d <= n:
        while n % d == 0:
            factors.append(d)
            n //= d
        d += 1
    if n > 1:
        factors.append(n)
    return factors


def gol_next(grid):
    """One Game of Life step using numpy convolution."""
    neighbors = (
        np.roll(np.roll(grid, -1, 0), -1, 1) +
        np.roll(grid, -1, 0) +
        np.roll(np.roll(grid, -1, 0),  1, 1) +
        np.roll(grid,  0, 0) * 0 +   # placeholder — center not counted
        np.roll(grid, -1, 1) +
        np.roll(grid,  1, 1) +
        np.roll(np.roll(grid,  1, 0), -1, 1) +
        np.roll(grid,  1, 0) +
        np.roll(np.roll(grid,  1, 0),  1, 1)
    )
    return ((neighbors == 3) | ((grid == 1) & (neighbors == 2))).astype(np.int8)


def path_number(grid):
    """
    Sum of all 9-bit Moore neighbourhood decimal values.
    Each cell's neighbourhood is read as a 9-bit integer (NW N NE W C E SW S SE).
    Computed via numpy shifts — equivalent to the pure Python version but fast.
    """
    rows, cols = grid.shape
    shifts = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,0),(0,1),(1,-1),(1,0),(1,1)]
    total = np.zeros((rows, cols), dtype=np.int64)
    for bit, (dr, dc) in enumerate(shifts):
        weight = 1 << (8 - bit)  # MSB first: NW=256, N=128, NE=64, ...
        shifted = np.roll(np.roll(grid, dr, axis=0), dc, axis=1)
        total += shifted.astype(np.int64) * weight
    return int(total.sum())


def sieve(n):
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(n ** 0.5) + 1):
        if is_prime[i]:
            for j in range(i * i, n + 1, i):
                is_prime[j] = False
    return set(i for i in range(2, n + 1) if is_prime[i])


# --- Configuration ---
GENS = 1300       # extend as needed 
SIZE = 700       # must be large enough — R-pentomino stabilizes around gen 1103 
                 # for full stabilization use SIZE >= 600, GENS >= 1200
SYSTEM_BOUNDARY = 511  # 2^9 - 1 = 7 × 73

system_primes = sieve(SYSTEM_BOUNDARY)

# R-pentomino start condition
mid = SIZE // 2
grid = np.zeros((SIZE, SIZE), dtype=np.int8)
grid[mid][mid]         = 1
grid[mid][mid + 1]     = 1
grid[mid + 1][mid - 1] = 1
grid[mid + 1][mid]     = 1
grid[mid + 2][mid]     = 1

# --- Analysis ---
print(f"R-pentomino Path Number Prime Analysis")
print(f"Grid: {SIZE}×{SIZE}  ·  Generations: {GENS}  ·  System boundary: 511 = 7 × 73")
print()
print(f"{'Gen':>4} | {'Active':>6} | {'Path number':>14}    {'511 × k':<16}  k factorization          [!p]")
print("-" * 100)

k_factors_all     = []
k_factors_outside = []
first_appearance  = {}

for gen in range(GENS):
    pn = path_number(grid)
    ac = int(grid.sum())
    k  = pn // SYSTEM_BOUNDARY

    k_factors = factorize(k)
    c = Counter(k_factors)
    k_factors_all.extend(k_factors)

    outside = [p for p in k_factors if p not in system_primes]
    k_factors_outside.extend(outside)

    for p in set(k_factors):
        if p not in first_appearance:
            first_appearance[p] = gen

    full_pf     = " × ".join(
        (f"{p}^{c[p]}" if c[p] > 1 else str(p)) for p in sorted(c)
    ) or "1"
    outside_str = " ".join(f"[!p {p}]" for p in sorted(set(outside))) or ""

    print(f"{gen:>4} | {ac:>6} | {pn:>14}  =  511 × {k:<12}  k = {full_pf:<28} {outside_str}")
    grid = gol_next(grid)

# --- Summary ---
print()
print("=" * 100)
print("SUMMARY")
print("=" * 100)
print()

unique_k_factors = sorted(set(k_factors_all))
outside_unique   = sorted(p for p in unique_k_factors if p not in system_primes)
inside_unique    = sorted(p for p in unique_k_factors if p in system_primes)

print(f"Distinct prime factors of k within system boundary (≤ 511):")
for i in range(0, len(inside_unique), 20):
    print(f"  {inside_unique[i:i+20]}")
print()

if outside_unique:
    print(f"Distinct prime factors of k BEYOND system boundary (> 511):  [!p]")
    print(f"  {outside_unique}")
    print()
    print(f"  First appearances:")
    for p in outside_unique:
        print(f"    {p:>6}  →  gen {first_appearance[p]}")
    print()
    lo, hi = min(outside_unique), max(outside_unique)
    missing = [p for p in range(lo, hi + 1) if sympy_isprime(p) and p not in outside_unique]
    if missing:
        print(f"  Primes between {lo} and {hi} not yet observed:")
        print(f"    {missing}")
else:
    print(f"No prime factors beyond system boundary 511 observed in {GENS} generations.")
    print(f"Largest prime factor of k observed: {max(unique_k_factors)}")