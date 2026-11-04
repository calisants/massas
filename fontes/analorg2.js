/* ================= ANALORG v2: COMPOSTOS, IDENTIFICAÇÃO, RMN, ORGÂNICA BÁSICA ================= */
const SOLNM={S2:'S₂',SA:'SA',SB:'SB',S1:'S₁',A1:'A₁',A2:'A₂',B:'B',MN:'MN',N:'N',I:'I'};
const GORD=['S2','SA','SB','S1','A1','A2','B','MN','N','I'];
const norm2=s=>String(s||'').toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g,'').replace(/[-\s,().]/g,'');
const tC=v=>v==null?'—':(String(v).replace('.',',')+' °C');
const gTxt=k=>{const g=(typeof SOLG!=='undefined'?SOLG:[]).find(x=>x.k===k);return g?g.t:'';};
const ivr=b=>[Math.min(b[0],b[1]),Math.max(b[0],b[1])];
const nCl=f=>{const m=String(f).match(/Cl(\d*)/);return m?(m[1]?+m[1]:1):0;};
const pfTag=s=>s==='c'?' <span class="tag sv">conferido</span>':s==='d'?' <span class="tag sm">fontes divergem</span>':'';
function srcTag(ok,txt){return '<span class="tag '+(ok?'sv':'sm')+'">'+esc(txt)+'</span>';}
function copyTxt(t,btn){
  const done=()=>{if(btn){const o=btn.textContent;btn.textContent='Copiado';setTimeout(()=>btn.textContent=o,1200);}};
  try{navigator.clipboard.writeText(t).then(done,done);}catch(e){done();}
}

/* ---------- lista de compostos ---------- */
function cpInit(){
  const g=$('#cpG'),g2=$('#icG'),sel=$('#rmSel'),ex=$('#icEx');
  GORD.forEach(k=>{[g,g2].forEach(s=>{const o=document.createElement('option');o.value=k;o.textContent=SOLNM[k];s.appendChild(o);});});
  const byName=[...COMP].sort((a,b)=>a.n.localeCompare(b.n,'pt'));
  byName.forEach(c=>{[sel,ex].forEach(s=>{const o=document.createElement('option');o.value=c.i;o.textContent=c.n;s.appendChild(o);});});
  $('#cpQ').addEventListener('input',cpDraw);['#cpE','#cpG'].forEach(id=>$(id).addEventListener('change',cpDraw));
  sel.onchange=rmDraw;
  cpDraw();rmDraw();
}
function cpDraw(){
  const q=norm2($('#cpQ').value),e=$('#cpE').value,g=$('#cpG').value;
  const l=COMP.filter(c=>(!q||[c.n,...c.a,c.f,c.cas].some(x=>norm2(x).includes(q)))&&(!e||c.est.indexOf(e)===0)&&(!g||c.g===g)).sort((a,b)=>a.n.localeCompare(b.n,'pt'));
  $('#cpN').textContent=l.length+' de '+COMP.length+' compostos';
  $('#cpL').innerHTML=l.length?l.map(c=>'<button class="cpc" type="button" data-cf="'+c.i+'"><span class="thumb">'+c.s+'</span><span><b>'+esc(c.n)+'</b><span class="m">'+fmt(c.f)+' · '+SOLNM[c.g]+'</span><span class="m">'+esc(c.est)+(c.pf!=null?' · PF '+tC(c.pf):'')+(c.pe!=null?' · PE '+tC(c.pe):'')+'</span></span></button>').join(''):'<p class="empty">Nenhum composto com esse filtro.</p>';
}
document.addEventListener('click',ev=>{const b=ev.target.closest('[data-cf]');if(b){cfDraw(+b.dataset.cf);go('p-cf');}
  const cp=ev.target.closest('[data-copy]');if(cp)copyTxt(cp.dataset.copy,cp);});

