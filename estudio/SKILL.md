---
name: estudio
description: Gera imagem com a pessoa ou a marca certa no ChatGPT (projeto) e no Gemini (notebook), pelo navegador, uma geração por vez, com o usuário na sessão. Dois modos, imagem pronta ou fundo + montagem (a IA gera só o fundo e o texto e a logo se montam no canvas do estúdio, editável). Cada repositório, e cada cliente dentro dele, tem a sua ficha `estudio.md` com o projeto, o notebook, o canvas, a marca, as fotos de referência, a pasta de saída e as instruções; a skill acha a ficha da tarefa e, se não houver, monta tudo na primeira vez. Use quando o usuário disser "monta o post", "faz o carrossel", "gera só o fundo", "monta no estúdio", "capa", "banner", ou quando o usuário disser "gera imagem", "gera uma foto da <pessoa>", "faz uma cena", "imagem para o site", "imagem para o post", "fundo para o carrossel", "estúdio", "pede no ChatGPT", "pede no Gemini", "cria o projeto de imagem", "cria a identidade visual", "não tenho logo nem cores", "monta o design system", ou rodar /estudio.
---

# estudio

Uma skill para qualquer repositório. Ela não sabe de quem é a imagem: quem
sabe é a **ficha** `estudio.md` do lugar onde a tarefa está.

## Regras do repositório vêm antes

A skill não traz regra de autorização, de privacidade ou de conformidade.
Vale o que o repositório manda (AGENTS.md, CLAUDE.md, fichas): se ele exige
autorização para abrir site, para ler fora da pasta ou para cada geração,
pedir antes; se ele barra imagem no Git, salvar só onde ele permite; se a
pessoa é profissional regulada, seguir o checklist do conselho dela.

Sempre, em qualquer repositório:

- uma geração por vez, no ritmo de uma pessoa, com o usuário na sessão;
- nunca em lote agendado, nunca por robô headless: só pelo navegador logado
  do usuário (Claude in Chrome);
- nada de foto de terceiro sem o usuário dizer de quem é; o assistente não
  reconhece pessoa pelo rosto.

## Com calma, para não perder a conta

O ChatGPT e o Gemini não foram feitos para serem operados por assistente, e
podem limitar ou suspender conta com uso que pareça robô. A skill fala disso
com o usuário, não só segue em silêncio:

- **No começo de cada sessão de geração**, uma linha: "Vou no ritmo de uma
  pessoa, uma imagem por vez. Se o ChatGPT ou o Gemini mostrarem qualquer
  aviso, eu paro e te chamo." Na primeira vez, junto, a sugestão de usar
  uma conta dedicada a esse trabalho, não a conta pessoal do dia a dia.
- **Ritmo**: esperar a imagem terminar antes do próximo pedido; nunca duas
  abas gerando ao mesmo tempo; nunca reenviar o mesmo pedido em sequência.
  Padrão da skill, ajustável na ficha: depois de **10 imagens na sessão**,
  sugerir uma pausa e perguntar se segue.
- **Pedido grande** (carrossel inteiro, lote de fotos para site): dizer
  antes quantas gerações vão ser e sugerir dividir em mais de um dia.
- **Sinal de alerta, para na hora e avisa**: captcha ou "confirme que você
  é humano"; "atividade incomum"; limite de uso atingido ("tente de novo em
  X horas"); pedido de novo login ou verificação; erro repetido na mesma
  geração. Não tentar contornar, não trocar de conta sozinho e não insistir:
  dizer o que apareceu e esperar o usuário decidir.
- **O usuário manda seguir, segue.** O freio é aviso, não trava: a conta é
  dele e a decisão também. Disse "segue", "continua" ou "pode ir": seguir
  sem repetir o alerta pelo mesmo motivo na mesma sessão (a pausa das 10
  volta só nas próximas 10). Captcha, verificação e login quem resolve é o
  usuário, na tela; resolvido, seguir. Limite de uso atingido: ali não dá
  mais, e ele escolhe outro destino ou outra hora.
