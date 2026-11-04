# Patch único: transforma o template do app de MS/IR da disciplina no Analorg geral.
import re
T=open('template.html',encoding='utf-8').read()
def rep(old,new,cnt=1):
    global T
    assert T.count(old)>=1,('não achei',old[:70])
    T=T.replace(old,new) if cnt==0 else T.replace(old,new,cnt)
def cut(a,b,new=''):
    global T
    i=T.index(a); j=T.index(b,i); T=T[:i]+new+T[j:]

# --- Início novo ---
cut('<section id="p-in"','<section id="p-en"','''<section id="p-in" role="tabpanel" aria-labelledby="t-in">
    <h2 class="scr">Início</h2>
    <p class="scrsub">Consulta e estudo de Análise Orgânica: do básico aos espectros. Escolha por onde começar.</p>
    <div class="menu">
      <button class="mi" type="button" data-go="p-ob"><b>Orgânica Básica</b><span>Grupos funcionais, hibridização, GDH, Lewis, acidez e forças intermoleculares.</span></button>
      <button class="mi" type="button" data-go="p-cp"><b>Compostos</b><span>Uma ficha por composto: estrutura, fórmula, solubilidade, cor, estado, PF, PE e espectros esperados.</span></button>
      <button class="mi" type="button" data-go="p-ic"><b>Identificação do Composto</b><span>Dê o que você mediu (solubilidade, PF, PE, IV, MS, RMN) e veja os compostos mais compatíveis.</span></button>
      <button class="mi" type="button" data-go="p-en"><b>Análise de Ensaios</b><span>Cor, ignição, PF e PE, solubilidade, análise elementar e problemas resolvidos.</span></button>
      <button class="mi" type="button" data-go="p-sp"><b>Espectros: IV, MS e RMN</b><span>Bandas, fragmentações, deslocamentos e como ler cada um.</span></button>
    </div>
    <h2>Passos da análise</h2>
    <div class="menu">
      <button class="mi" type="button" data-go="p-pf"><b>1. Preliminares e propriedades físicas</b><span>Cor, ignição, ponto de fusão e de ebulição.</span></button>
      <button class="mi" type="button" data-go="p-so"><b>2. Solubilidade</b><span>Fluxograma, os 10 grupos e treino.</span></button>
      <button class="mi" type="button" data-go="p-el"><b>3. Análise elementar</b><span>Testes para C, H, O, N, S, halogênios e P.</span></button>
      <button class="mi" type="button" data-go="p-iv"><b>4. Infravermelho (IV)</b><span>Bandas por composto e por número de onda.</span></button>
      <button class="mi" type="button" data-go="p-an"><b>5. Espectrometria de massas</b><span>Exemplos com mecanismo, treino e tabelas.</span></button>
      <button class="mi" type="button" data-go="p-rm"><b>6. RMN de ¹H e ¹³C</b><span>Quantos sinais, onde aparecem e como se dividem.</span></button>
    </div>
    <div class="rule"><h3>SDBS: espectros reais</h3>
      <p>O SDBS (AIST, Japão) é um banco aberto com IV, MS, RMN e outros espectros medidos de milhares de compostos. Cada ficha de composto aqui tem um botão que leva até ele. Ao usar dados de lá, cite a fonte (o app mostra o texto pronto).</p>
      <div class="row" style="margin:8px 0 0"><a class="btn" href="https://sdbs.db.aist.go.jp/" target="_blank" rel="noopener">Abrir o SDBS</a></div></div>
  </section>

  ''')
