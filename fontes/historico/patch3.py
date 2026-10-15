import re
s=open('template.html').read()
def rep(a,b,cnt=1):
    global s
    assert s.count(a)==cnt,(s.count(a),a[:90])
    s=s.replace(a,b)
# 1 origem
rep("function origemTxt(ex){return ex.ok?'Massa, estrutura e mecanismo: da lousa do professor. O porquê é explicação minha, baseada no Silverstein.'",
    "function origemTxt(ex){return ex.ok?(ex.n<=5?'Massa, estrutura e mecanismo: da lousa do professor, pelas suas anotações do tablet (iguais às fotos do quadro). O porquê é explicação minha, baseada no Silverstein.':'Massa, estrutura e mecanismo: da lousa do professor. O porquê é explicação minha, baseada no Silverstein.')")
rep("Exercícios 6 a 12 conferidos com a lousa do professor; 1 a 5 ainda precisam ser conferidos.","Exercícios 1 a 12 vêm da lousa do professor (os 1 a 5 pelas suas anotações do tablet, que são iguais às fotos do quadro; os 6 a 12 pelas fotos). O texto do porquê é minha explicação.")
m=re.search(r" \['Ex\. 1 a 5: conferir com a lousa'.*?\],\n",s);assert m
s=s.replace(m.group(0),'')
# 2 resumo + css
rep("return '<details class=\"why\"><summary>Mostrar o porquê</summary>","return resumoTxt(ex,row)+'<details class=\"why\"><summary>Mostrar o porquê</summary>")
rep("function whyBox(","function resumoTxt(ex,row){const t=(typeof RESUMO!=='undefined')&&RESUMO[ex.n+':'+row[0]];return t?'<p class=\"resumo\"><b>Resumo.</b> '+esc(t)+'</p>':'';}\nfunction whyBox(")
rep(".src{font-size:.82rem;color:var(--muted);margin:8px 0 0}",".src{font-size:.82rem;color:var(--muted);margin:8px 0 0}\n.resumo{margin:10px 0 4px;font-weight:500}\n.ionl{padding-left:18px;margin:6px 0}.ionl li{margin:7px 0}")
# 3 elétron: caixa + geral
rep("function decorateEx(ex){\n  const h=document.querySelector('#exinfo .ex-head');if(!ex||!h)return;",
"""function ionBox(ex){const d=(typeof IONI!=='undefined')&&IONI[ex.n];if(!d)return '';
  return '<details class="why ion"><summary>Por que o elétron saiu daí? (como nasce o M+·)</summary><p><b>'+esc(d[0])+'</b></p><ul class="ionl">'+d[1].map(c=>'<li><b>'+(c[1]===1?'✓ sai daqui: ':c[1]===2?'≈ quase empata: ':'✗ não sai daqui: ')+esc(c[0])+'.</b> '+esc(c[2])+'</li>').join('')+'</ul><p class="src">Ordem geral: par livre &lt; π &lt; σ. <button class="back" style="display:inline;margin:0" data-go="p-pq">Ver a explicação geral</button></p></details>';}
function decorateEx(ex){
  const h=document.querySelector('#exinfo .ex-head');if(!ex||!h)return;
  h.parentNode.insertAdjacentHTML('beforeend',ionBox(ex));""")
rep('<div class="rule"><h3>Antes de tudo: o que é o &ldquo;radical que some&rdquo;?</h3>','''<div class="rule"><h3>De onde o elétron sai primeiro? (a ionização)</h3>
      <p>O feixe arranca <b>1 elétron</b> da molécula, e sai o que está menos preso. Do mais fácil para o mais difícil:</p>
      <ol><li><b>Par livre (n)</b> de O ou N: não está em nenhuma ligação, só um núcleo o segura.</li><li><b>Elétron π</b> (C=C, C=O, anel): fica dividido entre dois núcleos e fora do eixo da ligação. Com conjugação, espalha-se ainda mais e fica mais fácil.</li><li><b>Elétron σ</b> (C–C, C–H): fica no eixo, entre dois núcleos, bem preso.</li></ol>
      <p><b>Desempates:</b></p>
      <ul><li><b>N contra O:</b> o N é menos eletronegativo e segura o par livre mais frouxo. Amina perde elétron mais fácil que álcool ou éter.</li><li><b>Par livre em ressonância fica mais preso:</b> o O do OH do ácido e o O do OCH3 do éster &ldquo;emprestam&rdquo; o par ao C=O. Por isso sai o par do O do C=O.</li><li><b>Conjugação facilita:</b> o estireno perde elétron mais fácil que o benzeno.</li><li><b>Sem par livre e sem π</b> (alcanos), só resta σ, e o M+· costuma ser fraco.</li></ul>
      <p>Cada exercício tem a caixa &ldquo;Por que o elétron saiu daí?&rdquo;. No Treinar, o modo <b>Elétron</b> pergunta isso.</p></div>

    <div class="rule"><h3>Antes de tudo: o que é o &ldquo;radical que some&rdquo;?</h3>''')
