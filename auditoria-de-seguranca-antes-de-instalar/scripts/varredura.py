#!/usr/bin/env python3
"""
Varredura estatica de uma pasta antes de instalar qualquer coisa.

Somente leitura: nao executa, nao instala, nao acessa a rede, nao escreve
nada dentro da pasta auditada. Usa apenas a biblioteca padrao.

Uso:
    python3 varredura.py <pasta>
    python3 varredura.py <pasta> --tudo     inclui node_modules, venv, .git
    python3 varredura.py <pasta> --json     saida estruturada
"""

import argparse
import json
import os
import re
import sys

PASTAS_IGNORADAS = {
    ".git", "node_modules", "venv", ".venv", "env", "__pycache__",
    "dist", "build", ".next", "target", ".tox", "site-packages",
}

EXT_BINARIAS = {
    ".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico", ".pdf", ".zip",
    ".gz", ".tar", ".7z", ".rar", ".exe", ".dll", ".so", ".dylib",
    ".bin", ".pyc", ".pyd", ".class", ".jar", ".woff", ".woff2",
    ".ttf", ".otf", ".mp3", ".mp4", ".mov", ".wasm", ".db", ".sqlite",
}

EXT_EXECUTAVEIS = {".sh", ".bash", ".zsh", ".bat", ".cmd", ".ps1", ".psm1"}

