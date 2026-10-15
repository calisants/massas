import re,sys
sys.path.insert(0,'.')
from svgmodels import MODELS
t=open('template.html',encoding='utf-8').read()
def rep(a,c,count=1):
    global t
    assert a in t,a[:70]; t=t.replace(a,c,count)

# ---------- CSS
rep('*{box-sizing:border-box}','''*{box-sizing:border-box}
:root{--arrow:#1F5FA8}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--arrow:#8FB8F0}}
:root[data-theme="dark"]{--arrow:#8FB8F0}
.why summary,.rearr summary{cursor:pointer;font-weight:600;color:var(--note)}
.why[open] summary{margin-bottom:8px}
.tag{font-size:.72rem;border-radius:4px;padding:1px 6px;background:var(--line);color:var(--muted);font-weight:500;margin-left:6px;white-space:nowrap}
.src{font-size:.82rem;color:var(--muted);margin:8px 0 0}
.nota{width:100%;min-height:64px;font:inherit;background:var(--surface);color:var(--ink);border:1px solid var(--line);border-radius:6px;padding:8px;resize:vertical}
.chipbar{display:flex;flex-wrap:wrap;gap:6px;margin:0 0 14px}
.optb{display:block;width:100%;text-align:left;font:inherit;background:var(--surface);color:var(--ink);border:1px solid var(--line);border-radius:6px;padding:10px 12px;margin:0 0 8px;cursor:pointer}
.optb.good{background:var(--keep-soft);border-color:var(--keep)}
.optb.bad{background:var(--lost-soft);border-color:var(--lost)}
.optb[disabled]{cursor:default}
.mdl{background:var(--surface);border:1px solid var(--line);border-radius:6px;padding:12px 14px;margin-bottom:12px}
.mdl h3{margin:0 0 4px;font-size:1rem}.mdl p{margin:0 0 6px}
.ctx{margin:0 0 10px}
.stud{font:inherit;font-size:.82rem;background:var(--surface);color:var(--ink);border:1px solid var(--line);border-radius:999px;padding:3px 10px;cursor:pointer}
.stud[aria-pressed="true"]{background:var(--keep);color:var(--surface);border-color:var(--keep)}''')

# ---------- HTML: Treinar, menu, telas novas
rep('    <div class="quiz" id="quiz"></div>','    <div class="chipbar" id="trmode" role="group" aria-label="Modo de treino"></div>\n    <div class="quiz" id="quiz"></div>')
rep('''      <button class="mi" type="button" data-go="p-pq">''','''      <button class="mi" type="button" data-go="p-es"><b>Espectro novo (modo detetive)</b><span>Digite fórmula, picos e bandas de IV de um composto desconhecido e veja as pistas.</span></button>
      <button class="mi" type="button" data-go="p-se"><b>Setas dos mecanismos</b><span>Modelos com setas de anzol e seta inteira para os mecanismos que se repetem.</span></button>
      <button class="mi" type="button" data-go="p-pq">''')
