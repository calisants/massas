s=open('template.html').read()
def rep(a,b,cnt=1):
    global s
    assert s.count(a)==cnt,(s.count(a),a[:90])
    s=s.replace(a,b)
# limite diário de revisão
rep("function repDue(){","""const REV_MAX=10;
function diaKey(){const d=new Date();return d.getFullYear()+'-'+(d.getMonth()+1)+'-'+d.getDate();}
function revFeitas(){const r=LS.get('massas-revdia',null);return r&&r.d===diaKey()?r.n:0;}
function revCount(){LS.set('massas-revdia',{d:diaKey(),n:revFeitas()+1});}
function repAvail(){return Math.max(0,Math.min(repDue(),REV_MAX-revFeitas()));}
function repDue(){""")
rep("if(TR.mode==='rev'){const rp=repGet(),now=Date.now();return all.filter(x=>{const o=rp[x.e.n+':'+x.r[0]];return o&&(TR.revAll||o.d<=now);});}",
    "if(TR.mode==='rev'){const rp=repGet(),now=Date.now();let l=all.filter(x=>{const o=rp[x.e.n+':'+x.r[0]];return o&&(TR.revAll||o.d<=now);});if(!TR.revAll){l.sort((a,b)=>rp[a.e.n+':'+a.r[0]].d-rp[b.e.n+':'+b.r[0]].d);l=l.slice(0,Math.max(0,REV_MAX-revFeitas()));}return l;}")
rep("rb.textContent='Revisar ('+repDue()+' hoje)';}","rb.textContent='Revisar ('+repAvail()+' hoje)';}")
rep("if(c.wrong)repAdd(key);else repOk(key);trLabel();}","if(c.wrong)repAdd(key);else repOk(key);if(TR.mode==='rev'&&!TR.revAll)revCount();trLabel();}")
rep("box.innerHTML=n?'<p class=\"empty\">Nenhuma revisão vencida hoje. Você tem '+n+' guardada(s): cada erro volta 1, 3 e 7 dias depois, e sai da lista quando você acerta nas três.</p>",
    "box.innerHTML=n?'<p class=\"empty\">'+(revFeitas()>=REV_MAX&&repDue()>0?'Você já revisou '+REV_MAX+' hoje. O resto fica para amanhã, para não pesar.':'Nenhuma revisão vencida hoje.')+' Você tem '+n+' guardada(s): cada erro volta 1, 3 e 7 dias depois, e sai da lista quando você acerta nas três.</p>")
# Hoje
rep('    <h2 class="scr">Analisar</h2>\n','    <h2 class="scr">Analisar</h2>\n    <div class="rule" id="hoje"></div>\n')
rep("function anStage(r){$('#an-in').hidden=r;$('#an-res').hidden=!r;window.scrollTo(0,0);}","function anStage(r){$('#an-in').hidden=r;$('#an-res').hidden=!r;window.scrollTo(0,0);if(!r)drawHoje();}")
rep("/* ---------- Elétron: de onde sai? ---------- */","""/* ---------- Hoje ---------- */
const ORD=[6,9,5,10,12,11,4,1,3,8,7,2];
function drawHoje(){
  const box=$('#hoje');if(!box)return;
  const due=repAvail(),next=ORD.find(n=>!isStud(n)),st=LS.get('massas-stud',[]),last=st.length?st[st.length-1]:null;
  let h='<h3>Hoje: 3 passos curtos</h3><ol class="hoje">';
  h+='<li>'+(due?'<button class="btn" data-hj="rev" type="button">Revisar '+due+'</button> erros que voltaram hoje (no máximo '+REV_MAX+' por dia).':'Revisão: nada vencido hoje.')+'</li>';
  h+='<li>'+(next?'<button class="btn" data-hj="ex" data-n="'+next+'" type="button">Estudar o Ex. '+next+'</button> '+esc(EX.find(e=>e.n===next).nome)+'. Marque como estudado no fim.':'Todos os exercícios estão marcados como estudados.')+'</li>';
  h+='<li>'+(last?'<button class="btn ghost" data-hj="sim" data-n="'+last+'" type="button">Simulado do Ex. '+last+'</button> o último que você estudou, sem consultar.':'O simulado aparece depois que você marcar um exercício como estudado.')+'</li></ol>';
  box.innerHTML=h;
}
document.addEventListener('click',ev=>{
  const b=ev.target.closest('[data-hj]');if(!b)return;const k=b.dataset.hj,n=+b.dataset.n;
  if(k==='rev'){TR.mode='rev';TR.revAll=false;go('p-tr');}
  else if(k==='ex'){const e=EX.find(x=>x.n===n);curEx=n;pkSel=null;$('#inM').value=e.M;$('#inP').value=e.peaks.filter(p=>p!==e.M).join(', ');buildChips();analyze();anStage(true);}
  else if(k==='sim'){TR.mode='sm';go('p-tr');$('#smsel').value=String(n);$('#smmod').value='1';$('#smgo').click();}
});

/* ---------- Elétron: de onde sai? ---------- */""")
rep(".resumo{margin:10px 0 4px;font-weight:500}",".resumo{margin:10px 0 4px;font-weight:500}\n.hoje{padding-left:20px;margin:6px 0}.hoje li{margin:10px 0}.hoje .btn{margin-right:6px}")
rep("function pgCollect(){const d={};try{for(let i=0;i<localStorage.length;i++){const k=localStorage.key(i);if(k&&k.indexOf('massas-')===0)d[k]","function pgCollect(){const d={};try{for(let i=0;i<localStorage.length;i++){const k=localStorage.key(i);if(k&&k.indexOf('massas-')===0&&k!=='massas-revdia')d[k]")
rep("buildChips();analyze();drawTable();calc();","buildChips();analyze();drawHoje();drawTable();calc();")
open('template.html','w').write(s);print('ok')
