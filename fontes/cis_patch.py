t=open('template.html',encoding='utf-8').read()
def rep(a,c):
    global t
    assert a in t,a[:60]; t=t.replace(a,c,1)
BLOCK='''    <div class="rule"><h3>Cisão homolítica × heterolítica</h3>
      <p>Toda quebra de ligação é de um de dois tipos, e o que muda é <b>para onde vão os 2 elétrons da ligação</b>.</p>
      <p><b>Homolítica:</b> cada lado leva <b>1 elétron</b>. Aparecem elétrons sozinhos (radicais). Seta de <b>anzol</b> (meia ponta), uma para cada elétron.<br><b>Heterolítica:</b> <b>um só lado leva os 2 elétrons</b>. O outro lado fica sem elétron e ganha carga +. Seta <b>inteira</b>, um par de elétrons andando.</p>
      <p class="ex"><b>Exemplo de solução (para fixar a ideia).</b> H3C–CH3 → 2 CH3· é homolítica (1 elétron para cada CH3). H3C–Cl → CH3<sup>+</sup> + Cl<sup>−</sup> é heterolítica (o Cl leva os 2 elétrons).</p>
      <p><b>No espectrômetro as duas acontecem, mas com um detalhe:</b> o íon já tem uma carga +. Então a heterolítica não gera um ânion. Ela gera um <b>cátion + molécula neutra</b>, e o par de elétrons vai para o pedaço neutro.</p>
      <p class="ex"><b>Homolítica (anzol), sai um radical:</b><br>• 1-propanol → CH2=OH<sup>+</sup> (31) + CH3CH2·<br>• 3-pentanona → CH3CH2–C≡O<sup>+</sup> (57) + CH3CH2·<br>• etilbenzeno → C6H5–CH2<sup>+</sup> (91) + CH3·<br>• dimetiletilamina → CH2=N<sup>+</sup>(CH3)2 (58) + CH3·<br>Em todas, o elétron sozinho do O, do N ou do anel pareia com 1 elétron da ligação, e o outro elétron sai com o radical.</p>
      <p class="ex"><b>Heterolítica (seta inteira), sai uma molécula neutra:</b><br>• 3-pentanona: CH3CH2–C≡O<sup>+</sup> (57) → CH3CH2<sup>+</sup> (29) + :C≡O. O par de elétrons da ligação C–C vai para o CO.<br>• benzofenona: C6H5–C≡O<sup>+</sup> (105) → C6H5<sup>+</sup> (77) + CO<br>• pentanal: C4H9–C≡O<sup>+</sup> (85) → C4H9<sup>+</sup> (57) + CO<br>Nos três, o íon é um cátion <b>sem elétron sozinho</b>. Por isso ele solta CO levando o par de elétrons, e não solta radical (regra 6).</p>
      <p><b>McLafferty e abertura de anel:</b> são sequências de passos. Os passos com o elétron sozinho (o H pulando, a quebra do α–β) são de anzol, homolíticos. O que sai no fim é uma molécula neutra.</p>
      <p class="hint">Pista para reconhecer: tem <b>·</b> (elétron sozinho) no pedaço que sai? Então foi homolítica. Saiu uma molécula completa (CO, H2O, C2H4) a partir de um cátion sem ·? Então foi heterolítica. Essa divisão é didática, a lousa do professor pode usar outros nomes.</p></div>

'''
rep('    <div class="rule"><h3>1. O primeiro elétron a sair é o mais fácil de tirar</h3>',BLOCK+'    <div class="rule"><h3>1. O primeiro elétron a sair é o mais fácil de tirar</h3>')
rep("As 7 regras: onde fica o radical, por que sai um pedaço e não outro, o que é McLafferty.","As 7 regras, cisão homolítica e heterolítica, onde fica o radical e o que é McLafferty.")
rep("<p><small><button class=\"back\" style=\"display:inline;margin:0\" data-go=\"p-pq\">Ver as 7 regras</button></small></p></div>';",
    "<p><b>Tipo de cisão.</b> '+cisTxt(row)+'</p><p><small><button class=\"back\" style=\"display:inline;margin:0\" data-go=\"p-pq\">Ver as 7 regras e homolítica × heterolítica</button></small></p></div>';")
rep("function whyBox(ex,row){","""function cisTxt(r){
  const k=tipoQ(r);
  if(k==='neu')return '<b>heterolítica</b>: o cátion solta uma molécula neutra e o par de elétrons da ligação vai com ela (seta inteira).';
  if(k==='anel')return 'começa <b>homolítica</b> (abre a ligação ao lado do heteroátomo, setas de anzol) e termina soltando uma molécula neutra.';
  if(k==='mcl')return '<b>homolítica</b> (setas de anzol): o H pula com 1 elétron e a ligação α–β se rompe, saindo um alqueno neutro.';
  return '<b>homolítica</b> (seta de anzol): cada lado fica com 1 elétron, e o pedaço que sai é um radical.';
}
function whyBox(ex,row){""")
open('template.html','w',encoding='utf-8').write(t)
