"""Fragmentos de MS propostos por regras, com a massa conferida contra os picos do SDBS.

Para cada pico (menos o M) procura, na ordem:
  1) rearranjo de McLafferty;
  2) quebra de uma ligação simples da molécula (o íon é um dos dois pedaços);
  3) a partir de um íon já atribuído: perda de CO (íon acílio) ou de um alceno (carbocátion);
  4) só pela massa: diferença compatível com uma perda comum (sem estrutura).
A massa usada é a nominal (C 12, H 1, N 14, O 16...). Dois caminhos diferentes podem dar o mesmo m/z:
por isso o app chama de "proposta", nunca de mecanismo medido."""
import re
from rdkit import Chem
from rdkit.Chem.Draw import rdMolDraw2D

NOM = {"C": 12, "H": 1, "N": 14, "O": 16, "F": 19, "Cl": 35, "Br": 79, "S": 32, "I": 127, "P": 31, "Si": 28}
SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
PERDAS = {15: "CH₃·", 17: "HO·", 18: "H₂O", 26: "HC≡CH", 27: "HCN ou C₂H₃·", 28: "CO ou CH₂=CH₂", 29: "C₂H₅· ou CHO·",
          30: "CH₂O", 31: "CH₃O·", 32: "CH₃OH", 42: "C₃H₆", 43: "C₃H₇· ou CH₃CO·", 44: "CO₂", 45: "C₂H₅O· ou HOC=O·"}

def formula(m, idxs, dh=0):
    c = {}
    for i in idxs:
        a = m.GetAtomWithIdx(i); c[a.GetSymbol()] = c.get(a.GetSymbol(), 0) + 1; c["H"] = c.get("H", 0) + a.GetTotalNumHs()
    c["H"] = c.get("H", 0) + dh
    ordem = [k for k in ("C", "H") if c.get(k)] + sorted(k for k in c if k not in ("C", "H") and c[k])
    return "".join(k + (str(c[k]).translate(SUB) if c[k] > 1 else "") for k in ordem)

def massa(m, idxs, dh=0):
    return sum(NOM.get(m.GetAtomWithIdx(i).GetSymbol(), 0) + m.GetAtomWithIdx(i).GetTotalNumHs() for i in idxs) + dh

def lado(m, ini, bloq):
    """átomos ligados a ini sem passar pela ligação bloq=(a,b)."""
    vis = {ini}; fila = [ini]
    while fila:
        x = fila.pop()
        for n in m.GetAtomWithIdx(x).GetNeighbors():
            j = n.GetIdx()
            if j in vis or {x, j} == set(bloq): continue
            vis.add(j); fila.append(j)
    return vis

def monta(m, keep, edits=None, notas=None):
    """molécula só com os átomos keep, com os H originais congelados. edits(rw, mp) mexe em ligações/cargas; mp: índice original -> novo."""
    rw = Chem.RWMol(m)
    for a in rw.GetAtoms():
        a.SetIntProp("o", a.GetIdx()); a.SetNumExplicitHs(a.GetTotalNumHs()); a.SetNoImplicit(True)
    for i in sorted((a.GetIdx() for a in rw.GetAtoms() if a.GetIdx() not in keep), reverse=True): rw.RemoveAtom(i)
    mp = {a.GetIntProp("o"): a.GetIdx() for a in rw.GetAtoms()}
    # ligações cortadas entre átomos mantidos (ex.: McLafferty) são tratadas no edits
    if edits: edits(rw, mp)
    for o, t in (notas or {}).items(): rw.GetAtomWithIdx(mp[o]).SetProp("atomNote", t)
    try:
        mm = rw.GetMol(); Chem.SanitizeMol(mm); return mm
    except Exception:
        return None

