# Campanha de Conversão no Site (Website Conversion)

Este guia prático detalha as variáveis obrigatórias, a estrutura e as limitações específicas para criar campanhas focadas em **Conversão no Site** via API/SDK.

---

## 1. Estrutura da Campanha

Para conversões no site, o objetivo deve ser focado em cadastros (Leads) ou vendas (Sales).

* **`objective`**: Deve ser obrigatoriamente um dos seguintes:
  * `OUTCOME_SALES` (Vendas/Conversões gerais)
  * `OUTCOME_LEADS` (Conversões focadas em cadastros no site)

---

## 2. Estrutura do Conjunto de Anúncios (Ad Set)

O conjunto possui parametrizações estritas para garantir que o algoritmo otimize para eventos externos.

* **`destination_type`**: Deve ser obrigatoriamente **`WEBSITE`**.
* **`optimization_goal`**: Deve ser obrigatoriamente **`OFFSITE_CONVERSIONS`**.
* **`billing_event`**: Deve ser obrigatoriamente **`IMPRESSIONS`**.
* **`promoted_object`**: Deve conter o Pixel, o evento de conversão e a página de origem:
  ```json
  {
    "page_id": "ID_DA_PAGINA_DO_FACEBOOK",
    "pixel_id": "ID_DO_PIXEL_DE_CONVERSAO",
    "custom_event_type": "EVENTO"
  }
  ```
  * *Valores comuns para `custom_event_type`:* `PURCHASE`, `LEAD`, `ADD_TO_CART`, `INITIATE_CHECKOUT`, `COMPLETE_REGISTRATION`.

---

## 3. Estrutura de Criativos (`AdCreative`)

Os criativos possuem diferenças cruciais na especificação de links dependendo do formato de mídia.

### Variáveis Comuns:
* `name`: Nome identificador do criativo.
* `url_tags`: Parâmetro de tracking de URL (ex: `utm_source=facebook&utm_medium=cpc`).

---

### Tipo A: Imagem (`link_data`)
Na criação de criativos de imagem, a URL é definida tanto no corpo do `link_data` quanto no botão de chamada para ação.

```json
{
  "page_id": "PAGE_ID",
  "link_data": {
    "link": "LINK_DO_SEU_SITE",
    "image_hash": "HASH_DA_IMAGEM",
    "caption": "MÁSCARA_DO_LINK",
    "call_to_action": {
      "type": "LEARN_MORE",
      "value": {
        "link": "LINK_DO_SEU_SITE"
      }
    }
  }
}
```
* **`caption`**: Usado para definir a "máscara" visual do link exibida no anúncio (ex: `seusite.com`).

---

### Tipo B: Vídeo (`video_data`)
> [!IMPORTANT]
> Em criativos de vídeo, **não existe** o campo de link direto no corpo do `video_data`. O link de destino deve ser definido obrigatoriamente **apenas** dentro do objeto `call_to_action`.

```json
{
  "page_id": "PAGE_ID",
  "video_data": {
    "video_id": "VIDEO_ID",
    "message": "Texto da legenda do post",
    "call_to_action": {
      "type": "LEARN_MORE",
      "value": {
        "link": "LINK_DO_SEU_SITE"
      }
    }
  }
}
```

---

## 4. Opções de Segmentação e Público (Targeting)

A segmentação no conjunto de anúncios para conversão pode ser feita de duas formas principais, não havendo obrigatoriedade em usar o modelo automático:

### Opção A: Segmentação Personalizada (Recomendado para campanhas com públicos específicos)
Permite controle manual completo de localizações, idades, gênero, interesses, comportamentos e públicos personalizados ou semelhantes (Lookalike):
```json
{
  "geo_locations": {
    "countries": ["BR"]
  },
  "age_min": 25,
  "age_max": 54,
  "genders": [1], 
  "interests": [
    {"id": "6003139266461", "name": "Marketing Digital"}
  ]
}
```

### Opção B: Segmentação Advantage+ Audience (Modelo Sugerido/Padrão de Automação)
Delega ao Meta a inteligência de encontrar o público, usando as configurações enviadas como sugestões iniciais:
```json
{
  "geo_locations": {
    "countries": ["BR"]
  },
  "age_min": 18,
  "targeting_automation": {
    "advantage_audience": 1
  }
}
```

---

## 5. Notas de Otimização e Advantage+ Shopping Campaigns (ASC)

Em versões recentes da API (v25.0+), a Meta descontinuou o uso de flags específicas como `smart_promotion_type` para campanhas de compras automáticas (ASC). O comportamento de Advantage+ Shopping é acionado de forma nativa quando:
1. O objetivo é `OUTCOME_SALES`.
2. A segmentação é configurada no formato Advantage+ Audience (`"targeting_automation": {"advantage_audience": 1}`).
3. O orçamento está ativado no nível da campanha (CBO) com posicionamentos automáticos habilitados.