# categoria -> lista de (rotulo, regex)
PADROES = {
    "EXECUCAO_DE_COMANDOS": [
        ("os.system", r"\bos\.system\s*\("),
        ("os.popen", r"\bos\.popen\s*\("),
        ("subprocess", r"\bsubprocess\.(run|call|check_output|check_call|Popen)\s*\("),
        ("shell=True", r"shell\s*=\s*True"),
        ("child_process (node)", r"require\s*\(\s*['\"]child_process['\"]|from\s+['\"]child_process['\"]"),
        ("exec/spawn (node)", r"\b(execSync|spawnSync|execFileSync|execFile)\s*\(|\b\w*[cC]hild_?[pP]rocess\w*\.(exec|spawn)\s*\("),
        ("Runtime.exec (java)", r"Runtime\.getRuntime\(\)\.exec"),
        ("Invoke-Expression", r"\b(Invoke-Expression|iex)\b"),
        ("EncodedCommand", r"-EncodedCommand"),
        ("rm -rf", r"rm\s+-[rRf]{1,2}f?\s"),
        ("chmod amplo", r"chmod\s+(\+x|777|a\+rwx)"),
        ("sudo", r"\bsudo\b"),
        ("dd / mkfs", r"\b(dd\s+if=|mkfs)"),
    ],
    "INSTALACAO_DE_DEPENDENCIAS": [
        ("pip install", r"\b(pip3?|uv pip)\s+install\b"),
        ("npm/yarn/pnpm install", r"\b(npm\s+(i|install|ci)|yarn\s+add|pnpm\s+(add|install))\b"),
        ("apt/brew/gem/cargo/go", r"\b(apt-get\s+install|apt\s+install|brew\s+install|gem\s+install|cargo\s+install|go\s+install)\b"),
        ("hook de instalacao npm", r"\"(pre|post)install\"\s*:|\"prepare\"\s*:"),
        ("setup.py com codigo", r"\bsetup\s*\(\s*$|cmdclass\s*="),
    ],
    "DOWNLOAD_E_EXECUCAO_REMOTA": [
        ("curl/wget encanado no shell", r"(curl|wget)[^\n|]*\|\s*(ba)?sh"),
        ("iwr encanado no iex", r"(iwr|Invoke-WebRequest)[^\n|]*\|\s*iex"),
        ("eval de conteudo baixado", r"(eval|exec)\s*\(\s*(requests|urlopen|fetch|urllib)"),
        ("new Function com fetch", r"new\s+Function\s*\("),
        ("install a partir de URL/git", r"(pip3?\s+install|npm\s+i(nstall)?)\s+(https?://|git\+)"),
        ("download de arquivo", r"\b(urlretrieve|wget|curl\s+-[oO]|downloadFile|createWriteStream)\b"),
    ],
    "ARQUIVOS_E_CREDENCIAIS_SENSIVEIS": [
        ("arquivo .env", r"\.env(\.local|\.production)?\b"),
        ("chaves ssh", r"\.ssh/|id_rsa|id_ed25519|authorized_keys|known_hosts"),
        ("credenciais de nuvem", r"\.aws/credentials|\.kube/config|\.docker/config\.json|gcloud/credentials"),
        ("credenciais de registro", r"\.npmrc|\.pypirc|\.netrc|\.git-credentials"),
        ("chaveiro / cofre do sistema", r"Keychain|keyring|libsecret|CredentialManager|wincred"),
        ("cookies e sessao do navegador", r"Cookies|Login Data|places\.sqlite|Local Storage|session\.json"),
        ("carteira cripto", r"wallet\.dat|keystore|mnemonic|seed phrase|metamask"),
        ("ambiente inteiro", r"dict\s*\(\s*os\.environ|os\.environ\.copy\s*\(|JSON\.stringify\s*\(\s*process\.env|\{\s*\.\.\.process\.env"),
        ("variavel de segredo", r"\b(API_?KEY|SECRET|ACCESS_?TOKEN|PRIVATE_?KEY|PASSWORD|PASSWD|CLIENT_SECRET)\b"),
        ("chave de IA", r"\b(ANTHROPIC_API_KEY|OPENAI_API_KEY|sk-ant-|sk-[A-Za-z0-9]{20,})"),
        ("pastas pessoais amplas", r"(Documents|Desktop|Downloads|Library|AppData)[/\\]"),
    ],
    "SAIDA_DE_DADOS": [
        ("requisicao http (python)", r"\b(requests|httpx|aiohttp)\.(get|post|put|patch|delete)\s*\("),
        ("urllib", r"\burllib\.request|urlopen\s*\("),
        ("fetch/axios (js)", r"\b(fetch|axios(\.\w+)?)\s*\("),
        ("socket bruto", r"\bsocket\.socket\s*\(|net\.(connect|createConnection)|new\s+WebSocket"),
        ("envio de e-mail", r"\bsmtplib\b|nodemailer|sendmail"),
        ("ssh/ftp/upload", r"\bparamiko\b|\bftplib\b|\bscp\b|multipart/form-data"),
        ("webhook discord/slack", r"discord(app)?\.com/api/webhooks|hooks\.slack\.com"),
        ("api de bot telegram", r"api\.telegram\.org"),
        ("coletor temporario", r"(pastebin|hastebin|ngrok|requestbin|webhook\.site|transfer\.sh|0x0\.st|termbin)"),
        ("ip cru como destino", r"https?://\d{1,3}(\.\d{1,3}){3}"),
        ("telemetria declarada", r"\b(telemetry|analytics|track(ing)?Event|posthog|mixpanel|amplitude|sentry)\b"),
        ("url qualquer", r"https?://[^\s'\"<>)]{4,}"),
    ],
    "OFUSCACAO": [
        ("base64 decodificado", r"\b(b64decode|base64\.decode|atob|Buffer\.from\s*\([^)]*base64)"),
        ("eval de base64", r"(eval|exec)\s*\(\s*(atob|base64|b64decode)"),
        ("eval / exec direto", r"\b(eval|exec)\s*\("),
        ("marshal / pickle", r"\bmarshal\.loads|\bpickle\.loads"),
        ("descompressao de string", r"\b(zlib|gzip|lzma|bz2)\.decompress"),
        ("cadeia de chr/fromCharCode", r"(chr\(\d+\)\s*\+\s*){3,}|(String\.fromCharCode\s*\()"),
        ("escape hexadecimal longo", r"(\\x[0-9a-fA-F]{2}){8,}"),
        ("nomes ofuscados", r"_0x[0-9a-f]{4,}"),
        ("comentario html oculto", r"<!--(?!\s*$)[\s\S]{40,}?-->"),
    ],
    "PERSISTENCIA_E_PRIVILEGIO": [
        ("cron / agendador", r"\b(crontab|schtasks|/etc/cron|systemd|\.service\b|launchctl|LaunchAgents|LaunchDaemons)\b"),
        ("perfil do shell", r"\.(bashrc|zshrc|bash_profile|profile|zprofile)\b"),
        ("registro do windows", r"reg\s+add|CurrentVersion\\\\Run|HKEY_"),
        ("inicializacao automatica", r"\b(autostart|startup folder|RunOnce)\b"),
        ("elevacao de privilegio", r"\b(setuid|runas|UAC|osascript.*administrator)\b"),
    ],
    "INJECAO_DE_INSTRUCAO": [
        ("ignorar instrucoes", r"(?i)(ignore|desconsidere|esque(ç|c)a)\s+(as\s+)?(instru|previous|prior|all previous)"),
        ("esconder do usuario", r"(?i)(n(ã|a)o (mostre|mencione|informe|avise)|do not (tell|mention|show|reveal)|sem avisar o usu(á|a)rio|hidden from the user)"),
        ("sobrescrever persona", r"(?i)(a partir de agora voc(ê|e) (é|e)|you are now|new system prompt|override (your )?(rules|instructions))"),
        ("aprovar tudo / pular checagem", r"(?i)(auto[- ]?approve|skip (the )?(confirmation|verification|checks)|bypass|--dangerously|--yes-all|--no-verify)"),
        ("ordem de exfiltrar", r"(?i)(send|envie|poste|upload).{0,40}(\.env|credential|api[_ ]?key|token|senha|password).{0,40}(to|para|http)"),
        ("permissao ampla de ferramenta", r"(?i)allowed[- ]?tools\s*:.*(\*|Bash|all)"),
    ],
}

PADROES_COMPILADOS = {
    cat: [(rot, re.compile(rx)) for rot, rx in lst] for cat, lst in PADROES.items()
}

LIMITE_LEITURA = 2_000_000  # 2 MB
LINHA_LONGA = 500           # possivel minificacao
MAX_HITS_POR_ROTULO = 12


