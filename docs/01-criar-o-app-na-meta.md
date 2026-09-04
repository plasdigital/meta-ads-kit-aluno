# Criar o aplicativo na Meta (e ligar o Claude Code nele) — manual do zero

> **Objetivo:** sair de "não tenho nada" e chegar a um **aplicativo criado no Meta for Developers**,
> e **falando com a Graph API** (token + primeira chamada que responde).
> **Ferramentas:** `developers.facebook.com` · `business.facebook.com` · Graph API Explorer · os `scripts/` desta pasta
> **Entrada:** um e-mail e uma pessoa disposta a criar uma conta no Facebook
> **Saída:** App ID na mão, app aparecendo para a IA, e uma chamada à Graph API devolvendo JSON
>
> **Escrito em 01/set/2026**, com cada rótulo de tela conferido na documentação oficial no mesmo dia
> (fontes no §10). É o **pré-requisito comum** de WhatsApp Cloud API, Instagram API e Marketing API:
> os três rodam em cima de um app da Meta, e é sempre este documento que vem antes.

---

## 0. Como ler isto

Este documento é **referência, não resumo**. Ninguém lê tudo.

| Você quer | Vá para |
|---|---|
| descobrir se precisa mesmo fazer isso | §1 — fazer × contratar |
| saber o que precisa ter **antes** do primeiro clique | §2 — a corrente do zero |
| parar de confundir portfólio, app, WABA e Página | §3 — os nomes que colidem |
| **criar o app**, tela por tela | §4 |
| por que aqui não tem MCP | §5 |
| falar com a Graph API pela primeira vez | §6 |
| entender por que "funciona pra mim e não pro cliente" | §7 — modo e nível de acesso |
| o erro que você está vendo agora | §8 — catálogo |
| conferir que terminou | §9 — checklist e prova |

> 🔴 **A Meta muda estas telas.** Cada rótulo aqui foi conferido em **01/set/2026**. Antes de gravar
> ou de ensinar, reabra a fonte do §10 — e leia o §4.0, que explica por que quase todo tutorial em
> português que você vai achar no Google descreve uma tela que **não existe mais**.

---

## 1. A primeira bifurcação: você precisa mesmo de um app seu?

Antes da técnica vem a pergunta de posse: **de quem é o aplicativo?**

| | **O app é da ferramenta que você contrata** | **O app é seu** |
|---|---|---|
| Como se faz | contrata, faz login, clica em *conectar* | este manual |
| Quem aparece para a Meta | a ferramenta | você |
| Exemplos | ManyChat, Wati, 360dialog, Twilio, Take Blip | Chatwoot na sua VPS, n8n, código próprio |
| Preço da mensagem | o da Meta **+ a margem deles** | o da Meta |
| Acesso à API crua | só o que a ferramenta expõe | tudo |
| Trocar de ferramenta depois | dói | é trocar o token |
| Tempo até funcionar | um dia | 1 a 2 horas o app; dias se depender de verificação |

**A mesma ferramenta aparece dos dois lados.** O Chatwoot contratado na nuvem deles é app **deles**;
o mesmo Chatwoot instalado na sua VPS é app **seu**. Não é a marca que decide — é a posse.

> 🗣️ **A frase honesta:** *"Zero configuração não é zero burocracia. A ferramenta te poupa o app —
> que é a parte difícil —, mas conta no Facebook, portfólio e verificação do negócio você faz do
> mesmo jeito."*

**Quem termina este manual vira a coluna da esquerda para o próprio cliente.** É o caminho de quem
vende automação: o app é seu, o ativo é do cliente.

---

## 2. A corrente do zero: o que existe antes do primeiro clique

> Esta seção lista **até o passo óbvio, de propósito**. É mais barato pular uma linha do que
> descobrir no meio que faltava uma conta.

Legenda: *(óbvio)* = quase todo mundo já tem · 🧱 = onde a pessoa trava de verdade · ⏯️ = assunto
grande o bastante para ser outro vídeo.

