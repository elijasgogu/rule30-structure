"""
Game of Life – Path Number Analysis
=====================================
Applies the path number method to 2D cellular automata (Game of Life B3/S23).

Instead of 1D triplet decimal values (0–7, system boundary 7),
this script measures 9-bit Moore neighbourhood values (0–511, system boundary 511).
The path number of a generation is the sum of all neighbourhood decimal values.

Three start conditions are analysed:
  - Blinker   : period-2 oscillator (3 active cells)
  - Glider    : moving pattern (5 active cells)
  - R-pentomino: chaotic growth (5 active cells)

Key findings:
  - A single active cell in 2D always produces path number 511 = 7 × 73
  - 511 = 2^9 - 1 is the system boundary, analogous to 7 = 2^3 - 1 in 1D
  - 73 appears as invariant factor in every path number across all patterns
  - 7 appears in most but not all path numbers (partial invariance)
  - No prime factors beyond system boundary 511 observed in 30 generations
  - All primes observed (11, 13, 19, 23, ...) lie within the system boundary

See: docs/game_of_life_path_numbers.md for full analysis and observations.
"""

from collections import Counter


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
    rows, cols = len(grid), len(grid[0])
    new = [[0] * cols for _ in range(rows)]
    for r in range(rows):
        for c in range(cols):
            neighbors = sum(
                grid[r + dr][c + dc]
                for dr in (-1, 0, 1)
                for dc in (-1, 0, 1)
                if (dr, dc) != (0, 0)
                and 0 <= r + dr < rows
                and 0 <= c + dc < cols
            )
            if grid[r][c] == 1:
                new[r][c] = 1 if neighbors in (2, 3) else 0
            else:
                new[r][c] = 1 if neighbors == 3 else 0
    return new


def path_number(grid):
    """Sum of all 9-bit Moore neighbourhood decimal values across the grid."""
    rows, cols = len(grid), len(grid[0])
    total = 0
    for r in range(rows):
        for c in range(cols):
            bits = []
            for dr in (-1, 0, 1):
                for dc in (-1, 0, 1):
                    if 0 <= r + dr < rows and 0 <= c + dc < cols:
                        bits.append(grid[r + dr][c + dc])
                    else:
                        bits.append(0)
            val = sum(b << (8 - i) for i, b in enumerate(bits))
            total += val
    return total


def make_grid(size, cells):
    g = [[0] * size for _ in range(size)]
    for r, c in cells:
        g[r][c] = 1
    return g


def sieve(n):
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(n ** 0.5) + 1):
        if is_prime[i]:
            for j in range(i * i, n + 1, i):
                is_prime[j] = False
    return set(i for i in range(2, n + 1) if is_prime[i])


# --- Configuration ---
SIZE = 50
GENS = 30
SYSTEM_BOUNDARY = 511  # 2^9 - 1 = 7 × 73

system_primes = sieve(SYSTEM_BOUNDARY)
mid = SIZE // 2

patterns = {
    "Blinker (period-2)": [
        (mid, mid - 1), (mid, mid), (mid, mid + 1)
    ],
    "Glider": [
        (mid,     mid + 1),
        (mid + 1, mid + 2),
        (mid + 2, mid),
        (mid + 2, mid + 1),
        (mid + 2, mid + 2),
    ],
    "R-pentomino (chaotic)": [
        (mid,     mid),
        (mid,     mid + 1),
        (mid + 1, mid - 1),
        (mid + 1, mid),
        (mid + 2, mid),
    ],
}

# --- Main analysis ---
for name, cells in patterns.items():
    grid = make_grid(SIZE, cells)
    print("=" * 88)
    print(f"  {name}")
    print(f"  Grid: {SIZE}×{SIZE}  ·  System boundary: {SYSTEM_BOUNDARY} = 7 × 73  ·  {GENS} generations")
    print("=" * 88)
    print(f"{'Gen':>4} | {'Active':>6} | {'Path number':>13}    {'511 × k':<14}    Prime factorization")
    print("-" * 88)

    root_pn = None
    outside_all = []

    for gen in range(GENS):
        pn = path_number(grid)
        ac = sum(cell for row in grid for cell in row)
        factors = factorize(pn)
        c = Counter(factors)

        inside  = [p for p in sorted(c) if p in system_primes]
        outside = [p for p in sorted(c) if p not in system_primes and p > 1]

        if gen == 0:
            root_pn = pn

        k           = pn // SYSTEM_BOUNDARY
        k_str       = f"511 × {k}"
        inside_str  = " × ".join(
            (f"{p}^{c[p]}" if c[p] > 1 else str(p)) for p in inside
        ) or "–"
        outside_str = " × ".join(str(p) for p in outside) or "–"

        outside_all.extend(outside)
        print(f"{gen:>4} | {ac:>6} | {pn:>13}  =  {k_str:<12} →  {inside_str}")
        grid = gol_next(grid)

    print()
    print(f"  Root path number : {root_pn}  =  {factorize(root_pn)}")
    unique = sorted(set(outside_all))
    print(f"  Primes beyond 511: {len(unique)}  →  {unique if unique else '–'}")
    print()

# --- Structural note: single active cell ---
print("=" * 88)
print("  STRUCTURAL NOTE: single active cell")
print("=" * 88)
single = [[0] * 10 for _ in range(10)]
single[5][5] = 1
pn_single = path_number(single)
print(f"  Path number of a single active cell in 2D: {pn_single} = {factorize(pn_single)}")
print(f"  2^9 - 1 = {2**9 - 1} = {factorize(2**9 - 1)}")
print(f"  The system boundary is the structural root — analogous to 7 in 1D.")