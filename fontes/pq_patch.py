import re, json
w=open('why.py',encoding='utf-8').read()
w=w.replace("A ligação C–O vizinha ao ·+ é a mais fraca. O CO que sai é muito estável (ligação tripla), e essa estabilidade empurra a reação.","O CO que sai é uma molécula neutra muito estável (ligação tripla), e essa estabilidade ajuda a reação a acontecer.")
w=w.replace(" Por isso a quebra de ligação do anel não acontece nesse passo.","")
open('why.py','w',encoding='utf-8').write(w)

b=open('build3.py',encoding='utf-8').read()
if 'const WHY=' not in b:
    b=b.replace('import re, json','import re, json, sys\nsys.path.insert(0,".")\nfrom why import WHY',1)
    old='json.dumps(out,ensure_ascii=False)+";\\n"'
    assert old in b
    b=b.replace(old,old+'+"const WHY="+json.dumps({f"{k[0]}:{k[1]}":list(v) for k,v in WHY.items()},ensure_ascii=False)+";\\n"')
    open('build3.py','w',encoding='utf-8').write(b)

t=open('template.html',encoding='utf-8').read()
def rep(a,c):
    global t
    assert a in t,a[:70]; t=t.replace(a,c,1)

# ---- paletas (Verde = original, sem override)
def css(name,L,D):
    f=lambda d:';'.join(f'--{k}:{v}' for k,v in d.items())
    return (f':root[data-pal="{name}"]{{{f(L)}}}\n@media (prefers-color-scheme:dark){{:root:not([data-theme="light"])[data-pal="{name}"]{{{f(D)}}}}}\n:root[data-theme="dark"][data-pal="{name}"]{{{f(D)}}}\n')
PAL={
 'azul':(dict(bg='#F3F6FA',surface='#FFFFFF',ink='#14202E',muted='#566677',line='#D5DEE8',keep='#1F5FA8',focus='#1F5FA8'),
         dict(bg='#0D1218',surface='#151C26',ink='#E3EAF2',muted='#93A3B5',line='#26323F',keep='#6FB1F0',focus='#6FB1F0')),
 'roxo':(dict(bg='#F6F4FA',surface='#FFFFFF',ink='#1E1830',muted='#655C7A',line='#DDD7EA',keep='#6B3FA0',focus='#6B3FA0'),
         dict(bg='#130F1A',surface='#1C1726',ink='#EBE4F5',muted='#A99DC0',line='#30283F',keep='#B794E8',focus='#B794E8')),
 'grafite':(dict(bg='#F4F4F3',surface='#FFFFFF',ink='#1D1D1B',muted='#5F5F5B',line='#DADAD6',keep='#3F5A66',focus='#3F5A66'),
         dict(bg='#121212',surface='#1B1B1B',ink='#E6E6E3',muted='#9A9A95',line='#2D2D2D',keep='#8FB3C2',focus='#8FB3C2')),
}
SOFT={'azul':('#DDE9F6','#172F4A'),'roxo':('#E9E0F5','#2E1F47'),'grafite':('#E1E9EC','#243238')}
out=''
for n,(L,D) in PAL.items():
    L=dict(L,**{'keep-soft':SOFT[n][0]}); D=dict(D,**{'keep-soft':SOFT[n][1]})
    out+=css(n,L,D)
EXTRA=out+'''
.why{margin-top:12px;background:var(--note-soft);border-radius:6px;padding:10px 14px;font-size:.93rem}
.why h4{margin:0 0 6px;font-size:.8rem;letter-spacing:.06em;text-transform:uppercase;color:var(--note)}
.why p{margin:0 0 6px}.why p:last-child{margin:0}
.why b{font-weight:600}
.rule{background:var(--surface);border:1px solid var(--line);border-radius:6px;padding:12px 14px;margin-bottom:10px}
.rule h3{margin:0 0 4px;font-size:1rem}
.rule p{margin:0 0 6px}.rule p:last-child{margin:0}
.rule .ex{background:var(--keep-soft);border-radius:6px;padding:8px 10px;font-size:.92rem}
.pal{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:10px;margin-top:10px}
.pal button{font:inherit;text-align:left;background:var(--surface);color:var(--ink);border:2px solid var(--line);border-radius:6px;padding:10px;cursor:pointer;display:grid;gap:6px}
.pal button[aria-pressed="true"]{border-color:var(--keep)}
.pal i{display:flex;height:22px;border-radius:4px;overflow:hidden;border:1px solid var(--line)}
.pal i s{flex:1}
'''
rep('*{box-sizing:border-box}',EXTRA+'*{box-sizing:border-box}')