/* ---------- RMN estimado ---------- */
function nmrSketch(c){
  const W=340,pad=14,rowH=15,rows=c.h1.length,H=rows*rowH+28,x=d=>pad+(12-d)/12*(W-2*pad);
  let s='<svg class="nmrsk" viewBox="0 0 '+W+' '+H+'" role="img" aria-label="Esboço das faixas de deslocamento de 1H">';
  c.h1.forEach((h,i)=>{const y=6+i*rowH,x1=x(Math.min(h.hi,12)),x2=x(Math.max(h.lo,0));
    s+='<rect class="bx" x="'+x1.toFixed(1)+'" y="'+y+'" width="'+Math.max(x2-x1,6).toFixed(1)+'" height="11" rx="4"/><text x="'+(Math.max(x2,x1+6)+4).toFixed(1)+'" y="'+(y+9)+'">'+h.h+'H '+esc(h.m)+'</text>';});
  const ay=rows*rowH+8;s+='<line class="ax" x1="'+pad+'" y1="'+ay+'" x2="'+(W-pad)+'" y2="'+ay+'"/>';
  for(let d=0;d<=12;d+=2)s+='<text x="'+(x(d)-(d>=10?6:3)).toFixed(1)+'" y="'+(ay+13)+'">'+d+'</text>';
  return s+'</svg>';
}
function nmrBlock(c){
  let h='<p class="srcl" style="margin:0 0 6px"><b>Estimativa por faixas típicas, não é o espectro real.</b> O número de sinais, a integração e a multiplicidade (regra n+1) saem da estrutura. O deslocamento é a faixa de tabela para aquele tipo de H.</p>';
  h+='<h4 style="margin:10px 0 4px">¹H: '+c.h1.length+(c.h1.length>1?' sinais':' sinal')+' ('+c.h1.reduce((a,x)=>a+x.h,0)+' H no total)</h4>'+nmrSketch(c);
  h+='<div class="tbl"><table class="obt"><thead><tr><th>Tipo de H</th><th>Nº de H</th><th>Multiplicidade</th><th>δ típico (ppm)</th></tr></thead><tbody>'+c.h1.map(x=>'<tr><td>'+esc(x.t)+'</td><td>'+x.h+'</td><td>'+esc(x.m)+'</td><td>'+String(x.lo).replace('.',',')+'–'+String(x.hi).replace('.',',')+'</td></tr>').join('')+'</tbody></table></div>';
  h+='<h4 style="margin:12px 0 4px">¹³C: '+c.c13.length+(c.c13.length>1?' sinais':' sinal')+' (de '+c.c13.reduce((a,x)=>a+x.n,0)+' C)</h4>';
  h+='<div class="tbl"><table class="obt"><thead><tr><th>Tipo de C</th><th>C equivalentes</th><th>δ típico (ppm)</th></tr></thead><tbody>'+c.c13.map(x=>'<tr><td>'+esc(x.t)+'</td><td>'+x.n+'</td><td>'+x.lo+'–'+x.hi+'</td></tr>').join('')+'</tbody></table></div>';
  return h;
}
function rmDraw(){const c=COMP[+$('#rmSel').value||COMP.findIndex(x=>x.n===$('#rmSel').options[0].textContent)];if(!c)return;
  $('#rmOut').innerHTML='<div class="cfh" style="margin-top:10px"><figure class="st"><div>'+c.s+'</div><figcaption>'+fmt(c.f)+'</figcaption></figure><div>'+nmrBlock(c)+'</div></div>';}

