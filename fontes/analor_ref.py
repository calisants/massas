"""Busca no PubChem os dados de referência para conferir o banco Analor (cache em ref_cache/, retomável).
Uso: python3 analor_ref.py base UNIV1.DBF   -> CAS->CID, propriedades e buscas por nome dos registros divergentes
     python3 analor_ref.py exp              -> propriedades experimentais (PF, PE, densidade) dos CIDs escolhidos (ref_cache/escolha.json)
Limite do PubChem: 5 requisições por segundo; aqui ficam ~4,5."""
import json, os, re, sys, time, threading
import requests
from concurrent.futures import ThreadPoolExecutor
H = os.path.dirname(os.path.abspath(__file__))
C = os.path.join(H, 'ref_cache'); os.makedirs(C, exist_ok=True)
PUG = 'https://pubchem.ncbi.nlm.nih.gov/rest/pug'
VIEW = 'https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/%s/JSON?heading=Experimental+Properties'
S = requests.Session()
_lk = threading.Lock(); _last = [0.0]

def get(url, tries=6):
    for t in range(tries):
        with _lk:
            w = _last[0] + 0.22 - time.time()
            if w > 0: time.sleep(w)
            _last[0] = time.time()
        try:
            r = S.get(url, timeout=45)
        except Exception:
            time.sleep(2 * (t + 1)); continue
        if r.status_code in (200, 400, 404): return r
        time.sleep(3 * (t + 1))
    return None

def load(n):
    p = os.path.join(C, n + '.json')
    return json.load(open(p, encoding='utf-8')) if os.path.exists(p) else {}
def save(n, d):
    p = os.path.join(C, n + '.json')
    json.dump(d, open(p + '.tmp', 'w', encoding='utf-8'), ensure_ascii=False); os.replace(p + '.tmp', p)

def registros(dbf):
    """Linhas do DBF sem os registros idênticos repetidos (mesma regra do analor_bd.py)."""
    sys.path.insert(0, H)
    import analor_bd as A
    L = []; vistos = set()
    for r in A.ler(dbf):
        k = (r['CAS'], r['NCOM'], r['SMILES'])
        if r['CAS'] and k in vistos: continue
        vistos.add(k); L.append(r)
    return L

def pool(keys, fn, nome, workers=4):
    d = load(nome); todo = [k for k in keys if k not in d]
    print(nome, 'a buscar:', len(todo), flush=True)
    n = 0
    with ThreadPoolExecutor(workers) as ex:
        for k, v in zip(todo, ex.map(fn, todo)):
            if v is not None: d[k] = v
            n += 1
            if n % 200 == 0: save(nome, d); print(nome, n, '/', len(todo), flush=True)
    save(nome, d); return d

def cids_de_nome(nome):
    from urllib.parse import quote
    r = get(PUG + '/compound/name/' + quote(nome, safe='') + '/cids/JSON')
    if r is None: return None
    if r.status_code != 200: return []
    return r.json().get('IdentifierList', {}).get('CID', [])[:6]

def cactus(q):
    """SMILES do NCI CACTUS (resolvedor independente do PubChem) para um nome ou CAS; '' se não achar."""
    from urllib.parse import quote
    for t in range(2):
        try:
            r = S.get('https://cactus.nci.nih.gov/chemical/structure/' + quote(q, safe='') + '/smiles', timeout=15)
        except Exception:
            continue
        if r.status_code == 404: return ''
        if r.status_code == 200:
            x = r.text.strip().split('\n')[0].strip()
            return '' if (not x or '<' in x) else x
    return None

def props(cids):
    d = load('props'); todo = sorted({str(c) for c in cids} - set(d)); print('props a buscar:', len(todo), flush=True)
    lotes = [todo[i:i + 100] for i in range(0, len(todo), 100)]
    def um(l):
        r = get(PUG + '/compound/cid/' + ','.join(l) + '/property/MolecularFormula,MolecularWeight,SMILES,IUPACName,Title/JSON')
        return None if r is None or r.status_code != 200 else r.json()['PropertyTable']['Properties']
    with ThreadPoolExecutor(4) as ex:
        for l, res in zip(lotes, ex.map(um, lotes)):
            for p in (res or []):
                d[str(p['CID'])] = {'f': p.get('MolecularFormula'), 'mw': float(p['MolecularWeight']) if p.get('MolecularWeight') else None,
                                    'smi': p.get('SMILES') or p.get('ConnectivitySMILES'), 'iupac': p.get('IUPACName'), 't': p.get('Title')}
    save('props', d); return d

def canon(smi, estereo=False):
    from rdkit import Chem
    m = Chem.MolFromSmiles(smi) if smi else None
    return Chem.MolToSmiles(m, isomericSmiles=estereo) if m else None

CAS_OK = re.compile(r'^\d{2,7}-\d\d-\d$')
def cas_valido(c):
    if not CAS_OK.match(c or ''): return False
    d = c.replace('-', ''); return sum(int(x) * (i + 1) for i, x in enumerate(reversed(d[:-1]))) % 10 == int(d[-1])

def base(dbf):
    from rdkit import RDLogger; RDLogger.DisableLog('rdApp.*')
    L = registros(dbf)
    cas = sorted({r['CAS'] for r in L if CAS_OK.match(r['CAS'] or '')})
    dc = pool(cas, cids_de_nome, 'cas')
    props([c for v in dc.values() for c in v])
    P = load('props')
    nomes = set()
    for r in L:
        cs = dc.get(r['CAS'], [])
        s = canon(r['SMILES'])
        if s and any(P.get(str(c)) and canon(P[str(c)]['smi']) == s for c in cs): continue   # CAS e estrutura do banco concordam
        for k in ('NINGLES', 'NIUP'):
            if r[k]: nomes.add(r[k])
    print('nomes a consultar:', len(nomes), flush=True)
    dn = pool(sorted(nomes), cids_de_nome, 'nomes')
    props([c for v in dn.values() for c in v])

def exp_prop(cid):
    r = get(VIEW % cid)
    if r is None: return None
    if r.status_code != 200: return {}
    rec = r.json()['Record']; refs = {x['ReferenceNumber']: x['SourceName'] for x in rec.get('Reference', [])}
    out = {}
    def walk(s):
        for x in s.get('Section', []):
            h = x.get('TOCHeading')
            if h in ('Melting Point', 'Boiling Point', 'Density'):
                for inf in x.get('Information', []):
                    for sm in inf.get('Value', {}).get('StringWithMarkup', []):
                        out.setdefault(h, []).append([sm['String'], refs.get(inf.get('ReferenceNumber'), '')])
            walk(x)
    walk(rec); return out

if __name__ == '__main__':
    if sys.argv[1] == 'base': base(sys.argv[2])
    elif sys.argv[1] == 'exp':
        esc = json.load(open(os.path.join(C, 'escolha.json')))
        pool(sorted({str(c) for c in esc.values() if c}), exp_prop, 'exp')