def tipo_aberto(m, keep, o):
    """Onde fica a carga quando a ligação em o foi cortada. Devolve (edits, regra, nota, nota_extra, nivel) ou None."""
    a = m.GetAtomWithIdx(o)
    if a.GetSymbol() != "C": return None
    viz = [n for n in a.GetNeighbors() if n.GetIdx() in keep]
    # íon acílio
    for n in viz:
        b = m.GetBondBetweenAtoms(o, n.GetIdx())
        if n.GetSymbol() == "O" and b.GetBondTypeAsDouble() == 2:
            def ed(rw, mp, o=o, x=n.GetIdx()):
                rw.GetBondBetweenAtoms(mp[o], mp[x]).SetBondType(Chem.BondType.TRIPLE); rw.GetAtomWithIdx(mp[x]).SetFormalCharge(1)
            return ed, "íon acílio: clivagem α ao C=O, o C≡O⁺ é muito estável", 6
    # par de elétrons vizinho (O, N, S) fora de anel aromático
    if not a.GetIsAromatic():
        for n in viz:
            b = m.GetBondBetweenAtoms(o, n.GetIdx())
            if n.GetSymbol() in ("O", "N", "S") and not n.GetIsAromatic() and b.GetBondTypeAsDouble() == 1:
                def ed(rw, mp, o=o, x=n.GetIdx()):
                    rw.GetBondBetweenAtoms(mp[o], mp[x]).SetBondType(Chem.BondType.DOUBLE); rw.GetAtomWithIdx(mp[x]).SetFormalCharge(1)
                return ed, "clivagem α ao %s: o par de elétrons dele estabiliza o íon (C=%s⁺)" % (n.GetSymbol(), n.GetSymbol()), 5
    def mais(rw, mp, o=o): rw.GetAtomWithIdx(mp[o]).SetFormalCharge(1)
    if a.GetIsAromatic(): return mais, "íon arila: o substituinte saiu do anel", 1
    sp3 = a.GetHybridization() == Chem.HybridizationType.SP3
    if sp3 and any(n.GetIsAromatic() for n in viz): return mais, "clivagem benzílica: o anel estabiliza o íon", 5
    if sp3 and any(m.GetBondBetweenAtoms(o, n.GetIdx()).GetBondTypeAsDouble() == 1 and any(
            m.GetBondBetweenAtoms(n.GetIdx(), k.GetIdx()).GetBondTypeAsDouble() == 2 for k in n.GetNeighbors() if k.GetIdx() != o) for n in viz):
        return mais, "carbocátion alílico (ressonância com a C=C)", 4
    if not sp3: return mais, "carbocátion vinílico (pouco estável)", 1
    k = len(viz)
    return mais, {1: "carbocátion primário (pouco estável)", 2: "carbocátion secundário", 3: "carbocátion terciário"}.get(k, "carbocátion"), {1: 1, 2: 3, 3: 4}.get(k, 1)

def svg_ion(mm, w=180, h=110, bond=32):
    mm = Chem.Mol(mm)
    for a in mm.GetAtoms():
        if a.GetSymbol() == "C" and a.GetFormalCharge() == 1:
            n = a.GetTotalNumHs(); a.SetProp("atomLabel", "C" + ("H" + ("<sub>%d</sub>" % n if n > 1 else "") if n else "") + "<sup>+</sup>")
    d = rdMolDraw2D.MolDraw2DSVG(w, h); o = d.drawOptions()
    o.clearBackground = False; o.fixedBondLength = bond; o.padding = 0.22; o.bondLineWidth = 2; o.annotationFontScale = 0.8
    rdMolDraw2D.PrepareAndDrawMolecule(d, mm); d.FinishDrawing()
    t = re.sub(r'<\?xml.*?\?>', '', d.GetDrawingText())
    t = re.sub(r"<rect[^>]*?style='opacity:1\.0;fill:#FFFFFF[^>]*?/>", '', t)
    t = t.replace('#000000', 'currentColor').replace('#FF0000', 'var(--lost)').replace('#0000FF', 'var(--blue)')
    t = re.sub(r"<svg[^>]*>", '<svg viewBox="0 0 %d %d" xmlns="http://www.w3.org/2000/svg" role="img">' % (w, h), t, count=1)
    return re.sub(r'\s+', ' ', re.sub(r'<!--.*?-->', '', t)).strip()

