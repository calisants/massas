/* ================= ANALORG v4: Análise funcional em uma tela só ================= */
/* Fonte dos procedimentos: Apostila de Análise Orgânica, IFRJ Nilópolis (2016), Parte III, números de procedimento indicados.
   Fonte dos reagentes: Receituário de reagentes do IFRJ (e a tabela de receitas da mesma apostila). As cores dos tubos são aproximadas, desenhadas
   a partir do que o texto descreve. Onde apostila e receituário divergem, o item traz a nota. */
const FUG=[
 ['hid','Alcenos e aromáticos'],['alc','Álcoois e éteres'],['fen','Fenóis'],['car','Aldeídos e cetonas'],['est','Ésteres e amidas'],['ami','Aminas e aminoácidos']
];
const FUN=[
 {g:'hid',n:'Bromo (alcenos e alcinos)',p:19,
  pr:'O bromo adiciona à ligação dupla ou tripla e o reagente avermelhado descora.',
  rg:[['Bromo em tetracloreto de carbono (5% p/v)','Dissolver 0,5 g (0,16 mL) de bromo em 10 mL de CCl₄. Os vapores de bromo são cáusticos: guarde e use na capela.'],['Água de bromo (3,5% p/v)','Dissolver 3,5 g (1,1 mL) de bromo em 100 mL de água. Dura 30 dias.']],
  st:['Se a amostra é sólida, dissolva antes em água (use a água de bromo) ou em CCl₄ (use o bromo em CCl₄).','Junte a amostra ao reagente.','Compare com o branco e com o controle.'],
  pos:'O reagente avermelhado descora.',
  cu:'Enóis, fenóis, aminas aromáticas e metilcetonas também gastam bromo, por substituição. Nesse caso sai HBr: aparecem bolhas e um papel de tornassol azul úmido fica vermelho. Na adição só há descoramento. Compostos aromáticos não descoram.',
  c:['#d9531e','#f1f1ec'],l:['bromo','incolor']},
 {g:'hid',n:'Bayer (permanganato neutro)',p:20,
  pr:'O permanganato reage com a ligação dupla e forma um glicol. Ele descora e, às vezes, aparece um precipitado marrom de MnO₂.',
  rg:[['Bayer (KMnO₄ neutro, 1% p/v)','Dissolver 0,1 g de permanganato de potássio e 0,1 g de sulfato de magnésio em 10 mL de água. O sulfato de magnésio mantém o meio neutro.']],
  st:['Dissolva a amostra em 1 gota de água. Se não dissolver, use etanol ou acetona.','Junte o reagente de Bayer.','Compare com o branco. O etanol sozinho também reduz o permanganato em uns 5 minutos.'],
  pos:'O violeta descora.',
  cu:'O permanganato é oxidante forte: qualquer grupo redutor também descora. Nem sempre se vê o precipitado marrom.',
  c:['#7b1fa2','#e7ddd2'],l:['violeta','descorado']},
 {g:'hid',n:'Le Rosen (formol e ácido sulfúrico)',p:21,
  pr:'Aromáticos condensam com o formaldeído em H₂SO₄ concentrado e dão cor intensa. Alifáticos não dão.',
  rg:[['Le Rosen','Dissolver 1 gota de formol (37% p/v) em 1 mL de H₂SO₄ 98%. Prepare na hora e só a quantidade que vai usar.']],
  st:['Num vidro de relógio ou placa de toque, trate a amostra com 5 gotas de H₂SO₄ concentrado e anote a cor.','Junte 2 gotas de formol.','Compare a cor nova com a anotada. O meio deve ter o mínimo de água.'],
  pos:'A cor aparece ou muda em relação à do H₂SO₄ sozinho. Exemplos da apostila: benzeno, tolueno e fenol dão vermelho (fenol vermelho-violeta), naftaleno e fenantreno dão verde, bifenila dá azul-esverdeado, estilbeno e mesitileno dão castanho.',
  cu:'Aromáticos com grupos retiradores (nitro, carbonila, carboxila, ciano) não dão. Por isso positivo prova aromático, mas negativo pode ser alifático ou aromático desativado.',
  c:['#efefe8','#c62828'],l:['H₂SO₄ + formol','vermelho']},

 {g:'alc',n:'Nitrato cérico amoniacal',p:22,
  pr:'O Ce(IV) forma um complexo vermelho com o álcool, que depois se desfaz quando o álcool é oxidado.',
  rg:[['Nitrato cérico (40% p/v)','Dissolver 4 g de nitrato cérico amoniacal, aquecendo, em 10 mL de HNO₃ 5% p/v.']],
  st:['Dissolva a amostra em 1 gota de água ou de dioxana.','Junte 1 gota do reagente.'],
  pos:'Amarelo passa a vermelho (álcoois de até 10 C).',
  cu:'O complexo dura de segundos a horas, mais com terciários, depois secundários e por último primários. Compostos nitrogenados e sulfurados interferem.',
  c:['#f2c230','#c0392b'],l:['amarelo','vermelho']},
 {g:'alc',n:'Xantato (álcoois primários e secundários)',p:23,
  pr:'O álcool vira alcóxido, reage com CS₂ e dá xantato, que forma um complexo violeta com molibdato.',
  rg:[['Molibdato de amônio (5% p/v)','Dissolver 0,5 g de molibdato de amônio em 10 mL de água.'],['Dissulfeto de carbono','Usar direto.'],['Ácido clorídrico 5%','Diluir 13 mL de HCl concentrado (d = 1,19) a 100 mL com água.']],
  st:['Em microtubo, ponha partes iguais de amostra e NaOH em pastilha, ambos sem água. Use óculos de segurança ao quebrar pastilhas.','Aqueça rápido na chama até o NaOH dissolver e deixe esfriar.','Junte 1 gota de CS₂ e 1 gota de molibdato.','Acidule com HCl 5% até pH ácido.'],
  pos:'Cor violeta. Se o álcool não tiver outros grupos hidrofílicos, o complexo passa para CHCl₃ ou CCl₄.',
  cu:'Álcoois terciários, na prática, não formam xantato.',
  c:['#efefef','#7b1fa2'],l:['incolor','violeta']},
 {g:'alc',n:'Jones (álcoois primários e secundários)',p:24,
  pr:'O Cr(VI) laranja oxida o álcool e vira Cr(III) azul-esverdeado. Terciário não reage.',
  rg:[['Jones (ácido crômico 15% p/v)','Dissolver 1,5 g de ácido crômico em 1,2 mL de H₂SO₄ 98% e diluir com cuidado até 10 mL com água. (A apostila dá outra receita: suspender 25 g de CrO₃ em 25 mL de H₂SO₄ concentrado e verter devagar, agitando, em 75 mL de água; esfriar antes de usar.)']],
  st:['Ponha a amostra num tubo com 1 mL de acetona.','Junte 1 gota do reagente de Jones.','Anote o que acontece nos primeiros 2 segundos.'],
  pos:'Laranja passa a verde em até 2 segundos.',
  cu:'Aldeídos também são oxidados e dão positivo. Cetonas dão negativo, então o ensaio separa aldeído de cetona.',
  c:['#e67e22','#2f8f6b'],l:['laranja','verde']},
 {g:'alc',n:'Lucas (álcoois secundários e terciários)',p:25,
  pr:'O álcool é protonado e vira cloreto de alquila, que é insolúvel e separa do meio.',
  rg:[['Lucas','Dissolver 13,6 g de ZnCl₂ anidro em 10,5 g de HCl concentrado, resfriando. Prepare na hora.']],
  st:['Ponha 2 mL do reagente de Lucas num microtubo e junte a amostra.','Feche, agite e deixe em repouso.','Anote quanto tempo leva para aparecer uma segunda camada ou uma emulsão.'],
  pos:'Forma-se uma segunda camada ou emulsão. Terciário reage mais depressa que secundário.',
  cu:'A apostila não traz tempos de referência para este ensaio, então use o controle (um álcool terciário e um primário) para calibrar o seu olho.',
  c:['#efefef','#d9d6c6'],l:['limpo','turvo']},
 {g:'alc',n:'Malaprade (glicóis vicinais)',p:26,
  pr:'O periodato quebra a ligação entre os dois C com OH e forma iodato. O nitrato de prata mostra o iodato como precipitado branco de AgIO₃.',
  rg:[['Malaprade (HIO₃/AgNO₃)','Dissolver 0,15 g de periodato de potássio em 8 mL de água. Nessa solução, dissolver 0,05 g de AgNO₃ e 0,5 mL de HNO₃ concentrado e completar a 10 mL. Se formar precipitado, filtrar.']],
  st:['Primeiro teste a amostra só com nitrato de prata. Se der precipitado branco, não continue.','Dissolva a amostra em etanol ou etanol-água.','Junte o reagente de Malaprade e deixe 5 minutos à temperatura ambiente.'],
  pos:'Precipitado branco.',
  cu:'Faça o branco e o controle junto.',
  c:['#efefef','#fbfbfb'],l:['limpo','precipitado branco']},
 {g:'alc',n:'Iodo em diclorometano (éteres)',p:27,
  pr:'O oxigênio ou o nitrogênio forma com o iodo um complexo de transferência de carga castanho.',
  rg:[['Iodo em diclorometano','Adicionar 2 cristais de iodo a 100 mL de CH₂Cl₂. Manter o frasco bem fechado.']],
  st:['Junte um pouco da amostra à solução de iodo.','Observe nos primeiros instantes, porque os complexos são instáveis.'],
  pos:'Púrpura passa a castanho.',
  cu:'Alguns álcoois e cetonas também dão. Hidrocarbonetos insaturados formam um sólido castanho claro e a cor púrpura não muda. Aromáticos, alcanos e cloretos ou fluoretos de alquila e arila não reagem. Use junto com outros ensaios de funções oxigenadas.',
  c:['#7b1fa2','#6d4c41'],l:['púrpura','castanho']},

 {g:'fen',n:'Cloreto férrico (fenóis)',p:28,
  pr:'O Fe³⁺ forma um complexo colorido com a hidroxila fenólica.',
  rg:[['Cloreto férrico 1% (aquoso)','Dissolver 0,1 g de FeCl₃ em 10 mL de água. Dura 30 dias.'],['Cloreto férrico em clorofórmio (1% p/v)','Dissolver 0,1 g de FeCl₃ em 10 mL de CHCl₃. Para fenóis insolúveis em água.']],
  st:['Trate a amostra com o FeCl₃ aquoso 1%.','Para fenol insolúvel em água, use o FeCl₃ em clorofórmio e junte 1 gota de piridina.'],
  pos:'Vermelho-vinho ou verde (em clorofórmio com piridina, a cor passa ao vermelho).',
  cu:'Oximas e ácidos hidroxâmicos também dão vermelho. Nitrofenóis não reagem. O ácido salicílico e os hidroxibenzaldeídos reagem bem. É o ensaio para fenóis com as posições orto e para ocupadas, em que Libermann e cobaltinitrito dão negativo.',
  c:['#f0e29a','#7b1e3a'],l:['amarelo claro','vinho']},
 {g:'fen',n:'Libermann (fenol com posição para livre)',p:29,
  pr:'O ácido nitroso nitrosa a posição para e o produto condensa com outro fenol e forma um indofenol colorido.',
  rg:[['Libermann (ácido nitroso em H₂SO₄)','Dissolver 0,1 g de NaNO₂ em 1 mL de H₂SO₄ 98%. Prepare na hora.']],
  st:['Trate a amostra com o reagente de Libermann (uma pequena porção de NaNO₂ com cerca de 5 gotas de H₂SO₄ concentrado).','Se quiser, dilua com cuidado com 1 gota de água.'],
  pos:'Cor intensa, em geral vermelha. Na maioria das vezes passa a azul e intensifica com a diluição.',
  cu:'Éteres fenólicos e tiofenas também dão cor intensa. Nitrofenóis não reagem.',
  c:['#efefef','#c62828'],l:['incolor','vermelho']},
 {g:'fen',n:'Cobaltinitrito (fenol com posição orto livre)',p:30,
  pr:'O cobaltinitrito nitrosa a posição orto e o o-nitrosofenol forma um quelato castanho com cobalto.',
  rg:[['Cobaltinitrito de sódio 5% (aquoso)','Dissolver 0,5 g de cobalto-hexanitrito de sódio em 10 mL de água. Instável: prepare pouco antes. A apostila descreve outro preparo: uma pequena porção de cobaltinitrito com 1 mL de água e igual volume de ácido acético glacial.']],
  st:['Trate a amostra com 4 gotas do reagente.','Aqueça em banho-maria por 5 minutos.','Para enxergar melhor, junte 3 gotas de CHCl₃ e extraia o complexo.'],
  pos:'Amarelo escuro passa a castanho.',
  cu:'O branco, ao aquecer, vai de amarelo a rosa claro. Carboxila e carbonila no anel (ácido salicílico, por exemplo) não impedem a reação.',
  c:['#b58a12','#6d4c41'],l:['amarelo escuro','castanho']},

 {g:'car',n:'2,4-dinitrofenilidrazina (aldeídos e cetonas)',p:31,
  pr:'O carbonilo condensa com a hidrazina e forma uma 2,4-dinitrofenilidrazona colorida.',
  rg:[['2,4-DNPH (3% p/v em etanol)','Dissolver 3 g de 2,4-dinitrofenilidrazina em 15 mL de H₂SO₄ concentrado. Juntar essa solução, agitando, a 20 mL de água e 70 mL de etanol. Misturar e filtrar.']],
  st:['Dissolva a amostra em 1 gota de etanol.','Junte o reagente 2,4-DNPH.'],
  pos:'Precipitado amarelo (carbonila alifática) ou laranja a vermelho (aromática ou conjugada).',
  cu:'Não separa aldeído de cetona. Para isso use Tollens, Fehling ou Schiff.',
  c:['#f7d28a','#e0831f'],l:['reagente','precipitado laranja']},
 {g:'car',n:'m-dinitrobenzeno (cetonas com –CH₂–CO–)',p:32,
  pr:'Cetonas com CH₂ vizinho à carbonila dão um composto violeta em meio alcalino. A estrutura ainda não foi bem esclarecida.',
  rg:[['1,3-dinitrobenzeno (1% p/v em etanol)','Dissolver 0,1 g de m-dinitrobenzeno em 10 mL de etanol.'],['KOH alcoólico','Usar uma solução alcoólica de hidróxido de potássio (a concentração não consta no receituário).']],
  st:['Dissolva a amostra em 1 gota de etanol.','Junte o reagente de m-dinitrobenzeno.','Junte 1 gota de KOH alcoólico.'],
  pos:'Cor violeta.',
  cu:'É específico para esse tipo de cetona. Aldeídos, alifáticos ou aromáticos, não reagem.',
  c:['#efefef','#7b1fa2'],l:['incolor','violeta']},
 {g:'car',n:'Índigo com o-nitrobenzaldeído (metilcetonas)',p:33,
  pr:'A metilcetona condensa com o-nitrobenzaldeído em meio alcalino e forma índigo (reação de Bayer, 1882).',
  rg:[['Aldeído 2-nitrobenzoico (5% p/v em CHCl₃)','Dissolver 0,5 g em 10 mL de clorofórmio. Dura 7 dias.'],['NaOH 5%','Dissolver 5 g de NaOH em 100 mL de água.']],
  st:['Trate a amostra com o reagente o-nitrobenzaldeído e depois com NaOH 5%.','Aqueça em banho-maria e esfrie.','Extraia com clorofórmio.'],
  pos:'Cor azul (anil) na fase clorofórmica.',
  cu:'Se houver álcool, a fase clorofórmica fica vermelha em vez de azul.',
  c:['#efefef','#2c4a9a'],l:['incolor','azul']},
 {g:'car',n:'Iodofórmio (metilcetonas)',p:34,
  pr:'A metila vizinha à carbonila é iodada várias vezes em meio básico e a ligação C–C se rompe, liberando iodofórmio (CHI₃, sólido amarelo).',
  rg:[['Iodo em iodeto (I₃⁻)','Adicionar 20 g de KI e 10 g de I₂ a 80 mL de água destilada e agitar até dissolver.'],['NaOH 10% p/v','Dissolver 10 g de NaOH em 100 mL de água.']],
  st:['Num tubo, ponha 4 gotas da amostra, 2 mL de água (ou de dioxana, se não dissolver em água) e 1 mL de NaOH 10%.','Junte um leve excesso da solução de iodo: a cor escura deve permanecer.','Aqueça a 60 °C, agitando. Se descorar, continue pondo iodo até a cor ficar por 2 minutos.','Junte gotas de NaOH 10%, ainda agitando, até remover o excesso de iodo (descorar).','Encha o tubo com água e deixe 15 minutos em repouso.'],
  pos:'Precipitado amarelo de odor desagradável (iodofórmio).',
  cu:'Também dão etanol, acetaldeído, CH₃CH(OH)R, β-dicetonas e 1,3-dióis, porque são oxidados a metilcetona nas condições do ensaio.',
  c:['#4e342e','#f1c40f'],l:['iodo','precipitado amarelo']},
 {g:'car',n:'Salicilaldeído (só para acetona)',p:35,
  pr:'A acetona reage com salicilaldeído em meio fortemente alcalino e dá um produto vermelho.',
  rg:[['NaOH 30%','Dissolver 30 g de NaOH em 100 mL de água. Proteja do CO₂ do ar e evite frasco com tampa de vidro esmerilhado.']],
  st:['Trate a amostra com salicilaldeído e depois com NaOH 30%.','Aqueça em banho-maria por 3 minutos.'],
  pos:'Cor vermelha (laranja se estiver diluído).',
  cu:'É específico para acetona.',
  c:['#efefef','#c0392b'],l:['incolor','vermelho']},
 {g:'car',n:'Tollens (espelho de prata)',p:36,
  pr:'O aldeído reduz o [Ag(NH₃)₂]⁺ a prata metálica e vira ácido carboxílico.',
  rg:[['Tollens','Tratar 5 mL de AgNO₃ 2% p/v com 2 mL de NaOH 5% p/v e agitar. Juntar 2 mL de amônia concentrada e depois, gota a gota, mais amônia até dissolver todo o precipitado negro. Completar a 20 mL com água. Não guarde: com o tempo se forma um sólido explosivo (a apostila cita nitreto de prata, o receituário cita fulminato de prata; as duas mandam descartar).']],
  st:['Dissolva a amostra em 2 gotas de etanol.','Junte cerca de 2 mL de Tollens e agite.','Aqueça em banho-maria por 5 a 10 minutos e deixe repousar alguns minutos.','Tubo muito limpo ajuda: limpe com HNO₃ concentrado.'],
  pos:'Espelho de prata ou precipitado negro.',
  cu:'Dão positivo aldeídos em geral e α-hidroxicetonas, mas não cetona simples. Açúcares redutores, α-dicetonas, 1-naftóis, aminofenóis, hidrazinas e p-fenilenodiamina também reduzem a prata.',
  c:['#efefef','#a6a6a6'],l:['incolor','espelho']},
 {g:'car',n:'Fehling (aldeídos alifáticos)',p:37,
  pr:'O Cu²⁺ complexado com tartarato é reduzido a Cu₂O pelo aldeído.',
  rg:[['Fehling','Misture volumes iguais das soluções A e B na hora. A: 7,5 g de CuSO₄·5H₂O em 100 mL de água. B: 30 g de tartarato de sódio e 25 g de KOH em 100 mL de água. A e B duram separadas.']],
  st:['Dissolva a amostra em 2 gotas de etanol.','Junte o reagente de Fehling (A e B em partes iguais).','Aqueça em banho-maria por 3 a 5 minutos.'],
  pos:'Precipitado amarelo (Cu₂O) ou vermelho.',
  cu:'Aldeídos aromáticos normalmente não dão. Outras substâncias redutoras podem dar falso positivo.',
  c:['#1e5aa8','#d35400'],l:['azul','precipitado vermelho']},
 {g:'car',n:'Benedict (açúcares redutores)',p:38,
  pr:'Igual ao de Fehling, mas o cobre vem complexado com citrato e o meio é menos alcalino. Detecta α-hidroxialdeídos e açúcares redutores.',
  rg:[['Benedict','Dissolver a quente 17,3 g de citrato de sódio e 1 g de Na₂CO₃ anidro em 80 mL de água. Juntar devagar, agitando, 1,7 g de sulfato de cobre dissolvido em 10 mL de água. Completar a 100 mL.']],
  st:['Dissolva a amostra em 2 gotas de água ou etanol.','Junte o reagente de Benedict.','Aqueça em banho-maria por 3 a 5 minutos.'],
  pos:'Precipitado vermelho ou amarelo.',
  cu:'Hidrazinas, fenil-hidroxilaminas, aminofenóis e p-difenóis também reduzem e dão positivo.',
  c:['#3a8fc7','#c0392b'],l:['azul','precipitado vermelho']},
 {g:'car',n:'Schiff (aldeídos)',p:39,
  pr:'A fucsina descorada com SO₂ reage com o aldeído e volta a ter cor.',
  rg:[['Schiff (fucsina descorada)','Dissolver 0,1 g de fucsina básica em 80 mL de água, juntar 10 mL de bissulfito de sódio saturado e deixar 1 hora. Juntar 5 mL de HCl concentrado, completar a 100 mL e deixar mais 12 horas. Se não estiver incolor, ativar com microgotas de formol 0,11% até leve cor fucsia, tratar com 1 g de carvão ativo a frio e filtrar. Tem de ficar incolor.']],
  st:['Dissolva a amostra em 1 gota de etanol sem aldeído.','Junte o reagente de Schiff.','Espere de 2 a 5 minutos.'],
  pos:'Cor rosa, com tom azul-violeta.',
  cu:'O reagente se decompõe com calor e com bases, então o branco é indispensável. Grupos doadores de elétrons no anel do aldeído impedem a reação.',
  c:['#efefef','#b5498f'],l:['incolor','rosa']},

 {g:'est',n:'Hidroxamato férrico (ésteres, amidas e nitrilas)',p:'43 e 49',
  pr:'A hidroxilamina converte o éster em ácido hidroxâmico, que forma com Fe³⁺ um quelato vermelho-vinho.',
  rg:[['Hidroxilamina','Saturar a quente 10 mL de etanol 96% com cloridrato de hidroxilamina, resfriar e filtrar. Alcalinizar o filtrado com NaOH 5% p/v em etanol. Atenção: a apostila manda chegar a pH 12 e o receituário dá pH 3,7 a 3,9; confira com o professor qual vale na sua aula.'],['Cloreto férrico 1% (aquoso)','Dissolver 0,1 g de FeCl₃ em 10 mL de água.']],
  st:['Antes, trate a amostra com 1 gota de FeCl₃ e 1 gota de HCl concentrado. Se já der cor (fenol, por exemplo), este ensaio não serve.','Num tubo, junte à amostra alguns cristais de cloridrato de hidroxilamina, 1 pastilha de NaOH e 2 mL de etanol.','Aqueça em banho-maria por 2 a 3 minutos, até aparecerem cristais. Esfrie e passe o sobrenadante para outro tubo.','Junte 2 gotas de HCl concentrado e confirme que o pH está ácido.','Junte 2 a 3 gotas de FeCl₃ 1%.','Para amidas e nitrilas, a reação é mais lenta: aqueça 10 minutos e use 5 mL de etanol.'],
  pos:'Cor vermelho-vinho.',
  cu:'Fenóis, oximas e ácidos hidroxâmicos já dão vermelho com FeCl₃, por isso o teste prévio.',
  c:['#f0e29a','#7b1e3a'],l:['amarelo claro','vinho']},

 {g:'ami',n:'Níquel-dimetilglioxima (qualquer base)',p:44,
  pr:'A base tira prótons do complexo e precipita o quelato rosa de níquel com dimetilglioxima.',
  rg:[['Feigl para bases','Dissolver 0,4 g de NiSO₄ em 50 mL de água e juntar 50 mL de solução de 0,4 g de dimetilglioxima em etanol 96%. Agitar, deixar 5 minutos e filtrar. Ativar com microgotas de NH₄OH 1% até começar a turvar (rosa) e filtrar de novo.']],
  st:['Junte à amostra algumas gotas do reagente.'],
  pos:'Precipitado rosa.',
  cu:'Mostra só o caráter básico, de qualquer grau de substituição.',
  c:['#efe6ea','#e0679a'],l:['reagente','precipitado rosa']},
 {g:'ami',n:'Duke I (aminas primárias)',p:45,
  pr:'A amina primária forma uma base de Schiff com o aldeído 5-nitrossalicílico, que precipita com níquel.',
  rg:[['Duke I','Dissolver 0,05 g de aldeído 5-nitrossalicílico em 1,5 mL de trietanolamina e 2,5 mL de água. Juntar 5 mL de NiSO₄·7H₂O 1%, filtrar se precipitar e completar a 10 mL.']],
  st:['Dissolva a amostra em 2 gotas de etanol.','Junte o reagente Duke I.','Espere de 2 a 3 minutos.'],
  pos:'Precipitado verde claro ou amarelo.',
  cu:'Hidroxilaminas e hidrazinas monossubstituídas também dão. Amidas e aminoácidos não.',
  c:['#ece9d2','#9bd0a0'],l:['reagente','precipitado verde']},
 {g:'ami',n:'Ácido nitroso e β-naftol (anilinas)',p:46,
  pr:'A anilina forma o sal de diazônio, que acopla com β-naftol e dá um corante azo.',
  rg:[['Papel de amido-iodetado','Mergulhar tiras de papel de filtro numa suspensão de amido recém-preparada com alguns cristais de KI.']],
  st:['Dissolva 3 gotas da amostra em 1 mL de HCl concentrado e dilua com 2 mL de água.','Esfrie a 0 °C em béquer com gelo picado.','Junte devagar, agitando, uma solução gelada de 0,5 g de NaNO₂ em 2 mL de água, até uma gota da mistura dar azul no papel de amido-iodetado (ácido nitroso em excesso).','À solução gelada do diazônio (cerca de 2 mL), junte 0,1 g de β-naftol em 2 mL de NaOH 10% e 5 mL de água.'],
  pos:'Corante vermelho-alaranjado.',
  cu:'O sal de diazônio só é estável abaixo de 0 °C, então mantenha tudo no gelo.',
  c:['#efefef','#e4572e'],l:['incolor','vermelho-alaranjado']},
 {g:'ami',n:'Duke II (aminas secundárias)',p:47,
  pr:'A amina secundária reage com CS₂ e forma um ditiocarbamato que precipita com níquel (verde) ou cobre (castanho).',
  rg:[['Duke IIa (CS₂ e níquel)','Dissolver 0,05 g de NiSO₄·7H₂O em 10 mL de água, juntar 1 gota de CS₂ e agitar. Deve sobrar sempre um excesso de CS₂ no frasco; se evaporar, ponha outra gota.'],['Duke IIb (CS₂ e cobre)','Igual, com 0,05 g de CuSO₄·5H₂O.']],
  st:['Dissolva a amostra em 2 gotas de etanol.','Junte o reagente Duke IIa (ou IIb).'],
  pos:'Duke IIa: precipitado verde. Duke IIb: precipitado castanho, solúvel em solventes orgânicos.',
  cu:'Faça o branco e o controle junto.',
  c:['#e8e8e8','#2e7d32'],l:['reagente','precipitado verde']},
 {g:'ami',n:'Kalnin-Ohkuma (aminas terciárias)',p:48,
  pr:'A amina terciária reage com ácido cítrico e anidrido acético e dá cor vermelha. A estrutura do produto não é conhecida.',
  rg:[['Kalnin-Ohkuma (2% p/v)','Dissolver 0,2 g de ácido cítrico em 10 mL de anidrido acético recém-destilado. Guardar seco e longe da luz.']],
  st:['Dissolva um pequeno cristal de ácido cítrico em 3 gotas de etanol.','Junte cerca de 5 gotas de anidrido acético e 1 gota da amostra.','Aqueça em banho-maria por 10 minutos.'],
  pos:'Cor vermelha.',
  cu:'Sensível para piridina e derivados. α,α-dipiridil e 1,10-fenantrolina não reagem.',
  c:['#efefef','#c0392b'],l:['incolor','vermelho']},
 {g:'ami',n:'Ninhidrina (aminoácidos)',p:52,
  pr:'Aminoácidos α e β dão um produto azul-violeta (cor de anil) com a ninhidrina.',
  rg:[['Ninhidrina (0,4% p/v)','Dissolver 0,04 g de ninhidrina em 10 mL de água. A apostila manda usar recém-preparada; o receituário diz que dura 4 semanas.']],
  st:['Dissolva a amostra em 2 gotas de etanol.','Junte a ninhidrina.','Aqueça em banho-maria por 2 minutos. Em papel de filtro, aqueça em estufa a 110 °C.'],
  pos:'Cor azul-violeta.',
  cu:'Prolina, hidroxiprolina e os ácidos aminobenzoicos dão amarelo. Algumas aminas dão amarelo a vermelho: conta como negativo.',
  c:['#efefef','#4a3f9a'],l:['incolor','azul-violeta']}
];
function fuTubo(a){
  const t=(x,cor,rot)=>'<g transform="translate('+x+',0)"><path d="M14 6v52a14 14 0 0 0 28 0V6" fill="none" stroke="currentColor" stroke-width="2"/><path d="M15 34h26v24a13 13 0 0 1-26 0z" fill="'+cor+'" stroke="none"/><text x="28" y="92" text-anchor="middle" font-size="10" fill="currentColor">'+rot+'</text></g>';
  return '<svg class="futb" viewBox="0 0 240 100" role="img" aria-label="Tubo do reagente e tubo positivo: '+a.l[0]+' passa a '+a.l[1]+'">'+t(40,a.c[0],a.l[0])+'<path d="M96 40h40m-8-8 8 8-8 8" fill="none" stroke="currentColor" stroke-width="2"/>'+t(158,a.c[1],a.l[1])+'</svg>';
}
/* ---- vidraria e utensílios: ícones simples (traço em currentColor) ---- */
const FUI={
 tubo:['Tubo de ensaio','<path d="M24 8v38a8 8 0 0 0 16 0V8" /><path d="M21 8h22"/><path d="M24 34h16" stroke-dasharray="2 3"/>'],
 micro:['Microtubo de ensaio','<path d="M26 14v28a6 6 0 0 0 12 0V14"/><path d="M23 14h18"/><path d="M26 34h12" stroke-dasharray="2 3"/>'],
 bequer:['Béquer','<path d="M16 12v38a4 4 0 0 0 4 4h24a4 4 0 0 0 4-4V12"/><path d="M13 12h38"/><path d="M16 32h32" stroke-dasharray="2 3"/><path d="M16 20h6M16 26h6M16 38h6M16 44h6"/>'],
 bunsen:['Bico de Bunsen','<path d="M28 54h8M32 54V28M27 28h10M29 54l-3 4M35 54l3 4"/><path d="M32 24c-5-4-5-9 0-15 5 6 5 11 0 15z" fill="currentColor" fill-opacity=".25"/>'],
 banho:['Banho-maria','<path d="M10 22v28a4 4 0 0 0 4 4h36a4 4 0 0 0 4-4V22"/><path d="M8 22h48"/><path d="M12 30q5-4 10 0t10 0 10 0 10 0" /><path d="M30 8v26a3 3 0 0 0 6 0V8"/><path d="M28 8h10"/>'],
 gota:['Conta-gotas ou pipeta Pasteur','<path d="M26 8a6 6 0 0 1 12 0v8H26z"/><path d="M28 16v22l4 8 4-8V16"/><path d="M32 52v4" stroke-dasharray="1 3"/>'],
 papel:['Papel de filtro','<path d="M14 12h36v40H14z"/><path d="M20 20h24M20 28h24M20 36h14" stroke-dasharray="3 3"/>'],
 gelo:['Banho de gelo','<path d="M12 24v26a4 4 0 0 0 4 4h32a4 4 0 0 0 4-4V24"/><path d="M10 24h44"/><rect x="18" y="30" width="10" height="9"/><rect x="32" y="34" width="10" height="9"/><rect x="24" y="43" width="10" height="7"/>'],
 funil:['Funil com papel de filtro','<path d="M14 12h36L36 34v14M28 34v14"/><path d="M28 48h8"/><path d="M20 18l12 14 12-14" stroke-dasharray="2 3"/>'],
 estufa:['Estufa','<rect x="10" y="10" width="44" height="44" rx="3"/><path d="M10 40h44"/><path d="M22 20q4-4 0-8M32 20q4-4 0-8M42 20q4-4 0-8"/><circle cx="46" cy="47" r="2"/>'],
 vidro:['Vidro de relógio','<path d="M10 34q22 20 44 0"/><path d="M10 34h44"/><path d="M24 40q8 5 16 0" stroke-dasharray="2 3"/>'],
 capela:['Capela de exaustão','<rect x="8" y="10" width="48" height="46" rx="3"/><path d="M8 24h48"/><path d="M16 34h32v14H16z"/><path d="M26 17h12" /><path d="M24 54v-6M40 54v-6"/>'],
 oculos:['Óculos de proteção e luvas','<path d="M8 28h48v8a8 8 0 0 1-8 8h-8a6 6 0 0 1-6-6h-4a6 6 0 0 1-6 6h-8a8 8 0 0 1-8-8z"/><path d="M8 30l-3-4M56 30l3-4"/>']
};
function fuIc(k){const d=FUI[k];return '<svg class="fuic" viewBox="0 0 64 64" role="img" aria-label="'+d[0]+'" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">'+d[1]+'</svg>';}
/* os materiais saem do texto do próprio procedimento: só aparece o que a apostila manda usar */
function fuMat(a){
  const t=(a.st.join(' ')+' '+a.rg.map(r=>r[1]).join(' ')).toLowerCase(),m=[];
  const add=(k,txt)=>{if(!m.some(x=>x[0]===k))m.push([k,txt]);};
  add('oculos','Óculos de proteção e luvas.');
  if(/microtubo/.test(t))add('micro','Microtubos de ensaio (para a amostra e o branco).');else add('tubo','Tubos de ensaio, com estante: um para a amostra, um para o branco e um para o controle.');
  add('gota','Conta-gotas ou pipeta Pasteur para as gotas de amostra e de reagente.');
  if(/banho-maria/.test(t))add('banho','Banho-maria: béquer com água quente sobre chapa de aquecimento ou bico de Bunsen.');
  if(/chama|bico de bunsen/.test(t))add('bunsen','Bico de Bunsen.');
  if(/gelo/.test(t))add('gelo','Banho de gelo.');
  if(/papel de filtro/.test(t))add('papel','Papel de filtro.');
  if(/filtr/.test(t)&&!/papel de filtro/.test(t))add('funil','Funil e papel de filtro, para filtrar.');
  if(/estufa/.test(t))add('estufa','Estufa a 110 °C.');
  if(/vidro de relógio/.test(t))add('vidro','Vidro de relógio.');
  if(/capela/.test(t))add('capela','Capela de exaustão (o reagente solta vapores).');
  if(/béquer/.test(t)&&!m.some(x=>x[0]==='banho'||x[0]==='bequer'))add('bequer','Béquer.');
  return m;
}
/* cena do banho-maria: só nos ensaios que pedem aquecimento assim */
function fuCena(a){
  if(!/banho-maria/.test(a.st.join(' ').toLowerCase()))return '';
  return '<figure class="fucena"><svg viewBox="0 0 220 120" role="img" aria-label="Tubo de ensaio mergulhado em béquer com água quente sobre um bico de Bunsen" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M60 40v46a4 4 0 0 0 4 4h60a4 4 0 0 0 4-4V40"/><path d="M56 40h76"/><path d="M60 56q10-5 20 0t20 0 20 0 14 0" /><path d="M92 10v62a8 8 0 0 0 16 0V10"/><path d="M88 10h24"/><path d="M92 62h16" fill="none" stroke-dasharray="2 3"/><path d="M96 92v10M92 102h8M160 100l-2 6M190 100l2 6"/><path d="M94 100c-4-3-4-6 0-11 4 5 4 8 0 11z" fill="currentColor" fill-opacity=".3"/><path d="M140 50h30M164 44l6 6-6 6" /></svg><figcaption>Banho-maria: o tubo fica dentro do béquer com água quente, preso por uma garra. A água não deve ferver dentro do tubo.</figcaption></figure>';
}
function fuCard(a){
  const mat=fuMat(a);
  return '<details class="el fuc"><summary><span class="fuch">'+esc(a.n)+'</span><span class="fudots" aria-hidden="true"><i style="background:'+a.c[0]+'"></i><i style="background:'+a.c[1]+'"></i></span></summary><div class="fucb">'
   +'<p>'+esc(a.pr)+'</p>'+fuTubo(a)
   +'<h4>Materiais</h4><ul class="fuul fumt">'+mat.map(x=>'<li>'+fuIc(x[0])+'<span>'+esc(x[1])+'</span></li>').join('')+'</ul>'
   +'<h4>Reagentes</h4><ul class="fuul">'+a.rg.map(r=>'<li><b>'+esc(r[0])+'</b><details class="fur"><summary>Como preparar</summary><p>'+esc(r[1])+'</p></details></li>').join('')+'</ul>'
   +'<h4>Procedimento</h4><ol class="steps2">'+a.st.map(s=>'<li>'+esc(s)+'</li>').join('')+'</ol>'+fuCena(a)
   +'<p class="pos"><b>Positivo:</b> '+esc(a.pos)+'</p>'+(a.cu?'<p class="fucu"><b>Cuidado:</b> '+esc(a.cu)+'</p>':'')
   +'<p class="fusrc"><span class="tag sv">Conferido: apostila IFRJ Nilópolis (2016)</span> Procedimento '+a.p+'. Reagentes: receituário do IFRJ. Cores do tubo aproximadas.</p></div></details>';
}
function fuDraw(){
  FUG.forEach(g=>{const box=document.getElementById('fu-'+g[0]);if(!box||box.dataset.ok)return;box.dataset.ok=1;
    box.innerHTML='<p class="fubar"><button type="button" class="chip" data-fuall="1">Abrir todos</button> <button type="button" class="chip" data-fuall="0">Fechar todos</button></p>'+FUN.filter(a=>a.g===g[0]).map(fuCard).join('');
    box.querySelectorAll('[data-fuall]').forEach(b=>b.onclick=()=>box.querySelectorAll('details.fuc').forEach(d=>d.open=b.dataset.fuall==='1'));});
}
function fuInit(){
  const sg=document.querySelector('#p-fu .sgm');if(!sg)return;
  FUG.slice().reverse().forEach(g=>{const b=document.createElement('button');b.type='button';b.dataset.fu=g[0];b.setAttribute('aria-pressed','false');b.textContent=g[1];sg.insertBefore(b,sg.firstChild);
    const d=document.createElement('div');d.id='fu-'+g[0];d.hidden=true;sg.parentNode.insertBefore(d,document.getElementById('fu-nit'));});
  fuDraw();
  sg.querySelectorAll('button').forEach(x=>x.setAttribute('aria-pressed','false'));
  const first=sg.querySelector('[data-fu="hid"]');
  /* os botões novos precisam do mesmo comportamento dos antigos */
  sg.querySelectorAll('[data-fu]').forEach(b=>{b.onclick=()=>{sg.querySelectorAll('button').forEach(x=>{x.setAttribute('aria-pressed',x===b?'true':'false');const p=document.getElementById('fu-'+x.dataset.fu);if(p)p.hidden=x!==b;});};});
  if(first)first.click();
}

