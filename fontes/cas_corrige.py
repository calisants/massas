"""Acha CAS inválido ou ausente no banco Analor e tenta corrigir pelo PubChem (confere a fórmula)."""
import json,re,urllib.request,urllib.parse,time,sys
rows=json.load(open('analor_bd.json'))['r']
esc=json.load(open('ref_cache/escolha.json'))
def ok(c):
    m=re.fullmatch(r'(\d{2,7})-(\d{2})-(\d)',c or '')
    if not m:return False
    dg=(m.group(1)+m.group(2))[::-1]
    return sum((i+1)*int(x) for i,x in enumerate(dg))%10==int(m.group(3))
def get(u):
    for t in range(3):
        try:return json.load(urllib.request.urlopen(u,timeout=25))
        except Exception as e:time.sleep(1.5)
    return None
def lev(a,b):
    d=list(range(len(b)+1))
    for i,x in enumerate(a,1):
        p=d[:];d[0]=i
        for j,y in enumerate(b,1):d[j]=min(p[j]+1,d[j-1]+1,p[j-1]+(x!=y))
    return d[-1]
if __name__=='__main__':
    alvo=[i for i,r in enumerate(rows) if not ok(r[0])]
    saida={}
    for i in alvo:
        r=rows[i];cid=esc.get(str(i));cands=[]
        if not cid and r[3]:
            j=get('https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/%s/property/MolecularFormula/JSON'%urllib.parse.quote(r[3]))
            if j:
                ps=[p for p in j['PropertyTable']['Properties'] if p.get('MolecularFormula')==r[4]]
                if len(ps)==1:cid=ps[0]['CID']
        if cid:
            pf=get('https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/%s/property/MolecularFormula/JSON'%cid)
            form=pf['PropertyTable']['Properties'][0].get('MolecularFormula') if pf else None
            sy=get('https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/%s/synonyms/JSON'%cid)
            if sy:
                cands=[s for s in sy['InformationList']['Information'][0].get('Synonym',[]) if re.fullmatch(r'\d{2,7}-\d{2}-\d',s) and ok(s)]
            saida[i]=dict(orig=r[0],nome=r[3],formula=r[4],cid=cid,formula_pc=form,cands=cands[:4])
        else:saida[i]=dict(orig=r[0],nome=r[3],formula=r[4],cid=None,cands=[])
        time.sleep(0.15)
    json.dump(saida,open('ref_cache/cas_pub.json','w'),ensure_ascii=False,indent=0)
    print(len(alvo),sum(1 for v in saida.values() if v['cands']))