def _item(mz, par, ion_f, neutro, regra, nivel, mm, tipo="c", rad=False):
    return dict(mz=mz, de=par, f=ion_f + ("⁺·" if rad else "⁺"), n=neutro, r=regra, nv=nivel, mm=mm, t=tipo)

def candidatos(m, M, picos):
    """{mz: [item,...]} da molécula inteira (profundidade 1)."""
    out = {}
    n = m.GetNumAtoms(); todos = set(range(n))
    for b in m.GetBonds():
        if b.IsInRing() or b.GetBondTypeAsDouble() != 1 or b.GetIsAromatic(): continue
        i, j = b.GetBeginAtomIdx(), b.GetEndAtomIdx()
        A = lado(m, i, (i, j)); B = todos - A
        for ion, ou, o, neu, outro in ((A, i, i, B, j), (B, j, j, A, i)):
            if len(ion) < 2: continue
            mz = massa(m, ion)
            if mz not in picos or mz == M: continue
            t = tipo_aberto(m, ion, o)
            if not t: continue
            ed, regra, nv = t
            mm = monta(m, ion, ed)
            if mm is None: continue
            nf = formula(m, neu)
            out.setdefault(mz, []).append(dict(item=_item(mz, M, formula(m, ion), nf + "·", regra, nv, mm), ion=ion, o=o))
    return out

MCL = Chem.MolFromSmarts("O=[CX3]-[CX4]-[CX4]-[CX4;!H0]")
def mclafferty(m, M, picos):
    out = {}
    for (o, c1, ca, cb, cg) in m.GetSubstructMatches(MCL):
        bd = m.GetBondBetweenAtoms(ca, cb)
        if bd.IsInRing(): continue
        E = lado(m, c1, (ca, cb)); G = set(range(m.GetNumAtoms())) - E
        mzE = massa(m, E, 1)
        if mzE in picos and mzE != M:
            def ed(rw, mp, o=o, c1=c1, ca=ca):
                rw.GetBondBetweenAtoms(mp[o], mp[c1]).SetBondType(Chem.BondType.SINGLE)
                rw.GetBondBetweenAtoms(mp[c1], mp[ca]).SetBondType(Chem.BondType.DOUBLE)
                x = rw.GetAtomWithIdx(mp[o]); x.SetNumExplicitHs(x.GetNumExplicitHs() + 1)
            mm = monta(m, E, ed, {o: "+•"})
            if mm is not None:
                nf = formula(m, G, -1)
                out.setdefault(mzE, []).append(dict(item=_item(mzE, M, formula(m, E, 1), nf, "rearranjo de McLafferty: o H do carbono γ passa para o O da C=O e sai um alceno (neutro)", 6, mm, rad=True), ion=E, o=None))
    return out

def filhos(m, pai, picos, M):
    """Do íon pai (já atribuído): perda de CO (acílio) ou de um alceno (carbocátion). Só para íons de quebra simples (têm 'o')."""
    out = {}
    P, o = pai["ion"], pai["o"]
    if o is None: return out
    a = m.GetAtomWithIdx(o)
    # acílio perde CO
    for n in a.GetNeighbors():
        if n.GetIdx() in P and n.GetSymbol() == "O" and m.GetBondBetweenAtoms(o, n.GetIdx()).GetBondTypeAsDouble() == 2:
            rest = P - {o, n.GetIdx()}
            viz = [k.GetIdx() for k in a.GetNeighbors() if k.GetIdx() in rest]
            if len(viz) == 1 and len(rest) >= 1:
                mz = massa(m, rest)
                if mz in picos:
                    t = tipo_aberto(m, rest, viz[0])
                    if t:
                        mm = monta(m, rest, t[0])
                        if mm is not None:
                            out.setdefault(mz, []).append(dict(item=_item(mz, pai["item"]["mz"], formula(m, rest), "C≡O", "o íon acílio perde CO (C≡O)", 5, mm), ion=rest, o=viz[0]))
            break
    # carbocátion alquílico perde alceno
    if a.GetSymbol() == "C" and not a.GetIsAromatic() and pai["item"]["nv"] <= 4 and "acílio" not in pai["item"]["r"]:
        for x in a.GetNeighbors():
            if x.GetIdx() not in P: continue
            for y in x.GetNeighbors():
                if y.GetIdx() == o or y.GetIdx() not in P: continue
                bd = m.GetBondBetweenAtoms(x.GetIdx(), y.GetIdx())
                if bd.IsInRing() or bd.GetBondTypeAsDouble() != 1: continue
                far = lado(m, y.GetIdx(), (x.GetIdx(), y.GetIdx())) & P
                near = P - far
                if len(far) < 1: continue
                mz = massa(m, far)
                if mz in picos and len(far) >= 1:
                    t = tipo_aberto(m, far, y.GetIdx())
                    if t:
                        mm = monta(m, far, t[0])
                        if mm is not None:
                            out.setdefault(mz, []).append(dict(item=_item(mz, pai["item"]["mz"], formula(m, far), formula(m, near), "o carbocátion perde um alceno (" + formula(m, near) + ") e a carga fica no pedaço maior; " + t[1], min(t[2], 4), mm), ion=far, o=y.GetIdx()))
    return out

