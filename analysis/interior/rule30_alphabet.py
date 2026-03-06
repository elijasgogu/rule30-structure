"""
Rule 30 – Interior Alphabet Analysis

The interior of each generation (values between the invariant boundaries
1,3,6 on the left and 4 on the right) is decoded into a letter sequence
using a predefined alphabet of number patterns.

Alphabet definitions:
    A = 136          B = 412          C = 4
    D = 53776        E = 5376         F = 41377776
    G = 41376        H = 536          I = 4136
    J = 52           K = 537776       L = 413777776
    M = 413776       N = 5377776      O = 4137776
    P = 5377777776   Q = 413777777776 R = 537777777776
    S = 4137777776   T = 537777776    U = 53777776
    V = 53777777776  W = 5377777777776 X = 5377777777777776

Matching is greedy, longest sequence first.
Any interior sub-sequence that cannot be matched is reported as unknown.
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

def parse_seq(s):
    return [int(c) for c in s]

# Alphabet sorted longest-first for greedy matching
ALPHABET = sorted([
    (parse_seq('136'),          'A'),
    (parse_seq('412'),          'B'),
    (parse_seq('4'),            'C'),
    (parse_seq('53776'),        'D'),
    (parse_seq('5376'),         'E'),
    (parse_seq('41377776'),     'F'),
    (parse_seq('41376'),        'G'),
    (parse_seq('536'),          'H'),
    (parse_seq('4136'),         'I'),
    (parse_seq('52'),           'J'),
    (parse_seq('537776'),       'K'),
    (parse_seq('413777776'),    'L'),
    (parse_seq('5377776'),      'N'),
    (parse_seq('413776'),       'M'),
    (parse_seq('4137776'),      'O'),
    (parse_seq('5377777777777776'), 'X'),
    (parse_seq('5377777777776'),  'W'),
    (parse_seq('53777777776'),    'V'),
    (parse_seq('53777776'),       'U'),
    (parse_seq('537777776'),      'T'),
    (parse_seq('5377777776'),     'P'),
    (parse_seq('413777777776'), 'Q'),
    (parse_seq('537777777776'), 'R'),
    (parse_seq('4137777776'),   'S'),
], key=lambda x: -len(x[0]))

# Deduplicate
seen = set()
ALPHA_DEDUP = []
for seq, sym in ALPHABET:
    k = tuple(seq)
    if k not in seen:
        seen.add(k)
        ALPHA_DEDUP.append((seq, sym))

def decode(interior):
    """
    Greedy decode of interior value list into letter sequence.
    Returns (letter_string, list_of_unknown_subsequences).
    """
    result = []
    unknowns = []
    i = 0
    while i < len(interior):
        matched = False
        for seq, sym in ALPHA_DEDUP:
            n = len(seq)
            if interior[i:i+n] == seq:
                result.append(sym)
                i += n
                matched = True
                break
        if not matched:
            # Collect unknown values until next match
            unk = [interior[i]]
            i += 1
            while i < len(interior):
                found_next = any(interior[i:i+len(seq)] == seq for seq, _ in ALPHA_DEDUP)
                if found_next:
                    break
                unk.append(interior[i])
                i += 1
            unknowns.append(''.join(map(str, unk)))
            result.append(f'?{"".join(map(str,unk))}?')
    return ''.join(result), unknowns

# --- Main ---

GENS = 55
cells = [0,0,1,0,0]
all_unknowns = {}

print(f"Rule 30 – Interior Alphabet Analysis (Gen 0–{GENS-1})")
print()
print("Alphabet:")
for seq, sym in sorted(ALPHA_DEDUP, key=lambda x: x[1]):
    print(f"  {sym} = {''.join(map(str,seq))}")
print()
print(f"{'Gen':>4}  {'Letter sequence'}")
print("-" * 70)

for gen in range(GENS):
    vals = active_triplet_values(cells)
    if gen < 2:
        interior = []
    else:
        interior = vals[3:-1]

    if interior:
        decoded, unknowns = decode(interior)
        for u in unknowns:
            all_unknowns[u] = all_unknowns.get(u, []) + [gen]
    else:
        decoded = '–'

    print(f"{gen:>4}  {decoded}")
    cells = next_gen(cells)

print()
if all_unknowns:
    print("Unknown subsequences (not in alphabet):")
    for u, gens in sorted(all_unknowns.items()):
        print(f"  {''.join(u):<20} in generations: {gens}")
else:
    print("No unknown subsequences found – interior fully covered by alphabet.")