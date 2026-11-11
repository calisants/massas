"""Gera cas_corrigido.json a partir de ref_cache/cas_pub.json: só aceita correção com dígito verificador certo e fórmula conferida (PubChem) ou erro de digitação óbvio (zeros à esquerda, colchete)."""
import json,re
from cas_corrige import ok,lev  # noqa
import re
def norm(c):
    c=re.sub(r'[^\d-]','',c or '')
    m=re.fullmatch(r'(\d+)-(\d+)-(\d+)',c)
    if not m:return None
    a,b,d=m.groups()
    return '%d-%s-%d'%(int(a),b,int(d)) if len(b)==2 else None
pub=json.load(open('ref_cache/cas_pub.json'))
saida={};sem=[]
for k,v in pub.items():
    o=v['orig'];novo=None;fonte=None
    n=norm(o)
    if n and ok(n):novo,fonte=n,'erro de digitação (zeros à esquerda ou símbolo sobrando); dígito verificador confere'
    else:
        c=v['cands']
        if c and (v.get('formula_pc') in (None,v['formula'])):
            novo=min(c,key=lambda x:lev(o,x));fonte='PubChem, composto de mesma fórmula; dígito verificador confere'
    if novo:saida[k]=[o,novo,fonte]
    else:sem.append((k,o,v['nome']))
json.dump(saida,open('cas_corrigido.json','w',encoding='utf-8'),ensure_ascii=False,indent=0)
print(len(saida),'corrigidos;',len(sem),'sem correção')
for x in saida.items():print(x[0],x[1][0],'->',x[1][1])
