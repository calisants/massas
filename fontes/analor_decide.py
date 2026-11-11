"""Decide, registro a registro, qual dado do banco Analor está certo, comparando com o PubChem (ref_cache/ de analor_ref.py).
Uso: python3 analor_decide.py estrutura UNIV1.DBF   -> ref_cache/decisao.json e ref_cache/escolha.json
     python3 analor_decide.py exp UNIV1.DBF          -> PF, PE e densidade: acrescenta correções em ref_cache/decisao.json
A decisão da estrutura é uma votação entre: SMILES do banco (2 votos), CAS no PubChem (2), nome em inglês e nome IUPAC no PubChem (1 cada),
mais 1 voto para quem bate com a fórmula do banco e 1 para quem bate com a massa molar do banco."""
import json, os, re, sys
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, H)
import analor_ref as R
from rdkit import Chem, RDLogger
from rdkit.Chem import rdMolDescriptors, Descriptors
from rdkit.Chem.inchi import MolToInchi
RDLogger.DisableLog('rdApp.*')

def mol(smi):
    return Chem.MolFromSmiles(smi) if smi else None
def camada(m):
    """Camada principal da InChI (fórmula, conectividade e H): ignora carga e estereoquímica e junta tautômeros."""
    try: ic = MolToInchi(m)
    except Exception: ic = ''
    if not ic: return Chem.MolToSmiles(m, isomericSmiles=False)
    p = ic.split('/'); return '/'.join(p[:2] + [x for x in p[2:] if x[:1] in 'ch'])
def inchi_est(m):
    try: return MolToInchi(m)
    except Exception: return ''
def elem(f):
    t = {}
    for parte in (f or '').split('.'):
        k = re.match(r'(\d+)', parte); k = int(k.group(1)) if k else 1
        for e, n in re.findall(r'([A-Z][a-z]?)(\d*)', parte): t[e] = t.get(e, 0) + k * (int(n) if n else 1)
    return t

def estrutura(L):
    dc = R.load('cas'); P = R.load('props'); dn = R.load('nomes')
    D = []; esc = {}
    for i, r in enumerate(L):
        pmol = R.A.num(r['PMOL']); fdb = r['FMOL']; mdb = mol(r['SMILES'])
        cand = {}   # camada -> {votos, fontes, smiles, cids}
        def add(key, v, fonte, smi=None, cid=None):
            c = cand.setdefault(key, {'v': 0, 'fontes': [], 'smi': {}, 'cids': []})
            if fonte not in c['fontes']: c['v'] += v; c['fontes'].append(fonte)
            if smi: c['smi'].setdefault('db' if cid is None else str(cid), smi)
            if cid is not None and cid not in c['cids']: c['cids'].append(cid)
        if mdb: add(camada(mdb), 2, 'banco', r['SMILES'])
        for cid in dc.get(r['CAS'], []):
            p = P.get(str(cid)); m = mol(p['smi']) if p else None
            if m: add(camada(m), 2, 'cas', p['smi'], cid)
        for k, fonte in (('NINGLES', 'nome_en'), ('NIUP', 'nome_iupac')):
            for cid in dn.get(r[k], []) if r[k] else []:
                p = P.get(str(cid)); m = mol(p['smi']) if p else None
                if m: add(camada(m), 1, fonte, p['smi'], cid)
        for key, c in cand.items():
            smi = next(iter(c['smi'].values())); m = mol(smi)
            c['f'] = rdMolDescriptors.CalcMolFormula(m); c['mw'] = Descriptors.MolWt(m)
            c['b'] = 0
            if fdb and elem(c['f']) == elem(fdb): c['b'] += 1
            if pmol and abs(c['mw'] - pmol) <= 0.35: c['b'] += 1
            c['tot'] = c['v'] + c['b']
        rank = sorted(cand.items(), key=lambda kv: -kv[1]['tot'])
        d = {'i': i, 'cas': r['CAS']}
        if not rank: d.update(est='sem_dado'); D.append(d); continue
        top = rank[0]; seg = rank[1][1]['tot'] if len(rank) > 1 else 0
        c = top[1]
        d['fontes'] = c['fontes']; d['votos'] = c['tot']; d['concorrente'] = rank[1][1]['f'] if len(rank) > 1 else None
        if c['tot'] - seg < 1:
            d.update(est='indeciso'); D.append(d); continue
        # estrutura final: a do banco se ela ganhou; senão a do PubChem (isomérica)
        if 'banco' in c['fontes']:
            smi = c['smi']['db']; cid = None
            # escolhe, entre os CIDs desta camada, o que tem a mesma estereoquímica do banco (se houver)
            for ci in c['cids']:
                if inchi_est(mol(c['smi'][str(ci)])) == inchi_est(mdb): cid = ci; break
            if cid is None and c['cids']: cid = c['cids'][0]
            d['est'] = 'banco_ok' if elem(c['f']) == elem(fdb or c['f']) else 'formula'
            d['estereo_igual'] = bool(cid is not None and inchi_est(mol(c['smi'][str(cid)])) == inchi_est(mdb))
        else:
            cid = c['cids'][0]; smi = c['smi'][str(cid)]
            d['est'] = 'troca'; d['estereo_igual'] = True
        d.update(smi=smi, f=c['f'], mw=round(c['mw'], 2), cid=cid)
        if pmol is not None and abs(c['mw'] - pmol) > 0.35: d['mw_banco'] = pmol
        if d['est'] == 'formula' or (d['est'] == 'troca' and fdb and elem(c['f']) != elem(fdb)): d['f_banco'] = fdb
        D.append(d); esc[str(i)] = cid
    return D, esc

