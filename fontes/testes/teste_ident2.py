"""Identificar: subestruturas, busca por um sinal, copiar/compartilhar/baixar."""
import sys,os;sys.path.insert(0,os.path.dirname(__file__))
from playwright.sync_api import sync_playwright
from _nav import abrir
URL='file:///home/claude/massas/index.html'
falhas=[]
def chk(n,ok):
    print(('ok  ' if ok else 'FALHOU ')+n)
    if not ok:falhas.append(n)
with sync_playwright() as p:
    b=abrir(p);ctx=b.new_context(viewport={'width':390,'height':800},permissions=['clipboard-read','clipboard-write'])
    pg=ctx.new_page();erros=[];pg.on('pageerror',lambda e:erros.append(str(e)))
    pg.goto(URL);pg.wait_for_timeout(300);pg.evaluate("go('p-ic')");pg.wait_for_timeout(150)
    chk('todo composto tem lista de subestruturas',pg.evaluate("COMP.every(c=>Array.isArray(c.sub))"))
    chk('anilina tem benz e anilina',pg.evaluate("(()=>{const c=COMP.find(c=>c.n==='anilina');return c.sub.includes('benz')&&c.sub.includes('anilina')})()"))
    chk('sem exportar antes de ter resultado',pg.evaluate("document.getElementById('icExp').hidden"))
    # subestrutura: nitro Sim + benzeno Sim -> nitrobenzeno entre os primeiros
    pg.evaluate("icSt.sub.nitro='sim';icSt.sub.benz='sim';icDraw();icRun()");pg.wait_for_timeout(300)
    nome=pg.evaluate("document.querySelector('#icOut .icr button[data-cf]').textContent")
    chk('nitro+benzeno põe um nitro-aromático no topo ('+nome+')',pg.evaluate("(()=>{const c=COMP.find(c=>c.n===document.querySelector('#icOut .icr button[data-cf]').textContent);return c.sub.includes('nitro')&&c.sub.includes('benz')})()"))
    pg.evaluate("icSt.sub.nitro='nao';icDraw();icRun()");pg.wait_for_timeout(300)
    chk('nitro Não tira os nitro do topo',pg.evaluate("(()=>{const c=COMP.find(c=>c.n===document.querySelector('#icOut .icr button[data-cf]').textContent);return !c.sub.includes('nitro')})()"))
    chk('exportar aparece com resultado',pg.evaluate("!document.getElementById('icExp').hidden"))
    t=pg.evaluate("icTexto()")
    chk('texto traz dados, compostos e aviso','DADOS INFORMADOS' in t and 'COMPOSTOS MAIS COMPATÍVEIS' in t and 'não é uma probabilidade' in t and 'Subestrutura' in t)
    pg.click('#icCopy');pg.wait_for_timeout(300)
    chk('copiar põe o texto na área de transferência','DADOS INFORMADOS' in pg.evaluate("navigator.clipboard.readText()"))
    chk('copiar avisa',('copiado' in pg.inner_text('#icExpMsg')))
    with pg.expect_download() as d: pg.click('#icDown')
    chk('baixar gera .txt',d.value.suggested_filename=='identificacao-anaquim.txt')
    pg.evaluate("window.__s=null;navigator.share=async o=>{window.__s=o}");pg.click('#icShare');pg.wait_for_timeout(200)
    chk('compartilhar chama o menu do aparelho',pg.evaluate("!!(window.__s&&window.__s.text.includes('DADOS INFORMADOS'))"))
    pg.evaluate("navigator.share=undefined");pg.click('#icShare');pg.wait_for_timeout(300)
    chk('sem menu de compartilhar, copia e avisa','copiou' in pg.inner_text('#icExpMsg') or 'copiado' in pg.inner_text('#icExpMsg'))
    # preenchimento de exemplo marca subestruturas
    pg.evaluate("icFill(%d)"%pg.evaluate("COMP.findIndex(c=>c.n==='acetona')"));pg.wait_for_timeout(300)
    chk('exemplo marca cetona Sim',pg.evaluate("icSt.sub.cetona==='sim'&&icSt.sub.benz==='nao'"))
    pg.wait_for_timeout(250)
    chk('selo da seção 7 conta marcados',pg.evaluate("document.querySelector('#p-ic .bdg[data-b=\"7\"]').textContent")!='')
    # busca por sinal
    pg.evaluate("document.getElementById('icSin').open=true")
    pg.select_option('#icSinT','iv');pg.fill('#icSinV','1715');pg.wait_for_timeout(200)
    chk('sinal IV 1715 acha compostos',pg.evaluate("+document.querySelector('#icSinO b').textContent")>3)
    pg.select_option('#icSinT','ms');pg.fill('#icSinV','105');pg.wait_for_timeout(200)
    chk('sinal MS 105 acha compostos',pg.evaluate("+document.querySelector('#icSinO b').textContent")>=1)
    pg.select_option('#icSinT','h');pg.fill('#icSinV','9,8');pg.wait_for_timeout(200)
    chk('¹H 9,8 acha aldeídos',pg.evaluate("[...document.querySelectorAll('#icSinO .hint')].some(e=>/aldeído/i.test(e.textContent))"))
    pg.fill('#icSinV','');pg.wait_for_timeout(100)
    chk('campo vazio limpa',pg.inner_text('#icSinO').strip()=='')
    # limpar
    pg.click('#icClr');pg.wait_for_timeout(200)
    chk('limpar esconde exportar',pg.evaluate("document.getElementById('icExp').hidden"))
    chk('limpar zera subestruturas',pg.evaluate("Object.keys(icSt.sub).length===0"))
    chk('sem erros de código',not erros);[print(e) for e in erros[:5]]
    b.close()
if falhas:print('\nFALHARAM:',falhas);sys.exit(1)
print('\nidentificar 2: tudo certo')
