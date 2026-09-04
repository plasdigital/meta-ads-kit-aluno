# Comece aqui — do zero até o primeiro relatório

Este é o único documento que você segue **na ordem**. Uns 40 minutos, e quase tudo é clique nas
telas da Meta — a parte de terminal são três comandos.

> **Atalho:** abra esta pasta no Claude Code e diga **"oi"**. Ele conduz tudo isto conversando, e
> este arquivo vira a sua conferência. Se preferir ler, siga daqui.

**A régua, para você saber onde pode parar:**

| Você quer | Vai até o passo |
|---|---|
| só **ler e medir** a conta | **3** |
| **criar e subir** anúncio | **5** |
| coisa rodando **sozinha** (relatório diário, regra de otimização) | **6** |
| **histórico** de métrica guardado | **7** |

Passos 6 e 7 são opcionais para sempre. Muita gente vive bem parando no 5.

---

## Passo 1 — Python e a pasta

```bash
python3 --version                      # precisa ser 3.8 ou mais novo
pip3 install -r requirements.txt       # instala o SDK oficial da Meta
```

Não tem Python? [python.org/downloads](https://www.python.org/downloads/) — no Windows, marque
**"Add Python to PATH"** na primeira tela do instalador. É o erro nº 1 de quem começa.

Agora abra a pasta no seu agente:

```bash
claude          # ou codex, ou o agente que você usa
```

Dentro dele, diga: *"oi"*. Ele lê o `CLAUDE.md` e assume a condução.

---

## Passo 2 — O aplicativo na Meta e o token

**É o passo mais longo, e ele acontece no navegador, não aqui.** Tudo que você automatiza na Meta —
anúncio, WhatsApp, Instagram — passa por um aplicativo criado no Meta for Developers.

👉 **O manual inteiro, tela por tela, está em [`docs/01-criar-o-app-na-meta.md`](docs/01-criar-o-app-na-meta.md).**
Não pule para lá agora: peça ao agente para te conduzir por ele. Ele avisa antes do passo que **não
tem desfazer**, e traduz o erro quando ele aparece.

O resumo do que vai acontecer:

| | |
|---|---|
| **1.** | criar (ou entrar em) uma conta no Meta for Developers com o seu Facebook pessoal |
| **2.** | criar o aplicativo escolhendo o caso de uso de **anúncios** — 🔴 essa escolha **não se remove depois** |
| **3.** | conectar o portfólio comercial (a "BM") onde mora a sua conta de anúncios |
| **4.** | gerar o token — o de teste vale ~24 h; o **permanente** sai do *usuário do sistema* dentro do portfólio |
| **5.** | conferir que o app está em modo **Live** se você for criar criativo |

As permissões que o token precisa carregar: **`ads_read`** (ler) e **`ads_management`** (criar e
editar).

Com o token na mão, crie o seu `.env`:

```bash
cp .env.exemplo .env
```

E preencha `META_ADS_TOKEN` e `META_APP_ID`. Confira:

```bash
python3 scripts/setup.py
```

Ele checa dependência, token e conexão — e diz em português o que faltou. **Não muda nada na sua
conta.**

---

## Passo 3 — O primeiro relatório (a prova de que funcionou)

```bash
python3 scripts/read.py accounts                                    # quais contas o token alcança
python3 scripts/insights.py account --id act_123 --date-preset last_7d
```

Trocando `act_123` pela sua conta, claro. Se voltou JSON com gasto e alcance, **acabou a parte
difícil** — daqui em diante é conversar.

Peça ao agente: *"me faz um resumo da última semana, por campanha"*. Compare com o Gerenciador de
Anúncios. Bateu? Confie. Não bateu? Peça para ele quebrar por campanha — o total da conta inclui
gasto que não está em campanha nenhuma.

---

## Passo 4 — Cadastrar suas contas

```bash
cp contas.yaml.exemplo contas.yaml
```

Preencha com as suas contas — ou melhor: peça ao agente *"me ajuda a preencher o contas.yaml"*, que
ele lista as contas disponíveis e faz as perguntas na ordem.

É este arquivo que faz você dizer **"sobe a campanha da loja tal"** em vez de decorar `act_`. Para
o anúncio aparecer no Instagram, o `instagram_id` precisa estar aqui.

> ⚠️ O `contas.yaml` **nunca** vai para o Git — ele é a sua carteira de clientes. O `.gitignore` já
> barra; deixe assim.

---

## Passo 5 — (recomendado) O MCP oficial da Meta

O MCP é um jeito de o seu agente enxergar o **painel** da Meta de dentro da conversa: configuração
do app, webhooks, pendências de App Review, limite de chamadas.

```bash
claude mcp add --transport http meta-devtools https://mcp.facebook.com/devtools --scope user
```

Depois, `/mcp` no Claude Code para autenticar. Existe também um MCP de anúncios em
`https://mcp.facebook.com/ads`.

**Por que isto não substitui os scripts** — e é bom que não substitua:

| | MCP | Scripts desta pasta |
|---|---|---|
| serve para | consultar o painel e diagnosticar, dentro do chat | **executar** na conta, com registro |
| roda sozinho, sem você? | não | sim — é o que o n8n chama no passo 6 |
| dá para auditar o que rodou? | difícil | é código: você lê antes e depois |

Ou seja: **MCP para enxergar, script para operar.**

---

## Passo 6 — (opcional) n8n, para o que roda sozinho

Até aqui, tudo acontece quando você pede. O n8n é o que faz acontecer **sem você pedir**: o
relatório que chega às 8h, a regra que avisa quando o custo por resultado estoura, a auditoria que
roda toda segunda.

👉 [`docs/04-n8n-o-que-roda-sozinho.md`](docs/04-n8n-o-que-roda-sozinho.md) — o que vale automatizar,
o que não vale, e como o n8n chama estes scripts.

Não tem n8n? [github.com/plasdigital/vps-kit-aluno](https://github.com/plasdigital/vps-kit-aluno)
instala um na sua VPS.

---

## Passo 7 — (opcional) Supabase, para guardar histórico

A Meta guarda os números, mas responde devagar e limita consulta. Se você quer **comparar hoje com
o mês passado**, montar painel ou deixar o cliente olhando sozinho, precisa de um espelho — e o
Supabase grátis dá conta.

👉 [`docs/05-supabase-a-memoria.md`](docs/05-supabase-a-memoria.md).

---

## Terminou? A conferência

- [ ] `python3 scripts/setup.py` passa em tudo
- [ ] `python3 scripts/read.py accounts` lista a sua conta
- [ ] `insights.py` traz número que bate com o Gerenciador
- [ ] o `.env` e o `contas.yaml` existem e **não** estão no Git (`git status` não pode citá-los)
- [ ] você leu [`docs/00-use-com-responsabilidade.md`](docs/00-use-com-responsabilidade.md)

Deu tudo certo? Pergunte ao agente: *"o que dá pra automatizar aqui?"* — e escolha a primeira.