SE='''
  <section id="p-se" role="region" aria-label="Setas dos mecanismos" hidden>
    <button class="back" data-go="p-ma">← Mais</button>
    <h2 class="scr">Setas dos mecanismos</h2>
    <p class="hint"><b>Seta de anzol</b> (meia ponta) = 1 elétron andando. <b>Seta inteira</b> (ponta cheia) = um par de elétrons andando. Os números mostram a ordem. Os modelos usam letras genéricas (Y = N ou O, R = grupo alquila). Para ver onde cada um aparece, abra o &ldquo;Por que quebra aqui?&rdquo; do pico.</p>
    <div class="mdl"><h3>0. Ionização</h3>'''+MODELS['ioniz']+'''<p>O elétron mais fácil de tirar é o do par livre. Sobra um elétron sozinho no O (ou no N) e carga +. É o ponto de partida de quase todos os mecanismos.</p></div>
    <div class="mdl"><h3>1. Clivagem α (homolítica)</h3>'''+MODELS['alfa']+'''<p><b>1:</b> o elétron sozinho de Y forma a ligação dupla com o carbono. <b>2:</b> 1 elétron da ligação C–R vai com o R, que sai como radical. A carga fica em Y. Aparece em: 1-propanol (31), 3-pentanona (57), dimetiletilamina (58), benzofenona (105).</p></div>
    <div class="mdl"><h3>2. McLafferty (homolítica, em sequência)</h3>'''+MODELS['mcl']+'''<p><b>1:</b> o H do carbono γ passa para o O (anel de 6 átomos). <b>2:</b> 1 elétron da ligação Cα–Cβ forma a ligação dupla Cβ=Cγ. <b>3:</b> o elétron da ligação π do C=O forma a nova ligação dupla com o Cα. Sai um alqueno neutro e fica o enol⁺·. Aparece em: ácido butanoico (60), pentanoato de metila (74), pentanal (44).</p></div>
    <div class="mdl"><h3>3. Cátion acílio perde CO (heterolítica)</h3>'''+MODELS['hetero']+'''<p>Aqui a seta é inteira: o par de elétrons da ligação R–C vai para o carbono do CO. O CO sai neutro levando o par, e a carga fica no R. Aparece em: 85 → 57 (pentanal e pentanoato), 105 → 77 (benzofenona), 57 → 29 (3-pentanona).</p></div>
    <div class="mdl"><h3>4. Perda de H· (M − 1)</h3>'''+MODELS['h']+'''<p><b>1:</b> o elétron sozinho de Y forma a ligação dupla. <b>2:</b> 1 elétron da ligação C–H vai com o H, que sai como radical. Aparece em: dimetiletilamina (72), pentanal (85).</p></div>
    <p class="hint">Estes são modelos. A lousa do professor vale para a prova: se ele desenhar de outro jeito, siga o dele.</p>
  </section>

  <section id="p-es" role="region" aria-label="Espectro novo" hidden>
    <button class="back" data-go="p-ma">← Mais</button>
    <h2 class="scr">Espectro novo (modo detetive)</h2>
    <p class="hint">Para um composto que você ainda não resolveu. Preencha o que tiver. O app dá pistas, não a resposta: quem decide é você.</p>
    <div class="row">
      <label for="esF">Fórmula (opcional)<input type="text" id="esF" placeholder="ex.: C6H12O2"></label>
      <label for="esM">M<input type="number" id="esM" class="f-m" inputmode="numeric" placeholder="ex.: 116"></label>
    </div>
    <label for="esP">Picos do espectro de massas<input type="text" id="esP" class="f-p" placeholder="ex.: 87, 85, 74, 57, 43, 29"></label>
    <label for="esI" style="margin-top:10px">Bandas do IV (cm⁻¹)<input type="text" id="esI" class="f-p" placeholder="ex.: 2960, 1743, 1250"></label>
    <div id="esOut" style="margin-top:16px"></div>
  </section>

'''
rep('  <section id="p-fo" role="region" aria-label="Fontes e avisos" hidden>',SE+'  <section id="p-fo" role="region" aria-label="Fontes e avisos" hidden>')
rep("const SCR=['p-an','p-tr','p-tb','p-iv','p-ma','p-ca','p-aj','p-fo','p-pq','p-co'];","const SCR=['p-an','p-tr','p-tb','p-iv','p-ma','p-ca','p-aj','p-fo','p-pq','p-co','p-se','p-es'];")
rep("'p-pq':'t-ma','p-co':'t-ma'};","'p-pq':'t-ma','p-co':'t-ma','p-se':'t-ma','p-es':'t-ma'};")
rep("if(id==='p-tr'&&!q)newQ();","if(id==='p-tr')trInit();")

