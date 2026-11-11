"""Decide, registro a registro, qual dado do banco Analor está certo, comparando com o PubChem (ref_cache/ de analor_ref.py).
Uso: python3 analor_decide.py estrutura UNIV1.DBF   -> ref_cache/decisao.json e ref_cache/escolha.json
     python3 analor_decide.py exp UNIV1.DBF          -> PF, PE e densidade: acrescenta correções em ref_cache/decisao.json
A decisão da estrutura é uma votação entre: SMILES do banco (2 votos), CAS no PubChem (2), nome em inglês e nome IUPAC no PubChem (1 cada),
mais 1 voto para quem bate com a fórmula do banco e 1 para quem bate com a massa molar do banco."""
import json, os, re, sys
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, H)
import analor_ref as R
import analor_bd as A
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

_CACHE = {k: R.load(k) for k in ('cas', 'props', 'nomes')}
def pontuar(r, CX=None):
    """Votação entre as estruturas candidatas de um registro. Devolve (ranking, candidatos)."""
    dc, P, dn = _CACHE['cas'], _CACHE['props'], _CACHE['nomes']
    pmol = A.num(r['PMOL']); fdb = r['FMOL']; mdb = mol(r['SMILES']); cand = {}
    nome = (r['NCOM'] + ' ' + r['NINGLES']).upper()
    def add(m, smi, parte, v, cid=None, ident=None):
        c = cand.setdefault(camada(m), {'p': {}, 'smi': {}, 'cids': [], 'm': m})
        c['p'][parte] = v; c['smi'].setdefault(ident or ('db' if cid is None else str(cid)), smi)
        if cid is not None and cid not in c['cids']: c['cids'].append(cid)
    if mdb: add(mdb, r['SMILES'], 'smiles', 1)
    for cid in dc.get(r['CAS'], []):
        p = P.get(str(cid)); m = mol(p['smi']) if p else None
        if m: add(m, p['smi'], 'cas', 1, cid)
    for k, parte, v in (('NINGLES', 'nome_en', 1.5), ('NIUP', 'nome_iupac', 0.5)):
        for cid in dn.get(r[k], []) if r[k] else []:
            p = P.get(str(cid)); m = mol(p['smi']) if p else None
            if m: add(m, p['smi'], parte, v, cid)
    if CX:
        for k, parte, v in (('NINGLES', 'cx_nome', 1.5), ('CAS', 'cx_cas', 1)):
            smi = CX.get(r[k]) if r[k] else None; m = mol(smi) if smi else None
            if m: add(m, smi, parte, v, ident=parte)
    hidr = bool(re.search(r'HIDRAT|IDRATO|IDRATAD|HYDRAT', nome)); anid = bool(re.search(r'ANIDR|ANHYDR', nome))
    for c in cand.values():
        m = c['m']; c['f'] = rdMolDescriptors.CalcMolFormula(m); c['mw'] = Descriptors.MolWt(m)
        if fdb and elem(c['f']) == elem(fdb): c['p']['formula'] = 1
        if pmol and abs(c['mw'] - pmol) <= 0.35: c['p']['mw'] = 1
        agua = '.O' in Chem.MolToSmiles(m) or Chem.MolToSmiles(m).startswith('O.') or Chem.MolToSmiles(m) == 'O'
        if (hidr and agua) or (anid and not agua and (hidr or True) and not hidr): c['p']['hidrato'] = 1
        c['tot'] = sum(c['p'].values())
    return sorted(cand.items(), key=lambda kv: -kv[1]['tot']), cand

COM_ESTEREO = re.compile(r'\b(D|L|DL|CIS|TRANS|R|S)\b|\(\+\)|\(-\)|[(][RS][)]', re.I)
def escolhe_cid(c, r, mdb):
    cids = c['cids']
    if not cids: return None
    if mdb is not None:
        for ci in cids:
            if inchi_est(mol(c['smi'][str(ci)])) == inchi_est(mdb): return ci
    if COM_ESTEREO.search(r['NCOM'] + ' ' + r['NINGLES']):
        for ci in cids:
            if re.search(r'[@/\\]', c['smi'][str(ci)]): return ci
    return cids[0]

def dc_cas(cas):
    """Nome e fórmula (PubChem) do que o CAS do banco aponta, para avisar quando o CAS é de outro composto."""
    P = _CACHE['props']; v = _CACHE['cas'].get(cas, [])
    return [P[str(v[0])].get('t'), P[str(v[0])].get('f')] if v and str(v[0]) in P else None

def cand_all(r, CX):
    return [c for _, c in pontuar(r, CX)[0]]