# ---- menu Mais
rep('''      <button class="mi" type="button" data-go="p-aj">''','''      <button class="mi" type="button" data-go="p-pq"><b>Por que a ligação quebra ali?</b><span>As 7 regras: onde fica o radical, por que sai um pedaço e não outro, o que é McLafferty.</span></button>
      <button class="mi" type="button" data-go="p-co"><b>Cor do app</b><span>Escolha o tom que for mais confortável para você.</span></button>
      <button class="mi" type="button" data-go="p-aj">''')

RULES='''
  <section id="p-pq" role="region" aria-label="Por que a ligação quebra ali" hidden>
    <button class="back" data-go="p-ma">← Mais</button>
    <h2 class="scr">Por que a ligação quebra ali?</h2>
    <p class="hint">Cada quebra tem um motivo. Estas 7 regras explicam quase todos os exercícios. Cada exercício, no cartão do pico, tem o &ldquo;Por que quebra aqui?&rdquo; com a regra aplicada.</p>

    <div class="rule"><h3>Antes de tudo: o que é o &ldquo;radical que some&rdquo;?</h3>
      <p>No espectrômetro, a molécula perde 1 elétron e vira <b>M<sup>+·</sup></b>: tem <b>carga</b> (+) e um <b>elétron sozinho</b> (·). Quando ela quebra em 2 pedaços, só <b>um</b> fica com a carga e é visto no espectro. O outro pedaço é <b>neutro</b> e some, porque o aparelho só enxerga o que tem carga.</p>
      <p>O elétron sozinho vai para um dos dois pedaços. Se ele vai para o pedaço neutro, esse pedaço é um <b>radical</b> (·CH3, por exemplo) e o íon que sobra é um cátion sem elétron sozinho. Se o pedaço neutro é uma molécula completa (CH2=CH2, CO, H2O), o elétron sozinho fica no íon (+·).</p>
      <p class="ex"><b>Contagem para a N,N-dimetiletilamina → 58.</b> M<sup>+·</sup> tem o N com 1 elétron sozinho (ex-par livre). Esse elétron forma a ligação dupla C=N com 1 elétron da ligação C–C vizinha. O outro elétron dessa ligação C–C sai com o CH3, que vira CH3· (radical, neutro, some). Sobra CH2=N<sup>+</sup>(CH3)2: a carga ficou no N, sem elétron sozinho. 73 − 15 = 58.</p>
      <p><b>Setas:</b> seta de ponta inteira = 2 elétrons andando. Seta de anzol (meia ponta) = 1 elétron andando. É por isso que o professor usa anzol nos mecanismos de massa.</p>
    </div>

    <div class="rule"><h3>1. O primeiro elétron a sair é o mais fácil de tirar</h3>
      <p>A ordem do que é mais fácil de arrancar é: <b>par livre (N, O)</b> &lt; <b>elétrons π</b> (C=O, C=C, anel) &lt; <b>elétrons σ</b> (C–C, C–H). Por isso o elétron sozinho (·+) começa no heteroátomo ou no π, e é daí que a quebra começa.</p>
      <p class="ex">Amina: ·+ no N. Álcool, éter, cetona, aldeído, éster: ·+ no O. Benzeno, estireno: ·+ no anel.</p></div>

    <div class="rule"><h3>2. Clivagem α: o elétron sozinho &ldquo;puxa&rdquo; a ligação do lado</h3>
      <p>O elétron sozinho do N ou do O forma uma <b>2ª ligação</b> com 1 elétron da ligação vizinha (C–C, a ligação α). O outro elétron dessa ligação sai junto com o grupo, que vira radical. O heteroátomo fica com ligação dupla (C=N<sup>+</sup>, C=O<sup>+</sup>) e a carga fica nele.</p>
      <p class="ex">Exemplos: 1-propanol → CH2=OH<sup>+</sup> (31); 3-pentanona → CH3CH2–C≡O<sup>+</sup> (57); dimetiletilamina → CH2=N<sup>+</sup>(CH3)2 (58).</p></div>

    <div class="rule"><h3>3. Por que a carga fica ali e não no outro pedaço?</h3>
      <p>A carga fica no pedaço onde ela é mais <b>estável</b>. Quatro coisas estabilizam uma carga +:</p>
      <p>• <b>Par livre do vizinho</b> que doa elétrons (N doa melhor que O): C=N<sup>+</sup> (imínio), C=O<sup>+</sup> (oxônio).<br>• <b>Ressonância</b>: benzila/tropílio, acílio (R–C≡O<sup>+</sup>), alila.<br>• <b>Mais carbonos ligados</b> ao C<sup>+</sup> (terciário &gt; secundário &gt; primário).<br>• <b>Aromaticidade</b> (ciclopropenil, tropílio).</p>
      <p>O pico base é, quase sempre, o íon mais estável que se forma fácil.</p></div>

    <div class="rule"><h3>4. Quando há duas ligações possíveis, sai o grupo maior</h3>
      <p>O radical que sai também tem que ser estável. Radical maior espalha melhor o elétron sozinho. Então, com duas opções de clivagem α, tende a sair o <b>maior</b> grupo alquila.</p>
      <p class="ex">Pentanal → 29 (HC≡O<sup>+</sup>): sai o butila (C4H9·). Metila de éster: sai ·OCH3 (31) e também o butila (59), mas o 85 é o maior.</p></div>

    <div class="rule"><h3>5. McLafferty: o H que &ldquo;pula&rdquo; para o O</h3>
      <p>Precisa de um C=O e de um <b>H no carbono γ</b> (a 3 carbonos do C=O: C=O, α, β, γ). O O (·+) alcança esse H por um anel de <b>6 átomos</b>, onde as distâncias e os ângulos encaixam. O H passa para o O (1 elétron do H pareia o elétron sozinho do O). Agora o elétron sozinho está no carbono γ. Ele forma uma ligação dupla com o β e a ligação α–β quebra. Sai um <b>alqueno neutro</b>, e o íon que sobra é um enol (+·).</p>
      <p class="ex">O elétron sozinho &ldquo;aparece em outro lugar&rdquo; porque o H, que leva 1 elétron, passou para o O. Ácido butanoico → 60; pentanoato de metila → 74; pentanal → 44.</p></div>

    <div class="rule"><h3>6. Íon de elétrons pares solta molécula neutra, não radical</h3>
      <p>Um cátion sem elétron sozinho (R<sup>+</sup>, R–C≡O<sup>+</sup>) <b>não</b> quebra soltando um radical, porque isso daria um íon-radical instável. Ele solta uma <b>molécula neutra estável</b> pequena: CO (28), C2H4 (28), C2H2 (26), H2O (18), HCN (27), CH2O (30).</p>
      <p class="ex">Acílio perde CO: 85 → 57, 105 → 77, 57 → 29. Butila perde eteno: 57 → 29. É por isso que as perdas &ldquo;entre picos&rdquo; quase sempre são moléculas neutras.</p></div>

    <div class="rule"><h3>7. Perda de H· (M − 1) e abertura de anel</h3>
      <p><b>M − 1:</b> sai o H mais fraco, que é o ligado ao carbono vizinho do heteroátomo (ou o H do CHO). Com o H fora, o heteroátomo fecha ligação dupla e a carga fica nele.</p>
      <p><b>Anel:</b> quebrar 1 ligação do anel não separa nada. Precisa de duas quebras: primeiro abre ao lado do heteroátomo, depois sai uma molécula neutra pequena e estável (CO, CH2O, HCN).</p></div>

    <p class="hint">Fonte dos princípios: Silverstein et al., cap. 1 (fragmentação de EI) e as lousas do professor. As regras são tendências, não leis: quando o exercício e a regra discordarem, vale a lousa.</p>
  </section>

  <section id="p-co" role="region" aria-label="Cor do app" hidden>
    <button class="back" data-go="p-ma">← Mais</button>
    <h2 class="scr">Cor do app</h2>
    <p class="hint">Toque numa cor. Ela fica salva neste aparelho. O vermelho e o âmbar dos cartões (o que saiu e o aviso) não mudam, para o significado continuar o mesmo.</p>
    <div class="pal" id="pals"></div>
  </section>

'''
rep('  <section id="p-fo" role="region" aria-label="Fontes e avisos" hidden>',RULES+'  <section id="p-fo" role="region" aria-label="Fontes e avisos" hidden>')
rep("const SCR=['p-an','p-tr','p-tb','p-iv','p-ma','p-ca','p-aj','p-fo'];","const SCR=['p-an','p-tr','p-tb','p-iv','p-ma','p-ca','p-aj','p-fo','p-pq','p-co'];")
rep("const OWN={'p-ca':'t-ma','p-aj':'t-ma','p-fo':'t-ma'};","const OWN={'p-ca':'t-ma','p-aj':'t-ma','p-fo':'t-ma','p-pq':'t-ma','p-co':'t-ma'};")