# ---------- whyBox novo (porquê escondido) + selos
i=t.index('function rearrBox(ex,row){'); j=t.index('function stepCard(ex,row){')
NEWBOX=r'''const POSS=['3:78','8:52','10:44','2:39','11:87'];
function origemTxt(ex){return ex.ok?'Massa, estrutura e mecanismo: da lousa do professor. O porquê é explicação minha, baseada no Silverstein.':'Ainda não conferido com o professor: tudo aqui é minha leitura do livro.';}
function cisTxt(r){
  const k=tipoQ(r);
  if(k==='neu')return '<b>heterolítica</b>: o cátion solta uma molécula neutra e o par de elétrons da ligação vai com ela (seta inteira).';
  if(k==='anel')return 'começa <b>homolítica</b> (abre a ligação ao lado do heteroátomo, setas de anzol) e termina soltando uma molécula neutra.';
  if(k==='mcl')return '<b>homolítica</b> (setas de anzol): o H pula com 1 elétron e a ligação α–β se rompe, saindo um alqueno neutro.';
  return '<b>homolítica</b> (seta de anzol): cada lado fica com 1 elétron, e o pedaço que sai é um radical.';
}
function rearrBox(ex,row){
  const r=(typeof REARR!=='undefined')&&REARR[ex.n+':'+row[0]];if(!r)return '';
  const poss=POSS.indexOf(ex.n+':'+row[0])>=0;
  let h='<details class="why rearr"><summary>Possível rearranjo (mesma massa)<span class="tag">'+(poss?'possibilidade':'bem descrito')+'</span></summary><p>'+fmt(esc(r[0]))+'</p>';
  if(r[1].length){h+='<div class="sp">'+r[1].map((s,i)=>(i?'<span class="op">⇄</span>':'')+fig(s[0],s[1],'keep','forma')).join('')+'</div>';}
  return h+'<p class="src">Na prova, desenhe só o que o professor desenhou.</p></details>';
}
function whyBox(ex,row){
  const w=(typeof WHY!=='undefined')&&WHY[ex.n+':'+row[0]];if(!w)return '';
  const k=tipoQ(row),mdl=({alfa:1,mcl:1,neu:1,h:1})[k];
  return '<details class="why"><summary>Mostrar o porquê</summary><p><b>Onde começa.</b> '+esc(w[0])+'</p><p><b>O que acontece.</b> '+fmt(esc(w[1]))+'</p><p><b>Por que aqui e não em outro lugar.</b> '+fmt(esc(w[2]))+'</p><p><b>Tipo de cisão.</b> '+cisTxt(row)+'</p><p class="src">'+origemTxt(ex)+'</p><p><small>'+(mdl?'<button class="back" style="display:inline;margin:0" data-go="p-se">Ver o modelo com setas</button> · ':'')+'<button class="back" style="display:inline;margin:0" data-go="p-pq">Ver as regras</button></small></p></details>'+rearrBox(ex,row);
}
'''
t=t[:i]+NEWBOX+t[j:]

# ---------- cartão: anotações, estudado, chips
rep("""cards[p]='<div class="card">'+head+'<div class="cols">'+body+'</div>'+ans+'</div>';""","""cards[p]='<div class="card">'+head+'<div class="cols">'+body+'</div>'+ans+(ex?notaBox(ex,p):'')+'</div>';""")
rep("$('#nrule').innerHTML=M?","decorateEx(ex);$('#nrule').innerHTML=M?")
rep("b.textContent='Ex. '+e.n+' '+e.nome;","b.textContent=(isStud(e.n)?'✓ ':'')+'Ex. '+e.n+' '+e.nome;")

