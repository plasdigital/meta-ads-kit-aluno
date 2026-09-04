# Supabase — a memória das suas campanhas

A Meta guarda os seus números, mas ela é **fonte**, não **memória**. Consultar toda hora é lento,
gasta limite de chamada, e algumas quebras (por dia, por anúncio, período longo) demoram tanto que
a API responde de forma assíncrona.

Um banco resolve isso: você grava os números uma vez por dia e passa a ler do seu lado, instantâneo
e sem limite. O plano grátis do Supabase dá conta com folga.

## Você precisa disto?

| Situação | Precisa? |
|---|---|
| olhar como foi a semana, de vez em quando | **não** — `insights.py` resolve |
| receber o relatório diário no WhatsApp | **não** — o n8n lê e manda, sem guardar |
| comparar este mês com o passado, sempre | **sim** |
| montar um painel para você ou para o cliente | **sim** |
| deixar o cliente olhando sozinho, sem dar acesso à conta | **sim** |

Se você respondeu "não" nas duas primeiras e parou aí, pule este documento. Volte quando a pergunta
*"e no mês passado?"* começar a aparecer.

---

## O desenho, em três peças

```
n8n (2x por dia)  →  scripts/insights.py  →  grava no Supabase  →  a tela lê do Supabase
```

A regra que sustenta isso: **a tela nunca fala com a Meta.** Ela lê o espelho. Se a Meta estiver
lenta ou fora do ar, o painel continua abrindo — com o número da última sincronização, que é
honesto e suficiente.

## As tabelas mínimas

Três chegam:

| Tabela | O que guarda | Chave |
|---|---|---|
| `contas` | as contas que você acompanha | `act_` |
| `campanhas` | id, nome, objetivo, status | id da campanha |
| `metricas_dia` | **uma linha por objeto, por dia**: gasto, impressões, cliques, resultados | (id do objeto, dia) |

O detalhe que evita o retrabalho: **grave por dia, nunca só o acumulado.** Com a linha diária você
monta qualquer período depois; com o acumulado, você perde a série para sempre.

E use **upsert** na chave (objeto, dia), não insert: o dia de hoje muda várias vezes até fechar, e o
de ontem ainda pode ser corrigido pela Meta em até alguns dias. Sem upsert, você duplica.

---

## O que **não** guardar

- **O token.** Ele mora no `.env` e nas credenciais do n8n. Nunca numa tabela.
- **Dado pessoal de quem clicou.** A API não te dá isso, e é bom que não dê.
- **Lista de e-mail ou telefone de público personalizado.** Se você sobe base de cliente, ela vai
  para a Meta com hash e acabou — cópia no seu banco é responsabilidade (e risco) a mais.

## Ligue a segurança antes de pôr o primeiro número

Se a sua tela for pública ou tiver login, **ligue RLS (Row Level Security)** nas tabelas e crie uma
role que só enxerga o que aquele cliente pode ver. Banco de métrica de cliente com a chave de
serviço exposta no navegador é o vazamento mais comum de painel feito às pressas.

Para o n8n gravar, use a chave de serviço **do lado do servidor** (nas credenciais do n8n). Para a
tela ler, use a chave pública com RLS ligado.

---

## Um atalho honesto

Você não precisa de painel para ter memória. Um fluxo que grava a linha do dia e um relatório
semanal que compara com as quatro semanas anteriores já entregam 80% do valor — e não exigem que
você mantenha uma tela no ar.

Painel é bonito e vende bem para cliente. Mas ele só se paga se alguém abrir. Se ninguém abre, o
relatório que chega sozinho é melhor.
