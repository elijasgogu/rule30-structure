## Interior Combinative Classes

### A Structured Language Within the Chaos

The interior of Rule 30 — the region between the invariant left boundary
`1, 3, 6` and the invariant right boundary `4` — appears at first inspection
to be entirely chaotic. No individual triplet value at any interior position
repeats consistently across generations, and no closed-form expression for the
interior sequence is known.

However, a finer analysis reveals that the interior is not uniformly chaotic.
Each generation's interior, once decoded into letters using a fixed alphabet,
decomposes into five structurally distinct segments:

```
  A  |  Core  |  L1  L2  L3  …  Ln  |       Chaos       |  R  |  C
fixed  stable   ←─ two alternating sets grow by concatenation ─→  alt  fixed
```

- **A**: the invariant left boundary symbol, always present (triplets `1, 3, 6`)
- **Core**: a fixed symbol sequence that builds up deterministically over the
  first repetitions and then stabilizes permanently
- **L1 – Ln**: a series of layer contributions that concatenate into two growing
  symbol sets which alternate pairwise as a unit; each new layer extends both
  sets and doubles the period of the overall alternation
- **Chaos**: a region of no identifiable structure, sandwiched between the last
  confirmed layer and the right segment; it grows without bound
- **R**: a right alternating segment immediately before the right boundary,
  permanently coupled to the parity of the two alternating sets; its structure
  varies by class
- **C**: the invariant right boundary symbol, always present (triplet `4`)

The boundary between the structured region and the chaos region is not fixed —
it advances outward as new layers stabilize — but once a position has been
claimed by a layer it is never relinquished.

---

### The Alphabet

To describe the interior precisely, the triplet sequence of each generation is
decoded into a letter sequence using a fixed alphabet. Each letter corresponds
to a specific sequence of consecutive triplet values:

```
A = 136          B = 412          C = 4
D = 53776        E = 5376         F = 41377776
G = 41376        H = 536          I = 4136
J = 52           K = 537776       L = 413777776
M = 413776       N = 5377776      O = 4137776
P = 5377777776   Q = 413777777776 R = 537777777776
S = 4137777776   T = 537777776    U = 53777776
V = 53777777776  W = 5377777777776 X = 5377777777777776
Y = 53777777777776               Z = 413777777777777776
```

Matching is greedy, longest-first. Analysis of the first 200 generations
confirms that this 26-symbol alphabet fully covers the interior — no unmatched
subsequences remain. The script `analysis/interior/rule30_alphabet.py` performs this
decoding for any number of generations.

The alphabet is not fixed in advance — it reflects the symbol sequences
observed up to the generations analyzed. As more generations are computed, it
is very likely that additional symbols will need to be added: longer triplet
sequences that do not yet appear within 200 generations may emerge further out,
requiring new entries. The alphabet should therefore be understood as a
current snapshot rather than a closed system.

---

### Overview: Four Combinative Classes

The decoded interior reveals four distinct combinative classes, each occupying
every fourth generation with a fixed offset:

| Class | Generations       | Core       | Symbol set                           |
|-------|-------------------|------------|--------------------------------------|
| A     | 2, 6, 10, 14, …   | BBEBHJJI   | {B, E, H, I, J}                      |
| B     | 3, 7, 11, 15, …   | DIJGJBD    | {B, E, H, I, J, K, N, O} and more   |
| C     | 4, 8, 12, 16, …   | BGMMJ      | {B, F, G, J, M}                      |
| D     | 5, 9, 13, 17, …   | DHGBHI     | {B, D, G, H, I}                      |

Together they partition every generation from generation 2 onward without
overlap or gap. The symbol set of Class B is marked as open because its R
segment introduces symbols that require increasingly many repetitions to observe
— the full set cannot be determined from a finite analysis window.

---

### Build-up Phase

Each class begins with a build-up phase in which the core grows by one or two
symbols roughly every two repetitions. Each symbol added is permanent — no
position is ever removed. The build-up has been empirically verified across the
first repetitions of each class:

