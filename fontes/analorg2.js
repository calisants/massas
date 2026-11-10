/* ================= ANALORG v2: COMPOSTOS, IDENTIFICAÇÃO, RMN, ORGÂNICA BÁSICA ================= */
const SOLNM={S2:'S₂',SA:'SA',SB:'SB',S1:'S₁',A1:'A₁',A2:'A₂',B:'B',MN:'MN',N:'N',I:'I'};
const GORD=['S2','SA','SB','S1','A1','A2','B','MN','N','I'];
const norm2=s=>String(s||'').toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g,'').replace(/[-\s,().]/g,'');
const tC=v=>v==null?'—':(String(v).replace('.',',')+' °C');
const gTxt=k=>{const g=(typeof SOLG!=='undefined'?SOLG:[]).find(x=>x.k===k);return g?g.t:'';};
const ivr=b=>[Math.min(b[0],b[1]),Math.max(b[0],b[1])];
const nCl=f=>{const m=String(f).match(/Cl(\d*)/);return m?(m[1]?+m[1]:1):0;};
const pfTag=s=>s==='c'?' <span class="tag sv">Conferido: PubChem</span>':s==='d'?' <span class="tag sm">fontes divergem</span>':'';
function srcTag(ok,txt){return '<span class="tag '+(ok?'sv':'sm')+'">'+esc(txt)+'</span>';}
function copyTxt(t,btn){
  const done=()=>{if(btn){const o=btn.textContent;btn.textContent='Copiado';setTimeout(()=>btn.textContent=o,1200);}};
  try{navigator.clipboard.writeText(t).then(done,done);}catch(e){done();}
}

/* ---------- lista de compostos ---------- */
function cpInit(){
  const g=$('#cpG'),sel=$('#rmSel'),ex=$('#icEx');
  GORD.forEach(k=>{const o=document.createElement('option');o.value=k;o.textContent=SOLNM[k];g.appendChild(o);});
  const byName=[...COMP].sort((a,b)=>a.n.localeCompare(b.n,'pt'));
  byName.forEach(c=>{[sel,ex].forEach(s=>{const o=document.createElement('option');o.value=c.i;o.textContent=c.n;s.appendChild(o);});});
  $('#cpF').addEventListener('click',()=>{CPFAV=!CPFAV;$('#cpF').setAttribute('aria-pressed',CPFAV?'true':'false');cpDraw();});
  $('#cpQ').addEventListener('input',cpDraw);['#cpE','#cpG'].forEach(id=>$(id).addEventListener('change',cpDraw));
  sel.onchange=rmDraw;
  cpDraw();rmDraw();
}
function cpDraw(){
  const q=norm2($('#cpQ').value),e=$('#cpE').value,g=$('#cpG').value;
  const l=COMP.filter(c=>(!q||[c.n,...c.a,c.f,c.cas].some(x=>norm2(x).includes(q)))&&(!e||c.est.indexOf(e)===0)&&(!g||c.g===g)&&(!CPFAV||favHas(c))).sort((a,b)=>(favHas(b)-favHas(a))||a.n.localeCompare(b.n,'pt'));
  $('#cpN').textContent=l.length+' de '+COMP.length+' compostos';
  $('#cpL').innerHTML=l.length?l.map(c=>'<button class="cpc" type="button" data-cf="'+c.i+'"><span class="thumb">'+c.s+'</span><span><b>'+esc(c.n)+'</b>'+(favHas(c)?' <span class="favst" role="img" aria-label="favorito">★</span>':'')+'<span class="m">'+fmt(c.f)+' · '+SOLNM[c.g]+'</span><span class="m">'+esc(c.est)+(c.pf!=null?' · PF '+tC(c.pf):'')+(c.pe!=null?' · PE '+tC(c.pe):'')+'</span></span></button>').join(''):'<p class="empty">'+(CPFAV&&!favGet().length?'Nenhum favorito ainda. Abra uma ficha e toque em Favoritar.':'Nenhum composto com esse filtro.')+'</p>';
}
document.addEventListener('click',ev=>{const fb=ev.target.closest('#favBtn');if(fb&&CFI!=null){favToggle(COMP[CFI]);fb.outerHTML=favBtnHtml(COMP[CFI]);const nb=$('#favBtn');if(nb)nb.focus();cpDraw();return;}
  const b=ev.target.closest('[data-cf]');if(b){cfDraw(+b.dataset.cf);go('p-cf');}
  const cp=ev.target.closest('[data-copy]');if(cp)copyTxt(cp.dataset.copy,cp);});

/* ---------- RMN estimado ---------- */
const HLRO='<div class="hlro" data-dica="Toque num número do espectro ou numa linha da tabela: o trecho da molécula fica colorido.">Toque num número do espectro ou numa linha da tabela: o trecho da molécula fica colorido.</div>';
function nmrBlock(c){
  const c13=c.c13.slice().sort((a,b)=>(b.lo+b.hi)-(a.lo+a.hi)),cc=Object.assign({},c,{c13:c13});
  const fr=x=>String(x).replace('.',',');
  let h='<p class="hint" style="margin:0 0 6px"><b>Espectro simulado, não é o medido.</b> Número de sinais, integração e multiplicidade (regra n+1) saem da estrutura. A posição de cada sinal é o meio da faixa de tabela, então não bate com o espectro real. Os desdobramentos foram aumentados e sinais com a mesma faixa foram afastados um pouco, para dar para ver. O espectro medido está no SDBS.</p><p class="srcl">Simulação por regras de tabela, sem fonte conferida.</p>';
  h+='<h4 style="margin:10px 0 4px">¹H: '+c.h1.length+(c.h1.length>1?' sinais':' sinal')+' ('+c.h1.reduce((a,x)=>a+x.h,0)+' H no total)</h4>';
  h+='<div class="nmrwrap">'+nmrSpec(c,'h')+'<button class="zbtn" type="button" data-zoom>Ampliar</button><button class="chip" type="button" data-nmrint aria-pressed="false">Mostrar a integração</button></div>';
  h+='<div class="tbl"><table class="obt nostk cmp cmp-nmr"><thead><tr><th>#</th><th>Sinal</th><th>Faixa (ppm)</th></tr></thead><tbody>'+c.h1.map((x,i)=>'<tr class="hlr" data-at="'+x.on.join(',')+'" data-hk="h'+(i+1)+'" data-tx="'+ea('¹H, sinal '+(i+1)+': '+x.t+' · '+x.h+' H'+(x.c?' em '+x.c:'')+' · δ '+x.lo+'–'+x.hi+' ppm')+'"><td><b>'+(i+1)+'</b></td><td>'+esc(x.t)+'<div class="mut sm">'+x.h+' H'+(x.c?' em '+esc(x.c):'')+' · '+esc(x.m)+'</div></td><td class="n">'+fr(x.lo)+'–'+fr(x.hi)+'</td></tr>').join('')+'</tbody></table></div>';
  if(c.h1m)h+='<div class="meas"><span class="tag sv">Conferido: SDBS</span> <b>¹H medido'+(c.h1m[0]?' (SDBS No. '+c.h1m[0]+')':'')+':</b> '+c.h1m[1].map(v=>String(v).replace('.',',')).join(' · ')+' ppm<div class="mut sm">Lido do print do SDBS, valores de δ do pico (o print não traz integração nem J). '+(c.h1m[2]?'O print traz só parte dos sinais. ':'')+'A faixa da tabela acima é só referência; o medido é o que vale.</div></div>';
  else h+='<p class="srcl">Sem print de ¹H conferido para este composto: use só a faixa de tabela.</p>';
  h+='<h4 style="margin:12px 0 4px">¹³C: '+c.c13.length+(c.c13.length>1?' sinais':' sinal')+' (de '+c.c13.reduce((a,x)=>a+x.n,0)+' C)</h4>';
  h+='<div class="nmrwrap">'+nmrSpec(cc,'c')+'<button class="zbtn" type="button" data-zoom>Ampliar</button><p class="mut" style="margin:2px 0 6px">Cada linha é um tipo de C. A altura é só ilustrativa (mais C equivalentes, linha um pouco maior).</p></div>';
  h+='<div class="tbl"><table class="obt nostk cmp cmp-nmr"><thead><tr><th>C</th><th>Sinal</th><th>Faixa (ppm)</th></tr></thead><tbody>'+c13.map((x,i)=>'<tr class="hlr" data-at="'+x.at.join(',')+'" data-hk="c'+(i+1)+'" data-tx="'+ea('¹³C, sinal '+(i+1)+': '+x.t+' · '+x.n+' C · δ '+x.lo+'–'+x.hi+' ppm')+'"><td><b>'+(i+1)+'</b></td><td>'+esc(x.t)+'<div class="mut sm">'+x.n+' C equivalente'+(x.n>1?'s':'')+(x.pos?' · posição '+x.pos+' ao substituinte':'')+'</div></td><td class="n">'+x.lo+'–'+x.hi+'</td></tr>').join('')+'</tbody></table></div>';
    if(c.c13m)h+='<div class="meas"><span class="tag sv">Conferido: SDBS</span> <b>¹³C medido'+(c.sdbs?' (SDBS No. '+c.sdbs+')':'')+':</b> '+c.c13m.slice().sort((a,b)=>b-a).map(v=>String(v).replace('.',',')).join(' · ')+' ppm<div class="mut sm">Lido da tabela de ppm do print do SDBS. A faixa acima é a de tabela; o valor medido é o que importa para este composto.</div></div>';
  else h+='<p class="srcl">Sem print de ¹³C conferido para este composto: use só a faixa de tabela.</p>';
  return h;
}
function rmDraw(){const c=COMP[+$('#rmSel').value||COMP.findIndex(x=>x.n===$('#rmSel').options[0].textContent)];if(!c)return;
  $('#rmOut').innerHTML='<div class="cfh" style="margin-top:10px"><figure class="st hlfig"><div>'+(c.sn||c.s)+'</div><figcaption>'+fmt(c.f)+'</figcaption>'+HLRO+'</figure><div>'+nmrBlock(c)+'</div></div>';}

