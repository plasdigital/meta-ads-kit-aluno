# n8n — o que roda sozinho

Tudo que esta pasta faz até aqui acontece **quando você pede**. Você abre o terminal, conversa com
o agente, ele executa e para. É o suficiente para a maior parte do trabalho.

O n8n resolve a outra metade: o que precisa acontecer **sem ninguém pedir**.

| | Agente no seu PC | n8n |
|---|---|---|
| quem dispara | você, conversando | o relógio, ou um evento |
| precisa do seu PC ligado? | sim | **não** |
| serve para | montar campanha, analisar, decidir | repetir a mesma coisa sempre igual |
| exemplo | "monta essa campanha pra mim" | "todo dia às 8h, me manda como foi ontem" |

Não é ou um ou outro: os dois usam os **mesmos scripts** desta pasta.

---

## As três que valem a pena

### 1. O relatório que chega sozinho

O caso mais óbvio e o que mais gente adota. Todo dia, no mesmo horário, você recebe: quanto gastou,
quantos resultados, custo por resultado, e o que mudou em relação ao dia anterior — no WhatsApp, no
e-mail ou no canal do time.

```
Agendamento (8h)
   → executa: python3 scripts/insights.py account --id act_123 --date-preset yesterday
   → um nó de IA escreve o texto em português a partir do JSON
   → envia
```

**A parte que quase todo mundo erra:** mandar o JSON cru. Ninguém lê. Passe por um nó de IA com a
instrução *"escreva em 5 linhas, em português, comparando com ontem, e destaque só o que mudou"*.

### 2. A regra de otimização que vigia

De hora em hora (ou uma vez por dia), o fluxo lê o desempenho e compara com o limite que você
definiu. Estourou? Ele te avisa.

```
Agendamento
   → scripts/insights.py adset --date-preset today
   → IF: custo por resultado acima do limite?
       → avisa você  (e só avisa)
```

🔴 **Não deixe o fluxo pausar campanha sozinho no começo.** Deixe ele avisar por duas ou três
semanas, e compare o que ele teria feito com o que você fez. Regra automática de pausa em conta de
cliente, sem esse período de observação, é como fica caro descobrir que a métrica do fim de semana é
diferente.

### 3. O espelho das métricas

Duas vezes por dia, o fluxo puxa os números e grava num banco. É o que permite comparar mês contra
mês e montar painel sem bater na API a cada abertura de tela.

👉 [`05-supabase-a-memoria.md`](05-supabase-a-memoria.md)

---

## Como o n8n chama estes scripts

Dois caminhos, e a escolha depende de onde o n8n está:

**a) O n8n roda na mesma máquina do kit** (VPS sua): use o nó **Execute Command**.

```
python3 /caminho/do/kit/scripts/insights.py account --id act_123 --date-preset yesterday
```

O script devolve JSON no stdout — o n8n segue com ele normalmente.

**b) O n8n está em outro lugar** (nuvem, outra máquina): use o nó **HTTP Request** direto na Graph
API, com o mesmo token do seu `.env`. Os scripts continuam servindo de referência: rode um deles
com o que você quer e copie a chamada que ele monta.

> ⚠️ Em qualquer um dos dois, o token vai para as **credenciais do n8n**, nunca escrito dentro do
> nó. Fluxo exportado com token dentro é como token vaza para um repositório.

---

## O que **não** vale automatizar assim

| Não | Por quê |
|---|---|
| criar campanha automaticamente | campanha nasce de uma decisão. Automatize o braço, não a cabeça |
| ativar anúncio por regra | ativação é a hora em que o dinheiro começa a sair. Deixe humana |
| relatório de hora em hora | ninguém lê, e você queima o limite de chamadas da API à toa |
| tudo num fluxo gigante | um fluxo por objetivo. Fluxo de 40 nós ninguém conserta seis meses depois |

---

## Rate limit — o detalhe que derruba fluxo em produção

A Meta limita chamadas, e **algumas contas limitam escrita a uma a cada 30 segundos**. Um fluxo que
pausa campanha e conjunto em sequência falha na segunda chamada com o erro `#613`.

Nos fluxos de escrita, ponha um **Wait** entre as operações. Nos de leitura, prefira uma chamada
que traz tudo (`--level ad`) a trinta chamadas em loop.

Erros `#17`, `#32` e `#80004` são limite estourado: espere 60 segundos antes de tentar de novo —
insistir na hora só piora.

---

Não tem n8n ainda? [github.com/plasdigital/vps-kit-aluno](https://github.com/plasdigital/vps-kit-aluno)
instala um na sua VPS, com HTTPS e backup.