# --- Ensaios ---
rep('<h2 class="scr">Ensaios</h2>','<h2 class="scr">Análise de Ensaios</h2>')
rep('<h2 class="mh">Ferramentas para a prova</h2>','<h2 class="mh">Ferramentas</h2>')
rep('Ferramenta de busca do professor (por elementos','Ferramenta de busca Analor (por elementos')
rep('Ferramenta Analor</a> do professor','Ferramenta Analor</a>')
rep('O app não tem banco de compostos. Para comparar PF/PEb com valores tabelados, use','Para comparar PF/PEb com valores tabelados de mais compostos, use')
rep('para consultar durante a prova (que é com consulta). Os dados','para consultar com rapidez. Os dados')
# --- Massas ---
rep('    <div class="rule" id="hoje"></div>\n','')
rep('Escolha um exercício ou digite M e os picos.','Escolha um composto ou digite M e os picos.')
rep('Exercícios da lista (nos PDFs a numeração vai do 10 direto ao 12):','Compostos com mecanismo de fragmentação:')
cut('<details class="how" style="margin-bottom:10px"><summary style="cursor:pointer;font-weight:600">Em que ordem estudar?','<div class="chips" id="exchips">','''<details class="how" style="margin-bottom:10px"><summary style="cursor:pointer;font-weight:600">Em que ordem estudar?</summary><p class="hint" style="margin-top:8px">Do mais simples ao mais complexo: <b>1-propanol</b> (álcool, clivagem α) → <b>ácido butanoico</b> (McLafferty) → <b>3-pentanona</b> (cetona) → <b>N,N-dimetiletilamina</b> (amina) → <b>pentanal</b> (aldeído) → <b>pentanoato de metila</b> (éster) → <b>benzofenona</b> → <b>etilbenzeno</b> → <b>estireno</b> → <b>piridina</b> → <b>1,4-dioxano</b> → <b>furano</b>. Os anéis ficam para o fim porque abrem e se rearranjam. Marque cada um como estudado depois de resolver.</p></details>
    ''')
