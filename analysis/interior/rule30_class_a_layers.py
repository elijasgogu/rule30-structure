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
GENS = 200
cells=[0,0,1,0,0]; itr_full={}
for gen in range(GENS):
    p=[0,0]+cells+[0,0]; v=[]
    for i in range(len(p)-2):
        l,m,r=p[i],p[i+1],p[i+2]
        if any(x for x in(l,m,r)): v.append(l*4+m*2+r)
    itr_full[gen] = v[3:]          # strip left boundary 1,3,6 — keep rightmost C
    cells = ng(cells)

# ── Class A definition ───────────────────────────────────────────────────────
LEFT_CONST  = "A"          # invariant left boundary  (triplets 1,3,6 = symbol A)
CORE        = "BBEBHJJI"   # stable core, from gen 34
RIGHT_CONST = "C"          # invariant right boundary (triplet 4 = symbol C)

# Left alternating layers  (label, even_token, odd_token, stable_from_rep)
# rep_idx counted from START_GEN with step STEP; parity: rep_idx % 2
LAYERS = [
    ("L1", "B",      "E",      0),
    ("L2", "JI",     "B",      2),
    ("L3", "EJI",    "IE",     8),
    ("L4", "BHB",    "IJB",   11),
    ("L5", "IHIIJ",  "BJHJHB",17),
]

# Right alternating segment  (before RIGHT_CONST)
# parity counted from gen 2 / step 4
RIGHT_EVEN = "B"    # rep_idx_abs % 2 == 0
RIGHT_ODD  = "BB"   # rep_idx_abs % 2 == 1

START_GEN = 34
STEP      = 4

BUILDUP = [
    ( 2, "B"),
    ( 6, "BB"),
    (10, "BB"),
    (14, "BBEB"),
    (18, "BBEB"),
    (22, "BBEB"),
    (26, "BBEBHJ"),
    (30, "BBEBHJJ"),
]

# ── column widths ─────────────────────────────────────────────────────────────
W_GEN    = 3
W_LCONST = len(LEFT_CONST)
W_CORE   = len(CORE)
W_LAYERS = [max(len(e), len(o), len(lbl)) for lbl, e, o, _ in LAYERS]
W_RIGHT  = max(len(RIGHT_EVEN), len(RIGHT_ODD), 1)
W_RCONST = len(RIGHT_CONST)

def cell(val, w):   return val.ljust(w)
def sep_col(w):     return "═" * (w + 2)   # +2 for surrounding spaces

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
    if tag:
        parts.append("  " + tag)
    return "".join(parts)

def make_sep(double=False):
    ch = "═" if double else "─"
    def sc(w): return ch*(w+2)
    mid = ("╬" if double else "╫").join(
        [sc(W_GEN)] +
        [sc(W_LCONST)] +
        [sc(W_CORE)] +
        [sc(w) for w in W_LAYERS] +
        [sc(W_RIGHT)] +
        [sc(W_RCONST)]
    )
    left  = "╠" if double else "╟"
    right_b = "╣" if double else "╢"
    return left + mid + right_b

def make_top():
    def sc(w): return "═"*(w+2)
    mid = "╦".join(
        [sc(W_GEN)] +
        [sc(W_LCONST)] +
        [sc(W_CORE)] +
        [sc(w) for w in W_LAYERS] +
        [sc(W_RIGHT)] +
        [sc(W_RCONST)]
    )
    return "╔" + mid + "╗"

def make_hdr():
    lbls = ["L%d"%i for i,_ in enumerate(LAYERS,1)]
    return make_row("Gen", "A", "Core", [l[0] for l in LAYERS], "Chaos", "R", "C")

def get_right_seg(d_full, abs_rep):
    if d_full.endswith(RIGHT_CONST):
        body = d_full[:-len(RIGHT_CONST)]
        tok  = RIGHT_EVEN if abs_rep % 2 == 0 else RIGHT_ODD
        if body.endswith(tok):
            return body[:-len(tok)], tok, RIGHT_CONST
        return body, "?", RIGHT_CONST
    return d_full, "?", "?"

empty_L = [""] * len(LAYERS)

