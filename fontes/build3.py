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
            ent["v"]=[[lab,ARWMOD.build(smi,mk,rec),rec["t"],rec.get("e",[])] for lab,mk,rec in spec["v"]]
        if spec.get("n"): ent["n"]=spec["n"]
        ent["p"]="íon molecular M+· (m/z %d)"%e["M"] if r[1]==e["M"] else "íon do pico m/z %d"%r[1]
        ARWD[f'{e["n"]}:{r[0]}']=ent
import base64
def _b64(f):
    return "data:image/webp;base64,"+base64.b64encode(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"mech",f),"rb").read()).decode()
_PDF="Do seu PDF: as setas e os anzóis que você copiou do quadro."
_FOTO="Foto do quadro, porque estes passos não estavam no seu PDF."

SL=[
("Benzamida: o exemplo-modelo do professor (slide 3)","M+• 121 (60%) → −•NH₂ → 105 (90%) → −CO → 77 (100%, pico base). Também 121 → −C₆H₅• → 44 (12%). Repare: o elétron sozinho sai do O (par livre), a ligação C–N vira a 2ª ligação e o NH₂ sai como radical.",3),
("Como representar íons e setas (slides 13 e 14)","A forma mais correta do íon é sem localizar a carga (A). Para entender o mecanismo, usamos as formas B e C, com carga e elétron sozinho localizados. Quebra homolítica = seta de meia ponta (1 elétron). Dá para desenhar os dois elétrons (I) ou só um (II), para evitar confusão. Quebra heterolítica = seta de duas pontas (par de elétrons): cátion + radical (III) ou cátion + molécula neutra (IV).",14),
("Anel saturado com ramificação e retro-Diels-Alder (slide 15)","Anel saturado ramificado: a carga fica no anel e a ramificação sai como radical neutro. Anel insaturado (ciclo-hexeno): retro-Diels-Alder, abre e solta eteno (28).",15),
("Íon tropílio, m/z 91 (slide 16)","Em alquilbenzeno a quebra é na ligação β ao anel, dando o íon benzila. O slide diz: benzila, estabilizado por ressonância, ou, como é mais provável, tropílio (anel de 7, aromático). Os dois têm m/z 91.",16),
("Rearranjo de McLafferty (slide 17)","Sai alqueno neutro (RHC=CH₂) e o íon fica como enol, com Y = H, R, OH ou OR/NH₂. O elétron sozinho aparece no carbono depois do H pular.",17),
("Hidrocarbonetos: anel saturado (slide 19)","Anel saturado aumenta a intensidade do M+•. O anel perde fragmentos de 2 carbonos: C₂H₄ (28) e C₂H₅ (29). Ciclo-hexano: M 84, base 56 (perde C₂H₄).",19),
("Álcoois primários, secundários e terciários (slides 22 e 23)","M+• pequeno em primário e secundário e quase ausente em terciário. Quebra da ligação C–C vizinha ao O. Primário: +CH₂–OH (31). Secundário: +CHR–OH (45, 59, 73…). Terciário: +CRR'–OH (59, 73, 87…).",22),
("Álcoois: perda de água e álcool benzílico (slide 24)","M−18 aparece às vezes forte, mais fácil em álcool primário. O slide interpreta por perda de H (I); e água junto com alqueno (II). Álcool benzílico: M+• 108 → −H• → 107 → −CO → 79 → −H₂ → 77.",24),
("Álcool benzílico passo a passo (slide 25)","Mecanismo do professor: 108 → 107 (sai H•), 107 → 79 (sai CO, com o anel de 7 do tropílio-OH), 79 → 77 (sai H₂).",25),
("Cetonas (slide 27)","M+• em geral bem intenso. As quebras principais são das ligações C–C vizinhas ao O (α). Ciclo-hexanona (M 98): abre o anel, depois sai C₂H₄ + CO, dando 55 e 42.",27),
("Ácidos carboxílicos (slide 28)","M+• pouco intenso, mas normalmente observado. Pico característico em m/z 60 pelo McLafferty (ácido decanoico, M 172).",28),
("Exemplo de prova: benzaldeído (slide 35)","Primeiro IV (IDH, bandas), depois MS confirma: M+• 106 → −H• → 105 → −CO → 77 → −HC≡CH → 51.",35),
("Isômeros: o-hidroxibenzaldeído (slide 37)","Orto: 122 → −H• → 121 → −CO → 93 → −OH• → 76. Há também a via da água: pela proximidade entre CHO e OH sai H₂O (−18), dando 104, e depois −CO → 76. Depois 93 → 65 → 39.",37),
("Isômero meta (slide 39)","Sem perda de água, porque o aldeído está longe da hidroxila: 122 → 121 → 93 → 65 → 39.",39),
("Isômero para (slide 41)","Igual ao meta, sem perda de água pelo afastamento entre aldeído e hidroxila: 122 → 121 → 93 → 65 → 39.",41),
("Ácido benzoico (slide 43)","122 → −OH• → 105 → −CO → 77 → −HC≡CH → 51. Não perde água.",43),
("Ácido salicílico, orto (slide 45)","Perde H₂O (138 → 120) pela proximidade entre COOH e OH, depois −CO → 92 → 64 → 38.",45),
]
SLIMG={n:_b64(f"../slides/s{n}.webp") for n in (3,14,15,16,17,19,22,24,25,27,28,35,37,39,41,43,45)}

