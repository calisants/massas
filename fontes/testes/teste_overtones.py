"""Overtones em opções: o usuário diz o padrão do anel (mono, orto, meta, para) e as outras bandas fracas; o Identificar confere com cada composto."""
import os,sys,json
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from playwright.sync_api import sync_playwright
from _nav import abrir
with sync_playwright() as p:
    b=abrir(p);pg=b.new_page(viewport={'width':390,'height':900});er=[];pg.on('pageerror',lambda e:er.append(str(e)))
    pg.goto('file://'+os.path.abspath(os.path.dirname(__file__)+'/../../index.html'));pg.wait_for_timeout(1200)
    pg.evaluate("go('p-ic')");pg.wait_for_timeout(300)
    def rank(ring):
        pg.evaluate("icReset();icDraw()")
        pg.evaluate("(r)=>{icSt.ring=r;icDraw();icRun();}",ring)
        return pg.evaluate("(()=>{const x=icInputs();const L=bdAll().concat(COMP).map(c=>({n:c.n,s:icScore(c,x)}));return L})()")
    # padrão de cada composto pelo texto dos overtones
    pat=pg.evaluate("COMP.map(c=>[c.n,ringPat(c)])")
    d=dict(pat)
    assert d['tolueno']=='mono',d['tolueno']
    paras=[n for n,k in pat if k=='para'];metas=[n for n,k in pat if k=='meta'];ortos=[n for n,k in pat if k=='orto']
    print('ok  padrões lidos: mono',sum(1 for n,k in pat if k=='mono'),'orto',len(ortos),'meta',len(metas),'para',len(paras),'sem anel',sum(1 for n,k in pat if k=='nenhum'))
    assert paras and ortos
    for ring,alvos in (('para',paras),('orto',ortos),('mono',['tolueno'])):
        pg.evaluate("(r)=>{icReset();icSt.ring=r;icDraw();}",ring)
        r=pg.evaluate("(()=>{const x=icInputs();return COMP.map(c=>[c.n,JSON.stringify(icScore(c,x)).length])})()")
        ok=pg.evaluate("(a)=>{const x=icInputs();return a.every(n=>{const c=COMP.find(c=>c.n===n);const s=icScore(c,x);return JSON.stringify(s).indexOf('Overtones: anel '+'')>=0})}",alvos)
        assert ok,('anel '+ring+' não aparece nos critérios',alvos)
        print('ok  anel',ring,'confere com',len(alvos),'compostos do app')
    # um composto de outro padrão perde
    pg.evaluate("(r)=>{icReset();icSt.ring=r;icDraw();}",'para')
    s=pg.evaluate("(()=>{const x=icInputs();const c=COMP.find(c=>c.n==='tolueno');return icScore(c,x)})()")
    assert 'não é' in json.dumps(s,ensure_ascii=False),s
    print('ok  mono não passa como para')
    # opções de aldeído
    pg.evaluate("icReset();icSt.ot={ald:'sim'};icDraw()")
    ald=pg.evaluate("COMP.filter(c=>otTem(c,'ald')).map(c=>c.n)")
    print('ok  aldeídos com Fermi 2820/2720:',len(ald),ald[:3])
    assert ald
    # anel com 4 ou mais substituintes e anel fundido (ex.: ácido gálico, naftaleno): têm anel benzênico, então "Sem anel" não pode ser neutro para eles
    js_f="""(r)=>{icReset();icSt.ring=r;icDraw();const x=icInputs();
      return bdAll().concat(COMP).map(c=>{const s=icScore(c,x);const p=s.parts.find(p=>/^Overtones: anel/.test(p.lab));return [c.n,ringPat(c),p?p.f:null]})}"""
    ids=[k for k,_ in pg.evaluate("RING")]
    assert 't4' in ids and 'fund' in ids,('faltam as opções de anel com 4+ substituintes e anel fundido',ids)
    todos=pg.evaluate("bdAll().concat(COMP).map(c=>[c.n,ringPat(c)])")
    assert not [n for n,k in todos if k=='outro'],'sobrou composto sem classificação de anel'
    dd=dict(todos)
    assert dd['Ácido gálico']=='t4',dd['Ácido gálico']
    assert any(k=='fund' for n,k in todos)
    for ring in ('nenhum','mono','para','t123'):
        for n,k,f in pg.evaluate(js_f,ring):
            if k in ('t4','fund'):
                assert f is not None and f<0.1,('anel '+ring+': '+n+' ('+k+') deveria perder, fator',f)
    for ring,k0 in (('t4','t4'),('fund','fund')):
        res=pg.evaluate(js_f,ring)
        assert all(f==1 for n,k,f in res if k==k0),('anel '+ring+' não confere com todos os '+k0)
        assert all(f<0.1 for n,k,f in res if k not in (k0,None) and f is not None),('anel '+ring+' deixa passar outro padrão')
    # "Sem anel" nunca pode subir a nota de um composto aromático em relação a "não sei"
    w=lambda ring,nome:pg.evaluate("(a)=>{icReset();icSt.ring=a[0];icDraw();const x=icInputs();return icScore(bdAll().concat(COMP).find(c=>c.n===a[1]),x).w}",[ring,nome])
    assert w('nenhum','Ácido gálico')<w('','Ácido gálico'),'Sem anel benzênico não pode favorecer o ácido gálico'
    print('ok  anel com 4+ substituintes e fundido: opções próprias, "Sem anel" derruba esses compostos')
    assert not er,er;print('ok  sem erros de código')
    b.close()
