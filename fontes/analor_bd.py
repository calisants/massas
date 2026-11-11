"""Converte o DBF do banco Analor (professor) em analor_bd.json.
Uso: python3 analor_bd.py caminho/UNIV1.DBF   (codificação cp1252)
Campos de cada linha: CAS, nome comum, nome IUPAC, nome em inglês, fórmula, massa molar, PF, PE,
PF e PE como texto, derivados (PFDER), picos de MS [[m/z, %],...], SMILES, solubilidade em água, densidade, no IFRJ (SIM/vazio)."""
import struct, json, sys, re
def ler(p):
    d=open(p,'rb').read(); n,hl,rl=struct.unpack('<IHH',d[4:12]); fl=[]; i=32
    while d[i]!=0x0D:
        f=d[i:i+32]; fl.append((f[:11].split(b'\0')[0].decode(),f[16])); i+=32
    for r in range(n):
        rec=d[hl+r*rl:hl+(r+1)*rl]
        if rec[0]==0x2A: continue
        o=1; row={}
        for nm,l in fl: row[nm]=rec[o:o+l].decode('cp1252').strip(); o+=l
        yield row
def num(t):
    try: return float(t) if '.' in t else int(t)
    except ValueError: return None
def valor(t):
    t=t.replace(',','.')
    return num(t) if re.fullmatch(r'-?\d+(\.\d+)?',t) else None
def desenho(smi):
    """Coordenadas 2D calculadas pelo RDKit (1 unidade = 0,1 do comprimento de ligação); o app desenha o SVG."""
    from rdkit import Chem, RDLogger
    from rdkit.Chem import rdDepictor
    RDLogger.DisableLog('rdApp.*')
    m=Chem.MolFromSmiles(smi) if smi else None
    if not m or m.GetNumAtoms()>80: return None
    rdDepictor.SetPreferCoordGen(True); rdDepictor.Compute2DCoords(m); Chem.Kekulize(m,clearAromaticFlags=True)
    c=m.GetConformer(); at=[]
    for a in m.GetAtoms():
        p=c.GetAtomPosition(a.GetIdx()); e=a.GetSymbol()
        at.append([0 if e=='C' and a.GetFormalCharge()==0 else e,round(p.x*10),round(p.y*10),a.GetTotalNumHs() if e!='C' else 0,a.GetFormalCharge()])
    return [at,[[b.GetBeginAtomIdx(),b.GetEndAtomIdx(),int(b.GetBondTypeAsDouble())] for b in m.GetBonds()]]
def grupo_sol(m, grupos, sol, nC):
    """Grupo de solubilidade ESTIMADO pela tabela de grupos do app (a do professor). O banco traz a solubilidade em água em g/100 mL a 25 °C
    (confirmado pelo professor); solúvel = 3 g/100 mL ou mais. O resto vem do grupo funcional e do número de C. Calibrado contra os 110 compostos
    do app (grupos do professor). É estimativa, não medida."""
    from rdkit import Chem
    P=lambda s: m.HasSubstructMatch(Chem.MolFromSmarts(s))
    n=lambda s: len(m.GetSubstructMatches(Chem.MolFromSmarts(s)))
    ac=P('[CX3](=O)[OX2H1]') or P('[CX3](=O)[O-]'); sulf=P('[SX4](=O)(=O)[OX2H1,O-]')
    amina=P('[NX3;H2,H1,H0;!$(NC=[O,N,S]);!$(N=O);!$(N-[O,N]);!$(N-a);!$(N-S);!$(NC#N)][CX4]')
    nitro=P('[N+](=O)[O-]')
    anil=(P('[NX3;H2,H1;!$(NC=O)]c') or P('[NX3;H0;!$(NC=O)](C)(C)c')) and not P('[NX3;H1](c)c') and not (nitro and P('[NX3;H2]c'))
    piri=P('[nX2;r6]')
    ureia=P('[NX3;H2]C(=O)[NX3;H2]')
    eter_puro=P('[OX2]([#6])[#6]') and not P('[OX2H]') and not P('[CX3]=[OX1]') and not P('[#7]') and not P('[SX4]') and not P('[OX2;R;!a]')
    sal=len(Chem.GetMolFrags(m))>1 or any(a.GetSymbol() in ('Na','K','Li','Ca','Mg','Zn','Cu','Fe','Ag','Hg','Pb','Al','Ba') for a in m.GetAtoms())
    poli=(n('[OX2H][CX4]')+n('[CX3](=O)[OX2H1]')+n('[NX3;H2][CX4]'))>=2 or P('[NX3;H2][CX4][CX3](=O)[OX2H1]')
    anidrido=P('[CX3](=O)O[CX3](=O)')
    hasN=P('[#7;!$([N+](=O)[O-]);!$(N=N)]'); hasS=P('[#16]')
    fenol=P('[OX2H]c'); ewg=fenol and n('[N+](=O)[O-]')>=2
    a2=fenol or P('[CX3]=[NX2][OX2H]') or P('[CX3](=O)[NX3][CX3](=O)') or P('[SX4](=O)(=O)[NX3;H1,H2]') or P('[SX2H]c')
    oxi=P('[#8]')
    poli=poli and not (ac and nC>6 and not sal)
    solu = (sol>=3) if sol is not None else None
    if solu is None:
        solu = sal or poli or ureia or ((ac or amina or piri) and nC<=6) or (nC<=5 and oxi) or (nC<=3 and hasN)
    if (eter_puro or anidrido) and not sal: solu=False
    if P('[NX3;H2,H3+][CX4][CX3](=O)[OX2H1,O-]'): return 'S2'
    if anil and not amina: return 'B'
    if solu:
        if ureia: return 'S2'
        if ac and poli and not sal and nC<=6: return 'SA'
        if sal or poli or sulf and not ac: return 'S2' if (sal or poli) else 'SA'
        if ac or sulf: return 'SA'
        if amina or piri: return 'SB'
        return 'S1'
    if ac: return 'A1'
    if fenol: return 'A1' if ewg else 'A2'
    if a2: return 'A2'
    if amina or anil or piri: return 'B'
    if hasN or hasS: return 'MN'
    if P('[F,Cl,Br,I]') and not oxi: return 'I'
    if oxi or P('[CX3]=[CX3]') or P('C#C'): return 'N'
    if P('N=N') and not hasN: return 'N'
    if P('c') and not oxi: return 'I'
    return 'I' if not P('[CX3]=[CX3]') else 'N'