```
Class A (gen 2, 6, 10, …):     Class B (gen 3, 7, 11, …):
  rep 1 (gen  2):  B              rep 1 (gen  3):  D
  rep 2 (gen  6):  BB             rep 2 (gen  7):  D
  rep 3 (gen 10):  BB             rep 3 (gen 11):  DIJ
  rep 4 (gen 14):  BBEB           rep 4 (gen 15):  DIJ
  rep 5 (gen 18):  BBEB           rep 5 (gen 19):  DIJ
  rep 6 (gen 22):  BBEB           rep 6 (gen 23):  DIJGJB
  rep 7 (gen 26):  BBEBHJ         rep 7 (gen 27):  DIJGJB
  rep 8 (gen 30):  BBEBHJJ        rep 8 (gen 31):  DIJGJB
  rep 9 (gen 34):  BBEBHJJI       rep 9 (gen 35):  DIJGJBD  ← core complete

Class C (gen 4, 8, 12, …):     Class D (gen 5, 9, 13, …):
  rep 1 (gen  4):  B              rep 1 (gen  5):  D
  rep 2 (gen  8):  BG             rep 2 (gen  9):  DH
  rep 3 (gen 12):  BG             rep 3 (gen 13):  DHG
  rep 4 (gen 16):  BGM            rep 4 (gen 17):  DHG
  rep 5 (gen 20):  BGM            rep 5 (gen 21):  DHGB
  rep 6 (gen 24):  BGM            rep 6 (gen 25):  DHGBH
  rep 7 (gen 28):  BGMM           rep 7 (gen 29):  DHGBH
  rep 8 (gen 32):  BGMMJ          rep 8 (gen 33):  DHGBHI
```

---

### Stable Phase and the Two Alternating Sets

After the build-up the core stabilizes, and a qualitatively different structure
emerges: the class region grows by accumulating layer contributions that
concatenate into **two symbol sets which alternate pairwise as a unit**. On
every repetition exactly one of the two sets appears in full, immediately after
the core. Each new layer contributes one token to each set by concatenation,
doubling the period of the full alternation with every addition. The period of
the complete set is always determined by the outermost layer.

This structure — and the open-ended growth it implies — is shared by all four
classes. The class-specific details are documented in the individual sections
below.

---

### Class A

**Generations:** 2, 6, 10, 14, … (every 4th generation starting from gen 2)
**Core:** `BBEBHJJI` — fully stable from gen 34 (rep 9), does not alternate
**Symbol set:** {B, E, H, I, J}

#### Layer Structure

Each layer stabilizes and contributes its token pair to the two alternating
sets. The even and odd tokens are concatenated to the respective sets:

```
  Core:  BBEBHJJI        stable from gen 34   (rep 0)
  L1:    B   | E         stable from gen 34   (rep 0)   → period 2
  L2:    JI  | B         stable from gen 42   (rep 2)   → period 4
  L3:    EJI | IE        stable from gen 66   (rep 8)   → period 8
  L4:    BHB | IJB       stable from gen 78   (rep 11)  → period 16
  L5:    IHIIJ | BJHJHB  stable from gen 102  (rep 17)  → period 32
```

Layer stabilization follows an irregular rhythm (rep 0, 2, 8, 11, 17, …).
Further layers are expected as more generations are computed.

#### Growth of the Two Alternating Sets

```
  After Core alone:   even= (nothing)        | odd= (nothing)
  After L1 (gen 34):  even= B                | odd= E
  After L2 (gen 42):  even= BJI              | odd= EB
  After L3 (gen 66):  even= BJIEJI           | odd= EBIE
  After L4 (gen 78):  even= BJIEJIBHB        | odd= EBIEIJB
  After L5 (gen 102): even= BJIEJIBHBIHIIJ   | odd= EBIEIJBBJHJHB
```

#### Full Interior Notation (from gen 102)

```
  even rep:  A  BBEBHJJI  BJIEJIBHBIHIIJ  [Chaos]  B   C
  odd rep:   A  BBEBHJJI  EBIEIJBBJHJHB   [Chaos]  BB  C
```

#### R Coupling

R is permanently coupled to the parity of the two alternating sets via a simple
two-symbol alternation:

```
  even set active → R = B
  odd set  active → R = BB
```

The coupling is fixed from gen 10 onward and does not change as further layers
are added. R acts as an immediate parity signature for the active set.

---

### Class B

