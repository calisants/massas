from playwright.sync_api import sync_playwright
P='/tmp/claude-0/-home-claude/e180213d-6606-518c-9aac-0bf913a30c5f/scratchpad/'
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':390,'height':900})
    er=[];pg.on('pageerror',lambda e:er.append(str(e)))
    pg.goto('file:///home/claude/massas/index.html')
    pg.evaluate("go('p-pq')");pg.locator('#p-pq .rule').first.screenshot(path=P+'ec_rule.png')
    pg.evaluate("go('p-se')");pg.wait_for_timeout(200)
    pg.locator('#se-anchor .mdl').nth(1).screenshot(path=P+'ec_alfa.png')
    pg.locator('#se-anchor .mdl').nth(3).screenshot(path=P+'ec_het.png')
    pg.evaluate("go('p-an')")
    print(pg.evaluate("typeof stepCard"))
    h=pg.evaluate("(()=>{const ex=EX.find(e=>e.n===9);const r=ex.rows.find(r=>r[0]===60);const d=document.createElement('div');d.id='tmpx';d.innerHTML=stepCard(ex,r);document.body.appendChild(d);return d.querySelectorAll('.ec').length})()")
    print('ec boxes',h)
    pg.locator('#tmpx .ec').first.screenshot(path=P+'ec_mcl.png')
    print(er)