CONF={}
_p=__import__('os').path.join(__import__('os').path.dirname(__file__) or '.','analor_conf.json')
if __import__('os').path.exists(_p): CONF={c['i']:c for c in json.load(open(_p,encoding='utf-8'))['r']}
def cas_valido(c):
    """CAS com formato e dígito verificador certos."""
    if not re.fullmatch(r'\d{2,7}-\d\d-\d',c or ''): return False
    d=c.replace('-',''); return sum(int(x)*(i+1) for i,x in enumerate(reversed(d[:-1])))%10==int(d[-1])
def _fontes(c):
    f=c.get('fontes') or []
    return ' e '.join(f) if f else 'as fontes consultadas'
def aplicar(r,c):
    """Aplica a conferência (analor_conf.json, feita contra PubChem e NCI CACTUS) a uma linha. Devolve [código, texto] ou None.
    1 = fórmula corrigida; 2 = estrutura trocada; 3 = estrutura que faltava, preenchida; 5 = nome/CAS apontam para outro composto."""
    from rdkit import Chem
    from rdkit.Chem import Descriptors
    est=c['est']
    if est=='banco_ok':
        if 'aviso_id' in c:
            return [5,'O nome e o CAS do banco apontam para '+c['aviso_id'][0]+' ('+c['aviso_id'][1]+'), mas a fórmula, a massa e a estrutura do banco são de outro composto. Mantive a estrutura do banco. Confira com o professor qual dos dois vale.']
        return None
    if est=='formula':
        antes=r[4]; r[4]=c['f']; r[5]=c['mw']
        return [1,'A fórmula do banco ('+antes+') não bate com a estrutura ('+c['f']+'). A estrutura está certa, conferida com '+_fontes(c)+'. Uso a fórmula da estrutura.']
    smi=c['smi']; antes=r[12]; fa=r[4]
    r[12]=smi; r[16]=desenho(smi); r[4]=c['f']; r[5]=c['mw']
    if est=='preenchida': return [3,'O banco não traz a estrutura deste composto. Usei a de '+_fontes(c)+' (CID '+str(c.get('cid'))+' no PubChem).']
    return [2,'A estrutura do banco não bate com '+_fontes(c)+'. Usei a estrutura do PubChem (CID '+str(c.get('cid'))+'), que bate com o nome e com a fórmula '+c['f']+'.'+(' A fórmula do banco ('+fa+') também foi corrigida.' if c.get('f_banco') else '')]

_COR_EN=[('incolor',r'colou?rless'),('branco',r'white'),('amarelo',r'yellow'),('laranja',r'orange'),('vermelho',r'\b(?:red|pink|scarlet)'),('marrom',r'brown|\btan\b'),('verde',r'green'),('azul',r'blue'),('violeta',r'violet|purple'),('preto',r'black|dark gr[ae]y')]
def cor_pt(cid):
    """Cor a partir do campo Color/Form do PubChem (ref_cache/cor.json). Fica a cor que aparece em metade ou mais das descrições que citam cor; 4 ou mais cores = ambíguo, sem dado."""
    import re,os
    global _COR
    if '_COR' not in globals():
        _COR=json.load(open('ref_cache/cor.json')) if os.path.exists('ref_cache/cor.json') else {}
    inf=_COR.get(str(cid)) or []
    ent=[];fontes=[]
    for t,f in inf:
        t0=re.split(r'\b(?:turn|turns|becomes|darken|darkens|on exposure|when exposed|changes to)\b',t.lower())[0]
        fam={n for n,rx in _COR_EN if re.search(rx,t0)}
        if fam:ent.append(fam);fontes.append(f)
    if not ent:return None
    cont={n:sum(1 for e in ent if n in e) for n,_ in _COR_EN}
    fam=[n for n,_ in _COR_EN if cont[n]*2>=len(ent)]
    if not fam or len(fam)>3:return None
    if 'incolor' in fam and 'branco' in fam:fam.remove('branco')
    return [' ou '.join(fam),sorted(set(x for x in fontes if x))[:2],inf[0][0][:80]]
