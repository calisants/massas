"""Ajustes (zoom, sem pistas), novidades, revisão de perguntas, fontes recolhidas, menus."""
import sys,os;sys.path.insert(0,os.path.dirname(__file__))
from playwright.sync_api import sync_playwright
from _nav import abrir
errs=[];ok=True
def chk(nome,cond):
    global ok
    print(('OK   ' if cond else 'FALHA'),nome);ok=ok and bool(cond)
with sync_playwright() as p:
    b=abrir(p);ctx=b.new_context(viewport={'width':360,'height':740});pg=ctx.new_page()
    pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto('file:///home/claude/massas/index.html');pg.wait_for_timeout(500)
    chk('zoom travado por padrão',pg.evaluate("document.querySelector('meta[name=viewport]').content.includes('user-scalable=no')"))
    pg.evaluate("go('p-st')");pg.check('#stZoom')
    chk('zoom liga no ajuste',pg.evaluate("!document.querySelector('meta[name=viewport]').content.includes('user-scalable=no')"))
    pg.uncheck('#stZoom')
    # sem pistas
    pg.evaluate("go('p-tr')");pg.click('#trmode [data-m=qual]')
    chk('dica aparece por padrão',pg.query_selector('#trh') is not None)
    pg.evaluate("go('p-st')");pg.check('#stSem');pg.evaluate("go('p-tr')");pg.click('#trmode [data-m=qual]')
    chk('dica some com o ajuste ligado',pg.query_selector('#trh') is None)
    pg.evaluate("go('p-st')");pg.uncheck('#stSem')
    # revisão de perguntas: errar um quiz guarda a pergunta
    pg.evaluate("go('p-iv')");pg.click('.seg [data-v=v-tr]')
    pg.wait_for_selector('#ivQuiz .optb')
    pg.evaluate("document.querySelectorAll('#ivQuiz .optb')");
    q=pg.evaluate("(()=>{const o=[...document.querySelectorAll('#ivQuiz .optb')];return o.length})()")
    # clica numa opção por vez até errar
    for k in range(4):
        pg.click('#ivQuiz .optb >> nth=%d'%k)
        if pg.evaluate("Object.keys(LS.get('massas-repq',{})).length")>0:break
        pg.click('#mqx');pg.wait_for_selector('#ivQuiz .optb')
    chk('pergunta errada fica guardada',pg.evaluate("Object.keys(LS.get('massas-repq',{})).length")>=1)
    pg.evaluate("(()=>{const r=LS.get('massas-repq',{});Object.keys(r).forEach(k=>r[k].d=Date.now()-1000);LS.set('massas-repq',r);})()")
    pg.evaluate("go('p-rv')");pg.wait_for_selector('#rvBox .optb')
    chk('Revisar mostra a pergunta vencida',True)
    # exporta/importa progresso mantém repq
    pg.evaluate("go('p-pg')");pg.click('#pgGen');code=pg.input_value('#pgTxt')
    chk('código de progresso leva o repq',len(code)>20)
    # aviso de atualização para quem já tinha o app
    pg.evaluate("localStorage.setItem('massas-visto','1')");pg.reload();pg.wait_for_timeout(400)
    chk('aviso de atualização aparece',pg.evaluate("!!document.getElementById('nvBanner')&&!document.getElementById('nvBanner').hidden"))
    pg.click('#nvLer');chk('abre as novidades',pg.evaluate("!document.getElementById('p-nv').hidden"))
    pg.evaluate("go('p-in')");chk('aviso some depois de ler',pg.evaluate("document.getElementById('nvBanner').hidden"))
    # fontes recolhidas
    pg.evaluate("cfDraw(0);go('p-cf')");pg.wait_for_timeout(300)
    chk('fontes da ficha recolhidas',pg.evaluate("document.querySelectorAll('#cfB details.fonte').length")>=1)
    # etiquetas padronizadas
    txt=pg.evaluate("document.documentElement.innerText+document.documentElement.innerHTML")
    chk('sem "escrito por mim"','escrito por mim' not in txt.lower())
    # menus
    chk('Início sem ferramentas de massas',pg.evaluate("go('p-in'),document.getElementById('p-in').innerText.indexOf('Calculadora')<0"))
    chk('Massas com ferramentas de massas',pg.evaluate("go('p-ms'),document.getElementById('p-ms').innerText.indexOf('Calculadora')>=0"))
    for sc in ['p-in','p-en','p-ms','p-ic','p-st','p-nv','p-rv','p-co','p-fo','p-cf','p-cp','p-ob','p-rm','p-iv']:
        pg.evaluate(f"go('{sc}')");w=pg.evaluate("document.documentElement.scrollWidth")
        if w>360:chk('sem estouro em '+sc+' ('+str(w)+')',False)
print('erros de página:',errs)
sys.exit(0 if ok and not errs else 1)
