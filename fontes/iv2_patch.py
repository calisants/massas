import json,re
p='template.html'; s=open(p,encoding='utf-8').read()
m=re.search(r'const IR=(\[.*?\]);\nconst IRT=',s,re.S); IR=json.loads(m.group(1))
byn={c['n']:c for c in IR}

# --- ajustes finos nas atribuições do arquivo de dados, alinhando com a tabela da disciplina ---
def setp(n,cm,txt=None,conf=None):
    for r in byn[n]['p']:
        if r[0]==cm:
            if txt: r[1]=txt
            if conf: r[2]=conf; return
            return
    raise KeyError((n,cm))
setp(1,'2967','C–H sp³: CH3 estiramento assimétrico'); setp(1,'2930','C–H sp³: CH2 estiramento assimétrico'); setp(1,'2870','C–H sp³: CH3 estiramento simétrico')
setp(10,'2817','C–H vizinho ao N: na tabela da disciplina o 2820 é CH2 estiramento simétrico')
setp(10,'2786','C–H vizinho ao N (banda típica de amina terciária)'); setp(10,'2768','C–H vizinho ao N (banda típica de amina terciária)')

IDH={1:4,2:3,3:5,4:9,5:1,6:0,7:1,8:4,9:1,10:0,12:1}
DISC={
1:[['3100–3000','C–H aromático (Csp²–H), estiramento'],['2960','CH3 estiramento assimétrico'],['2926','CH2 estiramento assimétrico'],['2880','CH3 estiramento simétrico'],['2850','CH2 estiramento simétrico'],['2000–1667','overtones com padrão de anel monossubstituído'],['1460','CH3 deformação assimétrica (escondida pela banda de 1450 do anel)'],['1455','CH2 deformação tesoura'],['1370','CH3 deformação simétrica'],['730','anel monossubstituído, C–H fora do plano'],['700','anel monossubstituído, C–H fora do plano']],
2:[['3120–3090','C–H aromático (Csp²–H), estiramento'],['1600, 1580, 1500','anel aromático, estiramento (na tabela está escrito "C–H"; a faixa é a de C=C do anel)'],['1270, 1050','C–O de éter aromático (Csp²–O), estiramento'],['750','anel não substituído, C–H fora do plano']],
4:[['3100–3000','C–H aromático (Csp²–H), estiramento'],['1690','C=O, estiramento'],['1600, 1580, 1450','anel aromático, estiramento (na tabela está escrito "C–H")'],['750','anel monossubstituído, C–H fora do plano'],['700','anel monossubstituído, C–H fora do plano']],
8:[['3450','banda larga: água na amostra'],['3160–3000','C–H aromático (Csp²–H), estiramento'],['1600, 1580, 1500, 1450','C=C aromático, estiramento'],['760','anel sem substituinte, C–H fora do plano']],
9:[['3100','O–H de ácido carboxílico, estiramento (larga)'],['2960','CH3 estiramento assimétrico'],['2920','CH2 estiramento assimétrico'],['2867','CH3 estiramento simétrico'],['2860','CH2 estiramento simétrico'],['1710','C=O de ácido carboxílico, estiramento'],['1460','CH3 deformação assimétrica'],['1455','CH2 deformação tesoura'],['1420','CH2 vizinho à carbonila, deformação tesoura'],['1385','CH3 deformação simétrica'],['1280','C–O do C(C=O)OH, estiramento'],['920','O–H fora do plano']],
5:[['2980','CH3 estiramento assimétrico'],['2940','CH2 estiramento assimétrico'],['2870','CH3 estiramento simétrico'],['2860','CH2 estiramento simétrico'],['1720','C=O de cetona, estiramento'],['1470','CH3 deformação assimétrica'],['1410','CH2 vizinho à carbonila, deformação tesoura'],['1380','CH3 deformação simétrica']],
7:[['2980','CH2 estiramento assimétrico'],['2860','CH2 estiramento simétrico'],['1455','CH2 deformação tesoura'],['1120','C–O de éter alifático (Csp³–O), estiramento']],
10:[['2980','CH3 estiramento assimétrico'],['2950','CH2 estiramento assimétrico'],['2870','CH3 estiramento simétrico'],['2820','CH2 estiramento simétrico'],['1460','CH3 deformação assimétrica'],['1450','CH2 deformação tesoura'],['1380','CH3 deformação simétrica ("guarda-chuva")'],['1270','C–N alifático (Csp³–N), estiramento']],
}
for n,c in byn.items():
    c['idh']=IDH[n]; c['disc']=DISC.get(n,[])
