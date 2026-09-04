# Parâmetros e Variáveis de Conjunto de Anúncios (Ad Set)

Esta referência detalha os parâmetros aceitos para criação e edição de conjuntos de anúncios (Ad Sets) no Meta Ads via API/SDK.

---

## 1. Parâmetros da Requisição

| Parâmetro | Tipo | Valores Válidos | Descrição |
|---|---|---|---|
| `campaign_id` | `string` | ID Válido | ID da campanha pai associada. |
| `name` | `string` | Livre | Nome do conjunto de anúncios. |
| `status` | `enum` | `ACTIVE`, `PAUSED` | Status de veiculação inicial. |
| `start_time` | `string` | ISO 8601 (`YYYY-MM-DDTHH:MM:SSZ`) | Data e hora de início da veiculação. |
| `end_time` | `string` | ISO 8601 (`YYYY-MM-DDTHH:MM:SSZ`) | Data e hora de término da veiculação. Obrigatório para orçamento vitalício. |
| `daily_budget` | `integer` | Valor em centavos (ex: `2500` = R$ 25,00) | Orçamento diário (caso CBO esteja desativado na campanha). |
| `lifetime_budget` | `integer` | Valor em centavos | Orçamento vitalício (caso CBO esteja desativado na campanha). |
| `bid_strategy` | `enum` | `LOWEST_COST_WITHOUT_CAP`, `COST_CAP`, `LOWEST_COST_WITH_BID_CAP`, `LOWEST_COST_WITH_MIN_ROAS` | Estratégia de lances a nível de conjunto. |
| `bid_amount` | `integer` | Valor em centavos | Lance máximo/alvo. Obrigatório com `COST_CAP` ou `LOWEST_COST_WITH_BID_CAP`. |
| `roas_average_floor` | `integer` | Ex: `150` (1.5x ROAS) | Retorno mínimo de ROAS. Usado com `LOWEST_COST_WITH_MIN_ROAS`. |
| `optimization_goal` | `enum` | *(Ver seção 2)* | Meta que o algoritmo otimizará. Limitado pelo objetivo da campanha. |
| `billing_event` | `enum` | *(Ver seção 3)* | Evento que gerará cobrança. Limitado por `optimization_goal`. |
| `destination_type` | `enum` | *(Ver seção 5)* | Tipo de destino do tráfego. |
| `promoted_object` | `JSON Object` | *(Ver seção 4)* | Conexão com ativos de dados (Pixel, Página, App ou Catálogo). |
| `targeting` | `JSON Object` | Estrutura de Targeting | Definição de segmentação e público (país, idade, gênero, etc.). |

---

## 2. Metas de Otimização (`optimization_goal`) por Objetivo

| Objetivo de Campanha (`objective`) | Metas de Otimização Permitidas (`optimization_goal`) |
|---|---|
| **`OUTCOME_TRAFFIC`** | `LINK_CLICKS`, `LANDING_PAGE_VIEWS`, `IMPRESSIONS`, `REACH` |
| **`OUTCOME_ENGAGEMENT`** | `POST_ENGAGEMENT`, `PAGE_LIKES`, `EVENT_RESPONSES`, `CONVERSATIONS`, `IMPRESSIONS`, `THRUPLAY` |
| **`OUTCOME_LEADS`** | `LEAD_GENERATION`, `OFFSITE_CONVERSIONS`, `LANDING_PAGE_VIEWS` |
| **`OUTCOME_SALES`** | `OFFSITE_CONVERSIONS`, `VALUE`, `LANDING_PAGE_VIEWS`, `LINK_CLICKS` |
| **`OUTCOME_APP_PROMOTION`** | `APP_INSTALLS`, `VALUE`, `ENGAGED_USERS` |

> [!NOTE]
> Enums gerais suportados pela API: `NONE`, `APP_INSTALLS`, `AD_RECALL_LIFT`, `ENGAGED_USERS`, `EVENT_RESPONSES`, `IMPRESSIONS`, `LEAD_GENERATION`, `QUALITY_LEAD`, `LINK_CLICKS`, `OFFSITE_CONVERSIONS`, `PAGE_LIKES`, `POST_ENGAGEMENT`, `QUALITY_CALL`, `REACH`, `LANDING_PAGE_VIEWS`, `VISIT_INSTAGRAM_PROFILE`, `VALUE`, `THRUPLAY`, `DERIVED_EVENTS`, `APP_INSTALLS_AND_OFFSITE_CONVERSIONS`, `CONVERSATIONS`, `IN_APP_VALUE`, `MESSAGING_PURCHASE_CONVERSION`, `SUBSCRIBERS`, `REMINDERS_SET`, `MEANINGFUL_CALL_ATTEMPT`, `PROFILE_VISIT`, `PROFILE_AND_PAGE_ENGAGEMENT`, `ADVERTISER_SILOED_VALUE`, `AUTOMATIC_OBJECTIVE`, `MESSAGING_APPOINTMENT_CONVERSION`.

---

## 3. Evento de Cobrança (`billing_event`) por `optimization_goal`

| Meta de Otimização (`optimization_goal`) | Evento de Cobrança (`billing_event`) |
|---|---|
| `CONVERSIONS`, `VALUE`, `LEAD_GENERATION`, `LANDING_PAGE_VIEWS`, `POST_ENGAGEMENT` | **`IMPRESSIONS`** (Padrão e obrigatório para a maioria) |
| `LINK_CLICKS` | **`LINK_CLICKS`** ou **`IMPRESSIONS`** |
| `THRUPLAY` | **`THRUPLAY`** ou **`IMPRESSIONS`** |
| `APP_INSTALLS` | **`APP_INSTALLS`** ou **`IMPRESSIONS`** |

---

## 4. Configuração do Objeto Promovido (`promoted_object`)

### Para Conversões (Pixel)
Obrigatório em campanhas como `OUTCOME_SALES` e `OUTCOME_LEADS` (quando usando site externo).
```json
{
  "pixel_id": "ID_DO_PIXEL",
  "custom_event_type": "EVENTO"
}
```
* **Eventos Padrão (`custom_event_type`):** `"PURCHASE"`, `"LEAD"`, `"ADD_TO_CART"`, `"INITIATE_CHECKOUT"`, `"COMPLETE_REGISTRATION"`.

### Para Engajamento (Páginas)
```json
{
  "page_id": "ID_DA_PAGINA"
}
```

---

## 5. Tipos de Destino (`destination_type`)

* **Conversas (`CONVERSATIONS`):**
  * `MESSENGER`, `WHATSAPP`, `INSTAGRAM_DIRECT`, `FACEBOOK`, `MESSAGING_MESSENGER_WHATSAPP`, `MESSAGING_INSTAGRAM_DIRECT_MESSENGER`, `MESSAGING_INSTAGRAM_DIRECT_MESSENGER_WHATSAPP`, `MESSAGING_INSTAGRAM_DIRECT_WHATSAPP`.
* **Conversões / Cliques no Link / LP Views:**
  * `WEBSITE`.
* **Geração de Leads Nativa (Formulários):**
  * `ON_AD`.