**Generations:** 3, 7, 11, 15, … (every 4th generation starting from gen 3)
**Core:** `DIJGJBD` — fully stable from gen 39 (rep 9), does not alternate
**Symbol set:** {B, E, H, I, J, K, N, O} and more (open — see R coupling below)

#### Layer Structure

```
  Core:  DIJGJBD          stable from gen 39   (rep 0)
  L1:    EH  | BB         stable from gen 43   (rep 1)   → period 2
  L2:    I   | K          stable from gen 51   (rep 3)   → period 4
  L3:    B   | B          stable from gen 59   (rep 5)   → period 8
  L4:    I   | G          stable from gen 67   (rep 7)   → period 16
  L5:    H   | I          stable from gen 75   (rep 9)   → period 32
  L6:    EJ  | O          stable from gen 83   (rep 11)  → period 64
  L7:    N   | JJ         stable from gen 91   (rep 13)  → period 128
  L8:    BE  | BJ         stable from gen 99   (rep 15)  → period 256
  L9:    E   | DI         stable from gen 107  (rep 17)  → period 512
  L10:   MJJ | GJ         stable from gen 123  (rep 21)  → period 1024
```

Each layer stabilizes exactly 2 repetitions after the previous one, always at
an odd repetition index. This produces a strictly regular build-up rhythm,
unlike Class A. Further layers are expected as more generations are computed.

Note: L1 seeds the two sets with `EH` and `BB` — the `E` belongs to L1, not
to the core. The core does not contribute to set alternation.

#### Growth of the Two Alternating Sets

```
  After L1  (gen 43):  even= EH                | odd= BB
  After L2  (gen 51):  even= EHI               | odd= BBK
  After L3  (gen 59):  even= EHIB              | odd= BBKB
  After L4  (gen 67):  even= EHIBI             | odd= BBKBG
  After L5  (gen 75):  even= EHIBIH            | odd= BBKBGI
  After L6  (gen 83):  even= EHIBIHEJ          | odd= BBKBGIO
  After L7  (gen 91):  even= EHIBIHEJN         | odd= BBKBGIOJJ
  After L8  (gen 99):  even= EHIBIHEJNBE       | odd= BBKBGIOJJBJ
  After L9  (gen 107): even= EHIBIHEJNBEE      | odd= BBKBGIOJJBJDI
  After L10 (gen 123): even= EHIBIHEJNBEEMJJ   | odd= BBKBGIOJJBJDIGJ
```

#### Full Interior Notation (from gen 123)

```
  even rep:  A  DIJGJBD  EHIBIHEJNBEEMJJ  [Chaos]  D   C
  odd rep:   A  DIJGJBD  BBKBGIOJJBJDIGJ  [Chaos]  D   C
```

(R = D on all even repetitions; odd repetitions follow the pattern below.)

#### R Coupling

R in Class B follows a hierarchical period-doubling pattern that is itself
open-ended. Rather than a simple two-symbol alternation, R is determined by
the binary structure of the repetition index:

```
  even rep (>0):   R = D
  odd rep:         determined by trailing-ones count of the odd rank index:
    trailing ones = 0, rank % 4 == 0  →  R = F   (period 4)
    trailing ones = 0, rank % 4 == 2  →  R = N   (period 4)
    trailing ones = 1                 →  R = L   (period 8)
    trailing ones = 2                 →  R = P   (period 16)
    trailing ones = 3                 →  R = X   (period 64)
    trailing ones = 4                 →  R = Z   (period 128)
    trailing ones = 5, 6, …          →  not yet observed
```

The symbols at positions requiring 5 or more trailing ones appear only at
repetitions 63, 127, 255, … — intervals that lie far beyond the current
analysis window. Those alphabet symbols have not yet been defined because the
triplet sequences they represent have not yet been observed. R in Class B is
therefore open in the same sense as the alphabet itself: the structural pattern
is understood, but the symbols it will eventually require lie beyond the current
observation window and will necessitate further alphabet extensions as more
generations are computed.

---

### Class C

**Generations:** 4, 8, 12, 16, … (every 4th generation starting from gen 4)
**Core:** `BGMMJ` — fully stable from gen 32 (rep 8), does not alternate
**Symbol set:** {B, E, F, G, H, I, J, M, O}

#### Layer Structure

