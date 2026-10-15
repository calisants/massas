import re
p='template.html'; s=open(p,encoding='utf-8').read()
def rep(a,b,cnt=1):
    global s
    assert a in s,a[:70]; s=s.replace(a,b,cnt)

# ---------- CSS ----------
rep("padding-inline:16px;padding-block:20px 48px}","padding-inline:16px;padding-block:18px 96px}")
rep("@media (prefers-reduced-motion:no-preference){.card{","""h1{font-size:1.15rem}
.scr{font-size:1.25rem;margin:4px 0 2px}.scrsub{color:var(--muted);margin:0 0 14px;max-width:70ch}
.bnav{position:fixed;left:0;right:0;bottom:0;z-index:20;display:flex;justify-content:center;background:var(--surface);border-top:1px solid var(--line);padding-bottom:env(safe-area-inset-bottom)}
.bnav .tab{flex:1;max-width:170px;display:flex;flex-direction:column;align-items:center;gap:1px;font-size:.74rem;padding:7px 4px 8px;margin:0;border:0;border-top:3px solid transparent;color:var(--muted)}
.bnav .tab[aria-selected="true"]{color:var(--keep);border-top-color:var(--keep);border-bottom:0}
.bnav svg{width:22px;height:22px;stroke:currentColor;fill:none;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round}
.bnav svg .dot{fill:currentColor;stroke:none}
.seg{display:flex;margin:0 0 14px}
.seg button{flex:1;font:inherit;font-weight:500;background:var(--surface);color:var(--ink);border:1px solid var(--line);padding:8px 6px;cursor:pointer}
.seg button:first-child{border-radius:6px 0 0 6px}.seg button:last-child{border-radius:0 6px 6px 0}.seg button+button{border-left:0}
.seg button[aria-pressed="true"]{background:var(--keep);border-color:var(--keep);color:var(--surface)}
.menu{display:grid;gap:10px}
.mi{font:inherit;text-align:left;background:var(--surface);color:var(--ink);border:1px solid var(--line);border-radius:6px;padding:14px 16px;cursor:pointer;display:grid;gap:2px}
.mi b{font-weight:600}.mi span{color:var(--muted);font-size:.9rem}
.back{font:inherit;background:none;border:0;color:var(--keep);font-weight:500;padding:4px 0;margin:0 0 8px;cursor:pointer}
#out.single{grid-template-columns:1fr}
.pkh{margin:6px 0 4px;font-size:.9rem;color:var(--muted)}
@media (prefers-reduced-motion:no-preference){.card{""")

# ---------- cabeçalho + navegação inferior ----------
a=s.index('  <h1>Quebra-cabeça de massas</h1>'); b=s.index('  <section id="p-an"')
s=s[:a]+'  <h1>Quebra-cabeça de massas</h1>\n\n'+s[b:]
ICON={'an':'<circle cx="11" cy="11" r="6.5"/><path d="M20 20l-4.4-4.4"/>',
      'tr':'<circle cx="12" cy="12" r="8.5"/><circle cx="12" cy="12" r="4.5"/><circle class="dot" cx="12" cy="12" r="1.2"/>',
      'tb':'<path d="M5 4h13v16H7a2 2 0 0 1-2-2z"/><path d="M5 18a2 2 0 0 1 2-2h11"/>',
      'iv':'<path d="M3 12h3.5l2-6 4 12 2.5-6H21"/>',
      'ma':'<circle class="dot" cx="5.5" cy="12" r="1.6"/><circle class="dot" cx="12" cy="12" r="1.6"/><circle class="dot" cx="18.5" cy="12" r="1.6"/>'}
LAB={'an':'Analisar','tr':'Treinar','tb':'Livro','iv':'IV','ma':'Mais'}
nav='<nav class="bnav" role="tablist" aria-label="Seções">\n'+''.join(
 f'  <button class="tab" role="tab" id="t-{k}" aria-selected="{"true" if k=="an" else "false"}" aria-controls="p-{k}"><svg viewBox="0 0 24 24" aria-hidden="true">{ICON[k]}</svg>{LAB[k]}</button>\n' for k in ['an','tr','tb','iv','ma'])+'</nav>\n'
