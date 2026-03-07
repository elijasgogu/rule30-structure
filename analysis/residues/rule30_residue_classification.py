"""
rule30_residue_classification.py

Analyzes Rule 30 path numbers over a configurable number of generations.

For each generation:
1. Compute the path number.
2. Remove all factors from {2, 3, 5, 7}.
3. Classify the remaining residue as:
   - resolved_to_1
   - prime
   - prime_power
   - mixed_composite

The script does not stop at the first counterexample.
It prints the full per-generation output and a complete summary at the end.
"""

RULE30 = {
    (1, 1, 1): 0, (1, 1, 0): 0, (1, 0, 1): 0, (1, 0, 0): 1,
    (0, 1, 1): 1, (0, 1, 0): 1, (0, 0, 1): 1, (0, 0, 0): 0,
}

GENS = 1024
SYSTEM_PRIMES = [2, 3, 5, 7]


def next_gen(cells):
    padded = [0, 0] + cells + [0, 0]
    return [RULE30[(padded[i], padded[i + 1], padded[i + 2])] for i in range(len(padded) - 2)]


def path_number(cells):
    total = 0
    for i in range(len(cells) - 2):
        l, m, r = cells[i], cells[i + 1], cells[i + 2]
        total += l * 4 + m * 2 + r
    return total


def strip_system_primes(n):
    remainder = n
    removed = {}

    for p in SYSTEM_PRIMES:
        count = 0
        while remainder % p == 0 and remainder > 0:
            remainder //= p
            count += 1
        if count > 0:
            removed[p] = count

    return remainder, removed


def factorize(n):
    if n <= 1:
        return []

    factors = []

    while n % 2 == 0:
        factors.append(2)
        n //= 2

    d = 3
    while d * d <= n:
        while n % d == 0:
            factors.append(d)
            n //= d
        d += 2

    if n > 1:
        factors.append(n)

    return factors


def is_prime(n):
    if n < 2:
        return False
    return len(factorize(n)) == 1


def classify_residue(n):
    if n == 1:
        return "resolved_to_1"

    factors = factorize(n)

    if len(factors) == 1:
        return "prime"

    unique_factors = set(factors)
    if len(unique_factors) == 1:
        return "prime_power"

    return "mixed_composite"


# --- Main ---

cells = [0, 0, 1, 0, 0]

results = []
counterexamples = []

category_counts = {
    "resolved_to_1": 0,
    "prime": 0,
    "prime_power": 0,
    "mixed_composite": 0,
}

for gen in range(GENS):
    pn = path_number(cells)
    remainder, removed = strip_system_primes(pn)
    classification = classify_residue(remainder)
    factors = factorize(remainder) if remainder > 1 else []

    category_counts[classification] += 1

    row = {
        "gen": gen,
        "path": pn,
        "remainder": remainder,
        "classification": classification,
        "removed": removed,
        "factors": factors,
    }
    results.append(row)

    print(
        f"Gen {gen:4d} | "
        f"path={pn:6d} | "
        f"remainder={remainder:6d} | "
        f"class={classification}"
    )

    if classification in {"prime_power", "mixed_composite"}:
        counterexamples.append(row)

    cells = next_gen(cells)

# --- Summary ---

print("\n" + "=" * 90)
print("SUMMARY")
print("=" * 90)
print(f"Generations analysed:  {GENS}")
print(f"Resolved to 1:         {category_counts['resolved_to_1']}")
print(f"Prime residues:        {category_counts['prime']}")
print(f"Prime powers:          {category_counts['prime_power']}")
print(f"Mixed composites:      {category_counts['mixed_composite']}")

print("\n" + "=" * 90)
print("COUNTEREXAMPLES")
print("=" * 90)

if not counterexamples:
    print("No counterexamples found.")
else:
    for c in counterexamples:
        print(
            f"Gen {c['gen']:4d} | "
            f"path={c['path']:6d} | "
            f"remainder={c['remainder']:6d} | "
            f"class={c['classification']:15s} | "
            f"factors={c['factors']} | "
            f"removed={c['removed']}"
        )

print("\n" + "=" * 90)
print("CATEGORY DETAILS")
print("=" * 90)

prime_power_rows = [r for r in results if r["classification"] == "prime_power"]
mixed_rows = [r for r in results if r["classification"] == "mixed_composite"]

print("\nPrime powers:")
if not prime_power_rows:
    print("  none")
else:
    for r in prime_power_rows:
        print(
            f"  Gen {r['gen']:4d} | remainder={r['remainder']:6d} | factors={r['factors']}"
        )

print("\nMixed composites:")
if not mixed_rows:
    print("  none")
else:
    for r in mixed_rows:
        print(
            f"  Gen {r['gen']:4d} | remainder={r['remainder']:6d} | factors={r['factors']}"
        )