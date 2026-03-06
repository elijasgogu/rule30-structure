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

# ── Class D definition ───────────────────────────────────────────────────────
LEFT_CONST  = "A"
CORE        = "DHGBHI"
RIGHT_CONST = "C"
CLASS_START = 5   # first gen of class D

# R alternates E/G: abs_rep=(gen-5)//4, E when abs_rep%2==0, G when abs_rep%2==1
def get_R(gen):
    abs_rep = (gen - CLASS_START) // 4
    return "E" if abs_rep % 2 == 0 else "G"

# Left alternating layers (label, G-set-token, H-set-token, stable_from_rep)
# G-set = starts with G (active when rep_idx%2==0)
# H-set = starts with H (active when rep_idx%2==1)
LAYERS = [
    ("L1",  "G",   "H",    0),   # stable from rep=0  (gen 37)
    ("L2",  "HJ",  "II",   4),   # stable from rep=4  (gen 53)
    ("L3",  "BB",  "G",    6),   # stable from rep=6  (gen 61) — note: G-set matches from rep 6
    ("L4",  "UH",  "IHJI", 12),  # stable from rep=12 (gen 85)
    ("L5",  "H",   "J",    14),  # stable from rep=14 (gen 93)
    ("L6",  "II",  "BH",   16),  # stable from rep=16 (gen 101)
    ("L7",  "KB",  "H",    18),  # stable from rep=18 (gen 109)
    ("L8",  "I",   "I",    20),  # stable from rep=20 (gen 117)
    ("L9",  "J",   "HJH",  22),  # stable from rep=22 (gen 125)
    ("L10", "HG",  "HO",   24),  # stable from rep=24 (gen 133)
    ("L11", "I",   "J",    26),  # stable from rep=26 (gen 141)
    ("L12", "B",   "E",    28),  # stable from rep=28 (gen 149)
]

START_GEN = 37   # first stable rep (rep_idx=0)
STEP      = 4

BUILDUP = [
    ( 5, "D"),
    ( 9, "DH"),
    (13, "DHG"),
    (17, "DHG"),
    (21, "DHGB"),
    (25, "DHGBH"),
    (29, "DHGBH"),
    (33, "DHGBHI"),
]

# ── column widths ─────────────────────────────────────────────────────────────
W_GEN    = 3
W_LCONST = len(LEFT_CONST)
W_CORE   = len(CORE)
W_LAYERS = [max(len(g), len(h), len(lbl)) for lbl, g, h, _ in LAYERS]
W_RIGHT  = 1   # E or G, both width 1
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
print("  Interior structure of Class D  (every 4th generation: 5, 9, 13, ...)")
print()
print("  ┌───┐  ┌────────┐  ┌──┐ ┌──┐ ┌──┐ ┌──┐ ┌──┐ ┌──┐ ┌──┐ ┌──┐ ┌──┐ ┌──┐ ┌──┐ ┌───┐  ┌────────────┐  ┌──┐  ┌───┐")
print("  │ A │  │ DHGBHI │  │L1│ │L2│ │L3│ │L4│ │L5│ │L6│ │L7│ │L8│ │L9│ │..│ │L12│  │    Chaos     │  │R │  │ C │")
print("  └───┘  └────────┘  └──┘ └──┘ └──┘ └──┘ └──┘ └──┘ └──┘ └──┘ └──┘ └──┘ └───┘  └────────────┘  └──┘  └───┘")
print("  fixed  build→stable  ←────────────── two alternating sets grow by concatenation ──────────────→  E|G  fixed")
print()
print("  Left boundary (A)  : invariant, always present (triplets 1,3,6)")
print("  Core (DHGBHI)      : builds up over first 8 reps, then stable")
print("  L1 .. L12          : each layer contributes one token to two growing sets;")
print("                       the sets alternate pairwise as a unit, period doubles with each new layer")
print("                       (further layers expected as more generations are computed)")
print("  R                  : strictly alternates E/G every repetition from gen 5 onward,")
print("                       independent of set parity — E on even abs_rep, G on odd abs_rep")
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
    rtok = get_R(gen)
    d_full = dec(itr_full[gen])
    body = d_full[:-len(RIGHT_CONST)] if d_full.endswith(RIGHT_CONST) else d_full
    if body.endswith(rtok): body = body[:-len(rtok)]
    chaos = body[len(prefix):] if body.startswith(prefix) else body
    rc = RIGHT_CONST if d_full.endswith(RIGHT_CONST) else ""
    print("  " + make_row("%d"%gen, "A", prefix, empty_L, chaos, rtok, rc, "[build]"))

print("  " + make_sep(double=True))

# stable phase
for rep_idx in range(130):
    gen = START_GEN + rep_idx * STEP
    if gen >= GENS: break

    rtok = get_R(gen)
    d_full = dec(itr_full[gen])
    rc = RIGHT_CONST if d_full.endswith(RIGHT_CONST) else ""
    body = d_full[:-len(RIGHT_CONST)] if d_full.endswith(RIGHT_CONST) else d_full
    if body.endswith(rtok): body = body[:-len(rtok)]

    if not body.startswith(CORE):
        print("  " + make_row("%d"%gen, "A", "?", empty_L, body, rtok, rc))
        continue
    rest = body[len(CORE):]

    # G-set active when rep_idx%2==0, H-set active when rep_idx%2==1
    use_G = (rep_idx % 2 == 0)
    set_G = ""; set_H = ""
    layer_cells = []
    for lbl, tok_g, tok_h, sfr in LAYERS:
        if rep_idx < sfr:
            layer_cells.append("")
            continue
        set_G += tok_g
        set_H += tok_h
        layer_cells.append(tok_g if use_G else tok_h)

    active_set = set_G if use_G else set_H
    chaos = rest[len(active_set):] if rest.startswith(active_set) else rest

    print("  " + make_row("%d"%gen, "A", CORE, layer_cells, chaos, rtok, rc))
