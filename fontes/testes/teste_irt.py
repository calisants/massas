from playwright.sync_api import sync_playwright
P='/tmp/claude-0/-home-claude/e180213d-6606-518c-9aac-0bf913a30c5f/scratchpad/'
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':390,'height':900})
    er=[];pg.on('pageerror',lambda e:er.append(str(e)))
    pg.goto('file:///home/claude/massas/index.html')
    pg.click('#t-iv');pg.click('[data-v="v-guia"]')
    print('linhas',pg.locator('#irtbl .irc').count())
    pg.fill('#irtq','guarda');print('guarda',pg.locator('#irtbl .irc').count())
    pg.fill('#irtq','1700');print('1700',pg.locator('#irtbl .irc').count())
    pg.fill('#irtq','xyzw');print('vazio',pg.locator('#irtbl .empty').count())
    pg.fill('#irtq','simétrico');pg.locator('#irtbl').screenshot(path=P+'irt.png',clip=None) if False else pg.screenshot(path=P+'irt.png')
    pg.click('[data-v="v-num"]');pg.fill('#ivq','1380');print('lookup',pg.locator('#ivres .irc').count())
    pg.locator('#v-guia').evaluate("e=>e.hidden=false");pg.locator('#v-guia dl.gl').first.screenshot(path=P+'gl.png')
    print(er)
