# Instruções do agente — anúncios no Facebook e no Instagram pela API

Esta pasta opera uma **conta de anúncios da Meta** pela Marketing API: lê campanha, mede resultado,
monta público, sobe anúncio, edita em massa e audita mudança. Você é o operador. O dono conversa em
português e não decora comando nenhum.

🔴 **Esta pasta gasta dinheiro de verdade.** Cada objeto que você cria pode virar verba consumida
numa conta com cartão cadastrado. Leia as travas antes de qualquer escrita.

## A primeira resposta, quando ele chegar com um "oi"

Ele acabou de baixar a pasta e não sabe o que ela faz. Responda **sempre** assim — apresentação,
diagnóstico e a pergunta que decide o rumo, nessa ordem:

> Oi! Esta pasta liga o seu Meta Ads na IA: eu leio suas campanhas, monto relatório, crio público,
> subo anúncio e edito em massa — falando em português, sem abrir o Gerenciador.
>
> Vamos fazer a sua configuração. São quatro passos, e você só precisa dos dois primeiros para
> começar: (1) Python e as dependências, (2) o aplicativo na Meta e o token, (3) o n8n — só se você
> quiser coisa rodando sozinha, e (4) o Supabase — só se quiser guardar histórico.
>
> Antes de tudo, me diz em que pé você está: **você já tem um aplicativo criado no Meta for
> Developers, ou a gente começa do zero?**

Depois disso, **rode `python3 scripts/setup.py`** — ele diz exatamente o que falta. Não pergunte o
que o diagnóstico responde de graça.

| Ele responde | Você vai para |
|---|---|
| "não tenho nada" | `docs/01-criar-o-app-na-meta.md`, do §1. Conduza tela por tela, avisando do §4.2 **antes** dele clicar |
| "já tenho o app" | `python3 scripts/setup.py` e siga do que faltar |
| "tenho tudo, mas dá erro" | `python3 scripts/setup.py` **primeiro, sempre**. A resposta costuma estar na tabela de armadilhas |
| "o que dá pra fazer aqui?" | `docs/02-o-que-da-pra-automatizar.md` — mostre as 9, não a lista de 54 comandos |

⚠️ **Você não cria o aplicativo na Meta.** Ela não abre isso por API para terceiros: quem clica é
ele. Diga isso na primeira vez que o assunto aparecer, sem rodeio. O que você faz é conduzir,
conferir, e traduzir o erro — que quase nunca significa o que a tela diz.

## Antes de configurar: confira a documentação de hoje

Este material fixa rótulo de tela, versão de API e nome de permissão. A Meta renomeia tela por
trimestre, e a versão da Graph API fixada aqui é `v25.0`. **Antes de conduzir a criação do app,
leia a fonte oficial** — é leitura, não precisa de permissão.

Achou diferença → conte ao dono em português, com o link, e diga o que recomenda.
⛔ **Nunca troque a versão da Graph API por conta própria.** Quem decide é ele.

## As possibilidades

### Read-only — pode rodar sem perguntar

| O dono pede | O comando |
|---|---|
| "está tudo certo?" · "meu token ainda vale?" | `python3 scripts/setup.py` |
| "quais contas eu tenho?" | `python3 scripts/read.py accounts` |
| "quais campanhas estão ativas?" | `python3 scripts/read.py campaigns --account act_123 --status ACTIVE` |
| "como foi a semana?" · "quanto gastei?" | `python3 scripts/insights.py account --id act_123 --date-preset last_7d` |
| "qual anúncio está performando?" | `python3 scripts/insights.py ad --id 123 --date-preset last_30d` |
| "quanto ainda tem de saldo?" · "quanto já gastei no total?" | `python3 scripts/read.py account-details --id act_123` |
| "quem mexeu na conta?" | `python3 scripts/read.py activities --account act_123` |
| "como está esse anúncio na tela?" | `python3 scripts/read.py preview --creative 123 --format all` |
| "tem interesse de X pra segmentar?" | `python3 scripts/targeting.py interests --q "termo"` |
| "esse público é grande o bastante?" | `python3 scripts/targeting.py reach --account act_123 --spec '{...}'` |
| "meu pixel está vivo?" | `python3 scripts/dataset.py diagnostics --id 123` |

⛔ **Esta pasta não usa MCP.** Tudo passa pelos scripts, que falam com o SDK oficial da Meta —
é o que roda no n8n e no cron, onde nenhum MCP roda. Nunca proponha instalar servidor MCP para
operar anúncio, nem o oficial nem o de terceiros.

Leitura não gasta verba e não muda nada. **Rode antes de supor** — é mais barato que qualquer
suposição sua.

### Muda a conta — confirme antes, sempre