/* ---------- ficha do composto ---------- */
function openMS(n){const e=EX.find(x=>x.n===n);if(!e)return;curEx=n;pkSel=null;$('#inM').value=e.M;$('#inP').value=e.peaks.filter(p=>p!==e.M).join(', ');buildChips();analyze();anStage(true);go('p-an');$('#an-in').hidden=true;$('#an-res').hidden=false;}
function cfDraw(i){
  const c=COMP[i],hoje=new Date().toLocaleDateString('pt-BR');
  const sd=c.sdbs||(c.ex&&typeof INTS!=='undefined'&&INTS[c.ex]?INTS[c.ex].sdbs:null);
  let h='<h2 class="scr">'+esc(c.n)+'</h2>'+(c.a.length?'<p class="scrsub">Também: '+c.a.map(esc).join(', ')+'</p>':'');
  h+='<div class="cfh"><figure class="st"><div>'+c.s+'</div><figcaption>'+fmt(c.f)+'</figcaption></figure><table class="cft"><tbody>'
   +'<tr><th>Fórmula molecular</th><td>'+fmt(c.f)+'</td></tr>'
   +'<tr><th>Massa molar</th><td>'+String(c.mw).replace('.',',')+' g/mol</td></tr>'
   +'<tr><th>M do íon molecular (MS)</th><td>'+c.M+'</td></tr>'
   +'<tr><th>GDH</th><td>'+c.gdh+'</td></tr>'
   +'<tr><th>Grupo funcional</th><td>'+esc(c.gf.join(', ')||'hidrocarboneto sem grupo funcional')+'</td></tr>'
   +'<tr><th>Estado (25 °C)</th><td>'+esc(c.est)+'</td></tr><tr><th>Cor</th><td>'+esc(c.cor)+'</td></tr>'
   +'<tr><th>Ponto de fusão</th><td>'+tC(c.pf)+pfTag(c.pfs)+'</td></tr><tr><th>Ponto de ebulição</th><td>'+tC(c.pe)+pfTag(c.pes)+'</td></tr>'
   +'<tr><th>Grupo de solubilidade</th><td><span class="gl2">'+SOLNM[c.g]+'</span>'+esc(gTxt(c.g))+'</td></tr>'
   +'<tr><th>CAS</th><td class="mono">'+esc(c.cas)+'</td></tr>'
   +(c.obs?'<tr><th>Observação</th><td>'+esc(c.obs)+'</td></tr>':'')+'</tbody></table></div>';
  {const pubs=c.pubsrc&&c.pubsrc.length;
   h+='<p class="srcl"><b>Fonte:</b> '+(pubs?'PF e PE marcados "conferido" vêm do PubChem (mediana dos valores de '+c.pubsrc.map(esc).join(', ')+'), acessado em 04/11/2026'+(c.cid?' (CID '+c.cid+')':'')+'. ':'')
   +((c.pfs==='d'||c.pes==='d')?'Onde aparece "fontes divergem", o PubChem traz valores diferentes entre si e eu mantive o valor que já estava no app. ':'')
   +'Estado, cor, grupo de solubilidade e CAS foram escritos por mim, <b>sem fonte conferida</b> nesta sessão'+(pubs?'':', assim como PF e PE')+' (confirme no SDBS ou na Plataforma do professor antes de usar em relatório). Fórmula, massa, GDH e estrutura são calculados a partir da estrutura (RDKit).</p>';}
  // IV
  const iv=c.iv.slice().sort((a,b)=>ivr(b)[1]-ivr(a)[1]);
  h+='<details class="sec" open><summary>Infravermelho: bandas esperadas</summary>'
   +(iv.length?'<div class="tbl"><table class="obt"><thead><tr><th>cm⁻¹</th><th>Atribuição</th><th>Intensidade</th><th>Fonte</th></tr></thead><tbody>'+iv.map(b=>'<tr><td class="mono">'+ivr(b)[0]+'–'+ivr(b)[1]+'</td><td>'+esc(b[2])+(b[4]?' <span class="tag sv">chave</span>':'')+'</td><td>'+esc(b[3])+'</td><td>'+(b[5]==='a'?'Apostila de IV':b[5]==='s'?'fontes citadas em "O que pode deslocar" e prints do SDBS':'tabela geral, sem fonte conferida')+'</td></tr>').join('')+'</tbody></table></div>':'<p class="empty">Sem bandas cadastradas.</p>')
   +'<p class="srcl" style="margin-top:6px">As faixas vêm do grupo funcional e dos fatores abaixo (não é o espectro medido). Bandas "chave" são as que decidem a identificação.</p>'
   +(c.irc?'<p class="srcl">'+srcTag(true,c.irc===1?'conferido no SDBS':'conferido em parte no SDBS')+' '+(c.irc===1?'As bandas-chave do espectro de IV do SDBS No. '+c.sdbs+' ('+esc(c.irm)+') caem nas faixas acima.':'Do IV do SDBS No. '+c.sdbs+' ('+esc(c.irm)+') só conferi o O–H largo e o C–O.')+' Lido dos prints enviados, acessado em 04/11/2026. O meio importa: ligação de H e solvente mudam a posição das bandas.</p>':'')
   +((c.ivf&&c.ivf.length)?'<h3 style="margin:12px 0 4px">O que pode deslocar as bandas deste composto</h3><ul class="fatl">'+c.ivf.map(f=>'<li><b>'+esc(f[0])+'.</b> '+esc(f[1])+'</li>').join('')+'</ul>':'')
   +'</details>';
  // MS
  h+='<details class="sec"><summary>Espectrometria de massas</summary><p>M = <b>'+c.M+'</b> ('+(c.M%2?'ímpar: número ímpar de N':'par: zero ou número par de N')+').</p>';
  if(c.ms){const tp=c.msi?c.msi.map(p=>'<span class="pk'+(p[0]===c.M?' base':'')+'">'+p[0]+' <small>'+p[1]+'%</small></span>').join(''):c.ms.map(p=>'<span class="pk'+(p===c.M?' base':'')+'">'+p+'</span>').join('');
    h+='<p>'+tp+'</p><p class="srcl">'+srcTag(c.msv>0,c.msv===2?'conferido no SDBS':(c.msv?'conferido (lousa e SDBS)':'sem fonte conferida'))+' '+(c.msv===2?'Picos do espectro SDBS No. '+c.sdbs+' ('+esc(c.msid)+'), lidos do gráfico em 04/11/2026; a intensidade relativa tem erro de uns 3 pontos.':c.msv?'Picos do exercício do app, com mecanismo.':'Picos típicos de EI 70 eV escritos por mim; confirme no SDBS.')+'</p>';}
  else h+='<p class="empty">Sem picos cadastrados.</p>';
  if(nCl(c.f))h+='<p class="srcl">Contém Cl: aparece M+2 (isótopo ³⁷Cl). Com 1 Cl, M : M+2 é cerca de 3 : 1.</p>';
  if(c.ex)h+='<button class="btn" type="button" data-ms="'+c.ex+'">Ver os mecanismos de fragmentação</button>';
  h+='</details>';
  // RMN
  h+='<details class="sec"><summary>RMN de ¹H e ¹³C</summary>'+nmrBlock(c)+'</details>';
  // SDBS
  h+='<details class="sec" open><summary>SDBS (espectros reais)</summary><p>O SDBS tem IV, MS, ¹H-RMN e ¹³C-RMN medidos deste composto. Busque pelo nome ou pelo CAS.</p><div class="row" style="margin:0 0 8px">'
   +'<a class="btn" href="'+(sd?'https://sdbs.db.aist.go.jp/sdbs/cgi-bin/landingpage?sdbsno='+sd:'https://sdbs.db.aist.go.jp/')+'" target="_blank" rel="noopener">Abrir o SDBS</a>'
   +'<button class="btn ghost" type="button" data-copy="'+esc(c.n)+'">Copiar nome</button><button class="btn ghost" type="button" data-copy="'+esc(c.cas)+'">Copiar CAS</button></div>'
   +(sd?'<p class="srcl">Nº SDBS: <b>'+sd+'</b>. Se o link abrir a página inicial, aceite o aviso e busque por esse número.</p>':'<p class="srcl">Nº SDBS não cadastrado aqui. Use o nome ou o CAS na busca.</p>')
   +'<p class="srcl">Ao usar dados do SDBS, cite: SDBS, National Institute of Advanced Industrial Science and Technology (AIST), https://sdbs.db.aist.go.jp, acessado em '+hoje+'. O SDBS não permite coleta automática nem download em massa; por isso o app só liga para ele.</p></details>';
  h+='<div class="row"><button class="btn ghost" type="button" data-icfill="'+c.i+'">Usar na Identificação do Composto</button></div>';
  $('#cfB').innerHTML=h;
}
document.addEventListener('click',ev=>{const b=ev.target.closest('[data-ms]');if(b)openMS(+b.dataset.ms);
  const f=ev.target.closest('[data-icfill]');if(f){icFill(+f.dataset.icfill);go('p-ic');}});

