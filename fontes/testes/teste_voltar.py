"""Botão voltar do aparelho: volta uma tela dentro do app, fecha ampliações e abre links diretos."""
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
    def tela():return pg.evaluate('CUR')
    def volta():
        pg.go_back();pg.wait_for_timeout(200)

    # 1) telas empilham e o voltar desfaz uma de cada vez
    pg.goto(URL);pg.wait_for_timeout(300)
    chk('começa no Início, primeira entrada do histórico',tela()=='p-in' and pg.evaluate('history.state.i')==0)
    pg.click('#t-en');pg.click('[data-go=p-pf]:visible >> nth=0')
    chk('foi para Preliminares',tela()=='p-pf')
    volta();chk('voltar leva a Ensaios',tela()=='p-en')
    volta();chk('voltar leva ao Início',tela()=='p-in')

    # 2) o botão "← Ensaios" do app não empilha mais uma entrada
    pg.click('#t-en');pg.click('[data-go=p-pf]:visible >> nth=0');pg.click('#p-pf .back:visible >> nth=0')
    chk('botão do app volta para Ensaios',tela()=='p-en')
    chk('sem entrada a mais no histórico',pg.evaluate('NAVI')==1)
    volta();chk('depois, voltar leva ao Início',tela()=='p-in')

    # 3) ampliação: voltar fecha a ampliação e fica na mesma tela
    pg.click('#t-sp');t0=tela()
    pg.evaluate("mechZoom('icon-192.png',null)")
    chk('ampliação abriu',pg.query_selector('.mechov') is not None)
    volta()
    chk('voltar fechou a ampliação',pg.query_selector('.mechov') is None)
    chk('continua na mesma tela',tela()==t0)
    pg.evaluate("mechZoom('icon-192.png',null)");pg.click('.mechx');pg.wait_for_timeout(200)
    chk('fechar pelo botão não deixa entrada sobrando',not pg.evaluate('!!(history.state&&history.state.ov)'))
    volta();chk('voltar leva ao Início',tela()=='p-in')

    # 4) link direto para uma tela e para uma ficha de composto
    pg.goto('about:blank');pg.goto(URL+'#/pf');pg.wait_for_timeout(300)
    chk('link #/pf abre Preliminares',tela()=='p-pf')
    cas=pg.evaluate('COMP[3].cas')
    pg.goto('about:blank');pg.goto(URL+'#/cf/'+cas);pg.wait_for_timeout(300)
    chk('link #/cf/CAS abre a ficha certa',tela()=='p-cf' and pg.evaluate('CFI')==3)
    chk('endereço da ficha guarda o CAS',pg.evaluate('location.hash')=='#/cf/'+cas)
    volta();chk('voltar da ficha leva ao Início',tela()=='p-in')
    pg.goto('about:blank');pg.goto(URL+'#/xyz');pg.wait_for_timeout(300)
    chk('endereço inválido cai no Início',tela()=='p-in')

    # 5) ficha aberta pela lista: voltar volta para a lista
    pg.evaluate("go('p-cp')");pg.evaluate("cfDraw(5);go('p-cf')")
    chk('ficha aberta',tela()=='p-cf' and pg.evaluate('CFI')==5)
    volta();chk('voltar da ficha leva à lista',tela()=='p-cp')

    chk('sem erros de código',not erros)
    [print(e) for e in erros[:5]]
    b.close()
if falhas:
    print('\nFALHARAM:',falhas);sys.exit(1)
print('\nvoltar: tudo certo')