- **O usuário digita a senha e os códigos**, sempre. O assistente nunca.

## Ajudantes em paralelo, com modelo menor

A geração é uma só, na sessão principal. O trabalho em volta dela pode ir
para subagentes com um modelo menor e mais barato (o Haiku, por exemplo),
rodando ao mesmo tempo, quando a ferramenta tiver subagente:

- escrever os textos da peça ou dos cards do carrossel, a partir da ficha
  e do pedido;
- ler site, Instagram ou prints para a identidade (`identidade.md`),
  dentro da regra do repositório para abrir link;
- conferir o texto contra o checklist do conselho e a política da
  plataforma que o repositório tiver;
- levantar na pasta de saída e no acervo se já existe imagem que sirva.

Regras:

- **Subagente nunca usa o navegador**: não abre ChatGPT, Gemini nem
  canvas, não gera e não baixa imagem. Navegador é só da sessão principal.
- Cada subagente recebe só o que a tarefa dele precisa; num cliente, só a
  pasta dele.
- Subagente não escreve na ficha nem no canvas: devolve o resultado, e a
  sessão principal confere, decide e registra. Texto escrito por subagente
  é texto do assistente e se declara como tal.
- **Mostrar ao usuário** o que está rodando, numa linha ao disparar
  ("rodando em paralelo: textos dos 3 cards, conferência do conselho") e o
  que cada um devolveu. Ele acompanha cada subagente no painel da
  ferramenta.
- Tarefa curta (um título, uma conferência rápida): fazer direto, sem
  subagente.

## 1. Achar a ficha

Partir da pasta da tarefa e subir até a raiz do repositório. Em cada pasta,
olhar só `estudio.md` nela mesma ou na pasta de criativos dela
(`04-criativos/` ou `criativos/`); vale a primeira encontrada. Nunca olhar
pasta vizinha: a ficha de um cliente não serve para outro. Na prática:

- tarefa de um cliente (`clientes/<slug>/...`): a ficha do cliente, em
  `clientes/<slug>/04-criativos/estudio.md`;
- tarefa da casa (numa pasta da própria empresa, ou na raiz): o
  `estudio.md` daquela pasta ou da raiz.

```sh
d="<caminho-absoluto-da-pasta-da-tarefa>"; r=$(git -C "$d" rev-parse --show-toplevel)
while :; do
  for f in "$d/estudio.md" "$d/04-criativos/estudio.md" "$d/criativos/estudio.md"; do
    [ -f "$f" ] && echo "$f" && break 2; done
  [ "$d" = "$r" ] && break; d=$(dirname "$d"); done
```

Sem pasta de tarefa clara, perguntar em uma linha de quem é a imagem.

Achou: ler a ficha inteira (instruções, fotos, aprendizados) e ir ao passo 3.
Não achou: passo 2.

## Dois modos

- **Imagem pronta**: foto ou cena sem texto (site, retrato, banco de
  imagens). Passos 3 e 4.
- **Fundo + montagem**: peça com texto ou logo (post, carrossel, capa,
  banner, story). A IA gera **só o fundo**, sem texto e sem logo; o texto,
  a logo e o ajuste fino se montam no canvas do estúdio, onde o usuário
  corrige direto. Ler `montagem.md` (nesta pasta) e seguir.

**Peça com texto: perguntar antes de gerar**, numa linha só, a não ser que
o pedido já diga:

> "Como fazemos? (1) versão completa, já com os textos, para servir de
> referência e mapa; (2) só o fundo, para montar no estúdio; (3) as duas:
> primeiro a completa como mapa, depois o fundo seguindo ela."

- **(1) Completa**: a IA gera a peça inteira, com texto e composição. É
  prévia, não peça final: o texto da IA não se corrige e a resolução
  costuma ser baixa. Salvar como `AAAA-MM-DD-<peca>-mapa.png`.
