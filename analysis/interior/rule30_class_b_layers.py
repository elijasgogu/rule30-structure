RULE30={(1,1,1):0,(1,1,0):0,(1,0,1):0,(1,0,0):1,(0,1,1):1,(0,1,0):1,(0,0,1):1,(0,0,0):0}
def ng(c):
    p=[0,0]+c+[0,0];return[RULE30[(p[i],p[i+1],p[i+2])]for i in range(len(p)-2)]
def ps(s):return[int(c)for c in s]

ALPHA_DEF = [
    ("A","136"),("B","412"),("C","4"),
    ("D","53776"),("E","5376"),("F","41377776"),("G","41376"),("H","536"),
    ("I","4136"),("J","52"),("K","537776"),("L","413777776"),
    ("M","413776"),("N","5377776"),("O","4137776"),("P","5377777776"),
    ("Q","413777777776"),("R","537777777776"),("S","4137777776"),
    ("T","537777776"),("U","53777776"),("V","53777777776"),
    ("W","5377777777776"),("X","5377777777777776"),
    ("Y","53777777777776"),("Z","413777777777777776"),
]
AL = sorted([(ps(seq), sym) for sym, seq in ALPHA_DEF], key=lambda x: -len(x[0]))
seen=set(); AD=[]
for seq, sym in AL:
    k=tuple(seq)
    if k not in seen: seen.add(k); AD.append((seq, sym))

def dec(interior):
    r=[]; i=0
    while i < len(interior):
        for seq, sym in AD:
            if interior[i:i+len(seq)] == seq:
                r.append(sym); i+=len(seq); break
        else:
            r.append("?"); i+=1
    return "".join(r)

# ── automaton ────────────────────────────────────────────────────────────────
GENS = 300
cells=[0,0,1,0,0]; itr_full={}
for gen in range(GENS):
    p=[0,0]+cells+[0,0]; v=[]
    for i in range(len(p)-2):
        l,m,r=p[i],p[i+1],p[i+2]
        if any(x for x in(l,m,r)): v.append(l*4+m*2+r)
    itr_full[gen] = v[3:]
    cells = ng(cells)

# ── Class B definition ───────────────────────────────────────────────────────
LEFT_CONST  = "A"
CORE        = "DIJGJBD"
RIGHT_CONST = "C"

# Left alternating layers (label, even_token, odd_token, stable_from_rep)
# rep_idx = (gen - START_GEN) / STEP
# Core DIJGJBD is fully stable from gen 39 - it does NOT alternate.
# L1 starts with EH (even) | BB (odd) — the E is part of L1, not the core.

LAYERS = [
    ("L1",  "EH",  "BB",   1),   # stable from rep=1  (gen 43)
    ("L2",  "I",   "K",    3),   # stable from rep=3  (gen 51)
    ("L3",  "B",   "B",    5),   # stable from rep=5  (gen 59)
    ("L4",  "I",   "G",    7),   # stable from rep=7  (gen 67)
    ("L5",  "H",   "I",    9),   # stable from rep=9  (gen 75)
    ("L6",  "EJ",  "O",    11),  # stable from rep=11 (gen 83)
    ("L7",  "N",   "JJ",   13),  # stable from rep=13 (gen 91)
    ("L8",  "BE",  "BJ",   15),  # stable from rep=15 (gen 99)
    ("L9",  "E",   "DI",   17),  # stable from rep=17 (gen 107)
    ("L10", "MJJ", "GJ",   21),  # stable from rep=21 (gen 123)
]

# ── R pattern for Class B ────────────────────────────────────────────────────
# rep_idx = (gen - 3) // 4
# rep=0: no R
# rep even (>0): R = "D"
# rep odd: odd_rank = (rep-1)//2
#   trailing_zeros(odd_rank+1)=0: "F" if odd_rank%4==0 else "N"
#   trailing_zeros(odd_rank+1)=1: "L"
#   trailing_zeros(odd_rank+1)=2: "P"
#   trailing_zeros(odd_rank+1)=3: "X"
#   trailing_zeros(odd_rank+1)=4: "Z"