def estrutura(L):
    CX = R.load('cactus'); D = []; esc = {}
    pre = [pontuar(r) for r in L]
    duvida = []
    for k, (rank, cand) in enumerate(pre):
        r = L[k]
        ok = rank and 'smiles' in rank[0][1]['p'] and rank[0][1]['tot'] - (rank[1][1]['tot'] if len(rank) > 1 else 0) >= 2 and 'formula' in rank[0][1]['p']
        if not ok: duvida.append(k)
    print('registros em dúvida (consulta ao CACTUS):', len(duvida), flush=True)
    consultas = sorted({L[k][c] for k in duvida for c in ('NINGLES', 'CAS') if L[k][c] and (c == 'NINGLES' or R.CAS_OK.match(L[k][c]))})
    CX = R.pool(consultas, R.cactus, 'cactus', workers=8)
    for i, r in enumerate(L):
        rank, cand = pontuar(r, CX if i in duvida else None)
        pmol = A.num(r['PMOL']); fdb = r['FMOL']; mdb = mol(r['SMILES'])
        d = {'i': i, 'cas': r['CAS']}
        if not rank: d.update(est='sem_dado'); D.append(d); continue
        top = rank[0][1]; seg = rank[1][1]['tot'] if len(rank) > 1 else 0
        d['partes'] = top['p']; d['votos'] = round(top['tot'], 1); d['concorrente'] = rank[1][1]['f'] if len(rank) > 1 else None
        nome_ev = lambda c: sum(v for k, v in c['p'].items() if k in ('nome_en', 'nome_iupac', 'cx_nome'))
        cas_ev = lambda c: sum(v for k, v in c['p'].items() if k in ('cas', 'cx_cas'))
        if top['tot'] - seg < 0.5 and len(rank) > 1 and rank[1][1]['tot'] == top['tot'] and elem(top['f']) == elem(rank[1][1]['f']):
            a, b = top, rank[1][1]
            if (nome_ev(b), cas_ev(b)) > (nome_ev(a), cas_ev(a)): top = b
            if (nome_ev(b), cas_ev(b)) != (nome_ev(a), cas_ev(a)): seg = -1   # desempate: nome pesa mais que CAS, mesma fórmula
        if top['tot'] - seg < 0.5 and seg != -1:
            d.update(est='indeciso', f_cand=[top['f'], rank[1][1]['f']], smi_cand=[next(iter(top['smi'].values())), next(iter(rank[1][1]['smi'].values()))]); D.append(d); continue
        if 'smiles' not in top['p'] and mdb is not None and fdb:
            fs = rdMolDescriptors.CalcMolFormula(mdb); mws = Descriptors.MolWt(mdb)
            if elem(fs) == elem(fdb) and pmol and abs(mws - pmol) <= 0.35 and elem(top['f']) != elem(fdb):
                # fórmula, massa e SMILES do banco concordam entre si; só nome/CAS apontam outra coisa: mantém a estrutura e avisa
                dbc = next((c for c in cand_all(r, CX if i in duvida else None) if 'smiles' in c['p']), None)
                if dbc is not None:
                    d['aviso_id'] = [(dc_cas(r['CAS']) or [top['smi'] and '', top['f']])[0] or '', top['f']]
                    top = dbc
        if 'smiles' in top['p']:
            smi = top['smi']['db']; cid = escolhe_cid(top, r, mdb)
            d['est'] = 'banco_ok' if (not fdb or elem(top['f']) == elem(fdb)) else 'formula'
            d['estereo_igual'] = bool(cid is not None and inchi_est(mol(top['smi'][str(cid)])) == inchi_est(mdb))
        else:
            cid = escolhe_cid(top, r, None)
            smi = top['smi'][str(cid)] if cid is not None else next(iter(top['smi'].values()))
            d['est'] = 'troca' if mdb is not None else 'preenchida'; d['estereo_igual'] = cid is not None
        d.update(smi=smi, f=top['f'], mw=round(top['mw'], 2), cid=cid)
        if 'cas' not in top['p'] and r['CAS'] and dc_cas(r['CAS']):
            d['cas_alt'] = dc_cas(r['CAS'])
        if pmol is not None and abs(top['mw'] - pmol) > 0.35: d['mw_banco'] = pmol
        if fdb and elem(top['f']) != elem(fdb): d['f_banco'] = fdb
        D.append(d)
        if cid is not None: esc[str(i)] = cid
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
            txt = r[campo + 'CARAC']; dbv = A.valor(txt) if A.valor(txt) is not None else A.num(r[campo])
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
        dd = A.num(r['DENS_20'])
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

FONTE = {'cas': 'o CAS no PubChem', 'cx_cas': 'o CAS no NCI CACTUS', 'nome_en': 'o nome em inglês no PubChem', 'cx_nome': 'o nome em inglês no NCI CACTUS', 'nome_iupac': 'o nome IUPAC no PubChem'}
def exportar(L, D):
    """Grava analor_conf.json: só o que a conferência mudou ou avisou (o analor_bd.py aplica isto ao gerar o banco)."""
    out = []
    for d in D:
        c = {k: d[k] for k in ('i', 'cas', 'est', 'smi', 'f', 'mw', 'f_banco', 'mw_banco', 'cid', 'aviso_id', 'exp') if k in d}
        c['fontes'] = [FONTE[k] for k in d.get('partes', {}) if k in FONTE]
        if d['est'] == 'banco_ok' and not any(k in c for k in ('mw_banco', 'aviso_id', 'exp')): continue
        if d['est'] == 'banco_ok': c.pop('smi', None)
        out.append(c)
    json.dump({'data': '11/11/2026', 'r': out}, open(os.path.join(H, 'analor_conf.json'), 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
    print('analor_conf.json:', len(out), 'registros')

if __name__ == '__main__':
    L = R.registros(sys.argv[2])
    if sys.argv[1] == 'estrutura':
        D, esc = estrutura(L); resumo(D)
        R.save('decisao', D); R.save('escolha', esc)
    elif sys.argv[1] == 'exportar':
        exportar(L, R.load('decisao'))
    elif sys.argv[1] == 'exp':
        D = R.load('decisao'); stat = experimentais(L, D); print(json.dumps(stat, indent=1))
        from collections import Counter
        print(Counter((k, v.get('acao')) for d in D for k, v in d.get('exp', {}).items()))
        R.save('decisao', D)
