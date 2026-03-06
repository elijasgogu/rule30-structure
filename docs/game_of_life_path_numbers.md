# Game of Life: Path Number Analysis

A first application of the path number method to two-dimensional cellular
automata, following directly from the structural observations documented in
the main project.

**Scripts:** `analysis/2d/gol_path_numbers.py` · `analysis/2d/gol_rpentomino_primes.py`  
**Automaton:** Game of Life B3/S23 (Conway)  
**Status:** Initial empirical observation — 1300 generations (R-pentomino),
30 generations (Blinker, Glider). To be extended to other patterns.

---

## Method

In the one-dimensional analysis, the path number of a generation is the sum of
all triplet decimal values (0–7). The system boundary is 2³ − 1 = **7** — the
maximum triplet value and a prime.

In two dimensions, Conway's Game of Life uses the Moore neighbourhood: 8
surrounding cells plus the cell itself — 9 bits. The decimal value of a 9-bit
neighbourhood lies between 0 and 511. The path number of a 2D generation is
therefore the sum of all 9-bit neighbourhood decimal values across the entire
grid.

```
1D: neighbourhood = 3 bits  ·  system boundary = 2³ − 1 = 7   (prime)
2D: neighbourhood = 9 bits  ·  system boundary = 2⁹ − 1 = 511 (composite: 7 × 73)
```

The structural difference is immediate: the 1D system boundary 7 is prime. The
2D system boundary 511 is composite — **7 × 73**. This has direct consequences
for the invariant structure of the path numbers.

---

## Start Conditions

Three start conditions were chosen to cover qualitatively different behaviours:

| Pattern       | Active cells | Behaviour         |
|---------------|:------------:|-------------------|
| Blinker       | 3            | period-2 oscillator — never changes cell count |
| Glider        | 5            | moves diagonally — never changes cell count |
| R-pentomino   | 5            | chaotic growth — cell count changes every generation |

All three start from a 50×50 zero grid with the pattern placed at the center.

---

## Results

### Blinker and Glider: constant path numbers

Both the Blinker and the Glider produce a **constant path number across all 30
generations**:

```
Blinker  (3 cells):  path number = 1533  =  511 × 3   →  3 × 7 × 73   (every generation)
Glider   (5 cells):  path number = 2555  =  511 × 5   →  5 × 7 × 73   (every generation)
```

This is structurally expected: both patterns have constant active cell counts
and fixed neighbourhood configurations. The path number cannot change if the
active neighbourhood structure is preserved up to translation — and the Glider
preserves it exactly as it moves.

### R-pentomino: dynamic path numbers

The R-pentomino grows and produces varying path numbers. Every path number
is divisible by 511 = 7 × 73. The additional prime factors beyond 7 and 73
vary by generation and reflect the evolving collision structure:

```
Gen  0:   2555  =  511 ×  5   →  5 × 7 × 73
Gen  1:   3066  =  511 ×  6   →  2 × 3 × 7 × 73
Gen  7:   5621  =  511 × 11   →  7 × 11 × 73
Gen 12:   6643  =  511 × 13   →  7 × 13 × 73
Gen 14:   9709  =  511 × 19   →  7 × 19 × 73
Gen 16:  11753  =  511 × 23   →  7 × 23 × 73
Gen 22:  18907  =  511 × 37   →  7 × 37 × 73
Gen 28:  15841  =  511 × 31   →  7 × 31 × 73
Gen 29:  14819  =  511 × 29   →  7 × 29 × 73
```

The multiplier (511 × k) varies with the active cell count and collision
geometry of each generation. The primes appearing as multipliers — 5, 11,
13, 19, 23, 29, 31, 37 — all lie within the system boundary 511 and are
direct products of the spatial structure of the pattern at that generation.

---

## Structural Observations

### Observation 1: 511 is the structural root

A single active cell in a 2D zero grid always produces path number **511 = 7 × 73**.
This is the 2D analogue of the 1D root value 7.

The reason is geometric: a single active cell at position (r,c) contributes
to exactly 9 overlapping Moore neighbourhoods. The sum of all 9 neighbourhood
decimal values for a single isolated 1 is always 511 — a consequence of the
binary positional structure of the 9-bit neighbourhood encoding, independent
of where in the grid the cell is placed.