- **(2) Só o fundo**: segue `montagem.md`.
- **(3) As duas**: gerar a completa, mostrar, e com o ok pedir o fundo na
  mesma conversa: "o mesmo fundo, sem nenhum texto, sem logo, com as áreas
  do texto livres". A completa vai para a página Referência do canvas e
  guia onde cada texto entra na montagem.

Foto ou cena sem texto não pergunta: é imagem pronta.

## 2. Primeira vez: montar projeto, notebook e ficha

**Nada se cria nem se sobrescreve sem perguntar.** Ficha sem link não quer
dizer que o projeto não existe: pode ter sido criado à mão.

### Antes de tudo: explicar, combinar o lugar e pedir as permissões

Numa mensagem só, antes de criar qualquer arquivo ou abrir qualquer site:

1. **O que vai acontecer**, em poucas linhas: a skill vai criar uma ficha
   `estudio.md` com as informações da marca; abrir o ChatGPT e o Gemini no
   navegador dele para criar o projeto e o notebook; subir algumas fotos e a
   logo; e, a cada imagem, baixar o arquivo e guardar numa pasta.
2. **Onde criar**, propondo o lugar e deixando trocar:
   - a ficha: a pasta de criativos do dono, se houver; senão, a pasta da
     marca ou a raiz do repositório;
   - a pasta das fotos de referência (onde já estão, ou onde ele vai pôr);
   - a pasta de saída das imagens.

   Se o repositório versiona tudo no Git, avisar que imagem pesa e pode ter
   pessoa: propor a pasta de saída fora do Git (no `.gitignore` ou na pasta
   que o repositório já usa para isso) e perguntar.
3. **As permissões que vão aparecer**, para ele aceitar sabendo o porquê:
   - **Claude in Chrome**: permitir os sites chatgpt.com,
     gemini.google.com e claude.ai, para ler a tela, digitar o pedido,
     anexar fotos e baixar a imagem. Sugerir "sempre permitir" nesses três.
   - **Login**: ele entra nas contas, no próprio navegador. O assistente
     nunca digita senha nem código de verificação. Lembrar, em uma linha,
     que uma conta dedicada a esse trabalho é mais segura que a pessoal.
   - **Chrome, vários downloads**: na segunda imagem baixada, o Chrome
     pergunta se o site pode baixar vários arquivos. Responder "Permitir".
   - **Claude Code**: ler a pasta das fotos, criar a ficha, e mover a
     imagem da pasta Downloads para a pasta de saída. Mexer fora do
     repositório (a pasta Downloads) costuma pedir aprovação; ele pode
     aprovar uma vez ou deixar liberado.
   - Se o repositório tiver regra própria de autorização (comando para
     abrir site, para gerar, para ler fora da pasta), dizer qual é e
     esperar por ela.
4. **O que já existe**: a pergunta do item 1 abaixo vai na mesma mensagem.

Só seguir com o ok. Gravar na ficha os lugares combinados.

1. **Perguntar antes, na mesma mensagem**: "Já existe projeto no ChatGPT,
   notebook no Gemini ou design system (em artifact ou no claude.ai/design)
   para <dono>? Se sim, me passe o nome ou o link." No navegador, conferir também a lista de projetos do ChatGPT
   e de notebooks do Gemini pelo nome, e a lista de design systems do
   usuário (ferramenta Artifact).
2. **Já existe**: só ler e gravar o link na ficha. Não colar instruções,
   não subir arquivo, não trocar nada. Comparar o que está lá com o que o
   passo 4 escreveria e, se diferir, **perguntar se atualiza**, mostrando a
   diferença. Sem o sim, fica como está.
3. Não existe: copiar `modelo-estudio.md` (nesta pasta) para o lugar
   combinado, e preencher nela a pasta das fotos e a pasta de saída.
4. **Extrair o que o repositório já sabe.** Antes de perguntar qualquer
   coisa, ler as fontes do dono: AGENTS.md, CLAUDE.md, README, ficha do
   cliente, posicionamento, público, tom de voz, identidade visual, pauta e
   regras de conformidade. Num cliente, só a pasta dele e as regras gerais
   do repositório; nunca a de outro cliente.