```
  Core:  BGMMJ          stable from gen 32   (rep 8)
  L1:    F   | BB        stable from gen 36   (rep 0)   → period 2
  L2:    J   | E         stable from gen 48   (rep 3)   → period 4
  L3:    F   | DH        stable from gen 64   (rep 7)   → period 8
  L4:    GJI | BB        stable from gen 76   (rep 10)  → period 16
  L5:    B   | B         stable from gen 80   (rep 11)  → period 32
  L6:    DJJ | JGJB      stable from gen 100  (rep 16)  → period 64
  L7:    G   | G         stable from gen 108  (rep 18)  → period 128
  L8:    JI  | B         stable from gen 120  (rep 21)  → period 256
  L9:    BJ  | JJ        stable from gen 128  (rep 23)  → period 512
  L10:   B   | B         stable from gen 132  (rep 24)  → period 1024
  L11:   BH  | OH        stable from gen 144  (rep 27)  → period 2048
```

Layer stabilization follows an irregular rhythm — unlike Class B, the gaps
between layers are not uniform. Notably, L5 stabilizes only one step after L4
(rep 11 vs. rep 10), while earlier gaps are larger. Further layers are expected
as more generations are computed.

#### Growth of the Two Alternating Sets

The two sets are named after their initial tokens: the **F-set** and the
**BB-set**. On odd rep_idx the F-set is active; on even rep_idx the BB-set is
active.

```
  After L1  (gen 36):  F-set= F                    | BB-set= BB
  After L2  (gen 48):  F-set= FJ                   | BB-set= BBE
  After L3  (gen 64):  F-set= FJF                  | BB-set= BBEDH
  After L4  (gen 76):  F-set= FJFGJI               | BB-set= BBEDHBB
  After L5  (gen 80):  F-set= FJFGJIB              | BB-set= BBEDHBBB
  After L6  (gen 100): F-set= FJFGJIBDJJ           | BB-set= BBEDHBBBJGJB
  After L7  (gen 108): F-set= FJFGJIBDJJG          | BB-set= BBEDHBBBJGJBG
  After L8  (gen 120): F-set= FJFGJIBDJJGJI        | BB-set= BBEDHBBBJGJBGB
  After L9  (gen 128): F-set= FJFGJIBDJJGJIBJ      | BB-set= BBEDHBBBJGJBGBJJ
  After L10 (gen 132): F-set= FJFGJIBDJJGJIBJB     | BB-set= BBEDHBBBJGJBGBJJB
  After L11 (gen 144): F-set= FJFGJIBDJJGJIBJBBH   | BB-set= BBEDHBBBJGJBGBJJBOH
```

#### Full Interior Notation (from gen 144)

```
  odd rep:   A  BGMMJ  FJFGJIBDJJGJIBJBBH   [Chaos]  B  C
  even rep:  A  BGMMJ  BBEDHBBBJGJBGBJJBOH  [Chaos]  B  C
```

#### R Coupling

R in Class C is **always B**, on every repetition without exception. There is
no parity variation, no period-doubling pattern, and no dependence on the
active set. R carries no structural information about which set is active — it
is a fixed constant, the simplest possible R behaviour observed across the four
classes.

---

### Class D

**Generations:** 5, 9, 13, 17, … (every 4th generation starting from gen 5)
**Core:** `DHGBHI` — fully stable from gen 33 (rep 8), does not alternate
**Symbol set:** {B, D, E, G, H, I, J, O, U}

#### Layer Structure

```
  Core:  DHGBHI          stable from gen 33   (rep 8)
  L1:    G    | H         stable from gen 37   (rep 0)   → period 2
  L2:    HJ   | II        stable from gen 53   (rep 4)   → period 4
  L3:    BB   | G         stable from gen 61   (rep 6)   → period 8
  L4:    UH   | IHJI      stable from gen 85   (rep 12)  → period 16
  L5:    H    | J         stable from gen 93   (rep 14)  → period 32
  L6:    II   | BH        stable from gen 101  (rep 16)  → period 64
  L7:    KB   | H         stable from gen 109  (rep 18)  → period 128
  L8:    I    | I         stable from gen 117  (rep 20)  → period 256
  L9:    J    | HJH       stable from gen 125  (rep 22)  → period 512
  L10:   HG   | HO        stable from gen 133  (rep 24)  → period 1024
  L11:   I    | J         stable from gen 141  (rep 26)  → period 2048
  L12:   B    | E         stable from gen 149  (rep 28)  → period 4096
```

