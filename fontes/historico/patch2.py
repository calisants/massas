import json,re
s=open('template.html').read()
def rep(a,b,cnt=1):
    global s
    assert s.count(a)==cnt,(s.count(a),a[:80])
    s=s.replace(a,b)
TIPO=json.load(open('/tmp/tipo.json'))
# 1 tipo manual
rep("function tipoE(ex,r){\n  const k=tipoQ(r);if(k!=='neu')return k;",
    "const TIPO="+json.dumps(TIPO,ensure_ascii=False)+";\nfunction tipoE(ex,r){\n  const t=TIPO[ex.n+':'+r[0]];if(t)return t;\n  const k=tipoQ(r);if(k!=='neu')return k;")
# 2 repetição espaçada
rep("function trPool(){","""function repGet(){let rp=LS.get('massas-rep',null);if(rp===null){rp={};LS.get('massas-erros',[]).forEach(k=>{rp[k]={b:0,d:0};});LS.set('massas-rep',rp);}return rp;}
function repAdd(k){const rp=repGet();rp[k]={b:0,d:Date.now()+864e5};LS.set('massas-rep',rp);}
function repOk(k){const rp=repGet(),o=rp[k];if(!o||o.d>Date.now())return;const DIAS=[1,3,7];if(o.b>=2)delete rp[k];else{o.b++;o.d=Date.now()+DIAS[o.b]*864e5;}LS.set('massas-rep',rp);}
function repDue(){const rp=repGet(),n=Date.now();return Object.keys(rp).filter(k=>rp[k].d<=n).length;}
function trPool(){""")
rep("if(TR.mode==='rev'){const er=LS.get('massas-erros',[]);return all.filter(x=>er.indexOf(x.e.n+':'+x.r[0])>=0);}",
    "if(TR.mode==='rev'){const rp=repGet(),now=Date.now();return all.filter(x=>{const o=rp[x.e.n+':'+x.r[0]];return o&&(TR.revAll||o.d<=now);});}")
rep("function trLabel(){const rb=document.querySelector('#trmode [data-m=\"rev\"]');if(rb)rb.textContent='Revisar erros ('+LS.get('massas-erros',[]).length+')';}",
    "function trLabel(){const rb=document.querySelector('#trmode [data-m=\"rev\"]');if(rb)rb.textContent='Revisar ('+repDue()+' hoje)';}")
rep("""c.done=true;const key=e.n+':'+r[0];let er=LS.get('massas-erros',[]);
      if(c.wrong){if(er.indexOf(key)<0)er.push(key);}else er=er.filter(x=>x!==key);
      LS.set('massas-erros',er);trLabel();}""","""c.done=true;const key=e.n+':'+r[0];
      if(c.wrong)repAdd(key);else repOk(key);trLabel();}""")
rep("if(!TR.cur){box.innerHTML='<p class=\"empty\">'+(TR.mode==='rev'?'Nenhum erro guardado. Faça rodadas em &ldquo;Qual saiu?&rdquo; ou &ldquo;Tente antes de ver&rdquo;. Os erros aparecem aqui.':'Nada para treinar.')+'</p>';return;}",
"""if(!TR.cur){
    if(TR.mode==='rev'){const n=Object.keys(repGet()).length;
      box.innerHTML=n?'<p class="empty">Nenhuma revisão vencida hoje. Você tem '+n+' guardada(s): cada erro volta 1, 3 e 7 dias depois, e sai da lista quando você acerta nas três.</p><div class="row"><button class="btn ghost" id="revall" type="button">Revisar todas agora</button></div>':'<p class="empty">Nenhum erro guardado. Faça rodadas em outros modos. Os erros aparecem aqui e voltam depois de 1, 3 e 7 dias.</p>';
      const ra=$('#revall');if(ra)ra.onclick=()=>{TR.revAll=true;trNext();};return;}
    box.innerHTML='<p class="empty">Nada para treinar.</p>';return;}""")
# modos
rep("[['qual','Qual saiu?'],['try','Tente antes de ver'],['calc','Digitar a perda'],['rev','Revisar erros']]",
    "[['qual','Qual saiu?'],['try','Tente antes de ver'],['calc','Digitar a perda'],['seta','Setas'],['sm','Simulado'],['rev','Revisar']]")
