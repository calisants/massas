/* ================= ANALORG v3: ajustes, estado salvo, novidades, revisão de perguntas, fontes recolhidas ================= */

/* ---------- Ajustes: zoom e treinos sem pistas ---------- */
const semDica=()=>LS.get('massas-semdica',false);
function zoomAplicar(on){
  const m=document.querySelector('meta[name="viewport"]');
  if(m)m.setAttribute('content',on?'width=device-width,initial-scale=1':'width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no');
  document.documentElement.classList.toggle('semzoom',!on);
}
['gesturestart','gesturechange'].forEach(ev=>document.addEventListener(ev,e=>{if(!LS.get('massas-zoom',false))e.preventDefault();},{passive:false}));
function stDraw(){
  $('#stZoom').checked=!!LS.get('massas-zoom',false);
  $('#stSem').checked=!!semDica();
}
function stInit(){
  zoomAplicar(!!LS.get('massas-zoom',false));
  $('#stZoom').onchange=e=>{LS.set('massas-zoom',e.target.checked);zoomAplicar(e.target.checked);};
  $('#stSem').onchange=e=>{LS.set('massas-semdica',e.target.checked);if(TR.cur)trDraw();};
  stDraw();
}

/* ---------- Novidades e aviso de atualização ---------- */
const NOVID=[
 {v:0,d:'04/11/2026',t:[
  'Novo composto: ácido 5-formilsalicílico (SDBS 23378), com MS, IV (pasta em Nujol, conferido em parte), ¹³C (8 sinais) e ¹H (4 de 5 sinais, o do ácido saiu cortado no print) medidos. O IV agora também mostra a banda do C=O de aldeído aromático em compostos com mais de uma carbonila. Nos fragmentos de MS, a perda de água seguida de CO (como no ácido salicílico) aparece em texto, sem estrutura desenhada.',
  'MS: a ficha de 70 compostos agora traz "Fragmentos propostos": a estrutura do íon de cada pico, o que ele perdeu e a regra (clivagem α, benzílica, McLafferty, perda de CO). É proposta por regras, com a massa conferida contra o pico do SDBS; não é o mecanismo medido. Os picos que nenhuma regra simples explica ficam listados como sem proposta.',
  'Abas: Início, Compostos, Ensaios e Espectros. Em Espectros ficam IV, Massas e RMN, e o antigo "Mais" foi para o Início. As páginas de cada assunto têm o mesmo layout: título, resumo e uma faixa de seções, como na aba RMN.',
  'RMN: nova aba com os quatro passos num espectro real (acetato de etila, SDBS), régua do deslocamento, laboratório de acoplamento, calculadoras de Hz e ppm, integração e GDH, macetes e dois problemas resolvidos.',
  'Toque num pico, banda ou sinal (IV, massas e RMN) e o trecho da molécula fica colorido. Os espectros simulados ganharam o botão Ampliar, e a estrutura do IV ficou do mesmo tamanho da do RMN e centralizada.',
  'RMN de 13C: 70 compostos conferidos na tabela de ppm do SDBS. O valor medido aparece na ficha. Corrigi faixas de tabela que não incluíam o valor real.',
  'RMN de 1H: 66 compostos mostram o δ medido nos prints do SDBS. Corrigi faixas que não incluíam o valor real (clorofórmio, DMSO, DMF, formiatos, salicilatos, enonas e outras).',
  'Compostos: a ficha não mostra mais os números dos carbonos. Os números ficam só na aba RMN.',
  'Fontes: ficaram discretas, num item "Fonte" recolhido. Saíram o aviso dos exercícios 1 a 12 e as etiquetas repetidas.',
  'Aviso de atualização: passou a mostrar a nota da versão em uso.'
 ]},
 {v:97,r:'86 a 97',d:'04/11/2026',t:[
  'IV: as bandas de 73 compostos foram conferidas na tabela de picos dos prints do SDBS. Corrigi as faixas de álcool, fenol, ácido, amina, amida, anidrido, éster aromático, vinila, furano e haletos.',
  'Massas: os picos de 75 compostos foram conferidos nos prints do SDBS (a leitura é visual, erro de cerca de 3 pontos de intensidade).',
  'RMN de 13C: 31 compostos conferidos na tabela de ppm do SDBS. Corrigi o CH₃ ligado a S (DMSO) e o CH₃ ao lado de nitrila.',
  'Compostos: a estrutura da ficha mostra os carbonos numerados. Cada sinal de 1H diz a qual carbono pertence, e os carbonos do anel dizem orto, meta ou para.',
  'Orgânica Básica: a tabela de grupos funcionais mostra a estrutura de cada grupo, com o grupo em destaque.',
  'Limpeza: apaguei arquivos soltos do app e do GitHub.'
 ]},
 {v:85,d:'04/11/2026',t:[
  'IV: dá para escolher qualquer um dos 109 compostos (com busca). Cada um mostra um espectro simulado, parecido com o do SDBS, e a tabela de bandas numerada. Os 15 primeiros compostos e têm as bandas-chave conferidas.',
  'Guia do IV: mais de 55 linhas novas (isocianatos, tiocianatos, amidas, alcenos por substituição, epóxidos, grupos com P, Si, S e outros). Cada linha diz a fonte.',
  'Cada composto ganhou mais bandas no IV: C–O por tipo de álcool, deformações de CH₃ e CH₂, haletos, sulfonas, anidridos e outros grupos.',
    'Ensaios: as tabelas ficaram legíveis no celular (palavras não são mais cortadas).',
  'Identificar: seções que abrem e fecham, com a contagem do que você marcou, e linhas mais baixas.',
  'Cor: Astronomia voltou. Início: a caixa Hoje saiu (Revisar tem atalho no Início). Avisos para o professor saíram.'
 ]},
 {v:83,d:'04/11/2026',t:[
  'Identificar: as duas telas viraram uma só, com o layout de Ensaios e todos os campos. Mostra as classes que sobram e os compostos mais compatíveis.',
    'Início > Ajustes: zoom com os dedos (desligado por padrão) e treinos sem pistas (opcional).',
  'Início > Revisar: pergunta errada nos quizzes volta em 1, 3 e 7 dias.',
  'O app lembra a tela e o que você digitou quando você sai e volta.',
  'Fontes ficam recolhidas, com a etiqueta visível. Cada bloco diz de onde vem o dado.',
  'Cores: ficaram 5 (Azul, Grafite, Roxo, Química e Orgânica).',
  'RMN: espectros de 1H e 13C simulados para cada composto, com sinais numerados e integração opcional. Não são os medidos (esses estão no SDBS).',
  'IV: o botão Treinar voltou (estava sem acesso).'
 ]}
];
const VNUM=parseInt(String(VERSAO).replace(/^v/,''),10)||0;
function nvDraw(){
  LS.set('massas-visto',VNUM);nvBanner();
  $('#nvList').innerHTML=NOVID.map(n=>'<div class="rule"><h3>v'+(n.r||(n.v||VNUM))+' <span class="mut" style="font-weight:400">· '+esc(n.d)+'</span></h3><ul class="nvl">'+n.t.map(x=>'<li>'+esc(x)+'</li>').join('')+'</ul></div>').join('');
}
function nvBanner(){
  let b=$('#nvBanner');
  const visto=LS.get('massas-visto',null);
  const mostrar=visto!==null&&visto<VNUM;
  if(!mostrar){if(b)b.hidden=true;return;}
  if(!b){b=document.createElement('div');b.id='nvBanner';b.className='nvb';b.setAttribute('role','status');
    b.innerHTML='<span>O Analorg foi atualizado para <b id="nvV"></b>. Leia as novidades.</span><span class="nvbb"><button type="button" class="btn" id="nvLer">Ler</button><button type="button" class="btn ghost" id="nvOk">Já li</button></span>';
    const w=document.querySelector('.wrap');w.insertBefore(b,w.children[1]||null);
    $('#nvLer').onclick=()=>go('p-nv');
    $('#nvOk').onclick=()=>{LS.set('massas-visto',VNUM);b.hidden=true;};}
  $('#nvV').textContent='v'+VNUM;b.hidden=false;
}
function nvInit(){
  if(LS.get('massas-visto',null)===null)LS.set('massas-visto',window.PRIMEIRA===false?0:VNUM);
  nvBanner();
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
    box.innerHTML='<p class="empty">'+(revFeitas()>=REV_MAX&&repqDue()>0?'Você já revisou '+REV_MAX+' hoje. O resto fica para amanhã, para não pesar.':'Nenhuma pergunta vencida hoje.')+' Há '+total+' guardada'+(total===1?'':'s')+'.</p>';
    return;
  }
  RVMODE=true;
  miniQuiz('#rvBox',due.map(k=>r[k].q),'Revisão');
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
    if(d.tela&&d.tela!=='p-in'&&SCR.indexOf(d.tela)>=0){
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
  return '<svg class="nmrspec" viewBox="0 0 '+W+' '+(base+34)+'" role="img" aria-label="Espectro de '+(isH?'1H':'13C')+' simulado">'
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
  return '<svg class="nmrspec irspec" viewBox="0 0 '+W+' '+(base+34)+'" role="img" aria-label="Espectro de IV simulado de '+esc(c.n)+'">'
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
  const c={1:(icSt.est?1:0)+(icSt.cor?1:0),2:icSt.g?1:0,3:v('icPF')+v('icPE'),4:n,5:ir,6:['icF','icGDH','icGF','icM','icP','icH','icC','icHd'].reduce((a,k)=>a+v(k),0)};
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
  /* ---- troca de painel ---- */
  function rp(k){
    document.querySelectorAll('[data-rpane]').forEach(d=>d.hidden=d.dataset.rpane!==k);
    document.querySelectorAll('.rseg [data-rp]').forEach(b=>b.setAttribute('aria-pressed',b.dataset.rp===k?'true':'false'));
    if(k==='mac')macDraw();
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
