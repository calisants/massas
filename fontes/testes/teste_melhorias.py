"""Melhorias de novembro: abas de Fontes/Avisos/Créditos e os próximos blocos (favoritos, offline, identificar...)."""
import sys,os;sys.path.insert(0,os.path.dirname(__file__))
from playwright.sync_api import sync_playwright
from _nav import abrir
URL='file:///home/claude/massas/index.html'
falhas=[]
def chk(nome,ok):
    print(('ok  ' if ok else 'FALHOU ')+nome)
    if not ok:falhas.append(nome)
with sync_playwright() as p:
    b=abrir(p);pg=b.new_page(viewport={'width':360,'height':740})
    erros=[]
    pg.on('pageerror',lambda e:erros.append(str(e)))
    pg.goto(URL);pg.wait_for_timeout(300)

    # Fontes, Avisos e Créditos em abas
    pg.evaluate("go('p-fo')")
    vis=lambda i:pg.evaluate(f"!document.getElementById('{i}').hidden")
    chk('abre em Fontes',vis('fo-fontes') and not vis('fo-avisos') and not vis('fo-creditos'))
    pg.click('#foTabs [data-fo=fo-avisos]')
    chk('aba Avisos',vis('fo-avisos') and not vis('fo-fontes'))
    pg.click('#foTabs [data-fo=fo-creditos]')
    chk('aba Créditos',vis('fo-creditos') and not vis('fo-avisos'))
    chk('texto dos créditos',pg.inner_text('#fo-creditos').startswith('Feito por Camila Silva, aluna de Bacharelado em Química do IFRJ, como material de apoio ao estudo de Análise Orgânica.'))

    # Favoritos
    pg.evaluate("go('p-cp')")
    chk('lista sem favoritos',pg.evaluate("favGet().length")==0)
    pg.evaluate("cfDraw(3);go('p-cf')")
    cas=pg.evaluate("COMP[3].cas")
    pg.click('#favBtn')
    chk('favoritar guarda o CAS',pg.evaluate("LS.get('massas-fav',[])")==[cas])
    chk('botão mostra favorito',pg.evaluate("document.getElementById('favBtn').getAttribute('aria-pressed')")=='true')
    pg.evaluate("go('p-cp')")
    chk('favorito vem primeiro com estrela',pg.evaluate("document.querySelector('#cpL .cpc').dataset.cf")==pg.evaluate("String(COMP[3].i)") and pg.query_selector('#cpL .cpc .favst') is not None)
    pg.click('#cpF')
    chk('filtro só favoritos',pg.evaluate("document.querySelectorAll('#cpL .cpc').length")==1)
    chk('progresso guarda favoritos',pg.evaluate("'massas-fav' in pgCollect()"))
    pg.click('#cpF')
    pg.evaluate("cfDraw(3);go('p-cf')");pg.click('#favBtn')
    chk('desfavoritar',pg.evaluate("favGet().length")==0)

    # Uso sem internet
    pg.evaluate("go('p-st')");pg.wait_for_timeout(400)
    tx=pg.inner_text('#offBox')
    chk('Ajustes mostra o estado offline',('CONEXÃO' in tx.upper()) and ('VERSÃO GUARDADA' in tx.upper()) and ('FAVORITOS' in tx.upper()))
    pg.context.set_offline(True);pg.wait_for_timeout(300)
    chk('faixa aparece sem internet',pg.evaluate("!!document.getElementById('offBar')&&!document.getElementById('offBar').hidden"))
    pg.context.set_offline(False);pg.wait_for_timeout(300)
    chk('faixa some com internet',pg.evaluate("document.getElementById('offBar').hidden"))


    # acessibilidade
    pg.evaluate("go('p-st')");pg.wait_for_timeout(100)
    fs=lambda:pg.evaluate("document.documentElement.style.fontSize")
    pg.click('#stFonte [data-fs="136"]')
    chk('letra muito grande aplica 136%',fs()=='136%')
    pg.reload();pg.wait_for_timeout(400)
    chk('tamanho da letra fica guardado',fs()=='136%')
    pg.evaluate("go('p-st')");pg.click('#stFonte [data-fs="100"]')
    chk('letra normal limpa o ajuste',fs()=='')
    pg.check('#stAltoc');chk('alto contraste liga classe',pg.evaluate("document.documentElement.classList.contains('altoc')"))
    pg.uncheck('#stAltoc')
    pg.check('#stSemmov');chk('reduzir animações liga classe',pg.evaluate("document.documentElement.classList.contains('semmov')"))
    pg.uncheck('#stSemmov')
    chk('há um landmark main',pg.evaluate("document.querySelectorAll('[role=main],main').length")==1)
    pg.evaluate("go('p-en')");pg.wait_for_timeout(150)
    chk('foco vai para o título da tela',pg.evaluate("document.activeElement&&document.activeElement.tagName")=='H2')

    chk('sem erros de código',not erros);[print(e) for e in erros[:5]]
    b.close()
if falhas:
    print('\nFALHARAM:',falhas);sys.exit(1)
print('\nmelhorias: tudo certo')
