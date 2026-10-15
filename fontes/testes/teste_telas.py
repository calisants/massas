from playwright.sync_api import sync_playwright
import json
errs=[]
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':360,'height':740})
    pg.on('pageerror',lambda e:errs.append(str(e)));pg.on('console',lambda m:m.type=='error' and 'fonts' not in m.text and errs.append(m.text))
    pg.goto('file:///home/claude/massas/index.html')
    print('tipo cobre todas:',pg.evaluate("EX.every(e=>e.rows.every(r=>TIPO[e.n+':'+r[0]]))"))
    pg.click('#t-tr')
    print('chips:',pg.evaluate("[...document.querySelectorAll('#trmode button')].map(b=>b.textContent)"))
    # seta
    pg.click('#trmode [data-m=seta]')
    for _ in range(3):
        for _ in range(pg.evaluate("TR.cur.qs.length")):
            pg.click('.optb >> nth=0');pg.click('#stn')
        pg.wait_for_selector('#quiz .mdl svg');print('svg final ok');pg.click('#sto')
    # simulado
    pg.click('#trmode [data-m=sm]');pg.select_option('#smsel','12');pg.click('#smgo')
    n=pg.evaluate("SM.qs.length")
    for i in range(n):
        pg.click('.optb >> nth=0' if i%2 else '.optb >> nth=1');pg.click('#smn')
    print(pg.inner_text('#quiz')[:200])
    print('rep:',pg.evaluate("localStorage.getItem('massas-rep')"))
    pg.click('#trmode [data-m=rev]');print(pg.inner_text('#trmode')[-30:]);print(pg.inner_text('#quiz')[:150])
    pg.click('#revall') if pg.query_selector('#revall') else None
    print('rev q:',pg.inner_text('#quiz')[:120])
    # perguntas/progresso
    pg.evaluate("go('p-pr')");pg.click('#pergL input >> nth=0');print('perg',pg.evaluate("localStorage.getItem('massas-perg')"))
    pg.evaluate("go('p-pg')");pg.click('#pgGen');code=pg.input_value('#pgTxt');print('code len',len(code))
    pg.evaluate("localStorage.clear()");pg.click('#pgImp');print(pg.inner_text('#pgMsg'));print(pg.evaluate("Object.keys(localStorage)"))
    pg.fill('#pgTxt','lixo');pg.click('#pgImp');print(pg.inner_text('#pgMsg'))
    pg.evaluate("go('p-se')");print('alias:',pg.evaluate("!document.getElementById('p-pq').hidden"))
    # todos os porquês e cisões
    pg.evaluate("go('p-an')")
    print('menu:',pg.evaluate("[...document.querySelectorAll('#p-ma .mi b')].map(b=>b.textContent)"))
    # overflow sweep
    pg.evaluate("TR.mode='qual'")
    for sc in ['p-an','p-tr','p-tb','p-iv','p-ma','p-pq','p-pr','p-pg','p-es','p-co','p-fo','p-aj']:
        pg.evaluate(f"go('{sc}')");w=pg.evaluate("document.documentElement.scrollWidth")
        if w>360:print('OVERFLOW',sc,w)
print('ERROS:',errs)