def trailing_zeros(n):
    if n == 0: return 99
    c = 0
    while not (n & 1): c += 1; n >>= 1
    return c

def get_R(rep):
    if rep == 0: return ""
    if rep % 2 == 0: return "D"
    odd_rank = (rep - 1) // 2
    tz = trailing_zeros(odd_rank + 1)
    if tz == 0: return "F" if odd_rank % 4 == 0 else "N"
    return {1:"L", 2:"P", 3:"X", 4:"Z"}.get(tz, "?")

START_GEN = 39   # first stable rep (rep_idx=0 for layers)
STEP      = 4
CLASS_START = 3  # first gen of class B

BUILDUP = [
    ( 3, "D"),
    ( 7, "D"),
    (11, "DIJ"),
    (15, "DIJ"),
    (19, "DIJ"),
    (23, "DIJGJB"),
    (27, "DIJGJB"),
    (31, "DIJGJB"),
    (35, "DIJGJBD"),
]

# ── column widths ─────────────────────────────────────────────────────────────
W_GEN    = 3
W_LCONST = len(LEFT_CONST)
W_CORE   = len(CORE)
W_LAYERS = [max(len(e), len(o), len(lbl)) for lbl, e, o, _ in LAYERS]
# R width: max of all possible R tokens
R_TOKENS = ["D","F","L","N","P","X","Z",""]
W_RIGHT  = max(len(t) for t in R_TOKENS)
W_RCONST = len(RIGHT_CONST)

def cell(val, w): return val.ljust(w)

def make_row(gen_str, lc, core, layers, chaos, right, rc, tag=""):
    parts = [
        "║",
        " %s " % gen_str.center(W_GEN),
        "║",
        " %s " % cell(lc,    W_LCONST),
        "║",
        " %s " % cell(core,  W_CORE),
        "║",
    ]
    for val, w in zip(layers, W_LAYERS):
        parts += [" %s " % cell(val, w), "║"]
    parts += [
        " %s " % cell(right, W_RIGHT), "║",
        " %s " % cell(rc,    W_RCONST), "║",
        "  %s" % chaos,
    ]
    if tag: parts.append("  " + tag)
    return "".join(parts)

def make_sep(double=False):
    ch = "═" if double else "─"
    def sc(w): return ch*(w+2)
    mid = ("╬" if double else "╫").join(
        [sc(W_GEN), sc(W_LCONST), sc(W_CORE)] +
        [sc(w) for w in W_LAYERS] +
        [sc(W_RIGHT), sc(W_RCONST)]
    )
    l = "╠" if double else "╟"
    r = "╣" if double else "╢"
    return l + mid + r

def make_top():
    def sc(w): return "═"*(w+2)
    mid = "╦".join(
        [sc(W_GEN), sc(W_LCONST), sc(W_CORE)] +
        [sc(w) for w in W_LAYERS] +
        [sc(W_RIGHT), sc(W_RCONST)]
    )
    return "╔" + mid + "╗"

def make_hdr():
    return make_row("Gen", "A", "Core", [l[0] for l in LAYERS], "Chaos", "R", "C")

def get_chaos(d_full, prefix, right_tok):
    """Strip A (already stripped from left), core+layers prefix, R token and C from decoded."""
    if d_full.endswith(RIGHT_CONST):
        body = d_full[:-len(RIGHT_CONST)]
    else:
        body = d_full
    if right_tok and body.endswith(right_tok):
        body = body[:-len(right_tok)]
    if body.startswith(prefix):
        return body[len(prefix):]
    return body

empty_L = [""] * len(LAYERS)

# ══ ALPHABET LEGEND ══════════════════════════════════════════════════════════
print()
print("  Rule 30 Interior Alphabet  (26 symbols)")
print("  " + "─"*52)
print("  Each symbol represents a fixed sequence of triplet values.")
print("  Decoding is greedy, longest match first.")
print("  The alphabet reflects sequences observed up to the generations analyzed;")
print("  additional symbols are expected as further generations are computed.")
print()
for i in range(0, len(ALPHA_DEF), 3):
    row = ALPHA_DEF[i:i+3]
    print("   ".join("  %s = %-20s" % (sym, seq) for sym, seq in row))

