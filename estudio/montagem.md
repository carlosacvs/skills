# Fundo + montagem

A IA gera só o fundo. Texto, logo e ajuste fino moram no **canvas do
estúdio** (Claude Design), onde o usuário corrige direto, sem gerar de novo.
Texto dentro da imagem gerada não se corrige: refaz tudo. No canvas, troca
uma palavra.

## O que a ficha precisa ter

Seção **Montagem** do `estudio.md`: link do **design system** do dono, link
do canvas da vez e o guia de estilo. Cor, fonte e logo vêm do design system
(seção "Design system" da SKILL), nunca da ficha nem de memória.

## 1. Texto antes do fundo

Escrever (ou receber) o texto da peça antes de pedir o fundo: título,
apoio, chamada, quantos cards. O tamanho do texto decide onde o fundo
precisa ficar livre. Texto escrito pelo assistente se declara como tal.

## 2. Pedir o fundo

No destino que o usuário escolher (passo 3 da SKILL), pedir:

- **sem texto, sem letra, sem logo, sem marca d'água**;
- onde fica a área livre e calma para o texto ("terço de cima livre",
  "lado esquerdo limpo");
- formato do uso final: post 4:5 (1080x1350), story 9:16, capa 16:9;
- **carrossel**: uma panorâmica única com a largura de todos os cards
  (3 cards = 3240x1350), e a frase fixa "um fundo fluido, uma só câmera,
  elementos atravessando os pontos de corte, sem emendas". O fatiamento
  sai do canvas, não da IA;
- cores da marca da ficha, em fotografia ou no estilo que o guia mandar;
- com pessoa da ficha: as regras de referência da SKILL (anexo em toda
  mensagem, alternar fotos).

Conferir emendas em 1/3 e 2/3 da panorâmica antes de baixar. Saiu com
emenda, pedir de novo dizendo onde ela está. Salvar o fundo na pasta de
saída da ficha.

## 3. Montar no canvas

1. Abrir o canvas da ficha. Não existe, ou é de outro trimestre: perguntar
   se já há um canvas para isso; não havendo, criar pela ferramenta
   Artifact (`quickstart` com intent `design`) **preso ao design system do
   dono**, com o título "Estúdio <nome> · <AAAA>-T<n>", e gravar o link na
   ficha. Sem design system, criar antes (SKILL, seção Design system). **Um
   canvas por dono e por trimestre**: o canvas tem limite de tamanho (uns
   40 posts). O link antigo fica na ficha, em Canvas anteriores.
2. Páginas do canvas: **Em produção** (a peça da vez), **Referência**
   (fundos e prévias que serviram de ideia) e **uma página por peça
   aprovada**, com a data. Páginas antigas não se releem.
3. Subir o fundo como asset do canvas. Montar a tela no tamanho final com o
   fundo, o texto e a logo, tudo pelos tokens e assets do design system;
   nada de cor ou fonte digitada à mão.
4. **Carrossel**: em cima, a tela larga (1080×N por 1350) com o texto
   corrido; embaixo, os cards já fatiados em 1080x1350, com 8 px entre eles,
   espelhando a tela larga, para mudar junto.
5. Mostrar a prévia. O usuário edita direto no canvas ou pede o ajuste; o
   assistente ajusta no canvas, não gera o fundo de novo, salvo se o
   problema for o fundo.

## 4. Fechar

- Antes de mostrar como pronta, passar o que o repositório exige para peça
  publicada (checklist do conselho, política da plataforma, campo vazio).
- Aprovada: exportar os PNGs no tamanho final para a pasta de saída da
  ficha, `AAAA-MM-DD-<peca>-<n>.png`, e mover a peça para uma página de
  aprovadas no canvas. Sem exportação pelo canvas, renderizar o HTML da
  tela no Chrome headless no tamanho exato.
- **Guia de estilo**: 2 ou 3 linhas no guia da ficha sobre o que funcionou
  e o que foi reprovado. O guia é lido antes de cada peça nova, no lugar de
  reler peças antigas.
- Algo da peça vale para a marca inteira (cor, jeito de título, uso da
  logo): sugerir em uma linha levar ao design system. Só sobe com o
  comando do usuário.
