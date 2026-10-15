from playwright.sync_api import sync_playwright
errs=[]
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':360,'height':740})
    pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto('file:///home/claude/massas/index.html')
    print('ok 1-12:',pg.evaluate("EX.every(e=>e.ok)"),'| resumo cobre:',pg.evaluate("EX.every(e=>e.rows.every(r=>RESUMO[e.n+':'+r[0]]))"),'| IONI cobre:',pg.evaluate("EX.every(e=>IONI[e.n]&&IONI[e.n][1].filter(c=>c[1]===1).length===1&&IONI[e.n][1].filter(c=>c[1]===0).length>=2)"))
    print('origem 1:',pg.evaluate("origemTxt(EX[0])")[:90])
    # caixa de ionização em todos os exercícios
    for n in range(1,13):
        pg.evaluate(f"curEx={n};const e=EX.find(x=>x.n=={n});$('#inM').value=e.M;$('#inP').value=e.peaks.filter(p=>p!==e.M).join(', ');analyze()")
        assert pg.query_selector('#exinfo details.ion'),n
    print('caixa ionização em todos: ok')
    # resumo aparece
    print('resumo visivel:',pg.query_selector('.resumo') is not None)
    pg.click('#t-tr');pg.click('#trmode [data-m=ion]')
    for i in range(5):
        pg.click('.optb >> nth=0');pg.click('#ion-n')
    print('fim sessao:',pg.inner_text('#quiz')[:60])
    pg.click('#sessMore');print('mais 5:',pg.query_selector('.optb') is not None)
    pg.click('#trmode [data-m=qual]')
    for i in range(5):
        pg.click('#tro')
    print('qual sessao:',pg.inner_text('#quiz')[:40]);pg.click('#sessStop');print(pg.inner_text('#sessMsg'))
    pg.click('#trmode [data-m=sm]');pg.select_option('#smsel','10');pg.select_option('#smmod','1');pg.click('#smgo')
    n=pg.evaluate("SM.qs.length");print('perguntas completo ex10:',n)
    for i in range(n):
        pg.click('.optb >> nth=0');pg.click('#smn')
    print(pg.inner_text('#quiz')[:70].replace('\n',' '))
    pg.click('#trmode [data-m=seta]')
    for i in range(pg.evaluate("TR.cur.qs.length")):
        pg.click('.optb >> nth=0');pg.click('#stn')
    print('papel:', 'no papel' in pg.inner_text('#quiz'))
    for sc in ['p-an','p-tr','p-pq','p-pr','p-fo']:
        pg.evaluate(f"go('{sc}')");w=pg.evaluate("document.documentElement.scrollWidth")
        if w>360:print('OVERFLOW',sc,w)
    # todas as perguntas montáveis
    print('qs:',pg.evaluate("EX.flatMap(e=>e.rows.map(r=>{try{keptQ(e,r);return null}catch(x){return e.n+':'+r[0]+' '+x}})).filter(Boolean)"))
print('ERROS:',errs)
