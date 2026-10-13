import re, json
from rdkit import Chem
from rdkit.Chem.Draw import rdMolDraw2D

def svg(smi, w=170, h=120):
    m = Chem.MolFromSmiles(smi)
    if m is None:
        m = Chem.MolFromSmiles(smi, sanitize=False)
        if m is None:
            raise ValueError(smi)
        m.UpdatePropertyCache(strict=False)
    d = rdMolDraw2D.MolDraw2DSVG(w, h)
    o = d.drawOptions()
    o.clearBackground = False
    o.fixedBondLength = 30
    o.padding = 0.12
    o.bondLineWidth = 2
    o.annotationFontScale = 0.8
    d.DrawMolecule(m)
    d.FinishDrawing()
    s = d.GetDrawingText()
    s = re.sub(r'<\?xml.*?\?>', '', s)
    s = re.sub(r"<rect[^>]*?style='opacity:1\.0;fill:#FFFFFF[^>]*?/>", '', s)
    s = s.replace('#000000', 'currentColor').replace('#FF0000', 'var(--lost)').replace('#0000FF', 'var(--blue)')
    s = re.sub(r"<svg[^>]*>", f'<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" role="img">', s, count=1)
    s = re.sub(r'<!--.*?-->', '', s)
    s = re.sub(r'\s+', ' ', s)
    return s.strip()