# ══ ALPHABET LEGEND ══════════════════════════════════════════════════════════
print()
print("  Rule 30 Interior Alphabet  (26 symbols)")
print("  " + "─"*52)
print("  Each symbol represents a fixed sequence of triplet values.")
print("  Decoding is greedy, longest match first.")
print()
cols = 3
rows = [ALPHA_DEF[i::cols] for i in range(cols)]
# transpose back to row-major
items = ALPHA_DEF
for i in range(0, len(items), cols):
    row = items[i:i+cols]
    line = "   ".join("  %s = %-20s" % (sym, seq) for sym, seq in row)
    print(line)

# ══ STRUCTURE DIAGRAM ════════════════════════════════════════════════════════
print()
print("  Interior structure of Class A  (every 4th generation: 2, 6, 10, ...)")
print()
print("  ┌───┐  ┌──────────┐  ┌──┐ ┌────┐ ┌───┐ ┌─────┐ ┌────────┐  ┌─────────────────┐  ┌──┐  ┌───┐")
print("  │ A │  │ BBEBHJJI │  │L1│ │ L2 │ │ L3│ │ L4  │ │   L5   │  │      Chaos      │  │R │  │ C │")
print("  └───┘  └──────────┘  └──┘ └────┘ └───┘ └─────┘ └────────┘  └─────────────────┘  └──┘  └───┘")
print("  fixed  build→stable   ←─────── alternating layers ────────→   grows unbounded    alt  fixed")
print()
print("  Left boundary (A)  : invariant, always present (triplets 1,3,6)")
print("  Core (BBEBHJJI)    : builds up over first 8 reps, then stable")
print("  L1 .. L5           : each layer contributes one token to two growing sets;")
print("                       the sets alternate pairwise as a unit, period doubles with each new layer")
print("                       (further layers expected as more generations are computed)")
print("  R                  : permanently coupled to set parity (B = even set / BB = odd set)")
print("  Right boundary (C) : invariant, always present (triplet 4)")
print()
print("  Note: the Chaos region lies between the last confirmed layer (L5 or")
print("  whichever is active) and the right segment R.  Because Chaos grows")
print("  without bound it has been moved to the far right of the table so that")
print("  all structured columns remain aligned and readable.")
print()

# ══ TABLE ════════════════════════════════════════════════════════════════════
print("  " + make_top())
print("  " + make_hdr())
print("  " + make_sep(double=True))

# build-up phase
for gen, prefix in BUILDUP:
    abs_rep = (gen - 2) // 4
    d_full  = dec(itr_full[gen])

    # gen 2: only Core exists – no Chaos, no R, no C
    if gen == 2:
        print("  " + make_row("%d"%gen, "A", prefix, empty_L, "", "", "", "[build]"))
        continue

    # gen 6: Core + Chaos only – R alternation begins at gen 10
    if gen == 6:
        body  = d_full[:-len(RIGHT_CONST)] if d_full.endswith(RIGHT_CONST) else d_full
        chaos = body[len(prefix):] if body.startswith(prefix) else body
        print("  " + make_row("%d"%gen, "A", prefix, empty_L, chaos, "", "", "[build]"))
        continue

    # gen 10 onward: R alternates normally
    mid, rtok, ctok = get_right_seg(d_full, abs_rep)
    chaos   = mid[len(prefix):] if mid.startswith(prefix) else mid
    print("  " + make_row("%d"%gen, "A", prefix, empty_L, chaos, rtok, ctok, "[build]"))

print("  " + make_sep(double=True))

# stable phase
for rep_idx in range(50):
    gen = START_GEN + rep_idx * STEP
    if gen >= GENS: break
    abs_rep = (gen - 2) // 4
    d_full  = dec(itr_full[gen])
    mid, rtok, ctok = get_right_seg(d_full, abs_rep)
    if not mid.startswith(CORE):
        print("  " + make_row("%d"%gen, "A", "?", empty_L, mid, rtok, ctok))
        continue
    rest = mid[len(CORE):]
    layer_cells = []
    for lbl, tok_e, tok_o, sfr in LAYERS:
        if rep_idx < sfr:
            layer_cells.append(""); continue
        tok = tok_e if rep_idx % 2 == 0 else tok_o
        if rest.startswith(tok):
            layer_cells.append(tok); rest = rest[len(tok):]
        else:
            layer_cells.append("?")
    print("  " + make_row("%d"%gen, "A", CORE, layer_cells, rest, rtok, ctok))