def resumo(D):
    from collections import Counter
    print(Counter(d['est'] for d in D)); print('mw diferente:', sum('mw_banco' in d for d in D), ' fórmula do banco trocada:', sum('f_banco' in d for d in D))


# ---------- propriedades experimentais ----------
NUM = r'-?\d+(?:\.\d+)?'
RT = re.compile(r'(%s)(?:\s*(?:to|–|—|-)\s*(%s))?\s*(?:°|º|deg\.?|degrees)?\s*([CFK])\b' % (NUM, NUM))
def temps(lista, ebulicao):
    """Valores em °C de strings do PubChem; na ebulição descarta valores medidos fora de ~760 mmHg."""
    out = []
    for s, fonte in lista:
        s = s.replace('−', '-')
        if ebulicao:
            m = re.search(r'(\d+(?:\.\d+)?)\s*(mm\s?Hg|mmHg|torr|kPa|atm|bar|mbar)', s, re.I)
            if m:
                v = float(m.group(1)); u = m.group(2).lower().replace(' ', '')
                p = {'mmhg': v, 'torr': v, 'kpa': v * 7.50062, 'atm': v * 760, 'bar': v * 750.062, 'mbar': v * 0.750062}[u]
                if abs(p - 760) > 10: continue
        for m in RT.finditer(s):
            a = float(m.group(1)); b = float(m.group(2)) if m.group(2) else a; u = m.group(3)
            f = (lambda x: (x - 32) / 1.8) if u == 'F' else (lambda x: x - 273.15) if u == 'K' else (lambda x: x)
            v = (f(a) + f(b)) / 2
            if -250 < v < 1000: out.append((round(v, 1), fonte))
            break   # só a primeira temperatura da frase (as seguintes costumam ser condições)
    return out
def densidades(lista):
    out = []
    for s, fonte in lista:
        s = s.replace('−', '-')
        m = re.search(r'(\d*\.?\d+)\s*(?:g/(?:cu\.?\s?cm|cm|ml|mL|cc|cm3|cm³)|kg/L)', s) or re.match(r'^[^\d]{0,30}?(\d\.\d+)\b', s)
        if not m: continue
        t = re.search(r'at\s*(-?\d+(?:\.\d+)?)\s*°?\s*C', s)
        if t and not 15 <= float(t.group(1)) <= 25: continue
        v = float(m.group(1))
        if 0.2 < v < 6: out.append((v, fonte))
    return out
def grupo(vals, tol):
    best = []
    for v in vals:
        g = [w for w in vals if abs(w - v) <= tol(v)]
        if len(g) > len(best): best = g
    return best
def nist(cas):
    """Tfus e Tboil (°C) do NIST WebBook pelo CAS, ou None."""
    r = R.get('https://webbook.nist.gov/cgi/cbook.cgi?ID=' + cas + '&Units=SI&Mask=4')
    if r is None or r.status_code != 200: return None
    t = re.sub(r'<[^>]+>', '|', r.text); t = re.sub(r'\|[\s|]*\|', '|', t)
    o = {}
    for k, v in re.findall(r'T\|(boil|fus)\|([\d.]+)', t):
        o.setdefault(k, round(float(v.rstrip('.')) - 273.15, 1))
    return o