rep('<script>\n/* ---------- dados: Apêndice C', nav+'\n<script>\n/* ---------- dados: Apêndice C')

# ---------- tela Analisar ----------
a=s.index('  <section id="p-an"'); b=s.index('    <div>Exercícios da lista')
how_start=s.index('    <div class="how">',a)
# extrai o bloco "how" e o <details> do glossário para a tela de ajuda
how_block=s[how_start:s.index('    <details><summary>O que significam',a)]
gl_block=s[s.index('    <details><summary>O que significam',a):b]
s=s[:a]+'''  <section id="p-an" role="tabpanel" aria-labelledby="t-an">
    <h2 class="scr">Analisar</h2>
    <p class="scrsub">Escolha um exercício ou digite M e os picos. Depois toque num pico para ver o que ficou e o que saiu. <button class="back" style="display:inline;margin:0" data-go="p-aj">Como ler um pico?</button></p>
'''+s[b:]
rep('    <div class="grid" id="out"></div>','    <div class="pkh" id="pkh"></div>\n    <div class="chips" id="pkbar" role="group" aria-label="Escolha o pico"></div>\n    <div class="grid" id="out"></div>')
rep("    <div>Exercícios da lista (carregam M e os picos). Nos seus PDFs a numeração vai de 10 direto para 12.</div>","    <div>Exercícios da lista (carregam M e os picos). Nos seus PDFs a numeração vai de 10 direto para 12.</div>")

# JS: um pico por vez
rep("  let html='';\n","  const cards={};\n")
rep("""    html+='<div class="card">'+head+'<div class="cols">'+body+'</div>'+ans+'</div>';""","""    cards[p]='<div class="card">'+head+'<div class="cols">'+body+'</div>'+ans+'</div>';""")
rep("  $('#out').innerHTML=html;","""  if(pkSel!=='all'&&!peaks.includes(pkSel))pkSel=peaks[0];
  $('#pkh').textContent='Toque num pico:';
  $('#pkbar').innerHTML='';
  peaks.forEach(p=>{const b=document.createElement('button');b.type='button';b.className='chip mono';b.setAttribute('aria-pressed',pkSel===p?'true':'false');b.textContent='m/z '+p+(p===M?' (M)':'');b.onclick=()=>{pkSel=p;analyze();};$('#pkbar').appendChild(b);});
  if(peaks.length>1){const b=document.createElement('button');b.type='button';b.className='chip';b.setAttribute('aria-pressed',pkSel==='all'?'true':'false');b.textContent='Todos';b.onclick=()=>{pkSel='all';analyze();};$('#pkbar').appendChild(b);}
  $('#out').className=pkSel==='all'?'grid':'grid single';
  $('#out').innerHTML=pkSel==='all'?peaks.map(p=>cards[p]).join(''):cards[pkSel];""")
rep("let curEx=null;","let curEx=null,pkSel=null;")
rep("b.onclick=()=>{curEx=e.n;$('#inM')","b.onclick=()=>{curEx=e.n;pkSel=null;$('#inM')")
rep("$('#go').onclick=()=>{curEx=null;buildChips();analyze();};","$('#go').onclick=()=>{curEx=null;pkSel=null;buildChips();analyze();};")
rep("""if(!M||!peaks.length){$('#out').innerHTML='<p class="empty">Digite M e pelo menos um pico.</p>';$('#pairs').innerHTML='';return;}""","""if(!M||!peaks.length){$('#out').innerHTML='<p class="empty">Digite M e pelo menos um pico.</p>';$('#pairs').innerHTML='';$('#pkbar').innerHTML='';$('#pkh').textContent='';return;}""")
# perdas entre picos: recolhido
rep("""'<h2>Perdas entre dois picos</h2><p class="hint">Quando um fragmento perde mais um pedaço, a diferença entre os dois picos também aparece no Apêndice C.</p><div class="pairs">'""","""'<details><summary>Perdas entre dois picos ('+prs.length+')</summary><p class="hint" style="margin-top:8px">Quando um fragmento perde mais um pedaço, a diferença entre os dois picos também aparece no Apêndice C.</p><div class="pairs">'""")
m=re.search(r"(\$\('#pairs'\)\.innerHTML=prs\.length\?.*?\.join\(''\)\+'</div>)(':'';)",s,re.S); assert m
s=s.replace(m.group(0),m.group(1)+"</details>"+m.group(2),1)

