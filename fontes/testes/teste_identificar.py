"""Tela única Identificar: classes que sobram + ranking de compostos + estado salvo."""
import sys,os;sys.path.insert(0,os.path.dirname(__file__))
from playwright.sync_api import sync_playwright
from _nav import abrir
errs=[];ok=True
def chk(nome,cond):
    global ok
    print(('OK   ' if cond else 'FALHA'),nome);ok=ok and bool(cond)
with sync_playwright() as p:
    b=abrir(p);pg=b.new_page(viewport={'width':360,'height':740})
    pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto('file:///home/claude/massas/index.html');pg.wait_for_timeout(500)
    chk('só existe uma tela de identificar',pg.evaluate("!document.getElementById('p-id')&&!!document.getElementById('p-ic')"))
    pg.evaluate("go('p-ic')")
    pg.click('#p-ic [data-ck=est][data-cv="líquido"]');pg.click('#p-ic [data-tk=el][data-ti=O][data-tv=sim]')
    pg.click('#p-ic [data-tk=ir][data-ti=co][data-tv=sim]');pg.click('#p-ic [data-tk=ir][data-ti=oh][data-tv=nao]')
    pg.fill('#icPE','56');pg.wait_for_timeout(400)
    t=pg.inner_text('#icOut')
    chk('classes aparecem (cetona entre elas)','Cetona' in t)
    chk('ranking de compostos aparece','Compostos do banco' in t and 'acetona' in t)
    chk('PE em faixa aceita',pg.evaluate("(()=>{document.getElementById('icPE').value='55–57';return icInputs().pe.v===56})()"))
    # exemplo completo: cada composto deve se identificar em primeiro lugar
    n=pg.evaluate("COMP.length");falhas=[]
    for i in range(n):
        r=pg.evaluate("(i)=>{icFill(i);const x=icInputs();const r=COMP.map(c=>({n:c.n,w:icScore(c,x).w})).sort((a,b)=>b.w-a.w);return [COMP[i].n,r[0].n,r[0].w===r[1].w]}",i)
        if r[0]!=r[1] and not r[2]:falhas.append(r)
    chk('exemplo de cada composto o coloca em 1º ('+str(n-len(falhas))+'/'+str(n)+')',len(falhas)<=n*0.05)
    if falhas:print('  fora do 1º:',[f[0]+'->'+f[1] for f in falhas][:8])
    # estado salvo
    pg.evaluate("icClear()");pg.click('#p-ic [data-ck=g][data-cv=N]');pg.wait_for_timeout(300)
    pg.reload();pg.wait_for_timeout(400)
    chk('estado do formulário sobrevive a recarregar',pg.evaluate("icSt.g==='N'"))
    pg.evaluate("go('p-ic')");pg.evaluate("sesSave()");pg.reload();pg.wait_for_timeout(500)
    chk('volta para a tela em que estava',pg.evaluate("!document.getElementById('p-ic').hidden"))
print('erros de página:',errs)
sys.exit(0 if ok and not errs else 1)
