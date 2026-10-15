# IONI[n] = (resumo, [(onde, nivel, porque)])  nivel: 1 = é daqui que sai; 0 = não sai daqui; 2 = quase empata (não entra no treino)
IONI = {
1: ("Não há par livre, então sai um elétron π do anel.", [
  ("Um elétron π do anel aromático", 1, "O etilbenzeno não tem par livre. O π está espalhado pelos 6 carbonos do anel e fica fora do eixo das ligações, então é o elétron mais fácil de tirar."),
  ("Um elétron σ da ligação C–C do etila", 0, "O σ fica entre dois núcleos, bem no eixo, bem preso. Tirar um σ pede mais energia do que tirar um π."),
  ("Um elétron σ de uma C–H", 0, "Mesma razão: σ é mais preso que π. A C–H é ainda mais difícil que a C–C.")]),
2: ("Sai do conjunto π do anel, que já inclui um par do O.", [
  ("Um elétron do conjunto π do anel (que inclui um par do O)", 1, "No furano, um dos pares do O faz parte do sexteto aromático. O orbital mais alto ocupado é desse conjunto π, então é de lá que sai o elétron."),
  ("O outro par livre do O (no plano do anel)", 0, "Esse par fica no plano da molécula, perpendicular ao π. Ele está mais baixo em energia, então é mais difícil de tirar."),
  ("Um elétron σ de C–H ou C–C", 0, "σ é mais preso que o π e que os pares livres.")]),
3: ("Sai do π conjugado de anel + vinila.", [
  ("Um elétron π do sistema conjugado (anel + vinila)", 1, "Anel e vinila formam um único sistema π de 8 carbonos. Quanto maior a conjugação, mais o elétron se espalha e mais fácil é tirá-lo. Por isso é mais fácil que num benzeno simples."),
  ("Um elétron σ da ligação anel–vinila", 0, "σ é mais preso que π. A quebra desta ligação só acontece depois, como fragmentação (pico 77)."),
  ("Um elétron σ de uma C–H", 0, "Mesma razão: σ é a última opção.")]),
4: ("Sai do par livre do O da carbonila.", [
  ("O par livre (n) do O do C=O", 1, "O par livre não faz parte de nenhuma ligação, então fica mais frouxo que π e σ. Em cetona, é o elétron mais fácil de tirar. A lousa e o livro desenham o ·+ no O."),
  ("Um elétron π de um dos anéis", 2, "A energia dos π dos anéis é parecida com a do par livre, e é por isso que a carga pode ficar espalhada no anel. Mas o mecanismo da lousa parte do O."),
  ("O elétron π do C=O", 0, "O π do C=O fica entre C e O e é bem mais preso que o par livre do O."),
  ("Um elétron σ de C–C ou C–H", 0, "σ é o mais difícil de tirar.")]),
5: ("Sai do par livre do O da carbonila.", [
  ("O par livre (n) do O do C=O", 1, "Sem anel, o par livre do O é o elétron mais frouxo da molécula: não está em ligação nenhuma."),
  ("O elétron π do C=O", 0, "O π do C=O fica entre dois átomos e é bem mais preso que o par livre."),
  ("Um elétron σ da ligação C–C α", 0, "σ é o mais preso. A ligação α quebra depois, como clivagem α, mas é o ·+ no O que comanda isso.")]),
6: ("Sai do par livre do O do álcool.", [
  ("Um par livre do O", 1, "Dos elétrons da molécula, só os pares livres do O não estão numa ligação. Por isso são os mais fáceis de tirar."),
  ("Um elétron σ da ligação C–O", 0, "σ está no eixo entre dois núcleos: bem preso."),
  ("Um elétron σ da ligação O–H", 0, "Mesma razão."),
  ("Um elétron σ da ligação C–C", 0, "Mesma razão. A C–C quebra depois (clivagem α), puxada pelo ·+ do O.")]),
7: ("Sai do par livre de um dos dois O (tanto faz qual).", [
  ("Um par livre de um dos O", 1, "Os pares livres do O são os elétrons mais frouxos. Os dois O são iguais, então tanto faz de qual sai: o desenho vale para qualquer um."),
  ("Um elétron σ da ligação C–O", 0, "σ é mais preso que o par livre."),
  ("Um elétron σ da ligação C–C", 0, "Mesma razão.")]),
8: ("Sai do N, mas o par livre e o π do anel quase empatam.", [
  ("O par livre do N (no plano do anel)", 1, "É o que a lousa e o livro desenham. O par livre do N não participa do sexteto aromático."),
  ("Um elétron π do anel aromático", 2, "Na piridina, a energia do par livre e a do π são muito parecidas, então não dá para decidir só por regra. O livro desenha o ·+ no N."),
  ("Um elétron σ de C–H", 0, "σ é o mais preso."),
  ("Um elétron σ da ligação C–N do anel", 0, "Mesma razão: σ é mais preso que o par livre.")]),
9: ("Sai do par livre do O do C=O, não do O do OH.", [
  ("O par livre do O do C=O", 1, "Esse par fica no plano da molécula e não participa de ressonância. É o mais frouxo."),
  ("O par livre do O do OH", 0, "Este O empresta elétrons ao C=O por ressonância (O–C=O ↔ +O=C–O−). Isso deixa o par mais preso, então é mais difícil de tirar."),
  ("O elétron π do C=O", 0, "O π do C=O é mais preso que o par livre."),
  ("Um elétron σ", 0, "σ é o último da fila.")]),
10: ("Sai do par livre do N, que o N segura mais frouxo que o O.", [
  ("O par livre do N", 1, "O N é menos eletronegativo que o O, então segura o par livre mais frouxo. Por isso aminas perdem o elétron mais fácil que álcoois e éteres."),
  ("Um elétron σ da ligação C–N", 0, "σ é bem mais preso que o par livre."),
  ("Um elétron σ da ligação C–C", 0, "Mesma razão."),
  ("Um elétron σ de uma C–H", 0, "Mesma razão.")]),
11: ("Sai do par livre do O do C=O, não do O do OCH3.", [
  ("O par livre do O do C=O", 1, "Esse par fica no plano e não participa de ressonância. É o mais frouxo do éster."),
  ("O par livre do O do OCH3", 0, "Este O empresta elétrons ao C=O por ressonância, o que deixa o par mais preso."),
  ("O elétron π do C=O", 0, "O π do C=O é mais preso que o par livre."),
  ("Um elétron σ", 0, "σ é o mais difícil.")]),
12: ("Sai do par livre do O do CHO.", [
  ("O par livre do O do C=O", 1, "O par livre do O não está em ligação nenhuma. Em aldeído, é o elétron mais fácil de tirar."),
  ("O elétron π do C=O", 0, "O π do C=O fica entre C e O e é mais preso que o par livre."),
  ("O elétron σ da C–H do CHO", 0, "σ é mais preso que o par livre. Esta C–H sai depois, no pico M − 1."),
  ("Um elétron σ de C–C", 0, "Mesma razão.")]),
}
