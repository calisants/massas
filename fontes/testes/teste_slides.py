import os;os.makedirs('/tmp/analorg_teste',exist_ok=True)
import sys;sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from playwright.sync_api import sync_playwright
from _nav import abrir
with sync_playwright() as p:
    b=abrir(p);pg=b.new_page(viewport={'width':390,'height':800})
    er=[];pg.on('pageerror',lambda e:er.append(str(e)))
    pg.goto('file:///home/claude/massas/index.html')
    pg.evaluate("go('p-sp')");pg.click('[data-go="p-sl"]')
    n=pg.locator('#slBody figure').count();print('figs',n)
    pg.wait_for_timeout(300)
    ok=pg.evaluate("[...document.querySelectorAll('#slBody img')].every(i=>i.complete&&i.naturalWidth>100)")
    print('imgs ok',ok, 'hscroll',pg.evaluate("document.documentElement.scrollWidth>innerWidth"))
    pg.click('#slBody .mechb');print('overlay',pg.locator('.mechov').count());pg.keyboard.press('Escape');print('closed',pg.locator('.mechov').count())
    pg.screenshot(path='/tmp/analorg_teste/sl.png')
    print('errors',er)