```
Single active cell path number:  511 = 7 × 73 = 2⁹ − 1
```

This is structurally equivalent to the 1D case:

```
1D single active cell:  triplets 001 + 010 + 100 = 1 + 2 + 4 = 7 = 2³ − 1
2D single active cell:  9 neighbourhood values summing to 511 = 2⁹ − 1
```

### Observation 2: Every path number is divisible by 511

**Every path number across all three patterns and all 30 generations is
divisible by 511 = 7 × 73 without exception.** This is the direct 2D
analogue of the 1D result: every path number is divisible by the structural
root. In 1D the root is 7 (prime). In 2D the root is 511 = 7 × 73
(composite) — but the divisibility is equally complete.

Since 511 = 7 × 73, divisibility by 511 implies divisibility by both 7 and
73. Both appear as factors in every path number. The full prime decomposition
(e.g. `2 × 3 × 7 × 73`) always contains both, confirming full divisibility
by 511.

### Observation 3: All observed prime factors lie within the system boundary

In 1D, prime factors beyond the system boundary 7 appear from generation 10
onward and accumulate rapidly (139 distinct primes within 1024 generations).

In 2D, no prime factors beyond the system boundary 511 were observed in 500
generations of systematic R-pentomino analysis (`analysis/2d/gol_rpentomino_primes.py`,
grid 300×300). The R-pentomino produces primes 11, 13, 19, 23, 29, 31, 37 as
multipliers of 511 — all well within the system boundary. Whether primes
beyond 511 eventually appear in 2D requires significantly longer runs and
larger grids. This is an open empirical question.

The multiplier k itself is structurally informative: when k is prime, the
generation has a minimal factorization — 511 and one additional prime, nothing
further. When k is composite, the generation carries more arithmetic structure.
Since k varies directly with the collision geometry of the pattern, the prime
factorization of k may serve as an arithmetic signature of the observed
complexity: two generations that appear visually distinct could share the same
k and be arithmetically equivalent; two that look similar could differ. This
suggests that what appears as chaos in 2D cellular automata may be
categorizable by the structure of the primes it produces — a classification
orthogonal to visual appearance and directly readable from the path number.

### Observation 4: The factorization of the system boundary determines the invariant structure

```
1D:  2³ − 1 = 7        (prime)          → root = 7,   every path number ÷ 7
2D:  2⁹ − 1 = 511 = 7 × 73 (composite) → root = 511, every path number ÷ 511
```

The divisibility is complete in both cases. The difference is that the 2D
root is composite — so the invariant decomposes into two prime factors (7 and 73) 
rather than one. This suggests a general principle: for any n-bit
cellular automaton, 2ⁿ − 1 is the structural root and every path number is
divisible by it. Whether the root is prime or composite determines whether
the invariant is a single factor or a product of factors.

### Observation 5: Stable patterns have a fixed arithmetic endpoint

Extended analysis of the R-pentomino over 1300 generations (grid 700×700,
`analysis/2d/gol_rpentomino_primes.py`) shows that from generation 1103
onward the output is constant:

```
Gen 1103 onward:  59276  =  511 × 116  →  k = 2² × 29   (every generation)
Active cells: 116
```

The R-pentomino has fully stabilized into a configuration of 116 active cells
whose neighbourhood structure no longer changes. Its entire lifespan — from
chaotic growth at generation 0 to complete stabilization at generation 1103
— is arithmetically described by a sequence of k-values that converges to a
fixed point: **k = 116 = 2² × 29**.

This means every pattern in Game of Life that reaches a stable or periodic
end state has a characteristic arithmetic endpoint: a fixed k-value (for
Still Lifes), a periodic k-sequence (for oscillators), or a translating
k-value (for Gliders, where k is constant across all positions). The
chaotic phase between start and stabilization is the arithmetic transition
from the initial k to the terminal k. Two patterns that stabilize to the
same k-value are arithmetically equivalent regardless of their visual
appearance or the path they took to get there.

This suggests a classification of 2D automaton patterns by their terminal
k-value — a structural fingerprint readable directly from the path number
without visual inspection.

### Observation 6: The 2D rule space and its reductions