rep("b.onclick=()=>{TR.mode=m;trInit();};","b.onclick=()=>{TR.mode=m;TR.revAll=false;trInit();};")
rep("  if(TR.mode==='calc'){newQ();return;}\n  trNext();","  if(TR.mode==='calc'){newQ();return;}\n  if(TR.mode==='sm'){smInit();return;}\n  if(TR.mode==='seta'){setaNext();return;}\n  trNext();")
# simulado + setas
rep("/* ---------- Espectro novo (detetive) ---------- */","""/* ---------- Simulado ---------- */
const SM={};
function smInit(){
  const box=$('#quiz');
  box.innerHTML='<p class="ctx"><b>Simulado.</b> Você escolhe um exercício e vê só a fórmula e a massa, sem dica de nome. Responde o que saiu em cada pico, uma pergunta de cada vez. No fim aparecem a nota, o tempo e o que errar. Os erros vão para &ldquo;Revisar&rdquo;.</p><div class="row"><select id="smsel" aria-label="Exercício do simulado"><option value="0">Qualquer exercício</option>'+EX.map(e=>'<option value="'+e.n+'">Ex. '+e.n+' ('+e.rows.length+' picos)</option>').join('')+'</select><button class="btn" id="smgo" type="button">Começar</button></div>';
  $('#smgo').onclick=()=>{
    const v=+$('#smsel').value,e=v?EX.find(x=>x.n===v):EX[Math.floor(Math.random()*EX.length)];
    SM.e=e;SM.qs=e.rows.map(r=>({r,q:lossQ(e,r)}));SM.i=0;SM.ok=0;SM.bad=[];SM.t0=Date.now();SM.pick=null;smDraw();};
}
function smDraw(){
  const box=$('#quiz'),e=SM.e;
  if(SM.i>=SM.qs.length){
    const sec=Math.round((Date.now()-SM.t0)/1000),mm=Math.floor(sec/60),ss=('0'+(sec%60)).slice(-2);
    SM.bad.forEach(b=>repAdd(e.n+':'+b.r[0]));SM.qs.forEach((x,i)=>{if(SM.bad.indexOf(x)<0)repOk(e.n+':'+x.r[0]);});trLabel();
    let h='<div class="ans" style="border-radius:6px"><span class="t">Nota: '+SM.ok+' de '+SM.qs.length+' · tempo '+mm+':'+ss+'</span>Exercício '+e.n+': <b>'+esc(e.nome)+'</b> <span class="mono">'+fmt(e.f)+'</span>.</div>';
    if(SM.bad.length){h+='<h3>Para revisar</h3><ul>'+SM.bad.map(b=>{const d=b.r[1]-b.r[0];return '<li>Pico <b class="mono">'+b.r[0]+'</b> (de '+b.r[1]+'): saiu <b>'+d+'</b>, que foi <b>'+fmt(b.r[3])+'</b> ('+esc(b.r[4])+').</li>';}).join('')+'</ul>';}
    else h+='<p>Sem erros. Sem nenhuma pergunta para revisar neste exercício.</p>';
    h+='<div class="row" style="margin-top:10px"><button class="btn" id="smagain" type="button">Outro simulado</button></div>';
    box.innerHTML=h;$('#smagain').onclick=smInit;return;
  }
  const x=SM.qs[SM.i],q=x.q;
  let h='<div class="k mono" style="color:var(--muted)">Pico '+(SM.i+1)+' de '+SM.qs.length+' · acertos '+SM.ok+'</div>';
  h+='<p class="ctx">Molécula <b class="mono">'+fmt(e.f)+'</b> (M = '+e.M+'). Picos: <span class="mono">'+e.peaks.join(', ')+'</span>.</p><p>'+q.p+'</p>';
  q.opts.forEach((o,k)=>{let cls='optb';if(SM.pick!==null){if(o.ok)cls+=' good';else if(SM.pick===k)cls+=' bad';}
    h+='<button type="button" class="'+cls+'" data-k="'+k+'"'+(SM.pick!==null?' disabled':'')+'>'+o.l+'</button>';});
  if(SM.pick!==null){h+='<div class="fb '+(q.opts[SM.pick].ok?'good':'bad')+'">'+(q.opts[SM.pick].ok?'Certo. ':'Ainda não. ')+q.fb+'</div><div class="row" style="margin-top:10px"><button class="btn" id="smn" type="button">'+(SM.i<SM.qs.length-1?'Próximo pico':'Ver a nota')+'</button></div>';}
  box.innerHTML=h;
  box.querySelectorAll('.optb').forEach(b=>b.onclick=()=>{const k=+b.dataset.k;SM.pick=k;if(q.opts[k].ok)SM.ok++;else SM.bad.push(x);smDraw();});
  const n=$('#smn');if(n)n.onclick=()=>{SM.i++;SM.pick=null;smDraw();};
}

/* ---------- Setas: onde vai cada seta? ---------- */
const SETAS=[
 {t:'Ionização (o 1º passo de todo espectro)',m:0,qs:[
  {p:'O feixe de elétrons arranca 1 elétron da molécula. De qual elétron isso é mais fácil?',o:['Do par livre (n) do O ou do N','De uma ligação C–C (σ)','De uma ligação C–H'],fb:'A ordem de facilidade é: par livre (n) &lt; π &lt; σ. Por isso o O ou o N perde o elétron.'},
  {p:'Depois da ionização, o que o O (ou N) fica tendo?',o:['Um elétron sozinho e carga + (íon-radical, +·)','Carga + e nenhum elétron sozinho (cátion)','Carga − e um elétron sozinho'],fb:'Perdeu 1 dos 2 elétrons do par livre: sobra 1 elétron sozinho e, como saiu um elétron (carga −), a carga fica +.'}]},
 {t:'Clivagem α (homolítica)',m:1,qs:[
  {p:'A seta que parte do elétron sozinho do O é de que tipo?',o:['Seta de anzol (1 elétron)','Seta inteira (par de elétrons)','Não há seta nessa etapa'],fb:'Um elétron só andando se desenha com meia ponta (anzol).'},
  {p:'Para onde vai esse elétron do O?',o:['Forma a ligação dupla C=O','Vai para o grupo R′ que sai','Volta para o anel'],fb:'O elétron do O se junta a 1 elétron do C e vira a segunda ligação do C=O.'},
  {p:'O que acontece com a ligação C–R′?',o:['Quebra e cada lado leva 1 elétron: R′ sai como radical (·)','Quebra e o par vai todo com R′, que sai como ânion','Não quebra; só o H sai'],fb:'O C usa 1 elétron dessa ligação para a nova C=O. O outro elétron fica com R′, que sai como radical.'}]},
 {t:'McLafferty (homolítica, em sequência)',m:2,qs:[
  {p:'De qual carbono vem o H que pula para o O?',o:['Do carbono γ (o 3º a partir do C=O)','Do carbono α (vizinho do C=O)','Do próprio O'],fb:'Precisa ser o H do γ: só ele alcança o O por um anel de 6 átomos.'},
  {p:'Quantos átomos tem o anel que o H atravessa?',o:['6','4','5'],fb:'O, C do C=O, Cα, Cβ, Cγ e o H: seis.'},
  {p:'O que sai no final?',o:['Um alqueno neutro (molécula completa)','Um radical alquila','Um ânion'],fb:'Sai um alqueno neutro. O íon que fica continua sendo íon-radical (+·), por isso a massa do pico é par se M era par.'}]},
 {t:'Cátion acílio perde CO (heterolítica)',m:3,qs:[
  {p:'A seta usada aqui é de que tipo?',o:['Seta inteira (um par de elétrons)','Seta de anzol (1 elétron)','Não há seta nessa etapa'],fb:'Aqui anda um par de elétrons: seta de ponta cheia.'},
  {p:'O que sai?',o:['CO, molécula neutra','R·, um radical, e fica CO+·','O·, um radical'],fb:'O cátion (sem elétron sozinho) solta uma molécula neutra, CO. Cátion não solta radical (regra dos elétrons pares).'},
  {p:'O que fica?',o:['Um cátion R+ (sem elétron sozinho)','Um radical R·','Um ânion R−'],fb:'Fica R+, com a carga que o íon já tinha.'}]},
 {t:'Perda de H· (M − 1)',m:4,qs:[
  {p:'O H sai levando quantos elétrons?',o:['1 elétron (H·)','0 elétron (H+)','2 elétrons (H−)'],fb:'Cisão homolítica: cada lado leva 1 elétron. O H sai como radical.'},
  {p:'Que seta se usa para o elétron que sobra no heteroátomo?',o:['Seta de anzol','Seta inteira','Nenhuma'],fb:'É 1 elétron andando: anzol.'},
  {p:'O que o heteroátomo faz com o elétron sozinho dele?',o:['Forma a ligação dupla com o carbono','Fica com o H','Perde o par livre inteiro'],fb:'O elétron do O ou do N forma a ligação dupla com o C vizinho; o H sai.'}]}
];
function setaNext(){
  let c;do{c=SETAS[Math.floor(Math.random()*SETAS.length)];}while(TR.cur&&TR.cur.c===c&&SETAS.length>1);
  TR.cur={kind:'seta',c,qs:c.qs.map(q=>({p:q.p,fb:q.fb,opts:shuf(q.o.map((l,i)=>({l,ok:i===0})))})),i:0,pick:null,done:false};setaDraw();
}
function setaDraw(){
  const box=$('#quiz'),c=TR.cur;
  let h='<div class="k mono" style="color:var(--muted)">Acertos: '+TR.score.ok+' de '+TR.score.n+'</div><p class="ctx"><b>'+c.c.t+'</b></p>';
  if(!c.done){
    const q=c.qs[c.i];
    h+='<p><b>Pergunta '+(c.i+1)+' de '+c.qs.length+'.</b> '+q.p+'</p>';
    q.opts.forEach((o,k)=>{let cls='optb';if(c.pick!==null){if(o.ok)cls+=' good';else if(c.pick===k)cls+=' bad';}
      h+='<button type="button" class="'+cls+'" data-k="'+k+'"'+(c.pick!==null?' disabled':'')+'>'+o.l+'</button>';});
    if(c.pick!==null)h+='<div class="fb '+(q.opts[c.pick].ok?'good':'bad')+'">'+(q.opts[c.pick].ok?'Certo. ':'Ainda não. ')+q.fb+'</div><div class="row" style="margin-top:10px"><button class="btn" id="stn" type="button">'+(c.i<c.qs.length-1?'Próxima pergunta':'Ver o modelo com setas')+'</button></div>';
    else h+='<div class="row"><button class="btn ghost" id="sto" type="button">Outro mecanismo</button></div>';
  }else{
    const m=document.querySelectorAll('#se-anchor .mdl')[c.c.m];
    h+='<div class="mdl">'+(m?m.innerHTML:'')+'</div><div class="row" style="margin-top:10px"><button class="btn" id="sto" type="button">Outro mecanismo</button></div>';
  }
  box.innerHTML=h;
  box.querySelectorAll('.optb').forEach(b=>b.onclick=()=>{const k=+b.dataset.k,q=c.qs[c.i];c.pick=k;TR.score.n++;if(q.opts[k].ok)TR.score.ok++;setaDraw();});
  const n=$('#stn');if(n)n.onclick=()=>{if(c.i<c.qs.length-1){c.i++;c.pick=null;}else c.done=true;setaDraw();};
  const o=$('#sto');if(o)o.onclick=setaNext;
}

/* ---------- Perguntas para o professor ---------- */
const PERG=[
 ['Ex. 1 a 5: conferir com a lousa','Montei os exercícios 1 a 5 (etilbenzeno, furano, estireno, benzofenona, 3-pentanona) pelo livro, sem a lousa. Posso mostrar para o senhor conferir as massas e os mecanismos?'],
 ['Ex. 1: o anel de 7 (tropílio) é obrigatório?','O senhor termina o 91 com o anel de 7 carbonos porque é mais estável. Na prova posso desenhar o íon benzila (anel de 6 com CH2+) ou tenho que desenhar o tropílio?'],
 ['Ex. 6, pico 59','O 59 do 1-propanol é a perda do H do O–H ou de um H do carbono ao lado do OH (clivagem α)? A literatura cita a segunda; a lousa mostrou a primeira.'],
 ['Ex. 9, pico 73','Na lousa o O fecha um anel de 4 membros quando sai CH3. Esse é o mecanismo que vale na prova?'],
 ['Ex. 10, pico 58','A lousa desenha a saída do CH3 ligado ao N. Pela clivagem α, o mais favorável seria sair o CH3 do etila. Vale o da lousa?'],
 ['Ex. 10, pico 44','O 44 é o nitrênio (CH3)2N+ ou o CH3–NH+=CH2? Qual desenhar?'],
 ['Ex. 8, pico 50','O 51 (C4H3+, cátion sem elétron sozinho) perde H· e vira 50 (C4H2+·). Isso não quebra a regra dos elétrons pares? Pode ser outro caminho?'],
 ['Ex. 11, pico 87','O 87 do valerato de metila: qual o mecanismo (rearranjo de H e saída do etila, como está na lousa)?'],
 ['Ex. 12, pico 58','O 58 do pentanal: H que passa para o O por anel de 6 e sai eteno. É McLafferty de novo, ou outro rearranjo?'],
 ['IV: bandas fora da tabela','Algumas bandas que usei (por exemplo CH3 simétrico perto de 2870 a 2890) não estão na tabela da disciplina. Na prova só vale a tabela?']
];
function drawPerg(){
  const done=LS.get('massas-perg',[]);
  $('#pergL').innerHTML=PERG.map((p,i)=>'<div class="rule"><label style="display:flex;gap:10px;align-items:flex-start"><input type="checkbox" data-i="'+i+'"'+(done.indexOf(i)>=0?' checked':'')+' style="margin-top:4px"><span><b>'+esc(p[0])+'</b><br>'+esc(p[1])+'</span></label></div>').join('');
  $('#pergL').querySelectorAll('input').forEach(c=>c.onchange=()=>{let d=LS.get('massas-perg',[]);const i=+c.dataset.i;d=c.checked?d.concat([i]):d.filter(x=>x!==i);LS.set('massas-perg',d);});
}

/* ---------- Salvar e levar o progresso ---------- */
function pgCollect(){const d={};try{for(let i=0;i<localStorage.length;i++){const k=localStorage.key(i);if(k&&k.indexOf('massas-')===0)d[k]=localStorage.getItem(k);}}catch(e){}return d;}
function pgEnc(o){return btoa(unescape(encodeURIComponent(JSON.stringify(o))));}
function pgDec(t){return JSON.parse(decodeURIComponent(escape(atob(t.replace(/\\s+/g,'')))));}
function pgMsg(t,bad){const m=$('#pgMsg');m.textContent=t;m.className='fb '+(bad?'bad':'good');}
function pgInit(){
  $('#pgGen').onclick=()=>{$('#pgTxt').value=pgEnc({v:1,d:pgCollect()});pgMsg('Código gerado. Toque em Copiar e cole no outro aparelho ou app.');};
  $('#pgCopy').onclick=()=>{const t=$('#pgTxt');if(!t.value)$('#pgGen').click();t.select();
    try{if(navigator.clipboard)navigator.clipboard.writeText(t.value);else document.execCommand('copy');pgMsg('Copiado.');}catch(e){pgMsg('Não consegui copiar sozinho. Selecione o texto e copie.',true);}};
  $('#pgImp').onclick=()=>{
    let o;try{o=pgDec($('#pgTxt').value);}catch(e){pgMsg('Código inválido. Cole o código inteiro, sem cortar.',true);return;}
    if(!o||o.v!==1||typeof o.d!=='object'){pgMsg('Código inválido.',true);return;}
    let n=0;
    Object.keys(o.d).forEach(k=>{
      if(k.indexOf('massas-')!==0)return;
      let inc,cur;try{inc=JSON.parse(o.d[k]);}catch(e){return;}
      cur=LS.get(k,null);
      if(k==='massas-stud'||k==='massas-perg'){LS.set(k,Array.from(new Set((cur||[]).concat(inc))));n++;}
      else if(k==='massas-rep'){const m=cur||{};Object.keys(inc).forEach(q=>{if(!m[q]||inc[q].d>m[q].d)m[q]=inc[q];});LS.set(k,m);n++;}
      else if(k==='massas-erros'){}
      else if(k.indexOf('massas-nota-')===0){if(!cur)LS.set(k,inc);else if(cur!==inc)LS.set(k,cur+'\\n— importado: '+inc);n++;}
      else if(cur===null){LS.set(k,inc);n++;}
    });
    buildChips();trLabel();drawPerg();pgMsg('Importado ('+n+' itens juntados com o que já existia). Nada foi apagado.');};
}

/* ---------- Espectro novo (detetive) ---------- */""")
# DUV marker no porquê
rep("<p class=\"src\">'+origemTxt(ex)+'</p>","'+duvTxt(ex,row)+'<p class=\"src\">'+origemTxt(ex)+'</p>")
rep("const POSS=","const DUV=['10:44','10:58','6:59','11:87','12:58','9:73','8:50'];\nfunction duvTxt(ex,row){return DUV.indexOf(ex.n+':'+row[0])>=0?'<p class=\"src\"><b>⚠ Mecanismo em dúvida.</b> Está na lista de perguntas para o professor.</p>':'';}\nconst POSS=")
# IV
rep("<h2 style=\"margin-top:18px\">Bandas do arquivo de dados</h2><p class=\"hint\">Cada selo mostra a confiança:","<h2 style=\"margin-top:18px\">Bandas do arquivo de dados (atribuição minha, fora da tabela do curso)</h2><p class=\"hint\">Estas atribuições são minhas, a partir do espectro do SDBS. Se a prova só aceita a tabela da disciplina, use a tabela de cima. Cada selo mostra a confiança:")
rep("(r[2]==='baixa'?'chk':'ok')+'\">'+r[2]","(r[2]==='alta'?'ok':'chk')+'\">'+r[2]")
# menu / telas
m=re.search(r'\n\s*<button class="mi" type="button" data-go="p-se">.*?</button>',s);assert m
s=s.replace(m.group(0),'')
m=re.search(r'<button class="mi" type="button" data-go="p-pq">.*?</button>',s);assert m
s=s.replace(m.group(0),'<button class="mi" type="button" data-go="p-pq"><b>Entender as quebras (regras e setas)</b><span>Por que a ligação quebra ali, cisão homolítica e heterolítica, rearranjos e os modelos com setas.</span></button>\n      <button class="mi" type="button" data-go="p-pr"><b>Perguntas para o professor</b><span>As dúvidas que ainda não consegui confirmar. Marque as que já perguntou.</span></button>\n      <button class="mi" type="button" data-go="p-pg"><b>Salvar e levar o progresso</b><span>Gere um código para passar o que você estudou de um aparelho ou app para outro.</span></button>')
i=s.index('<section id="p-se"');j=s.index('</section>',i)
blk=s[i:j]
inner=blk.split('</button>\n',1)[1]
inner=re.sub(r'<h2 class="scr">Setas dos mecanismos</h2>','<h2 class="scr" style="margin-top:28px">Modelos com setas</h2>',inner)
s=s[:i].rstrip()+'\n\n'+s[j+len('</section>'):].lstrip('\n')
k=s.index('<section id="p-pq"');l=s.index('</section>',k)
s=s[:l]+'<div id="se-anchor">'+inner+'</div>\n  '+s[l:]
rep('<section id="p-co"','''<section id="p-pr" role="region" aria-label="Perguntas para o professor" hidden>
    <button class="back" data-go="p-ma">← Mais</button>
    <h2 class="scr">Perguntas para o professor</h2>
    <p class="hint">Estas são as dúvidas em que não tenho certeza. Marque a caixa quando perguntar. Anote a resposta dele na nota do exercício.</p>
    <div id="pergL"></div>
  </section>

  <section id="p-pg" role="region" aria-label="Salvar e levar o progresso" hidden>
    <button class="back" data-go="p-ma">← Mais</button>
    <h2 class="scr">Salvar e levar o progresso</h2>
    <p class="hint">O que você marca aqui (estudados, notas, revisões, cor) fica só neste aparelho e neste navegador. O app do GitHub e a versão aberta no Claude são cópias separadas e não conversam. Para levar de um para o outro: gere o código, copie, e cole no outro.</p>
    <div class="row"><button class="btn" id="pgGen" type="button">1. Gerar código</button><button class="btn ghost" id="pgCopy" type="button">Copiar</button></div>
    <textarea id="pgTxt" rows="5" aria-label="Código do progresso" style="width:100%;margin:10px 0;font-family:var(--mono);font-size:.8rem;background:var(--surface);color:var(--ink);border:1px solid var(--line);border-radius:6px;padding:8px"></textarea>
    <div class="row"><button class="btn" id="pgImp" type="button">2. Importar o código colado</button></div>
    <p class="hint">Importar junta com o que já existe e não apaga nada.</p>
    <div id="pgMsg" role="status"></div>
  </section>

  <section id="p-co"''')
rep("const SCR=['p-an','p-tr','p-tb','p-iv','p-ma','p-ca','p-aj','p-fo','p-pq','p-co','p-se','p-es'];","const SCR=['p-an','p-tr','p-tb','p-iv','p-ma','p-ca','p-aj','p-fo','p-pq','p-co','p-es','p-pr','p-pg'];")
rep("'p-se':'t-ma','p-es':'t-ma'};","'p-es':'t-ma','p-pr':'t-ma','p-pg':'t-ma'};")
rep("function go(id){\n","function go(id){\n  if(id==='p-se'){go('p-pq');const a=$('#se-anchor');if(a)a.scrollIntoView();return;}\n")
rep("  if(id==='p-tr')trInit();","  if(id==='p-tr')trInit();\n  if(id==='p-pr')drawPerg();")
rep("curEx=6;$('#inM').value=60;","pgInit();curEx=6;$('#inM').value=60;")
open('template.html','w').write(s)
print('ok')
