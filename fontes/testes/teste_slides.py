from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':390,'height':800})
    er=[];pg.on('pageerror',lambda e:er.append(str(e)))
    pg.goto('file:///home/claude/massas/index.html')
    pg.click('#t-ma');pg.click('[data-go="p-sl"]')
    n=pg.locator('#slBody figure').count();print('figs',n)
    pg.wait_for_timeout(300)
    ok=pg.evaluate("[...document.querySelectorAll('#slBody img')].every(i=>i.complete&&i.naturalWidth>100)")
    print('imgs ok',ok, 'hscroll',pg.evaluate("document.documentElement.scrollWidth>innerWidth"))
    pg.click('#slBody .mechb');print('overlay',pg.locator('.mechov').count());pg.keyboard.press('Escape');print('closed',pg.locator('.mechov').count())
    pg.screenshot(path='/tmp/claude-0/-home-claude/e180213d-6606-518c-9aac-0bf913a30c5f/scratchpad/sl.png')
    print('errors',er)
