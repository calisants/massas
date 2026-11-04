"""IV com todos os compostos e espectro simulado, MS por seleção de composto, cor Astronomia, sem Hoje, tabelas legíveis."""
import sys,os;sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
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
    chk('sem caixa Hoje',pg.evaluate("!document.getElementById('hoje')"))
    pg.evaluate("go('p-co')")
    chk('Astronomia de volta',pg.evaluate("[...document.querySelectorAll('#pals button')].some(b=>/Astronomia/.test(b.textContent))"))
    chk('texto da tela Cor removido',pg.evaluate("!/Toque numa cor/.test(document.getElementById('p-co').innerText)"))
    pg.evaluate("setPal('astro')");chk('paleta astro aplica',pg.evaluate("document.documentElement.dataset.pal==='astro'"));pg.evaluate("setPal('azul')")
    pg.evaluate("go('p-fo')")
    t=pg.evaluate("document.documentElement.innerHTML")
    chk('sem avisos para falar com o professor','Pergunte a ele' not in t and 'Conferir com o professor' not in t and 'perguntas para o professor' not in t)
    # IV
    pg.evaluate("go('p-iv')")
    n=pg.evaluate("COMP.length");chk('seletor de IV lista todos os compostos',pg.evaluate("document.querySelectorAll('#ivSel option').length")==n)
    bad=[]
    for i in range(n):
        r=pg.evaluate("(i)=>{ivC=COMP[i].i;drawIV();const h=document.getElementById('ivout').innerHTML;return [/NaN|Infinity|undefined/.test(h),document.querySelectorAll('#ivout .irspec').length,document.querySelectorAll('#ivout tbody tr').length]}",i)
        if r[0] or r[1]!=1 or r[2]<1:bad.append((pg.evaluate("COMP[%d].n"%i),r))
    chk('todos os compostos têm espectro e ao menos 1 banda ('+str(n-len(bad))+'/'+str(n)+')',not bad)
    if bad:print('  ',bad[:6])
    chk('Guia tem mais de 150 linhas',pg.evaluate("IRT.length")>150)
    pg.fill('#ivQ','acetona');chk('busca filtra',pg.evaluate("document.querySelectorAll('#ivSel option').length")<8)
    # MS por seleção de composto
    pg.evaluate("go('p-an')")
    chk('seletor de MS lista todos os compostos',pg.evaluate("document.querySelectorAll('#msSel option').length")==n+1)
    pg.select_option('#msSel',label=pg.evaluate("(()=>{const c=COMP.find(c=>c.n==='tolueno');return c.n+' ('+c.f+')'})()"))
    pg.wait_for_timeout(300)
    chk('composto geral abre a análise',pg.evaluate("!document.getElementById('an-res').hidden")and pg.input_value('#inM')=='92')
    chk('exercícios não aparecem em destaque',pg.evaluate("!document.getElementById('exchips')&&!/Em que ordem estudar/.test(document.getElementById('p-an').innerText)"))
    # tabelas: nenhuma célula com palavra estourando
    est=pg.evaluate("""()=>{const o=[];for(const sc of ['p-pf','p-pb','p-el','p-cs','p-ec']){go(sc);document.querySelectorAll('#'+sc+' td,#'+sc+' th').forEach(c=>{if(c.scrollWidth>c.clientWidth+1)o.push(sc)})}return o}""")
    chk('tabelas do Ensaios sem texto cortado',not est)
print('erros de página:',errs)
sys.exit(0 if ok and not errs else 1)
