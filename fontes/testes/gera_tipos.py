from playwright.sync_api import sync_playwright
import json
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page();pg.goto('file:///home/claude/massas/fontes/saida.html')
    d=pg.evaluate("Object.fromEntries(EX.flatMap(e=>e.rows.map(r=>[e.n+':'+r[0],tipoE(e,r)])))")
d.update({'1:65':'neu','1:51':'neu','11:85':'alfa','12:29':'alfa'})
json.dump(d,open('/tmp/tipo.json','w'),ensure_ascii=False)
print(len(d))