/* ---------- Identificação do Composto ---------- */
const nums=s=>(String(s||'').replace(/,(?=\d)(?![^,]*\d{3}\b)/g,'.').match(/\d+(?:[.,]\d+)?/g)||[]).map(x=>parseFloat(x.replace(',','.')));
const numsInt=s=>(String(s||'').match(/\d+/g)||[]).map(Number);
const ELS=[['O','Oxigênio (O)'],['H','Hidrogênio (H)'],['N','Nitrogênio (N)'],['S','Enxofre (S)'],['Cl','Cloro (Cl)'],['Br','Bromo (Br)'],['I','Iodo (I)']];
const elCount=f=>{const m={};String(f).replace(/([A-Z][a-z]?)(\d*)/g,(a,e,n)=>{m[e]=(m[e]||0)+(n?+n:1);return '';});return m;};
const corFam=s=>{s=String(s||'').toLowerCase();const k=s.indexOf('('),main=k<0?s:s.slice(0,k),par=k<0?'':s.slice(k);
  const f=t=>{const r=new Set();if(/incolor|branc/.test(t))r.add('inc');if(/amarel/.test(t))r.add('amarelo');if(/laranj/.test(t))r.add('laranja');if(/verm|ros/.test(t))r.add('vermelho');if(/marrom|castanh/.test(t))r.add('marrom');if(/verde/.test(t))r.add('verde');if(/azul/.test(t))r.add('azul');if(/viole|roxo|purpur/.test(t))r.add('violeta');return r;};
  return [f(main),f(par)];};