IR.append(dict(id='etanol',n=None,nome='Etanol (exemplo da tabela da disciplina)',f='C2H6O',idh=0,pista='Exemplo de álcool primário: O–H larga em 3390 e C–O em 1050. Compare com o 1-propanol (Ex. 6).',p=[],disc=[['3390','O–H, estiramento'],['2980','CH3 estiramento assimétrico'],['2970','CH2 estiramento assimétrico'],['2880','CH3 estiramento simétrico'],['1460','CH3 deformação assimétrica'],['1455','CH2 deformação tesoura'],['1380','CH3 deformação simétrica'],['1050','C–C–OH, estiramento'],['630','C–OH, deformação fora do plano']]))

A,T='apostila','tabela'
IRT=[
 # [hi, lo, grupo, aspecto, confirme com, fonte]
 [3650,3580,'O–H livre de álcool ou fenol','média, estreita (solução diluída ou gás)','',A],
 [3550,3200,'O–H de álcool','forte, larga','C–O em 1150–1050',A],
 [3550,3200,'O–H de fenol','forte, larga','C=C em 1600–1450 e C–O em ~1200',A],
 [3300,2500,'O–H de ácido carboxílico','forte, muito larga','C=O em 1725–1700',A],
 [3500,3100,'N–H de amida','média, larga: amida 1ª 2 bandas, 2ª 1 banda','C=O em 1700–1630',A],
 [3500,3300,'N–H de amina primária','média, 2 bandas (simétrica e assimétrica)','C–N em 1250–1020',A],
 [3400,3300,'N–H de amina secundária','fraca a média, 1 banda','C–N em 1250–1020',A],
 [3500,3300,'N–H ausente = amina terciária','nenhuma banda aqui','',A],
 [3310,3300,'≡C–H de alcino terminal (Csp–H)','fraca, estreita','C≡C em 2260–2100',A],
 [3100,3000,'=C–H de alceno (Csp²–H)','fraca a média','C=C em 1680–1620',A],
 [3100,3000,'=C–H de aromático (Csp²–H)','fraca a média','C=C em 1600–1450',A],
 [2960,2850,'C–H de alcano (Csp³–H)','média a forte, 2 a 4 bandas','',A],
 [2820,2720,'C–H de aldeído','fraca, 2 bandas (~2820 e ~2720)','C=O em 1740–1720',A],
 [3000,2200,'N–H⁺ ou O–H⁺ (sal de amina, sal de ácido, aminoácido)','forte, larga','',A],
 [2600,2550,'S–H de tiol','fraca, estreita','',A],
 [2270,2130,'N=C=O ou N=C=N (acumuladas)','forte','',A],
 [2260,2210,'C≡N de nitrila','média a forte, estreita (não conjugada 2260–2240; conjugada 2235–2210)','',A],
 [2260,2100,'C≡C de alcino','fraca (pode sumir se for simétrico)','',A],
 [2150,2100,'C≡C de alcino terminal','fraca a média','C–H em ~3300',A],
 [2150,2150,'C=C=O de cetena','','',T],
 [2140,1990,'N=C=S de isotiocianato','larga e intensa','',T],
 [1950,1950,'C=C=C de aleno','','',T],
 [2000,1660,'overtones do anel aromático','fracas: mono 4–5 bandas "em escada"; orto 2 bandas; meta 3–4 bandas; para 2 bandas','confirme com 900–650',A],
 [1815,1790,'C=O de cloreto de ácido','forte','C–Cl em 800–600',A],
 [1830,1760,'C=O de anidrido','forte, 2 bandas (~1820 e ~1760)','',A],
 [1750,1735,'C=O de éster','forte','C–O em 1300–1000',A],
 [1740,1720,'C=O de aldeído','forte','C–H em 2820–2720',A],
 [1725,1700,'C=O de ácido carboxílico','forte (1710 é o dímero; o monômero fica perto de 1760)','O–H em 3300–2500',A],
 [1725,1705,'C=O de cetona','forte (cetona acíclica dialquil)','',A],
 [1705,1680,'C=O conjugado (cetona aromática)','forte; a conjugação baixa a banda cerca de 20 cm⁻¹ (regra da tabela da disciplina)','',T],
 [1700,1630,'C=O de amida','forte','N–H em 3500–3100',A],
 [1690,1640,'C=N de imina','média a forte','',A],
 [1680,1620,'C=C de alceno','fraca a média; ausente se simétrico','C–H em 3100–3000',A],
 [1600,1450,'C=C de anel aromático','média: ~1600, ~1580, ~1500 e ~1450','C–H em 3100–3000',A],
 [1550,1500,'N=O de nitro (assimétrico)','forte, 2 bandas','N=O simétrico em 1370–1300',A],
 [1370,1300,'N=O de nitro (simétrico)','forte','',A],
 [1590,1590,'N–H₂ deformação (amina e amida primária)','média a forte (1590 ± 50)','',T],
 [1470,1450,'CH2 deformação (tesoura) e CH3 deformação assimétrica','média','',A],
 [1420,1420,'CH2 vizinho à C=O, deformação','','',T],
 [1385,1370,'CH3 deformação simétrica','média; se for dubleto, i-propil ou geminal dimetil','1170 e 1140 confirmam dimetil geminal',A],
 [1400,1000,'C–F','forte','',A],
 [1300,1200,'C–O de ácido carboxílico (junto com uma banda em ~1420)','forte; acoplamento de O–H no plano com C–O','C=O ~1710 e O–H larga',T],
 [1300,1000,'C–O de éster','forte (insaturado ou aromático: 2 bandas, 1300–1250 e 1200–1050)','C=O em 1750–1735',A],
 [1275,1020,'C–O de éter','forte (alifático 1150–1070; aromático ou vinílico: 2 bandas, 1275–1200 e 1075–1020)','',T],
 [1250,1200,'C–O de fenol','forte','O–H em 3550–3200',A],
 [1150,1050,'C–O de éter alifático','forte','',A],
 [1150,1150,'C–O de álcool terciário','forte','O–H em 3550–3200',A],
 [1100,1100,'C–O de álcool secundário','forte','O–H em 3550–3200',A],
 [1050,1050,'C–O de álcool primário','forte','O–H em 3550–3200',A],
 [1250,1020,'C–N de amina alifática','média (1230 ± 50)','',A],
 [1340,1250,'C–N de amina aromática','(1295 ± 45)','',T],
 [1350,1320,'S=O de sulfona (assimétrico)','intensa (1330 ± 20)','',T],
 [1160,1120,'S=O de sulfona (simétrico)','intensa (1140 ± 20)','',T],
 [1060,1040,'S=O de sulfóxido','(1050 ± 10)','',T],
 [800,600,'C–Cl','forte','',A],
 [750,500,'C–Br','forte','',A],
 [500,500,'C–I','fraca','',A],
 [990,990,'vinila monossubstituída (RCH=CH2), C–H fora do plano','forte; junto com ~910','C=C em ~1655',A],
 [910,910,'vinila monossubstituída (RCH=CH2), C–H fora do plano','forte; junto com ~990','C=C em ~1655',A],
 [980,960,'alceno trans-dissubstituído','forte','C=C em ~1675',A],
 [895,880,'alceno gem-dissubstituído (R2C=CH2)','forte','C=C em ~1655',A],
 [840,790,'alceno trissubstituído (R2C=CHR)','forte','C=C em ~1670',A],
 [730,675,'alceno cis-dissubstituído','forte','C=C em ~1660',A],
 [770,730,'anel monossubstituído, C–H fora do plano','forte; junto com 710–690','overtones em 2000–1660',A],
 [710,690,'anel monossubstituído, C–H fora do plano','forte; junto com 770–730','',A],
 [770,735,'anel orto-dissubstituído, C–H fora do plano','1 banda (4 H adjacentes)','',A],
 [900,860,'H isolado no anel (ex.: meta-dissubstituído)','fraca','',T],
 [810,750,'anel meta-dissubstituído, C–H fora do plano','3 bandas no total (com ~890 e ~700)','',A],
 [725,680,'anel meta-dissubstituído','forte','',A],
 [860,800,'anel para-dissubstituído (2 H adjacentes)','normalmente 820–800','',T],
 [920,920,'O–H de ácido carboxílico, fora do plano','média, larga','C=O em 1725–1700',T],
 [790,770,'grupo etila, balanço (rocking)','','',T],
 [743,734,'grupo propila, balanço (rocking)','','',T],
 [720,720,'–(CH2)n– com n ≥ 4, balanço (rocking)','','',T],
]
REG=[
 ['3700–3100','O–H e N–H','Banda larga é O–H (álcool, fenol, ácido). Uma ou duas bandas mais finas são N–H. Sem banda: não há O–H nem N–H (amina terciária).'],
 ['3300–2700','C–H','Acima de 3000: C–H de anel ou de C=C (e ≡C–H em ~3300). Abaixo de 3000: C–H de cadeia. Duas bandas fracas em 2820 e 2720: aldeído.'],
 ['2700–2260','região silenciosa','Quase nada aparece. Se aparecer: S–H (2600–2550) ou sais de amina e de ácido (larga, 3000–2200).'],
 ['2300–2100','triplas e acumuladas','C≡N (2260–2210), C≡C (2260–2100), N=C=O e N=C=N (2270–2130).'],
 ['2000–1660','overtones do anel','Bandas fracas que desenham o padrão de substituição do anel aromático (mono, orto, meta, para).'],
 ['1850–1630','C=O','Banda forte. A posição diz o tipo: cloreto 1815–1790, anidrido 1830–1760, éster 1750–1735, aldeído 1740–1720, ácido 1725–1700, cetona 1725–1705, amida 1700–1630.'],
 ['1680–1450','C=C e anel','Alceno 1680–1620 (fraca a média). Anel aromático em ~1600, 1580, 1500, 1450. Nitro 1550–1500 e 1370–1300.'],
 ['1470–1350','deformação de C–H','CH2 e CH3 em 1470–1450; CH3 simétrico em 1385–1370.'],
 ['1300–1000','C–O e C–N','C–O é forte: álcool 1º ~1050, 2º ~1100, 3º ~1150, éter 1150–1050, fenol 1250–1200, éster 1300–1000. C–N de amina em 1250–1020 (média).'],
 ['1000–650','impressão digital e substituição','C–H fora do plano: define o padrão de substituição de alcenos e de anel aromático. Abaixo de 800 também ficam C–Cl, C–Br e C–I.'],
]
js_data="const IR="+json.dumps(IR,ensure_ascii=False)+";\nconst IRT="+json.dumps(IRT,ensure_ascii=False)+";\nconst IRREG="+json.dumps(REG,ensure_ascii=False)+";\n"
js_ui=r'''
/* ---------- aba IV ---------- */
let ivEx=6;
const ivKey=c=>c.n!==null?c.n:c.id;
const ivNums=t=>(String(t).match(/\d+/g)||[]).map(Number);
function drawIVChips(){const box=$('#ivchips');box.innerHTML='';
  IR.forEach(c=>{const b=document.createElement('button');b.type='button';b.className='chip';b.setAttribute('aria-pressed',ivEx===ivKey(c)?'true':'false');
    const e=c.n!==null?EX.find(x=>x.n===c.n):null;b.textContent=c.n!==null?'Ex. '+c.n+' '+e.nome:'Etanol (exemplo)';
    b.onclick=()=>{ivEx=ivKey(c);drawIVChips();drawIV();};box.appendChild(b);});}
function drawIV(){
  const c=IR.find(x=>ivKey(x)===ivEx),box=$('#ivout');
  if(!c){box.innerHTML='<p class="empty">Escolha um composto acima.</p>';return;}
  const e=c.n!==null?EX.find(x=>x.n===c.n):null;
  const nome=e?'Ex. '+e.n+': '+e.nome:c.nome,f=e?e.f:c.f;
  let h='<div class="ex-head"><b>'+esc(nome)+'</b><span class="mono">'+fmt(f)+'</span>'+(e?'<span>'+esc(e.g)+'</span>':'')+'<span class="badge ok" title="Índice de deficiência de hidrogênio: anéis + ligações π">IDH = '+c.idh+'</span></div>';
  h+='<div class="ans" style="border-radius:6px;margin-bottom:12px"><span class="t">Pista do IV'+(e?' para o espectro de massas':'')+'</span>'+esc(c.pista)+'</div>';
  if(c.disc.length){
    h+='<h2>Como a disciplina atribui</h2><p class="hint">Da sua <i>tabela análise org II</i>. "Estiramento" é o que a tabela chama de deformação axial.</p><div class="tbl"><table><thead><tr><th>Banda (cm⁻¹)</th><th>O que é</th></tr></thead><tbody>'+
      c.disc.map(r=>'<tr><td class="n">'+r[0]+'</td><td>'+esc(r[1])+'</td></tr>').join('')+'</tbody></table></div>';
  }else if(e){
    h+='<p class="hint">Este composto não está na tabela da disciplina. As atribuições abaixo usam as regras da apostila.</p>';
  }
  if(c.p.length){
    h+='<h2 style="margin-top:18px">Bandas do arquivo de dados</h2><p class="hint">Cada selo mostra a confiança: <b>alta</b> é região de tabela, <b>média</b> é atribuição típica, <b>baixa</b> é palpite ou sem atribuição segura.</p><div class="tbl"><table><thead><tr><th>Banda (cm⁻¹)</th><th>O que é</th><th>Confiança</th></tr></thead><tbody>'+
      c.p.map(r=>'<tr><td class="n">'+r[0]+'</td><td>'+esc(r[1])+'</td><td><span class="badge '+(r[2]==='baixa'?'chk':'ok')+'">'+r[2]+'</span></td></tr>').join('')+'</tbody></table></div>';
  }
  box.innerHTML=h;
}
function ivLookup(){
  const v=parseInt($('#ivq').value,10),box=$('#ivres');
  if(!v){box.innerHTML='';return;}
  const hits=IRT.filter(r=>{const w=r[0]-r[1],tol=w<20?10:0;return v<=r[0]+tol&&v>=r[1]-tol;}).sort((a,b)=>(a[0]-a[1])-(b[0]-b[1]));
  const mine=[];
  IR.forEach(c=>{const tag=c.n!==null?'Ex. '+c.n:'Etanol';
    c.p.forEach(r=>{const n=ivNums(r[0]);if(v>=Math.min(...n)-8&&v<=Math.max(...n)+8)mine.push(tag+' ('+r[0]+')');});
    c.disc.forEach(r=>{r[0].split(',').forEach(part=>{const n=ivNums(part);if(n.length&&v>=Math.min(...n)-8&&v<=Math.max(...n)+8)mine.push(tag+' tabela ('+part.trim()+')');});});});
  const uniq=[...new Set(mine)];
  box.innerHTML=(hits.length?'<div class="tbl"><table><thead><tr><th>Faixa</th><th>Grupo</th><th>Aspecto</th><th>Confirme com</th></tr></thead><tbody>'+hits.map(r=>'<tr><td class="n">'+(r[0]===r[1]?'~'+r[0]:r[1]+'–'+r[0])+'</td><td>'+esc(r[2])+'</td><td>'+esc(r[3])+'</td><td>'+esc(r[4])+'</td></tr>').join('')+'</tbody></table></div>':'<p class="empty">Nenhuma faixa da apostila cobre '+v+' cm⁻¹. Pode estar na região de impressão digital, que quase nunca se atribui banda a banda.</p>')+
   (uniq.length?'<p class="hint" style="margin-top:8px">Nos seus compostos (±8 cm⁻¹): '+uniq.map(x=>'<span class="xr">'+x+'</span>').join('')+'</p>':'');
}
function drawIVReg(){
  $('#ivreg').innerHTML='<div class="tbl"><table><thead><tr><th>Região (cm⁻¹)</th><th>O que olhar</th><th>O que fica lá</th></tr></thead><tbody>'+IRREG.map(r=>'<tr><td class="n">'+r[0]+'</td><td>'+esc(r[1])+'</td><td>'+esc(r[2])+'</td></tr>').join('')+'</tbody></table></div>';
}
'''
a=s.index('const IR='); b=s.index('/* ---------- abas ---------- */')
s=s[:a]+js_data+js_ui+"\n"+s[b:]
def rep(x,y):
    global s
    assert x in s,x[:60]; s=s.replace(x,y,1)