| # | O que | O que é, para quem nunca viu | Obrigatório? | Se faltar | |
|---|---|---|---|---|---|
| 1 | **E-mail que você acessa** | recebe confirmação e alerta do app | **sempre** *(óbvio)* | não passa da primeira tela | |
| 2 | **Conta pessoal no Facebook** | o perfil comum, de pessoa física — a Meta amarra **tudo** a uma pessoa | **sempre** *(óbvio)* | não existe conta de desenvolvedor, nem portfólio, nem app | |
| 3 | **Conta de desenvolvedor** | o mesmo login do Facebook, aceito em `developers.facebook.com` | **sempre** | não abre o painel de apps | |
| 4 | **Portfólio comercial** (a "BM") | a empresa dentro da Meta, que guarda apps, contas e a fatura — **não é a Página do Facebook** | **não para criar o app** ⬇️ | o app nasce solto: sem ele não há WABA, nem usuário do sistema, nem token permanente | ⏯️ |
| 5 | **Verificação do negócio** | a Meta conferindo CNPJ, endereço e documentos do portfólio | **depende do que você vai fazer** ⬇️ | trava o **Acesso Avançado** (e portanto o App Review) e limita volume | ⏯️ |
| 6 | **Node.js 18+** ou `curl` | roda a chamada da API | só a partir do §6 | você cria o app e não consegue provar que funciona | |
| 7 | **Claude Code** (ou Codex / Antigravity) | quem conduz e diagnostica | opcional, mas é o ponto deste material | você faz tudo na mão, navegando seis telas por dúvida | |

```
1. e-mail ─────────────────┐
2. conta pessoal Facebook  │
3. conta de desenvolvedor  ├── existe antes do primeiro clique
4. portfólio comercial     │   (4 e 5 começam no dia 1, em paralelo — 5 demora dias)
5. verificação do negócio ─┘
        │
        └──► §4 — criar o app
```

### As três coisas que quase todo mundo entende errado aqui

**1. O portfólio não é obrigatório para criar o app — mas é para usá-lo de verdade.** A própria tela
de criação oferece *"I don't want to connect a business portfolio yet"*, e a documentação diz com
todas as letras: *"You can connect a business portfolio at any time during development."* Ou seja:
dá para criar hoje e conectar amanhã. **O que não dá é ir longe sem ele** — o token permanente nasce
de um *usuário do sistema*, que mora dentro do portfólio. Conectar depois é possível; começar sem
saber disso é o que faz a pessoa refazer.

**2. Verificação do negócio não é obrigatória sempre.** É o engano mais comum, e ele erra nas duas
direções. Você cria o app, testa a API e envia mensagem **sem** verificação. O que ela destrava é o
**Acesso Avançado** — desde 01/fev/2023 a Meta exige negócio verificado para conceder Advanced
Access — e, no WhatsApp, o teto de 250 conversas iniciadas por dia. **Comece no primeiro dia e siga
sem esperar:** ela leva dias e não bloqueia o resto.

**3. Página do Facebook não entra nesta lista.** Não é pré-requisito de app nenhum. Confundir
*portfólio comercial* com *Página* é o erro clássico — são coisas diferentes, com telas diferentes.

---

## 3. Os nomes que colidem — separe antes de usar

Metade dos travamentos é confusão de nome. Estes pares se parecem e **não são a mesma coisa**:

| Isto | ...não é isto |
|---|---|
| **Portfólio comercial** (*business portfolio*, ex-*Business Manager*, "a BM") — a empresa dentro da Meta | **Página do Facebook** — o perfil público da empresa |
| **App** — a integração: permissões, domínios, webhooks | **Caso de uso / produto** — o que o app faz (WhatsApp, Instagram, Ads) |
| **Verificação do negócio** — a Meta conferindo o seu CNPJ | **App Review** — a Meta analisando o que o seu app faz |
| **App Review** | **Publicar o app** (modo Live) — etapas diferentes, ver §7 |
| **Token de acesso** — a credencial que a Meta te dá | **Token de verificação do webhook** — uma senha que **você inventa** |
| **App ID** — número público do app | **App Secret** — a senha do app, nunca sai do servidor |
| **Acesso Padrão** (*Standard*) — só quem tem papel no app | **Acesso Avançado** (*Advanced*) — qualquer usuário |

