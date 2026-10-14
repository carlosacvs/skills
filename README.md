# Skills

Skills para o Claude Code.

## estudio

Gera imagem com a pessoa ou a marca certa no ChatGPT (projeto) e no Gemini
(notebook), pelo navegador logado do usuário (Claude in Chrome), uma geração
por vez. Dois modos: imagem pronta, ou só o fundo, com texto e logo montados
no canvas do Claude Design, onde se editam direto.

Cada pessoa ou marca tem uma ficha `estudio.md` com o projeto, o notebook,
as fotos de referência, a pasta de saída e as instruções. Na primeira vez, a
skill monta a ficha a partir do que o repositório já sabe.

### Instalar

```sh
git clone https://github.com/carlosacvs/skills.git
cp -R skills/estudio ~/.claude/skills/
```

Para usar só num projeto, copie para `.claude/skills/` dele. Depois, no
Claude Code, rode `/estudio` ou peça "gera uma imagem para o post".

### Precisa de

- Claude Code com a extensão Claude in Chrome;
- conta no ChatGPT (com Projetos) e/ou no Gemini;
- para o modo fundo + montagem, acesso ao Claude Design no claude.ai.
