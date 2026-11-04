# Analorg

(Antes chamado "Quebra-cabeça de massas". Agora é o Analorg. O endereço continua o mesmo.)

App de uma página (`index.html`, instalável no celular) de consulta e estudo de Análise Orgânica, para graduação e ensino médio. Endereço: https://calisants.github.io/massas/

## Telas (menu fixo embaixo)
- **Início:** atalhos para Orgânica Básica, Compostos, Identificação do Composto, Análise de Ensaios e Espectros, mais os passos da análise e o cartão do SDBS.
- **Compostos:** 48 fichas (busca por nome, fórmula ou CAS; filtro por estado e grupo de solubilidade) com estrutura, fórmula, massa, GDH, cor, estado, PF, PE, solubilidade, CAS, bandas de IV esperadas, picos de MS, RMN estimado de ¹H e ¹³C e link para o SDBS.
- **Identificar:** Identificação do Composto. Aceita estado, cor, solubilidade, PF, PE, N/halogênio/S, bandas de IV, M e picos de MS, nº de sinais e δ de RMN; devolve os compostos mais compatíveis com uma porcentagem (compatibilidade dentro do banco do app, não probabilidade real).
- **Ensaios:** preliminares, solubilidade, análise elementar, problemas resolvidos, consulta rápida e notação ECGF.
- **Espectros:** IV, espectrometria de massas (mecanismos, treino, livro) e RMN (teoria, tabelas, estimativa por composto).
- **Mais:** calculadora de massa, modo detetive, regras de quebra, slides de mecanismos, cor do app, fontes.

## Avisos sobre os dados
- Estado, cor, PF, PE, CAS e grupo de solubilidade dos 48 compostos foram escritos sem fonte conferida; fórmula, massa, GDH, estrutura, número de sinais de RMN e multiplicidade são calculados pelo RDKit; os δ de RMN são faixas típicas de tabela.
- O banco de MS tem picos conferidos (lousa e SDBS) só para os 12 compostos dos exemplos com mecanismo; nos demais são picos típicos escritos sem fonte conferida.
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

## Instalar no celular
Abra o endereço acima. Android: menu do Chrome, "Instalar app". iPhone: Safari, Compartilhar, "Adicionar à Tela de Início". Depois da primeira abertura com internet, o app funciona sem internet (as fontes do Google também ficam guardadas).

## Pasta `fontes/`
`template.html` (página), `build_app.py` e `build3.py` (exercícios e estruturas em SVG com RDKit), `why.py` e `rearr.py` (explicações), `svgmodels.py` (modelos com setas) e `empacotar.py`. A pasta `historico/` guarda scripts antigos já aplicados.
