/* ================= ANALORG v3: ajustes, estado salvo, novidades, revisão de perguntas, fontes recolhidas ================= */

/* ---------- Ajustes: zoom e treinos sem pistas ---------- */
const semDica=()=>LS.get('massas-semdica',false);
function zoomAplicar(on){
  const m=document.querySelector('meta[name="viewport"]');
  if(m)m.setAttribute('content',on?'width=device-width,initial-scale=1':'width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no');
  document.documentElement.classList.toggle('semzoom',!on);
}
['gesturestart','gesturechange'].forEach(ev=>document.addEventListener(ev,e=>{if(!LS.get('massas-zoom',true))e.preventDefault();},{passive:false}));
function stDraw(){
  $('#stZoom').checked=!!LS.get('massas-zoom',true);
  acessDraw();
  $('#stSem').checked=!!semDica();
  offDraw();
}
function stInit(){
  zoomAplicar(!!LS.get('massas-zoom',true));acessAplicar();
  $('#stZoom').onchange=e=>{LS.set('massas-zoom',e.target.checked);zoomAplicar(e.target.checked);};
  $('#stSem').onchange=e=>{LS.set('massas-semdica',e.target.checked);if(TR.cur)trDraw();};
  stDraw();
}

const VNUM=parseInt(String(VERSAO).replace(/^v/,''),10)||0;
/* Quando o app mudar de endereço, preencha NOVO_ENDERECO (ex.: 'https://anaquim.seudominio.com.br/'). Quem abrir o endereço antigo vê o aviso. */
const NOVO_ENDERECO='';
function endBanner(){
  if(!NOVO_ENDERECO)return;
  let h;try{h=new URL(NOVO_ENDERECO).host;}catch(e){return;}
  if(location.host===h||location.protocol==='file:')return;
  const b=document.createElement('div');b.id='endBanner';b.className='nvb';b.setAttribute('role','status');
  b.innerHTML='<span>O Anaquim mudou de endereço. Antes de trocar, salve seu progresso em Início, O app, Salvar progresso, e cole o código no endereço novo.</span><span class="nvbb"><a class="btn" href="'+esc(NOVO_ENDERECO)+'">Abrir o novo</a></span>';
  const w=document.querySelector('.wrap');w.insertBefore(b,w.children[1]||null);
}
function nvInit(){
  endBanner();offBar();
}

/* ---------- Revisão espaçada das perguntas dos quizzes (1, 3 e 7 dias) ---------- */
const qzKey=q=>{let h=0;const t=String(q.q);for(let i=0;i<t.length;i++)h=(h*31+t.charCodeAt(i))|0;return 'q'+(h>>>0).toString(36);};
const repqGet=()=>LS.get('massas-repq',{});
function repqDue(){const r=repqGet(),n=Date.now();return Object.keys(r).filter(k=>r[k].d<=n).length;}
function repqAvail(){return Math.max(0,Math.min(repqDue(),REV_MAX-revFeitas()));}
let RVMODE=false;
function qzRec(q,ok){
  const k=qzKey(q),r=repqGet(),o=r[k],now=Date.now();
  if(!ok){r[k]={b:0,d:now+864e5,q:{q:q.q,o:q.o,ok:q.ok,w:q.w}};LS.set('massas-repq',r);if(RVMODE)revCount();return;}
  if(!o||o.d>now)return;
  const DIAS=[1,3,7];
  if(o.b>=2)delete r[k];else{o.b++;o.d=now+DIAS[o.b]*864e5;}
  LS.set('massas-repq',r);if(RVMODE)revCount();
}
function rvDraw(){
  const box=$('#rvBox'),r=repqGet(),now=Date.now();
  const total=Object.keys(r).length;
  const due=Object.keys(r).filter(k=>r[k].d<=now).sort((a,b)=>r[a].d-r[b].d).slice(0,Math.max(0,REV_MAX-revFeitas()));
  RVMODE=false;
  if(!due.length){
    box.innerHTML='<p class="empty">'+(revFeitas()>=REV_MAX&&repqDue()>0?'Você já revisou '+REV_MAX+' hoje. O resto fica para amanhã, para não pesar.':'Nenhuma pergunta vencida hoje.')+' Há '+total+' guardada'+(total===1?'':'s')+'.</p>'+(total===0?'<p class="sm">As perguntas que você errar nos treinos (Solubilidade, Elementar, RMN, IV e Massas) aparecem aqui para refazer.</p>':'');
    return;
  }
  RVMODE=true;
  miniQuiz('#rvBox',due.map(k=>r[k].q),'Revisão');
}



/* ---------- Uso sem internet: estado claro ---------- */
const fmtMB=b=>(b/1048576).toFixed(1).replace('.',',')+' MB';
async function offDraw(){
  const box=$('#offBox');if(!box)return;
  const L=[['Conexão',navigator.onLine?'Com internet':'Sem internet agora']];
  let sw='Só funciona abrindo pelo endereço do app (não vale para arquivo aberto direto).',ok=false;
  try{
    if('serviceWorker' in navigator&&location.protocol.indexOf('http')===0){
      const r=await navigator.serviceWorker.getRegistration();
      if(r&&r.active){ok=true;sw='Pronto: o app está guardado neste aparelho';}
      else sw='Ainda não guardado. Abra o app uma vez com internet.';
    }
  }catch(e){}
  L.push(['Uso sem internet',sw]);
  try{
    if(window.caches){
      let n=0;
      for(const k of await caches.keys()){if(k.indexOf('anaquim-')===0){const c=await caches.open(k);n+=(await c.keys()).length;}}
      if(n)L.push(['Arquivos guardados',n+' (app, ícones e fontes)']);
    }
  }catch(e){}
  try{
    if(navigator.storage&&navigator.storage.estimate){
      const e=await navigator.storage.estimate();
      if(e&&e.usage!=null)L.push(['Espaço usado no aparelho',fmtMB(e.usage)+(e.quota?' (de '+fmtMB(e.quota)+' disponíveis)':'')]);
    }
  }catch(e){}
  L.push(['Versão guardada',String(VERSAO)]);
  const nf=favGet().length;
  L.push(['Favoritos',nf+(nf===1?' composto':' compostos')+'. Ficam sempre disponíveis sem internet, porque o app inteiro fica guardado.']);
  box.innerHTML=L.map(r=>'<div class="cfr"><dt>'+esc(r[0])+'</dt><dd>'+esc(r[1])+'</dd></div>').join('');
  box.dataset.pronto=ok?'1':'0';
}
async function offCheck(){
  const m=$('#offMsg');m.textContent='Verificando...';
  try{
    const r=await fetch('index.html',{cache:'no-store'}),t=await r.text(),v=(t.match(/const VERSAO='([^']*)'/)||[])[1];
    m.textContent=!v?'Não deu para ler a versão publicada.':v===VERSAO?'Você está na versão mais recente ('+v+').':'Há uma versão nova ('+v+'). Feche e abra o app duas vezes para atualizar.';
  }catch(e){m.textContent='Sem internet: não deu para verificar agora.';}
}
function offBar(){
  let b=$('#offBar');
  if(navigator.onLine){if(b)b.hidden=true;return;}
  if(!b){b=document.createElement('div');b.id='offBar';b.className='offbar';b.setAttribute('role','status');
    b.textContent='Sem internet. O app continua funcionando; só os links para fora (SDBS) não abrem.';
    const w=document.querySelector('.wrap');w.insertBefore(b,w.firstChild);}
  b.hidden=false;
}
window.addEventListener('online',()=>{offBar();offDraw();});
window.addEventListener('offline',()=>{offBar();offDraw();});
document.addEventListener('click',ev=>{if(ev.target.closest('#offChk'))offCheck();});


/* ---------- Acessibilidade: tamanho da letra, alto contraste, menos animação, rótulos e foco ---------- */
function acessAplicar(){
  const r=document.documentElement,fs=LS.get('massas-fonte',100);
  r.style.fontSize=fs===100?'':fs+'%';
  r.classList.toggle('altoc',!!LS.get('massas-altoc',false));
  r.classList.toggle('semmov',!!LS.get('massas-semmov',false));
}
function acessDraw(){
  const fs=LS.get('massas-fonte',100);
  document.querySelectorAll('#stFonte button').forEach(b=>b.setAttribute('aria-pressed',String(+b.dataset.fs===fs)));
  $('#stAltoc').checked=!!LS.get('massas-altoc',false);
  $('#stSemmov').checked=!!LS.get('massas-semmov',false);
}
document.addEventListener('click',ev=>{
  const b=ev.target.closest('#stFonte button');
  if(b){LS.set('massas-fonte',+b.dataset.fs);acessAplicar();acessDraw();}
});
document.addEventListener('change',ev=>{
  if(ev.target.id==='stAltoc'){LS.set('massas-altoc',ev.target.checked);acessAplicar();}
  if(ev.target.id==='stSemmov'){LS.set('massas-semmov',ev.target.checked);acessAplicar();}
});
/* desenhos sem texto alternativo viram decoração (o nome e a fórmula já estão em texto ao lado) */
function a11yFix(root){
  (root||document).querySelectorAll('svg[role="img"]:not([aria-label]):not([aria-labelledby])').forEach(s=>{
    s.removeAttribute('role');s.setAttribute('aria-hidden','true');s.setAttribute('focusable','false');
  });
}
(function(){let t;new MutationObserver(()=>{clearTimeout(t);t=setTimeout(()=>a11yFix(document),40);}).observe(document.body,{childList:true,subtree:true});a11yFix(document);})();
/* ao trocar de tela, o foco vai para o título: o leitor de tela anuncia a tela nova */
function focoTitulo(id){
  const h=document.querySelector('#'+id+' h2.scr')||document.querySelector('#'+id+' h2');
  if(h){h.setAttribute('tabindex','-1');try{h.focus({preventScroll:true});}catch(e){}}
}

/* ---------- Favoritos: guardados no aparelho (por CAS), aparecem primeiro na lista e entram no "Salvar progresso" ---------- */
let CPFAV=false;
const favGet=()=>LS.get('massas-fav',[]);
const favHas=c=>favGet().indexOf(c.cas)>=0?1:0;
function favToggle(c){
  const l=favGet(),i=l.indexOf(c.cas);
  if(i>=0)l.splice(i,1);else l.push(c.cas);
  LS.set('massas-fav',l);
}
function favBtnHtml(c){
  const on=favHas(c);
  return '<button class="btn ghost" type="button" id="favBtn" aria-pressed="'+(on?'true':'false')+'">'+(on?'★ Favorito (toque para remover)':'☆ Favoritar')+'</button>';
}

/* ---------- Estado salvo ao sair do app (celular pode fechar o app em segundo plano) ---------- */
function sesSave(){
  try{
    const d={t:Date.now(),tela:CUR,y:window.scrollY,cf:CFI,tr:TR.mode,an:{M:$('#inM').value,P:$('#inP').value},cpq:$('#cpQ').value};
    LS.set('massas-sessao',d);
    if(typeof icSave==='function')icSave();
  }catch(e){}
}
function sesRestore(){
  const d=LS.get('massas-sessao',null);
  if(!d||Date.now()-d.t>12*36e5)return;
  try{
    if(d.an){if(d.an.M)$('#inM').value=d.an.M;if(d.an.P)$('#inP').value=d.an.P;}
    if(d.cpq){$('#cpQ').value=d.cpq;cpDraw();}
    if(d.tr)TR.mode=d.tr;
    if(d.tela&&d.tela!=='p-in'&&!NAVHASH0&&SCR.indexOf(d.tela)>=0){
      if(d.tela==='p-cf'){if(d.cf==null)return;cfDraw(d.cf);}
      go(d.tela);
      setTimeout(()=>window.scrollTo(0,d.y||0),80);
    }
  }catch(e){}
}
document.addEventListener('visibilitychange',()=>{if(document.hidden)sesSave();});
window.addEventListener('pagehide',sesSave);

/* ---------- Fontes recolhidas: a etiqueta fica visível, o texto abre ao tocar ---------- */
const FONTE_RE=/fonte|conferid|SDBS|PubChem|Silverstein|Analor|Plataforma|apostila|slides/i;
function fontesRecolher(root){
  (root||document).querySelectorAll('p.srcl,p.src').forEach(p=>{
    if(p.dataset.fr||p.closest('details.fonte'))return;
    const tags=[...p.querySelectorAll('.tag.sv,.tag.sm')];
    if(!tags.length&&!FONTE_RE.test(p.textContent))return;
    p.dataset.fr='1';
    const d=document.createElement('details');d.className='fonte';
    const sm=document.createElement('summary');
    if(tags.length){const ok=tags.some(t=>t.classList.contains('sv'));tags.forEach(t=>{t.replaceWith(document.createTextNode(t.textContent+'.'));});sm.textContent=ok?'Fonte':'Fonte não conferida';}
    else sm.textContent='Fonte';
    p.parentNode.insertBefore(d,p);d.appendChild(sm);d.appendChild(p);
  });
}
(function(){let tm;new MutationObserver(()=>{clearTimeout(tm);tm=setTimeout(()=>fontesRecolher(document),40);}).observe(document.body,{childList:true,subtree:true});})();