_FOLHA="Folha do professor (PDF “Mecanismos – Anal.Org. II”), recortada."
MECH={
 "1":[[_b64("f1.webp"),_FOLHA+" Ele termina no anel de 7 (tropílio)."],[_b64("e1.webp"),_PDF]],
 "2":[[_b64("f2.webp"),_FOLHA],[_b64("e2.webp"),_PDF]],
 "3":[[_b64("f3.webp"),_FOLHA+" Caminho do 103 → 77 → 51."],[_b64("f4.webp"),_FOLHA+" Caminho do 78."],[_b64("e3.webp"),_PDF]],
 "4":[[_b64("f5.webp"),_FOLHA],[_b64("e4.webp"),_PDF]],
 "5":[[_b64("f6.webp"),_FOLHA+" 86 → perde ·CH₂CH₃ → 57 → perde CO → 29 (CH₃–CH₂⁺)."],[_b64("e5.webp"),"Rascunho a lápis seu, de antes de a folha do professor chegar. O m/z 29 desenhado aqui está errado (CH₃–OH₂⁺ teria m/z 33). O certo, como na folha do professor acima, é CH₃–CH₂⁺ (m/z 29)."]],
 "6":[[_b64("f7.webp"),_FOLHA+" Pico 59: sai o H do O–H."],[_b64("f8.webp"),_FOLHA+" Pico 42 (perda de água). Atenção: a folha escreve m/z = 15 no fim, mas 60 − 18 = 42, e o fragmento desenhado (C₃H₆⁺·) tem 42. Parece erro de digitação; vale confirmar."],[_b64("f9.webp"),_FOLHA+" Pico 31."],[_b64("e6.webp"),_PDF]],
 "7":[[_b64("f10.webp"),_FOLHA],[_b64("e7.webp"),_PDF]],
 "8":[[_b64("f11.webp"),_FOLHA],[_b64("e8.webp"),_PDF]],
 "9":[[_b64("f12.webp"),_FOLHA+" Pico 73: o O fecha um anel de 4 membros quando sai CH₃."],[_b64("f13.webp"),_FOLHA+" Picos 71 e 43."],[_b64("f14.webp"),_FOLHA+" Pico 60 (McLafferty)."],[_b64("e9.webp"),_PDF]],
 "10":[[_b64("f15.webp"),_FOLHA+" Pico 58."],[_b64("f16.webp"),_FOLHA+" Pico 72."],[_b64("f17.webp"),_FOLHA+" Pico 44."],[_b64("e10.webp"),_PDF]],
 "11":[[_b64("f18.webp"),_FOLHA+" Picos 85, 57 e 29."],[_b64("f19.webp"),_FOLHA+" Pico 87."],[_b64("f20.webp"),_FOLHA+" Pico 74 (McLafferty)."],[_b64("e11.webp"),_PDF+" Falta aqui o McLafferty do m/z 87 e do 74."],[_b64("q11.webp"),_FOTO]],
 "12":[[_b64("e12.webp"),_PDF+" Falta aqui o McLafferty do m/z 44 e do 58. A folha do professor não tem o Ex. 12."],[_b64("q12.webp"),_FOTO]],
}

js="const SVG="+json.dumps(store,ensure_ascii=False)+";\nconst MAPS="+json.dumps(MAPS,ensure_ascii=False)+";\nconst EX="+json.dumps(out,ensure_ascii=False)+";\n"+"const REARR="+json.dumps({f"{k[0]}:{k[1]}":[v[0],[list(x) for x in v[1]]] for k,v in REARR.items()},ensure_ascii=False)+";\n"+"const WHY="+json.dumps({f"{k[0]}:{k[1]}":list(v) for k,v in WHY.items()},ensure_ascii=False)+";\n"+"const INTS="+json.dumps({str(k):dict(sdbs=v["sdbs"],id=v["id"],p={str(m):i for m,i in v["p"].items()}) for k,v in INTS.items()},ensure_ascii=False)+";\n"+"const ARWD="+json.dumps(ARWD,ensure_ascii=False)+";\n"+"const RESUMO="+json.dumps(RESUMO,ensure_ascii=False)+";\nconst IONI="+json.dumps({str(k):[v[0],[list(x) for x in v[1]]] for k,v in IONI.items()},ensure_ascii=False)+";\n"+"const MECH="+json.dumps(MECH,ensure_ascii=False)+";\n"+"const SLD="+json.dumps([[t,x,SLIMG[n]] for t,x,n in SL],ensure_ascii=False)+";\n"
a=html.index("/* ---------- dados: exercícios"); b=html.index("/* ---------- utilidades")
html=html[:a]+"/* ---------- dados ---------- */\n"+js+"\n"+html[b:]
open(os.environ.get('SAIDA','quebra_cabeca_v3.html'),'w',encoding='utf-8').write(html)
print(len(thumbs),len(MAPS),len(html))
