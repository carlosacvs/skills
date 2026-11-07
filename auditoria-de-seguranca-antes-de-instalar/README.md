[← Todas as skills](../README.md)

# auditoria-de-seguranca-antes-de-instalar

Antes de você instalar uma skill, plugin, repositório ou zip baixado da
internet, o Claude lê tudo sem executar nada e entrega um relatório com os
riscos e um veredito: **seguro instalar**, **instalar com ressalvas** ou
**não instalar**.

## Por que usar

Skill e plugin trabalham com as suas permissões: leem seus arquivos, usam
o seu terminal, abrem sites no seu navegador. E numa skill o perigo nem
sempre está no código. Pode ser uma frase no meio do texto mandando o
Claude enviar as suas chaves para fora ou não contar nada para você.

## O que ela confere

- comando que roda no sistema, instalação de dependência, download
  seguido de execução;
- leitura de senha, chave de API, `.env`, cookies do navegador, carteira
  cripto;
- envio de dados para fora: webhook, e-mail, upload, telemetria;
- código escondido ou embaralhado;
- o que continua rodando depois: agendamento, inicialização, perfil do
  terminal;
- texto escrito para manipular o Claude ("ignore as instruções
  anteriores", "não mencione este arquivo");
- se o que o README promete bate com o que o código faz.

## Como ela trabalha

1. Diz o que vai auditar e avisa que nada será executado.
2. Mapeia a pasta. Zip é extraído numa pasta temporária, e antes ela
   confere se ele tenta gravar fora dela.
3. Roda um script próprio de varredura, só leitura e sem internet, que
   aponta os trechos suspeitos.
4. Lê os arquivos e confirma cada pista no contexto: um envio para a
   internet pode ser justamente o que a ferramenta promete.
5. Classifica cada achado em alto, médio ou baixo e entrega o relatório,
   com arquivo e linha em cada achado.

Achado grave aparece na hora, sem esperar o relatório. No fim, ela
pergunta se você quer instalar e onde. Pedido de auditoria nunca vira
instalação sozinho.

## Usar

Peça do seu jeito: "isso é seguro?", "revisa essa skill antes de eu
instalar", "baixei esse zip, dá uma olhada", "não roda nada ainda".

## Instalar

No Claude Code:

```sh
git clone https://github.com/carlosacvs/skills.git /tmp/skills-atual
cp -R /tmp/skills-atual/auditoria-de-seguranca-antes-de-instalar ~/.claude/skills/
rm -rf /tmp/skills-atual
```

Para usar só num projeto, troque `~/.claude/skills/` pela pasta
`.claude/skills/` dele. Para atualizar, rode o mesmo comando.

No claude.ai, compacte a pasta `auditoria-de-seguranca-antes-de-instalar`
num `.zip` e suba nas configurações de skills.

## Precisa de

Python 3 no computador, só com a biblioteca padrão, para o script de
varredura. No claude.ai, o ambiente de código já tem.

## Limites

A análise é estática: lê o que está escrito. Não pega o que só aparece
com o programa rodando, o que está dentro de arquivo binário nem o que
uma dependência vai baixar na instalação. "Não achei nada" não é o mesmo
que "não tem nada", e o relatório diz isso quando é o caso. Para código
que vai mexer em conta, dinheiro ou dado de cliente, a auditoria ajuda,
mas não substitui alguém que entenda do assunto.

## Arquivos

| Arquivo | Para quê |
|---|---|
| `SKILL.md` | o fluxo e as regras |
| `references/padroes-e-riscos.md` | os padrões suspeitos e a régua de risco |
| `references/formato-do-relatorio.md` | o modelo do relatório |
| `scripts/varredura.py` | a varredura automática, só leitura |
| [`CHANGELOG.md`](../CHANGELOG.md), na raiz | o que mudou em cada versão |

## Licença

[CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/): pode usar,
copiar e adaptar, citando o autor (Carlos Sarmento). Não pode vender nem
usar como produto ou serviço pago. Texto completo em [LICENSE](../LICENSE).