# ---------- Livro, Treinar: títulos ----------
rep('<section id="p-tr" role="tabpanel" aria-labelledby="t-tr" hidden>\n    <p class="hint">','<section id="p-tr" role="tabpanel" aria-labelledby="t-tr" hidden>\n    <h2 class="scr">Treinar</h2>\n    <p class="scrsub">')
rep('<section id="p-tb" role="tabpanel" aria-labelledby="t-tb" hidden>\n','<section id="p-tb" role="tabpanel" aria-labelledby="t-tb" hidden>\n    <h2 class="scr">Livro</h2>\n    <p class="scrsub">Tabelas do Silverstein: o que saiu (Apêndice C) e o que ficou (Apêndice B).</p>\n')

# ---------- tela IV com 3 sub-páginas ----------
a=s.index('  <section id="p-iv"'); b=s.index('  <section id="p-ca"')
iv=s[a:b]
how_iv=iv[iv.index('    <div class="how">'):iv.index('    <details><summary>Por que')]
why=iv[iv.index('    <details><summary>Por que'):iv.index('    <details><summary>Guia por região')]
why_inner=why.replace('<details><summary>Por que cada banda aparece onde aparece?</summary><dl>','<h2>Por que cada banda aparece onde aparece?</h2><dl>').replace('</dl></details>','</dl>')
hintf=iv[iv.index('    <p class="hint">Fontes:'):iv.index('    <div class="chips" id="ivchips">')]
newiv=f'''  <section id="p-iv" role="tabpanel" aria-labelledby="t-iv" hidden>
    <h2 class="scr">IV</h2>
    <div class="seg" role="group" aria-label="Partes do IV">
      <button type="button" data-v="v-comp" aria-pressed="true">Composto</button>
      <button type="button" data-v="v-num" aria-pressed="false">Número de onda</button>
      <button type="button" data-v="v-guia" aria-pressed="false">Guia</button>
    </div>
    <div id="v-comp">
      <p class="scrsub">Escolha um composto para ver as bandas dele e a pista para o espectro de massas.</p>
      <div class="chips" id="ivchips"></div>
      <div id="ivout"></div>
    </div>
    <div id="v-num" hidden>
      <p class="scrsub">Digite uma banda e veja que grupo ela pode ser e com qual outra banda confirmar.</p>
      <label for="ivq">Número de onda (cm⁻¹)<input class="f-m" type="number" id="ivq" inputmode="numeric" min="400" max="4000" placeholder="ex.: 1712"></label>
      <div id="ivres"></div>
    </div>
    <div id="v-guia" hidden>
{how_iv}
{why_inner}
      <h2 style="margin-top:18px">Guia por região (da apostila)</h2>
      <div id="ivreg"></div>
{hintf}
    </div>
  </section>

'''
s=s[:a]+newiv+s[b:]