/* ---------- ficha do composto ---------- */
function openMS(n){const e=EX.find(x=>x.n===n);if(!e)return;curEx=n;pkSel=null;$('#inM').value=e.M;$('#inP').value=e.peaks.filter(p=>p!==e.M).join(', ');buildChips();analyze();anStage(true);go('p-an');$('#an-in').hidden=true;$('#an-res').hidden=false;}
let CFI=null;
function msFrag(c){
  if(!c.msf||!c.msf.length)return '';
  const nv=x=>x>=5?'Provável':x>=3?'Possível':x>0?'Pouco estável, mas possível':'Só pela massa';
  let h='<h3 style="margin:14px 0 4px">Fragmentos propostos</h3><p class="hint">Proposta por regras de fragmentação (clivagem α, benzílica, McLafferty, perda de CO). A massa de cada íon confere com o pico '+(c.msv===2?'do SDBS':'cadastrado (típico, sem fonte conferida)')+', mas <b>não é o mecanismo medido</b>: dois caminhos diferentes podem dar o mesmo m/z.</p><div class="msfl">';
  h+=c.msf.map(x=>'<div class="msfc"><div class="msfh"><b class="mono">m/z '+x.mz+'</b> '+(c.msv===2?'<small>'+x.p+'%</small>':'')+(x.f?'<span class="msff">'+x.f+'</span>':'')+'</div><div class="msfb">'+(x.k?'<figure class="st">'+MSFS[x.k]+'</figure>':'')
    +'<div><span>Vem de m/z '+x.de+', perdendo <b>'+esc(x.n)+'</b></span><br><small>'+esc(x.r)+'</small><br><small class="msfn">'+nv(x.nv)+(x.alt?'. Outro caminho dá o mesmo m/z.':'')+'</small></div></div></div>').join('')+'</div>';
  if(c.msfs&&c.msfs.length)h+='<p class="hint">Sem proposta para m/z '+c.msfs.join(', ')+': nenhuma regra simples fecha a massa (rearranjos mais complexos ou abertura de anel).</p>';
  return h;}
