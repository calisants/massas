import re, json, sys, os
sys.path.insert(0,".")
from why import WHY
from rearr import REARR
from resumo import RESUMO
from ioni import IONI
from intens import INTS
import arrows as ARWMOD
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
add(10,"CCN(C)C",[(72,None,1,0),(58,[1,2,3,4],None,0),(44,[2,3,4],None,0)])
add(11,"CCCCC(=O)OC",[(87,[2,3,4,5,6,7],None,0),(85,range(0,6),None,0),(74,[3,4,5,6,7],None,0),(57,[0,1,2,3],None,0),(29,[0,1],None,0)])
add(12,"CCCCC=O",[(85,None,4,0),(58,[2,3,4,5],None,0),(57,[0,1,2,3],None,0),(44,[3,4,5],None,0),(29,[4,5],None,0)])
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

for _k,(_t,_s) in REARR.items():
    for _smi,_c in _s: key(_smi)
html=open('template.html',encoding='utf-8').read()
BL=22
thumbs={}
for sm in set(re.findall(r'"[^"\n]*? @([^"\n]+)"',html)):
    thumbs[sm]=svg(sm,120,88)
store.update(thumbs)
ARWD={}
for e in EXD:
    byp={r[0]:r for r in e["rows"]}
    for r in e["rows"]:
        spec=ARWMOD.ARW.get((e["n"],r[0]))
        assert spec is not None,("sem setas nem nota",e["n"],r[0])
        smi=e["smi"] if r[1]==e["M"] else byp[r[1]][5]
        ent={}
        if spec.get("v"):
            ent["v"]=[[lab,ARWMOD.build(smi,mk,rec),rec["t"]] for lab,mk,rec in spec["v"]]
        if spec.get("n"): ent["n"]=spec["n"]
        ent["p"]="íon molecular M+· (m/z %d)"%e["M"] if r[1]==e["M"] else "íon do pico m/z %d"%r[1]
        ARWD[f'{e["n"]}:{r[0]}']=ent
import base64
def _b64(f):
    return "data:image/webp;base64,"+base64.b64encode(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"mech",f),"rb").read()).decode()
_PDF="Do seu PDF: as setas e os anzóis que você copiou do quadro."
_FOTO="Foto do quadro, porque estes passos não estavam no seu PDF."
MECH={
 "1":[[_b64("e1.webp"),_PDF]],
 "2":[[_b64("e2.webp"),_PDF]],
 "3":[[_b64("e3.webp"),_PDF]],
 "4":[[_b64("e4.webp"),_PDF]],
 "5":[[_b64("e5.webp"),"Rascunho a lápis seu, não é do quadro do professor. Atenção: o desenho do m/z 29 está errado. Depois de perder CO (28), o fragmento é CH₃–CH₂⁺ (C₂H₅⁺, m/z 29). O que está desenhado, CH₃–OH₂⁺, teria m/z 33. Confirme com o professor."]],
 "6":[[_b64("e6.webp"),_PDF]],
 "7":[[_b64("e7.webp"),_PDF]],
 "8":[[_b64("e8.webp"),_PDF]],
 "9":[[_b64("e9.webp"),_PDF]],
 "10":[[_b64("e10.webp"),_PDF]],
 "11":[[_b64("e11.webp"),_PDF+" Falta aqui o McLafferty do m/z 87 e do 74."],[_b64("q11.webp"),_FOTO]],
 "12":[[_b64("e12.webp"),_PDF+" Falta aqui o McLafferty do m/z 44 e do 58."],[_b64("q12.webp"),_FOTO]],
}

js="const SVG="+json.dumps(store,ensure_ascii=False)+";\nconst MAPS="+json.dumps(MAPS,ensure_ascii=False)+";\nconst EX="+json.dumps(out,ensure_ascii=False)+";\n"+"const REARR="+json.dumps({f"{k[0]}:{k[1]}":[v[0],[list(x) for x in v[1]]] for k,v in REARR.items()},ensure_ascii=False)+";\n"+"const WHY="+json.dumps({f"{k[0]}:{k[1]}":list(v) for k,v in WHY.items()},ensure_ascii=False)+";\n"+"const INTS="+json.dumps({str(k):dict(sdbs=v["sdbs"],id=v["id"],p={str(m):i for m,i in v["p"].items()}) for k,v in INTS.items()},ensure_ascii=False)+";\n"+"const ARWD="+json.dumps(ARWD,ensure_ascii=False)+";\n"+"const RESUMO="+json.dumps(RESUMO,ensure_ascii=False)+";\nconst IONI="+json.dumps({str(k):[v[0],[list(x) for x in v[1]]] for k,v in IONI.items()},ensure_ascii=False)+";\n"+"const MECH="+json.dumps(MECH,ensure_ascii=False)+";\n"
a=html.index("/* ---------- dados: exercícios"); b=html.index("/* ---------- utilidades")
html=html[:a]+"/* ---------- dados ---------- */\n"+js+"\n"+html[b:]
open(os.environ.get('SAIDA','quebra_cabeca_v3.html'),'w',encoding='utf-8').write(html)
print(len(thumbs),len(MAPS),len(html))