# ---- card "Por que quebra aqui?"
rep("""   '</ol><div class="sp">'+mapFig(ex,row[0])+strucPair(row)+'</div>';""","""   '</ol>'+whyBox(ex,row)+'<div class="sp">'+mapFig(ex,row[0])+strucPair(row)+'</div>';""")
rep("function stepCard(ex,row){","""function whyBox(ex,row){
  const w=(typeof WHY!=='undefined')&&WHY[ex.n+':'+row[0]];if(!w)return '';
  return '<div class="why"><h4>Por que quebra aqui?</h4><p><b>Onde começa.</b> '+esc(w[0])+'</p><p><b>O que acontece.</b> '+fmt(esc(w[1]))+'</p><p><b>Por que aqui e não em outro lugar.</b> '+fmt(esc(w[2]))+'</p><p><small><button class="back" style="display:inline;margin:0" data-go="p-pq">Ver as 7 regras</button></small></p></div>';
}
function stepCard(ex,row){""")

# ---- paletas JS
PALJS='''
/* ---------- cor do app ---------- */
const PALS=[['azul','Azul','#1F5FA8','#DDE9F6','#F3F6FA'],['grafite','Grafite','#3F5A66','#E1E9EC','#F4F4F3'],['roxo','Roxo','#6B3FA0','#E9E0F5','#F6F4FA'],['verde','Verde (o antigo)','#0F6E56','#DCEFE8','#F2F6F5']];
function setPal(n){
  const r=document.documentElement;
  if(n==='verde')r.removeAttribute('data-pal');else r.setAttribute('data-pal',n);
  try{localStorage.setItem('massas-pal',n);}catch(e){}
  const p=PALS.find(x=>x[0]===n);const m=document.querySelector('meta[name="theme-color"]');if(m&&p)m.setAttribute('content',p[2]);
  drawPals();
}
function drawPals(){
  const cur=document.documentElement.getAttribute('data-pal')||'verde';const box=$('#pals');if(!box)return;box.innerHTML='';
  PALS.forEach(p=>{const b=document.createElement('button');b.type='button';b.setAttribute('aria-pressed',cur===p[0]?'true':'false');
    b.innerHTML='<i><s style="background:'+p[4]+'"></s><s style="background:'+p[3]+'"></s><s style="background:'+p[2]+'"></s></i><b>'+p[1]+'</b>';
    b.onclick=()=>setPal(p[0]);box.appendChild(b);});
}
(function(){let n='azul';try{n=localStorage.getItem('massas-pal')||'azul';}catch(e){}
  if(!PALS.some(x=>x[0]===n))n='azul';setPal(n);})();
'''
rep("const SCR=[",PALJS+"const SCR=[")
open('template.html','w',encoding='utf-8').write(t)
print('ok')
