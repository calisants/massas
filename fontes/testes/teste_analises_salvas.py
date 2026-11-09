"""Identificar: salvar análises, reabrir, excluir, exportar/importar, relatório."""
import sys,os,json;sys.path.insert(0,os.path.dirname(__file__))
from playwright.sync_api import sync_playwright
from _nav import abrir
URL='file:///home/claude/massas/index.html'
falhas=[]
def chk(n,ok):
    print(('ok  ' if ok else 'FALHOU ')+n)
    if not ok:falhas.append(n)
with sync_playwright() as p:
    b=abrir(p);ctx=b.new_context(viewport={'width':390,'height':800},accept_downloads=True)
    pg=ctx.new_page();erros=[];pg.on('pageerror',lambda e:erros.append(str(e)))
    pg.goto(URL);pg.wait_for_timeout(300);pg.evaluate("go('p-ic')");pg.wait_for_timeout(150)
    chk('sem resultado não há botão de salvar visível',pg.evaluate("document.getElementById('icExp').hidden"))
    chk('lista começa vazia',pg.inner_text('#icSavN')=='0')
    pg.evaluate("icFill(%d)"%pg.evaluate("COMP.findIndex(c=>c.n==='acetona')"));pg.wait_for_timeout(400)
    pg.fill('#icNome','Amostra 3');pg.fill('#icObs','cheiro doce\nlíquido incolor')
    pg.click('#icSalvar');pg.wait_for_timeout(200)
    chk('salvou uma análise',pg.inner_text('#icSavN')=='1')
    chk('avisa que salvou','salva' in pg.inner_text('#icSavMsg'))
    chk('nome aparece na lista','Amostra 3' in pg.inner_text('#icSavL'))
    chk('mostra o melhor composto','acetona' in pg.inner_text('#icSavL').lower())
    chk('campos de nome e observação limpam depois de salvar',pg.input_value('#icNome')=='' and pg.input_value('#icObs')=='')
    chk('guardou no localStorage',pg.evaluate("JSON.parse(localStorage.getItem('massas-an')).length")==1)
    # texto e relatório trazem nome e observações
    pg.fill('#icNome','Amostra 3');pg.fill('#icObs','cheiro doce')
    t=pg.evaluate("icTexto()")
    chk('texto traz o nome e as observações','Amostra 3' in t and 'OBSERVAÇÕES' in t and 'cheiro doce' in t and 'DADOS INFORMADOS' in t)
    h=pg.evaluate("icRelatorio()")
    chk('relatório é um HTML completo com nome, ranking e aviso','<!doctype html>' in h and 'Amostra 3' in h and 'Compostos mais compatíveis' in h and 'não é uma probabilidade' in h)
    chk('relatório escapa HTML digitado',('<script>' not in (pg.evaluate("(()=>{document.getElementById('icObs').value='<script>x</script>';return icRelatorio()})()"))))
    # limpar e reabrir
    pg.click('#icClr');pg.wait_for_timeout(200)
    chk('limpar esconde exportar',pg.evaluate("document.getElementById('icExp').hidden"))
    pg.click('#icSavL [data-an=abrir]');pg.wait_for_timeout(500)
    chk('abrir restaura os dados e recalcula',pg.evaluate("!document.getElementById('icExp').hidden")  and 'acetona' in pg.inner_text('#icOut').lower())
    chk('abrir restaura o nome',pg.input_value('#icNome')=='Amostra 3')
    # relatório abre numa janela
    with ctx.expect_page() as np:
        pg.click('#icRel')
    rel=np.value;rel.wait_for_load_state()
    chk('relatório abre numa aba com o botão de imprimir','Imprimir' in rel.inner_text('body') and 'Amostra 3' in rel.inner_text('body'))
    rel.close()
    # exportar
    with pg.expect_download() as d: pg.click('#icSavExp')
    chk('exportar gera analises-anaquim.json',d.value.suggested_filename=='analises-anaquim.json')
    dados=json.load(open(d.value.path(),encoding='utf-8'))
    chk('json tem a análise',dados['anaquim']=='analises' and len(dados['a'])==1)
    # excluir (dois toques)
    pg.click('#icSavL [data-an=del]');
    chk('primeiro toque pede confirmação','Confirmar' in pg.inner_text('#icSavL'))
    pg.click('#icSavL [data-an=del]');pg.wait_for_timeout(150)
    chk('excluiu',pg.inner_text('#icSavN')=='0')
    # importar
    path='/tmp/imp.json';json.dump(dados,open(path,'w',encoding='utf-8'))
    pg.set_input_files('#icSavFile',path);pg.wait_for_timeout(300)
    chk('importou',pg.inner_text('#icSavN')=='1')
    pg.set_input_files('#icSavFile',path);pg.wait_for_timeout(300)
    chk('importar de novo não duplica',pg.inner_text('#icSavN')=='1')
    # o código do progresso leva e junta as análises
    code=pg.evaluate("pgEnc({v:1,d:pgCollect()})")
    pg.evaluate("localStorage.removeItem('massas-an')")
    pg.evaluate("go('p-pg')");pg.fill('#pgTxt',code);pg.click('#pgImp');pg.wait_for_timeout(200)
    chk('código de progresso restaura as análises',pg.evaluate("JSON.parse(localStorage.getItem('massas-an')||'[]').length")==1)
    # persiste ao recarregar
    pg.reload();pg.wait_for_timeout(400);pg.evaluate("go('p-ic')");pg.wait_for_timeout(150)
    chk('análise continua depois de recarregar',pg.inner_text('#icSavN')=='1')
    chk('sem erros de JavaScript',not erros)
    if erros:print(erros)
    b.close()
if falhas:
    print('\nFALHARAM:',falhas);sys.exit(1)
print('\nTudo certo.')