Layer stabilization follows an irregular rhythm overall, but becomes strictly
regular from L4 onward: each layer stabilizes exactly 2 repetitions after the
previous one (rep 12, 14, 16, 18, 20, 22, 24, 26, 28, …). The early layers
L1–L3 have larger and uneven gaps (rep 0, 4, 6). Class D has the most
individual layer tokens of all four classes within the analyzed window, and
contains the longest single tokens observed: `IHJI` at L4 and `HJH` at L9.
Further layers are expected as more generations are computed.

#### Growth of the Two Alternating Sets

The two sets are named after their initial tokens: the **G-set** and the
**H-set**. On even rep_idx the G-set is active; on odd rep_idx the H-set is
active.

```
  After L1  (gen 37):  G-set= G                    | H-set= H
  After L2  (gen 53):  G-set= GHJ                  | H-set= HII
  After L3  (gen 61):  G-set= GHJBB                | H-set= HIIG
  After L4  (gen 85):  G-set= GHJBBUH              | H-set= HIIGIHJI
  After L5  (gen 93):  G-set= GHJBBUHH             | H-set= HIIGIHJIJ
  After L6  (gen 101): G-set= GHJBBUHHII           | H-set= HIIGIHJIJBH
  After L7  (gen 109): G-set= GHJBBUHHIIKB         | H-set= HIIGIHJIJBHH
  After L8  (gen 117): G-set= GHJBBUHHIIKBI        | H-set= HIIGIHJIJBHHI
  After L9  (gen 125): G-set= GHJBBUHHIIKBIJ       | H-set= HIIGIHJIJBHHIHJH
  After L10 (gen 133): G-set= GHJBBUHHIIKBIJHG     | H-set= HIIGIHJIJBHHIHJHHO
  After L11 (gen 141): G-set= GHJBBUHHIIKBIJHGI    | H-set= HIIGIHJIJBHHIHJHHOJ
  After L12 (gen 149): G-set= GHJBBUHHIIKBIJHGIB   | H-set= HIIGIHJIJBHHIHJHHOJE
```

#### Full Interior Notation (from gen 149)

```
  even rep:  A  DHGBHI  GHJBBUHHIIKBIJHGIB   [Chaos]  E  C
  odd rep:   A  DHGBHI  HIIGIHJIJBHHIHJHHOJE  [Chaos]  G  C
```

#### R Coupling

R in Class D strictly alternates between **E** and **G** on every repetition,
beginning at gen 5 (the very first generation of the class). The alternation is
tied to the absolute repetition index: E appears when `(gen − 5) / 4` is even,
G when it is odd. This continues unconditionally across all verified generations.

Crucially, this alternation is **independent of the layer set parity**: R does
not track which of the two sets is active. It follows its own fixed two-beat
rhythm regardless of how many layers have accumulated. This distinguishes Class D
from Class A, where R is coupled to set parity, and from Class B, where R
carries its own hierarchical period-doubling structure.

---

### Comparative Overview

With all four classes documented, it is now possible to compare them directly
and assess what their shared architecture — and their differences — reveal about
the interior of Rule 30.

#### Core

All four cores stabilize after exactly 8 repetitions of their respective class.
Their lengths differ:

| Class | Core     | Length |
|-------|----------|--------|
| A     | BBEBHJJI | 8      |
| B     | DIJGJBD  | 7      |
| C     | BGMMJ    | 5      |
| D     | DHGBHI   | 6      |

No class reuses another's core sequence, and no core symbol sequence is a
subsequence of another. The cores are structurally independent.

#### Layer Count and Stabilization Rhythm

Within the analyzed window (approximately 150–300 generations per class) the
number of confirmed layers and their stabilization rhythm vary considerably:

| Class | Layers confirmed | Stabilization rhythm                          |
|-------|------------------|-----------------------------------------------|
| A     | 5                | irregular (rep 0, 2, 8, 11, 17)               |
| B     | 10               | strictly +2 per layer, always at odd rep      |
| C     | 11               | irregular, with one anomalous +1 gap (L4→L5)  |
| D     | 12               | irregular early (L1–L3), then strictly +2     |