function msSpec(c){
  const W=340,H=165,L=30,R=8,T=16,B=40,pk=c.msi,x0=0,x1=Math.ceil((c.M+8)/10)*10,X=v=>L+(v-x0)/(x1-x0)*(W-L-R),Y=v=>T+(100-v)/100*(H-T-B);
  let g='';
  [0,50,100].forEach(t=>{g+='<text class="tl" x="'+(L-4)+'" y="'+(Y(t)+3)+'" text-anchor="end">'+t+'</text>';});
  const st=x1>150?20:10;for(let t=0;t<=x1;t+=st)g+='<line class="tk" x1="'+X(t)+'" y1="'+Y(0)+'" x2="'+X(t)+'" y2="'+(Y(0)+4)+'"/><text class="tl" x="'+X(t)+'" y="'+(H-24)+'" text-anchor="middle">'+t+'</text>';
  const ma=c.msat||{};let bars='';
  pk.forEach(p=>{const x=X(p[0]).toFixed(1),y=Y(p[1]).toFixed(1),k=String(p[0]),a=ma[k];
    const d=a?' data-at="'+a[0].join(',')+'" data-hk="m'+k+'" data-tx="'+ea('m/z '+k+': '+a[1])+'" tabindex="0" role="button" aria-label="m/z '+k+'"':'';
    bars+='<g class="hpk"'+d+'><rect class="hit" x="'+(X(p[0])-6).toFixed(1)+'" y="'+T+'" width="12" height="'+(H-T-B)+'"/><line class="mb" x1="'+x+'" x2="'+x+'" y1="'+Y(0)+'" y2="'+y+'"/>'+(p[1]>=12||a?'<text class="mt" x="'+x+'" y="'+(y-3)+'" text-anchor="middle">'+p[0]+'</text>':'')+'</g>';});
  return '<svg class="nmrspec" viewBox="0 0 '+W+' '+H+'" role="img" aria-label="Espectro de massas de '+esc(c.n)+'">'+g+'<line class="ax" x1="'+L+'" y1="'+Y(0)+'" x2="'+(W-R)+'" y2="'+Y(0)+'"/>'+bars+'<text class="tl" x="'+(W/2)+'" y="'+(H-0)+'" text-anchor="middle">m/z · eixo vertical: intensidade relativa (%)</text></svg>';
}
function cfDraw(i){
  CFI=i;const c=COMP[i],hoje=new Date().toLocaleDateString('pt-BR');
  const sd=c.sdbs||(c.ex&&typeof INTS!=='undefined'&&INTS[c.ex]?INTS[c.ex].sdbs:null);
  let h='<h2 class="scr">'+esc(c.n)+'</h2>'+(c.a.length?'<p class="scrsub">Também: '+c.a.map(esc).join(', ')+'</p>':'')+'<div class="row" style="margin:0 0 8px">'+favBtnHtml(c)+'</div>';
  const rowd=(k,v)=>'<div class="cfr"><dt>'+k+'</dt><dd>'+v+'</dd></div>';
  h+='<figure class="cfs hlfig"><div>'+(c.si||c.s)+'</div><figcaption>'+fmt(c.f)+' · '+String(c.mw).replace('.',',')+' g/mol'+''+'</figcaption>'+HLRO+'</figure>'
   +'<div class="cfq">'
   +'<div class="cfqi"><span>Estado a 25 °C</span><b>'+esc(c.est)+'</b></div>'
   +'<div class="cfqi"><span>Cor</span><b>'+esc(c.cor)+'</b></div>'
   +'<div class="cfqi"><span>Ponto de fusão</span><b>'+tC(c.pf)+'</b>'+pfTag(c.pfs)+'</div>'
   +'<div class="cfqi"><span>Ponto de ebulição</span><b>'+tC(c.pe)+'</b>'+pfTag(c.pes)+'</div></div>'
   +'<dl class="cfd">'
   +rowd('Grupo de solubilidade','<span class="gl2">'+SOLNM[c.g]+'</span> '+esc(gTxt(c.g)))
   +rowd('Grupo funcional',esc(c.gf.join(', ')||'hidrocarboneto sem grupo funcional'))
   +rowd('GDH','<b>'+c.gdh+'</b> <span class="mut">(anéis + ligações π)</span>')
   +rowd('M do íon molecular','<b>'+c.M+'</b>')
   +rowd('CAS','<span class="mono">'+esc(c.cas)+'</span>')
   +(c.obs?rowd('Observação',esc(c.obs)):'')+'</dl>';
  let srcH='';
  {const pubs=c.pubsrc&&c.pubsrc.length;
   srcH='<p class="srcl"><b>Fonte:</b> '+(pubs?'PF e PE marcados "conferido" vêm do PubChem (mediana dos valores de '+c.pubsrc.map(esc).join(', ')+'), acessado em 04/11/2026'+(c.cid?' (CID '+c.cid+')':'')+'. ':'')
   +((c.pfs==='d'||c.pes==='d')?'Onde aparece "fontes divergem", o PubChem traz valores diferentes entre si e foi mantido o valor que já estava no app. ':'')
   +'Estado, cor, grupo de solubilidade e CAS estão <b>sem fonte conferida</b>'+(pubs?'':', assim como PF e PE')+' (confirme no SDBS ou na Plataforma do professor antes de usar em relatório). Fórmula, massa, GDH e estrutura são calculados a partir da estrutura (RDKit).</p>';}
  // IV
  const iv=c.iv.map((b,k)=>b.concat([k])).sort((a,b)=>ivr(b)[1]-ivr(a)[1]);
  h+='<details class="sec" open><summary>Infravermelho: bandas esperadas</summary>'
   +(iv.length?'<div class="tbl"><table class="obt nostk"><thead><tr><th>cm⁻¹</th><th>O que é</th></tr></thead><tbody>'+iv.map(b=>{const at=(c.ivat||[])[b[6]]||[],tx=b[2]+' · '+ivr(b)[0]+'–'+ivr(b)[1]+' cm⁻¹';return '<tr'+(at.length?' class="hlr" data-at="'+at.join(',')+'" data-hk="f'+b[6]+'" data-tx="'+ea(tx)+'"':'')+'><td class="mono n">'+ivr(b)[0]+'–'+ivr(b)[1]+'</td><td><b>'+esc(b[2].replace(' (estiramento)',''))+'</b>'+(b[4]?' <span class="tag sv">chave</span>':'')+'<span class="mut sm">Intensidade '+esc(b[3])+' · '+(b[5]==='a'?'apostila':b[5]==='s'?'fontes citadas abaixo':'tabela geral, sem fonte conferida')+'</span></td></tr>';}).join('')+'</tbody></table></div>':'<p class="empty">Sem bandas cadastradas.</p>')
   +'<p class="srcl" style="margin-top:8px">Faixas esperadas pelo grupo funcional, não o espectro medido. "Chave" = banda que decide a identificação.</p>'
   +(c.irc?'<p class="srcl">'+srcTag(true,c.irc===1?'Conferido: SDBS':'Conferido em parte: SDBS')+' '+(c.irc===1?'As bandas-chave do espectro de IV do SDBS No. '+c.sdbs+' ('+esc(c.irm)+') caem nas faixas acima.':(c.irn?esc(c.irn):'Do IV do SDBS No. '+c.sdbs+' ('+esc(c.irm)+') só conferi o O–H largo e o C–O.'))+' Lido dos prints enviados, acessado em 04/11/2026. O meio importa: ligação de H e solvente mudam a posição das bandas.</p>':'')
   +((c.ivf&&c.ivf.length)?'<h3 style="margin:12px 0 4px">O que pode deslocar as bandas deste composto</h3><ul class="fatl">'+c.ivf.map(f=>'<li><b>'+esc(f[0])+'.</b> '+esc(f[1])+'</li>').join('')+'</ul>':'')
   +'</details>';
  // MS
  h+='<details class="sec"><summary>Espectrometria de massas</summary><p>M = <b>'+c.M+'</b> ('+(c.M%2?'ímpar: número ímpar de N':'par: zero ou número par de N')+').</p>';
  if(c.ms){const ma=c.msat||{},mat=k=>ma[k]?' data-at="'+ma[k][0].join(',')+'" data-hk="m'+k+'" data-tx="'+ea('m/z '+k+': '+ma[k][1])+'" tabindex="0"':'';
    const tp=c.msi?c.msi.map(p=>'<span class="pk'+(p[0]===c.M?' base':'')+'"'+mat(p[0])+'>'+p[0]+' <small>'+p[1]+'%</small></span>').join(''):c.ms.map(p=>'<span class="pk'+(p===c.M?' base':'')+'"'+mat(p)+'>'+p+'</span>').join('');
    h+=(c.msi?'<div class="nmrwrap">'+msSpec(c)+'<button class="zbtn" type="button" data-zoom>Ampliar</button></div>':'')+'<p>'+tp+'</p>'+(Object.keys(ma).length?'<p class="srcl">Os picos sublinhados têm um trecho da molécula associado: toque para ver. Só marquei os fragmentos que a regra do livro atribui sem ambiguidade (M⁺·, CH₃⁺, C₆H₅⁺, C₇H₇⁺, C₆H₅CO⁺, CH₃CO⁺, CH₂=OH⁺, CH₂=NH₂⁺). Os demais picos ficam sem destaque porque eu não tenho fonte para dizer qual parte da molécula os origina.</p>':'')+'<p class="srcl">'+srcTag(c.msv>0,c.msv===2?'Conferido: SDBS':(c.msv?'Conferido: lousa e SDBS':'Sem fonte conferida'))+' '+(c.msv===2?'Picos do espectro SDBS No. '+c.sdbs+' ('+esc(c.msid)+'), lidos do gráfico em 04/11/2026; a intensidade relativa tem erro de uns 3 pontos.':c.msv?'Picos do exercício do app, com mecanismo.':'Picos típicos de EI 70 eV escritos por mim; confirme no SDBS.')+'</p>';}
  else h+='<p class="empty">Sem picos cadastrados.</p>';
  h+=msFrag(c);
  if(nCl(c.f))h+='<p class="srcl">Contém Cl: aparece M+2 (isótopo ³⁷Cl). Com 1 Cl, M : M+2 é cerca de 3 : 1.</p>';
  if(c.ex)h+='<button class="btn" type="button" data-ms="'+c.ex+'">Ver os mecanismos de fragmentação</button>';
  h+='</details>';
  // RMN
  h+='<details class="sec"><summary>RMN de ¹H e ¹³C</summary>'+nmrBlock(c)+'</details>';
  // SDBS
  h+='<details class="sec"><summary>SDBS (espectros reais)</summary><p>O SDBS tem IV, MS, ¹H-RMN e ¹³C-RMN medidos deste composto. Busque pelo nome ou pelo CAS.</p><div class="row" style="margin:0 0 8px">'
   +'<a class="btn" href="'+(sd?'https://sdbs.db.aist.go.jp/sdbs/cgi-bin/landingpage?sdbsno='+sd:'https://sdbs.db.aist.go.jp/')+'" target="_blank" rel="noopener">Abrir o SDBS</a>'
   +'<button class="btn ghost" type="button" data-copy="'+esc(c.n)+'">Copiar nome</button><button class="btn ghost" type="button" data-copy="'+esc(c.cas)+'">Copiar CAS</button></div>'
   +(sd?'<p class="srcl">Nº SDBS: <b>'+sd+'</b>. Se o link abrir a página inicial, aceite o aviso e busque por esse número.</p>':'<p class="srcl">Nº SDBS não cadastrado aqui. Use o nome ou o CAS na busca.</p>')
   +'<p class="srcl">Ao usar dados do SDBS, cite: SDBS, National Institute of Advanced Industrial Science and Technology (AIST), https://sdbs.db.aist.go.jp, acessado em '+hoje+'. O SDBS não permite coleta automática nem download em massa; por isso o app só liga para ele.</p></details>';
  h+='<details class="sec"><summary>De onde vêm os dados</summary>'+srcH+'</details>';
  h+='<div class="row"><button class="btn ghost" type="button" data-icfill="'+c.i+'">Usar na Identificação do Composto</button></div>';
  $('#cfB').innerHTML=h;
}
document.addEventListener('click',ev=>{const b=ev.target.closest('[data-ms]');if(b)openMS(+b.dataset.ms);
  const f=ev.target.closest('[data-icfill]');if(f){icFill(+f.dataset.icfill);go('p-ic');}});