# ---------- tela Mais e sub-telas ----------
a=s.index('  <section id="p-ca"'); b=s.index('  <p class="foot">'); c=s.index('</div>\n\n'+nav.split('\n')[0]) if False else None
calc=s[a:b]
foot_start=b; foot_end=s.index('</p>',b)+4
foot=s[foot_start:foot_end]
calc2=calc.replace('<section id="p-ca" role="tabpanel" aria-labelledby="t-ca" hidden>','<section id="p-ca" role="region" aria-label="Calculadora" hidden>\n    <button class="back" data-go="p-ma">← Mais</button>\n    <h2 class="scr">Calculadora de massa</h2>')
mais='''  <section id="p-ma" role="tabpanel" aria-labelledby="t-ma" hidden>
    <h2 class="scr">Mais</h2>
    <div class="menu">
      <button class="mi" type="button" data-go="p-ca"><b>Calculadora de massa</b><span>Some a fórmula de um pedaço e veja o que o livro lista para esse número.</span></button>
      <button class="mi" type="button" data-go="p-aj"><b>Como ler um pico e glossário</b><span>Os 4 passos, o que são +, +· e ·, clivagem α e McLafferty.</span></button>
      <button class="mi" type="button" data-go="p-fo"><b>Fontes e avisos</b><span>De onde vêm as tabelas e o que ainda precisa de conferência.</span></button>
    </div>
  </section>

'''
gl=gl_block.replace('<details><summary>O que significam esses termos?</summary><dl id="glos"></dl></details>','<h2 style="margin-top:18px">Glossário</h2><dl id="glos" class="gl"></dl>')
ajuda='''  <section id="p-aj" role="region" aria-label="Como ler um pico" hidden>
    <button class="back" data-go="p-ma">← Mais</button>
    <h2 class="scr">Como ler um pico</h2>
'''+how_block+gl+'''  </section>

'''
fonte='''  <section id="p-fo" role="region" aria-label="Fontes e avisos" hidden>
    <button class="back" data-go="p-ma">← Mais</button>
    <h2 class="scr">Fontes e avisos</h2>
    '''+foot.replace('<p class="foot">','<p>')+'''
  </section>
'''
s=s[:a]+mais+calc2+'\n'+ajuda+fonte+s[foot_end:]
s=s.replace(".gl{display:grid;gap:8px}","")
rep(".mhint{",".gl{margin:10px 0 0;display:grid;gap:8px}.gl dt{font-weight:600}.gl dd{margin:0;color:var(--muted)}\n.mhint{")

# ---------- roteador ----------
a=s.index("const tabs=[['t-an'"); b=s.index("/* ---------- início:")
router='''const SCR=['p-an','p-tr','p-tb','p-iv','p-ma','p-ca','p-aj','p-fo'];
const OWN={'p-ca':'t-ma','p-aj':'t-ma','p-fo':'t-ma'};
const NAV=['t-an','t-tr','t-tb','t-iv','t-ma'];
function go(id){
  SCR.forEach(x=>{$('#'+x).hidden=x!==id;});
  const own=OWN[id]||('t-'+id.slice(2));
  NAV.forEach(t=>$('#'+t).setAttribute('aria-selected',t===own?'true':'false'));
  if(id==='p-tr'&&!q)newQ();
  window.scrollTo(0,0);
}
NAV.forEach((t,i)=>{const el=$('#'+t);
  el.onclick=()=>go('p-'+t.slice(2));
  el.addEventListener('keydown',ev=>{const d=ev.key==='ArrowRight'?1:ev.key==='ArrowLeft'?-1:0;if(!d)return;ev.preventDefault();const n=NAV[(i+d+NAV.length)%NAV.length];$('#'+n).focus();$('#'+n).click();});});
document.addEventListener('click',ev=>{const b=ev.target.closest('[data-go]');if(b)go(b.dataset.go);});
document.querySelectorAll('.seg').forEach(g=>g.querySelectorAll('button').forEach(b=>{b.onclick=()=>{
  g.querySelectorAll('button').forEach(x=>x.setAttribute('aria-pressed',x===b?'true':'false'));
  ['v-comp','v-num','v-guia'].forEach(id=>{$('#'+id).hidden=id!==b.dataset.v;});};}));

'''
s=s[:a]+router+s[b:]
open(p,'w',encoding='utf-8').write(s)
print('ok')
