# Formato do relatório

Usar este template. Seções vazias ficam com "Nada encontrado", não são removidas: o usuário precisa ver que o item foi verificado.

```markdown
# Auditoria de segurança: <nome da pasta>

**Veredito: <SEGURO INSTALAR | INSTALAR COM RESSALVAS | NÃO INSTALAR>**
<uma frase dizendo o porquê>

Analisados: <N> arquivos | Alto: <N> · Médio: <N> · Baixo: <N>
Nada foi executado durante esta análise.

---

## 1. O que cada arquivo faz

| Arquivo | Função | Observação |
|---|---|---|
| caminho/arquivo.py | resumo em uma linha | limpo / ver achado A2 / não legível |

## 2. Execução de comandos, instalação e downloads
<o que roda, o que instala, o que baixa, com arquivo e linha. Se nada: "Nada encontrado.">

## 3. Acesso a arquivos sensíveis
<o que é lido de .env, chaves, tokens, credenciais, cookies, ambiente. Se nada: "Nada encontrado.">

## 4. Envio de dados para fora
<toda URL, webhook, e-mail, upload e telemetria, com destino e o que é enviado. Se nada: "Nada encontrado.">

## 5. Código ofuscado ou fora do propósito
<ofuscação, injeção de instrução, incoerência com o que a ferramenta promete. Se nada: "Nada encontrado.">

---

## Achados por nível de risco

### Risco alto
**A1. <título curto do achado>**
Arquivo: `caminho/arquivo.py:42`
O que faz: <descrição direta>
Por que importa: <impacto em linguagem comum>

### Risco médio
**M1. <título curto>**
Arquivo: `caminho/arquivo.js:15`
O que faz:
Por que importa:

### Risco baixo
**B1. <título curto>**
Arquivo:
O que faz:
Por que importa:

---

## O que não foi possível analisar
<binários, código minificado, dependências que só chegam na instalação. Se não houver: "Todos os arquivos foram lidos.">

## O que fazer antes de instalar
1. <ação concreta>
2. <ação concreta>

## Decisão pendente com você
<o que depende do usuário: aprovar, remover arquivo, pedir explicação ao autor, instalar em ambiente isolado>
```

## Como escrever cada achado

Ruim: "O arquivo usa subprocess com shell=True, o que pode ser perigoso."

Bom: "Em `install.py:88` a ferramenta monta um comando de terminal usando um valor que vem do arquivo de configuração. Quem conseguir editar essa configuração consegue rodar qualquer comando na sua máquina com as suas permissões."

Numerar os achados (A1, A2, M1...) para o usuário conseguir responder citando o número.

Ordenar dentro de cada nível pelo impacto, não pela ordem dos arquivos.