/* ---- da ficha para os ensaios: o grupo funcional do composto aponta para os ensaios que o reconhecem ---- */
const FUMAP=[
 [/^(alceno|alcino terminal|vinila)/,['Bromo','Bayer']],
 [/^(anel |benzeno)/,['Le Rosen']],
 [/^álcool/,['Nitrato cérico','Xantato','Jones','Lucas','Malaprade']],
 [/^(éter|epóxido)/,['Iodo em']],
 [/^fenol/,['Cloreto férrico','Libermann','Cobaltinitrito']],
 [/^aldeído/,['Jones','2,4-dinitro','Tollens','Fehling','Benedict','Schiff']],
 [/^cetona/,['2,4-dinitro','m-dinitro','Índigo','Iodofórmio']],
 [/^(éster|amida|nitrila)/,['Hidroxamato']],
 [/^amina primária/,['Níquel','Duke I ','Ácido nitroso']],
 [/^amina secundária/,['Níquel','Duke II']],
 [/^amina terciária/,['Níquel','Kalnin']]
];
const FUOLD=[[/^nitro$/,'nit','Nitrocomposto'],[/^ácido carboxílico/,'aci','Ácido carboxílico'],[/^(cloreto|brometo|iodeto|haloforme|dialeto)/,'clo','Cloro e halogênios']];
function fuSug(gf){
  const ids=[],olds=[];
  (gf||[]).forEach(g=>{
    FUMAP.forEach(m=>{if(m[0].test(g))m[1].forEach(p=>FUN.forEach((a,i)=>{if(a.n.indexOf(p)===0&&ids.indexOf(i)<0)ids.push(i);}));});
    FUOLD.forEach(m=>{if(m[0].test(g)&&!olds.some(o=>o[0]===m[1]))olds.push([m[1],m[2]]);});
  });
  if(!ids.length&&!olds.length)return '';
  return '<h3 style="margin:12px 0 4px">Ensaios de bancada para este composto</h3><div class="fusug">'
   +ids.map(i=>'<button type="button" class="chip" data-fuid="'+i+'">'+esc(FUN[i].n.replace(/ \(.*$/,''))+'</button>').join('')
   +olds.map(o=>'<button type="button" class="chip" data-fug="'+o[0]+'">'+esc(o[1])+'</button>').join('')+'</div>'
   +'<p class="sm">Cada botão abre o procedimento na tela Análise funcional. Eles são sugestões pelo grupo funcional da ficha, não um diagnóstico.</p>';
}
function fuGo(grupo,idx){
  go('p-fu');
  const b=document.querySelector('#p-fu .sgm [data-fu="'+grupo+'"]');if(b)b.click();
  if(idx!=null){const box=document.getElementById('fu-'+grupo);const card=box&&box.children[FUN.filter(a=>a.g===grupo).indexOf(FUN[idx])];
    if(card){const d=card.querySelector('details');card.scrollIntoView({block:'start'});card.classList.add('fuhl');setTimeout(()=>card.classList.remove('fuhl'),1800);}}
}
document.addEventListener('click',e=>{
  const b=e.target.closest&&e.target.closest('[data-fuid],[data-fug]');if(!b)return;
  if(b.dataset.fuid!=null){const i=+b.dataset.fuid;fuGo(FUN[i].g,i);}else fuGo(b.dataset.fug);
});

/* a barra de seções acompanha a tela aberta: o chip ativo fica visível */
(function(){const o=new MutationObserver(()=>{const b=document.querySelector('.chipbar.msub:not([hidden]) .chip[aria-pressed="true"]');if(b&&b.scrollIntoView)try{const bar=b.parentNode;bar.scrollLeft=b.offsetLeft-16;}catch(e){}});
 document.addEventListener('DOMContentLoaded',()=>document.querySelectorAll('.chipbar.msub .chip').forEach(c=>o.observe(c,{attributes:true,attributeFilter:['aria-pressed']})));})();

/* ---- importar espectro de IV (.jdx/.dx/.csv/.txt): acha as bandas e preenche o campo de números ---- */
function ivParseSpec(tx){
  const L=tx.split(/\r?\n/),H={};let xs=[],ys=[],mode='';
  L.forEach(l=>{const m=l.match(/^##\s*([^=]+?)\s*=\s*(.*)$/);if(m){H[m[1].toUpperCase().replace(/[\s_-]/g,'')]=m[2];mode=/^(XYDATA|PEAKTABLE|XYPOINTS|DATATABLE)/i.test(m[1].replace(/[\s_-]/g,''))?m[1].replace(/[\s_-]/g,'').toUpperCase():'';return;}
    if(!mode&&/##/.test(tx))return;
    const n=(l.replace(/[;,\t]+/g,' ').match(/-?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?/g)||[]).map(Number);
    if(!n.length)return;
    if(mode==='XYDATA'){const xf=+(H.XFACTOR||1);if(!(xs._fx!==undefined))xs._fx=1;ys.push(...n.slice(1).map(v=>v*(+(H.YFACTOR||1))));if(xs._first===undefined)xs._first=n[0]*xf;}
    else if(n.length>=2&&n.length%2===0){for(let i=0;i<n.length;i+=2){xs.push(n[i]);ys.push(n[i+1]);}}
    else if(!/##/.test(tx)&&n.length===2){xs.push(n[0]);ys.push(n[1]);}
  });
  if(mode==='XYDATA'||(H.XYDATA&&!xs.length)){
    const fx=+(H.FIRSTX),lx=+(H.LASTX),nn=ys.length;if(!isFinite(fx)||!isFinite(lx)||nn<10)return null;
    const xf=+(H.XFACTOR||1),d=(lx-fx)/(nn-1);xs=ys.map((_,i)=>fx+i*d);
  }
  if(xs.length<10||xs.length!==ys.length)return null;
  const o=xs.map((x,i)=>[x,ys[i]]).filter(p=>isFinite(p[0])&&isFinite(p[1])).sort((a,b)=>a[0]-b[0]);
  if(o.length<10)return null;
  const yv=o.map(p=>p[1]),mn=Math.min(...yv),mx=Math.max(...yv),md=yv.slice().sort((a,b)=>a-b)[yv.length>>1];
  const un=String(H.YUNITS||'').toUpperCase();
  const T=/TRANSM|%T/.test(un)?true:/ABSORB/.test(un)?false:md>(mn+mx)/2;
  let s=o.map(p=>T?mx-p[1]:p[1]-mn);const sm=Math.max(...s)||1;s=s.map(v=>v/sm);
  const X=o.map(p=>p[0]),n=X.length;
  /* suaviza com média de 5 pontos */
  const z=s.map((_,i)=>{let a=0,c=0;for(let k=-2;k<=2;k++){if(s[i+k]!==undefined){a+=s[i+k];c++;}}return a/c;});
  const win=(i,r)=>{let a=i,b=i;while(a>0&&X[i]-X[a-1]<=r)a--;while(b<n-1&&X[b+1]-X[i]<=r)b++;return[a,b];};
  const P=[];
  for(let i=1;i<n-1;i++){
    if(X[i]<650||X[i]>4000)continue;
    const [a,b]=win(i,6);let top=true;for(let k=a;k<=b;k++)if(z[k]>z[i]){top=false;break;}
    if(!top||z[i]<=z[i-1]&&z[i]<=z[i+1])continue;
    const [c,d]=win(i,60);let base=1;for(let k=c;k<=d;k++)base=Math.min(base,z[k]);
    const prom=z[i]-base;if(z[i]<0.10||prom<0.07)continue;
    /* largura na meia altura acima da base local */
    const [e,f]=win(i,250);let lo=base;for(let k=e;k<=f;k++)lo=Math.min(lo,z[k]);
    const half=lo+(z[i]-lo)/2;let l=i,r=i;while(l>0&&z[l]>half)l--;while(r<n-1&&z[r]>half)r++;
    P.push({v:Math.round(X[i]),h:z[i],w:X[r]-X[l]});}
  P.sort((p,q)=>q.h-p.h);const out=[];
  P.forEach(p=>{if(out.length<20&&!out.some(q=>Math.abs(q.v-p.v)<10))out.push(p);});
  out.sort((p,q)=>q.v-p.v);
  return {T,n,peaks:out};
}
/* ---- PDF: texto do PDF quando existe; senão, leitura de impressões do SDBS (imagem do espectro) ---- */
let _pdfjs=null;
async function pdfCarrega(){
  if(_pdfjs)return _pdfjs;
  const m=await import('./vendor/pdf.min.mjs');m.GlobalWorkerOptions.workerSrc='./vendor/pdf.worker.min.mjs';_pdfjs=m;return m;
}
async function pdfNativa(pg,P){
  /* maior imagem embutida na página: tem os pixels originais do SDBS, sem reamostrar */
  const ol=await pg.getOperatorList();let best=null;
  for(let i=0;i<ol.fnArray.length;i++){const f=ol.fnArray[i];
    if(f===P.OPS.paintImageXObject||f===P.OPS.paintJpegXObject){const nm=ol.argsArray[i][0];
      const o=await new Promise(r=>{try{pg.objs.get(nm,r);}catch(e){r(null);}});
      if(o&&o.width>=500&&(!best||o.width*o.height>best.width*best.height))best=o;}}
  if(!best)return null;
  const W=best.width,H=best.height,n=W*H;let rgba=null;
  if(best.bitmap){const c=document.createElement('canvas');c.width=W;c.height=H;const x=c.getContext('2d');x.drawImage(best.bitmap,0,0);rgba=x.getImageData(0,0,W,H).data;}
  else if(best.data&&best.data.length>=n*3){const d=best.data,bpp=Math.round(d.length/n);rgba=new Uint8ClampedArray(n*4);
    for(let i=0;i<n;i++){rgba[i*4]=d[i*bpp];rgba[i*4+1]=d[i*bpp+1];rgba[i*4+2]=d[i*bpp+2];rgba[i*4+3]=255;}}
  return rgba?{data:rgba,W,H}:null;
}
async function pdfLer(f){
  const P=await pdfCarrega(),doc=await P.getDocument({data:new Uint8Array(await f.arrayBuffer())}).promise,pg=await doc.getPage(1);
  const tc=await pg.getTextContent();let tx='';tc.items.forEach(i=>{tx+=i.str+(i.hasEOL?'\n':' ');});
  if((tx.match(/\d+(?:\.\d+)?/g)||[]).length>=20)return{texto:tx};
  try{const nat=await pdfNativa(pg,P);if(nat)return{nat};}catch(e){}
  const vp=pg.getViewport({scale:2.5}),cv=document.createElement('canvas');cv.width=Math.round(vp.width);cv.height=Math.round(vp.height);
  const cx=cv.getContext('2d');cx.fillStyle='#fff';cx.fillRect(0,0,cv.width,cv.height);
  await pg.render({canvasContext:cx,viewport:vp}).promise;return{canvas:cv};
}
function pdfMascaraD(d,W,H){
  /* M/B: escuro (curva e texto). K: preto sem cor (texto e linhas). C: azul (curva de impressões coloridas). G: tinta 0 a 255 do preto */
  const M=new Uint8Array(W*H),B=new Uint8Array(W*H),K=new Uint8Array(W*H),C=new Uint8Array(W*H),G=new Uint8Array(W*H);
  for(let i=0;i<W*H;i++){const r=d[i*4],g=d[i*4+1],b=d[i*4+2],gr=(r+g+b)/3,sat=Math.max(r,g,b)-Math.min(r,g,b);
    M[i]=gr<140?1:0;B[i]=gr<128?1:0;
    if(sat<70){K[i]=gr<175?1:0;G[i]=Math.max(0,255-gr);}
    C[i]=(b>r+70&&b>g+40&&gr<200)?1:0;}
  return{M,B,K,C,G,W,H};
}
function pdfMascara(r){
  if(r.nat)return pdfMascaraD(r.nat.data,r.nat.W,r.nat.H);
  const cv=r.canvas;return pdfMascaraD(cv.getContext('2d').getImageData(0,0,cv.width,cv.height).data,cv.width,cv.height);
}
/* moldura do gráfico: a maior linha vertical é o eixo esquerdo; a linha de baixo parte dela */
function pdfMoldura(I){
  const {M,W,H}=I,C=[];
  for(let x=0;x<W;x++){let y=0,bb=null;while(y<H){if(M[y*W+x]){const s=y;while(y<H&&M[y*W+x])y++;if(!bb||y-1-s>bb[0])bb=[y-1-s,x,s,y-1];}else y++;}if(bb&&bb[0]>=120)C.push(bb);}
  C.sort((p,q)=>q[0]-p[0]);
  for(const [len,xl,yt,yb] of C.slice(0,150)){
    let ln=0,yy=yb;for(let y=Math.max(yt,yb-Math.round(len*0.06));y<=Math.min(H-1,yb);y++){let x=xl;while(x<W&&M[y*W+x])x++;if(x-xl>ln){ln=x-xl;yy=y;}}
    if(ln>=len&&ln>250)return{xl,yt,yb:yy,xr:xl+ln-1};}
  return null;
}
/* IV do SDBS: eixo de 4000 a 2000 cm⁻¹ ocupa 38,5% da largura e o resto vai até 400 (valores ajustados nas impressões do SDBS) */
function pdfIV(I,fr,guia){
  const {M,W}=I,{xl,yt,yb,xr}=fr,Wd=xr-xl,k=Wd/620;
  const x4=xl-0.002*Wd,xk=xl+0.3848*Wd,x4h=xr+0.0006*Wd,pad=Math.max(3,Math.round((yb-yt)*0.03));
  const V=[],T=[];
  for(let x=xl+pad;x<xr;x++){let my=-1;for(let y=yt+pad;y<yb-pad*2;y++)if(M[y*W+x])my=y;if(my<0)continue;
    T.push((yb-my)/(yb-yt));V.push(x<=xk?4000-(x-x4)/(xk-x4)*2000:2000-(x-xk)/(x4h-xk)*1600);}
  const n=T.length,w=Math.max(4,Math.round(12*k)),res=[];
  for(let i=2;i<n-2;i++){
    let mn=1,mx=0;for(let j=i-2;j<=i+2;j++){mn=Math.min(mn,T[j]);mx=Math.max(mx,T[j]);}
    if(T[i]>mn||T[i]>=mx)continue;
    let hi=0;for(let j=Math.max(0,i-w);j<Math.min(n,i+w+1);j++)hi=Math.max(hi,T[j]);
    const pr=hi-T[i];if(pr<0.025||V[i]<450||V[i]>4000)continue;
    res.push({v:Math.round(V[i]),h:1-T[i],w:0,forte:pr>=0.07&&1-T[i]>=0.10});}
  /* forte: pico claro na curva. fraco: só entra se a tabela escrita tem um número de onda perto (±14) */
  const bons=res.filter(p=>p.forte||(guia||[]).some(g=>Math.abs(g-p.v)<=14));
  bons.sort((a,b)=>b.h-a.h);const out=[];bons.forEach(p=>{if(out.length<30&&!out.some(q=>Math.abs(q.v-p.v)<14))out.push(p);});
  out.sort((a,b)=>b.v-a.v);return out;
}
/* MS do SDBS: o primeiro tick maior é m/z 10 e cada tick maior vale 10 unidades; a altura da barra é a altura da coluna */
function pdfMS(I,fr){
  const {M,W,H}=I,{xl,yt,yb,xr}=fr,Wd=xr-xl;
  let y0=yb+1;while(y0<H&&(()=>{let c=0;for(let x=xl;x<=xr;x++)c+=M[y0*W+x];return c>Wd*0.5;})())y0++;
  const L=[];for(let x=xl-1;x<=xr+1;x++){let n=0;while(y0+n<H&&M[(y0+n)*W+x])n++;L.push(n);}
  const mx=Math.max(...L);if(mx<3)return[];
  const maj=[];for(let x=0;x<L.length;x++){if(L[x]>=mx*0.8){let a=x;while(x<L.length&&L[x]>=mx*0.8)x++;maj.push(xl-1+(a+x-1)/2);}}
  if(maj.length<3)return[];
  const u=(maj[maj.length-1]-maj[0])/(10*(maj.length-1)),x0=maj[0],pad=Math.max(3,Math.round((yb-yt)*0.01));
  const col=new Array(W).fill(0);for(let x=xl+3;x<xr-2;x++){let c=0;for(let y=yt+pad;y<yb-pad;y++)c+=M[y*W+x];col[x]=c;}
  const bins=new Map();
  for(let x=xl+3;x<xr-2;x++){if(col[x]>=3&&col[x]>col[x-1]&&col[x]>=col[x+1]){const mz=Math.round(10+(x-x0)/u);bins.set(mz,Math.max(bins.get(mz)||0,col[x]));}}
  const top=Math.max(...bins.values(),1);
  return[...bins].map(p=>[p[0],Math.round(p[1]/top*100)]).filter(p=>p[1]>=3&&p[0]>0).sort((a,b)=>b[1]-a[1]).slice(0,12).sort((a,b)=>a[0]-b[0]);
}
/* ---- tabela de picos escrita (imagem) das impressões de IV do SDBS ----
   A fonte é de pontos (5x7) e fica borrada no JPEG: 0, 3, 5, 6, 8 e 9 se confundem. Por isso a tabela só serve de guia (quais picos existem,
   inclusive os fracos); a posição de cada pico sai da curva. Os padrões abaixo foram rotulados a partir de impressões do SDBS. */
const PDF_PAT={"3|.#..#..#..#..#..#.###":1,"5|.###.#...##...##...##...##...#.###.":0,"5|...#...##...##..#.#.#####...#....#.":4,"2|.###.#.#.#.###":1,"4|#####..#...#..#..#..#...####":2,"4|.##.#..##..#..#..#..#...####":2,"2|##.#.#.#.#.###":1,"5|.###.#...#...#...#...#...#....#####":2,"4|#####..#...#...#..#...#...#.":7,"5|######...#....#...#....#....#...#..":7,"5|######....#....####.....##...######":5,"5|.###.#...##...######....#....#.###.":9,"5|######...#...#....#....#...#....#..":7,"3|.#.##..#..#..#..#.###":1,"5|.###.#...##...#.###.#...##...######":8,"5|######....#....######...##...#.###.":6,"3|##..#..#..#..#..#.###":1,"5|.###.#....#....######...##...#.###.":6,"4|.####..##..#..#..#..#...####":2,"5|######...#...#....#....#...#.......":7,"4|.####..##...#####..##..#.###":6,"2|#.#.#.#.#.#.##":1,"4|#####..#...#...#..#...#.....":7,"5|...#...##..#.#..#.#.#####...#....#.":4,"4|.##.#..#...#.###...#...#####":3,"4|#####...#...#####..##..#.###":6,"4|.####..#...#.###...##..#.###":3,"4|..##..##.#.#.#.#####...#...#":4,"5|.###.#...##...##...#.####....######":9,"5|...#....#...##..#.#..#.#.#####...#.":4,"4|.####..#...#.###...#...#####":3,"5|.###.#...##..##..#...#...#....#####":2,"5|.###.#...##...#...#...#...#...#####":2,"5|.###.#....#....####.#...##...#.###.":6,"4|.##.#..##..##..##..##..#####":0,"5|.###.#...#.#.#.######...##...#.###.":8,"4|#####...#...####...##..#####":5,"5|.###.#...##...#.####....#.#..#.###.":9,"4|.####..##..##..##..##..#.###":0,"4|.####..##..##..##..##..#####":0,"4|#####..##..##..##..##..#.##.":0,"4|..#..##..##.#.#.####..#...#.":4,"4|..#...#..##.#.#.####..#...#.":4,"5|######....#....####.#...##...#.###.":6,"4|#####..#...#..#...#...#..#..":7,"4|#####..#...#..#...#...#.....":7,"5|..##...##..#.#..#.#.#####...#....#.":4,"4|#####...####...##..##..#.###":5,"4|###....#...####....#...####.":3,"5|.###.#...###..#######...##...#.###.":8,"5|...#....#...##..#.#.#####...#....#.":4,"5|.###.#...##...##...##...##...######":0,"4|.##.#..##..##..#.###...#####":9,"4|###....####....#...#...####.":3,"4|...#..##.#.#.#.#####...#...#":4,"5|######..##...#....#...#....#....#..":7,"4|####...#...#.###...##..#.##.":3,"4|####...#.###...#...##..#.##.":3,"4|###.#..##...###.#..##..#####":6,"5|.###.##..##...#.###.#...##...######":8,"4|.####..##...#####..##..#####":6,"5|######....####.....##...###..#.###.":5,"4|.####..##..######..##..#.###":6,"4|###.#..##..##..##..##..####.":0,"5|.###.#...#.###.#...##...##...#.###.":8,"4|#####..##..##..##..##..####.":0,"4|###....#...#####...#...####.":3,"4|..#...#..##..##.#.#.####..#.":4,"4|.####..##..#.####..##..#####":8,"5|.###.#...##....######...##...#.###.":6,"4|.####..#...#..#..#..#...####":2,"5|.###.#..###...##...##...##...######":0,"4|###.#..##...#####..##..####.":6,"5|.###.#...##...#.####....#....#.###.":9,"4|#####...#...#####..##..#.##.":6,"4|#####...###.#..##..##..#.##.":6,"4|###.#..##..####.#..##..#####":8,"4|.####..##..#.###...#...#.###":3,"5|######...#....#...#....#...#....#..":7,"4|#####...#...###....##..#####":5,"5|.###.#....####.#...##...##...#.###.":6,"5|.###.##..##...#...#...#...#...#####":2,"5|.###.....#....#.###.....#....######":3,"4|.##.#..##...#####..##..####.":6,"5|######....####....###...##..##.###.":5,"5|.###.#....#....####.#...##...######":6,"5|.###.#..#.#....####.#...##...######":6,"4|#####..#...#...#...#..#...#.":7,"5|.###.#...#.#..#######...##...#.###.":8,"5|.###.#...##....####.#...##...######":8,"4|####...#.###...#...##..#.###":3,"4|...#..##..##.#.##..#####...#":4,"4|#####..##..#####...##..#.##.":9,"5|.###.#...#.###.##..##...###..#.###.":8,"5|.###.##...#....####.#...##...######":6,"5|.###.#...###..#.###.#...##...#.###.":8,"4|#####..##..#.###...##..#.###":3,"4|#####...#...#####..##..####.":5,"4|#####..######..##..##..#.##.":8,"5|.###.#...##...##...##...###..#.###.":0,"5|.###.#....####.#..###...##..##.###.":6,"4|#####..######..##..##..#.###":8,"4|.####..##..#####...#...#.###":9,"4|###.#..##..######..##..####.":8,"5|.###.#....####.#...##...###..#.###.":6,"4|#####..######..##..##..####.":8,"5|.###.#...##...#.####....#...##.###.":9,"4|#####..#.####..##..##..#.###":8,"5|.###.#...##..##.###.#...##...#.###.":8,"4|.##.#..#...#.##....#...#####":3,"5|.#####...##...#.####....#.#..#.###.":9,"5|.#####...#.###.#...##...###..#.###.":8,"5|.###.#...##..########...##...#.###.":8,"5|######....####.....##...##...#.###.":6,"5|.###.#...##...###..#.####....#.###.":9,"4|#####..##..######..##..#.##.":6,"4|.##.#..##..#.####..##..#####":0,"4|###.#..##..#..#..#..#...####":2,"4|.##.#..##...#####..##..#.###":6,"5|.###.#...##...##...##...##..##.###.":0,"5|.###..#..#....#.###.....#....######":3,"5|.###.#..###...#...#...#...#...#####":2,"5|.###.#...#.###.##..##...##...#.###.":8,"4|.####..##..#.####..##..#.###":3,"5|.#####....####.#...##...###..#.###.":0,"4|#####...#...#####..##..#####":5,"5|######..##...#....#...#....#.......":7,"4|.####..#.###...#...##..#.###":3,"4|#####..#...#..#...#...#...#.":7,"4|.##.#..##..#####...#...####.":3,"5|.###.##..##...##...##...##...######":0,"4|..#...#..##..##.####..#...#.":4,"5|...#...##..#.#..#.#.#..#.#####...#.":4,"5|...#...##...##..#.#.#..#.#####...#.":4,"5|.###.#...#.###.#..###...##..##.###.":8,"5|.###.#...#.###.#..###...##...#.###.":8,"4|.####..##..##..#.###...#####":0,"4|###.#..##..#####...##..####.":5,"5|######...#...#....#...#....#.......":7,"4|...#..##.#.#.#.##..#####...#":4,"5|...#...##...##..#.#..#.#.#####...#.":4,"4|.##.#..##..######..##..#####":0,"5|.###....##....#.###.....#....######":8,"4|.####..######..##..##..#.###":0,"4|#####..#..#..#..#...#...####":2,"4|###....####...##...#...####.":8,"5|######..##...#....#....#...#....#..":7,"4|.###...#...#.###...#...#####":3,"4|.##.#..#...#.###...##..#.###":3,"4|.##.#..#...#.###...#...####.":3,"4|#####..##..##..##..##..#.###":0,"4|.##.#..##...#####..##..#####":6,"5|.#####...#...#...#...#...#....#####":2,"4|.##.#..##..######..##..####.":0,"4|.####..##..#####...##..#.###":3,"5|.###.#..###...#.###.#...##...######":8,"4|.##.#..##...###.#..##..#####":6,"4|#####...###.#..##..##..####.":0,"5|######....####.....##...##..##.###.":6,"4|####...####....#...##..####.":0,"4|#####...###....##..##..#.##.":6,"5|.###.#...##...#...#...#..##...#####":2,"4|###.#..#...####....#...#####":3,"5|######....####....###...##...#.###.":6,"5|.###.#...##...###..#.####....######":9,"4|###.#..##..##..##..##..#####":0,"5|.#####...#.###.##..##...###..#.###.":8,"5|.###.#...#####.#...##...###..#.###.":0,"4|.##....#...#.###...#...#####":3,"5|.###.#...#...#....#...#..##...#####":2,"4|#####..#...#.##.#...#...####":2,"4|#####..#...#...#..#...#..#..":7,"5|.###.#...##..#.######...##...#.###.":6,"5|####.#....#....######...##...#.###.":6,"4|###....####....#...#..#####.":8,"5|####.#...#####.#..###...##..##.###.":8,"5|####.....#.###....##....##..##.###.":8,"4|.####..#.####..##..##..#.###":0,"5|.###.#...##...##...#.####....#.###.":9,"4|###....#..#.####...#...####.":8,"4|###....#..######...#...####.":9,"4|.####..##..#...#..#..#..####":2,"5|####.#...#...#...#...#...#....#####":2,"5|.###.#...#...##.####....##...#.###.":8,"5|.###.##..##...##...#.####....######":9};
function pdfCaixaTabela(I,fr){
  const {B:M,W,H}=I,Wd=fr.xr-fr.xl,fh=fr.yb-fr.yt;let top=-1,bot=-1;
  const run=y=>{let x=fr.xl;while(x<W&&M[y*W+x])x++;return x-fr.xl;};
  for(let y=fr.yb+Math.round(fh*0.04);y<Math.min(H,fr.yb+Math.round(fh*0.6));y++){const r=run(y);
    if(r>Wd*0.25){if(top<0)top=y;else if(y-top>fh*0.06){bot=y;break;}}}
  if(top<0||bot<0)return null;
  let b=bot;while(b+1<H&&run(b+1)>Wd*0.25)b++;
  return{x0:fr.xl,x1:Math.min(W-1,fr.xl+run(top)),y0:top,y1:b};
}
function pdfGlifos(I,cx){
  const {B:M,W}=I,x0=cx.x0,x1=cx.x1,y0=cx.y0+3,y1=cx.y1-3,h=y1-y0;
  const dc=[];for(let x=x0;x<=x1;x++){let c=0;for(let y=y0;y<=y1;y++)c+=M[y*W+x];if(c>h*0.85)dc.push(x);}
  const cen=[];dc.forEach(x=>{const l=cen[cen.length-1];if(l&&x-l[1]<=4)l[1]=x;else cen.push([x,x]);});
  if(cen.length<2)return[];
  const iv=[];for(let i=0;i+1<cen.length;i++)iv.push([cen[i][1]+2,cen[i+1][0]-2]);
  const w=iv.map(p=>p[1]-p[0]).sort((p,q)=>p-q),med=w[w.length>>1];
  const keep=iv.filter(p=>p[1]-p[0]<=med*1.4&&p[1]-p[0]>=med*0.6),rowsAll=[];
  keep.forEach(([a,c])=>{
    const has=(x,ya,yb)=>{for(let y=ya;y<=yb;y++)if(M[y*W+x])return true;return false;};
    const hasR=y=>{for(let x=a;x<=c;x++)if(M[y*W+x])return true;return false;};
    let y=y0;
    while(y<=y1){if(hasR(y)){const s0=y;while(y<=y1&&hasR(y))y++;if(y-1-s0>=4){
      const gl=[];let x=a;while(x<=c){if(has(x,s0,y-1)){const t=x;while(x<=c&&has(x,s0,y-1))x++;gl.push([t,x-1]);}else x++;}
      rowsAll.push({y:[s0,y-1],gl});}}else y++;}});
  return rowsAll;
}
function pdfPadrao(I,x0,x1,y0,y1){
  let k=(x1-x0+1)+'|';for(let y=y0;y<=y1;y++)for(let x=x0;x<=x1;x++)k+=I.B[y*I.W+x]?'#':'.';
  if(PDF_PAT[k]!==undefined)return PDF_PAT[k];
  /* padrão desconhecido: o mais parecido (alinhando à esquerda ou à direita) */
  const w=x1-x0+1;let best='?',bd=99;
  for(const kk in PDF_PAT){const p=kk.indexOf('|'),w2=+kk.slice(0,p),s=kk.slice(p+1);if(Math.abs(w2-w)>1)continue;
    for(let off=0;off<=Math.abs(w2-w);off++){let d=0;for(let y=0;y<=y1-y0;y++)for(let x=0;x<Math.min(w,w2);x++){const a=I.B[(y0+y)*I.W+x0+x+(w>w2?off:0)],b=s.charCodeAt(y*w2+x+(w2>w?off:0))===35?1:0;if(a!==b)d++;}
      d+=Math.abs(w-w2)*3;if(d<bd){bd=d;best=PDF_PAT[kk];}}}
  return bd<=5?best:'?';
}
/* números de onda (aprox.) lidos da tabela escrita; devolve [] se não achar a tabela */
function pdfTabelaIR(I,fr){
  const cx=pdfCaixaTabela(I,fr);if(!cx)return[];
  const out=[];
  pdfGlifos(I,cx).forEach(l=>{
    const gaps=l.gl.slice(1).map((g,i)=>g[0]-l.gl[i][1]).sort((p,q)=>p-q);
    const tok=[];let cur=[];l.gl.forEach((g,i)=>{if(i&&g[0]-l.gl[i-1][1]>9){tok.push(cur);cur=[];}cur.push(g);});if(cur.length)tok.push(cur);
    if(tok.length!==2)return;
    const s=tok[0].map(g=>pdfPadrao(I,g[0],g[1],l.y[0],l.y[1])).join('');
    if(/^\d{3,4}$/.test(s)&&+s>=400&&+s<=4000)out.push(+s);});
  return out;
}
/* ---- IV com os números dos picos escritos na vertical (rótulos girados 90°, fonte lisa de tela) ----
   Aqui os números são lidos de verdade: cada dígito é recortado, desvirado e comparado com modelos de dígitos. */
const PDF_ROT_Q={"3":["466401523612212611012610035610024510001431201442522533666514","244201544511312612102613024613035513001433211443533522555411","244210444521311521001521024621135521001443211444433533455411","356410433521111532002632136522013533101443311442555521233210","356410432620111530001630136620012531101341311441555520233310","378410721730200630001630025620034632001444210345621541677620","377410721731200631001730035620034631001441200342621542677623","257630442460110361000360014650014551000253110145441352377750","258630441460110361000360014650014551000253110144441352377751","004784117227302006400017500357500346400004311003126115006776","258630441460110361000360014650014551000253110144441352377740","378410722730200630001630024620034630001441210342621541677620","378410721730200631001632034622034622001443200353621541677620","258630441460110361000360014650014551000254110145441352377750","048841171272120062000172003571003562000054110034361153168761","047841164461161182000062000172001372005861001263000044000025","478410721730200632001632034622034632000443200243611531677620","258630441460110362000361014650014551000253110144441352377740"],"2":["467521422532111444001443002532014410244100441001642211776641","244310444520310441000331001431014420135100442000643220665531","344311444521311431001331002530014410134100441000643320665531","466410432531111431001431002521125313243114541112755431333320","367740541362110144000243001351012530124400254101662111787774","158851272163120044000044000262001441014510145100291111587775","057851272263120044000044000162001441014510146100292111587775","368740541362110244000243001352012531124300254000551111787774","368740541362110244000243001351012430124300253000551111787775","158851271263120044000044000163001441014510146100282111597775","158751271263120044000044000163001451014510146100292111587785","057751271163120044000044000163001441014510146100292111587775","205775127216012003000004100015300144501451404510129211059877","158851271263120044000044000162001441014510146100282111587775","367740541362110144000243001351012430124400254100651111787774"],"9":["466411623521511432521452554552344552011443211533523622566411","244200545411512433511444633553354552001441212531533621455311","234210445420421431421441543551354551000441211531433520456310","244200445411422432411443543553354553011443211532434521455310","048831272262450143460045264455034455000045020063261272167831","037841162253451134361045165455034455001045020054162263067841","026851154244442124453025255445224445100025111035143245047862","258620442451430243530254454465244454000254110262441461378620","038831271262450143460055264455034455000045120063261272167841","047830271262450143460045264455034455000045120063261272167841"],"8":["367410542530521531431530344420343420421431410341532541467520","366410643521621521621520443510444410522431411341522541566620","234210454520531530520530443520344420421431420441533541455520","366410543520531530521530443520344420421431420341521541566520","244211554511621520621520533510344410521431511341533531455510","244210454520531530520530443520344420421431420441543531455420","366410633520621520622520355411432423511345511443555521233310","038741182162170053171062044451144441261053450035371164167762","038741183262271053171062144451144441261053440035361164167762","037851073253172044072053044452044442251044441025262155067762","038841183262271053171062144451144441260053440035361154167761","026862055245153035054135034444034443243024442014254135047874","037851073253172044072053044452044442261044441025262155067762"],"0":["244211444521511431410342410343410342410341411431532522344411","244310443520520431410341410241410241420341420431432520345410","355410532530420431410341410242410241420331521431444520233210","355410532521411432410342410341410342411343521433444521233210","244310444520511431410331410342410343411345411444533521345410","355410532521411431410341410341410341411331521430444520233210","244310544510621430511341510251510251511341511431633520345410","025763154145353024342014242014242014242014153024054135135664","257640451361430243430144430134430135430134430243551351256641","025764145136244015343013443013443013343013244014045126025665","047751181162260043350034350025350025360034360043181162056661","257640451361430243430144430135430134430134430243551351256640","257640453451550361430243430144430134430135430135430134430143","257640551361440243430144430135430135430144430243551351256641","025763154145253024342014242014242014242014153024054135135664"],"5":["444411754422720001743300755520421441001351211342533523455413","344321654321521013643213655522321531001341211441433421455311","566531532211521101644311655521321431111343111344421533566421","344320654421520000543210655520321541001341211431433420455310","666621732211621102744311755521422441111353111344522533566511","566530542210531100655410543531211341100341311431555520233210","058775064111154000266542255455232135100014111024253135047763","058776165221054000166542155455132135110014211024253135047863","488762552210440000564530564551331253000135110145441351477630","058786165221154000256542155454132135000014011024253135147763","188773192221180000184541284462141054010035120034361162167851","158775164111053000156542155455032135000014011024253135047763","487762551111440000565530564551331253000145110144541351377631","048777146221145000146453146445123125100013311014344126037774"],"1":["013101346201456202125202014202014201014200014201014202014101","124201456202346202025202015202014201014200014201014202014202","125200357200237200016200016200016200016200015200015200015200","113101346202456202125202014202014201014200014201014202014201","012100346201346302114201014201014201014202014203014202013201","124200456200346200025200014201015202015214015214014201014200","012100346201456201125200015200014200015200014201014202013101","124201456201235201024200014200014200015200014202014202012101","013101346202456202125200015200015200014200015201014213013214","124201456202235201025200014200014200014201014202014214012102","113100346201456201125200015200014200015200015200014200014200","013100347200347200116200016200016212016214016214016211014200","124201456202235202025203015203014203014203014202014201012100","123101346201456202125213015203014203014203014202014202014201","124201456202235202025203014203014203014203014202014201012100","124201456301235301014202014202014201014200014202014202002101","001441046751112551000451000351000351100351100341100341000341","016200668300226301006301006302006202006202006301006200006200","016200668300227301006301006302006202006201006201006200006200","001620156920022720000620000720000720000720000620000620000620","001441046761012451000351000351000351000341000341000341000341","016200668300226300006201006201006300006300006200006201006200","001441046761012451000451000351000351000351100351000341000341","016200668300226300006300006300006301006303006203006200006200","016200568301226300006200006200006300006300006200006201006200","016200668301226300006300006300006300006300006300006201006200","016200668301227300006300006300006300006300006300006201006203","016200568301226300006200006300006300006300006300006201006203","001441146761112551100451000351000351000351000351000341100341","016200668300227301006302006302006302006302006301006200006200","013510367610124510003510003511003511003510003510003510003510","016200668300227300006201006301006300006300006300006202006200","016200568301227300006300006300006300006300006300006201006200","016200668301227300006300006200006200006300006300006301006203","001620166820022720000720000720000720000720000720000720000620"],"4":["003411016511136511254411343421423421534521556641123522002411","013411025511145512244412533413523513656633335632012411001200","002310014511036511145511344411523411534632556644113522002311","013410026520136520244420433420423520556641334631002420001210","012310014510036510145510343411523412534634556644113521002310","002210015520136520145520343420422420534630556641113520002310","001440014740025641135441343440432440543552666773001440001340","000351001861004661025451153351251251553463566775111351000251","001440014740025640145440343340432340543551666773111441001341","000243100473102563114544034344143244354455466676010244100133","000351001861004651026451153351251251553463566785111351000251","000243001473002564014544034344143244354455466676011244000143"],"7":["344431344541001430001420003310015200025100143100152000121000","444431444542001422001412013312014202024102143102142001121001","444431444542001423002513013312014101024100143001142002121001","666641334532112422001512002413013313014203024103133103142002","267787112234100034000034000242000340101330203410105400012200","167787112234000034000134000242100340101430103410105400012200","157787112234100035100134000242000340001330003410005400112200","777862222441000521001521003312005202025102053101071000131000","777862222442000521001520004310006200025100053100071001131000","287785111143000062000151000431000610002510006200008100013000","787862122442000523001522004311006200025100053100071001130000","777862444542111431000521001521002412006202006202025102053101","777762111431000520001520003310006200025100053101072001130000"],"6":["255411643421721111511000655410633531521441621442445522133311","256410453421531322520112410012433212555423533543521443411343","156410544420732320720110510000533200655520633531621441511341","147740463352551111430001454421564552541254430144451352257750","016751174253281011360000364431374463371155260035172153036762","147740463352551111530000454420564552541254430144451352257740","026751184153281011360000363431374563371155260035172163036762","013774146325255111244000245442256455355125344013245126014775","001675207425119101026100036443237456437115526103207215003676","147740463342551111540000454420564552541254430145451352257750","167520842431910111610002644312744632721453610343821541367620","147740463342551111530001454420564551541254430144452352257750"]};
const PDF_ROT={};for(const k in PDF_ROT_Q)PDF_ROT[k]=PDF_ROT_Q[k].map(q=>[...q].map(c=>+c/9));let PDF_ROT_MAX=3,PDF_ROT_MU=0.1;const PDF_ROT_C=Object.keys(PDF_ROT);
function pdfMoldFina(I){
  /* eixo esquerdo: maior linha vertical FINA (borda grossa escura da imagem não conta); a linha de baixo parte dele */
  const {K,W,H}=I;let bb=null;
  for(let x=6;x<W-6;x++){let y=0;while(y<H){if(K[y*W+x]){const s0=y;while(y<H&&K[y*W+x])y++;const len=y-s0,ym=(s0+y)>>1;
      if(len>=100&&!K[ym*W+x-4]&&!K[ym*W+x+4]&&(!bb||len>bb.len))bb={len,x,yt:s0,yb:y-1};}else y++;}}
  if(!bb)return null;
  let best=null;
  for(let y=Math.max(0,bb.yb-3);y<=Math.min(H-1,bb.yb+3);y++){let a=bb.x,b=bb.x;while(a>0&&K[y*W+a-1])a--;while(b<W-1&&K[y*W+b+1])b++;
    if(!best||b-a>best.b-best.a)best={a,b,y};}
  if(!best||best.b-best.a<250)return null;
  const fr={xl:bb.x,yt:bb.yt,yb:best.y,xr:best.b,ticks:[]};
  /* marcas pequenas logo abaixo do eixo: 4000, 3000, 2000, 1000 */
  const xs=[];for(let x=fr.xl;x<=fr.xr;x++)if(K[(fr.yb+2)*W+x]&&K[(fr.yb+3)*W+x]&&K[(fr.yb+4)*W+x])xs.push(x);
  let g=[];xs.forEach((x,i)=>{if(i&&x-xs[i-1]>2){fr.ticks.push(g.reduce((p,q)=>p+q,0)/g.length);g=[];}g.push(x);});if(g.length)fr.ticks.push(g.reduce((p,q)=>p+q,0)/g.length);
  return fr;
}
function pdfRotGlifos(I,fr){
  /* um item por rótulo, da esquerda para a direita: {x0,x1,yb,v4:[4 vetores de dígitos, de baixo para cima]}.
     Os dígitos ficam encostados e as linhas-guia encostam no topo, então não dá para contar dígitos pela tinta: calculo 4 janelas
     iguais a partir da base e deixo pdfIVRot decidir se o rótulo tem 3 ou 4 dígitos pela ordem decrescente dos números. */
  const {K,G,W}=I,s=(fr.xr-fr.xl)/680,z0=fr.yb-Math.round(36*s),z1=fr.yb-Math.max(1,Math.round(2*s));
  const col=[];for(let x=fr.xl+2;x<fr.xr-3;x++){let n=0;for(let y=z0;y<=z1;y++)n+=K[y*W+x];col.push([x,n]);}
  const cl=[];let cur=null;col.forEach(([x,n])=>{if(n>0){if(!cur)cur={a:x,b:x};cur.b=x;}else if(cur){cl.push(cur);cur=null;}});if(cur)cl.push(cur);
  const C=[];
  cl.forEach(c=>{
    const wd=c.b-c.a+1;if(wd<Math.round(5*s)||wd>Math.round(16*s))return;
    let rb=-1;for(let y=z1;y>=z0&&rb<0;y--)for(let x=c.a;x<=c.b;x++)if(K[y*W+x]){rb=y;break;}
    if(rb>=0)C.push({a:c.a,b:c.b,rb,wd});});
  if(C.length<3)return[];
  const ws=C.map(c=>c.wd).sort((p,q)=>p-q),A=0.62*ws[ws.length>>1],out=[];
  C.forEach(c=>{
    const v4=[];
    for(let i=0;i<4;i++){
      const yb=c.rb+1-i*A,v=[];
      for(let j=0;j<10;j++)for(let k=0;k<6;k++){ /* desvira: modelo da esquerda para a direita = de baixo para cima; de cima para baixo = da esquerda para a direita */
        const y0=yb-(k+1)*A/6,y1=yb-k*A/6,x0=c.a+j*c.wd/10,x1=c.a+(j+1)*c.wd/10;let t=0,n=0;
        for(let y=Math.floor(y0);y<Math.ceil(y1);y++)for(let x=Math.floor(x0);x<Math.ceil(x1);x++){
          const ov=(Math.min(y+1,y1)-Math.max(y,y0))*(Math.min(x+1,x1)-Math.max(x,x0));if(ov>0){t+=ov*G[y*W+x]/255;n+=ov;}}
        v.push(n?t/n:0);}
      v4.push(v);}
    out.push({x0:c.a,x1:c.b,yb:c.rb,v4});});
  return out;
}
function pdfRotTopK(v,k){
  const m=[];for(const c in PDF_ROT){let d=1e9;PDF_ROT[c].forEach(t=>{let e2=0;for(let i=0;i<v.length;i++){const e=v[i]-t[i];e2+=e*e;}if(e2<d)d=e2;});m.push([c,d]);}
  m.sort((p,q)=>p[1]-q[1]);return m.slice(0,k);
}
function pdfRotCands(v4,N){
  let C=[{s:'',d:0}];
  for(let j=0;j<N;j++){const t=pdfRotTopK(v4[j],3),nc=[];C.forEach(c=>t.forEach(([k,d])=>nc.push({s:c.s+k,d:c.d+d})));C=nc;}
  return C.filter(c=>(N===4?+c.s>=1000&&+c.s<=4000:+c.s>=400&&+c.s<1000)&&c.d<PDF_ROT_MAX*N).sort((p,q)=>p.d-q.d);
}
function pdfRotLideres(I,fr){
  /* x de cada linha-guia vertical (do pico até perto do número): é a posição exata do pico */
  const {K,W}=I,s=(fr.xr-fr.xl)/680,y1=fr.yb-Math.round(38*s),min=Math.round(25*s),xs=[];
  for(let x=fr.xl+4;x<fr.xr-4;x++){let best=0,y=fr.yt+2;
    let fim=0;while(y<y1){if(K[y*W+x]){const s0=y;while(y<y1&&K[y*W+x])y++;if(y-s0>best){best=y-s0;fim=y;}}else y++;}
    if(best>=min&&fim>=fr.yb-Math.round(90*s))xs.push(x);} /* a linha-guia desce até perto dos números; traço escuro da curva não */
  const out=[];let g=[];xs.forEach((x,i)=>{if(i&&x-xs[i-1]>1){out.push(g.reduce((p,q)=>p+q,0)/g.length);g=[];}g.push(x);});if(g.length)out.push(g.reduce((p,q)=>p+q,0)/g.length);
  return out;
}
function pdfIVRot(I){
  const fr=pdfMoldFina(I);if(!fr)return null;
  const L=pdfRotGlifos(I,fr);if(L.length<3)return null;
  const bots=L.map(l=>l.yb).sort((a,b)=>a-b);if(bots[bots.length-1]-bots[0]>3)return null; /* os números ficam alinhados na base */
  const t=fr.ticks,W=I.W;if(t.length<2)return null;
  const xv=v=>t[0]+(4000-v)/1000*(t[1]-t[0]),vx=x=>4000-(x-t[0])/(t[1]-t[0])*1000;
  const lid=pdfRotLideres(I,fr),usaL=lid.length===L.length;
  let k4=L.length; /* sem linhas-guia: os primeiros k4 rótulos têm 4 dígitos e os demais 3 (a ordem é decrescente) */
  if(!usaL){let melhor=1e9;for(let k=0;k<=L.length;k++){let tot=0;L.forEach((l,i)=>{const N=i<k?4:3,c=pdfRotCands(l.v4,N)[0];tot+=c?c.d/N:5;});if(tot<melhor){melhor=tot;k4=k;}}}
  let falhas=0,estim=0;const out=[];
  L.forEach((l,i)=>{
    const vL=usaL?vx(lid[i]):null,N=usaL?(vL>=995?4:3):(i<k4?4:3),C=pdfRotCands(l.v4,N);
    let e=null;
    if(usaL){ /* todos os inteiros perto da linha-guia; vence o que mais se parece com os dígitos desenhados e menos se afasta da linha */
      const tb=[];for(let j=0;j<N;j++){const m={};PDF_ROT_C.forEach(c=>m[c]=1e9);const v=l.v4[j];
        for(const c in PDF_ROT)PDF_ROT[c].forEach(t=>{let e2=0;for(let q=0;q<v.length;q++){const e=v[q]-t[q];e2+=e*e;}if(e2<m[c])m[c]=e2;});tb.push(m);}
      let mz=1e9;for(let n=Math.round(vL)-30;n<=Math.round(vL)+30;n++){const sn=String(n);if(sn.length!==N||n<400||n>4000)continue;
        let z=PDF_ROT_MU*Math.pow((n-vL)/6,2);for(let j=0;j<N;j++)z+=tb[j][sn[j]]===undefined?9:tb[j][sn[j]];
        if(z<mz){mz=z;e={s:sn,d:z};}}}
    if(!e)e=C[0]||null;
    if(!e){falhas++;return;}
    if(usaL&&Math.abs(+e.s-vL)>28)estim++;
    const v=+e.s;let h=0.5,lo=-1;const xp=Math.round(xv(v));
    for(let x=xp-3;x<=xp+3;x++)for(let y=fr.yt;y<fr.yb-45;y++)if(I.C[y*W+x]&&y>lo)lo=y;
    if(lo>0)h=Math.min(1,Math.max(0.05,(lo-fr.yt)/(fr.yb-fr.yt)));
    out.push({v,h,w:0,forte:h>=0.35});});
  if(out.length<3)return null;
  out.sort((a,b)=>b.v-a.v);return{peaks:out,falhas,estim,lideres:usaL};
}
const PDF_ERR='Não consegui ler este PDF. O app lê PDF com texto (pares de números) e impressões de espectro do SDBS. Para outro tipo de imagem, digite os números.';
async function pdfIVArquivo(f){
  const r=await pdfLer(f);
  if(r.texto){const p=ivParseSpec(r.texto);return p&&p.peaks.length?{peaks:p.peaks,msg:'Li '+p.peaks.length+' bandas do texto do PDF'}:null;}
  const I=pdfMascara(r),rot=pdfIVRot(I);
  if(rot)return{peaks:rot.peaks,msg:'Li '+rot.peaks.length+' números escritos no espectro (rótulos dos picos)'+(rot.lideres?', conferidos com a linha de cada pico':'')+(rot.falhas?'. '+rot.falhas+' rótulo(s) eu não consegui ler: digite à mão':'')+'. Os dois últimos dígitos podem errar (6, 8 e 0 se parecem): confira a lista no campo acima. Não marquei largura (l/e)'};
  const fr=pdfMoldura(I);if(!fr)return null;
  const guia=pdfTabelaIR(I,fr),pk=pdfIV(I,fr,guia);
  return pk.length>=3?{peaks:pk,msg:'Li '+pk.length+' bandas da imagem do espectro (impressão do SDBS)'+(guia.length?', usando a tabela de picos escrita ('+guia.length+' linhas lidas) como guia':'')+'. A posição vem da curva. Não marquei largura (l/e): a imagem não dá isso com segurança'}:null;
}
async function pdfMSArquivo(f){
  const r=await pdfLer(f);
  if(r.texto){const p=bdParseSpec(r.texto);return p.length?{pk:p,msg:'Li '+p.length+' picos do texto do PDF'}:null;}
  const I=pdfMascara(r),fr=pdfMoldura(I);if(!fr)return null;
  const pk=pdfMS(I,fr);return pk.length>=2?{pk,msg:'Li '+pk.length+' picos da imagem do espectro (impressão do SDBS), pela altura das barras'}:null;
}
const ehPdf=f=>/\.pdf$/i.test(f.name)||f.type==='application/pdf';
function ivPreenche(peaks,msg,T,n){
  const out=document.getElementById('icIVMsg'),campo=document.getElementById('icIV');
  campo.value=peaks.map(p=>p.v+(p.w>=110&&p.v>2400?'l':'')).join(' ');
  campo.dispatchEvent(new Event('input',{bubbles:true}));
  out.textContent=msg+(T===undefined?'':' ('+(T?'espectro em transmitância':'espectro em absorbância')+', '+n+' pontos)')+'. Confira a lista no campo acima e apague as que não forem bandas de verdade. Só marquei "l" nas bandas muito largas acima de 2400 cm⁻¹; "e" você mesmo decide.';
}
document.addEventListener('change',async e=>{
  if(!e.target||e.target.id!=='icIVFile')return;
  const f=e.target.files[0];if(!f)return;const out=document.getElementById('icIVMsg');
  if(ehPdf(f)){
    out.textContent='Lendo o PDF…';
    try{const r=await pdfIVArquivo(f);if(r)ivPreenche(r.peaks,r.msg);else out.textContent=PDF_ERR;}
    catch(err){out.textContent=PDF_ERR+' (Este navegador pode ser antigo demais para o leitor de PDF.)';}
    return;}
  const rd=new FileReader();rd.onload=()=>{
    const r=ivParseSpec(String(rd.result));
    if(!r||!r.peaks.length){out.textContent='Não consegui ler bandas neste arquivo. Use .jdx ou .csv com duas colunas (número de onda e intensidade), ou um PDF. Para uma imagem, digite os números acima.';return;}
    ivPreenche(r.peaks,'Li '+r.peaks.length+' bandas',r.T,r.n);
  };rd.readAsText(f);
});
/* MS em PDF: captura antes do tratador do painel, que só lê texto */
document.addEventListener('change',async e=>{
  if(!e.target||e.target.id!=='icFile')return;const f=e.target.files[0];if(!f||!ehPdf(f))return;
  e.stopImmediatePropagation();const out=document.getElementById('icMsMsg');out.textContent='Lendo o PDF…';
  try{const r=await pdfMSArquivo(f);if(!r){out.textContent=PDF_ERR;return;}
    const campo=document.getElementById('icP');campo.value=r.pk.map(q=>q[0]+':'+q[1]).join(' ');campo.dispatchEvent(new Event('input',{bubbles:true}));
    out.textContent=r.msg+'. Confira os valores no campo acima: a leitura por imagem pode errar em 1 unidade de m/z ou em barras muito pequenas.';}
  catch(err){out.textContent=PDF_ERR+' (Este navegador pode ser antigo demais para o leitor de PDF.)';}
},true);

/* ---- avisos de erro e sugestões: vão para a aba "Sugestões de Mudanças" da planilha "Avisos do Claude" ---- */
/* Endereço do script publicado (Apps Script, termina em /exec). Vazio = o aviso fica só neste aparelho e pode ser copiado/compartilhado. */
const AV_URL='https://script.google.com/macros/s/AKfycbyQ2cNjylQc8PJNTiExj7RnzCAlKA_7qQn-5WA1lr7QVsdTCfnaljm7vugiOZKjLws/exec';
function avLista(){try{return JSON.parse(localStorage.getItem('anaquim_avisos')||'[]');}catch(e){return[];}}
function avGuarda(l){try{localStorage.setItem('anaquim_avisos',JSON.stringify(l.slice(-50)));}catch(e){}}
function avDesenha(){const b=document.getElementById('avL');if(!b)return;const l=avLista();
  b.innerHTML=l.length?l.slice().reverse().map(x=>'<p><b>'+esc(x.tipo)+'</b> · '+esc(x.tela)+' · '+esc(x.data.slice(0,10))+' · '+(x.enviado?'enviado':'só neste aparelho')+'<br>'+esc(x.msg)+'</p>').join(''):'<p class="hint">Nenhum ainda.</p>';}
function avInit(){
  const f=document.getElementById('avF');if(!f)return;avDesenha();
  f.onsubmit=async ev=>{ev.preventDefault();
    const m=document.getElementById('avM').value.trim();if(!m)return;
    const d={origem:'Usuário',tipo:f.avT.value,tela:document.getElementById('avTela').value,msg:m,contato:document.getElementById('avC').value.trim(),versao:String(VERSAO).split(' ')[0],data:new Date().toISOString()};
    const s=document.getElementById('avS');let ok=false;
    if(AV_URL){try{await fetch(AV_URL,{method:'POST',mode:'no-cors',headers:{'Content-Type':'text/plain'},body:JSON.stringify(d)});ok=true;}catch(e){}}
    d.enviado=ok;const l=avLista();l.push(d);avGuarda(l);avDesenha();
    if(ok){s.textContent='Enviado. Obrigada!';document.getElementById('avM').value='';}
    else{const txt='[Anaquim '+d.versao+'] '+d.tipo+' em '+d.tela+': '+d.msg;
      s.innerHTML='Guardei o aviso neste aparelho, mas o envio automático ainda não está ligado. <button type="button" class="chip" id="avCp">Copiar texto</button>'+(navigator.share?' <button type="button" class="chip" id="avSh">Compartilhar</button>':'');
      document.getElementById('avCp').onclick=()=>{navigator.clipboard&&navigator.clipboard.writeText(txt);s.textContent='Texto copiado.';};
      const sh=document.getElementById('avSh');if(sh)sh.onclick=()=>navigator.share({text:txt}).catch(()=>{});}
  };
}