function icInputs(){
  const v=id=>$(id).value.trim();
  const num=id=>{const x=parseFloat(v(id));return isFinite(x)?x:null;};
  return {est:v('#icEst'),cor:v('#icCor'),g:v('#icG'),F:v('#icF').replace(/\s+/g,''),gdh:num('#icGDH'),gf:v('#icGF'),els:ELS.map(e=>[e[0],v('#icE'+e[0])]).filter(e=>e[1]),pf:num('#icPF'),pe:num('#icPE'),tol:+v('#icTol')||5,
    iv:numsInt(v('#icIV')),M:num('#icM'),pk:numsInt(v('#icP')),h:num('#icH'),c:num('#icC'),hd:nums(v('#icHd'))};
}
const gauss=(d,t)=>Math.max(0.02,Math.exp(-0.5*Math.pow(d/t,2)));
function icScore(c,x){
  const parts=[];let w=1;
  const add=(k,lab,f,det)=>{parts.push({k,lab,f,det:det||''});w*=f;};
  if(x.est)add('est','estado',c.est.indexOf(x.est)===0?1:0.05,c.est);
  if(x.cor){const [m,p]=corFam(c.cor);add('cor','cor',m.has(x.cor)?1:p.has(x.cor)?0.5:0.12,c.cor);}
  if(x.g)add('g','solubilidade',c.g===x.g?1:0.04,'grupo '+SOLNM[c.g]);
  if(x.pf!=null)add('pf','PF',c.pf==null?0.05:gauss(c.pf-x.pf,x.tol),'PF '+tC(c.pf));
  if(x.pe!=null)add('pe','PE',c.pe==null?0.08:gauss(c.pe-x.pe,x.tol),'PE '+tC(c.pe));
  if(x.els.length){c._el=c._el||elCount(c.f);}
  x.els.forEach(([e,v])=>{const has=!!(c._el&&c._el[e]);add('el','elemento '+e,(v==='s')===has?1:0.03,has?'tem '+e:'sem '+e);});
  if(x.F){const a=elCount(x.F),b=c._el||(c._el=elCount(c.f));const ks=new Set([...Object.keys(a),...Object.keys(b)]);const ok=[...ks].every(k=>(a[k]||0)===(b[k]||0));add('F','fórmula',ok?1:0.02,c.f);}
  if(x.gdh!=null)add('gdh','GDH',c.gdh===x.gdh?1:0.05,'GDH '+c.gdh);
  if(x.gf)add('gf','grupo funcional',c.gf.indexOf(x.gf)>=0?1:0.04,c.gf.join(', ')||'sem grupo funcional');
  if(x.iv.length){
    const keys=c.iv.filter(b=>b[4]),all=c.iv;
    const hit=b=>{const r=ivr(b);return x.iv.some(v=>v>=r[0]-20&&v<=r[1]+20);};
    const rec=keys.length?keys.filter(hit).length/keys.length:1;
    const func=x.iv.filter(v=>v>1500),un=func.filter(v=>!all.some(b=>{const r=ivr(b);return v>=r[0]-20&&v<=r[1]+20;}));
    const prec=func.length?1-un.length/func.length:1;
    const miss=keys.filter(b=>!hit(b)).map(b=>b[2].split(' (')[0]+' ('+ivr(b)[0]+'–'+ivr(b)[1]+')');
    add('iv','IV',(0.12+0.88*rec)*(0.03+0.97*prec*prec),(un.length?'sem explicação: '+un.join(', ')+'. ':'')+(miss.length?'faltou: '+miss.join('; '):'bandas-chave presentes'));
  }
  if(x.M!=null){const d=Math.abs(c.M-x.M);add('M','M',d===0?1:(d===1?0.1:0.02),'M = '+c.M);}
  if(x.pk.length){
    if(c.ms){const ref=c.ms.filter(p=>p!==c.M),ok=p=>ref.some(r=>Math.abs(r-p)<=0.5);
      const rec=ref.length?ref.filter(r=>x.pk.some(p=>Math.abs(r-p)<=0.5)).length/ref.length:1,prec=x.pk.filter(ok).length/x.pk.length;
      add('ms','picos de MS',0.05+0.95*(0.5*rec+0.5*prec),'picos do banco: '+ref.join(', '));}
    else add('ms','picos de MS',0.4,'sem picos cadastrados (neutro)');
  }
  if(x.h!=null){const n=c.h1.length,ne=c.h1.filter(s=>/largo/.test(s.m)).length;const d=Math.min(Math.abs(n-x.h),Math.abs(n-ne-x.h));add('h','nº de sinais de ¹H',Math.pow(0.25,d),n+' sinais');}
  if(x.c!=null){const d=Math.abs(c.c13.length-x.c);add('c','nº de sinais de ¹³C',Math.pow(0.25,d),c.c13.length+' sinais');}
  if(x.hd.length){const ok=x.hd.filter(d=>c.h1.some(s=>d>=s.lo-0.3&&d<=s.hi+0.3)).length/x.hd.length;add('hd','δ de ¹H',0.1+0.9*ok,Math.round(ok*100)+'% dos δ dentro das faixas');}
  return {w,parts};
}
function icRun(){
  const x=icInputs();
  const res=COMP.map(c=>({c,...icScore(c,x)}));
  const used=res[0].parts.length;
  if(!used){$('#icOut').innerHTML='<p class="empty">Preencha pelo menos um dado.</p>';return;}
  const tot=res.reduce((a,r)=>a+r.w,0)||1;res.forEach(r=>r.p=r.w/tot*100);
  res.sort((a,b)=>b.w-a.w);
  const top=res.slice(0,5).filter((r,i)=>i<3||r.p>=1);
  let h='';
  if(used<3)h+='<div class="icwarn">Só '+used+' critério'+(used>1?'s':'')+' preenchido'+(used>1?'s':'')+': vários compostos ficam parecidos. Acrescente IV, PE ou RMN para separar.</div>';
  if(res[0].w<0.05)h+='<div class="icwarn">Nenhum composto do banco combina bem com todos os dados (encaixe absoluto baixo). O seu pode não estar na lista; os de baixo são só os mais parecidos.</div>';
  else if(res.length>1&&res[0].p<2*res[1].p)h+='<div class="icwarn">O primeiro e o segundo estão próximos. Falta um dado que os separe (veja o que difere nas linhas abaixo).</div>';
  h+=top.map(r=>'<div class="icr"><div class="top"><b><button class="back" style="margin:0;font-size:1rem" type="button" data-cf="'+r.c.i+'">'+esc(r.c.n)+'</button> <span class="mono" style="font-weight:400;color:var(--muted)">'+fmt(r.c.f)+'</span></b><span class="pct">'+(r.p>=10?r.p.toFixed(0):r.p.toFixed(1)).replace('.',',')+'%</span></div><div class="bar"><i style="width:'+Math.min(100,r.p).toFixed(1)+'%"></i></div>'
    +'<div class="cr">'+r.parts.map(p=>'<span class="'+(p.f>=0.7?'ok':p.f>=0.2?'md':'no')+'">'+(p.f>=0.7?'✓ ':p.f>=0.2?'~ ':'✗ ')+esc(p.lab)+'</span>').join('')+'</div>'
    +'<p class="det">'+r.parts.filter(p=>p.det&&p.f<0.7).map(p=>'<b>'+esc(p.lab)+':</b> '+esc(p.det)).join(' · ')+'</p></div>').join('');
  h+='<p class="srcl">Base: '+COMP.length+' compostos do app. ✓ combina, ~ combina em parte, ✗ não combina. Valores do banco que estão sem fonte conferida podem estar um pouco diferentes da sua tabela.</p>';
  $('#icOut').innerHTML=h;
}
function icClear(){['#icEst','#icCor','#icG','#icGF','#icEx'].forEach(i=>$(i).value='');ELS.forEach(e=>$('#icE'+e[0]).value='');['#icPF','#icPE','#icIV','#icM','#icP','#icH','#icC','#icHd','#icF','#icGDH'].forEach(i=>$(i).value='');$('#icTol').value='5';$('#icOut').innerHTML='';}
function icFill(i){
  const c=COMP[i];icClear();
  $('#icEst').value=c.est.indexOf('líquido')===0?'líquido':'sólido';$('#icG').value=c.g;
  {const fm=corFam(c.cor)[0];$('#icCor').value=[...fm][0]||'';const ce=elCount(c.f);['O','N','S','Cl','Br','I'].forEach(e=>$('#icE'+e).value=ce[e]?'s':'n');}
  if(c.pf!=null&&c.est.indexOf('sólido')===0)$('#icPF').value=c.pf;
  if(c.pe!=null&&c.est.indexOf('líquido')===0)$('#icPE').value=c.pe;
  $('#icIV').value=c.iv.filter(b=>b[4]).map(b=>Math.round((b[0]+b[1])/2)).join(', ');
  $('#icM').value=c.M;
  if(c.ms)$('#icP').value=c.ms.filter(p=>p!==c.M).slice(0,3).join(', ');
  $('#icH').value=c.h1.length;$('#icC').value=c.c13.length;$('#icEx').value=String(i);
  icRun();
}
function icInit(){
  $('#icEl').innerHTML=ELS.map(e=>'<label>'+e[1]+'<select id="icE'+e[0]+'"><option value="">não sei</option><option value="s">tem</option><option value="n">não tem</option></select></label>').join('');
  [...new Set(COMP.flatMap(c=>c.gf))].sort((a,b)=>a.localeCompare(b,'pt')).forEach(g=>{const o=document.createElement('option');o.value=g;o.textContent=g;$('#icGF').appendChild(o);});
  $('#icGo').onclick=icRun;$('#icClr').onclick=icClear;
  $('#icEx').onchange=()=>{if($('#icEx').value!=='')icFill(+$('#icEx').value);};
  document.querySelectorAll('#p-ic input').forEach(i=>i.addEventListener('keydown',e=>{if(e.key==='Enter')icRun();}));
}

/* ---------- GDH ---------- */
function gdhRun(){
  const f=$('#gdhF').value.trim(),o=$('#gdhOut');if(!f){o.textContent='';return;}
  const m={};let ok=true;const rest=f.replace(/([A-Z][a-z]?)(\d*)/g,(a,e,n)=>{m[e]=(m[e]||0)+(n?+n:1);return '';});
  if(rest.trim()||!m.C){o.textContent='Escreva uma fórmula como C7H6O (com C e H).';return;}
  const x=(m.F||0)+(m.Cl||0)+(m.Br||0)+(m.I||0),g=(2*m.C+2+(m.N||0)+(m.P||0)-(m.H||0)-x)/2;
  o.innerHTML='GDH = (2×'+m.C+' + 2 + '+((m.N||0)+(m.P||0))+' − '+(m.H||0)+' − '+x+') / 2 = <b>'+g+'</b>'+(g<0||g%1?'. Resultado impossível: confira a fórmula.':(g===0?'. Saturado, sem anel.':g===4?'. Compatível com um anel benzênico.':'.'));
}
function obInit(){$('#gdhGo').onclick=gdhRun;$('#gdhF').addEventListener('keydown',e=>{if(e.key==='Enter')gdhRun();});}
