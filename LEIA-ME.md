# Quebra-cabeça de massas

App de uma página só (`index.html`) para estudar espectrometria de massas (EI-MS) e IV.

- **Analisar:** digite M e os picos; o app mostra o que ficou (Apêndice B) e o que saiu (Apêndice C) do Silverstein, com estruturas.
- **Treinar:** quiz com os exercícios da lista.
- **Tabelas do livro:** Apêndices B (p. 67–68) e C (p. 69–70), com busca.
- **IV:** bandas dos 11 exercícios com atribuições e busca por número de onda.
- **Calculadora:** massa nominal e exata, com parênteses, e IDO.

Fonte das tabelas: Silverstein, Webster, Kiemle, Bryce, *Spectrometric Identification of Organic Compounds*, 8ª ed.

## Avisos sobre os dados
- Exercícios 1 a 5: conferir com o professor. Exercícios 10 e 12: quebras sugeridas, sem resolução do professor.
- B 51 (`CH2F2`) e B 58 (`C2H5S`) estão como impressos no livro, mas a massa não bate (provável erro de impressão).
- As atribuições de IV são faixas típicas de tabela; confira com a tabela do professor.

## Como regenerar
A pasta `fontes/` tem o gabarito (`template.html`) e os scripts Python (RDKit) que geram as estruturas em SVG. Os scripts têm caminhos de `/home/claude` e precisam ser ajustados.

## Instalar no celular
Abra https://calisants.github.io/motsparole/quebra-cabeca-massas/ e use "Adicionar à tela inicial" (Android: menu do Chrome, "Instalar app"; iPhone: Safari, Compartilhar, "Adicionar à Tela de Início"). Depois da primeira abertura, o app funciona sem internet.
Ao publicar uma versão nova do `index.html`, troque o número em `CACHE` no `sw.js` (v1 para v2).
