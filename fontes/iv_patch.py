import json
p='template.html'; s=open(p,encoding='utf-8').read()
def rep(a,b):
    global s
    assert a in s,a[:60]; s=s.replace(a,b,1)

A,M_,B='alta','média','baixa'
IR=[
 dict(n=1,pista='Sem C=O (nada em 1850–1650) e sem O–H/N–H (nada em 3600–3200). Tem anel aromático e C–H alifático. No MS isso favorece a quebra benzílica (91).',p=[
  ['3100–3000','C–H sp² do anel aromático',A],['2967','C–H sp³ (CH3)',A],['2950','C–H sp³',A],['2930','C–H sp³ (CH2)',A],['2870','C–H sp³ (CH3)',A],
  ['1600','C=C do anel aromático',A],['1450','C=C do anel e deformação de CH2/CH3 (sobrepostas)',M_],['1390','deformação de CH3',M_],
  ['750','C–H fora do plano, benzeno monossubstituído',A],['700','C–H fora do plano, benzeno monossubstituído',A]]),
 dict(n=2,pista='Sem C=O e sem O–H. As bandas são de anel aromático com O (furano). No MS o anel abre ao lado do O e perde CO ou CHO.',p=[
  ['3160','C–H sp² do anel (carbono ao lado do O)',A],['3121','C–H sp² do anel',A],['1592','C=C do anel',M_],['1485','C=C do anel',A],
  ['1172','banda do anel (C–H no plano)',B],['1061','C–O–C do anel',M_],['869','banda do anel',B],['749','C–H fora do plano',M_],['602','deformação do anel',B]]),
 dict(n=3,pista='Sem C=O e sem O–H. A banda em 1630 e as de 992/909 mostram o grupo vinila (C=C–H) ligado ao anel. No MS a vinila sai como acetileno (26).',p=[
  ['3082','C–H sp² aromático',A],['3060','C–H sp² aromático',A],['3027','C–H sp² aromático',A],['3009','C–H sp² da vinila (=CH)',M_],
  ['2980','sem atribuição segura (possível harmônico ou ombro)',B],['1630','C=C da vinila (CH=CH2)',A],['1495','C=C do anel',A],['1449','C=C do anel',A],
  ['992','=C–H fora do plano, vinila monossubstituída',A],['909','=CH2 fora do plano, vinila monossubstituída',A],['777','C–H fora do plano, anel monossubstituído',A],['698','C–H fora do plano, anel monossubstituído',A]]),
 dict(n=4,pista='C=O em 1666: abaixo de 1700 porque está conjugado com anéis (cetona aromática). Sem O–H. No MS a clivagem α dá o íon benzoíla (105).',p=[
  ['3088','C–H sp² aromático',A],['3067','C–H sp² aromático',A],['3030','C–H sp² aromático',A],['3003','C–H sp² aromático',A],
  ['1666','C=O de cetona aromática (conjugada)',A],['1595','C=C do anel',A],['1577','C=C do anel',A],['1449','C=C do anel',M_],
  ['1281','C–C(=O)–C da cetona aromática',M_],['705','C–H fora do plano, anel monossubstituído',M_],['697','C–H fora do plano, anel monossubstituído',M_]]),
 dict(n=5,pista='C=O em 1720 (cetona saturada). Sem C–H de aldeído (nada perto de 2720) e sem O–H. No MS: clivagem α dos dois lados do C=O dá o íon propanoíla (57).',p=[
  ['2981','C–H sp³',A],['2940','C–H sp³',A],['2908','C–H sp³',A],['2883','C–H sp³',A],['1720','C=O de cetona saturada',A],
  ['1460','deformação de CH2/CH3',A],['1414','deformação do CH2 vizinho ao C=O',M_],['1379','deformação de CH3',A],['1366','deformação de CH3',M_],['1121','C–C(=O)–C da cetona',M_]]),
 dict(n=6,pista='Banda larga de O–H em 3350 e C–O em 1054: álcool primário. Sem C=O. No MS: perde H2O (18) e faz clivagem α (31).',p=[
  ['3350','O–H de álcool (larga, ligação de hidrogênio)',A],['3340','O–H de álcool (a mesma banda larga)',A],['2964','C–H sp³',A],['2937','C–H sp³',A],['2878','C–H sp³',A],
  ['1465','deformação de CH2/CH3',A],['1387','deformação de CH3',M_],['1054','C–O de álcool primário',A],
  ['661','sem atribuição segura',B],['655','sem atribuição segura',B]]),
 dict(n=7,pista='Só C–H sp³ e uma banda forte de C–O–C em 1124 (éter). Sem C=O e sem O–H. No MS o anel perde CH2=O duas vezes (88 → 58 → 28).',p=[
  ['2963','C–H sp³ (CH2)',A],['2914','C–H sp³ (CH2)',A],['2869','C–H sp³ (CH2)',A],['2866','C–H sp³ (CH2)',A],['1453','deformação de CH2',A],['1124','C–O–C de éter',A]]),
 dict(n=8,pista='Sem C=O e sem O–H. Anel aromático com N (piridina). No MS o anel perde HCN (27).',p=[
  ['3079','C–H sp² do anel',A],['3055','C–H sp² do anel',A],['3026','C–H sp² do anel',A],['1600','C=C/C=N do anel',A],['1581','C=C/C=N do anel',A],['1482','C=C/C=N do anel',A],['1438','C=C/C=N do anel',A],
  ['748','C–H fora do plano',M_],['704','C–H fora do plano / deformação do anel',M_]]),
 dict(n=9,pista='Banda larguíssima de 3100 a 2500 (O–H de ácido) e C=O em 1712: ácido carboxílico. No MS: perde OH (71) e faz McLafferty (60).',p=[
  ['3100–2500','O–H de ácido carboxílico (muito larga, dímero)',A],['2971','C–H sp³ (sobre a banda larga)',A],['2940','C–H sp³',A],['2880','C–H sp³',A],
  ['2681','ombro da banda O–H do dímero',M_],['1712','C=O de ácido carboxílico (dímero)',A],['1451','deformação de CH2/CH3',M_],['1415','deformação do CH2 vizinho ao C=O / O–H no plano',M_],
  ['1285','C–O de ácido',M_],['937','O–H fora do plano (dímero, larga)',A]]),
 dict(n=10,pista='Sem N–H (nada em 3500–3300): é amina terciária. As bandas 2817–2768 são C–H ligados ao N. No MS: clivagem α, perde CH3 e dá o íon imínio (58).',p=[
  ['2974','C–H sp³',A],['2946','C–H sp³',A],['2907','C–H sp³',A],['2879','C–H sp³',A],
  ['2817','C–H ligado ao N (2820–2760)',M_],['2786','C–H ligado ao N (2820–2760)',M_],['2768','C–H ligado ao N (2820–2760)',M_],
  ['1452','deformação de CH2/CH3',A],['1383','deformação de CH3',M_],['1086','C–N de amina alifática',M_],['788','sem atribuição segura',B]]),
 dict(n=12,pista='C=O em 1727 e C–H de aldeído em 2719: aldeído saturado. No MS: McLafferty dá 44.',p=[
  ['2960','C–H sp³',A],['2935','C–H sp³',A],['2876','C–H sp³',A],['2719','C–H de aldeído (CHO)',A],['1727','C=O de aldeído saturado',A],
  ['1467','deformação de CH2/CH3',A],['1412','deformação do CH2 vizinho ao C=O',M_],['1390','deformação de CH3',M_],['1108','sem atribuição segura',B],['741','sem atribuição segura (balanço de CH2?)',B]]),
]
IRT=[
 [3600,3200,'O–H de álcool ou fenol','larga e forte (ligação de hidrogênio); livre fica perto de 3600, estreita'],
 [3500,3300,'N–H de amina ou amida','amina primária: 2 bandas; secundária: 1 banda; terciária: nenhuma'],
 [3300,2500,'O–H de ácido carboxílico','muito larga, cobre as bandas de C–H'],
 [3320,3270,'≡C–H de alcino terminal','estreita e forte'],
 [3100,3000,'C–H sp² (aromático ou alqueno)','fraca a média, acima de 3000'],
 [3000,2850,'C–H sp³','forte, abaixo de 3000'],
 [2830,2695,'C–H de aldeído','duas bandas, perto de 2820 e 2720'],
 [2820,2760,'C–H ligado ao N (amina)','banda de amina com C–H vizinho ao par de elétrons do N'],
 [2260,2210,'C≡N de nitrila','média, estreita'],
 [2260,2100,'C≡C de alcino','fraca'],
 [1750,1735,'C=O de éster','forte'],
 [1740,1720,'C=O de aldeído saturado','forte'],
 [1725,1705,'C=O de cetona saturada','forte'],
 [1725,1700,'C=O de ácido carboxílico','forte (dímero perto de 1710)'],
 [1700,1660,'C=O conjugado (cetona aromática ~1685–1666)','forte; conjugação baixa a frequência'],
 [1680,1620,'C=C de alqueno','fraca a média; vinila perto de 1640–1630'],
 [1600,1450,'C=C do anel aromático','bandas em ~1600, 1585, 1500 e 1450'],
 [1470,1450,'deformação de CH2/CH3',''],
 [1385,1365,'deformação de CH3','perto de 1380'],
 [1320,1210,'C–O de ácido ou éster','forte'],
 [1300,1000,'C–O de álcool ou éter','forte; álcool primário ~1050, éter alifático ~1150–1085'],
 [1250,1020,'C–N de amina alifática','média a fraca'],
 [1000,985,'=C–H fora do plano, vinila','junto com uma banda em ~910'],
 [915,905,'=CH2 fora do plano, vinila','junto com uma banda em ~990'],
 [950,910,'O–H fora do plano, ácido','larga'],
 [770,730,'C–H fora do plano, anel monossubstituído','junto com uma banda em ~700'],
 [710,690,'C–H fora do plano, anel monossubstituído','junto com uma banda em ~750'],
]
js="const IR="+json.dumps(IR,ensure_ascii=False)+";\nconst IRT="+json.dumps(IRT,ensure_ascii=False)+";\n"
js+="""
/* ---------- aba IV ---------- */
let ivEx=null;
function ivNums(t){const m=String(t).match(/\\d+/g)||[];return m.map(Number);}
function drawIVChips(){const box=$('#ivchips');box.innerHTML='';
  IR.forEach(c=>{const e=EX.find(x=>x.n===c.n);const b=document.createElement('button');b.type='button';b.className='chip';b.setAttribute('aria-pressed',ivEx===c.n?'true':'false');b.textContent='Ex. '+c.n+' '+e.nome;b.onclick=()=>{ivEx=c.n;drawIVChips();drawIV();};box.appendChild(b);});}
function drawIV(){
  const c=IR.find(x=>x.n===ivEx),box=$('#ivout');
  if(!c){box.innerHTML='<p class="empty">Escolha um exercício acima para ver as bandas dele.</p>';return;}
  const e=EX.find(x=>x.n===c.n);
  box.innerHTML='<div class="ex-head"><b>Ex. '+e.n+': '+esc(e.nome)+'</b><span class="mono">'+fmt(e.f)+'</span><span>'+esc(e.g)+'</span></div>'+
   '<div class="ans" style="border-radius:6px;margin-bottom:12px"><span class="t">Pista do IV para o espectro de massas</span>'+esc(c.pista)+'</div>'+
   '<div class="tbl"><table><thead><tr><th>Banda (cm⁻¹)</th><th>O que é</th><th>Confiança</th></tr></thead><tbody>'+
   c.p.map(r=>'<tr><td class="n">'+r[0]+'</td><td>'+esc(r[1])+'</td><td><span class="badge '+(r[2]==='baixa'?'chk':'ok')+'">'+r[2]+'</span></td></tr>').join('')+'</tbody></table></div>';
}
function ivLookup(){
  const v=parseInt($('#ivq').value,10),box=$('#ivres');
  if(!v){box.innerHTML='';return;}
  const hits=IRT.filter(r=>v<=r[0]&&v>=r[1]);
  const mine=[];IR.forEach(c=>c.p.forEach(r=>{const n=ivNums(r[0]);const lo=Math.min(...n),hi=Math.max(...n);if(v>=lo-8&&v<=hi+8)mine.push('Ex. '+c.n+' ('+r[0]+')');}));
  box.innerHTML=(hits.length?'<div class="tbl"><table><thead><tr><th>Faixa</th><th>Grupo</th><th>Aspecto</th></tr></thead><tbody>'+hits.map(r=>'<tr><td class="n">'+r[1]+'–'+r[0]+'</td><td>'+esc(r[2])+'</td><td>'+esc(r[3])+'</td></tr>').join('')+'</tbody></table></div>':'<p class="empty">Nenhuma faixa da tabela cobre '+v+' cm⁻¹. Pode estar na região de impressão digital (abaixo de 1000), que quase nunca se atribui.</p>')+
   (mine.length?'<p class="hint" style="margin-top:8px">Nos seus exercícios (±8 cm⁻¹): '+mine.map(x=>'<span class="xr">'+x+'</span>').join('')+'</p>':'');
}
"""
rep("/* ---------- abas ---------- */",js+"\n/* ---------- abas ---------- */")
rep("const tabs=[['t-an','p-an'],['t-tr','p-tr'],['t-tb','p-tb'],['t-ca','p-ca']];","const tabs=[['t-an','p-an'],['t-tr','p-tr'],['t-tb','p-tb'],['t-iv','p-iv'],['t-ca','p-ca']];")
rep("""    <button class="tab" role="tab" id="t-ca\"""","""    <button class="tab" role="tab" id="t-iv" aria-selected="false" aria-controls="p-iv">IV</button>
    <button class="tab" role="tab" id="t-ca\"""")