def eh_binario(caminho, ext):
    if ext in EXT_BINARIAS:
        return True
    try:
        with open(caminho, "rb") as f:
            return b"\x00" in f.read(4096)
    except OSError:
        return True


def varrer(raiz, tudo=False):
    arquivos = []
    achados = []
    notas = []

    for pasta, subpastas, nomes in os.walk(raiz):
        if not tudo:
            subpastas[:] = [d for d in subpastas if d not in PASTAS_IGNORADAS]
        else:
            subpastas[:] = [d for d in subpastas if d != ".git"]

        for nome in sorted(nomes):
            caminho = os.path.join(pasta, nome)
            rel = os.path.relpath(caminho, raiz)
            ext = os.path.splitext(nome)[1].lower()
            try:
                tamanho = os.path.getsize(caminho)
            except OSError:
                continue

            info = {"arquivo": rel, "bytes": tamanho, "tipo": "texto"}

            if ext in EXT_EXECUTAVEIS:
                notas.append(f"{rel}: script de shell, ler linha a linha")
            if nome.startswith(".") and ext not in {".env"}:
                notas.append(f"{rel}: arquivo oculto")

            if eh_binario(caminho, ext):
                info["tipo"] = "binario"
                notas.append(f"{rel}: binario, nao auditavel por leitura")
                arquivos.append(info)
                continue

            if tamanho > LIMITE_LEITURA:
                info["tipo"] = "grande"
                notas.append(f"{rel}: {tamanho // 1024} KB, lido apenas parcialmente")

            try:
                with open(caminho, "r", encoding="utf-8", errors="replace") as f:
                    conteudo = f.read(LIMITE_LEITURA)
            except OSError:
                continue

            linhas = conteudo.splitlines()
            info["linhas"] = len(linhas)
            longas = sum(1 for l in linhas if len(l) > LINHA_LONGA)
            if longas and len(linhas) < 50:
                info["tipo"] = "possivelmente minificado"
                notas.append(f"{rel}: linhas muito longas, possivel codigo minificado ou ofuscado")

            contagem = {}
            for i, linha in enumerate(linhas, 1):
                trecho = linha.strip()
                if not trecho:
                    continue
                for categoria, padroes in PADROES_COMPILADOS.items():
                    for rotulo, rx in padroes:
                        if rx.search(linha):
                            chave = (categoria, rotulo)
                            contagem[chave] = contagem.get(chave, 0) + 1
                            if contagem[chave] > MAX_HITS_POR_ROTULO:
                                continue
                            achados.append({
                                "categoria": categoria,
                                "rotulo": rotulo,
                                "arquivo": rel,
                                "linha": i,
                                "trecho": trecho[:180],
                            })
            arquivos.append(info)

    return arquivos, achados, notas


def imprimir(raiz, arquivos, achados, notas):
    print(f"# Varredura estatica: {raiz}")
    print("Nada foi executado. Apenas leitura.\n")
    print(f"Arquivos analisados: {len(arquivos)} | pontos de atencao: {len(achados)}\n")

    print("## Inventario")
    for a in arquivos:
        extra = f", {a['linhas']} linhas" if "linhas" in a else ""
        print(f"- {a['arquivo']}  ({a['bytes']} bytes{extra}, {a['tipo']})")
    print()

    if notas:
        print("## Observacoes de leitura")
        for n in sorted(set(notas)):
            print(f"- {n}")
        print()

    if not achados:
        print("## Pontos de atencao\nNenhum padrao conhecido encontrado. "
              "Isso nao substitui a leitura dos arquivos.")
        return

    print("## Pontos de atencao por categoria")
    for categoria in PADROES:
        do_grupo = [h for h in achados if h["categoria"] == categoria]
        if not do_grupo:
            continue
        print(f"\n### {categoria}  ({len(do_grupo)})")
        for h in do_grupo:
            print(f"- [{h['rotulo']}] {h['arquivo']}:{h['linha']}")
            print(f"      {h['trecho']}")

    print("\n---")
    print("Estes resultados sao pistas, nao veredito. Confirme cada um lendo o "
          "arquivo em volta da linha apontada antes de classificar o risco.")


def main():
    p = argparse.ArgumentParser(description="Varredura estatica somente leitura.")
    p.add_argument("pasta")
    p.add_argument("--tudo", action="store_true",
                   help="inclui node_modules, venv, dist e afins")
    p.add_argument("--json", action="store_true", help="saida estruturada")
    args = p.parse_args()

    raiz = os.path.abspath(args.pasta)
    if not os.path.isdir(raiz):
        print(f"Pasta nao encontrada: {raiz}", file=sys.stderr)
        sys.exit(1)

    arquivos, achados, notas = varrer(raiz, args.tudo)

    if args.json:
        print(json.dumps({
            "raiz": raiz,
            "arquivos": arquivos,
            "achados": achados,
            "notas": sorted(set(notas)),
        }, ensure_ascii=False, indent=2))
    else:
        imprimir(raiz, arquivos, achados, notas)


if __name__ == "__main__":
    main()