# row: (pico, de, ficou, saiu, ligacao, smiles_ficou, smiles_saiu, cap_ficou, cap_saiu)
EXD = [
 dict(n=1, nome="etilbenzeno", f="C8H10", M=106, g="alquilbenzeno", ok=False, sug=False, smi="CCc1ccccc1", peaks=[106,91,77,65,51], rows=[
  (91,106,"C7H7+ (benzila/tropílio), pico base","CH3·","ligação benzílica, entre o CH2 e o CH3","[CH2+]c1ccccc1","[CH3]","C7H7+","CH3·"),
  (77,106,"C6H5+","C2H5·","ligação anel–CH2","[c+]1ccccc1","C[CH2]","C6H5+","C2H5·"),
  (65,91,"C5H5+","CH≡CH","o anel rearranja e perde acetileno","[CH+]1C=CC=C1","C#C","C5H5+","C2H2"),
  (51,77,"C4H3+","CH≡CH","o anel rearranja e perde acetileno","C#CC=[CH+]","C#C","C4H3+","C2H2")]),
 dict(n=2, nome="furano", f="C4H4O", M=68, g="heteroaromático com O", ok=False, sug=False, smi="c1ccoc1", peaks=[68,40,39,29], rows=[
  (40,68,"C3H4+·","CO","anel abre e sai CO","C#CC","[C-]#[O+]","C3H4+·","CO"),
  (39,68,"C3H3+ (ciclopropenil)","·CHO","anel abre ao lado do O e sai C(H)=O","[CH+]1C=C1","[CH]=O","C3H3+","·CHO"),
  (29,68,"CHO+","C3H3·","mesmo anel aberto, carga no CHO","C#[O+]","C#C[CH2]","CHO+","C3H3·")]),
 dict(n=3, nome="estireno", f="C8H8", M=104, g="alceno ligado a anel", ok=False, sug=False, smi="C=Cc1ccccc1", peaks=[104,103,78,77,52,51], rows=[
  (103,104,"C8H7+","H·","H sai da molécula","C=[C+]c1ccccc1","[H]","C8H7+","H·"),
  (78,104,"C6H6+·","CH≡CH","a vinila sai como acetileno","c1ccccc1","C#C","C6H6+·","C2H2"),
  (77,104,"C6H5+","CH2=CH·","ligação anel–vinila (ou 78 − H·)","[c+]1ccccc1","C=[CH]","C6H5+","C2H3·"),
  (52,78,"C4H4+·","CH≡CH","o anel perde acetileno","C=CC#C","C#C","C4H4+·","C2H2"),
  (51,77,"C4H3+","CH≡CH","o anel perde acetileno","C#CC=[CH+]","C#C","C4H3+","C2H2")]),
 dict(n=4, nome="benzofenona", f="C13H10O", M=182, g="cetona aromática", ok=False, sug=False, smi="O=C(c1ccccc1)c1ccccc1", peaks=[182,105,77,51], rows=[
  (105,182,"C6H5–C≡O+ (benzoíla), pico base","C6H5·","clivagem α: ligação C(=O)–anel","[O+]#Cc1ccccc1","[c]1ccccc1","C6H5CO+","C6H5·"),
  (77,105,"C6H5+","CO","o íon acila perde CO","[c+]1ccccc1","[C-]#[O+]","C6H5+","CO"),
  (51,77,"C4H3+","CH≡CH","o anel perde acetileno","C#CC=[CH+]","C#C","C4H3+","C2H2")]),
 dict(n=5, nome="3-pentanona", f="C5H10O", M=86, g="cetona alifática", ok=False, sug=False, smi="CCC(=O)CC", peaks=[86,57,29,27], rows=[
  (57,86,"CH3CH2C≡O+ (propanoíla), pico base","CH3CH2·","clivagem α: ligação C(=O)–CH2","CCC#[O+]","C[CH2]","C2H5CO+","C2H5·"),
  (29,57,"C2H5+","CO","o íon acila perde CO","C[CH2+]","[C-]#[O+]","C2H5+","CO"),
  (27,29,"C2H3+","H2","perda de H2 do etila","C=[CH+]","[H][H]","C2H3+","H2")]),
 dict(n=6, nome="1-propanol", f="C3H8O", M=60, g="álcool primário", ok=True, sug=False, smi="CCCO", peaks=[60,59,42,31], rows=[
  (59,60,"C3H7O+","H·","H do O–H","CCC[O+]","[H]","C3H7O+","H·"),
  (42,60,"C3H6+·","H2O","H de um C do outro lado vai para o O; sai água","CC=C","O","C3H6+·","H2O"),
  (31,60,"CH2=OH+, pico base","CH3CH2·","clivagem α: ligação C–C vizinha ao carbono do OH","C=[OH+]","C[CH2]","CH2OH+","C2H5·")]),
 dict(n=7, nome="1,4-dioxano", f="C4H8O2", M=88, g="éter cíclico", ok=True, sug=False, smi="C1COCCO1", peaks=[88,58,28], rows=[
  (58,88,"C3H6O+·","CH2O","o anel abre ao lado de um O e sai CH2=O","[CH2]C[O+]=C","C=O","C3H6O+·","CH2O"),
  (28,58,"C2H4+·, pico base","CH2O","sai o segundo CH2=O","C=C","C=O","C2H4+·","CH2O")]),
 dict(n=8, nome="piridina", f="C5H5N", M=79, g="heteroaromático com N", ok=True, sug=False, smi="c1ccncc1", peaks=[79,78,52,51,50], rows=[
  (78,79,"C5H4N+","H·","H sai do anel","[c+]1ccncc1","[H]","C5H4N+","H·"),
  (52,79,"C4H4+·","HC≡N","o anel abre ao lado do N e sai H–C≡N","C=CC#C","C#N","C4H4+·","HCN"),
  (51,52,"C4H3+","H·","perda de H","C#CC=[CH+]","[H]","C4H3+","H·"),
  (50,51,"C4H2+·","H·","perda de H","C#CC#C","[H]","C4H2+·","H·")]),
 dict(n=9, nome="ácido butanoico", f="C4H8O2", M=88, g="ácido carboxílico", ok=True, sug=False, smi="CCCC(=O)O", peaks=[88,73,71,60,43], rows=[
  (73,88,"C3H5O2+","CH3·","perde CH3 da ponta; o O fecha um anel de 4 membros (lousa)","OC1=[O+]CC1","[CH3]","C3H5O2+","CH3·"),
  (71,88,"CH3CH2CH2C≡O+","HO·","clivagem α: ligação C(=O)–OH","CCCC#[O+]","[OH]","C4H7O+","HO·"),
  (60,88,"CH2=C(OH)2+·, pico base","CH2=CH2","McLafferty: H do carbono γ vai para o O do C=O","C=C(O)O","C=C","C2H4O2+·","C2H4"),
  (43,71,"C3H7+","CO","o íon acila perde CO","CC[CH2+]","[C-]#[O+]","C3H7+","CO")]),
 dict(n=10, nome="N,N-dimetiletilamina", f="C4H11N", M=73, g="amina terciária", ok=False, sug=True, smi="CCN(C)C", peaks=[73,72,58,44,30], rows=[
  (72,73,"C4H10N+","H·","H sai do carbono ao lado do N","CC=[N+](C)C","[H]","C4H10N+","H·"),
  (58,73,"(CH3)2N+=CH2, pico base","CH3·","clivagem α: o CH3 do etila sai e o N fica com a carga","C=[N+](C)C","[CH3]","C3H8N+","CH3·"),
  (44,73,"(CH3)2N+","CH3CH2·","ligação N–CH2 do etila (sugestão minha)","C[N+]C","C[CH2]","C2H6N+","C2H5·"),
  (30,58,"CH2=NH2+","CH2=CH2","a partir do 58 (sugestão minha)","C=[NH2+]","C=C","CH4N+","C2H4")]),
 dict(n=12, nome="valeraldeído (pentanal)", f="C5H10O", M=86, g="aldeído alifático", ok=False, sug=True, smi="CCCCC=O", peaks=[86,58,57,44,43,41,29], rows=[
  (58,86,"C3H6O+·","CH2=CH2","perde eteno (sugestão minha)","CCC=O","C=C","C3H6O+·","C2H4"),
  (57,86,"C4H9+","·CHO","sai o ·CHO (29), sobra o butila","CCC[CH2+]","[CH]=O","C4H9+","·CHO"),
  (44,86,"CH2=CH–OH+·, pico base","CH2=CH–CH3","McLafferty: H do carbono γ vai para o O; sai propeno","C=CO","C=CC","C2H4O+·","C3H6"),
  (43,86,"C3H7+","CH2=CH–O·","sai CH2=CH–O· (sugestão minha)","CC[CH2+]","C=C[O]","C3H7+","C2H3O·"),
  (29,86,"CHO+","C4H9·","carga no CHO (sugestão minha)","C#[O+]","CCC[CH2]","CHO+","C4H9·")]),
]

store = {}
def key(s):
    if s not in store:
        store[s] = svg(s)
    return s

out = []
for e in EXD:
    d = dict(n=e["n"], nome=e["nome"], f=e["f"], M=e["M"], g=e["g"], ok=e["ok"], sug=e["sug"], peaks=e["peaks"], smi=key(e["smi"]), rows=[])
    for r in e["rows"]:
        d["rows"].append([r[0], r[1], r[2], r[3], r[4], key(r[5]), key(r[6]), r[7], r[8]])
    out.append(d)

js = "const SVG=" + json.dumps(store, ensure_ascii=False) + ";\nconst EX=" + json.dumps(out, ensure_ascii=False) + ";\n"
html = open('/home/claude/quebra_cabeca.html', encoding='utf-8').read()
start = html.index("/* ---------- dados: exercícios")
end = html.index("/* ---------- utilidades")
html = html[:start] + "/* ---------- dados: exercícios (linha: pico, vem de, ficou, saiu, ligação, estrutura ficou, estrutura saiu, legenda ficou, legenda saiu) ---------- */\n" + js + "\n" + html[end:]
open('/home/claude/quebra_cabeca_v2.html', 'w', encoding='utf-8').write(html)
print(len(store), len(html))