# ══ STRUCTURE DIAGRAM ════════════════════════════════════════════════════════
print()
print("  Interior structure of Class B  (every 4th generation: 3, 7, 11, ...)")
print()
print("  ┌───┐  ┌─────────┐  ┌──┐ ┌──┐ ┌──┐ ┌──┐ ┌──┐ ┌──┐ ┌──┐ ┌──┐ ┌──┐ ┌───┐  ┌──────────────────┐  ┌──────┐  ┌───┐")
print("  │ A │  │ DIJGJBD │  │L1│ │L2│ │L3│ │L4│ │L5│ │L6│ │L7│ │L8│ │L9│ │L10│  │      Chaos       │  │  R   │  │ C │")
print("  └───┘  └─────────┘  └──┘ └──┘ └──┘ └──┘ └──┘ └──┘ └──┘ └──┘ └──┘ └───┘  └──────────────────┘  └──────┘  └───┘")
print("  fixed  build→stable  ←────────────── two alternating sets grow by concatenation ──────────────→   parity   fixed")
print()
print("  Left boundary (A)  : invariant, always present (triplets 1,3,6)")
print("  Core (DIJGJBD)     : builds up over first 9 reps, then stable")
print("  L1 .. L10          : each layer contributes one token to two growing sets;")
print("                       the sets alternate pairwise as a unit, period doubles with each new layer")
print("                       (further layers expected as more generations are computed)")
print("  R                  : permanently coupled to set parity via a structured symbol sequence")
print("                       (D on even reps; F/L/N/P/X/Z on odd reps by period-doubling pattern)")
print("  Right boundary (C) : invariant, always present (triplet 4)")
print()
print("  Note: the Chaos region lies between the last confirmed layer and R.")
print("  Because Chaos grows without bound it has been moved to the far right of")
print("  the table so that all structured columns remain aligned and readable.")
print()

# ══ TABLE ════════════════════════════════════════════════════════════════════
print("  " + make_top())
print("  " + make_hdr())
print("  " + make_sep(double=True))

# build-up phase
for gen, prefix in BUILDUP:
    rep = (gen - CLASS_START) // STEP
    rtok = get_R(rep)
    d_full = dec(itr_full[gen])
    chaos = get_chaos(d_full, prefix, rtok)
    rc = RIGHT_CONST if d_full.endswith(RIGHT_CONST) else ""
    print("  " + make_row("%d"%gen, "A", prefix, empty_L, chaos, rtok, rc, "[build]"))

print("  " + make_sep(double=True))

# stable phase
for rep_idx in range(80):
    gen = START_GEN + rep_idx * STEP
    if gen >= GENS: break
    abs_rep = (gen - CLASS_START) // STEP
    rtok = get_R(abs_rep)
    d_full = dec(itr_full[gen])
    rc = RIGHT_CONST if d_full.endswith(RIGHT_CONST) else ""

    # strip A (left boundary already stripped by itr_full[3:])
    # strip right: C then R token
    body = d_full[:-len(RIGHT_CONST)] if d_full.endswith(RIGHT_CONST) else d_full
    if rtok and body.endswith(rtok):
        body = body[:-len(rtok)]

    if not body.startswith(CORE):
        print("  " + make_row("%d"%gen, "A", "?", empty_L, body, rtok, rc))
        continue
    rest = body[len(CORE):]

    # build even/odd sets by concatenation of active layers
    # parity: rep_idx % 2 == 1 shows even set tokens (inverted convention for Class B)
    set_even = ""
    set_odd  = ""
    layer_cells = []
    for lbl, tok_e, tok_o, sfr in LAYERS:
        if rep_idx < sfr:
            layer_cells.append("")
            continue
        set_even += tok_e
        set_odd  += tok_o
        layer_cells.append(tok_e if rep_idx % 2 == 1 else tok_o)

    # active set for this rep
    active_set = set_even if rep_idx % 2 == 1 else set_odd
    if rest.startswith(active_set):
        chaos = rest[len(active_set):]
    else:
        chaos = rest  # fallback

    print("  " + make_row("%d"%gen, "A", CORE, layer_cells, chaos, rtok, rc))