E o contrário também vale: **um nome com vários apelidos** — *portfólio comercial*, *gerenciador de
negócios*, *Business Manager*, *BM* são **a mesma coisa**. Quem não sabe disso acha que está na tela
errada.

---

## 4. Criar o app, tela por tela

### 4.0 🔴 Antes: por que o tutorial que você achou no Google está errado

A Meta trocou o modelo de criação de app. **Não existe mais escolher "tipo do app: Negócios /
Consumidor / Jogos"** na criação. Hoje você escolhe **casos de uso** (*use cases*), e é o caso de uso
que traz junto as permissões e os produtos.

> Todo tutorial que manda *"clique em Criar App e escolha o tipo Negócios"* foi escrito antes dessa
> mudança. A tela não tem mais esse botão. Quem segue aquele texto trava na segunda etapa e acha que
> fez algo errado — não fez.

Isso vale inclusive para material **antigo da própria Meta**: há posts no blog deles, ainda no ar,
mandando escolher o tipo. **A página que vale é a `Create an App`** (§10).

### 4.1 O caminho

**Vá direto para `developers.facebook.com/apps/creation/`** — o assistente inteiro mora nessa URL.
(Se preferir navegar: *My Apps* → *Create App*; o botão fica no canto superior direito da lista.)

As cinco etapas do assistente, na ordem em que aparecem:

| # | Etapa | O que ela pede | Cuidado |
|---|---|---|---|
| 1 | **App details** | nome do app + e-mail de contato | o nome **não pode** conter "Facebook", "Instagram", "WhatsApp" nem "Meta"; use o nome da sua empresa |
| 2 | **Use cases** | um ou mais casos de uso | 🧱 **ver 4.2 — é aqui que se erra de forma irreversível** |
| 3 | **Business** | portfólio verificado, não verificado, criar um, ou *"I don't want to connect a business portfolio yet"* | dá para conectar depois, mas conecte agora se já tiver |
| 4 | **Requirements** | mostra o que aquele caso de uso vai exigir (ex.: App Review) | é **leitura**, não é formulário |
| 5 | **Overview** | revisão de tudo | dá para voltar clicando no nome de cada etapa, no topo |

Fecha em **Go to dashboard**.

**✅ Sinal de sucesso:** você cai no painel do app e existe um **App ID** (número longo) no topo.
Anote: é o que todo comando vai pedir daqui pra frente.

### 4.2 🧱 O erro irreversível: caso de uso não se remove

A frase está na documentação oficial, e é curta:

> *"Use cases cannot be removed after you create your app."*

Você pode **adicionar** casos de uso compatíveis depois, a qualquer momento. **Remover, não.** E os
incompatíveis aparecem em cinza — o assistente não deixa combinar o que não combina.

O que isso significa na prática:

- **Escolha pelo que você vai fazer, não pelo que talvez faça.** Sobra é permanente.
- Errou feio? O conserto é **criar outro app**. Custa refazer token, webhook e domínio — e, no
  WhatsApp, apagar um app pode deixar o número mudo. Não é o fim do mundo; é uma tarde perdida.
- Dá para criar um app **sem nenhum caso de uso**, só para ter um App ID. Ele nasce sem permissão,
  sem produto e sem funcionalidade — serve para experimento, não para trabalho.

**Os casos de uso que interessam** (o rótulo muda de tempos em tempos; procure pelo texto, não pela
posição na lista):

| Você quer | Caso de uso |
|---|---|
| WhatsApp Cloud API | **Connect with customers through WhatsApp** |
| Instagram (publicar, comentários, DM) | **Instagram** |
| Anúncios por API | **Marketing API** |
| Página do Facebook por API | **Manage everything on your Page** |
| Nada disso | **Other** — e siga o guia *Other App Types* |

> ⚠️ Alguns produtos entram **sozinhos** junto do caso de uso — a documentação cita *Facebook Login
> for Business* e *Webhooks*. Ver esses itens na barra lateral sem ter pedido não é erro.

