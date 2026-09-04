# Parâmetros e Variáveis de Campanha

Esta referência detalha os parâmetros aceitos para criação e edição de campanhas no Meta Ads via API/SDK.

---

## 1. Parâmetros da Requisição

| Parâmetro | Tipo | Valores Válidos | Descrição |
|---|---|---|---|
| `name` | `string` | Livre (permite emojis) | Nome da campanha. |
| `status` | `enum` | `ACTIVE`, `PAUSED` | Status de veiculação inicial. Campanhas pausadas mostram status efetivo como `CAMPAIGN_PAUSED` para seus conjuntos e anúncios. |
| `special_ad_categories` | `array<enum>` | `NONE`, `EMPLOYMENT`, `HOUSING`, `CREDIT`, `ISSUES_ELECTIONS_POLITICS`, `ONLINE_GAMBLING_AND_GAMING`, `FINANCIAL_PRODUCTS_SERVICES` | **Obrigatório**. Se não houver categoria especial, preencher com `["NONE"]`. |
| `buying_type` | `enum` | `AUCTION` (padrão), `RESERVED` | Tipo de compra. `AUCTION` para Leilão e `RESERVED` para Alcance e Frequência. |
| `objective` | `enum` | *(Ver tabela abaixo)* | Objetivo principal de marketing da campanha. |
| `is_adset_budget_sharing_enabled` | `boolean` | `true`, `false` | Se `true`, ativa o Orçamento de Campanha Advantage (CBO) compartilhando a verba entre os conjuntos. |
| `daily_budget` | `integer` | Valor em centavos (ex: `2500` = R$ 25,00) | Orçamento diário da campanha (aplicável se CBO estiver ativo). |
| `lifetime_budget` | `integer` | Valor em centavos | Orçamento vitalício (aplicável se CBO estiver ativo). Exige `end_time` no conjunto de anúncios. |
| `bid_strategy` | `enum` | `LOWEST_COST_WITHOUT_CAP`, `LOWEST_COST_WITH_BID_CAP`, `COST_CAP`, `LOWEST_COST_WITH_MIN_ROAS` | Estratégia de lances da campanha. |

---

## 2. Objetivos de Campanha (`objective`)

O objetivo determina quais otimizações e metas estarão disponíveis nos níveis abaixo (conjuntos e anúncios).

* **`OUTCOME_TRAFFIC`**: Direcionar tráfego para sites, landing pages, aplicativos ou visitas ao perfil do Instagram.
* **`OUTCOME_LEADS`**: Capturar leads por meio de formulários nativos ou páginas externas.
* **`OUTCOME_SALES`**: Otimizar para conversões e ações de compra no site.
* **`OUTCOME_AWARENESS`**: Maximizar alcance, reconhecimento de marca e visualizações.
* **`OUTCOME_ENGAGEMENT`**: Focado em interações, mensagens (WhatsApp, Direct, Messenger) e engajamento com posts.
* **`OUTCOME_APP_PROMOTION`**: Focado em downloads e engajamento dentro de aplicativos.
