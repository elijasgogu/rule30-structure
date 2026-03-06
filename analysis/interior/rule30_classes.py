RULE30={(1,1,1):0,(1,1,0):0,(1,0,1):0,(1,0,0):1,(0,1,1):1,(0,1,0):1,(0,0,1):1,(0,0,0):0}
def ng(c):
    p=[0,0]+c+[0,0];return[RULE30[(p[i],p[i+1],p[i+2])]for i in range(len(p)-2)]
def atv(c):
    p=[0,0]+c+[0,0];v=[]
    for i in range(len(p)-2):
        l,m,r=p[i],p[i+1],p[i+2]
        if any(x!=0 for x in(l,m,r)):v.append(l*4+m*2+r)
    return v
def ps(s):return[int(c)for c in s]
AL=sorted([(ps("136"),"A"),(ps("412"),"B"),(ps("4"),"C"),(ps("53776"),"D"),(ps("5376"),"E"),(ps("41377776"),"F"),(ps("41376"),"G"),(ps("536"),"H"),(ps("4136"),"I"),(ps("52"),"J"),(ps("537776"),"K"),(ps("413777776"),"L"),(ps("413776"),"M"),(ps("5377776"),"N"),(ps("4137776"),"O"),(ps("5377777776"),"P"),(ps("413777777776"),"Q"),(ps("537777777776"),"R"),(ps("4137777776"),"S"),(ps("537777776"),"T"),(ps("53777776"),"U"),(ps("53777777776"),"V"),(ps("5377777777776"),"W"),(ps("5377777777777776"),"X"),(ps("53777777777776"),"Y"),(ps("413777777777777776"),"Z")],key=lambda x:-len(x[0]))
seen=set();AD=[]
for seq,sym in AL:
    k=tuple(seq)
    if k not in seen:seen.add(k);AD.append((seq,sym))
def dec(interior):
    r=[];i=0
    while i<len(interior):
        m=False
        for seq,sym in AD:
            n=len(seq)
            if interior[i:i+n]==seq:r.append(sym);i+=n;m=True;break
        if not m:r.append("?");i+=1
    return "".join(r)

# Hardcoded build-up phase prefixes (empirically verified, iterations 1-7)
# Key: generation, Value: exact confirmed class prefix
BUILDUP = {
    "A": {2:"B",6:"BB",10:"BB",14:"BBEB",18:"BBEB",22:"BBEB",26:"BBEBHJ",30:"BBEBHJJ"},
    "B": {3:"D",7:"D",11:"DIJ",15:"DIJ",19:"DIJ",23:"DIJGJB",27:"DIJGJB",31:"DIJGJB",35:"DIJGJBD"},
    "C": {4:"B",8:"BG",12:"BG",16:"BGM",20:"BGM",24:"BGM",28:"BGMM",32:"BGMMJ"},
    "D": {5:"D",9:"DH",13:"DHG",17:"DHG",21:"DHGB",25:"DHGBH",29:"DHGBH",33:"DHGBHI"},
}
# Stable phase: confirmed positions (hard cap)
# pos 0..stable_len-2 constant, pos stable_len-1 alternates
STABLE = {
    "A": (34,9,"BBEBHJJI","[B|E]",set("BEHIJ")),
    "B": (39,8,"DIJGJBD","[B|E]",set("BDEGIJ")),
    "C": (36,6,"BGMMJ","[B|F]",set("BFGJM")),
    "D": (37,7,"DHGBHI","[G|H]",set("BDGHI")),
}
GENS=250
cells=[0,0,1,0,0];itr={}
for gen in range(GENS):
    v=atv(cells);itr[gen]=v[3:-1]if gen>=2 else[];cells=ng(cells)

CLS=[("A",2),("B",3),("C",4),("D",5)]
print("Rule 30 - Left Interior Class Analysis")
print()
print("Interior = [ CLASS REGION | CHAOS REGION ]")
print("Boundary: 1,3,6 (left invariant) | 4 (right invariant)")
print()
print("Build-up phase: hardcoded from empirical verification (iterations 1-7).")
print("Stable phase: prefix hard-capped at positionally confirmed stable length.")
print("All symbols beyond the confirmed prefix are chaos region.")
print()
for name,start in CLS:
    sf,sl,core,alt,syms=STABLE[name]
    buildup=BUILDUP[name]
    print("="*72)
    print("  Class %s  |  gen %d, %d, %d, ...  (every 4 generations)"%(name,start,start+4,start+8))
    print("  Symbols  : {%s}"%", ".join(sorted(syms)))
    print("  Build-up : gen %d to %d  (hardcoded, 8 iterations)"%(start,sf-4))
    print("  Stable   : gen %d+   core = %s   alternates = %s"%(sf,core,alt))
    print("="*72)
    print("  %4s  %-16s  %s"%("Gen","Class prefix","Chaos region"))
    print("  "+"-"*65)
    for gen in range(start,GENS,4):
        d=dec(itr[gen])
        if gen in buildup:
            cp=buildup[gen]
            chaos=d[len(cp):]
            phase="build "
        else:
            raw=[]
            for ch in d:
                if ch in syms:raw.append(ch)
                else:break
            raw="".join(raw)
            cp=raw[:sl];chaos=d[len(cp):];phase="stable"
        print("  %4d  %-16s  %s   [%s]"%(gen,cp,chaos if chaos else"-",phase))
    print()