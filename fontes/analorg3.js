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
  '@@PENDENTE@@'
 ]},
 {v:97,r:'86 a 97',d:'04/11/2026',t:[
  'IV: as bandas de 72 compostos foram conferidas na tabela de picos dos prints do SDBS. Corrigi as faixas de álcool, fenol, ácido, amina, amida, anidrido, éster aromático, vinila, furano e haletos.',
  'Massas: os picos de 74 compostos foram conferidos nos prints do SDBS (a leitura é visual, erro de cerca de 3 pontos de intensidade).',
  'RMN de 13C: 31 compostos conferidos na tabela de ppm do SDBS. Corrigi o CH₃ ligado a S (DMSO) e o CH₃ ao lado de nitrila.',
  'Compostos: a estrutura da ficha mostra os carbonos numerados. Cada sinal de 1H diz a qual carbono pertence, e os carbonos do anel dizem orto, meta ou para.',
  'Orgânica Básica: a tabela de grupos funcionais mostra a estrutura de cada grupo, com o grupo em destaque.',
  'Limpeza: apaguei arquivos soltos do app e do GitHub.'
 ]},
 {v:85,d:'04/11/2026',t:[
  'IV: dá para escolher qualquer um dos 106 compostos (com busca). Cada um mostra um espectro simulado, parecido com o do SDBS, e a tabela de bandas numerada. Os 15 compostos que você enviou do SDBS vêm primeiro e têm as bandas-chave conferidas.',
  'Guia do IV: mais de 55 linhas novas (isocianatos, tiocianatos, amidas, alcenos por substituição, epóxidos, grupos com P, Si, S e outros). Cada linha diz a fonte.',
  'Cada composto ganhou mais bandas no IV: C–O por tipo de álcool, deformações de CH₃ e CH₂, haletos, sulfonas, anidridos e outros grupos.',
  'Massas: o exercício 1 a 12 deixou de ficar em destaque. Escolha qualquer composto numa lista só.',
  'Ensaios: as tabelas ficaram legíveis no celular (palavras não são mais cortadas).',
  'Identificar: seções que abrem e fecham, com a contagem do que você marcou, e linhas mais baixas.',
  'Cor: Astronomia voltou. Início: a caixa Hoje saiu (Revisar tem atalho no Início). Avisos para o professor saíram.'
 ]},
 {v:83,d:'04/11/2026',t:[
  'Identificar: as duas telas viraram uma só, com o layout de Ensaios e todos os campos. Mostra as classes que sobram e os compostos mais compatíveis.',
  'Início, Ensaios, Espectros e Mais foram reorganizados, sem cartões repetidos. As ferramentas de massas foram para Espectros.',
  'Início tem a caixa Hoje: revisão, próximo exercício e simulado.',
  'Mais > Ajustes: zoom com os dedos (desligado por padrão) e treinos sem pistas (opcional).',
  'Mais > Revisar: pergunta errada nos quizzes volta em 1, 3 e 7 dias.',
  'O app lembra a tela e o que você digitou quando você sai e volta.',
  'Fontes ficam recolhidas, com a etiqueta visível. Etiquetas: "Conferido: [fonte]" ou "Escrito por Claude, sem fonte conferida".',
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
    if(tags.length){tags.forEach(t=>{sm.appendChild(t.cloneNode(true));t.remove();});sm.insertAdjacentHTML('beforeend','<span class="mut"> ver fonte</span>');}
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
  h+='<p class="srcl" style="margin:0 0 8px">'+(c.irc?srcTag(true,c.irc===1?'Conferido: SDBS':'Conferido em parte: SDBS')+' As bandas-chave foram conferidas no espectro do SDBS que você enviou (medido em '+esc(c.irm)+'). ':srcTag(false,'Escrito por Claude, sem fonte conferida')+' ')
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