Class B stands out as the most regular: every layer arrives exactly 2
repetitions after the previous one, always at an odd repetition index. Class D
converges to the same +2 rhythm from L4 onward. Classes A and C remain
irregular throughout the analyzed window.

The larger layer counts of Classes B, C, and D relative to Class A reflect in
part the earlier stabilization of their cores and the shorter intervals between
layers — not necessarily a deeper structural complexity.

#### R Coupling: Four Distinct Behaviours

The right segment R shows the greatest variation across the four classes, and
is arguably the most structurally informative dimension of the comparison:

| Class | R behaviour                                              | Complexity         |
|-------|----------------------------------------------------------|--------------------|
| A     | alternates B / BB, coupled to set parity                 | simple, parity-bound |
| B     | hierarchical period-doubling sequence D/F/L/N/P/X/Z/…   | open, unbounded    |
| C     | constant B on every repetition                           | trivial            |
| D     | strictly alternates E / G, independent of set parity    | simple, fixed      |

Class C represents the minimum: R carries no information whatsoever. Class A
carries exactly one bit per repetition — parity of the active set. Class D also
carries one bit, but decoupled from set parity, following instead the absolute
repetition count. Class B is qualitatively different from all three: its R
segment is itself a hierarchical structure that grows without bound, requiring
new alphabet symbols at repetitions 63, 127, 255, … that lie beyond the current
observation window. In this sense Class B's R mirrors the layer structure
itself — both are open-ended period-doubling hierarchies running in parallel.

#### The R Values of Class B and Their Cross-Class Connections

The symbols that appear in Class B's R segment — F, L, P, X, Z — are not
arbitrary. They are specific alphabet symbols defined by triplet sequences of
increasing length, and they appear at repetition indices whose binary
representation contains a specific number of consecutive trailing ones (1, 2, 3,
4, … trailing ones respectively). This is structurally the same counting
mechanism that governs the layer period-doubling sequence itself.

The question of whether these R values stand in systematic relation to the R
values of the other three classes is open and worth investigating. All four
classes run in parallel — their generations interleave as 2, 3, 4, 5, 6, 7, 8,
9, … — and the R values of all four classes together form a joint sequence
across every generation. If that joint sequence contains regularities that are
not visible when each class is examined in isolation, it would suggest that the
four classes are not independent structures but aspects of a single coordinated
automaton-wide pattern.

The symmetric rep intervals at which Class B's rarer R symbols appear (4, 8,
16, 32, 64, …) are powers of two — the same sequence that governs layer period
doubling. Whether these intervals align in any meaningful way with the layer
stabilization points or the R alternation rhythms of Classes A, C, and D is an
open structural question.

#### Can the Chaos Region Be Further Constrained?

The chaos region currently begins immediately after the last confirmed layer and
extends to R. Its inner content has been treated as entirely unstructured.
However, two observations suggest it may repay further investigation.

First, the chaos regions of all four classes share the same 26-symbol alphabet,
and many of the same high-frequency symbols (B, I, J, H) appear prominently
in all of them. If the chaos region of each class contains recurring local
patterns — sub-sequences that appear with non-random frequency — those patterns
might be identifiable by cross-class comparison.

Second, the chaos region of Class B is flanked on its right by an R value that
is itself part of a deep hierarchical structure. It is conceivable that the
immediately adjacent positions in the chaos — those closest to R — exhibit
partial structure that becomes visible only when the R hierarchy is taken into
account. Investigating the chaos region of Class B at the boundary with R, in
parallel with the corresponding positions in the other three classes, may reveal
whether the chaos is uniform throughout or whether it has an internal gradient
of decreasing structure moving left to right.

#### Structural Assessment

The four combinative classes of Rule 30 share a single underlying architecture:
invariant boundaries, a stabilizing core, two alternating symbol sets that grow
by layer concatenation with period doubling, an unbounded chaos region, and a
right segment R. This architecture emerges without parameterization from the
rule and the single-cell initial condition.

