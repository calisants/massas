# Analorg

(Antes chamado "Quebra-cabeça de massas". Agora é o Analorg. O endereço continua o mesmo.)

App de uma página (`index.html`, instalável no celular) de consulta e estudo de Análise Orgânica, para graduação e ensino médio. Endereço: https://calisants.github.io/massas/

## Telas (menu fixo embaixo)
- **Início:** a ordem da análise em 6 passos e atalhos para Revisar, Orgânica Básica, Ensaios e Espectros.
- **Compostos:** 108 fichas (busca por nome, fórmula ou CAS; filtro por estado e grupo de solubilidade) com estrutura, fórmula, massa, GDH, cor, estado, PF, PE, solubilidade, CAS, bandas de IV esperadas, picos de MS, RMN estimado de ¹H e ¹³C e link para o SDBS.
- **Identificar:** uma tela só. Seções numeradas (aspecto, solubilidade, constantes físicas, análise elementar, IV, e fórmula/massas/RMN como opcional). Mostra as classes de compostos que sobram e o ranking de compostos do banco. O botão "Ver como funciona" preenche com um composto de exemplo. O que você digita fica salvo.
- **Ensaios:** preliminares, solubilidade, análise elementar, problemas resolvidos, consulta rápida e notação ECGF.
- **Espectros:** IV (qualquer um dos 106 compostos, espectro simulado e tabela de bandas numerada; Guia com a tabela completa), espectrometria de massas (escolha de composto, mecanismos, treino, livro, ferramentas de massas) e RMN (teoria, tabelas, espectros ¹H e ¹³C simulados por composto, com integração opcional).
- **Mais:** Ajustes (zoom com os dedos, treinos sem pistas), Revisar (erros de massa e perguntas de quiz voltam em 1, 3 e 7 dias, no máximo 10 por dia), Novidades, cor do app (6 opções, com Astronomia), salvar o progresso, fontes.

## Avisos sobre os dados
- PF e PE de 185 valores foram conferidos no PubChem (mediana de HSDB, ICSC, HMDB e outras; 7 divergiram e ficam marcados); estado, cor, CAS (só o dígito verificador) e grupo de solubilidade foram escritos sem fonte conferida; fórmula, massa, GDH, estrutura, número de sinais de RMN e multiplicidade são calculados pelo RDKit; os δ de RMN são faixas típicas de tabela.
- Os picos de MS de 74 compostos foram conferidos nos prints do SDBS (e os 12 dos exemplos com mecanismo na lousa); nos demais são picos típicos escritos sem fonte conferida. O IV de 72 compostos foi conferido contra a tabela de picos do SDBS (bandas-chave); o ¹³C de 31 compostos foi conferido contra a tabela de ppm do SDBS (todos os sinais caem dentro das faixas mostradas); o ¹H ainda usa faixas típicas de tabela.
- SDBS (AIST): o app só liga para o site e mostra o texto de citação. O SDBS proíbe coleta automática e download em massa.
- A teoria de RMN resume os slides de RMN do Prof. Jeronimo (IFRJ). Os slides trazem δ de H do estireno em dois valores diferentes (6,73 e 6,37).
- B 51 (`CH2F2`), B 58 (`C2H5S`) e C 102 estão como impressos no livro, mas a massa não bate (provável erro de impressão).

## Como atualizar (quando mexer em `fontes/`)
```
cd fontes
pip install rdkit
python3 empacotar.py
```
Isso gera `index.html`, sobe a versão em `sw.js` e mostra a versão em Mais > Fontes e avisos. Depois é só enviar para o GitHub.

## Testes (antes de cada envio ao GitHub)
```
cd fontes
python3 empacotar.py
python3 testes/rodar.py
```
`rodar.py` roda um teste de cada vez e para no primeiro que falhar. Se o Chromium do Playwright não estiver instalado, usa o Chrome do sistema. Só envie para o GitHub com "Tudo passou."

## Formulário de sugestões (ainda não ligado)
O botão em Mais só aparece quando `FORM_URL` (em `fontes/analorg3.js`) tem o link de um Google Formulário. Sugestão: formulário com tipo (sugestão ou erro), tela, texto e e-mail opcional; as respostas vão para uma planilha, e uma segunda planilha controla o que já foi resolvido.

## Instalar no celular
Abra o endereço acima. Android: menu do Chrome, "Instalar app". iPhone: Safari, Compartilhar, "Adicionar à Tela de Início". Depois da primeira abertura com internet, o app funciona sem internet (as fontes do Google também ficam guardadas).

## Pasta `fontes/`
`template.html` (página), `build_app.py` e `build3.py` (exercícios e estruturas em SVG com RDKit), `why.py` e `rearr.py` (explicações), `svgmodels.py` (modelos com setas) e `empacotar.py`. Os scripts antigos já aplicados ficam só no histórico do Git.