rep("ivEx=6;drawIVChips();drawIV();$('#ivq').addEventListener('input',ivLookup);","drawIVChips();drawIV();drawIVReg();$('#ivq').addEventListener('input',ivLookup);")
# painel: explicação + guia por região + lógica
rep("""    <p class="hint">Bandas do seu arquivo de dados. Conforme a confiança: <b>alta</b> é região de tabela, <b>média</b> é atribuição típica, <b>baixa</b> é palpite ou sem atribuição segura. As faixas vêm de tabelas típicas de IV; confira com a tabela do professor.</p>
""","""    <details><summary>Por que cada banda aparece onde aparece?</summary><dl>
      <div><dt>Posição: ligação mais forte e átomo mais leve vibram mais alto</dt><dd>C≡C ~2150 &gt; C=C ~1650 &gt; C–C ~1000. C–H, N–H e O–H ficam acima de 2500 porque o H é muito leve.</dd></div>
      <div><dt>Intensidade: depende de quanto o dipolo muda</dt><dd>C=O é sempre forte porque o O é muito eletronegativo. C=C simétrico é fraco ou some, porque a vibração não muda o dipolo.</dd></div>
      <div><dt>Hibridização do carbono</dt><dd>Quanto mais caráter s, mais alto: C–H sp (alcino) ~3300; C–H sp² (anel, alceno) 3100–3000; C–H sp³ (alcano) 2960–2850. Mesma lógica no C–O: fenol (~1200) fica acima de álcool (~1050).</dd></div>
      <div><dt>Estiramento × deformação</dt><dd>Estiramento (muda o comprimento da ligação) fica sempre acima da deformação (muda o ângulo). Exemplo do C–H: estiramento 3000–2900; deformação 1470–1350.</dd></div>
    </dl></details>
    <details><summary>Guia por região (da apostila)</summary><div id="ivreg"></div></details>
    <p class="hint">Fontes: sua <i>Apostila de Interpretação de Espectros de IV</i>, a <i>tabela análise org II</i> e a tabela de números de onda do Drive. Os números do arquivo de dados são os do JSON que você enviou, e as atribuições dele são minhas; confira com a tabela do professor.</p>
""")
open(p,'w',encoding='utf-8').write(s)
print('ok',len(IRT))