/* ---------- Identificação do Composto (tela única: classes + compostos) ---------- */
const nums=s=>(String(s||'').replace(/,(?=\d)(?![^,]*\d{3}\b)/g,'.').match(/\d+(?:[.,]\d+)?/g)||[]).map(x=>parseFloat(x.replace(',','.')));
const numsInt=s=>(String(s||'').match(/\d+/g)||[]).map(Number);
const ELS=[['O','Oxigênio (O)'],['H','Hidrogênio (H)'],['N','Nitrogênio (N)'],['S','Enxofre (S)'],['Cl','Cloro (Cl)'],['Br','Bromo (Br)'],['I','Iodo (I)']];
const ELORD=['N','S','Cl','Br','I','O','H'];
const COR=[['inc','Incolor ou branco'],['amarelo','Amarelo'],['laranja','Laranja'],['vermelho','Vermelho ou rosa'],['marrom','Marrom'],['verde','Verde'],['azul','Azul'],['violeta','Violeta ou roxo']];
const IRF={oh:/^O–H/,nh:/^N–H/,co:/^C=O/,ald:/C–H de aldeído/,cn:/^C≡N/,cc:/^C≡C|^≡C–H/,dc:/^C=C \(|^=C–H/,no2:/^N=O/,ar:/anel|aromático/};
const cIr=(c,k)=>c.iv.some(b=>IRF[k].test(b[2]));
const elCount=f=>{const m={};String(f).replace(/([A-Z][a-z]?)(\d*)/g,(a,e,n)=>{m[e]=(m[e]||0)+(n?+n:1);return '';});return m;};
const corFam=s=>{s=String(s||'').toLowerCase();const k=s.indexOf('('),main=k<0?s:s.slice(0,k),par=k<0?'':s.slice(k);
  const f=t=>{const r=new Set();if(/incolor|branc/.test(t))r.add('inc');if(/amarel/.test(t))r.add('amarelo');if(/laranj/.test(t))r.add('laranja');if(/verm|ros/.test(t))r.add('vermelho');if(/marrom|castanh/.test(t))r.add('marrom');if(/verde/.test(t))r.add('verde');if(/azul/.test(t))r.add('azul');if(/viole|roxo|purpur/.test(t))r.add('violeta');return r;};
  return [f(main),f(par)];};
const IC_CAMPOS=['#icPF','#icPE','#icTol','#icIV','#icM','#icP','#icH','#icC','#icHd','#icF','#icGDH','#icGF'];
let icSt={est:'',cor:'',g:'',el:{},ir:{},sub:{}};
const sx=h=>String(h).replace(/<[^>]*>/g,'');

function icChips(key,opts){
  return opts.map(o=>'<button class="chip" type="button" data-ck="'+key+'" data-cv="'+o[0]+'" aria-pressed="'+(icSt[key]===o[0]?'true':'false')+'">'+o[1]+'</button>').join('');
}
function icTri(kind,key,label){
  const cur=icSt[kind][key]||'';
  return '<div class="tri"><span class="tl">'+label+'</span><span class="tb" role="group" aria-label="'+esc(label.replace(/<[^>]*>/g,''))+'">'+[['sim','Sim'],['nao','Não'],['','Não sei']].map(v=>'<button type="button" data-tk="'+kind+'" data-ti="'+key+'" data-tv="'+v[0]+'" aria-pressed="'+(cur===v[0]?'true':'false')+'">'+v[1]+'</button>').join('')+'</span></div>';
}
function icDraw(){
  $('#icEstC').innerHTML=icChips('est',[['','Estado: não sei'],['líquido','Líquido'],['sólido','Sólido']]);
  $('#icCorC').innerHTML=icChips('cor',[['','Cor: não sei']].concat(COR));
  $('#icGrpC').innerHTML=icChips('g',[['','Não sei']].concat(SOLG.map(x=>[x.k,SOLN[x.k]])));
  $('#icElR').innerHTML=ELORD.map(k=>icTri('el',k,ELS.find(e=>e[0]===k)[1])).join('');
  $('#icIrR').innerHTML=IDIR.map(x=>icTri('ir',x[0],x[1])).join('');
  $('#icSubR').innerHTML=SUBL.map(x=>icTri('sub',x[0],x[1])).join('');
}
function icReset(){icSt={est:'',cor:'',g:'',el:{},ir:{},sub:{}};IC_CAMPOS.forEach(i=>$(i).value='');$('#icTol').value='5';$('#icEx').value='';}
let icTm;
function icQueue(){clearTimeout(icTm);icTm=setTimeout(()=>{icRun();icSave();},160);}
function icSave(){const f={};IC_CAMPOS.forEach(i=>f[i]=$(i).value);LS.set('massas-ic',{st:icSt,f:f});}
function icLoad(){const d=LS.get('massas-ic',null);if(!d||!d.st)return;
  icSt={est:d.st.est||'',cor:d.st.cor||'',g:d.st.g||'',el:d.st.el||{},ir:d.st.ir||{},sub:d.st.sub||{}};
  IC_CAMPOS.forEach(i=>{if(d.f&&d.f[i]!=null)$(i).value=d.f[i];});}
function icRange(id,tol){
  let s=$(id).value.trim().replace(/[–—]|\s+a\s+/g,'|').replace(/,/g,'.');if(!s)return null;
  let m=s.match(/^(\d+(?:\.\d+)?)\s*-\s*(\d+(?:\.\d+)?)$/);if(m)s=m[1]+'|'+m[2];
  const p=s.split('|').map(x=>parseFloat(x.replace('−','-'))).filter(x=>isFinite(x));
  if(!p.length)return null;
  return p.length>1?{v:(p[0]+p[1])/2,t:Math.max(tol,Math.abs(p[1]-p[0])/2)}:{v:p[0],t:tol};
}
function icInputs(){
  const v=id=>$(id).value.trim();
  const num=id=>{const x=parseFloat(v(id).replace(',','.'));return isFinite(x)?x:null;};
  const tol=+v('#icTol')||5;
  return {est:icSt.est,cor:icSt.cor,g:icSt.g,F:v('#icF').replace(/\s+/g,''),gdh:num('#icGDH'),gf:v('#icGF'),
    els:ELORD.map(e=>[e,icSt.el[e]]).filter(e=>e[1]),ir:icSt.ir,sub:icSt.sub||{},
    pf:icRange('#icPF',tol),pe:icRange('#icPE',tol),
    iv:numsInt(v('#icIV')),M:num('#icM'),pk:numsInt(v('#icP')),h:num('#icH'),c:num('#icC'),hd:nums(v('#icHd'))};
}
const gauss=(d,t)=>Math.max(0.02,Math.exp(-0.5*Math.pow(d/t,2)));
function icScore(c,x){
  const parts=[];let w=1;
  const add=(k,lab,f,det)=>{parts.push({k,lab,f,det:det||''});w*=f;};
  if(x.est)add('est','estado',c.est.indexOf(x.est)===0?1:0.05,c.est);
  if(x.cor){const [m,p]=corFam(c.cor);add('cor','cor',m.has(x.cor)?1:p.has(x.cor)?0.5:0.12,c.cor);}
  if(x.g)add('g','solubilidade',c.g===x.g?1:0.04,'grupo '+SOLNM[c.g]);
  if(x.pf)add('pf','PF',c.pf==null?0.05:gauss(c.pf-x.pf.v,x.pf.t),'PF '+tC(c.pf));
  if(x.pe)add('pe','PE',c.pe==null?0.08:gauss(c.pe-x.pe.v,x.pe.t),'PE '+tC(c.pe));
  if(x.els.length){c._el=c._el||elCount(c.f);}
  x.els.forEach(([e,v])=>{const has=!!(c._el&&c._el[e]);add('el','elemento '+e,(v==='sim')===has?1:0.03,has?'tem '+e:'sem '+e);});
  IDIR.forEach(([k,lab])=>{const u=x.ir[k];if(!u)return;const has=cIr(c,k);add('irf','IV: '+lab.replace(/ \(.*/,''),(u==='sim')===has?1:0.05,has?'tem essa banda':'não tem essa banda');});
  SUBL.forEach(([k,lab])=>{const u=x.sub[k];if(!u)return;const has=(c.sub||[]).indexOf(k)>=0;add('sub',lab.replace(/ \(.*/,''),(u==='sim')===has?1:0.04,has?'tem':'não tem');});
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
/* quais classes de composto sobram (grupo de solubilidade, elementos e bandas de IV marcados) */
function icClasses(){
  const hs=['Cl','Br','I'].map(e=>icSt.el[e]);
  const E={N:icSt.el.N,S:icSt.el.S,O:icSt.el.O,X:hs.indexOf('sim')>=0?'sim':(hs.every(v=>v==='nao')?'nao':'')};
  const st={g:icSt.g,el:E,ir:icSt.ir},ok=[],out=[];
  const any=st.g||Object.keys(E).some(k=>E[k])||Object.keys(st.ir).length;
  if(!any)return {any:false,ok,out};
  IDCLS.forEach(c=>{
    let why=[],bad='',pts=0;
    if(st.g){if(c.g.indexOf(st.g)<0)bad='o grupo '+sx(SOLN[st.g])+' não combina (essa classe cai em '+c.g.map(x=>sx(SOLN[x])).join(', ')+')';else{pts++;why.push('grupo '+sx(SOLN[st.g]));}}
    [['el',IDEL],['ir',IDIR]].forEach(P=>{
      const req=c[P[0]]||{};
      P[1].forEach(x=>{const u=st[P[0]][x[0]],r=req[x[0]];
        if(!u||r===undefined)return;
        const lab=x[1].replace(/ \(.*/,'');
        if(u==='sim'&&r===1){pts++;why.push(lab+' presente');}
        else if(u==='nao'&&r===0){pts++;why.push(lab+' ausente');}
        else if(!bad){bad=(r===1?'exige ':'não tem ')+lab+(r===1?', mas você marcou Não':', mas você marcou Sim');}});});
    (bad?out:ok).push({c,pts,why,bad});});
  ok.sort((a,b)=>b.pts-a.pts);
  return {any:true,ok,out};
}
function icBands(){
  const v=($('#icIV').value.match(/\d{3,4}/g)||[]).map(Number).filter(x=>x>=400&&x<=4000);
  if(!v.length){$('#icBandOut').innerHTML='';return;}
  $('#icBandOut').innerHTML=v.map(x=>{
    const hit=IRT.filter(r=>x<=r[0]+(r[0]===r[1]?5:0)&&x>=r[1]-(r[0]===r[1]?5:0));
    const seen={},nm=[];hit.forEach(r=>{if(!seen[r[2]]){seen[r[2]]=1;nm.push(r[2]);}});
    return '<p class="hint" style="margin:6px 0"><b>'+x+' cm⁻¹</b>: '+(nm.length?esc(nm.slice(0,5).join('; '))+(nm.length>5?'; ...':''):'nada na tabela do app')+'</p>';}).join('')
   +'<p class="hint">As faixas se sobrepõem. Use isso como pista e confirme com a outra banda indicada na aba IV.</p>';
}
function icRun(){setTimeout(()=>{if(typeof icBadges==="function")icBadges();},0);
  icBands();
  const x=icInputs(),cl=icClasses();
  const res=COMP.map(c=>({c,...icScore(c,x)}));
  const used=res[0].parts.length;
  let h='',sum='';
  if(!used&&!cl.any){ICLAST=null;icExpShow();$('#icOut').innerHTML='<p class="empty">Marque pelo menos um dado acima.</p>';$('#icSum').textContent='Marque pelo menos um dado.';return;}
  /* 1. classes */
  h+='<details class="sec" open><summary>Classes que sobram'+(cl.any?' ('+cl.ok.length+' de '+IDCLS.length+')':'')+'</summary>';
  if(!cl.any)h+='<p class="empty">Marque solubilidade, elementos ou bandas de IV para filtrar as classes.</p>';
  else{
    h+=cl.ok.length?cl.ok.map(o=>'<div class="rescls"><h3>'+o.c.n+'</h3><p>Grupos possíveis: '+o.c.g.map(g=>SOLN[g]).join(', ')+'</p>'+(o.why.length?'<p>Combina: '+o.why.join('; ')+'.</p>':'')+(IDHINT[o.c.n]?'<p>'+IDHINT[o.c.n]+'</p>':'')+'</div>').join(''):'<p class="empty">Nenhuma classe da lista combina com tudo. Confira o que você marcou.</p>';
    if(cl.out.length)h+='<details style="margin-top:10px"><summary>Descartadas ('+cl.out.length+')</summary>'+cl.out.map(o=>'<div class="rescls out"><h3>'+o.c.n+'</h3><p>'+o.bad+'.</p></div>').join('')+'</details>';
    h+='<p class="srcl">'+srcTag(false,'Sem fonte conferida')+' As regras das classes (quais bandas e elementos cada uma exige) foram montadas a partir da tabela de grupos do Analor e das bandas de IV do app. A lista não tem todas as classes.</p>';
  }
  h+='</details>';
  /* 2. compostos */
  h+='<details class="sec" open><summary>Compostos do banco mais compatíveis</summary>';
  if(!used)h+='<p class="empty">Preencha estado, cor, PF, PE, elementos, IV (Sim/Não ou números) ou os dados da seção 6 para comparar com os '+COMP.length+' compostos.</p>';
  else{
    const tot=res.reduce((a,r)=>a+r.w,0)||1;res.forEach(r=>r.p=r.w/tot*100);
    res.sort((a,b)=>b.w-a.w);
    const top=res.slice(0,5).filter((r,i)=>i<3||r.p>=1);
    if(used<3)h+='<div class="icwarn">Só '+used+' critério'+(used>1?'s':'')+' preenchido'+(used>1?'s':'')+': vários compostos ficam parecidos. Acrescente IV, PE ou RMN para separar.</div>';
    if(res[0].w<0.05)h+='<div class="icwarn">Nenhum composto do banco combina bem com todos os dados. O seu pode não estar na lista; os de baixo são só os mais parecidos.</div>';
    else if(res.length>1&&res[0].p<2*res[1].p)h+='<div class="icwarn">O primeiro e o segundo estão próximos. Falta um dado que os separe (veja o que difere nas linhas abaixo).</div>';
    h+=top.map(r=>'<div class="icr"><div class="top"><b><button class="back" style="margin:0;font-size:1rem" type="button" data-cf="'+r.c.i+'">'+esc(r.c.n)+'</button> <span class="mono" style="font-weight:400;color:var(--muted)">'+fmt(r.c.f)+'</span></b><span class="pct">'+(r.p>=10?r.p.toFixed(0):r.p.toFixed(1)).replace('.',',')+'%</span></div><div class="bar"><i style="width:'+Math.min(100,r.p).toFixed(1)+'%"></i></div>'
      +'<div class="cr">'+r.parts.map(p=>'<span class="'+(p.f>=0.7?'ok':p.f>=0.2?'md':'no')+'">'+(p.f>=0.7?'✓ ':p.f>=0.2?'~ ':'✗ ')+esc(p.lab)+'</span>').join('')+'</div>'
      +'<p class="det">'+r.parts.filter(p=>p.det&&p.f<0.7).map(p=>'<b>'+esc(p.lab)+':</b> '+esc(p.det)).join(' · ')+'</p></div>').join('');
    h+='<p class="hint">Base: '+COMP.length+' compostos do app. ✓ combina, ~ combina em parte, ✗ não combina.</p><p class="srcl">'+srcTag(false,'Sem fonte conferida')+' Estado, cor e grupo de solubilidade do banco podem estar um pouco diferentes da sua tabela. PF e PE com a etiqueta Conferido vêm do PubChem.</p>';
    sum=' · melhor composto: '+esc(res[0].c.n)+' ('+(res[0].p>=10?res[0].p.toFixed(0):res[0].p.toFixed(1)).replace('.',',')+'%)';
  }
  h+='</details>';
  $('#icOut').innerHTML=h;
  ICLAST={x,cl,top:used?res.slice(0,5).filter((r,i)=>i<3||r.p>=1):[],used};icExpShow();
  $('#icSum').innerHTML=(cl.any?'<b>'+cl.ok.length+'</b> de '+IDCLS.length+' classes':'<b>'+used+'</b> critério'+(used>1?'s':''))+sum+' <span class="mut">· ver resultado ↓</span>';
  fontesRecolher($('#icOut'));
}
function icClear(){icReset();if($('#icNome'))$('#icNome').value='';if($('#icObs'))$('#icObs').value='';icDraw();ICLAST=null;icExpShow();$('#icOut').innerHTML='<p class="empty">Marque pelo menos um dado acima.</p>';$('#icSum').textContent='Marque pelo menos um dado.';$('#icBandOut').innerHTML='';icSave();}
function icFill(i){
  const c=COMP[i];icReset();
  icSt.est=c.est.indexOf('líquido')===0?'líquido':'sólido';icSt.g=c.g;
  icSt.cor=[...corFam(c.cor)[0]][0]||'';
  const ce=elCount(c.f);['O','N','S','Cl','Br','I'].forEach(e=>{icSt.el[e]=ce[e]?'sim':'nao';});
  IDIR.forEach(([k])=>{icSt.ir[k]=cIr(c,k)?'sim':'nao';});
  SUBL.forEach(([k])=>{icSt.sub[k]=(c.sub||[]).indexOf(k)>=0?'sim':'nao';});
  if(c.pf!=null&&c.est.indexOf('sólido')===0)$('#icPF').value=c.pf;
  if(c.pe!=null&&c.est.indexOf('líquido')===0)$('#icPE').value=c.pe;
  $('#icIV').value=c.iv.filter(b=>b[4]).map(b=>Math.round((b[0]+b[1])/2)).join(', ');
  $('#icM').value=c.M;
  if(c.ms)$('#icP').value=c.ms.filter(p=>p!==c.M).slice(0,3).join(', ');
  $('#icH').value=c.h1.length;$('#icC').value=c.c13.length;$('#icEx').value=String(i);
  icDraw();icRun();icSave();
}

/* ---------- Identificar: exportar/compartilhar, relatório e análises salvas ---------- */
let ICLAST=null;
function icExpShow(){const e=$('#icExp');if(e)e.hidden=!ICLAST;const m=$('#icExpMsg');if(m)m.textContent='';}
const icPct=r=>(r.p>=10?r.p.toFixed(0):r.p.toFixed(1)).replace('.',',');
/* os dados informados, em grupos (usado pelo texto e pelo relatório) */
const lista=t=>t.replace(/\s*[,;]\s*/g,', ').replace(/\s{2,}/g,' ');
function icDados(){
  const L=ICLAST;if(!L)return [];const x=L.x,v=id=>$(id).value.trim(),G=[];
  const add=(t,it)=>{if(it.length)G.push({t,it});};
  const ap=[];if(x.est)ap.push(['Estado',x.est]);
  if(x.cor){const c=COR.find(k=>k[0]===x.cor);ap.push(['Cor',c?c[1]:x.cor]);}
  add('Aparência',ap);
  add('Solubilidade',x.g?[['Grupo',sx(SOLN[x.g])]]:[]);
  const cf=[];if(v('#icPF'))cf.push(['PF',v('#icPF')+' °C (±'+v('#icTol')+')']);if(v('#icPE'))cf.push(['PE',v('#icPE')+' °C (±'+v('#icTol')+')']);
  add('Constantes físicas',cf);
  add('Análise elementar',x.els.map(([e,u])=>[e,u==='sim'?'presente':'ausente']));
  const iv=[];IDIR.forEach(([k,lab])=>{if(x.ir[k])iv.push([lab.replace(/ \(.*/,''),x.ir[k]==='sim'?'sim':'não']);});
  if(v('#icIV'))iv.push(['Bandas (cm⁻¹)',lista(v('#icIV'))]);
  add('Infravermelho',iv);
  const sb=[];SUBL.forEach(([k,lab])=>{if(x.sub[k])sb.push([lab.replace(/ \(.*/,''),x.sub[k]==='sim'?'sim':'não']);});
  add('Subestrutura',sb);
  const ms=[];if(x.F)ms.push(['Fórmula',x.F]);if(x.gdh!=null)ms.push(['GDH',String(x.gdh)]);
  if(x.M!=null)ms.push(['M',String(x.M)]);if(v('#icP'))ms.push(['Picos de MS (m/z)',lista(v('#icP'))]);
  add('Fórmula e massas',ms);
  const rm=[];if(x.h!=null)rm.push(['Sinais de ¹H',String(x.h)]);if(x.c!=null)rm.push(['Sinais de ¹³C',String(x.c)]);
  if(v('#icHd'))rm.push(['δ de ¹H (ppm)',lista(v('#icHd'))]);
  add('RMN',rm);
  return G;
}
function icNomeObs(){const n=$('#icNome'),o=$('#icObs');return {nome:n?n.value.trim():'',obs:o?o.value.trim():''};}
function icTexto(){
  const L=ICLAST;if(!L)return '';
  const no=icNomeObs(),o=[],linha='────────────────────────';
  o.push('ANAQUIM · Identificação do composto');
  if(no.nome)o.push('Análise: '+no.nome);
  o.push('Data: '+new Date().toLocaleDateString('pt-BR'));
  o.push(linha);o.push('DADOS INFORMADOS');
  const G=icDados();
  if(!G.length)o.push('(nenhum)');
  G.forEach(g=>{o.push('');o.push(g.t);g.it.forEach(([k,val])=>o.push('  '+k+': '+val));});
  if(L.cl.any){o.push('');o.push(linha);o.push('CLASSES QUE SOBRAM ('+L.cl.ok.length+' de '+IDCLS.length+')');
    o.push(L.cl.ok.length?L.cl.ok.map(k=>'  · '+sx(k.c.n)).join('\n'):'  nenhuma');}
  if(L.top.length){o.push('');o.push(linha);o.push('COMPOSTOS MAIS COMPATÍVEIS');
    L.top.forEach((r,i)=>{o.push('');o.push((i+1)+'. '+r.c.n+' · '+icPct(r)+'%');
      o.push('   '+r.c.f+' · CAS '+r.c.cas);
      const nb=r.parts.filter(p=>p.f<0.7).map(p=>p.lab);if(nb.length)o.push('   Não combina bem: '+nb.join(', '));});}
  if(no.obs){o.push('');o.push(linha);o.push('OBSERVAÇÕES');o.push(no.obs);}
  o.push('');o.push(linha);
  o.push('A porcentagem compara os compostos do banco do app; não é uma probabilidade real. Confirme com os espectros e com a literatura.');
  o.push('Feito no Anaquim: https://anaquim.litteraria.com.br');
  return o.join('\n');
}
/* relatório visual: página autônoma, pronta para imprimir ou salvar em PDF */
function icRelatorio(){
  const L=ICLAST;if(!L)return '';
  const no=icNomeObs(),cs=getComputedStyle(document.documentElement);
  const cor=(cs.getPropertyValue('--keep')||'#1F5FA8').trim(),hoje=new Date().toLocaleDateString('pt-BR');
  const G=icDados();
  let b='';
  b+='<header><div class="mk">Anaquim</div><h1>'+esc(no.nome||'Identificação do composto')+'</h1><p class="sub">'+(no.nome?'Identificação do composto · ':'')+hoje+'</p></header>';
  b+='<section><h2>Dados informados</h2>';
  b+=G.length?'<div class="grid">'+G.map(g=>'<div class="card"><h3>'+esc(g.t)+'</h3><dl>'+g.it.map(([k,val])=>'<div><dt>'+esc(k)+'</dt><dd>'+esc(val)+'</dd></div>').join('')+'</dl></div>').join('')+'</div>':'<p class="mut">Nenhum dado informado.</p>';
  b+='</section>';
  if(L.cl.any){b+='<section><h2>Classes que sobram <span class="mut">('+L.cl.ok.length+' de '+IDCLS.length+')</span></h2>';
    b+=L.cl.ok.length?'<div class="pills">'+L.cl.ok.map(k=>'<span class="pill">'+esc(sx(k.c.n))+'</span>').join('')+'</div>':'<p class="mut">Nenhuma classe da lista combina com tudo.</p>';b+='</section>';}
  if(L.top.length){b+='<section><h2>Compostos mais compatíveis</h2>';
    L.top.forEach((r,i)=>{
      const nb=r.parts.filter(p=>p.det&&p.f<0.7).map(p=>'<b>'+esc(p.lab)+':</b> '+esc(p.det.indexOf(p.lab+' ')===0?p.det.slice(p.lab.length+1):p.det)).join(' · ');
      b+='<article class="res"><div class="rt"><span class="n">'+(i+1)+'</span><div class="nm"><b>'+esc(r.c.n)+'</b><span class="mut">'+fmt(r.c.f)+' · CAS '+esc(r.c.cas)+'</span></div><span class="pc">'+icPct(r)+'%</span></div>'
        +'<div class="bar"><i style="width:'+Math.max(2,Math.min(100,r.p)).toFixed(1)+'%"></i></div>'
        +'<div class="cr"><span class="ok">✓ '+r.parts.filter(p=>p.f>=0.7).length+' de '+r.parts.length+' critérios combinam</span>'+r.parts.filter(p=>p.f<0.7).map(p=>'<span class="'+(p.f>=0.2?'md':'no')+'">'+(p.f>=0.2?'~ ':'✗ ')+esc(p.lab)+'</span>').join('')+'</div>'
        +(nb?'<p class="det">'+nb+'</p>':'')+'</article>';});
    b+='<p class="leg">✓ combina · ~ combina em parte · ✗ não combina</p></section>';}
  if(no.obs)b+='<section><h2>Observações</h2><p class="obs">'+esc(no.obs).replace(/\n/g,'<br>')+'</p></section>';
  b+='<footer><p>A porcentagem compara os compostos do banco do app e não é uma probabilidade real. Se o composto não está na lista, o app mostra só o mais parecido. Confirme com os espectros e com a literatura.</p><p>Feito no Anaquim · anaquim.litteraria.com.br</p></footer>';
  b+='<button class="imp" onclick="window.print()">Imprimir ou salvar em PDF</button>';
  const css=':root{--c:'+cor+'}*{box-sizing:border-box}body{margin:0;background:#EEF1F4;color:#15202B;font:15px/1.5 "IBM Plex Sans",system-ui,-apple-system,"Segoe UI",sans-serif}'
   +'.pg{max-width:780px;margin:0 auto;background:#fff;padding:0 0 28px}'
   +'header{background:var(--c);color:#fff;padding:26px 28px 22px}.mk{font-size:.78rem;letter-spacing:.14em;text-transform:uppercase;opacity:.85;font-weight:600}'
   +'h1{margin:6px 0 2px;font-size:1.65rem;line-height:1.2}.sub{margin:0;opacity:.9;font-size:.92rem}'
   +'section{padding:22px 28px 0}h2{font-size:1.05rem;margin:0 0 12px;padding-bottom:6px;border-bottom:2px solid var(--c)}h3{margin:0 0 6px;font-size:.74rem;letter-spacing:.07em;text-transform:uppercase;color:var(--c)}'
   +'.mut{color:#5B6877;font-weight:400}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:10px}'
   +'.card{border:1px solid #D9E0E7;border-radius:10px;padding:10px 12px;break-inside:avoid}dl{margin:0}dl div{display:flex;justify-content:space-between;gap:10px;padding:4px 0;border-bottom:1px solid #EDF1F5;min-width:0}dl div:last-child{border:0}dt{color:#5B6877}dd{margin:0;font-weight:600;text-align:right;min-width:0;overflow-wrap:anywhere}dt{flex:none;max-width:45%}'
   +'.pills{display:flex;flex-wrap:wrap;gap:6px}.pill{background:#EEF3F8;border:1px solid #D4DEE9;border-radius:99px;padding:3px 11px;font-size:.88rem}'
   +'.res{border:1px solid #D9E0E7;border-radius:12px;padding:12px 14px;margin:0 0 10px;break-inside:avoid}.rt{display:flex;align-items:center;gap:10px}'
   +'.n{flex:none;width:28px;height:28px;border-radius:50%;background:var(--c);color:#fff;display:grid;place-items:center;font-weight:700;font-size:.9rem}'
   +'.nm{flex:1;min-width:0}.nm b{display:block;font-size:1.05rem}.nm span{font-size:.86rem}.pc{font-size:1.3rem;font-weight:700;color:var(--c)}'
   +'.bar{height:8px;border-radius:99px;background:#E4EAF0;margin:9px 0}.bar i{display:block;height:100%;background:var(--c);border-radius:99px}'
   +'.cr{display:flex;flex-wrap:wrap;gap:5px}.cr span{font-size:.78rem;border-radius:6px;padding:2px 8px;background:#EEF1F4;color:#4B5866}.cr .ok{background:#DDF1E6;color:#17613B}.cr .md{background:#FBF0CF;color:#7A5A00}.cr .no{background:#F7E3DE;color:#9A2F20}'
   +'.det{font-size:.86rem;color:#5B6877;margin:8px 0 0}.leg{font-size:.8rem;color:#5B6877;margin:4px 0 0}.obs{margin:0;padding:10px 12px;background:#FBF6E4;border-radius:10px}'
   +'footer{padding:20px 28px 0;font-size:.8rem;color:#5B6877}footer p{margin:0 0 4px}'
   +'.imp{display:block;margin:20px auto 0;font:inherit;font-weight:600;background:var(--c);color:#fff;border:0;border-radius:10px;padding:11px 20px;cursor:pointer}'
   +'@media print{body{background:#fff}.pg{max-width:none}.imp{display:none}header{-webkit-print-color-adjust:exact;print-color-adjust:exact}.n,.bar i,.cr span{-webkit-print-color-adjust:exact;print-color-adjust:exact}}';
  return '<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+esc((no.nome||'Identificação do composto')+' · Anaquim')+'</title><style>'+css+'</style></head><body><div class="pg">'+b+'</div></body></html>';
}
function icMsg(t){const m=$('#icExpMsg');if(m)m.textContent=t;}
async function icCopiar(){
  const t=icTexto();if(!t)return;
  try{await navigator.clipboard.writeText(t);icMsg('Resultado copiado.');}
  catch(e){const a=document.createElement('textarea');a.value=t;a.setAttribute('readonly','');a.style.cssText='position:fixed;opacity:0';document.body.appendChild(a);a.select();
    try{document.execCommand('copy');icMsg('Resultado copiado.');}catch(e2){icMsg('Não consegui copiar. Use "Baixar".');}a.remove();}
}
async function icCompartilhar(){
  const t=icTexto();if(!t)return;
  if(navigator.share){try{await navigator.share({title:'Identificação do composto (Anaquim)',text:t});return;}catch(e){if(e&&e.name==='AbortError')return;}}
  icCopiar();icMsg('Este aparelho não abre o menu de compartilhar. O resultado foi copiado.');
}
function icBaixarArq(conteudo,tipo,nome){
  const b=new Blob([conteudo],{type:tipo}),u=URL.createObjectURL(b),a=document.createElement('a');
  a.href=u;a.download=nome;document.body.appendChild(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(u),1500);
}
function icBaixar(){
  const t=icTexto();if(!t)return;
  icBaixarArq(t+'\n','text/plain;charset=utf-8','identificacao-anaquim.txt');
  icMsg('Arquivo baixado.');
}
function icRel(){
  const h=icRelatorio();if(!h)return;
  const b=new Blob([h],{type:'text/html;charset=utf-8'}),u=URL.createObjectURL(b),w=window.open(u,'_blank');
  if(!w){icBaixarArq(h,'text/html;charset=utf-8','relatorio-anaquim.html');icMsg('O navegador bloqueou a janela. Baixei o relatório: abra o arquivo e use Imprimir para gerar o PDF.');}
  else icMsg('Relatório aberto. Toque em "Imprimir ou salvar em PDF".');
  setTimeout(()=>URL.revokeObjectURL(u),60000);
}

/* ---------- Análises salvas (ficam neste aparelho; entram no código de "Salvar e levar o progresso") ---------- */
const AN_KEY='massas-an';
function anGet(){const a=LS.get(AN_KEY,[]);return Array.isArray(a)?a:[];}
function anFmtData(t){try{return new Date(t).toLocaleDateString('pt-BR')+' '+new Date(t).toLocaleTimeString('pt-BR',{hour:'2-digit',minute:'2-digit'});}catch(e){return '';}}
function anMsg(t,bad){const m=$('#icSavMsg');if(!m)return;m.textContent=t;m.className='hint fb '+(bad?'bad':'good');}
function anSalvar(){
  if(!ICLAST){anMsg('Preencha pelo menos um dado antes de salvar.',true);return;}
  const f={};IC_CAMPOS.forEach(i=>f[i]=$(i).value);
  const no=icNomeObs(),L=ICLAST,t=Date.now();
  const a=anGet();
  const nome=no.nome||('Análise de '+new Date(t).toLocaleDateString('pt-BR'));
  a.unshift({id:'a'+t.toString(36)+Math.random().toString(36).slice(2,5),t,n:nome,o:no.obs,st:JSON.parse(JSON.stringify(icSt)),f,
    top:L.top.slice(0,3).map(r=>({n:r.c.n,p:+r.p.toFixed(1)})),k:L.cl.any?L.cl.ok.length:null});
  LS.set(AN_KEY,a.slice(0,80));
  if($('#icNome'))$('#icNome').value='';if($('#icObs'))$('#icObs').value='';
  anDesenha();anMsg('Análise salva neste aparelho: '+nome+'.');
  const d=$('#icSaved');if(d)d.open=true;
}
function anDesenha(){
  const a=anGet(),L=$('#icSavL'),n=$('#icSavN');if(!L)return;
  if(n)n.textContent=a.length;
  L.innerHTML=a.length?a.map(x=>'<div class="ansv" data-id="'+esc(x.id)+'"><div class="ansh"><b>'+esc(x.n)+'</b><span class="mut">'+esc(anFmtData(x.t))+'</span></div>'
    +'<p class="mut ansr">'+(x.top&&x.top.length?'Melhor: '+esc(x.top[0].n)+' ('+String(x.top[0].p).replace('.',',')+'%)':(x.k!=null?x.k+' classes sobram':'sem ranking'))+'</p>'
    +(x.o?'<p class="ansn">'+esc(x.o)+'</p>':'')
    +'<div class="row"><button class="btn" type="button" data-an="abrir">Abrir</button><button class="btn ghost" type="button" data-an="del">Excluir</button></div></div>').join(''):'<p class="empty">Nenhuma análise salva ainda.</p>';
}
function anAbrir(id){
  const x=anGet().find(k=>k.id===id);if(!x)return;
  icReset();
  icSt={est:x.st.est||'',cor:x.st.cor||'',g:x.st.g||'',el:x.st.el||{},ir:x.st.ir||{},sub:x.st.sub||{}};
  IC_CAMPOS.forEach(i=>{if(x.f&&x.f[i]!=null)$(i).value=x.f[i];});
  if($('#icNome'))$('#icNome').value=x.n;if($('#icObs'))$('#icObs').value=x.o||'';
  icDraw();icRun();icSave();
  anMsg('Análise aberta: '+x.n+'. O resultado foi recalculado com o banco atual do app.');
  const r=$('#icResT');if(r&&r.scrollIntoView)r.scrollIntoView({behavior:'smooth',block:'start'});
}
function anExportar(){
  const a=anGet();if(!a.length){anMsg('Não há análises salvas para exportar.',true);return;}
  icBaixarArq(JSON.stringify({anaquim:'analises',v:1,a},null,1),'application/json','analises-anaquim.json');
  anMsg('Arquivo analises-anaquim.json baixado.');
}
function anJuntar(inc){
  const cur=anGet(),ids=new Set(cur.map(x=>x.id));let n=0;
  (Array.isArray(inc)?inc:[]).forEach(x=>{if(x&&x.id&&x.st&&x.f&&!ids.has(x.id)){cur.push(x);ids.add(x.id);n++;}});
  cur.sort((p,q)=>q.t-p.t);LS.set(AN_KEY,cur.slice(0,80));return n;
}
function anImportar(file){
  const r=new FileReader();
  r.onload=()=>{let o;try{o=JSON.parse(r.result);}catch(e){anMsg('Arquivo inválido.',true);return;}
    if(!o||o.anaquim!=='analises'){anMsg('Esse arquivo não é de análises do Anaquim.',true);return;}
    const n=anJuntar(o.a);anDesenha();anMsg(n+' análise'+(n===1?'':'s')+' importada'+(n===1?'':'s')+'. Nada foi apagado.');};
  r.readAsText(file);
}
function anInit(){
  const P=$('#icSaved');if(!P)return;
  $('#icSalvar').onclick=anSalvar;$('#icRel').onclick=icRel;
  $('#icSavExp').onclick=anExportar;
  $('#icSavImp').onclick=()=>$('#icSavFile').click();
  $('#icSavFile').onchange=e=>{if(e.target.files[0])anImportar(e.target.files[0]);e.target.value='';};
  $('#icSavL').addEventListener('click',ev=>{
    const b=ev.target.closest('[data-an]');if(!b)return;
    const id=b.closest('.ansv').dataset.id;
    if(b.dataset.an==='abrir'){anAbrir(id);return;}
    if(b.dataset.an==='del'){
      if(b.dataset.ok!=='1'){b.dataset.ok='1';b.textContent='Confirmar exclusão';setTimeout(()=>{if(b.isConnected){b.dataset.ok='';b.textContent='Excluir';}},4000);return;}
      LS.set(AN_KEY,anGet().filter(k=>k.id!==id));anDesenha();anMsg('Análise excluída.');
    }
  });
  anDesenha();
}
/* quais compostos têm um sinal: tolerância própria de cada técnica */
function icSinRun(){
  const t=$('#icSinT').value,raw=$('#icSinV').value.trim(),o=$('#icSinO');
  const ph={iv:'ex.: 1715',h:'ex.: 7,3',c:'ex.: 128',ms:'ex.: 105'};$('#icSinV').placeholder=ph[t];
  const n=nums(raw);if(!n.length){o.innerHTML='';return;}
  const v=n[0],tol={iv:20,h:0.3,c:5,ms:0.5}[t];
  const hit=[];
  COMP.forEach(c=>{
    let d=null;
    if(t==='iv'){const b=c.iv.find(b=>{const r=ivr(b);return v>=r[0]-tol&&v<=r[1]+tol;});if(b)d=b[2].split(' (')[0]+(b[4]?' (banda-chave)':'');}
    else if(t==='h'){const s=c.h1.find(s=>v>=s.lo-tol&&v<=s.hi+tol);if(s)d=s.t+', '+s.lo+' a '+s.hi+' ppm';}
    else if(t==='c'){const s=c.c13.find(s=>v>=s.lo-tol&&v<=s.hi+tol);if(s)d=s.t+', '+s.lo+' a '+s.hi+' ppm';}
    else if(c.ms&&c.ms.some(p=>Math.abs(p-v)<=tol))d=(c.ms.indexOf(v)===0||Math.round(v)===c.M)?'íon molecular':'pico no espectro do banco';
    if(d)hit.push([c,d]);
  });
  const un={iv:' cm⁻¹ (±20)',h:' ppm (±0,3)',c:' ppm (±5)',ms:' (±0,5)'}[t];
  o.innerHTML='<p class="hint"><b>'+hit.length+'</b> de '+COMP.length+' compostos com sinal em '+String(v).replace('.',',')+un+'.</p>'
    +hit.slice(0,40).map(([c,d])=>'<p style="margin:4px 0"><button class="back" style="margin:0" type="button" data-cf="'+c.i+'">'+esc(c.n)+'</button> <span class="hint">'+esc(d)+'</span></p>').join('')
    +(hit.length>40?'<p class="hint">Mostrando 40. Acrescente outros dados na conta acima para afunilar.</p>':'')
    +'<p class="hint">As faixas são as esperadas pelo grupo funcional, não o espectro medido. Vários grupos caem na mesma região.</p>';
}

function icInit(){
  [...new Set(COMP.flatMap(c=>c.gf))].sort((a,b)=>a.localeCompare(b,'pt')).forEach(g=>{const o=document.createElement('option');o.value=g;o.textContent=g;$('#icGF').appendChild(o);});
  icLoad();icDraw();
  const P=$('#p-ic');
  P.addEventListener('click',ev=>{
    const c=ev.target.closest('[data-ck]');
    if(c){icSt[c.dataset.ck]=c.dataset.cv;icDraw();const e=P.querySelector('[data-ck="'+c.dataset.ck+'"][data-cv="'+c.dataset.cv+'"]');if(e)e.focus({preventScroll:true});icRun();icSave();return;}
    const t=ev.target.closest('[data-tk]');
    if(t){const m=icSt[t.dataset.tk];if(t.dataset.tv)m[t.dataset.ti]=t.dataset.tv;else delete m[t.dataset.ti];icDraw();const e=P.querySelector('[data-tk="'+t.dataset.tk+'"][data-ti="'+t.dataset.ti+'"][data-tv="'+t.dataset.tv+'"]');if(e)e.focus({preventScroll:true});icRun();icSave();}
  });
  P.addEventListener('input',icQueue);P.addEventListener('change',e=>{if(e.target.id==='icEx'){if(e.target.value!=='')icFill(+e.target.value);return;}icQueue();});
  $('#icClr').onclick=icClear;
  $('#icCopy').onclick=icCopiar;$('#icShare').onclick=icCompartilhar;$('#icDown').onclick=icBaixar;anInit();
  $('#icSinT').onchange=icSinRun;$('#icSinV').oninput=icSinRun;
  $('#icSum').onclick=()=>{const r=$('#icResT');if(r)r.scrollIntoView({behavior:'smooth',block:'start'});};
  icRun();
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