### 4.3 O que o caso de uso já traz configurado

Escolher o caso de uso não é só um rótulo: ele **já adiciona as permissões obrigatórias**. No do
WhatsApp o app nasce com três, e elas **não podem ser removidas**:

`public_profile` · `whatsapp_business_management` · `whatsapp_business_messaging`

E deixa três opcionais à sua escolha: `business_management` (só se for ler o portfólio por API),
`email`, `whatsapp_business_manage_events` (só para Marketing Messages Lite + Conversions API).

> 🎯 **A regra que evita reprovação:** *peça só o que você usa.* A própria Meta escreve que
> permissão desnecessária **causa reprovação** no App Review. Isso pesa mais lá na frente (§7), mas
> a decisão começa aqui.

Depois de criado, o painel do caso de uso tem sempre o mesmo menu à esquerda — vale conhecer os
nomes, porque é para lá que qualquer instrução vai te mandar:

**Permissions and features** (o que o app pode pedir) · **Quickstart** · **API Setup** (gera token,
manda a primeira mensagem, configura webhook) · **Configuration** (webhooks) · **Resources**.

### 4.4 Conectar o portfólio depois (se você pulou a etapa 3)

No painel do app, procure **Business** / *Portfólio comercial* nas configurações e selecione o
portfólio. É o mesmo que a etapa 3 do assistente faria.

**Por que não deixar para depois:** o **token permanente** nasce de um *usuário do sistema* (§6.3),
que só existe dentro de um portfólio. Sem portfólio você fica preso ao token de teste, que **vence
em ~24 horas** — e aí a integração morre sozinha no dia seguinte, com um erro que parece outra coisa
(§8, erro 190).

---

## 5. Aqui não tem MCP — quem opera a conta são os scripts

Você vai achar tutorial mandando plugar um servidor MCP no agente para mexer em anúncio.
**Esta pasta não usa nenhum**, e é decisão de projeto:

| | script (o que tem aqui) | MCP |
|---|---|---|
| roda no n8n, no cron, às 3 da manhã | sim | não — só dentro de uma conversa aberta |
| você lê o código antes e confere o que rodou depois | sim | não |
| continua de pé se o servidor do outro sair do ar | sim | não |
| fala com a conta pelo SDK oficial da Meta | sim | — |

Tudo que você vai fazer com anúncio — criar campanha, planejar público, criar público
personalizado, subir anúncio, editar em massa, otimizar, medir, ver saldo e auditar mudança
— está em `scripts/`, chamando o SDK oficial `facebook-business`. O agente monta o comando;
você lê e confirma.

NUNCA instale MCP de terceiro para mexer em anúncio (`fb-ads-mcp-server` e parecidos): é
entregar o token que gasta o seu dinheiro para código de estranho — e os scripts daqui já
fazem o que eles prometem.

---

## 6. Falar com a Graph API pela primeira vez

O app existe e a IA enxerga. Falta a parte que **faz**.

### 6.1 O que é a Graph API, em uma frase

É a porta única de tudo na Meta: `https://graph.facebook.com/<versão>/<o que você quer>`, com um
**token** junto. WhatsApp, Instagram e Ads são endereços diferentes da mesma porta.

### 6.2 O token de teste (vale ~24 h)

No painel do app, dentro do seu caso de uso → **API Setup** → **Generate access token**.

⏳ **Ele vence em menos de um dia.** Serve para provar que funciona hoje. Não serve para produção —
e é por não saber disso que a integração de muita gente "para de funcionar sozinha".

### 6.3 O token permanente (usuário do sistema)

Este mora no **portfólio**, não no app:

1. **Business Settings** (`business.facebook.com`) → **System users** → **Add**.
2. Crie o usuário do sistema (papel **Admin** quando for operar tudo).
3. **Assign Assets** — atribua **o app** (*Manage app*, controle total) e, se for WhatsApp, também
   **a conta do WhatsApp** (*Manage WhatsApp Business Accounts*).
