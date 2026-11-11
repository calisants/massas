"""Busca o campo 'Color/Form' (descrição de cor/forma) do PubChem para cada composto do banco. Guarda texto e fonte em ref_cache/cor.json."""
import json,time,urllib.request,threading,os,sys
from concurrent.futures import ThreadPoolExecutor
ESC=json.load(open('ref_cache/escolha.json'));cids=sorted({str(v) for v in ESC.values() if v})
OUT='ref_cache/cor.json';res=json.load(open(OUT)) if os.path.exists(OUT) else {}
URL='https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/%s/JSON?heading=Color%%2FForm'
def walk(sec,acc):
    for s in sec if isinstance(sec,list) else [sec]:
        if s.get('TOCHeading')=='Color/Form':
            for i in s.get('Information',[]):
                t=''.join(x.get('String','') for x in i.get('Value',{}).get('StringWithMarkup',[]))
                if t:acc.append([t,i.get('Reference','')])
        walk(s.get('Section',[]),acc) if s.get('Section') else None
ref={}
def one(c):
    if c in res:return
    for t in range(3):
        try:
            d=json.load(urllib.request.urlopen(URL%c,timeout=30));acc=[]
            walk(d['Record']['Section'],acc);ref_=d['Record'].get('Reference',[])
            m={r['ReferenceNumber']:r.get('SourceName','') for r in ref_}
            res[c]=[[a[0],m.get(a[1],'')] for a in acc];break
        except urllib.error.HTTPError as e:
            if e.code==404:res[c]=[];break
            time.sleep(2)
        except Exception:time.sleep(2)
    time.sleep(0.05)
n=0
with ThreadPoolExecutor(12) as ex:
    futs=[ex.submit(one,c) for c in cids]
    for i,f in enumerate(futs):
        f.result()
        if i%200==0:
            json.dump(res,open(OUT,'w'));print(i,len(res),flush=True)
json.dump(res,open(OUT,'w'));print('fim',len(res))