5. **Escrever o descritivo** a partir disso, no bloco de instruções da
   ficha, nesta ordem: quem é (e o que faz, para quem); tom das imagens;
   como a pessoa aparece (rosto, corpo e idade idênticos às fotos, sem
   "embelezar"); cenário; nunca gerar (tirado das regras de conformidade e
   da ficha, com a fonte de cada item); paleta (lida do design system);
   fotografia ou ilustração; texto e logo fora da imagem; formatos. Curto e
   concreto: o projeto lê tudo a cada pedido. Dado que não está no
   repositório fica "[a preencher]", nunca palpite.
6. **Escolher os arquivos do projeto**: 2 a 10 fotos da pessoa (nítidas,
   luz boa, rosto e corpo), a logo e, se ajudar, um resumo de marca de uma
   página escrito para o projeto. **Nunca** subir documento inteiro do
   repositório: ficha, ICP, avatar ou briefing podem ter dado sensível (de
   paciente, de lead, de contrato). Na dúvida, resumir o que serve e
   deixar o original de fora.
7. Mostrar ao usuário, de uma vez: o descritivo, a lista de arquivos e só
   as perguntas que o repositório não respondeu (nome do projeto, qual
   conta, quais fotos). Marcar o que o assistente escreveu. Criar só com o
   ok.
8. **ChatGPT**: chatgpt.com › Projetos › Novo projeto, com o nome da ficha.
   Colar as instruções no campo do projeto e subir os arquivos. Copiar o
   link do projeto.
9. **Gemini**: gemini.google.com, na conta que a ficha indicar, criar o
   notebook com o mesmo nome, colar as instruções e subir só a logo e o
   resumo de marca. **Foto de pessoa não vai como fonte do notebook**: o
   Gemini recusa rosto nítido ("Conteúdo incompatível") e a fonte recusada
   fica contando e pode travar a conversa; a foto vai anexada em cada
   mensagem. Se a conta não tiver notebook, criar um Gem (Gems ›
   Novo Gem) e anotar na ficha qual dos dois foi. Copiar o link.
10. Gravar os dois links e a data na ficha. O design system nasce na
    primeira peça com texto (`montagem.md`), com a mesma pergunta antes.

