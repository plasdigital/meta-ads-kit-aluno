# meta-ads-kit-aluno — seus anúncios do Facebook e do Instagram, operados por IA

Esta é a pasta de tráfego pago que eu rodo de verdade, empacotada para você rodar na sua conta.
Não é demonstração: são os mesmos scripts que sobem campanha e puxam relatório todo dia, com os
meus segredos trocados por placeholders e os caminhos da minha máquina apagados.

Você não vai decorar comando nenhum. Abre o Claude Code (ou Codex, ou Antigravity) **aqui dentro** e
conversa em português — a pasta sabe se explicar para ele.

```bash
git clone https://github.com/plasdigital/meta-ads-kit-aluno.git
cd meta-ads-kit-aluno
claude
```

E aí, na conversa: **"oi"**. Ele começa a configuração com você.

## O que dá para fazer com isto

| | |
|---|---|
| 📊 **Medir** | "como foi a semana?" — gasto, alcance, custo por resultado, por campanha e por anúncio |
| 🧱 **Montar** | campanha, conjunto e público, do jeito certo, sem passar por 12 telas |
| 🚀 **Subir** | anúncio novo com a imagem, o texto e a UTM certa — em minutos, não em uma tarde |
| ✏️ **Editar em massa** | trocar UTM, orçamento ou posicionamento de dezenas de anúncios de uma vez |
| 🔍 **Auditar** | quem mexeu na conta, o quê e quando |
| ⏰ **Deixar rodando** | o relatório que chega sozinho todo dia, com o seu PC desligado |

A lista completa, com o que cada uma exige: [`docs/02-o-que-da-pra-automatizar.md`](docs/02-o-que-da-pra-automatizar.md).

## O que você precisa ter

| # | O quê | Obrigatório? |
|---|---|---|
| 1 | **Python 3** (`python3 --version`) | sempre |
| 2 | uma **conta de anúncios** da Meta com Página vinculada | sempre |
| 3 | um **aplicativo no Meta for Developers** com a Marketing API | sempre — o passo a passo está aqui dentro |
| 4 | um agente de IA de terminal (Claude Code, Codex, Antigravity) | é o ponto desta pasta |
| 5 | um **portfólio comercial** (a "BM") | **não** para começar — mas sim para o token que não vence |
| 6 | **n8n** (na sua VPS ou na nuvem) | só para o que roda sozinho: relatório diário, regra de otimização |
| 7 | **Supabase** (o plano grátis serve) | só para guardar histórico de métrica |

**Você não precisa de:** verificação do negócio aprovada, site no ar, nem experiência com API.
Para *ler* a conta, os itens 1 a 4 bastam.

## O que tem aqui dentro

| Arquivo | Para quem |
|---|---|
| `COMECE-AQUI.md` | **você**, se preferir ler na ordem em vez de conversar |
| `CLAUDE.md` | **o agente de IA** — é isto que faz a pasta se explicar sozinha |
| `AGENTS.md` | Codex, Cursor, Antigravity |
| `scripts/` | os 9 scripts Python: 54 operações na sua conta |
| `docs/` | o porquê de tudo: criar o app, o que automatizar, cada comando, n8n, Supabase |
| `aprendizados.md` | a memória do seu agente — as regras que ele aprende com você |
| `.env.exemplo` | o molde das credenciais. Copie para `.env` |
| `contas.yaml.exemplo` | o cadastro das suas contas. Copie para `contas.yaml` |

## A ordem de leitura

1. **[`docs/00-use-com-responsabilidade.md`](docs/00-use-com-responsabilidade.md)** — dois minutos,
   e são os mais importantes. É a sua conta com cartão cadastrado do outro lado.
2. **[`COMECE-AQUI.md`](COMECE-AQUI.md)** — do zero até o primeiro relatório saindo.
3. **[`docs/02-o-que-da-pra-automatizar.md`](docs/02-o-que-da-pra-automatizar.md)** — o mapa do que
   dá para fazer, para você escolher por onde começar.
4. O resto você pergunta ao agente.

## Uma coisa dita agora, antes de você começar

**Comece lendo.** Passe os primeiros dias só puxando relatório e conferindo número contra o
Gerenciador. Automação em anúncio não é como automação em planilha: aqui o erro sai caro, e sai
rápido. Quando o relatório já for rotina, aí sim deixe a IA criar campanha — sempre pausada, sempre
revisada por você antes de ativar.

Os scripts nascem com essa trava: **tudo que é criado nasce PAUSED**. Ativar é sempre uma decisão
sua, dita no chat.

## Depois daqui

| Você quer | Vá para |
|---|---|
| só o aplicativo da Meta, do zero, sem anúncios | [github.com/plasdigital/meta-kit-aluno](https://github.com/plasdigital/meta-kit-aluno) |
| WhatsApp: número, template, App Review | [github.com/plasdigital/wa-kit-aluno](https://github.com/plasdigital/wa-kit-aluno) |
| Instagram: publicar, comentário, DM por API | [github.com/plasdigital/insta-kit-aluno](https://github.com/plasdigital/insta-kit-aluno) |
| a VPS que hospeda o n8n | [github.com/plasdigital/vps-kit-aluno](https://github.com/plasdigital/vps-kit-aluno) |

---

⏳ **Rótulo de tela envelhece.** Este material foi conferido na documentação oficial da Meta em
**04/set/2026**. Se a tela que você está vendo não bate com o que está escrito aqui, **acredite na
tela** e peça ao seu agente para conferir a documentação de hoje — ele sabe fazer isso, está
instruído a isso.
