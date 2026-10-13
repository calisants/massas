import re, json
from rdkit import Chem
from rdkit.Chem.Draw import rdMolDraw2D
src=open('build_app.py',encoding='utf-8').read().split("store = {}")[0]
BL=30
src=src.replace("o.fixedBondLength = 30","o.fixedBondLength = BL")
exec(src)  # svg, EXD

def post(s,w,h):
    s=re.sub(r'<\?xml.*?\?>','',s)
    s=re.sub(r"<rect[^>]*?style='opacity:1\.0;fill:#FFFFFF[^>]*?/>",'',s)
    s=s.replace('#000000','currentColor').replace('#FF0000','var(--lost)').replace('#0000FF','var(--blue)')
    s=re.sub(r"<svg[^>]*>",f'<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" role="img">',s,count=1)
    s=re.sub(r'<!--.*?-->','',s); return re.sub(r'\s+',' ',s).strip()

KEEP=(0,170/255,1/255); LOST=(204/255,0,2/255); AMB=(1,165/255,0)
def mapsvg(smi,keep,h=None,w=210,hh=140):
    m=Chem.MolFromSmiles(smi); n=m.GetNumAtoms()
    d=rdMolDraw2D.MolDraw2DSVG(w,hh); o=d.drawOptions()
    o.clearBackground=False; o.fixedBondLength=30; o.padding=0.12; o.bondLineWidth=2
    o.useBWAtomPalette(); o.addAtomIndices=False; o.highlightRadius=0.5
    ats={};bds={}
    if keep is None: keep=list(range(n))
    for i in range(n): ats[i]=KEEP if i in keep else LOST
    if h is not None: ats[h]=AMB
    for b in m.GetBonds():
        a,c=b.GetBeginAtomIdx(),b.GetEndAtomIdx()
        if (a in keep)!=(c in keep): bds[b.GetIdx()]=AMB
    d.DrawMolecule(m,highlightAtoms=list(ats),highlightAtomColors=ats,highlightBonds=list(bds),highlightBondColors=bds)
    d.FinishDrawing(); s=d.GetDrawingText()
    s=s.replace('#00AA01','var(--keep-soft)').replace('#CC0002','var(--lost-soft)').replace('#FFA500','var(--amber)')
    assert 'var(--keep-soft)' in s
    return post(s,w,hh)

# (ex, pico): (SMILES do pai, índices que ficam, átomo de onde sai H, aproximado?)
P={}
def add(n,smi,items):
    for pico,keep,h,ap in items: P[(n,pico)]=(smi,keep,h,ap)
add(1,"CCc1ccccc1",[(91,range(1,8),None,0),(77,range(2,8),None,0),(65,[2,3,4,5,6],None,1),(51,[2,3,4,5],None,1)])
add(2,"c1ccoc1",[(40,[0,1,4],None,1),(39,[0,1,4],None,1),(29,[2,3],None,1)])
add(3,"C=Cc1ccccc1",[(103,None,0,0),(78,range(2,8),None,0),(77,range(2,8),None,0),(52,[2,3,4,5],None,1),(51,[2,3,4,5],None,1)])
add(4,"O=C(c1ccccc1)c1ccccc1",[(105,range(0,8),None,0),(77,range(2,8),None,0),(51,[2,3,4,5],None,1)])
add(5,"CCC(=O)CC",[(57,[0,1,2,3],None,0),(29,[0,1],None,0),(27,[0,1],None,1)])
add(6,"CCCO",[(59,None,3,0),(42,[0,1,2],None,1),(31,[2,3],None,0)])
add(7,"C1COCCO1",[(58,[1,2,3,4],None,0),(28,[1,4],None,1)])
add(8,"c1ccncc1",[(78,None,0,0),(52,[0,1,2,5],None,0),(51,None,0,0),(50,None,0,0)])
add(9,"CCCC(=O)O",[(73,[1,2,3,4,5],None,1),(71,[0,1,2,3,4],None,0),(60,[2,3,4,5],None,0),(43,[0,1,2],None,0)])
add(10,"CCN(C)C",[(72,None,1,0),(58,[1,2,3,4],None,0),(44,[2,3,4],None,0),(30,[1,2],None,1)])
add(12,"CCCCC=O",[(58,[2,3,4,5],None,1),(57,[0,1,2,3],None,0),(44,[3,4,5],None,0),(43,[0,1,2],None,0),(29,[4,5],None,0)])
# nota: H que sai de átomo único (H·) -> marca o átomo em âmbar
MAPS={}
for (n,p),(smi,keep,h,ap) in P.items():
    MAPS[f"{n}:{p}"]=dict(s=mapsvg(smi,None if keep is None else list(keep),h),a=ap)
# confere que todo pico das linhas tem mapa
for e in EXD:
    for r in e["rows"]: assert (e["n"],r[0]) in P,(e["n"],r[0])

store={}
def key(s):
    if s not in store: store[s]=svg(s)
    return s
out=[]
for e in EXD:
    d=dict(n=e["n"],nome=e["nome"],f=e["f"],M=e["M"],g=e["g"],ok=e["ok"],sug=e["sug"],peaks=e["peaks"],smi=key(e["smi"]),rows=[])
    for r in e["rows"]: d["rows"].append([r[0],r[1],r[2],r[3],r[4],key(r[5]),key(r[6]),r[7],r[8]])
    out.append(d)

html=open('template.html',encoding='utf-8').read()
BL=22
thumbs={}
for sm in set(re.findall(r'"[^"\n]*? @([^"\n]+)"',html)):
    thumbs[sm]=svg(sm,120,88)
store.update(thumbs)
js="const SVG="+json.dumps(store,ensure_ascii=False)+";\nconst MAPS="+json.dumps(MAPS,ensure_ascii=False)+";\nconst EX="+json.dumps(out,ensure_ascii=False)+";\n"
a=html.index("/* ---------- dados: exercícios"); b=html.index("/* ---------- utilidades")
html=html[:a]+"/* ---------- dados ---------- */\n"+js+"\n"+html[b:]
open('/home/claude/quebra_cabeca_v3.html','w',encoding='utf-8').write(html)
print(len(thumbs),len(MAPS),len(html))
