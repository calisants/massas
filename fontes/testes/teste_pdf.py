"""Importar espectro em PDF (impressões do SDBS): IV e MS. Sobe um servidor local porque o leitor de PDF é um módulo carregado sob demanda."""
import os,sys,subprocess,time
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from playwright.sync_api import sync_playwright
from _nav import abrir
aqui=os.path.dirname(os.path.abspath(__file__));raiz=os.path.abspath(aqui+'/../..')
srv=subprocess.Popen([sys.executable,'-m','http.server','8771','--directory',raiz],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);time.sleep(1)
try:
  with sync_playwright() as p:
    b=abrir(p);pg=b.new_page(viewport={'width':390,'height':900});er=[];pg.on('pageerror',lambda e:er.append(str(e)))
    pg.goto('http://localhost:8771/index.html');pg.wait_for_timeout(1200)
    pg.set_input_files('#icIVFile',aqui+'/fixtures/sdbs_anilina_ir.pdf')
    pg.wait_for_function("document.querySelector('#icIVMsg').textContent.indexOf('Lendo')<0",timeout=60000)
    v=[int(x) for x in pg.input_value('#icIV').split()]
    for alvo in (3384,1500,1275,878,690):
        assert any(abs(x-alvo)<=15 for x in v),('IV sem banda perto de',alvo,v)
    print('ok  IV em PDF: bandas',len(v))
    pg.set_input_files('#icIVFile',aqui+'/fixtures/iv_rotulos_girados.pdf')
    pg.wait_for_function("document.querySelector('#icIVMsg').textContent.indexOf('Lendo')<0",timeout=60000)
    v=sorted([int(x) for x in pg.input_value('#icIV').split()],reverse=True)
    esperado=[3298,3052,1599,1581,1518,1458,1387,1363,1270,1240,1148,1084,1044,1015,790,766]
    assert v==esperado,('rótulos escritos lidos errado',v)
    print('ok  IV com rótulos escritos na vertical: 16 de 16 números exatos')
    pg.set_input_files('#icFile',aqui+'/fixtures/sdbs_anilina_ms.pdf')
    pg.wait_for_function("document.querySelector('#icMsMsg').textContent.indexOf('Lendo')<0",timeout=60000)
    m=dict(tuple(int(y) for y in t.split(':')) for t in pg.input_value('#icP').split())
    assert m.get(93)==100 and abs(m.get(66,0)-50)<=3 and abs(m.get(65,0)-24)<=3,m
    print('ok  MS em PDF:',m)
    assert not er,er;print('ok  sem erros de código')
    b.close()
finally:srv.terminate()
