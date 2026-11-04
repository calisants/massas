import os;os.makedirs('/tmp/analorg_teste',exist_ok=True)
import sys;sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from playwright.sync_api import sync_playwright
from _nav import abrir
errs=[]
with sync_playwright() as p:
    b=abrir(p);pg=b.new_page(viewport={'width':360,'height':740})
    pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto('file:///home/claude/massas/index.html')
    pg.wait_for_timeout(500);pg.evaluate("go('p-an')")
    for n in range(1,13):
        pg.evaluate(f"curEx={n};const e=EX.find(x=>x.n=={n});$('#inM').value=e.M;$('#inP').value=e.peaks.filter(p=>p!==e.M).join(', ');analyze()")
        imgs=pg.query_selector_all('#mech img');txt=pg.inner_text('#mech')[:70].replace('\n',' ')
        ok=all(pg.evaluate("i=>i.complete&&i.naturalWidth>500",i) for i in imgs)
        print(n,len(imgs),ok,txt)
    pg.evaluate("curEx=12;const e=EX.find(x=>x.n==12);$('#inM').value=e.M;$('#inP').value=e.peaks.filter(p=>p!==e.M).join(', ');analyze()")
    pg.evaluate("document.getElementById('an-res').hidden=false;document.getElementById('an-setup')&&0")
    pg.click('[data-mech="0"]');print('overlay:',pg.query_selector('.mechov') is not None)
    pg.screenshot(path='/tmp/analorg_teste/ov.png')
    pg.keyboard.press('Escape');print('fechou:',pg.query_selector('.mechov') is None)
    pg.evaluate("window.scrollTo(0,0)")
    pg.locator('#mech').scroll_into_view_if_needed()
    pg.screenshot(path='/tmp/analorg_teste/mech.png')
    print('erros:',errs)
