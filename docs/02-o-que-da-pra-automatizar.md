# O que dá para automatizar em anúncios

Gestão de tráfego é um trabalho de três tempos: **montar**, **publicar e ajustar**, **medir e
conferir**. Nos três, boa parte do que consome o seu dia é clique repetido — e é exatamente isso que
a API faz melhor do que você.

Esta página é o mapa. Cada bloco diz **o que a automação faz**, **o comando** e **o que ela exige**.

> Nenhuma delas exige que você saiba programar. O que aparece aqui como comando é o que o seu
> agente vai montar sozinho quando você pedir em português.

---

## 🧱 Montar

### 1. Criação de campanha

Você descreve o objetivo e o agente monta a estrutura inteira — campanha, conjunto e anúncio — já
com as regras que evitam os erros clássicos (criativo sem botão, carrossel que quebra em certos
posicionamentos, anúncio que não sai no Instagram).

```
scripts/create.py campaign --account act_123 --name "LEADS-Teste" --objective OUTCOME_LEADS
scripts/create.py adset    --account act_123 --campaign 123 --daily-budget 5000 --targeting '{...}'
scripts/create.py ad       --account act_123 --adset 123 --creative '{"creative_id":"456"}'
```

**Exige:** token com `ads_management` · app em modo Live.
**Nasce sempre pausada** — quem ativa é você.

### 2. Planejamento de público

Antes de gastar, dá para perguntar à Meta quanta gente existe do outro lado. O agente busca
interesse e comportamento pelo nome, monta a segmentação e mede o alcance **antes** de a campanha
existir.

```
scripts/targeting.py interests --q "musculação"
scripts/targeting.py reach     --account act_123 --spec '{...}'
scripts/targeting.py delivery  --account act_123 --spec '{...}' --daily-budget 5000
```

**Exige:** só leitura. É o melhor lugar para começar a experimentar — não muda nada.

### 3. Criação de públicos personalizados

Lista de clientes vira público. Público bom vira semelhante (*lookalike*). O que na tela são vinte
cliques por público vira uma frase.

```
scripts/create.py custom-audience --account act_123 --name "Compradores-2026"
scripts/create.py lookalike       --account act_123 --name "LAL-Compradores" --source 123 --spec '{"country":"BR","ratio":0.01}'
```

**Exige:** `ads_management`. ⚠️ Dado de cliente na lista: você é o responsável pela base que sobe.

---

## 🚀 Publicar e ajustar

### 4. Subir anúncios

Imagem ou vídeo, texto, botão, link com UTM certa, conta do Instagram vinculada. É a etapa com mais
detalhe fácil de esquecer — e é justamente por isso que ela ganha tanto com automação.

```
scripts/create.py image    --account act_123 --url "https://exemplo.com/imagem.jpg"
scripts/create.py creative --account act_123 --instagram-user-id 123 --url-tags "utm_source=facebook&utm_medium=cpc"
scripts/create.py ad       --account act_123 --adset 123 --creative '{"creative_id":"456"}'
```

**Exige:** `ads_management` · app em modo Live · Página vinculada ao app.

### 5. Edições em massa

Trocar a UTM de trinta anúncios. Ajustar orçamento de um conjunto inteiro. Pausar tudo que tem
custo por resultado acima do limite. Na tela é uma tarde; aqui é um comando por item, em sequência.

```
scripts/advanced.py swap-url-tags --ad 123 --url-tags "utm_campaign=promo"
scripts/update.py   adset --id 123 --daily-budget 5000
scripts/update.py   ad    --id 123 --status PAUSED
```

**Exige:** `ads_management`.
⚠️ **Criativo na Meta é imutável.** Não dá para editar a URL de um criativo existente — o caminho
é duplicar com o valor certo e trocar no anúncio. O `swap-url-tags` faz exatamente isso.

### 6. Otimização de campanhas

Aqui a IA deixa de ser braço e vira olho: ela lê o desempenho, compara com o que você definiu como
aceitável e propõe o corte — pausar o anúncio caro, mover orçamento para o que converte, duplicar o
vencedor com outro público.

```
scripts/insights.py adset --id 123 --date-preset last_7d
scripts/advanced.py duplicate-campaign --id 123 --deep
```