def perda_h(m, M, picos):
    """M−1: sai um H· de um carbono onde o íon fica bem estabilizado (formila, benzílico, α a O ou N, alílico)."""
    out = {}
    if M - 1 not in picos: return out
    todos = set(range(m.GetNumAtoms()))
    for a in m.GetAtoms():
        if a.GetSymbol() != "C" or a.GetTotalNumHs() < 1: continue
        t = tipo_aberto(m, todos, a.GetIdx())
        if not t or t[2] < 4: continue
        def ed(rw, mp, o=a.GetIdx(), f=t[0]):
            x = rw.GetAtomWithIdx(mp[o]); x.SetNumExplicitHs(x.GetNumExplicitHs() - 1); f(rw, mp)
        mm = monta(m, todos, ed)
        if mm is None: continue
        reg = t[1].replace("clivagem α ao C=O, ", "").replace("clivagem α", "perda de H· α")
        if not reg.startswith("perda"): reg = "perda de H·: " + reg
        out.setdefault(M - 1, []).append(dict(item=_item(M - 1, M, formula(m, todos, -1), "H·", reg, t[2], mm), ion=todos, o=None, atomo=a.GetIdx()))
    return out

def hetero_alqueno(m, pai, picos):
    """Íon C=X⁺–R (X = O, N, S): um H do R passa para X e sai um alceno (ex.: éter dietílico 59 → 31)."""
    out = {}
    P, o = pai["ion"], pai["o"]
    if o is None: return out
    for x in m.GetAtomWithIdx(o).GetNeighbors():
        if x.GetIdx() not in P or x.GetSymbol() not in ("O", "N", "S") or x.GetIsAromatic(): continue
        if m.GetBondBetweenAtoms(o, x.GetIdx()).GetBondTypeAsDouble() != 1: continue
        for r in x.GetNeighbors():
            if r.GetIdx() == o or r.GetIdx() not in P or r.GetSymbol() != "C" or r.GetIsAromatic(): continue
            if r.GetHybridization() != Chem.HybridizationType.SP3: continue
            if not any(k.GetTotalNumHs() > 0 and k.GetIdx() != x.GetIdx() for k in r.GetNeighbors()): continue
            alq = lado(m, r.GetIdx(), (x.GetIdx(), r.GetIdx())) & P
            if any(m.GetAtomWithIdx(i).GetSymbol() != "C" or m.GetAtomWithIdx(i).GetHybridization() != Chem.HybridizationType.SP3 for i in alq): continue
            keep = P - alq; mz = massa(m, keep, 1)
            if mz not in picos or len(keep) < 2: continue
            def ed(rw, mp, o=o, x=x.GetIdx()):
                rw.GetBondBetweenAtoms(mp[o], mp[x]).SetBondType(Chem.BondType.DOUBLE)
                y = rw.GetAtomWithIdx(mp[x]); y.SetFormalCharge(1); y.SetNumExplicitHs(y.GetNumExplicitHs() + 1)
            mm = monta(m, keep, ed)
            if mm is None: continue
            nf = formula(m, alq, -1)
            out.setdefault(mz, []).append(dict(item=_item(mz, pai["item"]["mz"], formula(m, keep, 1), nf, "um H do grupo ligado ao %s passa para ele e sai um alceno (%s)" % (x.GetSymbol(), nf), 5, mm), ion=keep, o=None))
    return out