A complete scan of all outer totalistic 2D rules
(`analysis/2d/gol_rule_space.py`) allows a precise comparison with the 1D
case — but requires a careful distinction between different types of reduction.

**In 1D the reduction is absolute:**

```
2^8  =   256   all elementary 1D rules
      →    32   structurally valid  (factor 8×, no further distinctions)
```

The 32 rules are the complete set of structurally valid 1D automata. The
reduction from 256 to 32 follows from a single geometric necessity: every
rule requires two boundary zeros on each side for the recursion to terminate
correctly. No additional assumptions are needed.

**In 2D the reduction is hierarchical:**

```
2^512        all possible 9-bit 2D rules (no constraints)
             each of the 512 neighbourhood states mapped independently

2^18         outer totalistic rules
             next state depends only on neighbour sum (0–8), not position
             this is a symmetry assumption: left ≠ right is ignored
             Game of Life is outer totalistic — but not all 2D automata are

2^16 = 65,536  outer totalistic + structural constraint:
               0 ∉ birth_set — dead cells with 0 neighbours stay dead
               (no spontaneous generation from empty space)
```

The step from 2^512 to 2^18 is a well-known consequence of the outer
totalistic symmetry assumption and is not a finding of this analysis.

**Classification of the 65,536 candidate rules by single-cell behaviour:**

```
dies        32,768  (50.0%)   — pattern reaches 0 active cells        = 2^15
growing     17,144  (26.2%)   — unbounded growth from single cell      }
exploding   14,571  (22.2%)   — rapid expansion beyond grid threshold  } = 31,715
stable         486  ( 0.7%)   — fixed point                            }
period-2       226  ( 0.3%)   — oscillating with period 2              } = 883
period-4       168  ( 0.3%)   — oscillating with period 4              }
period-3         3  ( 0.0%)   — oscillating with period 3              }
```

Three arithmetically distinct groups emerge:

**2^15 = 32,768 rules** kill a single cell — not an empirical count but an
arithmetic necessity. The survival bit for neighbour sum 0 is independent of
all other bits: rules where 0 ∉ survival_set always kill an isolated cell
regardless of all other parameters. Exactly half of the 65,536 candidate
rules have this property.

**31,715 rules** produce unbounded growth (growing + exploding) — the single
cell either expands without limit or collapses after explosive growth. These
rules do not respect the zero-space boundary condition: an isolated active
pattern generates unbounded activity into the surrounding zero space.

**883 rules** are non-trivially bounded — the single cell neither dies nor
expands unboundedly but reaches a stable or periodic state. These are the
structural analogue of the 32 valid rules in 1D: patterns that can exist in
a defined zero space without destroying it.

```
65,536  =  2^15  +  31,715  +  883
            dies    unbounded   non-trivially bounded
```

The comparison to 1D therefore holds at the level of the non-trivially
bounded rules:

```
1D:  32 rules     structurally valid (single reduction, factor 8×)
2D:  883 rules    non-trivially bounded outer totalistic rules
```

The factor between 65,536 and 883 is approximately 74× — larger than the
1D factor of 8×, reflecting the additional complexity of the 2D zero-space
boundary condition acting in eight directions simultaneously.

Game of Life B3/S23 falls into the "dies" category for a single-cell start
— structurally correct, since a single cell with 0 neighbours cannot satisfy
the birth condition B3. It is not among the 883 non-trivially bounded rules
by this criterion alone, but produces non-trivial behaviour with multi-cell
start conditions. Whether it occupies a distinguished position among the 883
non-trivially bounded rules — analogous to Rule 60 among the 32
one-dimensional rules — requires investigating its path number structure
across the full set of 883 candidates.

**What 883 is — and what it is not.**
883 is a precise answer to a precise question: how many outer totalistic 2D
rules are non-trivially bounded under a single-cell start condition? The scan
is complete — all 65,536 candidates were tested, no sampling. The answer is
not an estimate.

What remains open is whether this is the right question for determining the
total number of structurally valid 2D rules. The outer totalistic assumption
— that the position of neighbours does not matter, only their count — is a
design choice that Game of Life makes but that is not a structural necessity
for all 2D automata. A rule that distinguishes left from right neighbours
would inhabit a different and far larger rule space. The single-cell start
condition is likewise a choice: with other minimal start conditions the
bounded set could differ.

