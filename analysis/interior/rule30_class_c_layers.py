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
GENS = 250
cells=[0,0,1,0,0]; itr_full={}
for gen in range(GENS):
    p=[0,0]+cells+[0,0]; v=[]
    for i in range(len(p)-2):
        l,m,r=p[i],p[i+1],p[i+2]
        if any(x for x in(l,m,r)): v.append(l*4+m*2+r)
    itr_full[gen] = v[3:]
    cells = ng(cells)

# ── Class C definition ───────────────────────────────────────────────────────
LEFT_CONST  = "A"
CORE        = "BGMMJ"
RIGHT_CONST = "C"
R_TOKEN     = "B"   # R is always B, every repetition

# Left alternating layers (label, F-set-token, BB-set-token, stable_from_rep)
# F-set  = starts with F  (parity=0: rep_idx even w.r.t. class parity)
# BB-set = starts with BB (parity=1)
# Empirically: rep_idx%2==0 -> BB-set active, rep_idx%2==1 -> F-set active
LAYERS = [
    ("L1",  "F",   "BB",   0),   # stable from rep=0  (gen 36)
    ("L2",  "J",   "E",    3),   # stable from rep=3  (gen 48)
    ("L3",  "F",   "DH",   7),   # stable from rep=7  (gen 64)
    ("L4",  "GJI", "BB",   10),  # stable from rep=10 (gen 76)
    ("L5",  "B",   "B",    11),  # stable from rep=11 (gen 80) — note: rep 11 not 14
    ("L6",  "DJJ", "JGJB", 16),  # stable from rep=16 (gen 100)
    ("L7",  "G",   "G",    18),  # stable from rep=18 (gen 108)
    ("L8",  "JI",  "B",    21),  # stable from rep=21 (gen 120)
    ("L9",  "BJ",  "JJ",   23),  # stable from rep=23 (gen 128)
    ("L10", "B",   "B",    24),  # stable from rep=24 (gen 132)
    ("L11", "BH",  "OH",   27),  # stable from rep=27 (gen 144)
]

START_GEN   = 36   # first stable rep
STEP        = 4
CLASS_START = 4    # first gen of class C

BUILDUP = [
    ( 4, "B"),
    ( 8, "BG"),
    (12, "BG"),
    (16, "BGM"),
    (20, "BGM"),
    (24, "BGM"),
    (28, "BGMM"),
    (32, "BGMMJ"),
]

# ── column widths ─────────────────────────────────────────────────────────────
W_GEN    = 3
W_LCONST = len(LEFT_CONST)
W_CORE   = len(CORE)
W_LAYERS = [max(len(e), len(o), len(lbl)) for lbl, e, o, _ in LAYERS]
W_RIGHT  = len(R_TOKEN)
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

empty_L = [""] * len(LAYERS)

# ── ALPHABET LEGEND ───────────────────────────────────────────────────────────
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

# ── STRUCTURE DIAGRAM ─────────────────────────────────────────────────────────
print()
print("  Interior structure of Class C  (every 4th generation: 4, 8, 12, ...)")
print()
print("  ┌───┐  ┌───────┐  ┌──┐ ┌──┐ ┌──┐ ┌──┐ ┌──┐ ┌──┐ ┌──┐ ┌──┐ ┌──┐ ┌──┐ ┌───┐  ┌──────────────────┐  ┌──┐  ┌───┐")
print("  │ A │  │ BGMMJ │  │L1│ │L2│ │L3│ │L4│ │L5│ │L6│ │L7│ │L8│ │L9│ │..│ │L11│  │      Chaos       │  │R │  │ C │")
print("  └───┘  └───────┘  └──┘ └──┘ └──┘ └──┘ └──┘ └──┘ └──┘ └──┘ └──┘ └──┘ └───┘  └──────────────────┘  └──┘  └───┘")
print("  fixed  build→stable  ←────────────── two alternating sets grow by concatenation ──────────────→   fixed  fixed")
print()
print("  Left boundary (A)  : invariant, always present (triplets 1,3,6)")
print("  Core (BGMMJ)       : builds up over first 8 reps, then stable")
print("  L1 .. L11          : each layer contributes one token to two growing sets;")
print("                       the sets alternate pairwise as a unit, period doubles with each new layer")
print("                       (further layers expected as more generations are computed)")
print("  R                  : always B — constant on every repetition, no parity variation")
print("  Right boundary (C) : invariant, always present (triplet 4)")
print()
print("  Note: the Chaos region lies between the last confirmed layer and R.")
print("  Because Chaos grows without bound it has been moved to the far right of")
print("  the table so that all structured columns remain aligned and readable.")
print()

# ── TABLE ─────────────────────────────────────────────────────────────────────
print("  " + make_top())
print("  " + make_hdr())
print("  " + make_sep(double=True))

# build-up phase
for gen, prefix in BUILDUP:
    rep = (gen - CLASS_START) // STEP
    d_full = dec(itr_full[gen])
    body = d_full[:-len(RIGHT_CONST)] if d_full.endswith(RIGHT_CONST) else d_full
    if body.endswith(R_TOKEN): body = body[:-len(R_TOKEN)]
    chaos = body[len(prefix):] if body.startswith(prefix) else body
    rc = RIGHT_CONST if d_full.endswith(RIGHT_CONST) else ""
    print("  " + make_row("%d"%gen, "A", prefix, empty_L, chaos, R_TOKEN if gen>=8 else "", rc, "[build]"))

print("  " + make_sep(double=True))

# stable phase
for rep_idx in range(120):
    gen = START_GEN + rep_idx * STEP
    if gen >= GENS: break

    d_full = dec(itr_full[gen])
    rc = RIGHT_CONST if d_full.endswith(RIGHT_CONST) else ""
    body = d_full[:-len(RIGHT_CONST)] if d_full.endswith(RIGHT_CONST) else d_full
    if body.endswith(R_TOKEN): body = body[:-len(R_TOKEN)]

    if not body.startswith(CORE):
        print("  " + make_row("%d"%gen, "A", "?", empty_L, body, R_TOKEN, rc))
        continue
    rest = body[len(CORE):]

    # parity: rep_idx%2==1 -> F-set, rep_idx%2==0 -> BB-set
    use_F = (rep_idx % 2 == 1)
    set_F = ""; set_BB = ""
    layer_cells = []
    for lbl, tok_f, tok_bb, sfr in LAYERS:
        if rep_idx < sfr:
            layer_cells.append("")
            continue
        set_F  += tok_f
        set_BB += tok_bb
        layer_cells.append(tok_f if use_F else tok_bb)

    active_set = set_F if use_F else set_BB
    chaos = rest[len(active_set):] if rest.startswith(active_set) else rest

    print("  " + make_row("%d"%gen, "A", CORE, layer_cells, chaos, R_TOKEN, rc))