def _els(f):
    return set(re.findall(r"[A-Z][a-z]?", f.translate(str.maketrans("₀₁₂₃₄₅₆₇₈₉", "0123456789"))))

def coerente(m, x):
    """Barreira final: só passa o que usa átomos que o composto tem (ex.: sem N ou S se a molécula não tem)."""
    perm = {a.GetSymbol() for a in m.GetAtoms()} | {"H"}
    return _els(x["f"]) <= perm and _els(x["n"]) <= perm

def propor(m, M, pk):
    itens, svgs, sem = _propor(m, M, pk)
    ok = [x for x in itens if coerente(m, x)]
    sem = sem + [x["mz"] for x in itens if not coerente(m, x)]
    return ok, svgs, sem

def _propor(m, M, pk):
    """pk: [(mz, int)]. Devolve (lista de itens para o app, {chave: svg})."""
    picos = {p[0] for p in pk}; inten = dict(pk)
    todas = {}
    def junta(d):
        for k, v in d.items(): todas.setdefault(k, []).extend(v)
    junta(candidatos(m, M, picos)); junta(mclafferty(m, M, picos)); junta(perda_h(m, M, picos))
    def melhor(mz): return sorted(todas[mz], key=lambda x: -x["item"]["nv"])[0]
    for _ in range(3):
        for mz in sorted([k for k in todas if k != M], reverse=True):
            pai = melhor(mz)
            for fn in (filhos, hetero_alqueno):
                novos = fn(m, pai, picos, M) if fn is filhos else fn(m, pai, picos)
                for k, v in novos.items():
                    if k < mz:
                        for x in v:
                            if all(x["item"]["r"] != y["item"]["r"] or x["item"]["de"] != y["item"]["de"] for y in todas.get(k, [])): todas.setdefault(k, []).append(x)
    itens = []; svgs = {}; sem = []
    aro = {"C₆H₅⁺": 26, "C₇H₇⁺": 26}
    for mz in sorted(picos, key=lambda x: -inten[x]):
        if mz == M or mz == M + 2: continue
        if mz in todas:
            e = melhor(mz); it = e["item"]
            alt = len({(Chem.MolToSmiles(x["item"]["mm"]), x["item"]["de"]) for x in todas[mz]}) > 1
            key = Chem.MolToSmiles(it["mm"]) + "|" + it["f"]
            if key not in svgs: svgs[key] = svg_ion(it["mm"])
            itens.append(dict(mz=mz, p=inten[mz], f=it["f"], n=it["n"], de=it["de"], r=it["r"], nv=it["nv"], k=key, alt=alt))
            continue
        # sem estrutura: só dois casos de texto seguros
        ach = None
        for pai_mz, txt in ((M, None),):
            pass
        for pm in sorted(picos, reverse=True):
            if pm in todas and todas[pm] and melhor(pm)["item"]["f"] in aro and pm - mz == 26:
                ach = (pm, "HC≡CH", "o anel perde acetileno (regra geral dos aromáticos; estrutura não desenhada)"); break
        if ach is None and mz == M - 18 and m.HasSubstructMatch(Chem.MolFromSmarts("[OX2H]")):
            ach = (M, "H₂O", "perda de água (M−18), comum em álcoois e ácidos; estrutura não desenhada")
        if ach: itens.append(dict(mz=mz, p=inten[mz], f="", n=ach[1], de=ach[0], r=ach[2], nv=0, k="", alt=False))
        else: sem.append(mz)
    return itens, svgs, sem