4. **Generate token**, marcando só as permissões que você usa. Para WhatsApp:
   `whatsapp_business_messaging` + `whatsapp_business_management` (+ `business_management` se for
   ler o portfólio por API).
5. Copie e guarde. **A Meta não mostra o token de novo.**

> 🔒 Token em `.env.local`, nunca no git, nunca colado em chat, nunca dentro de um nó do n8n — no
> n8n ele vira **credencial**. Quem tem o seu token fala com a Meta **como se fosse a sua empresa**.

### 6.4 A primeira chamada — a prova

A mais barata de todas, que serve para qualquer app: perguntar quem é o dono do token.

```bash
curl -s "https://graph.facebook.com/v23.0/me?access_token=$TOKEN"
```

Voltou um JSON com `id` (e `name`, dependendo da permissão)? **O token é válido e a API responde.**
É o menor pedaço que já prova que tudo está de pé.

Para ver o app em si, usando o token de app (`APP_ID|APP_SECRET`):

```bash
curl -s "https://graph.facebook.com/v23.0/<APP_ID>?fields=name,category,link&access_token=<APP_ID>|<APP_SECRET>"
```

> ⛔ **Nunca troque a versão da Graph API por conta própria** num projeto que já funciona. Versão
> nova renomeia campo e quebra tudo de uma vez. A versão fixada nos materiais da casa é `v23.0`;
> mudar é decisão consciente, não faxina.

### 6.5 As duas telas que resolvem 90% dos "não sei por que falhou"

- **Graph API Explorer** (`developers.facebook.com/tools/explorer`) — monta a chamada clicando,
  escolhe o app, marca permissões e mostra a resposta. É o melhor lugar para descobrir que o token
  não tem a permissão que você jurava que tinha.
- **Access Token Debugger** (`developers.facebook.com/tools/debug/accesstoken`) — cole qualquer
  token e ele diz de quem é, quando vence e quais escopos carrega.

---

## 7. Modo do app e nível de acesso — a origem do "funciona pra mim e não pro cliente"

Duas chaves diferentes controlam quem consegue usar o seu app. Confundi-las é o motivo #1 de "está
tudo certo na tela e não funciona".

### 7.1 Modo: Development × Live

| | **Development mode** | **Live mode** |
|---|---|---|
| Quem consegue usar | **só quem tem papel no app** (admin, dev, testador) | qualquer pessoa |
| Permissões | as que existem, para quem tem papel | **só as aprovadas no App Review** |
| Aparece em busca pública | não | sim |
| Quando usar | montar e testar | quando terminou e passou no review |

**Todo app novo nasce em Development.** A troca é um interruptor na barra de cima do painel.

> ⚠️ Dado criado em Development (post de teste, mensagem de teste) **fica visível para todo mundo**
> quando você vira para Live. Não guarde piada interna em post de teste.

### 7.2 Nível de acesso: Padrão × Avançado

| | **Standard Access** | **Advanced Access** |
|---|---|---|
| De quem você lê dados | seus, e de quem tem papel no app | **de qualquer pessoa ou empresa** |
| Como se consegue | automático | **App Review**, permissão por permissão |
| Exige negócio verificado | não | **sim** (desde 01/fev/2023) |

> 🧱 **É aqui que trava quem vende serviço.** Enquanto você testa com a sua própria conta, tudo
> funciona com Acesso Padrão. No dia em que o **cliente** entra, a mesma chamada devolve erro de
> permissão — e não há ajuste de código que resolva: falta App Review, que exige verificação do
> negócio, que leva dias. **Comece a verificação no dia 1.**
>
> ⚠️ A página *Access Levels* da Meta abre dizendo que é *"only applicable to apps created using an
> App Type"* — o modelo antigo. Para app criado por **caso de uso**, a chave equivalente aparece
> dentro de *Permissions and features* do próprio caso de uso. **Confira na tela do seu app**, não
> na memória.

E `grant_status: REJECTED` numa permissão que ninguém pediu **não é reprovação** — é o estado padrão
de permissão nunca analisada.

---

## 8. Catálogo de erros