# 4 cubra e desenhe
rep('<h2 class="scr" style="margin-top:28px">Modelos com setas</h2>','<h2 class="scr" style="margin-top:28px">Modelos com setas</h2>\n    <p class="hint"><b>Treino de papel:</b> olhe um modelo por 20 segundos, cubra, e redesenhe as setas de memória. Depois descubra e compare. O app treina a escolha; só o papel treina a mão.</p>')
rep("h+='<div class=\"mdl\">'+(m?m.innerHTML:'')+'</div><div class=\"row\"","h+='<div class=\"mdl\">'+(m?m.innerHTML:'')+'</div><p class=\"hint\"><b>Agora no papel:</b> cubra o modelo e redesenhe as setas de memória.</p><div class=\"row\"")
# 5 sessões
rep("const TR={mode:'qual'","""function sessGate(){if(TR.sess>=5){sessEnd();return true;}TR.sess++;return false;}
function sessEnd(){
  const box=$('#quiz');TR.cur=null;
  box.innerHTML='<div class="ans" style="border-radius:6px"><span class="t">Sessão de 5 cartões completa</span>Perguntas certas: '+TR.score.ok+' de '+TR.score.n+'. O que você errou volta na aba Revisar amanhã. Pode parar por hoje.</div><div class="row" style="margin-top:10px"><button class="btn" id="sessMore" type="button">Mais 5 cartões</button><button class="btn ghost" id="sessStop" type="button">Terminei por hoje</button></div><p id="sessMsg" class="hint"></p>';
  $('#sessMore').onclick=trInit;
  $('#sessStop').onclick=()=>{$('#sessMsg').textContent='Bom trabalho. Pode fechar o app: o progresso já está guardado.';};
}
const TR={sess:0,mode:'qual'""")
rep("  if(!pool.length){TR.cur=null;trDraw();return;}\n","  if(!pool.length){TR.cur=null;trDraw();return;}\n  if(sessGate())return;\n")
rep("function setaNext(){\n","function setaNext(){\n  if(sessGate())return;\n")
rep("function trInit(){\n","function trInit(){\n  TR.sess=0;TR.score={ok:0,n:0};\n")
rep("Escolha um modo. ","Cada rodada tem 5 cartões e depois você pode parar. Escolha um modo. ")
# 6 modos
rep("['seta','Setas'],['sm','Simulado']","['ion','Elétron'],['seta','Setas'],['sm','Simulado']")
rep("  if(TR.mode==='seta'){setaNext();return;}","  if(TR.mode==='seta'){setaNext();return;}\n  if(TR.mode==='ion'){ionNext();return;}")
# 7 modo Elétron
rep("/* ---------- Simulado ---------- */","""/* ---------- Elétron: de onde sai? ---------- */
function ionNext(){
  if(sessGate())return;
  const e=EX[Math.floor(Math.random()*EX.length)],d=IONI[e.n],good=d[1].find(c=>c[1]===1);
  const wr=shuf(d[1].filter(c=>c[1]===0)).slice(0,3);
  const opts=shuf([{l:good[0],ok:true,w:good[2]}].concat(wr.map(c=>({l:c[0],ok:false,w:c[2]}))));
  TR.cur={kind:'ion',e,d,good,opts,pick:null};ionDraw();
}
function ionDraw(){
  const box=$('#quiz'),c=TR.cur,e=c.e;
  let h='<div class="k mono" style="color:var(--muted)">Acertos: '+TR.score.ok+' de '+TR.score.n+'</div>';
  h+='<p class="ctx">Molécula <b>'+esc(e.nome)+'</b> <span class="mono">'+fmt(e.f)+'</span> (M = '+e.M+').</p><div class="mol">'+fig(e.smi,e.f,'keep','molécula')+'</div>';
  h+='<p><b>De onde o feixe de elétrons tira o elétron primeiro?</b></p>';
  c.opts.forEach((o,k)=>{let cls='optb';if(c.pick!==null){if(o.ok)cls+=' good';else if(c.pick===k)cls+=' bad';}
    h+='<button type="button" class="'+cls+'" data-k="'+k+'"'+(c.pick!==null?' disabled':'')+'>'+esc(o.l)+'</button>';});
  if(c.pick!==null){
    const ch=c.opts[c.pick];
    let fb='<b>Sai de: '+esc(c.good[0])+'.</b> '+esc(c.good[2]);
    if(!ch.ok)fb+='<br><b>Por que não &ldquo;'+esc(ch.l)+'&rdquo;:</b> '+esc(ch.w);
    c.d[1].filter(x=>x[1]===2).forEach(x=>{fb+='<br><i>'+esc(x[0])+':</i> '+esc(x[2]);});
    h+='<div class="fb '+(ch.ok?'good':'bad')+'">'+(ch.ok?'Certo. ':'Ainda não. ')+fb+'</div>';
  }
  h+='<div class="row" style="margin-top:10px"><button class="btn'+(c.pick!==null?'':' ghost')+'" id="ion-n" type="button">'+(c.pick!==null?'Próxima':'Outra')+'</button></div>';
  box.innerHTML=h;
  box.querySelectorAll('.optb').forEach(b=>b.onclick=()=>{const k=+b.dataset.k;c.pick=k;TR.score.n++;if(c.opts[k].ok)TR.score.ok++;else{repAdd('ion:'+e.n);}ionDraw();});
  $('#ion-n').onclick=ionNext;
}

/* ---------- Simulado ---------- */""")
# 8 simulado completo
i=s.index("/* ---------- Simulado ---------- */");j=s.index("/* ---------- Setas: onde vai cada seta? ---------- */")
novo='''/* ---------- Simulado ---------- */
const SM={};
function keptQ(e,r){
  const ok=r[7];
  let pool=[];EX.forEach(x=>x.rows.forEach(y=>{if(y[7]!==ok&&y[0]!==r[0]&&Math.abs(y[0]-r[0])<=25)pool.push(y[7]);}));
  pool=Array.from(new Set(pool));
  if(pool.length<3)EX.forEach(x=>x.rows.forEach(y=>{if(y[7]!==ok&&y[0]!==r[0]&&pool.indexOf(y[7])<0)pool.push(y[7]);}));
  const wr=shuf(pool).slice(0,3);
  return {p:'O pico <b class="mono">'+r[0]+'</b> vem do '+(r[1]===e.M?'íon molecular (M = '+e.M+')':'pico '+r[1])+'. Qual fragmento <b>ficou</b>?',
    opts:shuf([{l:fmt(ok),ok:true}].concat(wr.map(l=>({l:fmt(l),ok:false})))),
    fb:'Ficou <b>'+fmt(ok)+'</b> (massa '+r[0]+'). '+estIon(r[7])+'.'};
}
function smItems(e,comp){
  const it=[];
  e.rows.forEach(r=>{
    const qs=comp?[keptQ(e,r),lossQ(e,r)]:[lossQ(e,r)];
    if(comp){const a=cisQ(e,r);if(a)qs.push(a);qs.push(regQ(e,r));}
    qs.forEach(q=>it.push({r,q}));
  });
  return it;
}
function smInit(){
  const box=$('#quiz');
  box.innerHTML='<p class="ctx"><b>Simulado.</b> Você escolhe um exercício e vê só a fórmula, a massa e os picos, sem o nome. No fim aparecem a nota, o tempo e o que errou. Os erros vão para &ldquo;Revisar&rdquo;.</p><div class="row"><select id="smsel" aria-label="Exercício do simulado"><option value="0">Qualquer exercício</option>'+EX.map(e=>'<option value="'+e.n+'">Ex. '+e.n+' ('+e.rows.length+' picos)</option>').join('')+'</select><select id="smmod" aria-label="Tipo de simulado"><option value="0">Só o que saiu</option><option value="1">Completo: o que ficou, o que saiu, tipo e regra</option></select><button class="btn" id="smgo" type="button">Começar</button></div>';
  $('#smgo').onclick=()=>{
    const v=+$('#smsel').value,e=v?EX.find(x=>x.n===v):EX[Math.floor(Math.random()*EX.length)];
    SM.e=e;SM.qs=smItems(e,$('#smmod').value==='1');SM.i=0;SM.ok=0;SM.bad=[];SM.t0=Date.now();SM.pick=null;smDraw();};
}
function smDraw(){
  const box=$('#quiz'),e=SM.e;
  if(SM.i>=SM.qs.length){
    const sec=Math.round((Date.now()-SM.t0)/1000),mm=Math.floor(sec/60),ss=('0'+(sec%60)).slice(-2);
    SM.bad.forEach(r=>repAdd(e.n+':'+r[0]));e.rows.forEach(r=>{if(SM.bad.indexOf(r)<0)repOk(e.n+':'+r[0]);});trLabel();
    let h='<div class="ans" style="border-radius:6px"><span class="t">Nota: '+SM.ok+' de '+SM.qs.length+' · tempo '+mm+':'+ss+'</span>Exercício '+e.n+': <b>'+esc(e.nome)+'</b> <span class="mono">'+fmt(e.f)+'</span>.</div>';
    if(SM.bad.length){h+='<h3>Para revisar</h3><ul>'+SM.bad.map(r=>{const d=r[1]-r[0];return '<li>Pico <b class="mono">'+r[0]+'</b> (de '+r[1]+'): saiu <b>'+d+'</b>, que foi <b>'+fmt(r[3])+'</b> ('+esc(r[4])+').</li>';}).join('')+'</ul>';}
    else h+='<p>Sem erros neste exercício.</p>';
    h+='<div class="row" style="margin-top:10px"><button class="btn" id="smagain" type="button">Outro simulado</button></div>';
    box.innerHTML=h;$('#smagain').onclick=smInit;return;
  }
  const x=SM.qs[SM.i],q=x.q;
  let h='<div class="k mono" style="color:var(--muted)">Pergunta '+(SM.i+1)+' de '+SM.qs.length+' · acertos '+SM.ok+'</div>';
  h+='<p class="ctx">Molécula <b class="mono">'+fmt(e.f)+'</b> (M = '+e.M+'). Picos: <span class="mono">'+e.peaks.join(', ')+'</span>.</p><p>'+q.p+'</p>';
  q.opts.forEach((o,k)=>{let cls='optb';if(SM.pick!==null){if(o.ok)cls+=' good';else if(SM.pick===k)cls+=' bad';}
    h+='<button type="button" class="'+cls+'" data-k="'+k+'"'+(SM.pick!==null?' disabled':'')+'>'+o.l+'</button>';});
  if(SM.pick!==null){h+='<div class="fb '+(q.opts[SM.pick].ok?'good':'bad')+'">'+(q.opts[SM.pick].ok?'Certo. ':'Ainda não. ')+q.fb+'</div><div class="row" style="margin-top:10px"><button class="btn" id="smn" type="button">'+(SM.i<SM.qs.length-1?'Próxima':'Ver a nota')+'</button></div>';}
  box.innerHTML=h;
  box.querySelectorAll('.optb').forEach(b=>b.onclick=()=>{const k=+b.dataset.k;SM.pick=k;if(q.opts[k].ok)SM.ok++;else if(SM.bad.indexOf(x.r)<0)SM.bad.push(x.r);smDraw();});
  const n=$('#smn');if(n)n.onclick=()=>{SM.i++;SM.pick=null;smDraw();};
}

'''
s=s[:i]+novo+s[j:]
open('template.html','w').write(s)
print('ok')