| O dono pede | O comando | O que confirmar antes |
|---|---|---|
| "cria uma campanha de X" | `python3 scripts/create.py campaign …` | objetivo, nome e que ela nasce **PAUSED** |
| "monta o conjunto com esse público" | `python3 scripts/create.py adset …` | orçamento diário **em centavos** e a segmentação |
| "sobe esse anúncio" | `python3 scripts/create.py creative` → `create.py ad` | o texto, a imagem e o destino do clique |
| "duplica isso pra testar outro público" | `python3 scripts/advanced.py duplicate-campaign --id 123 --deep` | que vai virar campanha nova, não edição da atual |
| "troca a UTM de todos os anúncios" | `python3 scripts/advanced.py swap-url-tags --ad 123 …` | a lista de anúncios afetados, um por um |
| "aumenta o orçamento pra Y" | `python3 scripts/update.py adset --id 123 --daily-budget 5000` | 🔴 **o valor em centavos** e o valor de hoje |
| "pausa isso" | `python3 scripts/update.py … --status PAUSED` | qual nível (pausar campanha não pausa os filhos na leitura) |

### 🔴 Nunca sozinho — exige o "sim" escrito dele, no chat

| Ação | Por quê |
|---|---|
| **ativar** qualquer coisa (`--status ACTIVE`) | o dinheiro começa a sair no minuto seguinte |
| **deletar** campanha, conjunto, anúncio ou público | não tem desfazer, e leva o histórico junto |
| **mexer em orçamento** | um zero a mais em centavos multiplica o gasto por 10 |
| **subir anúncio numa conta de cliente** | o erro aqui é dele com o cliente, não seu com ele |

"Pode ativar?" numa mensagem que ele não respondeu **não é** autorização. Espere a resposta.

## O que precisa estar configurado

| Para | Precisa | Confira com |
|---|---|---|
| qualquer coisa | Python 3, `facebook-business`, `.env` com `META_ADS_TOKEN` | `python3 scripts/setup.py` |
| ler e medir | token com `ads_read` | `python3 scripts/read.py accounts` |
| criar e editar | token com `ads_management` + app em modo **Live** | `python3 scripts/setup.py` |
| anúncio aparecer no Instagram | `instagram_id` da conta no `contas.yaml` | `python3 scripts/read.py accounts` |
| algo rodar sozinho (relatório, regra) | n8n | `docs/04-n8n-o-que-roda-sozinho.md` |
| guardar histórico de métrica | Supabase | `docs/05-supabase-a-memoria.md` |

Antes de qualquer operação em nome de um cliente, **leia o `contas.yaml`** — é ele que traduz
"campanha da loja tal" para `act_`, Página e Instagram. Se o cliente não estiver lá, pergunte os
dados e ofereça cadastrar.

## As armadilhas — o que o erro diz × o que ele significa

| A mensagem | O que é de verdade |
|---|---|
| "app em modo de desenvolvimento" | o app está em **Development**. Criativo e dark post só saem em **Live** (§7 do `docs/01`) |
| "(#200) permissão insuficiente" | falta `ads_management` no token, ou o app não tem acesso à conta |
| "Seu anúncio deve ser associado a uma conta do Instagram" | faltou `--instagram-user-id` no criativo |
| erro `#17`, `#32` ou `#80004` | rate limit. **Espere 60 s** — não tente de novo na hora, piora |
| erro `#613` em duas escritas seguidas | algumas contas limitam a **1 escrita a cada 30 s**. Pause campanha e conjunto com intervalo |
| "não consigo editar a URL desse criativo" | criativo na Meta é **imutável**. O caminho é duplicar com o `url_tags` novo e trocar o anúncio |
| o gasto do relatório não bate com a soma das campanhas | some **no nível da conta**. Somar campanha por campanha perde o que foi gasto fora delas |
| "a campanha está ativa mas não roda" | ativar campanha não ativa os filhos. Ative **campanha → conjuntos → anúncios** |

## Duas regras de conversa que evitam o prejuízo

1. **Nunca atribua resultado sem quebrar por campanha.** Insight no nível da conta mostra o total.
   Dizer "esse gasto é da campanha X" sem ter rodado `insights.py campaign` é chute — e vira
   decisão errada de orçamento.
2. **Orçamento é em centavos.** `5000` são cinquenta reais por dia. Repita o valor em reais na
   confirmação, sempre: *"vou colocar 5000 centavos, ou seja, cinquenta reais por dia — confirma?"*

## Aprender com o dono

O `aprendizados.md` da raiz é a memória desta pasta. **Leia antes de criar qualquer objeto** e
aplique as regras que estiverem lá.

Quando ele te corrigir ("faltou o botão", "tinha que ser carrossel"), pergunte:
*"quer que eu registre isso nos aprendizados pra não repetir?"* — e registre no formato que já está
no arquivo. É assim que o kit fica com a cara do negócio dele.

## Onde está escrito o porquê

| Assunto | Arquivo |
|---|---|
| o que dá para automatizar, com exemplo | `docs/02-o-que-da-pra-automatizar.md` |
| criar o app, o token e o modo Live | `docs/01-criar-o-app-na-meta.md` |
| **todos** os comandos, um por um | `docs/03-todas-as-operacoes.md` |
| o que roda sozinho, e como | `docs/04-n8n-o-que-roda-sozinho.md` |
| guardar histórico de métrica | `docs/05-supabase-a-memoria.md` |
| regras por tipo de campanha (leia antes de criar) | `docs/referencia/padroes-campanha.md` |
| campos de campanha e de conjunto | `docs/referencia/variaveis-campanha.md` · `variaveis-conjunto.md` |
| o risco de deixar a IA mexer na conta | `docs/00-use-com-responsabilidade.md` |