JS=r'''
/* ---------- armazenamento (com proteção) ---------- */
const VERSAO='v9 · 15/10/2026';
const LS={get(k,d){try{const v=localStorage.getItem(k);return v==null?d:JSON.parse(v);}catch(e){return d;}},set(k,v){try{localStorage.setItem(k,JSON.stringify(v));}catch(e){}}};
const isStud=n=>(LS.get('massas-stud',[])).indexOf(n)>=0;
function decorateEx(ex){
  const h=document.querySelector('#exinfo .ex-head');if(!ex||!h)return;
  const b=document.createElement('button');b.type='button';b.className='stud';b.dataset.n=ex.n;b.setAttribute('aria-pressed',isStud(ex.n)?'true':'false');b.textContent=isStud(ex.n)?'✓ estudado':'marcar como estudado';h.appendChild(b);
}
function notaBox(ex,p){
  const v=LS.get('massas-nota-'+ex.n+'-'+p,'');
  return '<details class="why" '+(v?'open':'')+'><summary>Minha anotação (o que o professor disse)</summary><textarea class="nota" data-k="massas-nota-'+ex.n+'-'+p+'" placeholder="Escreva aqui. Fica salvo só neste aparelho.">'+esc(v)+'</textarea></details>';
}
document.addEventListener('input',ev=>{const a=ev.target.closest&&ev.target.closest('.nota');if(a)LS.set(a.dataset.k,a.value);});
document.addEventListener('click',ev=>{const b=ev.target.closest&&ev.target.closest('.stud');if(!b)return;
  const n=+b.dataset.n;let s=LS.get('massas-stud',[]);s=s.indexOf(n)>=0?s.filter(x=>x!==n):s.concat([n]);LS.set('massas-stud',s);
  b.setAttribute('aria-pressed',isStud(n)?'true':'false');b.textContent=isStud(n)?'✓ estudado':'marcar como estudado';buildChips();});

/* ---------- Treinar: modos ---------- */
const REGRA={
 alfa:['Clivagem α','O elétron sozinho do N ou do O puxa a ligação vizinha e o grupo sai como radical (regra 2).'],
 mcl:['McLafferty','O H do carbono γ pula para o O por um anel de 6 átomos e sai um alqueno neutro (regra 5).'],
 neu:['Cátion solta molécula neutra','Um cátion sem elétron sozinho solta CO, eteno, etc., e não um radical (regra 6).'],
 h:['Perda de H·','Sai o H mais fraco, o do carbono vizinho ao heteroátomo ou o do CHO (regra 7).'],
 benz:['Cisão benzílica','A ligação vizinha ao anel quebra porque o cátion benzila/tropílio é muito estável (regras 3 e 4).'],
 anel:['Abertura de anel','Uma ligação do anel abre ao lado do heteroátomo e depois sai uma molécula neutra (regra 7).'],
 sim:['Quebra simples','Uma ligação se rompe e o pedaço que sai leva o elétron sozinho (regras 3 e 4).']
};
const TR={mode:'qual',cur:null,i:0,score:{ok:0,n:0},hint:false,wrong:false};
function shuf(a){a=a.slice();for(let i=a.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[a[i],a[j]]=[a[j],a[i]];}return a;}
function trPool(){
  const all=[];EX.forEach(e=>e.rows.forEach(r=>all.push({e,r})));
  if(TR.mode==='rev'){const er=LS.get('massas-erros',[]);return all.filter(x=>er.indexOf(x.e.n+':'+x.r[0])>=0);}
  return all;
}
function lossQ(e,r){
  const d=r[1]-r[0],valid=CM.get(d)||[];
  const okL=valid.length?fmt(valid[0][0]):fmt(r[3]);
  let keys=[...CM.keys()].filter(k=>k!==d&&k>0&&Math.abs(k-d)<=20);
  if(keys.length<3)keys=[...CM.keys()].filter(k=>k!==d&&k>0);
  const wrong=shuf(keys).slice(0,3).map(k=>fmt(CM.get(k)[0][0]));
  const opts=shuf([{l:okL,ok:true}].concat(wrong.map(l=>({l,ok:false}))));
  return {p:'Saiu <b class="mono">'+d+'</b> ('+r[1]+' → '+r[0]+'). Qual fragmento poderia ter saído?',opts,
    fb:'Para '+d+' o livro lista: '+(valid.length?valid.map(x=>fmt(x[0])).join(' · '):'(nada)')+'. Neste exercício foi <b>'+fmt(r[3])+'</b>. Qual combina é decidido pelo grupo funcional.'};
}
function cisQ(r){
  const k=tipoQ(r);if(k==='anel')return null;
  const het=k==='neu';
  return {p:'Essa quebra foi homolítica ou heterolítica?',opts:[{l:'Homolítica (cada lado leva 1 elétron, sai um radical)',ok:!het},{l:'Heterolítica (um lado leva o par; sai molécula neutra)',ok:het}],
    fb:cisTxt(r)};
}
function regQ(r){
  const k=tipoQ(r),keys=Object.keys(REGRA).filter(x=>x!==k);
  const opts=shuf([{l:REGRA[k][0],ok:true}].concat(shuf(keys).slice(0,3).map(x=>({l:REGRA[x][0],ok:false}))));
  return {p:'Qual regra explica esse pico?',opts,fb:'<b>'+REGRA[k][0]+'.</b> '+REGRA[k][1]};
}
function trNext(){
  const pool=trPool();
  if(!pool.length){TR.cur=null;trDraw();return;}
  const c=pool[Math.floor(Math.random()*pool.length)];
  const qs=[lossQ(c.e,c.r)];
  if(TR.mode!=='qual'){const a=cisQ(c.r);if(a)qs.push(a);qs.push(regQ(c.r));}
  TR.cur={e:c.e,r:c.r,qs,i:0,pick:null,wrong:false,done:false};TR.hint=false;trDraw();
}
function trInit(){
  const bar=$('#trmode');
  if(!bar.dataset.ok){
    bar.dataset.ok=1;
    [['qual','Qual saiu?'],['try','Tente antes de ver'],['calc','Digitar a perda'],['rev','Revisar erros']].forEach(([m,l])=>{
      const b=document.createElement('button');b.type='button';b.className='chip';b.dataset.m=m;b.textContent=l;
      b.onclick=()=>{TR.mode=m;trInit();};bar.appendChild(b);});
  }
  bar.querySelectorAll('button').forEach(b=>{b.setAttribute('aria-pressed',b.dataset.m===TR.mode?'true':'false');
    if(b.dataset.m==='rev')b.textContent='Revisar erros ('+LS.get('massas-erros',[]).length+')';});
  if(TR.mode==='calc'){newQ();return;}
  trNext();
}
function trDraw(){
  const box=$('#quiz');
  if(!TR.cur){box.innerHTML='<p class="empty">'+(TR.mode==='rev'?'Nenhum erro guardado. Faça rodadas em &ldquo;Qual saiu?&rdquo; ou &ldquo;Tente antes de ver&rdquo;. Os erros aparecem aqui.':'Nada para treinar.')+'</p>';return;}
  const c=TR.cur,e=c.e,r=c.r;
  let h='<div class="k mono" style="color:var(--muted)">Acertos: '+TR.score.ok+' de '+TR.score.n+'</div>';
  h+='<p class="ctx">Molécula <b class="mono">'+fmt(e.f)+'</b> (M = '+e.M+')'+(TR.hint?': <b>'+esc(e.nome)+'</b>, '+esc(e.g):'')+'.</p>';
  if(!c.done){
    const q=c.qs[c.i];
    h+='<p><b>Pergunta '+(c.i+1)+' de '+c.qs.length+'.</b> '+q.p+'</p>';
    q.opts.forEach((o,k)=>{
      let cls='optb';if(c.pick!==null){if(o.ok)cls+=' good';else if(c.pick===k)cls+=' bad';}
      h+='<button type="button" class="'+cls+'" data-k="'+k+'"'+(c.pick!==null?' disabled':'')+'>'+o.l+'</button>';});
    if(c.pick!==null){
      h+='<div class="fb '+(q.opts[c.pick].ok?'good':'bad')+'">'+(q.opts[c.pick].ok?'Certo. ':'Ainda não. ')+q.fb+'</div>';
      h+='<div class="row" style="margin-top:10px"><button class="btn" id="trn" type="button">'+(c.i<c.qs.length-1?'Próxima pergunta':'Ver a resposta do exercício')+'</button></div>';
    }else{
      h+='<div class="row"><button class="btn ghost" id="trh" type="button">Dica: nome da molécula</button><button class="btn ghost" id="tro" type="button">Outra</button></div>';
    }
  }else{
    h+='<div class="ans" style="border-radius:6px"><span class="t">'+esc(e.nome)+'</span>'+stepCard(e,r)+(e.ok?'':'<br><i>Conferir com o professor.</i>')+'</div>';
    h+='<div class="row" style="margin-top:10px"><button class="btn" id="tro" type="button">Outra</button></div>';
  }
  box.innerHTML=h;
  box.querySelectorAll('.optb').forEach(b=>b.onclick=()=>{
    const k=+b.dataset.k,q=c.qs[c.i];c.pick=k;TR.score.n++;
    if(q.opts[k].ok)TR.score.ok++;else c.wrong=true;trDraw();});
  const n=$('#trn');if(n)n.onclick=()=>{
    if(c.i<c.qs.length-1){c.i++;c.pick=null;}else{
      c.done=true;const key=e.n+':'+r[0];let er=LS.get('massas-erros',[]);
      if(c.wrong){if(er.indexOf(key)<0)er.push(key);}else er=er.filter(x=>x!==key);
      LS.set('massas-erros',er);trInit.upd&&trInit.upd();}
    trDraw();};
  const o=$('#tro');if(o)o.onclick=trNext;
  const hh=$('#trh');if(hh)hh.onclick=()=>{TR.hint=true;trDraw();};
}

/* ---------- Espectro novo (detetive) ---------- */
const IRR=[
 [3650,3200,'O–H (álcool, fenol) ou N–H','Banda larga é O–H. Duas bandas finas é NH2 de amina primária. Uma banda fina é amina secundária.'],
 [3300,2500,'O–H de ácido carboxílico (se for uma banda muito larga)','Estende-se até ~2500, por cima dos C–H.'],
 [3320,3280,'≡C–H de alcino terminal','Banda fina e forte perto de 3300.'],
 [3100,3000,'C–H sp² (anel aromático ou alceno)','Acima de 3000 é sp²; abaixo de 3000 é sp³.'],
 [3000,2850,'C–H sp³ (CH3, CH2)','Quase todo composto orgânico tem.'],
 [2850,2800,'C–H de aldeído (1ª banda de Fermi)','Aldeído tem duas bandas: ~2820 e ~2720.'],
 [2750,2700,'C–H de aldeído (2ª banda de Fermi)','A banda perto de 2720 é a mais característica.'],
 [2260,2210,'C≡N (nitrilo)','Banda fina, intensidade média.'],
 [2260,2100,'C≡C (alcino)','Fraca; pode sumir se for simétrico.'],
 [1850,1650,'C=O','Veja o valor exato abaixo.'],
 [1680,1620,'C=C de alceno (ou C=O de amida)','C=C costuma ser fraca.'],
 [1600,1450,'Anel aromático (C=C)','Bandas perto de 1600, 1580, 1500 e 1450.'],
 [1470,1430,'Deformação de CH2/CH3','Quase todo composto com C sp³.'],
 [1390,1370,'CH3, deformação simétrica (guarda-chuva)',''],
 [1300,1000,'C–O (álcool, éter, éster, ácido) ou C–N','Éster costuma ter duas bandas fortes, ~1250 e ~1030.'],
 [900,690,'C–H fora do plano de anel aromático','750 + 700: monossubstituído. ~750: orto.']
];
function coHint(v){
  if(v>=1750&&v<=1735)return 'éster saturado (~1740)';
  if(v<1735&&v>=1720)return 'aldeído ou éster saturado (1740–1720)';
  if(v<1720&&v>=1705)return 'cetona ou ácido carboxílico (~1715–1710)';
  if(v<1705&&v>=1630)return 'amida, ou carbonila conjugada com anel ou C=C';
  if(v>1750)return 'anidrido, cloreto de acila ou cetona em anel pequeno (>1750)';
  return '';
}
const MSD={15:'CH3⁺',29:'C2H5⁺ ou HC≡O⁺',30:'CH2=NH2⁺ (amina primária)',31:'CH2=OH⁺ (álcool primário)',43:'C3H7⁺ ou CH3–C≡O⁺',44:'CH2=CH–OH⁺· (McLafferty de aldeído) ou CH3CH=NH2⁺',45:'CH3CH=OH⁺ (álcool secundário)',57:'C4H9⁺ ou CH3CH2–C≡O⁺',58:'McLafferty de metil-cetona, ou CH2=N⁺(CH3)2 (amina)',60:'McLafferty de ácido carboxílico (CH2=C(OH)2⁺·)',74:'McLafferty de éster metílico',77:'C6H5⁺ (anel monossubstituído)',91:'C7H7⁺ (benzila/tropílio: alquilbenzeno)',105:'C6H5–C≡O⁺ (benzoíla)'};
const MSL={1:'H·',15:'CH3·',17:'HO·',18:'H2O',26:'HC≡CH',27:'HC≡N',28:'CO ou CH2=CH2',29:'CH3CH2· ou ·CHO',31:'·OCH3',42:'CH2=CH–CH3',43:'C3H7· ou CH3–C≡O·',44:'CO2',45:'·OCH2CH3 ou ·COOH'};
function esRun(){
  const out=[];
  const F=$('#esF').value.trim().replace(/\s+/g,''),M=parseInt($('#esM').value,10);
  const peaks=[...new Set(($('#esP').value.match(/\d+/g)||[]).map(Number))].filter(p=>p>0).sort((a,b)=>b-a);
  const ir=($('#esI').value.match(/\d+/g)||[]).map(Number).filter(v=>v>=400&&v<=4000);
  if(F){const f=parseF(F);if(f){const X=(f.F||0)+(f.Cl||0)+(f.Br||0)+(f.I||0),idh=((2*(f.C||0)+2+(f.N||0)-(f.H||0)-X)/2);
    out.push('<div class="rule"><h3>Fórmula</h3><p><b>IDH = '+idh+'</b> (anéis + ligações π). '+(idh===0?'Sem anel, sem C=O, sem C=C.':idh===1?'1 anel ou 1 dupla (C=O, C=C).':idh>=4?'IDH ≥ 4 sugere anel aromático.':'')+'</p>'+(f.N?'<p>Tem N: M ímpar é esperado.</p>':'')+'</div>');}
    else out.push('<div class="rule"><h3>Fórmula</h3><p>Não entendi a fórmula. Use letras como C6H12O2.</p></div>');}
  if(M)out.push('<div class="rule"><h3>Regra do nitrogênio</h3><p>M = '+M+' é <b>'+(M%2?'ímpar → número ímpar de N':'par → zero ou número par de N')+'</b>.</p></div>');
  if(ir.length){
    let h='<div class="rule"><h3>IV: o que cada banda sugere</h3>';const fl={};
    ir.forEach(v=>{const m=IRR.filter(r=>v<=r[0]&&v>=r[1]);
      h+='<p><b class="mono">'+v+'</b>: '+(m.length?m.map(r=>r[2]+(r[3]?' <span style="color:var(--muted)">('+r[3]+')</span>':'')).join('; '):'sem região de tabela. Confira.');
      if(v>=1650&&v<=1850){const c=coHint(v);if(c)h+=' <b>Valor: '+c+'.</b>';fl.co=v;}
      h+='</p>';
      if(v>=2700&&v<=2730)fl.ald=1;if(v>=3200&&v<=3650)fl.oh=1;if(v>=1450&&v<=1610)fl.ar=1;if(v>=3000&&v<3100)fl.sp2=1;if(v>=3300&&v<=3500)fl.nh=1;});
    const g=[];
    if(fl.co&&fl.ald)g.push('C=O + C–H em ~2720: <b>aldeído</b>.');
    else if(fl.co&&fl.co>=1735&&fl.co<=1750)g.push('C=O em ~1740, sem 2720: <b>éster</b> (confira C–O em ~1250 e ~1030).');
    else if(fl.co&&fl.oh)g.push('C=O e O–H largo: <b>ácido carboxílico</b>, se o O–H for muito largo.');
    else if(fl.co)g.push('C=O sem 2720 e sem O–H: <b>cetona</b> (ou amida, se menor que ~1690).');
    else if(fl.oh)g.push('Sem C=O e com O–H: <b>álcool ou fenol</b>.');
    if(fl.ar)g.push('Bandas de anel: <b>aromático</b>. Veja 900–690 para o padrão de substituição.');
    if(g.length)h+='<p class="ex"><b>Pistas combinadas.</b><br>'+g.join('<br>')+'</p>';
    out.push(h+'</div>');
  }
  if(peaks.length){
    let h='<div class="rule"><h3>Massas: íons conhecidos</h3>';let any=false;
    peaks.forEach(p=>{if(MSD[p]){any=true;h+='<p><b class="mono">'+p+'</b>: '+MSD[p]+'</p>';}});
    if(!any)h+='<p>Nenhum dos picos está na lista curta de íons diagnósticos. Use a aba Analisar para o Apêndice B.</p>';
    out.push(h+'</div>');
    if(M){let h2='<div class="rule"><h3>Massas: perdas a partir de M</h3>';let any2=false;
      peaks.filter(p=>p<M).forEach(p=>{const d=M-p;if(MSL[d]){any2=true;h2+='<p><b class="mono">M − '+p+' = '+d+'</b>: '+MSL[d]+'</p>';}});
      if(!any2)h2+='<p>Nenhuma perda da lista curta. A aba Analisar usa o Apêndice C completo.</p>';
      out.push(h2+'</div>');}
  }
  $('#esOut').innerHTML=out.length?out.join('')+'<p class="hint">Pistas gerais. Elas não substituem a lousa nem o Apêndice B e C. Confirme com a aba Analisar.</p>':'<p class="empty">Preencha pelo menos um campo.</p>';
}
['#esF','#esM','#esP','#esI'].forEach(s=>$(s).addEventListener('input',esRun));
'''
rep("const SCR=[",JS+"\nconst SCR=[")
# ---------- ordem de estudo
rep('<div class="chips" id="exchips"></div>','''<details class="how" style="margin-bottom:10px"><summary style="cursor:pointer;font-weight:600">Em que ordem estudar?</summary><p class="hint" style="margin-top:8px">Do mais simples ao mais complexo: <b>6</b> (álcool, clivagem α) → <b>9</b> (ácido, McLafferty) → <b>5</b> (cetona) → <b>10</b> (amina) → <b>12</b> (aldeído) → <b>11</b> (éster) → <b>4</b> (benzofenona) → <b>1</b> (etilbenzeno) → <b>3</b> (estireno) → <b>8</b> (piridina) → <b>7</b> (dioxano) → <b>2</b> (furano). Os anéis ficam para o fim porque abrem e se rearranjam. Marque cada um como estudado depois de resolver.</p></details>
    <div class="chips" id="exchips"></div>''')
# ---------- versão
rep('<h2 class="scr">Fontes e avisos</h2>','<h2 class="scr">Fontes e avisos</h2>\n    <p class="hint">Versão do app: <b class="mono" id="vers"></b>. Se a data não for a mais recente, feche e abra o app duas vezes.</p>')
rep("const LS={get(k,d)","document.addEventListener('DOMContentLoaded',()=>{});\nconst LS={get(k,d)")
rep("const SCR=['p-an'","(function(){const v=document.getElementById('vers');if(v)v.textContent=VERSAO;})();\nconst SCR=['p-an'")
open('template.html','w',encoding='utf-8').write(t)
print('ok')
