# Identidade visual para quem não tem

Antes do design system vem a identidade: cor, fonte, logo, jeito de foto e
tom. Quem já tem, o repositório responde e este arquivo não roda. Quem não
tem, ou tem só pedaços (um Instagram, um cartão, uma logo antiga), passa por
aqui uma vez.

## 1. Juntar o que já existe

Perguntar numa mensagem só, sem exigir tudo:

> "Para montar a identidade, me passe o que tiver: (a) site; (b) Instagram
> ou outra rede; (c) prints ou fotos de material já usado (cartão, fachada,
> receituário, post antigo); (d) logo, se houver; (e) marcas que você admira,
> do seu ramo ou não. Pode ser só uma coisa."

- **Site**: ler pelo navegador (ou pela ferramenta de leitura de site do
  repositório): cores usadas, fontes, logo, fotos e o texto da página
  inicial. Respeitar a regra do repositório para abrir link.
- **Instagram**: abrir o perfil e olhar a grade, a bio e os destaques. Sem
  login ou bloqueado, pedir print da grade.
- **Prints e fotos**: ler a imagem; tirar as cores pelo arquivo (amostrar
  pixels), não de olho.
- **Marcas admiradas**: servem de direção, nunca de cópia. Não reproduzir
  logo, paleta inteira ou fonte proprietária de outra marca, sobretudo do
  mesmo ramo e da mesma cidade.

Mostrar o que foi achado, em poucas linhas: "Achei isto: azul-petróleo em
quase tudo, fonte sem serifa, logo só em texto, fotos claras de consultório."

## 2. Entrevista curta

Só as perguntas que o passo 1 não respondeu, de uma vez, numeradas, para
responder por número:

1. Nome que aparece na marca, e o que faz, para quem.
2. Três palavras que a marca deve passar (ex.: acolhedora, técnica, leve).
3. Três que ela não pode passar (ex.: fria, barata, infantil).
4. Cores que gosta e cores que não quer de jeito nenhum.
5. Tem logo? Se tem, gosta dela ou quer refazer?
6. Onde a marca mais aparece: Instagram, site, impresso, fachada.
7. Vai aparecer em foto (rosto) ou a marca fala sem pessoa?
8. Há regra de conselho ou de profissão para o que pode ser mostrado?

Resposta vaga ("tanto faz") vira escolha do assistente, declarada como tal.

## 3. Propor duas direções

Duas direções, não cinco. Cada uma com:

- **Paleta**: principal, apoio, neutro claro, neutro escuro e destaque, com
  o hex e o uso de cada uma. Conferir contraste do texto sobre o fundo
  (mínimo 4,5:1 em texto corrido).
- **Fontes**: uma para título e uma para texto, de licença livre (Google
  Fonts), com o motivo da escolha.
- **Logo**: se existe, como usar (versões, área livre, fundo claro e
  escuro). Se não existe, propor logotipo só com o nome na fonte de título;
  símbolo desenhado fica para um designer, e o assistente diz isso em uma
  linha. Logo gerada por IA não se usa como marca registrável.
- **Foto**: luz, cenário, enquadramento e o que evitar.
- **Tom**: duas frases de exemplo, uma de post e uma de chamada.
- **Amostra**: uma peça de teste (post 4:5) em cada direção, montada em
  HTML com o nome e um texto real, para o usuário ver aplicado.

Mostrar as duas lado a lado num artifact (página com as duas pranchas). O
usuário escolhe uma, mistura ou pede ajuste. Tudo que o assistente escreveu
(paleta, tom, frases) vem marcado como dele.

## 4. Virar design system

Com a direção aprovada:

1. Criar o design system pela ferramenta Artifact (`quickstart` com intent
   `other`, tipo Design System), com os tokens da direção, a logo e um
   README curto: quem é, as três palavras, o que evitar, como usar a logo e
   a foto.
2. Gravar o link na ficha `estudio.md`, seção Montagem, e a data.
3. Se o repositório guarda identidade em arquivo (`identidade-visual/`,
   `marca.md`, design guide), escrever lá também, como cópia que aponta
   para o design system.
4. Acrescentar a paleta e o jeito de foto ao descritivo do projeto de
   imagem (passo 2.5 da SKILL), perguntando antes se o projeto já existe.

## Fora daqui

Registro de marca no INPI, manual de marca completo e símbolo desenhado
são trabalho de designer. A skill entrega uma identidade de trabalho,
coerente e usável, e diz isso ao usuário quando ele pedir mais.
