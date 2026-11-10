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
def linha(r):
    ms=[[num(r['MS%d'%i]),num(r['IMS%d'%i])] for i in range(1,9)]
    return [r['CAS'],r['NCOM'],r['NIUP'],r['NINGLES'],r['FMOL'],num(r['PMOL']),valor(r['PFCARAC']) if valor(r['PFCARAC']) is not None else num(r['PF']),valor(r['PECARAC']) if valor(r['PECARAC']) is not None else num(r['PE']),r['PFCARAC'],r['PECARAC'],r['PFDER'],[m for m in ms if m[0]],r['SMILES'],num(r['SOL_H2O']),num(r['DENS_20']),1 if r['NO_IFRJ'] else 0,desenho(r['SMILES'])]
if __name__=='__main__':
    L=[linha(r) for r in ler(sys.argv[1])]
    json.dump(L,open('analor_bd.json','w',encoding='utf-8'),ensure_ascii=False,separators=(',',':'))
    print(len(L),'compostos')
