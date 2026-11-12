/* ---- ilustrações dos ensaios (Preliminares, Solubilidade, Análise elementar, funcional de nitro, ácido e cloro) ----
   Os desenhos são esquemas (traço em currentColor, líquidos em cor fixa). As cores vêm do texto de cada ensaio. */
const E5={
 svg(w,h,body,al){return '<svg class="ens5" viewBox="0 0 '+w+' '+h+'" role="img" aria-label="'+al+'" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'+body+'</svg>';},
 tx(x,y,t,o){o=o||{};return '<text x="'+x+'" y="'+y+'" text-anchor="'+(o.a||'middle')+'" font-size="'+(o.s||9.5)+'" fill="currentColor" stroke="none"'+(o.b?' font-weight="700"':'')+'>'+String(t).split('|').map((l,i)=>'<tspan x="'+x+'" dy="'+(i?11:0)+'">'+l+'</tspan>').join('')+'</text>';},
 arr(x1,y1,x2,y2){const a=Math.atan2(y2-y1,x2-x1),h=5;return '<path d="M'+x1+' '+y1+'L'+x2+' '+y2+'M'+x2+' '+y2+'l'+(-h*Math.cos(a-0.5)).toFixed(1)+' '+(-h*Math.sin(a-0.5)).toFixed(1)+'M'+x2+' '+y2+'l'+(-h*Math.cos(a+0.5)).toFixed(1)+' '+(-h*Math.sin(a+0.5)).toFixed(1)+'" stroke-width="1.6"/>';},
 /* tubo de ensaio: x,y = canto superior esquerdo; o = {h, lvl (0-1), liq, layer (fase de baixo), pre (precipitado), solid, bub, cloud} */
 tube(x,y,o){o=o||{};const H=o.h||72,top=H*(1-(o.lvl==null?0.55:o.lvl));let s='<g transform="translate('+x+','+y+')">';
  if(o.liq)s+='<path d="M1 '+top.toFixed(1)+'H27V'+(H-14)+'A13 13 0 0 1 1 '+(H-14)+'Z" fill="'+o.liq+'" stroke="none"/>';
  if(o.layer)s+='<path d="M1 '+(H-27)+'H27V'+(H-14)+'A13 13 0 0 1 1 '+(H-14)+'Z" fill="'+o.layer+'" stroke="none"/><path d="M1 '+(H-27)+'H27" stroke-width="1" stroke-dasharray="2 2"/>';
  if(o.pre)s+=[[7,H-5],[13,H-8],[19,H-5],[10,H-3],[17,H-10],[22,H-9],[14,H-4]].map(p=>'<circle cx="'+p[0]+'" cy="'+p[1]+'" r="2.1" fill="'+o.pre+'" stroke-width=".8"/>').join('');
  if(o.solid)s+='<path d="M5 '+(H-4)+'q9 -8 18 0q-9 4 -18 0z" fill="'+o.solid+'" stroke-width="1"/>';
  if(o.bub)for(let i=0;i<o.bub;i++)s+='<circle cx="'+(8+(i*7)%13)+'" cy="'+(top+8+i*9).toFixed(1)+'" r="'+(1.5+(i%2)*.8)+'" stroke-width="1"/>';
  s+='<path d="M0 0V'+(H-14)+'A14 14 0 0 0 28 '+(H-14)+'V0"/><path d="M-3 0H31"/></g>';return s;},
 flame(x,y,k,c1,c2){return '<g transform="translate('+x+','+y+') scale('+k+')"><path d="M0 0C-11 -12 -8 -26 0 -42C8 -26 11 -12 0 0Z" fill="'+c1+'" stroke="none"/><path d="M0 0C-5 -6 -4 -13 0 -20C4 -13 5 -6 0 0Z" fill="'+c2+'" stroke="none"/></g>';},
 paper(x,y,w,h,c){return '<rect x="'+x+'" y="'+y+'" width="'+w+'" height="'+h+'" rx="1.5" fill="'+c+'" stroke-width="1.5"/>';},
 /* microtubo de pirólise: reagente no fundo, papel na boca, chama embaixo */
 pirol(x,y,paper,lab){return '<g transform="translate('+x+','+y+')">'+E5.paper(-6,-4,24,7,paper)+'<path d="M0 3V52a6 6 0 0 0 12 0V3" /><path d="M1 36H11V52a5 5 0 0 1 -10 0Z" fill="#a98a5e" stroke="none"/><path d="M1 28H11V36H1Z" fill="#d9c9a3" stroke="none"/>'+E5.flame(6,76,.5,'#f4b400','#f08a1c')+E5.tx(6,92,lab,{s:8.5})+'</g>';},
 dot(c){return '<i class="ens5dot" style="background:'+c+'"></i>';}
};
const E5CORES=[['azul arroxeado','#5a4a9a'],['castanho-alaranjada','#c4742a'],['azul','#2b5fd0'],['carmim','#c0143c'],['eosina','#c0143c'],['fúcsia','#c2188b'],['castanha','#8b5a2b'],['castanho','#8b5a2b'],['violeta','#7b3fc4'],['negra','#222']];
/* ---- Preliminares ---- */
function e5Cor(){
 const seg=[[35,'#7b3fc4','#b5c93a'],[45,'#2f5ccf','#f2d21b'],[10,'#1a9aa0','#f08a1c'],[10,'#1fa38a','#d6322b'],[60,'#3aa047','#a0309a'],[20,'#b5c93a','#7b3fc4'],[15,'#f2d21b','#2f5ccf'],[10,'#f08a1c','#1fa38a'],[95,'#d6322b','#1a9aa0']];
 let x=15,a='',b='';seg.forEach(s=>{const w=s[0]*0.7;a+='<rect x="'+x.toFixed(1)+'" y="26" width="'+w.toFixed(1)+'" height="18" fill="'+s[1]+'" stroke="none"/>';b+='<rect x="'+x.toFixed(1)+'" y="60" width="'+w.toFixed(1)+'" height="18" fill="'+s[2]+'" stroke="none"/>';x+=w;});
 let ax='';[400,500,600,700].forEach(n=>{const px=15+(n-400)*0.7;ax+='<path d="M'+px+' 82v4" stroke-width="1.2"/>'+E5.tx(px,97,n,{s:8.5});});
 return E5.svg(260,106,E5.tx(15,12,'Luz que a substância absorve',{a:'start',s:9,b:1})+a+E5.tx(15,55,'Cor que o olho vê (a complementar)',{a:'start',s:9,b:1})+b+ax+E5.tx(232,97,'nm',{s:8.5,a:'start'}),'Faixas de luz absorvida e a cor complementar que o olho vê, de 400 a 700 nanômetros');
}
function e5Aspecto(){
 const t=(x,l,c,sol,lab)=>(sol?'<path d="M'+(x-4)+' 52q22 22 44 0Z" fill="'+c+'" stroke-width="1.6"/><path d="M'+(x+8)+' 56q10 6 20 0" stroke-width="1" stroke-dasharray="2 2"/>':E5.tube(x+6,10,{h:56,lvl:.55,liq:c}))+E5.tx(x+18,86,lab,{s:8.5});
 return E5.svg(260,100,t(5,'',"#e8f1f7",0,'líquido|incolor')+t(70,'','#e0a030',0,'líquido|colorido')+t(135,'','#f2f2ee',1,'sólido|incolor')+t(200,'','#e8c820',1,'sólido|colorido'),'Líquido incolor, líquido colorido, sólido incolor e sólido colorido');
}
function e5Cheiro(){
 const w='<path d="M26 30q-4 -6 0 -12t0 -12" stroke-width="1.4"/><path d="M34 32q-4 -6 0 -12t0 -12" stroke-width="1.4"/><path d="M42 30q-4 -6 0 -12t0 -12" stroke-width="1.4"/>';
 return E5.svg(260,100,E5.tube(20,38,{h:50,lvl:.5,liq:'#e8f1f7'})+w+'<path d="M92 56q22 -26 54 -10" stroke-width="1.8"/>'+E5.arr(138,40,150,46)+'<path d="M98 66l8 -8M106 70l8 -8" stroke-width="1.6"/>'+'<circle cx="205" cy="48" r="20"/><path d="M225 48q9 0 6 8h-8" /><circle cx="213" cy="42" r="1.6" fill="currentColor"/>'+E5.tx(62,98,'abane o vapor com a mão',{s:8.5})+E5.tx(205,86,'em direção ao nariz',{s:8.5}),'Tubo com amostra soltando vapor e a mão abanando o vapor em direção ao nariz');
}
function e5Ignicao(){
 const f=(x,k,c1,c2,soot,lab)=>E5.flame(x,84,k,c1,c2)+(soot?[[0,-6],[7,-14],[-6,-21],[3,-28]].slice(0,soot).map(p=>'<circle cx="'+(x+p[0])+'" cy="'+(84-42*k+p[1])+'" r="2" fill="currentColor" stroke="none" opacity=".55"/>').join(''):'')+'<path d="M'+(x-18)+' 88h36" stroke-width="2.2"/>'+E5.tx(x,104,lab,{s:8.5});
 return E5.svg(260,132,f(32,1,'#f4b400','#f08a1c',4,'aromático:|amarela e|fuliginosa')+f(97,.8,'#f4b400','#f08a1c',1,'alifático:|amarela, pouca|fuligem')+f(162,.65,'#9ccaff','#3b82f6',0,'com oxigênio:|mais clara|(azulada)')+'<path d="M214 88h36" stroke-width="2.2"/><path d="M222 87q10 -8 20 0" fill="#9a9a9a" stroke="none"/><circle cx="228" cy="80" r="1.6" fill="#9a9a9a" stroke="none"/><circle cx="237" cy="78" r="1.4" fill="#9a9a9a" stroke="none"/>'+E5.tx(232,104,'sobrou|resíduo',{s:8.5}),'Quatro chamas: aromático amarela e fuliginosa, alifático amarela com pouca fuligem, composto oxigenado azulada, e um resíduo que sobra');
}
function e5PF(){
 const body='<path d="M96 30V118a4 4 0 0 0 4 4H150a4 4 0 0 0 4-4V30" fill="#f5e6a8" fill-opacity=".6" stroke-width="2"/><path d="M96 30h58" /><path d="M96 100H66V52H96" fill="none"/><path d="M96 90H78V62H96" fill="#f5e6a8" fill-opacity=".6" stroke="none"/>';
 return E5.svg(260,150,'<path d="M96 38H154" stroke-dasharray="3 3" stroke-width="1"/>'+body+'<path d="M125 8V92" stroke-width="2.2"/><circle cx="125" cy="96" r="4.5" fill="#c0392b" stroke-width="1.2"/><rect x="128" y="74" width="2.4" height="16" fill="#e8e8e8" stroke-width="1"/><path d="M122 70h8" stroke-width="2.4"/>'+E5.flame(74,128,.55,'#3b82f6','#9ccaff')+'<path d="M64 130h20" stroke-width="2"/>'+E5.tx(176,45,'óleo (sem água)',{a:'start',s:8.5})+E5.tx(176,70,'capilar preso ao|termômetro com|anel de borracha',{a:'start',s:8.5})+E5.tx(34,144,'chama branda',{s:8.5})+E5.tx(176,116,'bulbo na altura da|alça lateral ou abaixo',{a:'start',s:8.5})+E5.arr(172,112,134,100),'Tubo de Thiele com óleo, termômetro com capilar preso por anel de borracha e chama branda sob a alça lateral');
}
function e5PEb(){
 const A=E5.tube(44,10,{h:64,lvl:.5,liq:'#e8f1f7'})+'<path d="M58 14V58" stroke-width="1.4"/><circle cx="55" cy="52" r="1.6" stroke-width="1"/><circle cx="60" cy="46" r="1.6" stroke-width="1"/><circle cx="56" cy="40" r="1.6" stroke-width="1"/>'+E5.flame(58,102,.5,'#3b82f6','#9ccaff')+E5.tx(58,116,'aquecendo:|bolhas contínuas',{s:8.5});
 const B=E5.tube(124,10,{h:64,lvl:.5,liq:'#e8f1f7'})+'<path d="M138 14V58" stroke-width="1.4"/><rect x="136.6" y="38" width="2.8" height="20" fill="#e8f1f7" stroke-width="1"/>'+E5.tx(138,92,'chama retirada,|esfriando',{s:8.5});
 return E5.svg(260,128,A+B+E5.arr(92,40,118,40)+E5.arr(180,44,160,44)+E5.tx(186,36,'o líquido sobe|no capilar: anote|a temperatura',{a:'start',s:8.5}),'Microtubo com capilar selado: bolhas contínuas ao aquecer; ao retirar a chama, o líquido sobe no capilar');
}
function e5Pureza(){
 let ax='<path d="M20 60H240" stroke-width="1.4"/>'+E5.arr(232,60,242,60);
 return E5.svg(260,84,ax+'<rect x="150" y="14" width="22" height="9" fill="#3aa047" stroke="none"/>'+E5.tx(161,36,'puro: faixa|estreita',{s:8.5})+'<rect x="66" y="14" width="64" height="9" fill="#d6322b" stroke="none"/>'+E5.tx(98,36,'impuro: faixa larga|e mais baixa',{s:8.5})+E5.tx(130,80,'temperatura de fusão (°C)',{s:8.5}),'Faixa de fusão estreita indica substância pura; faixa larga e deslocada para baixo indica impureza');
}
/* nova ficha: cor da chama */
function e5ChamaMetais(){
 const m=[['Li','#e0243a','vermelho|(carmim)'],['Na','#f4b400','amarelo'],['K','#b58be0','lilás'],['Ca','#e8671c','laranja-|avermelhado'],['Sr','#d01c2f','vermelho|(escarlate)'],['Ba','#9fd36a','verde claro'],['Cu','#2fb59a','azul-|esverdeado']];
 return E5.svg(260,166,m.map((e,i)=>{const x=36+(i%4)*62,y=i<4?48:120;return E5.flame(x,y,.7,e[1],'#fff6d0')+'<path d="M'+(x-10)+' '+(y+4)+'h20" stroke-width="1.6"/>'+E5.tx(x,y+17,e[0],{s:10,b:1})+E5.tx(x,y+28,e[2],{s:8});}).join(''),'Cor da chama de sete metais: lítio vermelho, sódio amarelo, potássio lilás, cálcio laranja-avermelhado, estrôncio vermelho, bário verde claro, cobre azul-esverdeado');
}
function e5Beilstein(){
 return E5.svg(260,118,E5.flame(90,70,1.1,'#7fd6c2','#e0fff7')+'<path d="M120 72H60" stroke-width="2.2"/><path d="M70 96l4 -26" stroke-width="2"/><path d="M70 72q-8 -14 0 -16q8 2 0 16" fill="none" stroke="#b87333" stroke-width="2.4"/><path d="M70 72V108" stroke="#b87333" stroke-width="2.4"/>'+E5.tx(185,40,'chama verde-azulada|na alça de cobre',{s:9,b:1})+E5.tx(185,66,'= possível halogênio',{s:9})+E5.tx(185,82,'(piridinas também dão|verde: não é prova)',{s:8.5}),'Alça de cobre com amostra na chama de um bico de Bunsen, com chama verde-azulada');
}
/* ---- Solubilidade ---- */
function e5SolFase(){
 return E5.svg(260,128,E5.tube(26,8,{h:70,lvl:.6,liq:'#dbeaf7'})+E5.tx(40,96,'solúvel|(uma só fase)',{s:8.5})+E5.tube(116,8,{h:70,lvl:.6,liq:'#dbeaf7',solid:'#b9a77a'})+E5.tx(130,96,'insolúvel|(sobra sólido)',{s:8.5})+E5.tube(206,8,{h:70,lvl:.6,liq:'#dbeaf7',layer:'#e2c46b'})+E5.tx(220,96,'insolúvel|(duas fases)',{s:8.5}),'Três tubos: solúvel com uma só fase, insolúvel com sólido no fundo, insolúvel com duas fases');
}
function e5SolAgua(){
 return E5.svg(260,128,E5.tube(36,8,{h:70,lvl:.6,liq:'#dbeaf7'})+E5.tx(50,96,'poucos C por|grupo polar:|dissolve',{s:8.5})+E5.tube(176,8,{h:70,lvl:.6,liq:'#dbeaf7',layer:'#e2c46b'})+E5.tx(190,96,'cadeia longa:|não dissolve',{s:8.5})+'<path d="M96 30l8 6l8 -6l8 6l8 -6l8 6" stroke-width="1.8"/><circle cx="92" cy="30" r="5" fill="#c0392b" fill-opacity=".35" stroke-width="1.4"/>'+E5.tx(118,56,'≈ 5 C para cada|grupo polar (OH,|NH₂, C=O, COOH)',{s:8.5}),'Tubo com composto de cadeia curta dissolvido e tubo com composto de cadeia longa em duas fases');
}
function e5SolEter(){
 return E5.svg(260,128,E5.tube(36,8,{h:70,lvl:.6,liq:'#f1f0d8'})+E5.tx(50,96,'polar orgânico|(etanol, acetona):|dissolve',{s:8.5})+E5.tube(176,8,{h:70,lvl:.6,liq:'#f1f0d8',solid:'#e8e8e8'})+E5.tx(190,96,'sal ou muito polar:|não dissolve|(S₂)',{s:8.5}),'Dois tubos com éter: polar orgânico dissolve, sal não dissolve');
}
function e5SolTorn(){
 const c=(x,a,b,l)=>E5.paper(x,18,26,34,a)+E5.arr(x+13,56,x+13,66)+E5.paper(x,70,26,34,b)+E5.tx(x+13,120,l,{s:8.5});
 return E5.svg(260,136,c(22,'#6d8fe0','#d6453a','SA|vira vermelho')+c(117,'#d6453a','#6d8fe0','SB|vira azul')+c(212,'#6d8fe0','#6d8fe0','S₁|não muda')+E5.tx(130,10,'papel de tornassol na solução aquosa',{s:9,b:1}),'Papel de tornassol: azul que fica vermelho indica ácido, vermelho que fica azul indica base, sem mudança indica neutro');
}
function e5SolNaOH(){
 return E5.svg(260,128,E5.tube(26,8,{h:70,lvl:.6,liq:'#dbeaf7',solid:'#b9a77a'})+E5.tx(40,96,'2-naftol em|água: não dissolve',{s:8.5})+E5.arr(80,40,112,40)+E5.tx(96,32,'+ NaOH',{s:8.5})+E5.tube(130,8,{h:70,lvl:.6,liq:'#dbeaf7'})+E5.tx(144,96,'vira sal (naftóxido|de sódio): dissolve',{s:8.5})+E5.tx(215,40,'R–COOH + NaOH|↓|R–COO⁻Na⁺ + H₂O',{s:8.5}),'Tubo com 2-naftol que não dissolve em água e dissolve depois de adicionar NaOH');
}
function e5SolBicarb(){
 return E5.svg(260,128,E5.tube(36,8,{h:70,lvl:.7,liq:'#dbeaf7',bub:5})+'<path d="M44 6q-3 -6 0 -9M52 6q-3 -6 0 -9" stroke-width="1.2"/>'+E5.tx(50,96,'ácido forte (A₁):|borbulha, sai CO₂',{s:8.5})+E5.tube(176,8,{h:70,lvl:.6,liq:'#dbeaf7',solid:'#b9a77a'})+E5.tx(190,96,'ácido fraco: não|dissolve e não borbulha',{s:8.5}),'Tubo com bicarbonato borbulhando com ácido forte e tubo sem reação com ácido fraco');
}
function e5SolHCl(){
 return E5.svg(260,128,E5.tube(26,8,{h:70,lvl:.6,liq:'#dbeaf7',layer:'#e2c46b'})+E5.tx(40,96,'amina em água:|não dissolve',{s:8.5})+E5.arr(80,40,112,40)+E5.tx(96,32,'+ HCl 5%',{s:8.5})+E5.tube(130,8,{h:70,lvl:.6,liq:'#dbeaf7'})+E5.tx(144,96,'vira sal de amônio:|dissolve (grupo B)',{s:8.5})+E5.tx(215,40,'R–NH₂ + HCl|↓|R–NH₃⁺Cl⁻',{s:8.5}),'Tubo com amina que não dissolve em água e dissolve depois de adicionar HCl');
}
function e5SolNeutro(){
 const bx=(x,y,w,t)=>'<rect x="'+x+'" y="'+y+'" width="'+w+'" height="26" rx="4"/>'+E5.tx(x+w/2,y+16,t,{s:9});
 return E5.svg(260,118,bx(10,8,115,'não dissolveu em água,')+bx(135,8,115,'NaOH nem HCl: neutro')+E5.arr(130,34,130,50)+bx(10,56,115,'tem N ou S: MN')+bx(135,56,115,'sem N e S: H₂SO₄')+E5.arr(70,34,70,52).replace('M70 34','M70 34'),'Composto neutro: se tem nitrogênio ou enxofre vai para MN, se não tem faz o teste com ácido sulfúrico');
}
function e5SolH2SO4(){
 return E5.svg(260,128,E5.tube(36,8,{h:70,lvl:.6,liq:'#dbeaf7',layer:'#e2c46b'})+E5.tx(50,96,'neutro em água|(2 fases)',{s:8.5})+E5.arr(90,40,122,40)+E5.tx(106,32,'+ H₂SO₄ 96%',{s:8.5})+E5.tube(136,8,{h:70,lvl:.6,liq:'#8a5a2a'})+E5.tx(150,96,'dissolve: sal|(às vezes com calor,|cor ou precipitado)',{s:8.5}),'Tubo com composto neutro que dissolve em ácido sulfúrico concentrado, com mudança de cor');
}
function e5SolErro(){
 return E5.svg(260,128,E5.tube(36,8,{h:70,lvl:.6,liq:'#dbeaf7',solid:'#b9a77a'})+E5.tx(50,96,'dissolveu só um pouco,|sobrou sólido:|insolúvel',{s:8.5})+'<path d="M110 28l30 30M140 28l-30 30" stroke="#c0392b" stroke-width="2.4"/>'+E5.tube(176,8,{h:70,lvl:.6,liq:'#dbeaf7'})+E5.tx(190,96,'uma única fase|límpida: solúvel',{s:8.5}),'Tubo com sólido restante conta como insolúvel; tubo com uma fase límpida conta como solúvel');
}
/* ---- Análise elementar ---- */
function e5Pirol(paper,legenda,al){return E5.svg(260,128,E5.pirol(40,12,paper,'amostra +|reagente')+E5.arr(128,14,62,14)+E5.tx(188,12,legenda,{s:8.5})+E5.tx(188,70,'o papel fica úmido,|na boca do microtubo',{s:8.5}),al);}
function e5Papeis(lista,al){const n=lista.length,w=240/n;return E5.svg(260,84,lista.map((p,i)=>{const x=10+i*w+w/2;return E5.paper(x-14,10,28,36,p[0])+E5.tx(x,60,p[1],{s:8.5});}).join(''),al);}
function e5Iodo(){
 return E5.svg(260,128,E5.tube(36,8,{h:70,lvl:.6,liq:'#8a5a2a'})+E5.tx(50,96,'oxigenado:|castanho',{s:8.5})+E5.tube(116,8,{h:70,lvl:.6,liq:'#7b3fc4'})+E5.tx(130,96,'hidrocarboneto|saturado ou|halogenado: violeta',{s:8.5})+E5.tube(206,8,{h:70,lvl:.6,liq:'#b5532a'})+E5.tx(220,96,'alguns aromáticos:|castanho a|vermelho',{s:8.5}),'Três tubos com iodo: castanho para oxigenado, violeta para hidrocarboneto saturado, castanho-avermelhado para alguns aromáticos');
}
function e5Halog(){
 return E5.svg(260,128,'<path d="M84 52V100a6 6 0 0 0 12 0V52" /><path d="M85 76H95V100a5 5 0 0 1 -10 0Z" fill="#f2d21b" stroke="none"/>'+E5.paper(78,45,24,7,'#2b5fd0')+'<path d="M40 100H140V112H40z" fill="#9ccaff" fill-opacity=".5"/>'+'<path d="M40 100V112M140 100V112" />'+E5.tx(90,30,'X₂ sobe até o papel',{s:8.5})+E5.tx(205,52,'microtubo em|banho-maria,|com o papel|na boca',{s:8.5}),'Microtubo em banho-maria com papel reagente na boca recebendo o vapor do halogênio');
}
function e5Pirolise3(){
 const tb=(x,l,c)=>'<path d="M'+x+' 36V74a7 7 0 0 0 14 0V36" /><path d="M'+(x+1)+' 58H'+(x+13)+'V74a6 6 0 0 1 -12 0Z" fill="'+c+'" stroke="none"/>'+E5.paper(x-4,28,22,6,'#e8e8e8')+E5.tx(x+7,100,l,{s:8.5});
 return E5.svg(260,128,'<rect x="30" y="38" width="200" height="8" fill="#bdbdbd" stroke-width="1.4"/>'+tb(60,'amostra +|reagente','#a98a5e')+tb(123,'branco:|só reagente','#d9c9a3')+tb(186,'positivo:|padrão + reag.','#a98a5e')+E5.tx(130,14,'placa com furos e microtubos pendurados por anéis de borracha',{s:8.5}),'Placa com três microtubos: amostra com reagente, branco só com reagente e positivo com padrão');
}
function e5Lassaigne(){
 const bx=(x,t)=>'<rect x="'+x+'" y="40" width="64" height="34" rx="5"/>'+E5.tx(x+32,54,t,{s:8.5});
 return E5.svg(260,96,bx(4,'1. pirolisar|amostra + metal')+E5.arr(70,57,90,57)+bx(92,'2. dissolver|em água')+E5.arr(158,57,178,57)+bx(180,'3. filtrar e|testar o filtrado')+E5.tx(130,20,'elementos viram íons: N → CN⁻, S → S²⁻, X → X⁻',{s:9,b:1}),'Três etapas: pirolisar a amostra com o metal, dissolver em água, filtrar e testar o filtrado');
}
function e5Resumo(){
 const el=[['C',['#2b5fd0']],['H',['#8b5a2b','#7b3fc4']],['N',['#c4742a','#222','#2b5fd0']],['S',['#8b5a2b','#7b3fc4']],['P',['#2b5fd0']]];
 return E5.svg(260,64,el.map((e,i)=>{const x=14+i*50;return '<circle cx="'+(x+14)+'" cy="18" r="12"/>'+E5.tx(x+14,22,e[0],{s:11,b:1})+e[1].map((c,j)=>'<rect x="'+(x+3+j*10)+'" y="40" width="9" height="14" rx="2" fill="'+c+'" stroke-width="1"/>').join('');}).join(''),'Cores por elemento: C azul; H castanha ou violeta; N castanho-alaranjada, negra ou azul; S castanha ou violeta; P azul');
}
/* ---- Funcional: nitro, ácido, cloro (formato antigo) ---- */
function e5Tubos(a,b,l,al,extra){
 const tb=(x,c,pre)=>E5.tube(x,8,{h:72,lvl:.55,liq:c,pre:pre});
 return E5.svg(260,128,tb(44,a[0],a[2])+E5.arr(96,44,134,44)+tb(170,b[0],b[2])+E5.tx(58,98,l[0],{s:8.5})+E5.tx(184,98,l[1],{s:8.5}),al);
}
const E5FU={
 '1. Hidróxido ferroso':[['#7fb069'],['#8b4a2b'],['reagente:|precipitado verde','positivo: castanho-|avermelhado']],
 '2. Zinco, cloreto':[['#eeeeee'],['#7a4fb0'],['antes:|incolor','positivo: púrpura,|azul ou verde']],
 '1. Iodeto e iodato':[['#eeeeee'],['#2b3a8a'],['antes do iodato:|sem azul','depois do iodato:|azul']],
 '2. Hidroxamato':[['#f2e3b0'],['#7a2f6b'],['antes:|amarelo-claro','positivo:|vermelho-violeta']],
 '3. Resorcinol':[['#eeeeee'],['#c8e04a'],['antes:|incolor','fluorescência|verde ou amarela']],
 '4. Ácido tiobarbitúrico':[['#eeeeee'],['#c0392b'],['antes:|incolor','positivo:|vermelho']],
 'B. De que tipo':[['#eeeeee'],['#e8eef5','#ffffff'],['antes:|incolor','positivo: precipitado|branco (AgCl)']],
 'C. Alternativa':[['#eeeeee'],['#e8eef5','#ffffff'],['filtrado:|incolor','positivo: precipitado|branco (cloreto)']]
};
function e5Blocos(){
 const mk=(fig,cap)=>{const f=document.createElement('figure');f.className='ens';f.innerHTML=fig+(cap?'<figcaption>'+cap+'</figcaption>':'');return f;};
 /* Preliminares, Solubilidade, Elementar: figura logo depois do título, ou depois de um ponto indicado */
 let ctr=0;const add=(pageSel,rx,fn,cap,after)=>{const id='|'+(++ctr)+'|';document.querySelectorAll(pageSel).forEach(h=>{if(!rx.test(h.textContent.trim()))return;const el=h.closest('.el');if((el.dataset.e5k||'').indexOf(id)>=0)return;el.dataset.e5k=(el.dataset.e5k||'')+id;const fg=mk(fn(),cap);const ref=after?el.querySelector(after):null;(ref||h).insertAdjacentElement('afterend',fg);});};
 const P='#p-pf .el > h3',S='#p-so .el > h3',L='#p-el .el > h3';
 add(P,/^Cor$/,e5Cor,'Cada faixa de cima é a luz absorvida; a de baixo é a cor que o olho vê. Esquema: as larguras seguem a tabela abaixo.','p');
 add(P,/^Aspecto e cheiro/,e5Cheiro,'Cheiro: só abane o vapor na direção do nariz, na capela.');
 add(P,/^Aspecto e cheiro/,e5Aspecto,'Aspecto: líquido ou sólido, incolor ou colorido.');
 add(P,/^Teste de ignição/,e5Ignicao,'O que olhar na chama: cor e fuligem.','p');
 add(P,/^Ponto de fusão/,e5PF,'Tubo de Thiele: capilar junto ao bulbo do termômetro, aquecimento brando na alça lateral.');
 add(P,/^Ponto de ebulição/,e5PEb,'Capilar selado com a ponta aberta no líquido: anote a temperatura em que o líquido sobe no capilar.');
 add(P,/^Para que servem/,e5Pureza,'Regra geral: impureza alarga e abaixa a faixa de fusão.');
 add(S,/^Água$/,e5SolAgua,'Cadeia carbônica longa vence o grupo polar.');
 add(S,/^Éter$/,e5SolEter,'');
 add(S,/^Tornassol$/,e5SolTorn,'');
 add(S,/^NaOH 5%/,e5SolNaOH,'');
 add(S,/^NaHCO/,e5SolBicarb,'');
 add(S,/^HCl 5%/,e5SolHCl,'');
 add(S,/^Análise elementar entre/,e5SolNeutro,'');
 add(S,/^H₂SO₄ 96%/,e5SolH2SO4,'');
 add(S,/^Erros comuns/,e5SolErro,'');
 add(S,/^Como se faz cada teste/,e5SolFase,'Como ler o resultado de cada tubo: 30 a 50 mg de amostra em 1 mL do solvente.');
 add(L,/^CCarbono|^Carbono/,()=>e5Pirol('#2b5fd0','mancha azul: HCN, logo há carbono','Pirólise com reagente de mercúrio, papel de acetato de benzidina com acetato de cobre II'),'');
 add(L,/^HHidrogênio|^Hidrogênio/,()=>e5Pirol('#8b5a2b','castanha (acetato de chumbo)|ou violeta (nitroprussiato)','Pirólise com enxofre e papel que recebe H₂S'),'');
 add(L,/^OOxigênio|^Oxigênio/,e5Iodo,'Ensaio do iodo: o tubo mostra a cor do complexo.');
 add(L,/^NNitrogênio|^Nitrogênio/,()=>e5Papeis([['#c4742a','Nessler:|castanho-laranja'],['#222','prata-manganês:|negra'],['#6d8fe0','tornassol|vermelho: azul']],'Três papéis que recebem o NH₃'),'Cada papel mostra o NH₃ de um jeito.');
 add(L,/^SEnxofre|^Enxofre/,()=>e5Pirol('#8b5a2b','castanha (acetato de chumbo)|ou violeta (nitroprussiato)','Pirólise com formiato de sódio e papel que recebe H₂S'),'');
 add(L,/^PFósforo|^Fósforo/,()=>e5Papeis([['#2b5fd0','molibdato + acetato de|benzidina: azul']],'Cor azul indica fósforo'),'');
 add(L,/^Resumo de cores/,e5Resumo,'');
 add(L,/^Como se faz$/,e5Halog,'');
 add(L,/^Pirólise reativa/,e5Pirolise3,'');
 add(L,/^Mineralização/,e5Lassaigne,'Esquema geral, sem detalhar o metal usado.');
 /* pontos de cor nas tabelas de cores */
 document.querySelectorAll('#p-el table.cola td:last-child, #p-el table:not(.cola) td:last-child').forEach(td=>{if(td.dataset.e5)return;td.dataset.e5=1;let t=td.textContent.toLowerCase(),out='';const usados=[];E5CORES.forEach(c=>{if(t.indexOf(c[0])>=0&&!usados.some(u=>u.indexOf(c[0])>=0)){usados.push(c[0]);t=t.replace(c[0],' ');out+=E5.dot(c[1]);}});if(out)td.insertAdjacentHTML('afterbegin',out+' ');});
}
/* ---- funcional antigo (nitro, ácido, cloro): tubo e materiais, como nos outros ensaios ---- */
function e5Funcional(){
 ['fu-nit','fu-aci','fu-clo'].forEach(id=>{const box=document.getElementById(id);if(!box)return;box.querySelectorAll('.el').forEach(el=>{
  if(el.dataset.e5)return;el.dataset.e5=1;const h=el.querySelector('h3');if(!h)return;const t=h.textContent.trim();
  const chave=Object.keys(E5FU).find(k=>t.indexOf(k)===0);
  if(t.indexOf('Segurança')===0){const f=document.createElement('figure');f.className='ens';f.innerHTML='<div class="ens5ic">'+fuIc('oculos')+fuIc('capela')+'</div><figcaption>Óculos, luvas e capela.</figcaption>';h.insertAdjacentElement('afterend',f);return;}
  if(!chave&&!/^A\. Tem cloro/.test(t))return;
  let fig;
  if(/^A\. Tem cloro/.test(t))fig=E5.svg(260,128,'<path d="M60 52V100a6 6 0 0 0 12 0V52"/><path d="M61 76H71V100a5 5 0 0 1 -10 0Z" fill="#c9a64a" stroke="none"/>'+E5.paper(54,45,24,7,'#5a4a9a')+E5.tx(66,32,'papel de Villier',{s:8.5})+E5.arr(86,60,124,60)+E5.tx(185,56,'cloro: o papel fica|azul arroxeado',{s:8.5})+E5.tx(185,84,'(só amido iodetado azul:|pode ser bromo)',{s:8.5}),'Microtubo com papel de Villier que fica azul arroxeado se houver cloro');
  else{const d=E5FU[chave];fig=E5.svg(260,128,E5.tube(44,8,{h:72,lvl:.55,liq:d[0][0]})+E5.arr(96,44,134,44)+E5.tube(170,8,{h:72,lvl:.55,liq:d[1][0],pre:d[1][1]})+E5.tx(58,98,d[2][0],{s:8.5})+E5.tx(184,98,d[2][1],{s:8.5}),'Antes e depois: '+d[2][0].replace('|',' ')+' para '+d[2][1].replace('|',' '));}
  const f=document.createElement('figure');f.className='ens';f.innerHTML=fig+'<figcaption>Cores do tubo aproximadas.</figcaption>';
  const steps=[...el.querySelectorAll('.steps2 li')].map(x=>x.textContent),rg=[...el.querySelectorAll('p')].filter(p=>/Reagente/i.test(p.textContent)).map(p=>['',p.textContent]);
  const mat=fuMat({st:steps,rg:rg.length?rg:[['','']]});
  const ul=document.createElement('div');ul.innerHTML='<h4>Materiais</h4><ul class="fuul fumt">'+mat.map(x=>'<li>'+fuIc(x[0])+'<span>'+esc(x[1])+'</span></li>').join('')+'</ul>';
  h.insertAdjacentElement('afterend',f);f.insertAdjacentElement('afterend',ul);
 });});
}
/* ---- ficha nova: cor da chama (Preliminares, depois do teste de ignição) ---- */
function e5FichaChama(){
 const ig=[...document.querySelectorAll('#p-pf .el > h3')].find(h=>/^Teste de ignição/.test(h.textContent));if(!ig||document.getElementById('e5chama'))return;
 const d=document.createElement('div');d.className='el';d.id='e5chama';
 d.innerHTML='<h3>Cor da chama</h3>'
 +'<p>Três ensaios diferentes usam a chama do bico de Bunsen, e cada um responde a uma pergunta.</p>'
 +'<h4>1. Cor da chama da própria amostra</h4>'
 +'<p>Ao queimar a amostra, anote cinco coisas: se pega fogo, a velocidade, a altura da chama, a cor (amarela, amarelo-azulada, azul ou lilás) e a fuligem. Chama amarela e fuliginosa sugere muito carbono, como em aromáticos; quanto mais oxigênio, mais clara (azulada) fica a chama. A leitura está desenhada no teste de ignição, acima.</p>'
 +'<p class="src"><span class="tag sv">Conferido: Analor</span> página &ldquo;Teste de ignição&rdquo;. <span class="tag sv">Conferido: Prof. Flávio Violante</span> Atividade 1 de Análise Orgânica (2025/2), que lista esses cinco parâmetros.</p>'
 +'<h4>2. Alça de cobre (ensaio de Beilstein)</h4>'
 +'<figure class="ens">'+e5Beilstein()+'<figcaption>Esquema do ensaio.</figcaption></figure>'
 +'<p>Leve a amostra à chama numa alça de cobre. Cor <b>verde-azulada</b> indica halogênio (Cl, Br ou I, não F): o halogênio reage com o cobre e leva íons Cu<sup>2+</sup> para a chama.</p>'
 +'<p class="pos"><b>Positivo:</b> chama verde-azulada.</p>'
 +'<p class="fucu"><b>Cuidado:</b> o resultado engana nos dois sentidos. Algumas substâncias nitrogenadas sem halogênio, principalmente derivadas da piridina, também dão verde (cianeto de cobre). E halogenados voláteis podem evaporar da alça antes de reagir e dar negativo. Por isso a apostila não aceita o Beilstein como prova de halogênio: confirme na análise elementar (halogênios).</p>'
 +'<p class="src"><span class="tag sv">Conferido: apostila IFRJ Nilópolis (2016)</span> Parte II, análise elementar qualitativa. A apostila descreve o resultado e as interferências; os passos práticos de limpar e esfriar a alça não estão no trecho que li.</p>'
 +'<h4>3. Resíduo da queima: cor da chama dos metais</h4>'
 +'<p>Se sobrou resíduo inorgânico no teste de ignição, a cor da chama ajuda a ver qual metal há nele (por exemplo, o sódio de um sal de ácido carboxílico).</p>'
 +'<figure class="ens">'+e5ChamaMetais()+'<figcaption>Cores de chama mais citadas.</figcaption></figure>'
 +'<ol class="steps2"><li>Limpe a alça (fio de níquel-cromo ou de platina) com ácido diluído, e queime até a chama não mudar de cor.</li><li>Molhe a alça no resíduo dissolvido, ou toque no resíduo úmido.</li><li>Leve à zona quente da chama e observe a cor nos primeiros segundos.</li></ol>'
 +'<p class="fucu"><b>Cuidado:</b> sódio é muito comum e o amarelo dele esconde os outros metais; para ver o potássio (lilás), olhe a chama por um vidro azul de cobalto. O bário dá cor fraca e curta. A cor sozinha não identifica com certeza.</p>'
 +'<p class="src"><span class="tag sv">Conferido: Creative Chemistry e Royal Society of Chemistry</span> tabelas de cores de chama (Li, Na, K, Ca, Sr, Ba, Cu). Fonte da web, não é da apostila nem do Analor. Os passos 1 a 3 e o vidro azul vêm de roteiros escolares desses sites e da Wikipédia.</p>';
 ig.closest('.el').insertAdjacentElement('afterend',d);
}
function ensInit(){try{e5FichaChama();e5Blocos();e5Funcional();}catch(e){console.error('ensInit',e);}}