**Exige:** `ads_management` para executar.
🔴 **A decisão continua sua.** O agente propõe e explica; ativar e mexer em orçamento pede o seu sim.

---

## 📊 Medir e conferir

### 7. Alerta de saldo

Conta de anúncio que fica sem saldo para de entregar no meio do dia, e você só descobre quando o
resultado some. O saldo, o total gasto e o limite de gasto saem numa chamada de leitura — é a
automação mais barata desta lista e a que mais evita prejuízo.

```
scripts/read.py account-details --id act_123
```

Vem `balance` (o que resta em conta pré-paga), `amount_spent` (o acumulado) e `account_status`
(se a conta foi desativada). Ligado no n8n, vira o aviso que chega antes de a entrega parar: *"o saldo caiu abaixo do
limite que você definiu"*.

**Exige:** só leitura.
⚠️ Cartão de crédito no lugar de saldo pré-pago não mostra `balance` — nesse caso o que vale
acompanhar é o `spend_cap` e o gasto do dia.

### 8. Análise de campanhas e envio de relatórios

A pergunta "como foi a semana?" respondida em segundos, no nível que você quiser — conta, campanha,
conjunto ou anúncio —, quebrada por idade, gênero, região ou posicionamento.

```
scripts/insights.py account  --id act_123 --date-preset last_7d
scripts/insights.py campaign --id 123 --date-preset last_30d --breakdowns age,gender
```

**Exige:** só `ads_read`. **É por aqui que se começa.**

#### O mesmo número, chegando sozinho

O mesmo número de cima, mas chegando sozinho: no seu e-mail, no seu WhatsApp ou no grupo do
cliente, todo dia no mesmo horário, com o seu computador desligado.

**Exige:** o n8n do [passo 5](../COMECE-AQUI.md) — é ele que tem o relógio.
👉 [`04-n8n-o-que-roda-sozinho.md`](04-n8n-o-que-roda-sozinho.md)

### 9. Auditoria de mudanças na conta

Quem mexeu, no quê e quando. Vale ouro em conta compartilhada com cliente ou com outro gestor — e
é o primeiro lugar para olhar quando o resultado muda do nada.

```
scripts/read.py activities --account act_123
scripts/read.py activities-by-adset --adset 123
```

**Exige:** só leitura.

---

## Por onde começar, na prática

| Semana | O que fazer |
|---|---|
| **1** | só os itens 7, 8 e 9 — saldo, métrica e auditoria. Leitura pura, zero risco |
| **2** | item 2 (planejar público) e item 5 em uma edição pequena, com você olhando |
| **3** | itens 1 e 4: monte uma campanha inteira pausada e revise na tela antes de ativar |
| **4** | ponha o relatório (item 8) e o alerta de saldo (item 7) para chegarem sozinhos |

Automação em anúncio erra caro. A ordem acima existe para que, quando você deixar a IA criar
campanha, você já saiba **conferir** o que ela criou.

---

## O que a API **não** faz

Para você não perder tempo procurando:

- **Não cria o aplicativo na Meta** por você. Essa parte é clique seu (`01-criar-o-app-na-meta.md`).
- **Não escreve o criativo.** Ela sobe a imagem e o texto que você (ou a IA) produziu — a peça em si
  nasce fora daqui.
- **Não edita criativo publicado.** Duplica e substitui; ver o item 5.
- **Não cria público de engajamento nem de site.** Público de "quem viu 50% do vídeo", "quem
  interagiu com o Instagram" ou "quem visitou tal página" ainda sai na tela do Gerenciador — aqui
  os scripts criam o público de **lista de clientes** e o **semelhante** a partir de um existente.
- **Não baixa os leads do formulário instantâneo.** A campanha de Cadastros sobe daqui; os leads
  você busca no Gerenciador, no CRM integrado ou por um fluxo próprio.
- **Não sobe imagem nem vídeo do seu computador** — só por URL pública. Hospede o arquivo antes
  (o próprio Supabase do `docs/05` serve).
- **Não te livra das políticas da Meta.** Anúncio reprovado continua reprovado, e conta restringida
  por automação abusiva é problema seu. Leia [`00-use-com-responsabilidade.md`](00-use-com-responsabilidade.md).