Within that shared architecture, the four classes realize four qualitatively
different behaviours — most strikingly in R, which ranges from a fixed constant
(Class C) through a parity signature (Class A) and an independent alternation
(Class D) to an open hierarchical sequence (Class B). The existence of this
range within a single automaton suggests that Rule 30's interior is not simply
chaotic but is organized at multiple levels simultaneously: the layer structure
represents one level of organization, R represents another, and the relationship
between R across classes may represent a third level that has not yet been fully
described.

The most structurally productive direction for continued analysis is likely
Class B, precisely because its R segment and its layer structure are both
open-ended hierarchies of the same type. Understanding whether they interact —
whether the R values constrain or predict anything about the chaos region, or
whether the joint R sequence across all four classes contains regularities
invisible within any single class — would substantially deepen the structural
picture of Rule 30's interior.

---

### Stability Criterion

A position is assigned to a layer if and only if the symbol at that position is
strictly alternating between exactly two values across at least three
consecutive repetitions of its period. Any position that does not satisfy this
criterion — including positions where class-alphabet symbols appear beyond the
confirmed stable prefix — is assigned to the chaos region.

This criterion is deliberately conservative: it never claims more order than
the data directly supports.

---

### The Chaos Region

The chaos region occupies the interior between the last confirmed layer and the
right segment R. It grows without bound: new symbols accumulate on its right
side faster than new layers can claim them on its left. The symbols it contains
are drawn from the same 26-symbol alphabet as the class region, but no position
within it has ever been observed to satisfy the stability criterion.

Because the chaos region grows unboundedly while all structured segments remain
at fixed positions to its left and right, it has been placed at the far right of
the analysis table so that all structured columns remain aligned and readable
regardless of how large the chaos region becomes.

---

### Significance

This finding does not resolve the prize problems or reduce the complexity of
Rule 30. The chaos region remains genuinely unstructured and grows without
bound.

What it establishes is that the interior is not a uniform chaos. A precise
structure — fixed boundaries, a stable core, and two growing symbol sets that
alternate pairwise with a period that doubles each time a new layer stabilizes
— forms spontaneously from the rule and the initial condition `00100`, without
any external parameterization.

The period-doubling sequence 2, 4, 8, 16, 32, … is a mathematical invariant
of the automaton. The two alternating sets grow by concatenation as each layer
is added, and their parity is permanently reflected in the right segment R.
The R segment itself may carry additional hierarchical structure, as observed
in Class B, where R follows its own period-doubling pattern whose full extent
requires alphabet symbols not yet observed and not yet defined.

The layers documented here are those confirmed within the first 200–300
generations. As more generations are computed, additional layers are expected
to continue appearing: the structured region grows alongside the chaos region,
with each new layer claiming a fixed width from its left edge. The ratio of
structured to chaotic interior remains an open observation — as does the
question of whether a regular pattern governs the number of generations between
the stabilization of one layer and the next.

---

### Scripts

| Script                                              | Description                                                                                                                                          |
|-----------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------|
| `analysis/interior/rule30_interior.py`              | strips invariant boundaries and displays the raw interior triplet sequence for each generation; entry point for the interior investigation            |
| `analysis/interior/rule30_invariants.py`            | classifies every interior triplet value as boundary, isolated, or collision; makes the three-layer structure of the automaton explicit               |
| `analysis/interior/rule30_alphabet.py`              | decodes any generation into the 26-symbol alphabet; the alphabet reflects observed sequences up to the generations analyzed and will likely grow as further generations are computed |
| `analysis/interior/rule30_classes.py`               | class/chaos separation for all four combinative classes; shows the class prefix growing toward its stable core across the build-up phase              |
| `analysis/interior/rule30_class_a_layers.py`        | full layer table for Class A (gen 2, 6, 10, …) with alphabet legend and structure diagram                                                            |
| `analysis/interior/rule30_class_b_layers.py`        | full layer table for Class B (gen 3, 7, 11, …) with alphabet legend and structure diagram                                                            |
| `analysis/interior/rule30_class_c_layers.py`        | full layer table for Class C (gen 4, 8, 12, …) with alphabet legend and structure diagram                                                            |
| `analysis/interior/rule30_class_d_layers.py`        | full layer table for Class D (gen 5, 9, 13, …) with alphabet legend and structure diagram                                                            |