def experimentais(L, D):
    E = R.load('exp'); N = R.load('nist'); stat = {}
    def tem_estereo(smi):
        ic = inchi_est(mol(smi)); return '/t' in ic or '/b' in ic
    cand = []   # correções propostas que pedem a segunda fonte
    for d in D:
        if 'cid' not in d: continue
        r = L[d['i']]; e = E.get(str(d['cid']))
        if not e: continue
        liberado = d.get('estereo_igual') or not tem_estereo(d['smi'])
        for chave, rotulo, campo, ebul in (('Melting Point', 'pf', 'PF', False), ('Boiling Point', 'pe', 'PE', True)):
            refs = temps(e.get(chave, []), ebul)
            txt = r[campo + 'CARAC']; dbv = R.A.valor(txt) if R.A.valor(txt) is not None else R.A.num(r[campo])
            s = stat.setdefault(rotulo, {'comparaveis': 0, 'ate5': 0, 'diverge': 0, 'sem_ref': 0, 'estereo': 0})
            if dbv is None or not isinstance(dbv, (int, float)): continue
            if not refs: s['sem_ref'] += 1; continue
            if not liberado: s['estereo'] += 1; continue
            g = grupo([v for v, _ in refs], lambda v: 3)
            if len(g) < 2 or len(g) / len(refs) < 0.6: continue     # fontes não concordam entre si
            ref = sorted(g)[len(g) // 2]; s['comparaveis'] += 1
            if abs(dbv - ref) <= 5: s['ate5'] += 1; continue
            s['diverge'] += 1
            d.setdefault('exp', {})[rotulo] = {'banco': dbv, 'ref': ref, 'n': len(g), 'de': len(refs), 'fontes': sorted({f for v, f in refs if abs(v - ref) <= 3})[:4]}
            cand.append((d['i'], rotulo))
        dens_refs = densidades(e.get('Density', []))
        dd = R.A.num(r['DENS_20'])
        if dens_refs and dd and liberado:
            g = grupo([v for v, _ in dens_refs], lambda v: v * 0.02)
            if len(g) >= 3 and len(g) / len(dens_refs) >= 0.7:
                ref = sorted(g)[len(g) // 2]; s = stat.setdefault('dens', {'comparaveis': 0, 'ate3': 0, 'diverge': 0}); s['comparaveis'] += 1
                if abs(dd - ref) / ref <= 0.03: s['ate3'] += 1
                else: s['diverge'] += 1; d.setdefault('exp', {})['dens'] = {'banco': dd, 'ref': ref, 'n': len(g), 'de': len(dens_refs)}
    # segunda fonte (NIST) para PF/PE que seriam corrigidos
    for i, rot in cand:
        cas = L[i]['CAS']
        if cas not in N:
            n = nist(cas) if R.CAS_OK.match(cas or '') else {}
            if n is None: continue
            N[cas] = n
    R.save('nist', N)
    for i, rot in cand:
        x = D[i]['exp'][rot]; n = N.get(L[i]['CAS'], {}).get('fus' if rot == 'pf' else 'boil')
        x['nist'] = n
        if n is None: x['acao'] = 'corrige' if x['n'] >= 3 else 'mantem'          # sem NIST: só com 3 ou mais entradas do PubChem concordando
        elif abs(n - x['ref']) <= 6: x['acao'] = 'corrige'                         # NIST concorda com o PubChem
        elif abs(n - x['banco']) <= 3: x['acao'] = 'mantem'                        # NIST confirma o banco
        else: x['acao'] = 'mantem'                                                 # fontes em conflito
    return stat

if __name__ == '__main__':
    L = R.registros(sys.argv[2])
    if sys.argv[1] == 'estrutura':
        D, esc = estrutura(L); resumo(D)
        R.save('decisao', D); R.save('escolha', esc)
    elif sys.argv[1] == 'exp':
        D = R.load('decisao'); stat = experimentais(L, D); print(json.dumps(stat, indent=1))
        from collections import Counter
        print(Counter((k, v.get('acao')) for d in D for k, v in d.get('exp', {}).items()))
        R.save('decisao', D)