| O que aparece | O que realmente é |
|---|---|
| Erro **190** — "token inválido", e funcionava ontem | o token de teste vale **~24 h**. Nada quebrou: gere o permanente (§6.3) |
| Erro **200** — "sem permissão" | falta o escopo no token, ou falta **Acesso Avançado** (§7.2) |
| Erro **100** — parâmetro inválido | quase sempre é ID no campo errado (no WhatsApp: `PHONE_NUMBER_ID` onde devia ir `WABA_ID`) |
| Erro **10** ou **#2655111** | falta Acesso Avançado → falta App Review |
| A tela manda escolher **"tipo do app: Negócios"** e o botão não existe | você está seguindo um tutorial anterior ao modelo de casos de uso (§4.0) |
| O caso de uso errado ficou no app e não sai | **não sai mesmo.** Casos de uso não são removíveis (§4.2) |
| Webhook verificado e nenhuma mensagem chega | verificar a URL **não é** assinar o campo. Falta assinar (`messages`, por exemplo) |
| Funciona na sua conta e falha na do cliente | modo ou nível de acesso (§7) — não é o código |
| `grant_status: REJECTED` numa permissão que ninguém pediu | estado padrão de permissão nunca analisada. Não é reprovação |

---

## 9. Checklist e a prova

- [ ] Conta pessoal no Facebook e conta de desenvolvedor aceitas
- [ ] Portfólio comercial criado *(ou decisão consciente de conectar depois)*
- [ ] **Verificação do negócio iniciada** — mesmo que você não precise dela hoje
- [ ] App criado, com **App ID anotado**
- [ ] Caso de uso escolhido **com consciência de que não sai depois**
- [ ] Portfólio conectado ao app
- [ ] Usuário do sistema criado e **token permanente** guardado no `.env.local`
- [ ] 🎯 **A prova:** `GET /v23.0/me` devolve JSON com `id`

> **Termine na prova.** Um app criado que nunca respondeu a uma chamada não é um app funcionando — é
> uma tela bonita. A chamada do §6.4 custa 5 segundos e é a diferença entre "acho que deu certo" e
> "está de pé".

---

## 10. Fontes — e a data em que cada uma foi lida

Tudo conferido em **01/set/2026**, na documentação oficial da Meta:

| Assunto | Onde |
|---|---|
| As 5 etapas da criação, e *"use cases cannot be removed"* | `developers.facebook.com/docs/development/create-an-app/` |
| Caso de uso do WhatsApp, permissões obrigatórias e o menu do painel | `.../create-an-app/whatsapp-use-case` |
| Development × Live | `.../development/build-and-test/app-modes/` |
| Standard × Advanced Access, e a exigência de negócio verificado | `.../graph-api/overview/access-levels/` |
| Usuário do sistema e token permanente | `.../business-messaging/whatsapp/get-started` (passo 5) |

**O que envelhece mais rápido, em ordem:** rótulo de tela > lista de casos de uso > política de
review > preço. Antes de gravar qualquer aula com este material, reabra as duas primeiras linhas da
tabela.

---

## 11. Onde continuar

| Depois do app, você quer | Vá para |
|---|---|
| **começar a mexer nos anúncios** — é para isto que você criou o app | volte ao `COMECE-AQUI.md` desta pasta, passo 3 |
| a lista do que dá para automatizar em Ads | `docs/02-o-que-da-pra-automatizar.md` |
| o comando exato de cada operação | `docs/03-todas-as-operacoes.md` |
| **WhatsApp:** número, registro, template, App Review | [github.com/plasdigital/wa-kit-aluno](https://github.com/plasdigital/wa-kit-aluno) |
| **Instagram:** publicar, comentário, DM por API | [github.com/plasdigital/insta-kit-aluno](https://github.com/plasdigital/insta-kit-aluno) |
| só o aplicativo da Meta, sem os anúncios | [github.com/plasdigital/meta-kit-aluno](https://github.com/plasdigital/meta-kit-aluno) |
| a VPS que hospeda o n8n do passo 4 | [github.com/plasdigital/vps-kit-aluno](https://github.com/plasdigital/vps-kit-aluno) |