rep("""  <section id="p-ca\"""","""  <section id="p-iv" role="tabpanel" aria-labelledby="t-iv" hidden>
    <div class="how">
      <b>Como ler um espectro de IV</b>
      <ol>
        <li><b>Olhe 1850–1650.</b> Tem banda forte? É C=O. A posição diz o tipo (aldeído, cetona, ácido, éster).</li>
        <li><b>Olhe 3600–3200.</b> Banda larga é O–H; uma ou duas bandas mais finas são N–H. Se não tem nada, não há O–H nem N–H.</li>
        <li><b>Olhe perto de 3000.</b> Acima de 3000 é C–H de anel ou C=C; abaixo é C–H de cadeia. Duas bandas em ~2820 e ~2720 indicam aldeído.</li>
        <li><b>Leve a pista para o MS.</b> O grupo funcional diz quais perdas do Apêndice C fazem sentido.</li>
      </ol>
    </div>
    <p class="hint">Bandas do seu arquivo de dados. Conforme a confiança: <b>alta</b> é região de tabela, <b>média</b> é atribuição típica, <b>baixa</b> é palpite ou sem atribuição segura. As faixas vêm de tabelas típicas de IV; confira com a tabela do professor.</p>
    <div class="chips" id="ivchips"></div>
    <div id="ivout"></div>
    <h2 style="margin-top:20px">Tenho um número de onda</h2>
    <label for="ivq">Número de onda (cm⁻¹)<input class="f-m" type="number" id="ivq" inputmode="numeric" min="400" max="4000" placeholder="ex.: 1712"></label>
    <div id="ivres"></div>
  </section>

  <section id="p-ca\"""")
rep("buildChips();analyze();drawTable();calc();","buildChips();analyze();drawTable();calc();ivEx=6;drawIVChips();drawIV();$('#ivq').addEventListener('input',ivLookup);")
open(p,'w',encoding='utf-8').write(s)
