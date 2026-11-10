# Analorg

(Antes chamado "Quebra-cabeça de massas". Agora é o Analorg. O endereço continua o mesmo.)

App de uma página (`index.html`, instalável no celular) de consulta e estudo de Análise Orgânica, para graduação e ensino médio. Endereço: https://calisants.github.io/massas/

## Telas (menu fixo embaixo)
- **Início:** a ordem da análise em 6 passos e atalhos para Revisar, Orgânica Básica, Identificar, modo detetive e o bloco "O app" (Ajustes, Novidades, Salvar, Fontes).
- **Compostos:** 110 fichas (busca por nome, fórmula ou CAS; filtro por estado e grupo de solubilidade) com estrutura, fórmula, massa, GDH, cor, estado, PF, PE, solubilidade, CAS, bandas de IV esperadas, picos de MS, RMN estimado de ¹H e ¹³C e link para o SDBS.
- **Identificar:** uma tela só. Seções numeradas (aspecto, solubilidade, constantes físicas, análise elementar, IV, e fórmula/massas/RMN como opcional). Mostra as classes de compostos que sobram e o ranking de compostos do banco. O botão "Ver como funciona" preenche com um composto de exemplo. O que você digita fica salvo.
- **Ensaios:** preliminares, solubilidade, análise elementar, análise funcional (nitrocomposto, ácido carboxílico e cloro orgânico), problemas resolvidos, consulta rápida e notação ECGF.
- **Quatro abas:** Início, Compostos, Ensaios e Espectros (o antigo "Mais" virou seção "O app" do Início). A aba Espectros dá acesso a IV, Massas (MS) e RMN, e todas as páginas seguem o mesmo layout (voltar, título, subtítulo e barra de botões), tendo o RMN como referência. **IV:** qualquer um dos 106 compostos, espectro simulado e tabela de bandas numerada; Guia com a tabela completa. **Massas:** teoria, prática, livro e calculadora. **RMN:** quatro passos num espectro real, régua de deslocamento, laboratório de acoplamento, cálculos (Hz/ppm, integração, GDH), macetes, tabelas e espectros simulados por composto. Tocar num pico, banda ou sinal colore o trecho da molécula.
- **Início > O app:** Ajustes (zoom com os dedos, treinos sem pistas), Revisar (erros de massa e perguntas de quiz voltam em 1, 3 e 7 dias, no máximo 10 por dia), Novidades, cor do app (6 opções, com Astronomia), salvar o progresso, fontes.

## Avisos sobre os dados
- A tela Análise funcional segue a apostila de Análise Orgânica do IFRJ Nilópolis (2016) e as receitas do Receituário da Plataforma QO é Vida. Os textos das páginas de análise funcional da Plataforma não abriram na hora da conferência, então os passos vêm da apostila. Onde as fontes divergem (KOH ou NaOH no hidróxido ferroso, pH da hidroxilamina, KIO4 ou KIO3, concentração do amido), a página diz qual usou.
- PF e PE de 185 valores foram conferidos no PubChem (mediana de HSDB, ICSC, HMDB e outras; 7 divergiram e ficam marcados); estado, cor, CAS (só o dígito verificador) e grupo de solubilidade foram escritos sem fonte conferida; fórmula, massa, GDH, estrutura, número de sinais de RMN e multiplicidade são calculados pelo RDKit; os δ de RMN são faixas típicas de tabela.
- Os picos de MS de 75 compostos foram conferidos nos prints do SDBS (e os 12 dos exemplos com mecanismo na lousa); nos demais são picos típicos escritos sem fonte conferida. O IV de 73 compostos foi conferido contra a tabela de picos do SDBS (bandas-chave); o ¹³C de 70 compostos e o ¹H de 66 foram conferidos contra os valores de ppm dos prints do SDBS (o valor medido aparece na ficha; as faixas de tabela foram corrigidas onde não incluíam o valor real). Os prints de ¹H não trazem integração nem J, e alguns vêm truncados.
- SDBS (AIST): o app só liga para o site e mostra o texto de citação. O SDBS proíbe coleta automática e download em massa.
- A teoria de RMN resume os slides de RMN do Prof. Jeronimo (IFRJ). Os slides trazem δ de H do estireno em dois valores diferentes (6,73 e 6,37).
- B 51 (`CH2F2`), B 58 (`C2H5S`) e C 102 estão como impressos no livro, mas a massa não bate (provável erro de impressão).

## Como atualizar (quando mexer em `fontes/`)
```
cd fontes
pip install rdkit
python3 empacotar.py
```
Isso gera `index.html`, sobe a versão em `sw.js` e mostra a versão em Início > O app > Fontes e avisos. Depois é só enviar para o GitHub.

## Testes (antes de cada envio ao GitHub)
```
cd fontes
python3 empacotar.py
python3 testes/rodar.py
```
`rodar.py` roda um teste de cada vez e para no primeiro que falhar. Se o Chromium do Playwright não estiver instalado, usa o Chrome do sistema. Só envie para o GitHub com "Tudo passou."

## Formulário de sugestões (ainda não ligado)
O botão em Início > O app só aparece quando `FORM_URL` (em `fontes/analorg3.js`) tem o link de um Google Formulário. Sugestão: formulário com tipo (sugestão ou erro), tela, texto e e-mail opcional; as respostas vão para uma planilha, e uma segunda planilha controla o que já foi resolvido.

## Instalar no celular
Abra o endereço acima. Android: menu do Chrome, "Instalar app". iPhone: Safari, Compartilhar, "Adicionar à Tela de Início". Depois da primeira abertura com internet, o app funciona sem internet (as fontes do Google também ficam guardadas).

## Pasta `fontes/`
`template.html` (página), `build_app.py` e `build3.py` (exercícios e estruturas em SVG com RDKit), `why.py` e `rearr.py` (explicações), `svgmodels.py` (modelos com setas) e `empacotar.py`. Os scripts antigos já aplicados ficam só no histórico do Git.

- **Fragmentos de MS propostos:** `fontes/msfrag.py` gera, para os compostos com MS do SDBS, a estrutura de cada íon (clivagem α, benzílica, McLafferty, perda de CO ou de alceno), conferindo a massa nominal com o pico. É proposta por regras, não mecanismo medido; os picos sem regra simples aparecem como "sem proposta".


## Banco Analor
A tela Ensaios > Banco busca no arquivo UNIV1_290926.DBF (banco do professor, 4668 compostos). `fontes/analor_bd.py` converte o DBF (cp1252) em `fontes/analor_bd.json`, que o `build3.py` embute no app. Os valores não foram alterados e o banco não cita a fonte de cada número.
