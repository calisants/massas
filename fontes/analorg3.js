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
  $('#nvList').innerHTML=NOVID.map(n=>'<div class="rule"><h3>v'+n.v+' <span class="mut" style="font-weight:400">· '+esc(n.d)+'</span></h3><ul class="nvl">'+n.t.map(x=>'<li>'+esc(x)+'</li>').join('')+'</ul></div>').join('');
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
    lb+='<circle class="lc" cx="'+x.toFixed(1)+'" cy="'+y.toFixed(1)+'" r="7"/><text class="ln" x="'+x.toFixed(1)+'" y="'+(y+3.5).toFixed(1)+'" text-anchor="middle">'+(o.idx+1)+'</text>';});
  return '<svg class="nmrspec" viewBox="0 0 '+W+' '+(base+34)+'" role="img" aria-label="Espectro de '+(isH?'1H':'13C')+' simulado">'
    +(isH?'<path class="int" d="'+ip+'"/>':'')+'<path class="sp" d="'+p+'"/><line class="ax" x1="'+L+'" y1="'+base+'" x2="'+(W-R)+'" y2="'+base+'"/>'+tk+lb
    +'<text class="tl" x="'+(W/2)+'" y="'+(base+30)+'" text-anchor="middle">δ (ppm)'+(isH?'':' · ¹³C com desacoplamento de ¹H')+'</text></svg>';
}
document.addEventListener('click',ev=>{const b=ev.target.closest('[data-nmrint]');if(!b)return;
  const w=b.closest('.nmrwrap'),s=w&&w.querySelector('svg'),on=s&&s.classList.toggle('showint');
  b.setAttribute('aria-pressed',on?'true':'false');b.textContent=on?'Esconder a integração':'Mostrar a integração';});