sg='<div class="sgm msub" role="group" aria-label="Massas">'
rep(sg,'<button class="back" type="button" data-go="p-sp">← Espectros</button>\n    '+sg,0)
# --- IV ---
rep('<h2 class="scr">IV</h2>','<button class="back" type="button" data-go="p-sp">← Espectros</button>\n    <h2 class="scr">Infravermelho (IV)</h2>')
rep('<button type="button" data-v="v-tr" aria-pressed="false">Treinar</button>','<button type="button" data-v="v-tr" data-go="p-ic" aria-pressed="false">Identificar</button>')
rep("g.querySelectorAll('button').forEach(b=>{b.onclick=()=>{\n  g.querySelectorAll","g.querySelectorAll('button').forEach(b=>{b.onclick=()=>{if(b.dataset.go)return;\n  g.querySelectorAll")
# --- Mais ---
rep('''    <h2 class="mh">Estudo</h2>
    <div class="menu">
      <button class="mi" type="button" data-go="p-pr"><b>Perguntas para o professor</b><span>As dúvidas que ainda não consegui confirmar. Marque as que já perguntou.</span></button>
    </div>
''','')
cut('<section id="p-pr"','<section id="p-pg"')
rep('<b>Slides do professor</b><span>Regras e mecanismos do deck dele: benzamida','<b>Slides de mecanismos</b><span>Regras e mecanismos de aula: benzamida')
rep('aria-label="Slides do professor"','aria-label="Slides de mecanismos"')
rep('<h2 class="scr">Slides do professor</h2>','<h2 class="scr">Slides de mecanismos</h2>')
rep('Fonte: slides do professor. Os resumos','Fonte: slides de aula de Análise Orgânica (IFRJ). Os resumos')
# --- navegação ---
cut('<nav class="bnav"','<script>','''<nav class="bnav" role="tablist" aria-label="Seções">
  <button class="tab" role="tab" id="t-in" aria-selected="true" aria-controls="p-in"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 11l8-7 8 7"/><path d="M6 10v10h12V10"/></svg>Início</button>
  <button class="tab" role="tab" id="t-cp" aria-selected="false" aria-controls="p-cp"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3l7 4v8l-7 4-7-4V7z"/><path d="M12 11v8M5 7l7 4 7-4"/></svg>Compostos</button>
  <button class="tab" role="tab" id="t-ic" aria-selected="false" aria-controls="p-ic"><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="6.5"/><path d="M20 20l-4.4-4.4"/></svg>Identificar</button>
  <button class="tab" role="tab" id="t-en" aria-selected="false" aria-controls="p-en"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M9 3h6"/><path d="M10 3v6l-5 9a2 2 0 0 0 2 3h10a2 2 0 0 0 2-3l-5-9V3"/></svg>Ensaios</button>
  <button class="tab" role="tab" id="t-sp" aria-selected="false" aria-controls="p-sp"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 12h3.5l2-6 4 12 2.5-6H21"/></svg>Espectros</button>
  <button class="tab" role="tab" id="t-ma" aria-selected="false" aria-controls="p-ma"><svg viewBox="0 0 24 24" aria-hidden="true"><circle class="dot" cx="5.5" cy="12" r="1.6"/><circle class="dot" cx="12" cy="12" r="1.6"/><circle class="dot" cx="18.5" cy="12" r="1.6"/></svg>Mais</button>
</nav>

''')
rep('.bnav .tab{flex:1;max-width:170px;','.bnav .tab{flex:1;min-width:0;max-width:170px;')
rep('font-size:.74rem;padding:7px 4px 8px','font-size:.68rem;padding:7px 2px 8px')
# SCR / OWN / NAV
rep("'p-pq','p-sl','p-co','p-es','p-pr','p-pg'];","'p-pq','p-sl','p-co','p-es','p-pg','p-cp','p-cf','p-ic','p-sp','p-rm','p-ob'];")
OWN="const OWN={'p-ec':'t-en','p-pb':'t-en','p-cs':'t-en','p-pf':'t-en','p-so':'t-en','p-el':'t-en','p-id':'t-en','p-tr':'t-sp','p-tb':'t-sp','p-an':'t-sp','p-iv':'t-sp','p-rm':'t-sp','p-cf':'t-cp','p-ob':'t-in','p-ca':'t-ma','p-aj':'t-ma','p-fo':'t-ma','p-pq':'t-ma','p-sl':'t-ma','p-co':'t-ma','p-es':'t-ma','p-pg':'t-ma'};"
T=re.sub(r"const OWN=\{[^\n]*\};",OWN,T,1)
rep("const NAV=['t-in','t-en','t-iv','t-an','t-ma'];","const NAV=['t-in','t-cp','t-ic','t-en','t-sp','t-ma'];")
rep("  if(id==='p-pr')drawPerg();\n","")
rep("  if(id==='p-an')drawHoje();\n","")
# cronograma / prova
T=re.sub(r"const CRON=\[\[[^\n]*\n","",T,1)
T=re.sub(r"function agInit2\(\)\{[^\n]*\n","function agInit2(){}\n",T,1)
cut("  const h=agHoje(),lim=new Date(2026,10,3);","  sgmBind('so','so-')","function agInit(){\n") if False else None
i=T.index("function agInit(){"); j=T.index("  sgmBind('so','so-')",i); T=T[:i]+"function agInit(){\n"+T[j:]
rep("  if(id==='p-in')agInit2();\n","")
# rótulos 'Ex. N'
rep("(isStud(e.n)?'✓ ':'')+'Ex. '+e.n+' '+e.nome","(isStud(e.n)?'✓ ':'')+e.nome")
rep("<b>Ex. '+ex.n+': '+esc(ex.nome)","<b>'+esc(ex.nome)")
T=T.replace("refs.push('Ex. '+e.n+' ('+r[1]+' → '+r[0]+')')","refs.push(e.nome+' ('+r[1]+' → '+r[0]+')')").replace("refs.push('Ex. '+e.n)","refs.push(e.nome)")
T=T.replace("'Ex. '+c.n+' '+e.nome","e.nome").replace("'Ex. '+e.n+': '+e.nome","e.nome").replace("'Ex. '+c.n:'Etanol'","EX.find(x=>x.n===c.n).nome:'Etanol'")
T=T.replace("'Exercício '+e.n+': ","''+e.nome+': ")
rep("const VERSAO='v9 · 15/10/2026';","const VERSAO='v10 · 04/11/2026';")
# módulos novos
rep('/* ---------- Analorg: módulos novos','/*@@ANALORG2_JS@@*/\n/* ---------- Analorg: módulos novos')
rep("go('p-in');\n(function(){","cpInit();icInit();obInit();\ngo('p-in');\n(function(){")
rep('/* BEGIN temas */','/*@@ANALORG2_CSS@@*/\n/* BEGIN temas */')
i=T.index('<nav class="bnav"'); T=T[:i].rstrip()[:-len('</div>')].rstrip()+'\n\n'+open('analorg2.html',encoding='utf-8').read()+'\n</div>\n\n'+T[i:] if False else T
j=T.rindex('</div>',0,T.index('<nav class="bnav"'))
T=T[:j]+open('analorg2.html',encoding='utf-8').read()+'\n'+T[j:]
open('template.html','w',encoding='utf-8').write(T)
print('ok')