/* ---------- Enviar sugestão ou erro (formulário do Google) ---------- */
const FORM_URL='';
function sugInit(){const a=$('#mSug');if(a&&FORM_URL){a.href=FORM_URL;a.hidden=false;}}

/* ---------- Espectros de RMN simulados (didáticos) ---------- */
const NMR_MULT={'s':[1],'s largo':[1],'d':[1,1],'t':[1,2,1],'q':[1,3,3,1],'quinteto':[1,4,6,4,1],'sexteto':[1,5,10,10,5,1],'septeto':[1,6,15,20,15,6,1],'m':[1,3,4,3,1]};
const ea=s=>esc(s).replace(/"/g,'&quot;');
function pkG(cx,cy,n,at,hk,tx){
  const d=(at&&at.length)?' data-at="'+at.join(',')+'" data-hk="'+hk+'" data-tx="'+ea(tx)+'" tabindex="0" role="button" aria-label="'+ea(tx)+'"':'';
  return '<g class="hpk"'+d+'><circle class="hit" cx="'+cx+'" cy="'+cy+'" r="12"/><circle class="lc" cx="'+cx+'" cy="'+cy+'" r="7"/><text class="ln" x="'+cx+'" y="'+(+cy+3.5).toFixed(1)+'" text-anchor="middle">'+n+'</text></g>';
}
function nmrSpec(c,kind){
  const isH=kind==='h',W=340,L=12,R=12,pw=W-L-R,top=14,base=122,maxH=base-top-26;
  const its=(isH?c.h1:c.c13).map(x=>({x:(x.lo+x.hi)/2,n:isH?x.h:x.n,m:isH?x.m:'s'}));
  if(!its.length)return '';
  const grp={};its.forEach(i=>{const k=i.x.toFixed(1);(grp[k]=grp[k]||[]).push(i);});
  Object.values(grp).forEach(g=>{if(g.length>1){const st=isH?0.25:3;g.forEach((i,k)=>{i.x-=(k-(g.length-1)/2)*st;});}});
  const xs=its.map(i=>i.x);let lo,hi,step;
  if(isH){lo=Math.floor(Math.max(Math.min(...xs)-1.2,-0.5));hi=Math.ceil(Math.min(Math.max(...xs)+1.2,14));
    if(hi-lo<5){const m=(hi+lo)/2;lo=Math.floor(m-2.5);hi=lo+5;} step=hi-lo>8?2:1;}
  else{lo=Math.floor(Math.max(Math.min(...xs)-15,-10)/10)*10;hi=Math.ceil(Math.min(Math.max(...xs)+15,230)/10)*10;step=hi-lo>120?20:10;}
  const span=hi-lo,px=d=>L+(hi-d)/span*pw,J=isH?span*0.014:0,gam=isH?J*0.22:span*0.0016;
  const sg=its.map(i=>{const w=NMR_MULT[i.m]||NMR_MULT.m,sw=w.reduce((a,b)=>a+b,0),broad=/largo/.test(i.m);
    const spread=i.m==='m'?J*0.8:J,area=isH?i.n:0.45+0.25*Math.min(i.n,3);
    return {x:i.x,g:broad?span*0.012:gam,half:(w.length-1)/2*spread,L:w.map((v,k)=>[(k-(w.length-1)/2)*spread,area*v/sw])};});
  const N=Math.round(pw/0.25),ys=new Array(N+1);let mx=0;
  for(let k=0;k<=N;k++){const d=hi-k/N*span;let y=0;
    for(const s of sg)if(Math.abs(d-s.x)<s.half+s.g*40)for(const l of s.L){const t=d-s.x-l[0];y+=l[1]*s.g/Math.PI/(t*t+s.g*s.g);}
    ys[k]=y;if(y>mx)mx=y;}
  const Y=v=>base-v/mx*maxH;let p='',tot=0,cum=new Array(N+1);
  for(let k=N;k>=0;k--){tot+=ys[k];cum[k]=tot;}
  for(let k=0;k<=N;k++)p+=(k?'L':'M')+(L+k/N*pw).toFixed(1)+','+Y(ys[k]).toFixed(1);
  let ip='';if(isH){for(let k=0;k<=N;k++)ip+=(k?'L':'M')+(L+k/N*pw).toFixed(1)+','+(base-cum[k]/tot*maxH*0.8).toFixed(1);}
  let tk='';for(let d=Math.ceil(lo/step)*step;d<=hi;d+=step){const x=px(d).toFixed(1);tk+='<line class="tk" x1="'+x+'" y1="'+base+'" x2="'+x+'" y2="'+(base+4)+'"/><text class="tl" x="'+x+'" y="'+(base+15)+'" text-anchor="middle">'+d+'</text>';}
  const placed=[];let lb='';
  its.map((i,idx)=>({i,idx,s:sg[idx]})).sort((a,b)=>px(a.s.x)-px(b.s.x)).forEach(o=>{
    const x=px(o.s.x),k0=Math.max(0,Math.floor((hi-(o.s.x+o.s.half+o.s.g*3))/span*N)),k1=Math.min(N,Math.ceil((hi-(o.s.x-o.s.half-o.s.g*3))/span*N));
    let m=0;for(let k=k0;k<=k1;k++)if(ys[k]>m)m=ys[k];
    let y=Math.max(Y(m)-12,9);while(placed.some(q=>Math.abs(q[0]-x)<15&&Math.abs(q[1]-y)<14))y-=14;
    if(y<8)y=8;placed.push([x,y]);
    const src=(isH?c.h1:c.c13)[o.idx];
    lb+=pkG(x.toFixed(1),y.toFixed(1),o.idx+1,isH?src.on:src.at,(isH?'h':'c')+(o.idx+1),(isH?'¹H, sinal ':'¹³C, sinal ')+(o.idx+1)+': '+src.t+' · '+(isH?src.h+' H':src.n+' C')+(isH&&src.c?' em '+src.c:'')+' · δ '+src.lo+'–'+src.hi+' ppm');});
  return '<svg class="nmrspec" viewBox="0 0 '+W+' '+(base+34)+'" role="group" aria-label="Espectro de '+(isH?'1H':'13C')+' simulado">'
    +(isH?'<path class="int" d="'+ip+'"/>':'')+'<path class="sp" d="'+p+'"/><line class="ax" x1="'+L+'" y1="'+base+'" x2="'+(W-R)+'" y2="'+base+'"/>'+tk+lb
    +'<text class="tl" x="'+(W/2)+'" y="'+(base+30)+'" text-anchor="middle">δ (ppm)'+(isH?'':' · ¹³C com desacoplamento de ¹H')+'</text></svg>';
}
document.addEventListener('click',ev=>{const b=ev.target.closest('[data-nmrint]');if(!b)return;
  const w=b.closest('.nmrwrap'),s=w&&w.querySelector('svg'),on=s&&s.classList.toggle('showint');
  b.setAttribute('aria-pressed',on?'true':'false');b.textContent=on?'Esconder a integração':'Mostrar a integração';});

/* ---------- IV: linhas novas na tabela do Guia ---------- */
(function(){
  const LT='LibreTexts (tabela de IV)',GER='referência geral, não conferida em fonte nomeada',E='estiramento',D='deformação';
  [
   [2349,2349,'CO₂ do ar (artefato de fundo)','forte, estreita','Aparece quando o fundo não foi bem subtraído. Não é do composto.',LT,'estiramento assimétrico'],
   [2275,2250,'N=C=O de isocianato','forte, larga','',LT,E],
   [2175,2140,'S–C≡N de tiocianato','forte','',LT,E],
   [2145,2120,'N=C=N de carbodiimida','forte','',LT,E],
   [1800,1770,'C=O de haleto de ácido conjugado','forte','',LT,E],
   [1690,1650,'C=O de amida primária','forte; livre ~1690, associada ~1650','',LT,E],
   [1680,1640,'C=O de amida secundária','forte; livre ~1680, associada ~1640','',LT,E],
   [1680,1630,'C=O de amida terciária','forte; livre ~1680, associada ~1630','',LT,E],
   [1678,1668,'C=C de alceno trans-dissubstituído','fraca','',LT,E],
   [1675,1665,'C=C de alceno tri ou tetrassubstituído','fraca','',LT,E],
   [1662,1626,'C=C de alceno cis-dissubstituído','média','',LT,E],
   [1658,1648,'C=C de alceno vinilideno (R₂C=CH₂)','média','',LT,E],
   [1648,1638,'C=C de alceno monossubstituído','forte','',LT,E],
   [1650,1566,'C=C de alceno cíclico','média','',LT,E],
   [1650,1580,'N–H de amina','média','',LT,D],
   [1210,1163,'C–O de éster','forte','',LT,E],
   [1205,1124,'C–O de álcool terciário','forte','',LT,E],
   [1124,1087,'C–O de álcool secundário','forte','',LT,E],
   [1085,1050,'C–O de álcool primário','forte','',LT,E],
   [1050,1040,'C–O–C de anidrido','forte, larga','',LT,E],
   [850,550,'C–Cl','forte','A faixa da apostila é 800–600.',LT,E],
   [690,515,'C–Br','forte','',LT,E],
   [600,500,'C–I','forte segundo esta tabela','A apostila dá fraca.',LT,E],
   [2260,2222,'C≡N de nitrila','fraca segundo esta tabela','A apostila dá média a forte.',LT,E],
   [3333,3267,'≡C–H de alcino terminal','forte, estreita segundo esta tabela','A apostila dá fraca.',LT,E],
   [1280,1230,'anel do epóxido (simétrico)','média','',GER,E],
   [950,815,'anel do epóxido (assimétrico)','forte','',GER,E],
   [890,820,'O–O de peróxido','fraca','',GER,E],
   [1250,1020,'C=S de tiocarbonila','média a forte','',GER,E],
   [540,480,'S–S de dissulfeto','fraca','',GER,E],
   [700,600,'C–S','fraca','',GER,E],
   [1300,1250,'P=O','forte','',GER,E],
   [1050,970,'P–O–C','forte','',GER,E],
   [2440,2275,'P–H','média','',GER,E],
   [2250,2100,'Si–H','média a forte','',GER,E],
   [1100,1000,'Si–O–Si','forte, larga','',GER,E],
   [1260,1250,'Si–CH₃','média a forte','Confirme com 840–800 (Si–C).',GER,D],
   [1380,1310,'B–O','forte','',GER,E],
   [3100,3070,'C–H de ciclopropano','fraca a média','',GER,E],
   [1395,1385,'CH₃ do terc-butila (par de bandas com ~1365)','média','',GER,D],
   [1600,1430,'anel heteroaromático (piridina e similares)','média, várias bandas','',GER,E],
   [3500,3200,'N–H de anel (pirrol, indol)','média','',GER,E],
   [1740,1680,'C=O de carbamato (uretano)','forte','',GER,E],
   [1690,1630,'C=O de ureia','forte','',GER,E],
   [1780,1740,'C=O de carbonato','forte','C–O em 1280–1240.',GER,E],
   [1790,1700,'C=O de imida','forte, 2 bandas','',GER,E],
   [1650,1620,'N–O de nitrato de alquila (assimétrico)','forte','Simétrico em 1285–1270.',GER,E],
   [1600,1500,'N=O de nitroso (C–N=O)','forte','',GER,E],
   [1630,1575,'N=N de azocomposto','fraca (some se for simétrico)','',GER,E],
   [2165,2110,'N≡C de isocianeto','forte','',GER,E],
   [3650,3500,'O–H de oxima','média, larga','C=N em 1690–1640 e N–O em 960–930.',GER,E],
   [1420,1330,'S=O de sulfonato (assimétrico)','forte','Simétrico em 1200–1145.',GER,E],
   [1350,1342,'S=O de ácido sulfônico (assimétrico)','forte','Simétrico em 1165–1150.',GER,E],
   [865,810,'anel 1,3,5-trissubstituído, C–H fora do plano','forte','Confirme com 730–675.',GER,D],
   [870,800,'anel tetrassubstituído (1 H isolado)','forte','',GER,D]
  ].forEach(r=>IRT.push(r));
})();

/* ---------- IV: escolha do composto, espectro simulado e tabela ---------- */
let ivC=null;
const IVSRC={a:'apostila',g:'referência geral, não conferida em fonte nomeada',s:'tabela de IV citada (LibreTexts, disciplina)'};
function ivIw(code){const p=String(code).split(',').map(x=>x.trim()),b=p[0],m={'F':'forte','M–F':'média a forte','M':'média','f–M':'fraca a média','f':'fraca'};
  return (m[b]||b)+(p.length>1?', '+p.slice(1).join(', '):'');}
function ivDepth(code){const b=String(code).split(',')[0].trim();return {'F':1,'M–F':.62,'M':.4,'f–M':.22,'f':.12}[b]||.4;}
function ivBands(c){
  const out=c.iv.map((b,k)=>({hi:b[0],lo:b[1],t:b[2],i:b[3],s:b[5],at:(c.ivat||[])[k]||[]}));
  const e=c.ex?IR.find(x=>x.n===c.ex):null;
  if(e)e.p.forEach(r=>{const nums=String(r[0]).match(/\d+/g).map(Number),hi=Math.max(...nums),lo=Math.min(...nums);
    if(out.some(b=>(hi+lo)/2<=b.hi+5&&(hi+lo)/2>=b.lo-5))return;
    const t=IRT.find(x=>(hi+lo)/2<=x[0]+10&&(hi+lo)/2>=x[1]-10);
    out.push({hi:hi,lo:lo,t:r[1],i:t?(/forte|intensa/.test(t[3])?'F':/fraca/.test(t[3])?'f':'M'):'M',s:'g',extra:true});});
  return out.sort((a,b)=>(b.hi+b.lo)-(a.hi+a.lo));
}
function ivPeaks(b){
  const w=b.hi-b.lo,d=ivDepth(b.i),big=/larga/.test(b.i),mid=(b.hi+b.lo)/2;
  if(/2 bandas/.test(b.i))return [[b.lo+w*.12,Math.max(7,w*.07),d],[b.hi-w*.12,Math.max(7,w*.07),d]];
  if(big)return [[mid,w/(/muito/.test(b.i)?2:2.4),d]];
  if(w>50&&/C–H/.test(b.t))return [[b.lo+w*.12,9,d*.8],[mid,9,d],[b.hi-w*.1,9,d*.8]];
  return [[mid,Math.max(7,w/(w>50?3.2:2.6)),d]];
}
function ivSpec(c,bs){
  const W=340,L=24,R=10,pw=W-L-R,top=14,base=132,hgt=base-top,x=v=>L+(4000-v)/3600*pw,N=Math.round(pw/0.5);
  const pk=bs.map(b=>ivPeaks(b));
  const T=new Array(N+1);
  for(let k=0;k<=N;k++){const v=4000-k/N*3600;let a=0;for(const g of pk)for(const q of g){const t=(v-q[0])/q[1];if(t<5&&t>-5)a+=q[2]*1.05*Math.exp(-t*t/2);}
    T[k]=Math.max(3,100*Math.pow(10,-a));}
  const Y=t=>base-(t*0.96)/100*(hgt-18);let p='';
  for(let k=0;k<=N;k++)p+=(k?'L':'M')+(L+k/N*pw).toFixed(1)+','+Y(T[k]).toFixed(1);
  let g='<rect class="fp" x="'+x(1500).toFixed(1)+'" y="'+top+'" width="'+(x(400)-x(1500)).toFixed(1)+'" height="'+hgt+'"/>';
  g+='<text class="tl" x="'+((x(1500)+x(400))/2).toFixed(1)+'" y="'+(top+9)+'" text-anchor="middle">impressão digital</text>';
  g+='<text class="tl" x="'+((x(4000)+x(1500))/2).toFixed(1)+'" y="'+(top+9)+'" text-anchor="middle">grupos funcionais</text>';
  for(const t of [0,50,100])g+='<text class="tl" x="'+(L-4)+'" y="'+(Y(t)+3).toFixed(1)+'" text-anchor="end">'+t+'</text>';
  for(let v=4000;v>=500;v-=500)g+='<line class="tk" x1="'+x(v).toFixed(1)+'" y1="'+base+'" x2="'+x(v).toFixed(1)+'" y2="'+(base+4)+'"/><text class="tl" x="'+x(v).toFixed(1)+'" y="'+(base+15)+'" text-anchor="middle">'+v+'</text>';
  const placed=[];let lb='';
  bs.forEach((b,i)=>{const q=pk[i].slice().sort((a,b2)=>b2[2]-a[2])[0],cx=x(q[0]);
    const k=Math.max(0,Math.min(N,Math.round((4000-q[0])/3600*N)));let y=Math.max(Y(T[k])-11,top+14);
    while(placed.some(o=>Math.abs(o[0]-cx)<15&&Math.abs(o[1]-y)<14))y-=14;
    if(y<top+4)y=top+4;placed.push([cx,y]);
    lb+=pkG(cx.toFixed(1),y.toFixed(1),i+1,b.at,'b'+(i+1),'Banda '+(i+1)+': '+b.t+' · '+(b.hi===b.lo?'~'+b.hi:b.lo+'–'+b.hi)+' cm⁻¹');});
  return '<svg class="nmrspec irspec" viewBox="0 0 '+W+' '+(base+34)+'" role="group" aria-label="Espectro de IV simulado de '+esc(c.n)+'">'
    +g+'<path class="sp" d="'+p+'"/><line class="ax" x1="'+L+'" y1="'+base+'" x2="'+(W-R)+'" y2="'+base+'"/>'+lb
    +'<text class="tl" x="'+(W/2)+'" y="'+(base+30)+'" text-anchor="middle">número de onda (cm⁻¹) · eixo vertical: transmitância (%)</text></svg>';
}
function drawIVChips(){
  const sel=$('#ivSel');if(!sel)return;
  const q=($('#ivQ').value||'').trim().toLowerCase();
  const ok=COMP.filter(c=>!q||(c.n+' '+c.a.join(' ')+' '+c.f+' '+c.cas).toLowerCase().includes(q));
  const opt=c=>'<option value="'+c.i+'"'+(ivC===c.i?' selected':'')+'>'+esc(c.n)+' ('+c.f+')</option>';
  const by=(a,b)=>a.n.localeCompare(b.n,'pt-BR');
  const sd=ok.filter(c=>c.irc).sort(by),rest=ok.filter(c=>!c.irc).sort(by);
  sel.innerHTML=(sd.length?'<optgroup label="Com espectro do SDBS conferido">'+sd.map(opt).join('')+'</optgroup>':'')+(rest.length?'<optgroup label="Demais compostos">'+rest.map(opt).join('')+'</optgroup>':'')||'<option value="">Nenhum composto encontrado</option>';
  if(ok.length&&!ok.some(c=>c.i===ivC)){ivC=ok[0].i;sel.value=String(ivC);drawIV();}
}
function drawIV(){
  const box=$('#ivout');if(ivC===null){const a=COMP.find(x=>x.n==='acetona');ivC=a?a.i:COMP[0].i;}
  const c=COMP.find(x=>x.i===ivC);if(!c){box.innerHTML='<p class="empty">Escolha um composto acima.</p>';return;}
  const e=c.ex?IR.find(x=>x.n===c.ex):null,bs=ivBands(c);
  let h='<p style="margin:10px 0 0"><b>'+esc(c.n)+'</b> <span class="mut">· '+(c.gf.length?esc(c.gf.join(', ')):'sem grupo funcional')+' · IDH = '+c.gdh+'</span></p>'
   +'<figure class="st ivfig hlfig"><div>'+(c.si||c.s)+'</div><figcaption>'+fmt(c.f)+'</figcaption><div class="hlro" data-dica="Toque num número do espectro ou numa linha da tabela: o trecho da molécula que dá a banda fica colorido.">Toque num número do espectro ou numa linha da tabela: o trecho da molécula que dá a banda fica colorido.</div></figure>';
  if(e)h+='<div class="ans" style="border-radius:6px;margin:10px 0"><span class="t">Pista do IV para o espectro de massas</span>'+esc(e.pista)+'</div>';
  const sd=c.sdbs||(c.ex&&typeof INTS!=='undefined'&&INTS[c.ex]?INTS[c.ex].sdbs:null);
  h+='<h3 style="margin:12px 0 4px">Espectro simulado</h3><div class="nmrwrap">'+ivSpec(c,bs)+'<button class="zbtn" type="button" data-zoom>Ampliar</button></div>';
  h+='<p class="srcl" style="margin:0 0 8px">'+(c.irc?srcTag(true,c.irc===1?'Conferido: SDBS':'Conferido em parte: SDBS')+' As bandas-chave foram conferidas no espectro do SDBS (medido em '+esc(c.irm)+'). ':srcTag(false,'Sem fonte conferida')+' ')
    +'<b>O desenho é simulado, não é o medido.</b> Cada banda é posta no meio da faixa da tabela, com a intensidade típica. Os números dos círculos são os da tabela abaixo. No espectro real, conjugação, ligação de H e o meio da medida deslocam as bandas.'+(sd?' Nº SDBS: <b>'+sd+'</b>.':'')+'</p>';
  h+='<div class="tbl"><table class="obt nostk cmp cmp-iv"><thead><tr><th>#</th><th>cm⁻¹</th><th>O que é</th></tr></thead><tbody>'+bs.map((b,i)=>'<tr'+(b.at&&b.at.length?' class="hlr" data-at="'+b.at.join(',')+'" data-hk="b'+(i+1)+'" data-tx="'+ea('Banda '+(i+1)+': '+b.t+' · '+(b.hi===b.lo?'~'+b.hi:b.lo+'–'+b.hi)+' cm⁻¹')+'"':'')+'><td><b>'+(i+1)+'</b></td><td class="n">'+(b.hi===b.lo?'~'+b.hi:b.lo+'–'+b.hi)+'</td><td>'+esc(b.t)+'<div class="mut sm">'+esc(ivIw(b.i))+' · '+esc(IVSRC[b.s]||b.s)+'</div></td></tr>').join('')+'</tbody></table></div>';
  if(c.ivf&&c.ivf.length)h+='<h3 style="margin:14px 0 4px">O que desloca as bandas deste composto</h3><dl class="gl">'+c.ivf.map(f=>'<div><dt>'+esc(f[0])+'</dt><dd>'+esc(f[1])+'</dd></div>').join('')+'</dl>';
  h+=(c.ot&&c.ot.length)?'<h3 style="margin:14px 0 4px">Overtones, combinações e ressonância de Fermi</h3><dl class="gl">'+c.ot.map(o=>'<div><dt>'+esc(o[0])+' ('+esc(o[1])+' cm⁻¹)</dt><dd>'+esc(o[2])+' Fonte: '+esc(o[3])+'.</dd></div>').join('')+'</dl>':'<p class="sm">Overtones diagnósticos: nenhum esperado para este composto.</p>';
  h+=fuSug(c.gf);
  if(e&&e.disc.length)h+='<details class="sec"><summary>Como a disciplina atribui</summary><div class="tbl"><table class="obt"><thead><tr><th>Banda (cm⁻¹)</th><th>O que é</th></tr></thead><tbody>'+e.disc.map(r=>'<tr><td class="n">'+r[0]+'</td><td>'+esc(r[1])+'</td></tr>').join('')+'</tbody></table></div></details>';
  h+='<p class="hint" style="margin-top:12px"><button class="btn ghost" type="button" data-cf="'+c.i+'">Abrir a ficha de '+esc(c.n)+'</button></p>';
  box.innerHTML=h;
}
document.addEventListener('change',ev=>{if(ev.target.id==='ivSel'){ivC=+ev.target.value;drawIV();}});
document.addEventListener('input',ev=>{if(ev.target.id==='ivQ')drawIVChips();});

/* ---------- Identificar: contagem por seção ---------- */
function icBadges(){
  const v=id=>{const e=$('#'+id);return e&&String(e.value).trim()!==''?1:0;};
  const n=Object.values(icSt.el||{}).filter(Boolean).length,ir=Object.values(icSt.ir||{}).filter(Boolean).length+v('icIV');
  const c={1:(icSt.est?1:0)+(icSt.cor?1:0),2:icSt.g?1:0,3:v('icPF')+v('icPE'),4:n,5:ir,7:Object.values(icSt.sub||{}).filter(Boolean).length,6:['icF','icGDH','icGF','icM','icP','icH','icC','icHd'].reduce((a,k)=>a+v(k),0)};
  document.querySelectorAll('#p-ic .bdg').forEach(b=>{const k=+b.dataset.b;b.textContent=c[k]?c[k]+(c[k]>1?' marcados':' marcado'):'';});
}
document.addEventListener('click',ev=>{if(typeof CUR!=='undefined'&&CUR==='p-ic')setTimeout(icBadges,120);});
document.addEventListener('input',ev=>{if(typeof CUR!=='undefined'&&CUR==='p-ic')setTimeout(icBadges,120);});
document.addEventListener('change',ev=>{if(typeof CUR!=='undefined'&&CUR==='p-ic')setTimeout(icBadges,120);});

/* ---------- Destaque do trecho da molécula e botão Ampliar ---------- */
function hlSet(sc,atoms){
  sc.querySelectorAll('svg .hl.on').forEach(e=>e.classList.remove('on'));
  atoms.forEach(a=>sc.querySelectorAll('svg .hl.h'+a).forEach(e=>e.classList.add('on')));
}
function hlClick(el){
  const sc=el.closest('[data-hlscope]');if(!sc)return;
  const was=el.classList.contains('sel'),ro=sc.querySelector('.hlro'),fig=sc.querySelector('.hlfig');
  sc.querySelectorAll('.sel').forEach(e=>e.classList.remove('sel'));
  if(was){hlSet(sc,[]);if(ro)ro.textContent=ro.dataset.dica||'';if(fig)fig.classList.remove('stuck');return;}
  sc.querySelectorAll('[data-hk="'+el.dataset.hk+'"]').forEach(e=>e.classList.add('sel'));
  hlSet(sc,(el.dataset.at||'').split(',').filter(Boolean).map(Number));
  if(ro)ro.textContent=el.dataset.tx||'';
  if(fig&&!sc.classList.contains('zmov'))fig.classList.add('stuck');
}
document.addEventListener('click',ev=>{
  const z=ev.target.closest('[data-zoom]');if(z){zoomOpen(z);return;}
  const el=ev.target.closest('[data-at]');if(el)hlClick(el);
});
document.addEventListener('keydown',ev=>{
  if((ev.key==='Enter'||ev.key===' ')&&ev.target.matches&&ev.target.matches('.hpk[data-at]')){ev.preventDefault();hlClick(ev.target);}
});
function zoomOpen(btn){
  const wrap=btn.closest('.nmrwrap'),svg=wrap&&wrap.querySelector('svg.nmrspec');if(!svg)return;
  const sc=wrap.closest('[data-hlscope]'),fg=sc&&sc.querySelector('.hlfig svg');
  const o=document.createElement('div');o.className='zmov';o.setAttribute('data-hlscope','');o.setAttribute('role','dialog');o.setAttribute('aria-modal','true');o.setAttribute('aria-label','Espectro ampliado');
  const dica='Toque num número para ver o trecho da molécula. Arraste para os lados para ver o espectro todo.';
  o.innerHTML='<div class="zmh"><b>Espectro ampliado</b><button type="button" class="btn zmx">Fechar</button></div>'
    +(fg?'<figure class="st hlfig zmfig"><div>'+fg.outerHTML+'</div><div class="hlro" data-dica="'+dica+'">'+dica+'</div></figure>':'<div class="hlro" data-dica="'+dica+'">'+dica+'</div>')
    +'<div class="zmsc"><div class="zmsp">'+svg.outerHTML+'</div></div>';
  const close=()=>{document.removeEventListener('keydown',kd);o.remove();document.body.classList.remove('zmopen');btn.focus();};
  const kd=e=>{if(e.key==='Escape')close();};
  document.addEventListener('keydown',kd);
  o.querySelector('.zmx').onclick=close;
  document.body.classList.add('zmopen');document.body.appendChild(o);o.querySelector('.zmx').focus();
}

/* ---------- RMN: aba didática (figuras, laboratório de acoplamento, cálculos, macetes) ---------- */
(function(){
  const NS='http://www.w3.org/2000/svg',fr=(x,d)=>(+x).toFixed(d==null?2:d).replace('.',',');
  const NM={0:'singleto',1:'dubleto',2:'tripleto',3:'quarteto',4:'quinteto',5:'sexteto',6:'septeto'},AB={0:'s',1:'d',2:'t',3:'q',4:'quint',5:'sext',6:'sept'};
  const PASC=n=>{let r=[1];for(let i=0;i<n;i++){const s=[1];for(let k=1;k<r.length;k++)s.push(r[k-1]+r[k]);s.push(1);r=s;}return r;};
  /* um sinal lorentziano com as linhas de n+1 */
  function sinal(d0,n,J,pw,span,hi){return PASC(n).map((w,k)=>({x:d0+(k-n/2)*J,w:w}));}
  /* ---- figura 1: acetato de etila anotado ---- */
  function fig1(){
    const W=340,H=210,L=12,R=12,top=40,base=196,hi=5,lo=0,px=d=>L+(hi-d)/(hi-lo)*(W-L-R);
    const S=[{d:4.119,n:3,h:2,l:'q',lab:'CH₂'},{d:2.038,n:0,h:3,l:'s',lab:'CH₃–C=O'},{d:1.26,n:2,h:3,l:'t',lab:'CH₃'}];
    const J=0.075,g=0.012,N=700,pw=W-L-R;let ys=[];let mx=0;
    for(let k=0;k<=N;k++){const d=hi-k/N*(hi-lo);let y=0;
      S.forEach(s=>{const ls=sinal(s.d,s.n,J),sw=ls.reduce((a,b)=>a+b.w,0);ls.forEach(l=>{const t=d-l.x;y+=s.h*(l.w/sw)*g/Math.PI/(t*t+g*g);});});
      ys.push(y);if(y>mx)mx=y;}
    const Y=v=>base-v/mx*80;let p='';ys.forEach((y,k)=>p+=(k?'L':'M')+(L+k/N*pw).toFixed(1)+','+Y(y).toFixed(1));
    let tk='';for(let d=0;d<=5;d++){tk+='<line class="tk" x1="'+px(d)+'" y1="'+base+'" x2="'+px(d)+'" y2="'+(base+4)+'"/><text class="tl" x="'+px(d)+'" y="'+(base+15)+'" text-anchor="middle">'+d+'</text>';}
    /* integração em degraus: sobe da esquerda para a direita (δ alto → baixo) */
    let acc=0,ip='M'+L+','+(base-96),tot=8;const step=h=>h/tot*40;
    let ibase=108,iy=ibase;ip='M'+L+','+iy.toFixed(1);
    let ilab='';
    S.forEach(s=>{const x0=px(s.d+0.45),x1=px(s.d-0.45),y1=iy-step(s.h);ip+='L'+x0.toFixed(1)+','+iy.toFixed(1)+'L'+x1.toFixed(1)+','+y1.toFixed(1);iy=y1;
      ilab+='<text class="rmt" x="'+(px(s.d)+0).toFixed(1)+'" y="'+(iy-4).toFixed(1)+'" text-anchor="middle" fill="var(--blue)">'+s.h+' H</text>';});
    ip+='L'+(W-R)+','+iy.toFixed(1);
    const badge=(x,y,n)=>'<circle cx="'+x+'" cy="'+y+'" r="8" fill="var(--keep)"/><text x="'+x+'" y="'+(y+3.6)+'" text-anchor="middle" font-size="10.5" font-weight="700" fill="var(--surface)">'+n+'</text>';
    let lbl='';S.forEach(s=>{lbl+='<text class="rmt" x="'+px(s.d).toFixed(1)+'" y="'+(base+40)+'" text-anchor="middle">'+s.l+'</text>'
      +'<text class="rmt mut" x="'+px(s.d).toFixed(1)+'" y="'+(base+53)+'" text-anchor="middle">'+s.lab+'</text>';
      lbl+='<text class="rmt" x="'+px(s.d).toFixed(1)+'" y="'+(base+66)+'" text-anchor="middle" style="font-size:9.5px">'+fr(s.d,2)+'</text>';});
    return '<svg viewBox="0 0 '+W+' '+(base+74)+'" class="nmrspec" role="img" aria-label="Espectro de 1H do acetato de etila com os quatro passos de leitura">'
      +'<path d="'+ip+'" fill="none" stroke="var(--blue)" stroke-width="1.4"/>'+ilab
      +'<path class="sp" d="'+p+'"/><line class="ax" x1="'+L+'" y1="'+base+'" x2="'+(W-R)+'" y2="'+base+'"/>'+tk
      +'<text class="tl" x="'+(W/2)+'" y="'+(base+28)+'" text-anchor="middle" style="font-size:9px">δ (ppm)</text>'+lbl
      +badge(20,16,1)+'<text class="rmt" x="34" y="19.5">3 sinais</text>'
      +badge(130,16,2)+'<text class="rmt" x="144" y="19.5">posição em ppm</text>'
      +badge(20,34,3)+'<text class="rmt" x="34" y="37.5" fill="var(--blue)">integral (degraus)</text>'
      +badge(200,34,4)+'<text class="rmt" x="214" y="37.5">forma: q, s, t</text>'
      +'</svg>';
  }
  /* ---- régua de deslocamento ---- */
  function ruler(){
    const W=340,L0=96,R0=8,mx=13,pxd=d=>L0+(mx-d)/mx*(W-L0-R0),rh=19,top=34;
    const B=[['Alifático (CH₃, CH₂, CH)',0.8,2.0,'--keep'],['α a C=O, anel ou N',2.0,3.2,'--blue'],['H–C–O e H–C–X',3.0,4.4,'--amber'],['Alceno',4.5,6.5,'--lost'],['Aromático',6.5,8.4,'--blue'],['Aldeído',9.3,10.1,'--keep'],['Ácido COOH',10,13,'--lost'],['O–H, N–H (varia)',0.5,8.5,'--muted',1]];
    const H=top+B.length*rh+30;let s='';
    s+='<text class="rmt mut" x="'+(W-R0)+'" y="12" text-anchor="end">blindado ← mais elétrons em volta</text><text class="rmt mut" x="'+L0+'" y="12">desblindado →</text>';
    s+='<line x1="'+L0+'" y1="19" x2="'+(W-R0)+'" y2="19" stroke="var(--muted)" stroke-width="1" marker-end="none"/>';
    B.forEach((b,i)=>{const y=top+i*rh,x0=pxd(b[2]),x1=pxd(b[1]);
      s+='<text class="rmt" x="2" y="'+(y+12)+'" style="font-size:9.5px">'+b[0]+'</text>'
        +'<rect x="'+x0.toFixed(1)+'" y="'+y+'" width="'+(x1-x0).toFixed(1)+'" height="14" rx="3" fill="var('+b[3]+')" opacity="'+(b[4]?.28:.75)+'"'+(b[4]?' stroke="var(--muted)" stroke-dasharray="3 2"':'')+'/>';});
    const yb=top+B.length*rh+2;s+='<line class="ax" x1="'+L0+'" y1="'+yb+'" x2="'+(W-R0)+'" y2="'+yb+'"/>';
    for(let d=0;d<=13;d++){s+='<line class="tk" x1="'+pxd(d)+'" y1="'+yb+'" x2="'+pxd(d)+'" y2="'+(yb+4)+'"/><text class="tl" x="'+pxd(d)+'" y="'+(yb+15)+'" text-anchor="middle">'+d+'</text>';}
    s+='<text class="rmt mut" x="'+(W-R0)+'" y="'+(yb+28)+'" text-anchor="end" style="font-size:9px">0 = TMS</text><text class="tl" x="'+L0+'" y="'+(yb+28)+'" style="font-size:9px">δ (ppm)</text>';
    return '<svg viewBox="0 0 '+W+' '+H+'" class="nmrspec" role="img" aria-label="Régua com as regiões de deslocamento químico de 1H">'+s+'</svg>';
  }
  /* ---- laboratório de acoplamento ---- */
  function lab(){
    const o=document.getElementById('lbOut');if(!o)return;
    let n1=+$('#lbN1').value,n2=+$('#lbN2').value,J1=Math.max(.5,+$('#lbJ1').value||7),J2=Math.max(.5,+$('#lbJ2').value||2);
    let gr=[];if(n1>0)gr.push({n:n1,J:J1,c:0});if(n2>0)gr.push({n:n2,J:J2,c:1});
    const eq=gr.length===2&&Math.abs(J1-J2)<0.05;
    if(eq)gr=[{n:n1+n2,J:J1,c:0}];
    gr.sort((a,b)=>b.J-a.J);
    const steps=[];gr.forEach(g=>{for(let i=0;i<g.n;i++)steps.push([g.J,g.c]);});
    if(steps.length>8){o.innerHTML='<p class="srcl">O desenho vai até 8 H vizinhos no total.</p>';return;}
    let cur=[{x:0,w:1}];const lv=[cur],ed=[];
    steps.forEach(st=>{const nx={},e=[];cur.forEach(l=>{[-1,1].forEach(sg=>{const x=+(l.x+sg*st[0]/2).toFixed(3);(nx[x]=nx[x]||{x:x,w:0}).w+=l.w;e.push([l.x,x]);});});
      cur=Object.values(nx).sort((a,b)=>a.x-b.x);lv.push(cur);ed.push(e);});
    const span=steps.reduce((a,b)=>a+b[0],0),W=340,cx=W/2,sc=Math.min(14,250/Math.max(span,10)),dy=20,top=22,K=steps.length;
    const base=top+K*dy+54,mw=Math.max(...cur.map(l=>l.w));
    let s='<text class="rmt mut" x="'+cx+'" y="12" text-anchor="middle">um H, sem vizinhos</text>';
    s+='<line x1="'+cx+'" y1="'+(top-6)+'" x2="'+cx+'" y2="'+top+'" stroke="var(--ink)" stroke-width="1.6"/>';
    ed.forEach((e,i)=>{const y0=top+i*dy,y1=y0+dy,col=steps[i][1]?'var(--blue)':'var(--ink)';
      e.forEach(p=>{s+='<line x1="'+(cx+p[0]*sc).toFixed(1)+'" y1="'+y0+'" x2="'+(cx+p[1]*sc).toFixed(1)+'" y2="'+y1+'" stroke="'+col+'" stroke-width="1" opacity=".75"/>';});});
    const yE=top+K*dy;
    cur.forEach(l=>{const x=(cx+l.x*sc).toFixed(1),h=8+l.w/mw*34;
      s+='<line x1="'+x+'" y1="'+yE+'" x2="'+x+'" y2="'+(yE+h)+'" stroke="var(--ink)" stroke-width="2.2"/><text class="rmt" x="'+x+'" y="'+(yE+h+12)+'" text-anchor="middle" style="font-size:10px">'+l.w+'</text>';});
    if(!K)s+='<text class="rmt" x="'+cx+'" y="'+(top+30)+'" text-anchor="middle">1 linha: singleto</text>';
    const nl=cur.length,ws=cur.map(l=>l.w).join(' : ');
    let nome;
    if(!K)nome='singleto (s)';
    else if(gr.length===1)nome=(NM[gr[0].n]||'multipleto')+(AB[gr[0].n]?' ('+AB[gr[0].n]+')':'');
    else{const a=AB[gr[0].n],b=AB[gr[1].n];nome=(a&&b)?'"'+(NM[gr[0].n])+' de '+NM[gr[1].n].replace('dubleto','dubletos').replace('tripleto','tripletos').replace('quarteto','quartetos').replace('quinteto','quintetos')+'" ('+a+b+')':'multipleto (m)';}
    let txt='<p style="margin:8px 0 0"><b>'+nome+'</b>: '+nl+(nl>1?' linhas':' linha')+(K?', alturas '+ws+'.':'.')+'</p>';
    if(eq)txt+='<p class="srcl">As duas J são iguais, então as linhas se sobrepõem e vale n+1 com n = '+(n1+n2)+'.</p>';
    else if(gr.length===2)txt+='<p class="srcl">Cada linha do grupo de J maior ('+fr(gr[0].J,1)+' Hz) se divide de novo pelo grupo de J menor ('+fr(gr[1].J,1)+' Hz). Linhas: ('+(gr[0].n+1)+') × ('+(gr[1].n+1)+') = '+(gr[0].n+1)*(gr[1].n+1)+'.</p>';
    else if(K)txt+='<p class="srcl">'+gr[0].n+' H vizinhos: n + 1 = '+(gr[0].n+1)+' linhas. A distância entre linhas vizinhas é a J = '+fr(gr[0].J,1)+' Hz.</p>';
    o.innerHTML='<svg viewBox="0 0 '+W+' '+(base+6)+'" class="nmrspec" role="img" aria-label="Desdobramento do sinal: '+nome+'">'+s+'<line class="ax" x1="12" y1="'+(yE+46)+'" x2="'+(W-12)+'" y2="'+(yE+46)+'" style="display:none"/></svg>'+txt;
  }
  /* ---- calculadoras ---- */
  function calcF(){
    const F=+$('#cxF').value,D=+$('#cxD').value,J=+$('#cxJ').value,o=$('#cxOut');if(!(F>0)){o.innerHTML='';return;}
    o.innerHTML='<div class="rmcalcr"><span>δ em Hz do TMS</span><b>'+fr(D*F,1)+' Hz</b><em>'+fr(D,2)+' ppm × '+fr(F,1)+' MHz</em></div>'
      +'<div class="rmcalcr"><span>J em ppm</span><b>'+fr(J/F,4)+' ppm</b><em>'+fr(J,1)+' Hz ÷ '+fr(F,1)+' MHz</em></div>'
      +'<div class="rmcalcr"><span>Campo magnético B₀</span><b>'+fr(F/42.577,2)+' T</b><em>¹H: 42,577 MHz por tesla</em></div>'
      +'<div class="rmcalcr"><span>Frequência do ¹³C neste campo</span><b>'+fr(F*0.25145,1)+' MHz</b><em>cerca de ¼ da do ¹H</em></div>';
    const T=$('#cxTab');
    T.innerHTML='<div class="tbl"><table class="obt nostk"><thead><tr><th>Aparelho</th><th>Sinal de '+fr(D,2)+' ppm, em Hz</th><th>J de '+fr(J,1)+' Hz, em ppm</th></tr></thead><tbody>'
      +[60,90,300,400,600].map(f=>'<tr><td>'+f+' MHz</td><td class="n">'+fr(D*f,0)+'</td><td class="n">'+fr(J/f,4)+'</td></tr>').join('')+'</tbody></table></div>';
  }
  function calcI(){
    const v=$('#cgI').value.split(/[\s;]+/).map(x=>parseFloat(x.replace(',','.'))).filter(x=>x>0),T=+$('#cgT').value,o=$('#cgOut');
    if(!v.length){o.innerHTML='<p class="srcl">Digite os valores das integrais.</p>';return;}
    const mn=Math.min(...v),r=v.map(x=>x/mn);let k=0;
    for(let m=1;m<=8&&!k;m++)if(r.every(x=>Math.abs(x*m-Math.round(x*m))<0.15))k=m;
    let h='<div class="tbl"><table class="obt nostk"><thead><tr><th>Sinal</th><th>Valor</th><th>÷ menor</th>'+(k>1?'<th>× '+k+'</th>':'')+(T>0?'<th>× '+T+' ÷ soma</th>':'')+'</tr></thead><tbody>';
    const sum=v.reduce((a,b)=>a+b,0);
    v.forEach((x,i)=>{h+='<tr><td>'+(i+1)+'</td><td class="n">'+fr(x,1)+'</td><td class="n">'+fr(r[i],2)+'</td>'+(k>1?'<td class="n">'+fr(r[i]*k,2)+'</td>':'')+(T>0?'<td class="n"><b>'+fr(x/sum*T,2)+'</b></td>':'')+'</tr>';});
    h+='</tbody></table></div>';
    if(k){const ints=r.map(x=>Math.round(x*k));h+='<p style="margin:8px 0 0"><b>Proporção: '+ints.join(' : ')+'</b> (soma '+ints.reduce((a,b)=>a+b,0)+').'+(T>0?(ints.reduce((a,b)=>a+b,0)===T?' Bate com os '+T+' H da fórmula.':' A fórmula tem '+T+' H: '+(T%ints.reduce((a,b)=>a+b,0)===0?'multiplique a proporção por '+T/ints.reduce((a,b)=>a+b,0)+'.':'confira se falta um sinal ou se a proporção está certa.')):'')+'</p>';}
    else h+='<p class="srcl" style="margin-top:8px">Não deu proporção de números inteiros pequenos. Confira as medidas ou procure um sinal sobreposto.</p>';
    if(T>0)h+='<p class="srcl">A última coluna distribui o total de H da fórmula na proporção das áreas. O valor mais próximo de um inteiro é o número de H do sinal.</p>';
    o.innerHTML=h;
  }
  function calcG(){
    const C=+$('#gdC').value,H=+$('#gdH').value,N=+$('#gdN').value,X=+$('#gdX').value,o=$('#gdOut'),g=(2*C+2+N-H-X)/2;
    let m;
    if(!Number.isInteger(g)||g<0)m='Resultado inválido: confira a fórmula (para uma molécula neutra o GDH é inteiro e não negativo).';
    else if(g===0)m='Sem anel e sem ligação π: cadeia saturada. No ¹H, não espere sinais acima de ~4,5 ppm além de O–H e N–H.';
    else if(g===1)m='Um anel <b>ou</b> uma ligação π (C=O, C=C). O IV ajuda a decidir: banda de C=O perto de 1700 aponta para carbonila.';
    else if(g>=4)m='4 ou mais: pense em anel benzênico (3 ligações π + 1 anel = 4). Procure sinais em 6,5 a 8,5 ppm.';
    else m='Duas ou três insaturações: combine anéis, C=C, C=O, C≡C (conta 2) e C≡N (conta 2).';
    o.innerHTML='<div class="rmcalcr"><span>GDH</span><b>'+(Number.isFinite(g)?fr(g,Number.isInteger(g)?0:1):'—')+'</b><em>(2·'+C+' + 2 + '+N+' − '+H+' − '+X+') ÷ 2</em></div><p style="margin:6px 0 0">'+m+'</p>';
  }
  function tabSinais(){
    const el=$('#cqTab');if(!el||typeof COMP==='undefined')return;
    const want=['etanol','acetona','éter dietílico','ciclohexano','tolueno','benzeno','acetato de etila','2-butanona'];
    const rows=[];want.forEach(w=>{const c=COMP.find(x=>x.n.toLowerCase()===w);if(c&&c.h1&&c.c13)rows.push('<tr><td>'+esc(c.n)+' <span class="mut sm">'+fmt(c.f)+'</span></td><td class="n">'+c.h1.length+'</td><td class="n">'+c.c13.length+'</td></tr>');});
    el.innerHTML=rows.length?'<div class="tbl"><table class="obt nostk"><thead><tr><th>Composto</th><th>Sinais de ¹H</th><th>Sinais de ¹³C</th></tr></thead><tbody>'+rows.join('')+'</tbody></table></div><p class="srcl" style="margin-top:6px">Contagem teórica, pela simetria da estrutura. No espectro real, sinais com δ muito parecido podem se sobrepor e aparecer como um só.</p>':'';
  }
  /* ---- macetes ---- */
  function mini(t){
    const one=(n,x)=>PASC(n).map((w,k)=>{const xx=x+(k-n/2)*7,h=4+w/Math.max(...PASC(n))*16;return '<line x1="'+xx+'" y1="30" x2="'+xx+'" y2="'+(30-h)+'" stroke="var(--ink)" stroke-width="2"/>';}).join('');
    const map={s:[[0,20]],d:[[1,20]],t:[[2,20]],q:[[3,20]],'t+q':[[2,22],[3,66]],'d+sept':[[1,22],[6,70]],'d+d':[[1,22],[1,66]]};
    const lst=map[t]||map.s;
    return '<svg viewBox="0 0 100 34" width="100" height="34" aria-hidden="true">'+lst.map(a=>one(a[0],a[1])).join('')+'<line x1="2" y1="31" x2="98" y2="31" stroke="var(--line)"/></svg>';
  }
  const MAC=[
    ['Ordem de ataque',null,'Fórmula → GDH → número de sinais → integração → δ → multiplicidade → monte os pedaços. Pular um passo é onde mais se erra.'],
    ['A soma das integrais é o total de H',null,'Se a conta não fecha, falta um sinal (um O–H largo, por exemplo) ou a proporção está errada. Confira antes de interpretar.'],
    ['Etila: tripleto + quarteto','t+q','CH₃ em tripleto (~1,2) e CH₂ em quarteto, com a mesma J (~7 Hz). Onde o quarteto cai mostra quem está ligado ao CH₂: ~2,4 ao lado de C=O (2-butanona, 2,449), ~3,4 a 3,5 em éter e ~4,1 em éster (acetato de etila, 4,119).'],
    ['Isopropila: dubleto de 6 H + septeto de 1 H','d+sept','Dois CH₃ iguais presos a um mesmo CH. O CH vê 6 H e vira septeto; os CH₃ veem 1 H e viram dubleto.'],
    ['tert-butila: singleto grande de 9 H','s','Nove H iguais e nenhum vizinho com H. Um singleto altíssimo, em torno de 1,0 a 1,3.'],
    ['Singleto de 3 H: olhe o δ','s','~2,1: CH₃–C=O (2-butanona, 2,139). ~2,3: CH₃ preso a anel (tolueno). ~3,3 a 3,9: CH₃–O (anisol, 3,745; salicilato de metila, 3,926).'],
    ['Quem corta o acoplamento',null,'O, N, C=O e carbono sem H não passam o acoplamento. Os H de um lado e do outro deles não se enxergam. Por isso CH₃–O e CH₃–C=O saem em singleto.'],
    ['Sinal largo que some com D₂O',null,'É O–H, N–H ou COOH. Uma gota de D₂O troca o H por D e o sinal desaparece. Esse H também não desdobra os vizinhos, em geral.'],
    ['Região de cada coisa, de relance',null,'Acima de 10: ácido carboxílico. 9 a 10: aldeído. 6,5 a 8,5: aromático. 4,5 a 6,5: alceno. 3 a 4,5: H em carbono com O ou halogênio. 2 a 3: ao lado de C=O ou de anel. Abaixo de 2: alcano.'],
    ['Aldeído: o sinal solitário',null,'Um pico de 1 H entre 9 e 10 ppm. Se há CH ao lado, vira tripleto ou dubleto fino (J de 1 a 3 Hz). Se for aromático (benzaldeído), é singleto.'],
    ['Anel aromático',null,'Monossubstituído: 5 H juntos perto de 7,1 a 7,4. Para com grupos diferentes: dois "dubletos" de 2 H, J ≈ 8 Hz. Para com grupos iguais: um só singleto.'],
    ['A mesma J nos dois sinais','d+d','Dois grupos que se acoplam mostram a mesma J. Para ligar pedaços, procure pares com a mesma J: tripleto de 7 Hz só combina com quarteto de 7 Hz.'],
    ['Erro comum: contar os H do próprio carbono',null,'Na regra n+1, n são os H dos carbonos <b>vizinhos</b>. Os H do próprio grupo não desdobram o sinal dele.'],
    ['Telhado aponta para o parceiro',null,'Dois sinais acoplados e próximos se inclinam um para o outro, como um telhado. O lado mais alto aponta para o H com que ele se acopla.'],
    ['¹³C: conte carbonos diferentes',null,'Simetria junta carbonos iguais num só sinal. Benzeno monossubstituído: 4 sinais para 6 C (ipso, orto, meta, para). Para-xileno: 3 sinais (CH₃, C do anel com CH₃, CH do anel).'],
    ['¹³C: onde cada coisa cai',null,'Abaixo de 90: sp³. 100 a 150: alceno e aromático. 160 a 185: éster, ácido, amida. 190 a 220: aldeído e cetona. Carbono sem H (C=O, quaternário) costuma sair mais baixo que os outros.'],
    ['DEPT-135: quantos H tem cada C',null,'CH e CH₃ saem para cima, CH₂ para baixo, e carbono sem H não aparece. Com isso você separa CH₃/CH de CH₂ e acha os quaternários pelo que falta.'],
    ['Pico de solvente não é composto',null,'CDCl₃: ¹H em 7,26 e ¹³C em 77,2. DMSO-d₆: 2,50 e 39,5. D₂O: 4,79. Tire esses picos antes de contar sinais.'],
    ['GDH ≥ 4 e sinais entre 6,5 e 8,5',null,'Quase sempre é um anel benzênico (3 ligações π + 1 anel = 4). Confira o padrão de substituição pelo número de H aromáticos.']
  ];
  function macDraw(){const o=$('#rmMac');if(!o||o.dataset.ok)return;o.dataset.ok='1';
    o.innerHTML=MAC.map(m=>'<div class="rule rmtip"><div class="rmtipt"><h3>'+m[0]+'</h3>'+(m[1]?'<div class="rmmini">'+mini(m[1])+'</div>':'')+'</div><p>'+m[2]+'</p></div>').join('')
      +'<p class="srcl">Regras de bolso de livro-texto, sem fonte conferida. Os δ citados de compostos (2-butanona, acetato de etila, anisol, salicilato de metila) vêm dos prints do SDBS enviados. Regras não substituem os quatro passos.</p>';}

  /* ---- Treinar: perguntas de RMN geradas dos compostos do app ---- */
  const MULT={'s':0,'d':1,'t':2,'q':3,'quinteto':4,'sexteto':5,'septeto':6};
  const MNOME={0:'singleto',1:'dupleto',2:'tripleto',3:'quarteto',4:'quinteto',5:'sexteto',6:'septeto'};
  let TQ='todas',TS={ok:0,n:0},TCUR=null;
  const pick=a=>a[Math.floor(Math.random()*a.length)];
  const mix=a=>a.map(x=>[Math.random(),x]).sort((p,q)=>p[0]-q[0]).map(p=>p[1]);
  function trnMake(){
    const tipos=TQ==='todas'?['h','c','m','q']:[TQ];let t=pick(tipos),tent=0;
    while(tent++<40){
      const c=pick(COMP.filter(x=>x.h1&&x.h1.length&&x.c13&&x.c13.length&&(t==='c'||t==='m'||!x.h1.some(y=>/arom/i.test(y.t)))));
      if(t==='h'||t==='c'){
        const real=t==='h'?c.h1.length:c.c13.length;
        let op=[real];[real-1,real+1,real+2,real-2,real+3].forEach(v=>{if(v>=1&&op.indexOf(v)<0&&op.length<4)op.push(v);});
        const ex=t==='h'?'Cada sinal é um grupo de H equivalentes: '+c.h1.map(x=>x.t+' ('+x.h+' H)').join('; ')+'.':'Cada sinal é um tipo de C: '+c.c13.map(x=>x.t+(x.n>1?' ('+x.n+' C)':'')).join('; ')+'.';
        return{t:t,c:c,q:'Quantos sinais de '+(t==='h'?'¹H':'¹³C')+' tem '+c.n+'?',op:mix(op).map(v=>({k:String(v),v:String(v)})),ok:String(real),ex:ex+' Total: '+real+'.'};
      }
      if(t==='m'){
        const un=c.h1.filter(x=>MULT[x.m]!==undefined&&c.h1.filter(y=>y.t===x.t).length===1);if(!un.length)continue;
        const x=pick(un),real=MULT[x.m];let op=[real];mix([0,1,2,3,4,5,6]).forEach(v=>{if(op.length<4&&op.indexOf(v)<0)op.push(v);});
        return{t:t,c:c,q:'No '+c.n+', como aparece o sinal de '+x.t+' ('+x.h+' H)?',op:mix(op).map(v=>({k:String(v),v:MNOME[v]})),ok:String(real),ex:'Regra n+1: o sinal aparece como '+MNOME[real]+', então o grupo tem '+real+' H vizinho'+(real===1?'':'s')+' (n = '+real+', n+1 = '+(real+1)+').'};
      }
      if(t==='q'){
        const mesmo=COMP.filter(y=>y!==c&&y.h1&&y.h1.length===c.h1.length&&y.c13&&y.c13.length);if(mesmo.length<3)continue;
        const sig=y=>y.h1.map(x=>x.h+x.m+x.lo+x.hi).sort().join('|');if(mesmo.some(y=>sig(y)===sig(c)))continue;
        const op=[c].concat(mix(mesmo).slice(0,3));
        const lin=c.h1.slice().sort((a,b)=>(b.lo+b.hi)-(a.lo+a.hi)).map(x=>'δ '+String(x.lo).replace('.',',')+' a '+String(x.hi).replace('.',',')+' ppm · '+x.h+' H · '+x.m).join('<br>');
        return{t:t,c:c,q:'Qual composto tem estes sinais de ¹H, com a fórmula '+fmt(c.f)+'?',tab:lin,op:mix(op).map(y=>({k:y.n,v:y.n})),ok:c.n,ex:'Os sinais de '+c.n+': '+c.h1.map(x=>x.t+' ('+x.h+' H, '+x.m+')').join('; ')+'.',noF:1};
      }
    }
    return null;
  }
  function trnDraw(){
    const box=$('#trnQ');if(!box)return;const q=trnMake();TCUR=q;
    if(!q){box.innerHTML='<p class="empty">Não consegui montar uma pergunta agora. Toque em outro tipo.</p>';return;}
    $('#trnPlacar').textContent=TS.n?'Acertos: '+TS.ok+' de '+TS.n+'.':'Escolha uma resposta.';
    box.innerHTML='<div class="rule"><h3 style="margin:0 0 8px">'+q.q+'</h3>'
      +(q.t==='q'?'<p class="mut" style="margin:0 0 8px">'+q.tab+'</p>':'<figure class="st" style="margin:0 0 8px"><div>'+(q.c.si||q.c.s)+'</div></figure>')
      +'<div class="chips" id="trnOp">'+q.op.map(o=>'<button class="chip" type="button" data-k="'+ea(o.k)+'">'+esc(o.v)+'</button>').join('')+'</div><div id="trnFb" aria-live="polite"></div></div>';
    $('#trnOp').onclick=e=>{const b=e.target.closest('[data-k]');if(!b||$('#trnOp').dataset.done)return;$('#trnOp').dataset.done=1;
      const ok=b.dataset.k===q.ok;TS.n++;if(ok)TS.ok++;
      $('#trnOp').querySelectorAll('[data-k]').forEach(x=>{if(x.dataset.k===q.ok)x.style.cssText='background:var(--keep);color:var(--surface);border-color:var(--keep)';else if(x===b)x.style.cssText='border-color:#b3261e;color:#b3261e';x.disabled=true;});
      $('#trnFb').innerHTML='<div class="ans" style="margin-top:10px"><span class="t">'+(ok?'Certo.':'Errado.')+'</span> '+q.ex+'</div><div class="row" style="margin-top:8px"><button class="btn" type="button" id="trnNx">Próxima pergunta</button></div>';
      $('#trnPlacar').textContent='Acertos: '+TS.ok+' de '+TS.n+'.';$('#trnNx').onclick=trnDraw;$('#trnNx').focus();};
  }
  document.addEventListener('click',e=>{const b=e.target.closest('[data-tq]');if(!b)return;TQ=b.dataset.tq;document.querySelectorAll('[data-tq]').forEach(x=>x.setAttribute('aria-pressed',x===b?'true':'false'));trnDraw();});
  /* ---- troca de painel ---- */
  function rp(k){
    document.querySelectorAll('[data-rpane]').forEach(d=>d.hidden=d.dataset.rpane!==k);
    document.querySelectorAll('.rseg [data-rp]').forEach(b=>b.setAttribute('aria-pressed',b.dataset.rp===k?'true':'false'));
    if(k==='mac')macDraw();
    if(k==='treino'&&!TCUR)trnDraw();
    try{sessionStorage.setItem('massas-rp',k);}catch(e){}
  }
  window.rmPane=rp;
  function init(){
    if(!document.getElementById('rmFig1'))return;
    $('#rmFig1').innerHTML=fig1();$('#rmRuler').innerHTML=ruler();
    const o1=[0,1,2,3,4,5,6].map(n=>'<option value="'+n+'">'+n+'</option>').join('');$('#lbN1').innerHTML=o1;    $('#lbN2').innerHTML=[0,1,2,3,4].map(n=>'<option value="'+n+'">'+n+'</option>').join('');
    $('#lbN1').value=3;$('#lbN2').value=0;
    const PRE=[['CH₂ de etila (3 H vizinhos)',3,7,0,2],['CH de isopropila (6 H)',6,7,0,2],['CH₂ do meio de propila (3 + 2 H)',3,7,2,7],['H de vinil (trans 17 + cis 10 Hz)',1,17,1,10],['H aromático (orto 8 + meta 2 Hz)',1,8,1,2]];
    $('#lbPre').innerHTML=PRE.map((p,i)=>'<button class="chip" type="button" data-pre="'+i+'">'+p[0]+'</button>').join('');
    $('#lbPre').onclick=e=>{const b=e.target.closest('[data-pre]');if(!b)return;const p=PRE[+b.dataset.pre];$('#lbN1').value=p[1];$('#lbJ1').value=p[2];$('#lbN2').value=p[3];$('#lbJ2').value=p[4];lab();};
    ['lbN1','lbN2','lbJ1','lbJ2'].forEach(i=>$('#'+i).addEventListener('input',lab));lab();
    ['cxF','cxD','cxJ'].forEach(i=>$('#'+i).addEventListener('input',calcF));calcF();
    ['cgI','cgT'].forEach(i=>$('#'+i).addEventListener('input',calcI));calcI();
    ['gdC','gdH','gdN','gdX'].forEach(i=>$('#'+i).addEventListener('input',calcG));calcG();
    tabSinais();
    document.querySelectorAll('.rseg [data-rp]').forEach(b=>b.onclick=()=>rp(b.dataset.rp));
    rp('ler');
  }
  init();
})();

/* ---------- Banco Analor (DBF do professor), dentro de Compostos ---------- */
let BD=null,BDT={b:[],g:[],f:[]},BDC=null;
const BDMASS={C:12,H:1,N:14,O:16,S:32,P:31,F:19,Cl:35,Br:79,I:127,Si:28,B:11,Se:80};
function bdLoad(){if(BD)return BD;try{const o=JSON.parse(BDJSON);BD=o.r;BDT=o.t}catch(e){BD=[]}return BD;}
/* "ACETONA" -> "Acetona"; mantém prefixos curtos (N, o-, p-) como estão */
let BDEN=null;
function bdEn(cas,fallback){if(!BDEN){BDEN={};bdLoad().forEach(r=>{if(r[0]&&r[3]&&!BDEN[r[0]])BDEN[r[0]]=bdNome(r[3]);});}return (cas&&BDEN[cas])||fallback||'';}
const BDFT={1:'Fórmula corrigida.',2:'Estrutura corrigida.',3:'Estrutura preenchida.',5:'Confira o nome e o CAS.'};
function bdNome(s){s=String(s||'').trim();s=s.replace(/[A-ZÀ-Ý]{2,}/g,m=>m.toLowerCase());return s.charAt(0).toUpperCase()+s.slice(1);}
function bdNominal(f,mw){const el=elCount(f);let m=0;for(const e in el){if(BDMASS[e]===undefined)return mw?Math.round(mw):null;m+=BDMASS[e]*el[e];}return m||(mw?Math.round(mw):null);}
function bdGdh(f){const e=elCount(f);for(const k in e)if(!['C','H','N','F','Cl','Br','I','O','S'].includes(k))return null;
  const g=(2*(e.C||0)+2+(e.N||0)-(e.H||0)-(e.F||0)-(e.Cl||0)-(e.Br||0)-(e.I||0))/2;return g>=0&&Number.isInteger(g)?g:null;}
/* estado a 25 °C pelo PF e PE do banco (não é dado do banco: é calculado) */
function bdEstado(pf,pe){if(pf!==null&&pf>25)return 'sólido';if(pf!==null&&pe!==null)return pe>25?'líquido':'gás';return '';}
/* compostos do banco no mesmo formato dos de COMP (os que já estão em COMP, pelo CAS, ficam só em COMP) */
function bdAll(){
  if(BDC)return BDC;const D=bdLoad(),cas=new Set(COMP.map(c=>c.cas));BDC=[];
  D.forEach((r,ix)=>{if(r[0]&&cas.has(r[0]))return;
    const ms=r[11],nm=bdNome(r[1]),M=bdNominal(r[4],r[5]);
    const c={i:1000+ix,bd:1,r,n:nm,a:[r[2],r[3]].filter(x=>x&&x.toLowerCase()!==r[1].toLowerCase()).map(bdNome),f:r[4]||'',cas:r[0]||'',mw:r[5],M:M,
      est:bdEstado(r[6],r[7]),cor:'',g:'',pf:r[6],pe:r[7],gdh:bdGdh(r[4]||''),
      gf:r[17]?r[17][0].map(i=>BDT.g[i]):[],iv:r[17]?r[17][1].map(i=>BDT.b[i]):[],ivf:r[17]?r[17][2].map(i=>BDT.f[i]):[],ot:(r[17]&&r[17][7])||[],
      ms:ms.length?ms.map(p=>p[0]):null,msi:ms.length?ms:null,sub:r[17]?r[17][5]:[],h1:r[17]?r[17][3].map(x=>({lo:x[0],hi:x[1],h:x[2],m:x[3]?'largo':''})):[],c13:r[17]?r[17][4].map(x=>({lo:x[0],hi:x[1],n:x[2]})):[],ge:r[17]?r[17][6]:'',flag:r[18],msalto:r[19],corr:r[20],casx:r[21],
      k:[r[1],r[2],r[3],r[4],r[0]].join(' ')};
    BDC.push(c);});
  return BDC;}
/* "m/z:intensidade" ou só "m/z"; devolve [[m/z,intensidade|null]] */
function bdPicos(s){return(String(s).match(/\d+(?::\d+(?:\.\d+)?)?/g)||[]).map(t=>{const a=t.split(':');return[Number(a[0]),a[1]===undefined?null:Number(a[1])];});}
/* lê JCAMP-DX (PEAK TABLE / XYDATA simples), CSV ou texto com pares; devolve até 12 picos [m/z inteiro, % da base] */
function bdParseSpec(tx){
  const pts=[];let on=false,jd=/##(PEAK TABLE|XYPOINTS|XYDATA|DATA TABLE)/i.test(tx);
  tx.split(/\r?\n/).forEach(l=>{
    if(/^##/.test(l)){on=/^##(PEAK TABLE|XYPOINTS|XYDATA|DATA TABLE)/i.test(l);return;}
    if(jd&&!on)return;
    const n=(l.replace(/[;,\t]+/g,' ').match(/-?\d+(?:\.\d+)?/g)||[]).map(Number);
    if(n.length>=2&&n.length%2===0)for(let i=0;i<n.length;i+=2)pts.push([n[i],n[i+1]]);
  });
  if(!pts.length)return[];
  const bins=new Map();pts.forEach(p=>{const m=Math.round(p[0]);if(m>0&&p[1]>0)bins.set(m,Math.max(bins.get(m)||0,p[1]));});
  const mx=Math.max(...bins.values());
  return[...bins].map(x=>[x[0],Math.round(x[1]/mx*100)]).filter(x=>x[1]>=3).sort((a,b)=>b[1]-a[1]).slice(0,12).sort((a,b)=>a[0]-b[0]);
}
/* IV: "3300l" = banda larga, "2250e" = banda estreita; sem letra, não se sabe */
function bdIvQuery(s){return(String(s).match(/\d{3,4}(?:\.\d+)?[lLeE]?/g)||[]).map(t=>({v:parseFloat(t),w:/[lL]$/.test(t)?'l':/[eE]$/.test(t)?'e':''})).filter(x=>x.v>=400&&x.v<=4000);}
/* Bandas esperadas (do grupo funcional, já com conjugação etc.) contra as bandas lidas.
   O meio muda a posição: solução diluída mostra O–H e N–H livres (finos, mais altos) e C=O de ácido monomérico mais alto; gás sobe o C=O.
   Esses deslocamentos por meio são regra geral de livro-texto; eu não os conferi em fonte nesta sessão. */
function bdScoreIV(c,Qi,meio){
  const B=c.iv.map(b=>({lo:Math.min(b[0],b[1]),hi:Math.max(b[0],b[1]),t:b[2],k:b[4],l:/larga/.test(b[3])}));
  if(!B.length)return{rec:1,prec:1,miss:[],un:[],note:'sem bandas esperadas'};
  const covers=(b,ob)=>{const o=ob.v;if(ob.w==='l'&&!b.l)return false;if(ob.w==='e'&&b.l)return false;let lo=b.lo,hi=b.hi,tol=20;
    if(/^[ON]–H/.test(b.t)){tol=30;if(meio==='sol'||meio==='gas')hi=b.t[0]==='O'?3680:3520;}
    if(/^C=O/.test(b.t)){if(meio==='gas')hi+=35;else if(meio==='sol'&&/ácido/.test(b.t+c.n+c.gf.join(' ')))hi+=15;}
    return o>=lo-tol&&o<=hi+tol;};
  (c.ot||[]).forEach(o=>{const m=String(o[1]).match(/(\d{3,4})\D+(\d{3,4})/);if(m)B.push({lo:Math.min(+m[1],+m[2]),hi:Math.max(+m[1],+m[2]),t:'overtone',k:false,l:false});});
  const used=new Set(),miss=[];let keys=0,hit=0;
  /* cada banda lida explica só uma banda esperada; as bandas-chave escolhem primeiro e pegam a mais perto do centro da faixa */
  B.filter(b=>b.k).forEach(b=>{keys++;let best=-1,bd=1e9;
    Qi.forEach((o,ix)=>{if(used.has(ix)||!covers(b,o))return;const d=Math.abs(o.v-(b.lo+b.hi)/2)/100;if(d<bd){bd=d;best=ix;}});
    if(best>=0){used.add(best);hit++;}else miss.push(b.t.split(' (')[0]+' ('+b.hi+'–'+b.lo+')');});
  const hi=Qi.filter(o=>o.v>1500),un=hi.filter(o=>!B.some(b=>covers(b,o))).map(o=>o.v);
  return{rec:keys?hit/keys:1,prec:hi.length?1-un.length/hi.length:1,miss,un};
}
/* Estrutura no estilo do RDKit usado nas outras telas: comprimento de ligação fixo, duplas de anel por dentro,
   ligação dividida na cor de cada átomo, rótulos com H do lado livre (OH, HO, NH₂) e carga em sobrescrito.
   mod 'f' = ficha (tamanho natural); sem mod = miniatura (largura vem do CSS). */
function bdSvg(e,mod){
  if(!e)return'';const at=e[0],bd=e[1],n=at.length;
  const ln0=bd.map(b=>Math.hypot(at[b[0]][1]-at[b[1]][1],at[b[0]][2]-at[b[1]][2])).sort((p,q)=>p-q),u=ln0.length?ln0[ln0.length>>1]:15,BL=30,k=BL/(u||15);
  const px=at.map(a=>a[1]*k),py=at.map(a=>a[2]*k);
  const COR={O:'var(--lost,#e0533d)',N:'var(--blue,#4a6cf0)',S:'#c99a12',P:'#e8923a',F:'#3daa5c',Cl:'#3daa5c',Br:'#b5651d',I:'#8e5bb5'};
  const lab=at.map(a=>a[0]!==0),cor=at.map(a=>a[0]?(COR[a[0]]||'currentColor'):'currentColor');
  const nb=at.map(()=>[]);bd.forEach(b=>{nb[b[0]].push(b[1]);nb[b[1]].push(b[0]);});
  const fs=Math.round(BL*0.48*10)/10,sw=2.1,cut=fs*0.62;
  /* menor anel que contém a ligação (até 8 átomos); devolve o centro dele */
  const anel=(i,j)=>{const prev=new Map([[i,-1]]);let fr=[i],d=0;
    while(fr.length&&d<7){const nx=[];for(const a of fr)for(const c of nb[a]){if(a===i&&c===j)continue;if(prev.has(c))continue;prev.set(c,a);if(c===j){const P=[];let t=j;while(t!==-1){P.push(t);t=prev.get(t);}return[P.reduce((s,t)=>s+px[t],0)/P.length,P.reduce((s,t)=>s+py[t],0)/P.length];}nx.push(c);}fr=nx;d++;}
    return null;};
  const f1=v=>v.toFixed(1);
  const seg=(x1,y1,x2,y2,c1,c2)=>{const L=l=>'<line x1="'+f1(l[0])+'" y1="'+f1(l[1])+'" x2="'+f1(l[2])+'" y2="'+f1(l[3])+'" stroke="';
    if(c1===c2)return L([x1,y1,x2,y2])+c1+'"/>';const mx=(x1+x2)/2,my=(y1+y2)/2;return L([x1,y1,mx,my])+c1+'"/>'+L([mx,my,x2,y2])+c2+'"/>';};
  let g='';
  bd.forEach(b=>{const i=b[0],j=b[1],o=b[2];let ax=px[i],ay=py[i],bx=px[j],by=py[j];const dx=bx-ax,dy=by-ay,L=Math.hypot(dx,dy)||1,ux=dx/L,uy=dy/L,nx=-uy,ny=ux;
    const ci=cor[i],cj=cor[j],A=lab[i]?cut:0,B=lab[j]?cut:0;
    const par=(off,sh)=>{const s1=Math.max(A,sh),s2=Math.max(B,sh);return seg(ax+ux*s1+nx*off,ay+uy*s1+ny*off,bx-ux*s2+nx*off,by-uy*s2+ny*off,ci,cj);};
    if(o===1)g+=par(0,0);
    else if(o===3)g+=par(0,0)+par(BL*0.16,0)+par(-BL*0.16,0);
    else if(o===2){
      const r=anel(i,j);
      if(r){const side=((r[0]-ax)*nx+(r[1]-ay)*ny)>=0?1:-1;g+=par(0,0)+par(side*BL*0.17,BL*0.14);}
      else if(nb[i].length<2||nb[j].length<2)g+=par(BL*0.09,0)+par(-BL*0.09,0);
      else{let sd=0;nb[i].concat(nb[j]).forEach(c=>{if(c===i||c===j)return;sd+=(px[c]-ax)*nx+(py[c]-ay)*ny;});const side=sd>=0?1:-1;g+=par(0,0)+par(side*BL*0.17,BL*0.14);}
    }else g+=par(0,0);});
  let t='';
  at.forEach((a,i)=>{if(!lab[i]&&!a[4])return;const sym=a[0]||'C',c=cor[i],h=a[3]||0,q=a[4]||0;
    let sdx=0;nb[i].forEach(j=>{sdx+=px[j]-px[i];});const left=sdx>BL*0.2;
    const X=px[i],Y=py[i]+fs*0.36,w=fs*0.62*sym.length;
    t+='<text x="'+f1(X)+'" y="'+f1(Y)+'" text-anchor="middle" fill="'+c+'">'+sym+'</text>';
    let cx=X+w/2+1;
    if(q){const qt=(Math.abs(q)>1?Math.abs(q):'')+(q>0?'+':'−');t+='<text x="'+f1(cx)+'" y="'+f1(Y-fs*0.42)+'" font-size="'+f1(fs*0.66)+'" fill="'+c+'">'+qt+'</text>';cx+=fs*0.42*qt.length+1;}
    if(h>0){const sub=h>1?'<tspan dy="'+f1(fs*0.28)+'" font-size="'+f1(fs*0.68)+'">'+h+'</tspan>':'';
      if(left)t+='<text x="'+f1(X-w/2-1)+'" y="'+f1(Y)+'" text-anchor="end" fill="'+c+'">H'+sub+'</text>';
      else t+='<text x="'+f1(cx)+'" y="'+f1(Y)+'" fill="'+c+'">H'+sub+'</text>';}});
  let x0=1e9,x1=-1e9,y0=1e9,y1=-1e9;at.forEach((a,i)=>{const m=lab[i]?fs*1.6:2;x0=Math.min(x0,px[i]-m);x1=Math.max(x1,px[i]+m);y0=Math.min(y0,py[i]-m);y1=Math.max(y1,py[i]+m);});
  const P=mod==='f'?18:10;let W=x1-x0+2*P,H=y1-y0+2*P;if(mod==='f'){W=Math.max(W,170);H=Math.max(H,110);}
  const ox=(W-(x1-x0))/2-x0,oy=(H-(y1-y0))/2-y0;
  return '<svg viewBox="0 0 '+f1(W)+' '+f1(H)+'" role="img" aria-label="Estrutura" class="bdsv"'+(mod==='f'?' style="width:'+Math.round(W)+'px"':'')+'><g transform="translate('+f1(ox)+' '+f1(oy)+')"><g stroke-width="'+sw+'" stroke-linecap="round" stroke-linejoin="round" fill="none">'+g+'</g><g font-size="'+f1(fs)+'" font-family="inherit">'+t+'</g></g></svg>';
}
/* ficha de um composto do banco (mesma tela p-cf dos outros) */
function bdFicha(ix){
  const c=bdAll().find(x=>x.i===1000+ix);if(!c)return;CFI=1000+ix;const r=c.r,hoje=new Date().toLocaleDateString('pt-BR');
  const rowd=(k,v)=>'<div class="cfr"><dt>'+k+'</dt><dd>'+v+'</dd></div>';
  const tx=v=>v&&v!=='-'?esc(v):'sem dado';
  let h='<h2 class="scr">'+esc(c.n)+'</h2>'+''
   +(c.a.length?'<p class="scrsub">Também: '+c.a.map(esc).join(' · ')+'</p>':'')
   +'<figure class="cfs"><div>'+bdSvg(r[16],'f')+'</div><figcaption>'+fmt(c.f)+(c.mw?' · '+String(c.mw).replace('.',',')+' g/mol':'')+'</figcaption></figure>'
   +'<div class="cfq"><div class="cfqi"><span>Estado a 25 °C</span><b>'+(c.est?esc(c.est):'sem dado')+'</b></div>'
   +'<div class="cfqi"><span>Ponto de fusão</span><b>'+tx(r[8])+(r[8]&&r[8]!=='-'?' °C':'')+'</b></div>'
   +'<div class="cfqi"><span>Ponto de ebulição</span><b>'+tx(r[9])+(r[9]&&r[9]!=='-'?' °C':'')+'</b></div></div>'
   +'<dl class="cfd">'
   +rowd('Grupo funcional',esc(c.gf.join(', ')||'sem grupo funcional reconhecido'))
   +(c.ge?rowd('Grupo de solubilidade (estimado)','<span class="gl2">'+SOLNM[c.ge]+'</span> '+esc(gTxt(c.ge))+' <span class="tag sm">estimado</span>'):'')
   +(c.sub.length?rowd('Subestruturas',esc(c.sub.map(k=>{const q=SUBL.find(x=>x[0]===k);return q?q[1].replace(/ \(.*/,''):k;}).join(', '))):'')
   +(c.gdh!=null?rowd('GDH','<b>'+c.gdh+'</b> <span class="mut">(anéis + ligações π)</span>'):'')
   +(c.M?rowd('M nominal','<b>'+c.M+'</b>'):'')
   +(bdEn(c.cas,bdNome(r[3]))?rowd('Nome em inglês','<span class="mono">'+esc(bdEn(c.cas,bdNome(r[3])))+'</span> <button class="btn ghost cpy" type="button" data-copy="'+esc(bdEn(c.cas,bdNome(r[3])))+'">Copiar</button>'):'')
   +rowd(c.casx?'Identificador':'CAS','<span class="mono">'+esc(c.cas||'sem dado')+'</span>'+(c.casx&&c.cas?' <span class="mut">(não é um CAS válido; o CAS deste composto não foi encontrado)</span>':''))
   +(r[13]!==null?rowd('Solubilidade em água',r[13]+' g/100 mL a 25 °C'):'')+(r[14]!==null?rowd('Densidade',r[14]+' g/mL a 20 °C'):'')
   +(r[10]?rowd('Derivados (PF °C)',esc(r[10])):'')+'</dl>';
  const iv=c.iv.map((b,k)=>b.concat([k])).filter(b=>b[4]).sort((a,b)=>Math.max(b[0],b[1])-Math.max(a[0],a[1]));
  h+='<details class="sec" open><summary>Infravermelho: bandas esperadas</summary>'
   +(iv.length?'<div class="tbl"><table class="obt nostk"><thead><tr><th>cm⁻¹</th><th>O que é</th></tr></thead><tbody>'+iv.map(b=>'<tr><td class="n">'+Math.min(b[0],b[1])+'–'+Math.max(b[0],b[1])+'</td><td>'+esc(b[2])+'</td></tr>').join('')+'</tbody></table></div>':'<p class="empty">Sem bandas esperadas para este composto.</p>')
   +'<p class="srcl">Faixas esperadas pelo grupo funcional da estrutura, não o espectro medido deste composto.</p>'
   +(c.ivf.length?'<h3 style="margin:12px 0 4px">O que pode deslocar as bandas</h3><ul class="fatl">'+c.ivf.map(f=>'<li><b>'+esc(f[0])+'.</b> '+esc(f[1])+'</li>').join('')+'</ul>':'')
   +((c.ot.length)?'<h3 style="margin:12px 0 4px">Overtones, combinações e ressonância de Fermi</h3><ul class="fatl">'+c.ot.map(o=>'<li><b>'+esc(o[0])+' ('+esc(o[1])+' cm⁻¹).</b> '+esc(o[2])+' <i>Fonte: '+esc(o[3])+'.</i></li>').join('')+'</ul>':'<p class="sm" style="margin:10px 0 0">Overtones diagnósticos: nenhum esperado para este composto.</p>')+fuSug(c.gf)+'</details>';
  h+='<details class="sec"><summary>Espectrometria de massas</summary>'+(c.M?'<p>M nominal = <b>'+c.M+'</b> ('+(c.M%2?'ímpar: número ímpar de N':'par: zero ou número par de N')+').</p>':'');
  if(c.msi){const cc=Object.assign({},c,{M:Math.max(c.M||0,...c.ms)});
    h+='<div class="nmrwrap">'+msSpec(cc)+'<button class="zbtn" type="button" data-zoom>Ampliar</button></div><p>'+c.msi.map(p=>'<span class="pk">'+p[0]+' <small>'+p[1]+'%</small></span>').join('')+'</p>';}
  else h+='<p class="empty">Sem picos de MS neste banco.</p>';
  if(nCl(c.f))h+='<p class="srcl">Contém Cl: aparece M+2 (isótopo ³⁷Cl). Com 1 Cl, M : M+2 é cerca de 3 : 1.</p>';
  h+='</details>';
  if(c.h1.length||c.c13.length){const fr=x=>String(x).replace('.',',');
    h+='<details class="sec"><summary>RMN de ¹H e ¹³C (estimado)</summary><p class="hint">Número de sinais e faixas de deslocamento saem da estrutura (regras de tabela). Não é espectro medido.</p>'
     +(c.h1.length?'<h4 style="margin:10px 0 4px">¹H: '+c.h1.length+(c.h1.length>1?' sinais':' sinal')+'</h4><div class="tbl"><table class="obt nostk"><thead><tr><th>δ (ppm)</th><th>H</th></tr></thead><tbody>'+c.h1.slice().sort((a,b)=>b.hi-a.hi).map(x=>'<tr><td class="n">'+fr(x.lo)+'–'+fr(x.hi)+(x.m?' (largo)':'')+'</td><td>'+x.h+'</td></tr>').join('')+'</tbody></table></div>':'')
     +(c.c13.length?'<h4 style="margin:10px 0 4px">¹³C: '+c.c13.length+(c.c13.length>1?' sinais':' sinal')+'</h4><div class="tbl"><table class="obt nostk"><thead><tr><th>δ (ppm)</th><th>C</th></tr></thead><tbody>'+c.c13.slice().sort((a,b)=>b.hi-a.hi).map(x=>'<tr><td class="n">'+x.lo+'–'+x.hi+'</td><td>'+x.n+'</td></tr>').join('')+'</tbody></table></div>':'')+'</details>';}
  h+='<details class="sec"><summary>SDBS (espectros reais)</summary><p>O SDBS tem IV, MS, ¹H-RMN e ¹³C-RMN medidos de muitos compostos. Busque pelo nome ou pelo CAS.</p><div class="row" style="margin:0 0 8px"><a class="btn" href="https://sdbs.db.aist.go.jp/" target="_blank" rel="noopener">Abrir o SDBS</a>'
   +'<button class="btn ghost" type="button" data-copy="'+esc(bdEn(c.cas,bdNome(r[3]))||c.n)+'">Copiar nome em inglês</button>'+(c.casx?'':'<button class="btn ghost" type="button" data-copy="'+esc(c.cas)+'">Copiar CAS</button>')+'</div>'
   +'<p class="srcl">Ao usar dados do SDBS, cite: SDBS, National Institute of Advanced Industrial Science and Technology (AIST), https://sdbs.db.aist.go.jp, acessado em '+hoje+'.</p></details>';
  h+='<details class="sec"><summary>De onde vêm os dados</summary><p class="srcl"><span class="tag sv">Conferido: banco Analor</span> Nome, CAS, fórmula, massa molar, PF, PE, picos de MS, solubilidade, densidade e SMILES vêm do arquivo UNIV1_290926.DBF, passado pelo professor. O banco não cita a fonte de cada número, e a solubilidade está em g/100 mL de água a 25 °C (confirmado pelo professor). O desenho, o GDH, o grupo funcional, as bandas de IV, os overtones, o RMN estimado, o M nominal e o estado a 25 °C são calculados aqui a partir da estrutura. <span class="tag sv">Conferido: PubChem, NCI CACTUS e NIST</span> Em 11/2026 comparei os 4663 registros com essas fontes. Fórmula e estrutura bateram em 4525. Corrigi 72 fórmulas com erro de digitação e troquei 60 estruturas que não correspondiam ao nome e ao CAS, e preenchi 6 que faltavam. PF e PE só foram trocados quando o PubChem e o NIST concordaram entre si (20 PF e 15 PE); quando o NIST confirmava o banco, o valor ficou. Cada composto alterado mostra o que mudou e a fonte. Alguns registros ficaram com o aviso "confira nome e CAS", porque o nome, o CAS e a estrutura apontam para compostos diferentes. Identificadores que não são CAS válidos aparecem como "Identificador". <span class="tag sm">Estimado</span> O grupo de solubilidade vem das regras da tabela do professor, com a solubilidade em água do banco (3 g/100 mL ou mais conta como solúvel). Ajustei as regras com os 110 compostos do app, e elas acertam 108; em compostos fora desse grupo o acerto não foi medido. O PubChem também pode errar, principalmente em isômeros.</p></details>';
  $('#cfB').innerHTML=h;
}

/* ---------- Atalhos dentro da ficha: IV, MS, RMN, SDBS ---------- */
(function(){
  const box=document.getElementById('cfB');if(!box)return;
  const CURTO=[['Infravermelho','IV'],['Espectrometria','Massas'],['RMN','RMN'],['SDBS','SDBS'],['De onde','Fontes']];
  function monta(){
    if(box.querySelector('.cfnav'))return;
    const ds=[...box.querySelectorAll('details.sec')].filter(d=>d.parentElement===box||d.parentElement.hasAttribute('data-hlscope')||true);
    const itens=[];ds.forEach(d=>{const s=d.querySelector('summary');if(!s)return;const t=s.textContent;const m=CURTO.find(x=>t.indexOf(x[0])===0);if(m)itens.push([m[1],d]);});
    if(itens.length<2)return;
    const nav=document.createElement('div');nav.className='chipbar cfnav';nav.setAttribute('role','group');nav.setAttribute('aria-label','Ir para uma seção da ficha');
    itens.forEach(([n,d])=>{const b=document.createElement('button');b.type='button';b.className='chip';b.textContent=n;
      b.onclick=()=>{d.open=true;d.scrollIntoView({behavior:'smooth',block:'start'});};nav.appendChild(b);});
    const primeiro=itens[0][1];primeiro.parentNode.insertBefore(nav,primeiro);
  }
  new MutationObserver(monta).observe(box,{childList:true});
})();
