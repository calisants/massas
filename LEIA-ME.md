# Quebra-cabeça de massas

App de uma página (`index.html`, instalável no celular) para estudar espectrometria de massas (EI-MS) e IV de Análise Orgânica. Endereço: https://calisants.github.io/massas/

## Telas (menu fixo embaixo)
- **Analisar:** exercícios 1 a 12 ou seus próprios picos. Um pico por vez: o que ficou (Apêndice B), o que saiu (Apêndice C), estruturas, mapa na molécula, "Mostrar o porquê" e "Possível rearranjo".
- **Treinar:** quatro modos: "Qual saiu?" (múltipla escolha), "Tente antes de ver" (o que saiu, tipo de cisão, regra), "Digitar a perda" e "Revisar erros".
- **Livro:** Apêndices B e C do Silverstein com busca.
- **IV:** bandas por composto, por número de onda e um guia por região.
- **Mais:** calculadora de massa, espectro novo (modo detetive), setas dos mecanismos, regras de quebra (homolítica, heterolítica, rearranjos), cor do app, glossário e fontes.

## Avisos sobre os dados
- Exercícios 6 a 12 foram conferidos com a lousa do professor. Exercícios 1 a 5 ainda precisam de conferência.
- "Por que quebra aqui?" é explicação baseada no Silverstein e não vem da lousa. Rearranjos marcados como "possibilidade" não são exigidos.
- B 51 (`CH2F2`), B 58 (`C2H5S`) e C 102 estão como impressos no livro, mas a massa não bate (provável erro de impressão).
- Atribuições de IV que não estão na tabela da disciplina são leitura minha e trazem um selo de confiança.

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