**Atualizar** projeto, notebook ou design system que já existe ("atualiza o
descritivo do projeto") é sempre perguntado: reler as fontes, mostrar o que
mudou e, só com o sim, colar de novo. Nunca apagar arquivo do projeto ou do
notebook sem pedido.

## Design system: a marca mora nele

Cada dono tem um design system no claude.ai (artifact do tipo Design
System, ou projeto no claude.ai/design). **Ele manda** em cor, fonte, logo,
espaço e raio. A ficha guarda só o link; nunca copia hex nem nome de fonte.
Se a ficha lista mais de um, ela diz qual é o oficial e qual está em teste:
a sincronização abaixo vale só para o oficial, e dois design systems nunca
se misturam, se apagam ou se copiam um no outro.

- **Design system → repositório, automático.** Se a ficha aponta uma cópia
  local da marca (tokens, design guide), a cada uso ler o `tokens.json` e o
  `README.md` do design system e comparar com a cópia. Mudou valor:
  atualizar a cópia (o mesmo nome de token, o valor novo) e o texto que a
  traduz, e avisar em uma linha o que mudou. Token novo entra; token que
  sumiu do design system se lista ao usuário antes de sair da cópia. Gravar
  na ficha a data do `lastChange` lido.
- **Repositório ou canvas → design system, só por comando do usuário**
  ("leva pro design system", "atualiza o design system"). Peça aprovada com
  um padrão que vale para a marca: o assistente pode sugerir em uma linha,
  e não sobe nada sem o comando. Com o comando: mostrar a diferença e
  publicar no design system seguindo as instruções do tipo.
- **Espelho no claude.ai/design**, se a ficha listar um: é cópia, nunca
  manda. Só se lê ou escreve nele pelo comando `/design-sync`, que o
  usuário inicia. Mudou o design system que manda: avisar em uma linha que
  o espelho ficou atrasado até o próximo `/design-sync`.
- **Dono com design system só no claude.ai/design** (nenhum em artifact):
  não criar do zero. Pedir ao usuário que rode `/design-sync`, ler o
  projeto de lá (tokens, readme, logos), criar o artifact a partir dele,
  conferir que os valores batem e registrar o projeto como espelho na
  ficha. Nada se apaga nem se altera lá nesse passo.
- Dono sem design system: criar na primeira peça com texto, a partir da
  identidade que o repositório tiver, depois da pergunta do passo 2.1.
  **Sem identidade visual** (sem cor, fonte ou logo definidas, ou o
  usuário pede "cria a identidade"): seguir `identidade.md` (nesta pasta)
  antes de criar o design system.

## 3. Gerar

1. **Onde gerar é escolha do usuário, na hora.** Se o pedido já diz
   ("no ChatGPT", "no Gemini", "no <PROJETO> 2"), seguir. Se não diz e a
   ficha tem mais de um destino, perguntar numa linha só, com os destinos
   da tabela numerados: "Onde gero? (1) ChatGPT, <PROJETO>; (2) ChatGPT,
   <PROJETO> 2; (3) Gemini, notebook <PROJETO>". Vários números valem: o
   mesmo pedido roda em cada destino escolhido, um depois do outro. A
   ficha não guarda destino preferido. Abrir o link do destino e começar
   conversa nova dentro dele. **Nunca gerar fora do destino** (conversa
   avulsa, outro projeto) sem perguntar: se o destino travar (mais de 5
   minutos sem imagem), parar a geração e perguntar em uma linha se tenta
   de novo ali ou onde gera.
2. **Anexar 2 ou 3 fotos de referência em toda mensagem**, não só na
   primeira. Foto guardada no projeto não vira referência de rosto: sem
   anexo, sai outra pessoa. No ChatGPT, por **+ › Adicionar da biblioteca**
   ou subindo do disco.
3. **Alternar as fotos** de um pedido para o outro; com as mesmas, todas as
   imagens saem com a mesma cara.
4. Montar o pedido com a cena, o formato (proporção e uso) e as linhas fixas
   que a ficha mandar repetir. No Gemini, o pedido vai **num parágrafo só**:
   texto com quebra de linha entra fora de ordem na caixa.
5. Para manter o rosto no Gemini, usar o modo edição: "edite a foto anexada:
   troque só roupa e ambiente".
6. Enviar **clicando no botão**, não no Enter (há extensão que inverte Enter
   e Cmd+Enter). Conferir se o começo do texto não foi cortado ao digitar.
7. Conferir a imagem antes de baixar: rosto, mãos, dedos, acessórios,
   texto indevido e o que a ficha proíbe. Errou, pedir ajuste na mesma
   conversa.
8. Baixar e mover para a pasta de saída da ficha com o nome
   `AAAA-MM-DD-<o-que-e>-<formato>.png`. Lote vai numa subpasta
   `AAAA-MM-DD-loteN/`. O Chrome bloqueia downloads em sequência até alguém
   liberar o site: no primeiro bloqueio, parar e pedir ao usuário.

Formato: ChatGPT costuma entregar 3:4 mesmo pedindo 4:5 (cortar depois);
Gemini entrega maior. Panorâmica para carrossel: pedir "um fundo fluido, uma
só câmera, elementos atravessando os pontos de corte".

## 4. Registrar

- Aprendeu algo sobre a pessoa ou a ferramenta (cabelo mudou, acessório a
  evitar, pedido que funcionou): uma linha em **Aprendido** na ficha, com a
  data.
- O que foi gerado e onde ficou: no registro do dia que o repositório usar.

## Pedido vindo de outra sessão

Outra sessão (por exemplo, a que monta uma página) pode pedir imagem por
mensagem à sessão que está gerando. A sessão que gera executa só pedido de
imagem, dentro da autorização em vigor no repositório, salva na pasta de
saída da ficha e responde com o caminho do arquivo.
