from playwright.sync_api import sync_playwright
errs=[]
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':360,'height':780})
    pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto('file:///home/claude/massas/index.html')
    print('hoje inicial:',pg.inner_text('#hoje').replace('\n',' | ')[:230])
    pg.click('[data-hj=ex]');print('abriu ex:',pg.evaluate("curEx"),'| res visível:',not pg.evaluate("$('#an-res').hidden"))
    pg.click('.stud');pg.click('#an-back');print('depois:',pg.inner_text('#hoje').replace('\n',' | ')[:260])
    pg.click('[data-hj=sim]');print('sim completo:',pg.evaluate("SM.e.n"),pg.evaluate("SM.qs.length"))
    # 12 erros vencidos -> limite 10
    pg.evaluate("const rp={};EX.flatMap(e=>e.rows.map(r=>e.n+':'+r[0])).slice(0,14).forEach(k=>rp[k]={b:0,d:1});LS.set('massas-rep',rp);go('p-an')")
    print('hoje com 14 vencidos:',pg.inner_text('#hoje').split('\n')[1][:60])
    pg.evaluate("go('p-tr')");pg.click('#trmode [data-m=rev]')
    for rodada in range(2):
        for i in range(5):
            pg.click('#tro') if False else None
            # responde tudo até concluir o cartão
            for _ in range(4):
                if pg.query_selector('.optb:not([disabled])'):
                    pg.click('.optb:not([disabled]) >> nth=0')
                    if pg.query_selector('#trn'):pg.click('#trn')
            if pg.query_selector('#tro') and pg.query_selector('.ans'):pg.click('#tro')
        if pg.query_selector('#sessMore'):pg.click('#sessMore')
    print('feitas hoje:',pg.evaluate("revFeitas()"),'| rótulo:',pg.inner_text('#trmode [data-m=rev]'))
    print(pg.inner_text('#quiz')[:140].replace('\n',' '))
print('ERROS:',errs)