def linha(r):
    ms=[[num(r['MS%d'%i]),num(r['IMS%d'%i])] for i in range(1,9)]
    return [r['CAS'],r['NCOM'],r['NIUP'],r['NINGLES'],r['FMOL'],num(r['PMOL']),valor(r['PFCARAC']) if valor(r['PFCARAC']) is not None else num(r['PF']),valor(r['PECARAC']) if valor(r['PECARAC']) is not None else num(r['PE']),r['PFCARAC'],r['PECARAC'],r['PFDER'],[m for m in ms if m[0]],r['SMILES'],num(r['SOL_H2O']),(lambda d:d if d is not None and 0.2<d<6 else None)(num(r['DENS_20'])),1 if r['NO_IFRJ'] else 0,desenho(r['SMILES'])]
if __name__=='__main__':
    sys.path.insert(0,'.')
    import compostos
    from rdkit.Chem import Descriptors
    from rdkit import Chem
    L=[]; vistos=set()
    for r0 in ler(sys.argv[1]):
        k=(r0['CAS'],r0['NCOM'],r0['SMILES'])
        if r0['CAS'] and k in vistos: continue   # registro repetido idêntico
        vistos.add(k); L.append(linha(r0))
    BT={};GT={};FT={}
    ESCOLHA=json.load(open('ref_cache/escolha.json'))
    for ix,r in enumerate(L):
        c=CONF.get(ix); flag=None; corr=[]
        if c:
            assert c['cas']==r[0],(ix,c['cas'],r[0])
            if 'mw_banco' in c and c['est']=='banco_ok': r[5]=c['mw']
            if c['est']!='banco_ok' or 'aviso_id' in c: flag=aplicar(r,c)
            if 'mw_banco' in c: corr.append(['Massa molar',c['mw_banco'],c['mw'],'recalculada pela fórmula'])
            for k,(nome,i1,i2) in {'pf':('Ponto de fusão',6,8),'pe':('Ponto de ebulição',7,9),'dens':('Densidade',14,None)}.items():
                x=(c.get('exp') or {}).get(k)
                if x and x.get('acao')=='corrige':
                    r[i1]=x['ref']
                    if i2: r[i2]=str(x['ref']).rstrip('0').rstrip('.') if '.' in str(x['ref']) else str(x['ref'])
                    corr.append([nome,x['banco'],x['ref'],'PubChem: '+str(x['n'])+' de '+str(x['de'])+' valores concordam'+('; NIST confirma' if x.get('nist') is not None and abs(x['nist']-x['ref'])<=6 else '')])
        m=Chem.MolFromSmiles(r[12]) if r[12] else None
        msalto=1 if (r[5] and any(p[0]>r[5]+4 for p in r[11])) else 0   # pico de MS acima da massa molar (+4 para isótopos)
        if m is None:
            r.append(None)
        else:
            g,b,f=compostos.iv_bands(m)   # bandas de IV esperadas por grupo funcional, com os ajustes de conjugação etc. (as mesmas do resto do app)
            nC=sum(1 for a in m.GetAtoms() if a.GetSymbol()=='C')
            h1=[[x['lo'],x['hi'],x['h'],1 if 'largo' in str(x.get('m','')) else 0] for x in compostos.nmr_h(m)]
            c13=[[x['lo'],x['hi'],x['n']] for x in compostos.nmr_c(m)]
            sub=compostos.subestruturas(m)
            ge=grupo_sol(m,g,r[13],nC)
            r.append([[GT.setdefault(x,len(GT)) for x in g],[BT.setdefault(tuple(x[:5]),len(BT)) for x in b],[FT.setdefault(tuple(x),len(FT)) for x in f]]+[h1,c13,sub,ge,compostos.overtones(m)])
        r.append(flag)                          # r[18]: [código, texto] da conferência
        r.append(msalto)                        # r[19]
        r.append(corr or None)                  # r[20]: dados numéricos corrigidos [campo, antes, depois, fonte]
        r.append(0 if cas_valido(r[0]) else 1)  # r[21]: 1 = o identificador não é um CAS (nem o dígito verificador fecha)
        r.append(cor_pt(ESCOLHA.get(str(ix))))   # r[22]: [cor em português, fontes, texto original do PubChem] ou None
    tab={'b':list(BT),'g':list(GT),'f':list(FT)}
    json.dump({'t':tab,'r':L},open('analor_bd.json','w',encoding='utf-8'),ensure_ascii=False,separators=(',',':'))
    print(len(L),'compostos',len(BT),'bandas distintas')