883 is therefore the 2D analogue of the 32 one-dimensional rules — but the
analogy is partial. In 1D, the reduction from 256 to 32 requires no
additional assumptions beyond the geometric boundary condition. In 2D, the
reduction to 883 requires the outer totalistic symmetry assumption first. The
indications that 883 is the structurally meaningful number are strong — the
complete scan, the arithmetic cleanliness of the three-group decomposition,
and the proximity of the reduction factor to the prime factor of the system
boundary — but the question of how many 2D rules truly exist remains open.

---

## Open Questions

**Does 511 divisibility hold for all Game of Life patterns and all generation
counts?** The observations across three patterns and up to 1300 generations
are consistent, but a systematic test across a wider range of start conditions
would establish this more firmly.

**Do prime factors beyond 511 eventually appear?** In 1D, primes beyond the
system boundary 7 appear reliably from generation 10 onward. In 2D, no such
primes were observed in 500 generations of R-pentomino analysis. Whether this
reflects a structural difference between 1D and 2D automata, or simply
requires longer runs, is an open question.

**Can the terminal k-value of a pattern be predicted without full simulation?**
If the stable k-value is structurally determined by the pattern's geometry,
it may be computable directly — bypassing the chaotic transition phase
entirely. This would have direct implications for any application that
requires predicting the end state of a complex 2D pattern.

**Is Game of Life structurally distinguished within the 883 non-trivially
bounded rules?** The rule space scan confirms that Game of Life belongs to
the "dies" category for single-cell starts — not among the 883 directly, but
producing non-trivial behaviour with multi-cell patterns. Whether it occupies
a position as arithmetically unique as Rule 60 among the 32 one-dimensional
rules requires investigating its path number structure across the full set of
883 candidates.

**Is the reduction factor 74 related to the prime factor 73?** The most
structurally suggestive observation in this analysis: the reduction factor
from 65,536 to 883 non-trivially bounded rules is approximately 74 — and 73
is the non-trivial prime factor of the system boundary 511 = 7 × 73. In 1D,
the reduction factor is exactly 8 = 2³, equal to the number of possible
neighbourhood states. In 2D, the analogous count is 2⁹ = 512 = 7 × 73 + 1.
The proximity of 74 to 73 + 1 is arithmetically precise enough to suggest a
structural relationship between the factorization of the system boundary
2ⁿ − 1 and the reduction factor of the rule space. Whether this is a general
principle — that the reduction factor is determined by the prime factors of
2ⁿ − 1 — is an open hypothesis that would require verification across
automata of different neighbourhood sizes.

---

## Relation to the Main Project

This analysis applies the path number method introduced for Rule 30 directly
to a 2D automaton. The core method transfers without modification: measure
neighbourhood decimal values, sum them, factorize. The structural findings — invariant root, complete divisibility by 2ⁿ − 1,
prime factors within and potentially beyond the system boundary — follow the
same pattern as in 1D, with the composite nature of 2⁹ − 1 introducing a
two-factor invariant structure instead of a single prime.

The full 1D analysis and the path number method are documented in the main
`README.md` and in `docs/interior_classes.md`.

---

## Scripts

| Script                                  | Description                                                                                      |
|-----------------------------------------|--------------------------------------------------------------------------------------------------|
| `analysis/2d/gol_path_numbers.py`       | path number analysis for three start conditions (Blinker, Glider, R-pentomino), 30 generations; establishes 511 as structural root and confirms full divisibility |
| `analysis/2d/gol_rpentomino_primes.py`  | systematic prime factor analysis of R-pentomino over configurable generation window; tracks primes within and beyond system boundary 511; documents stabilization at gen 1103 |
| `analysis/2d/gol_rule_space.py`         | complete scan of all 2^16 structurally valid outer totalistic 2D rules; classifies single-cell behaviour; establishes reduction factor ≈ 8× analogous to 1D |

```bash
python3 analysis/2d/gol_path_numbers.py
python3 analysis/2d/gol_rpentomino_primes.py
python3 analysis/2d/gol_rule_space.py
```

`gol_path_numbers.py` requires `numpy`. `gol_rpentomino_primes.py` requires
`numpy` and `sympy`. `gol_rule_space.py` requires `numpy`. See `requirements.txt`.