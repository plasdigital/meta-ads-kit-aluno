# Meta Ads — Referência de API (Master)

Este é o índice de referências técnicas para criação, edição e configuração de campanhas, conjuntos de anúncios e criativos no Meta Ads via API/SDK.

## Módulos de Parâmetros e Variáveis

Consulte os arquivos específicos de cada nível para obter detalhes de campos, tipos, limitações e valores aceitos:

1. **[Campanhas (Campaigns)](variaveis-campanha.md)**
   * Definições de Objetivos de marketing (`objective`).
   * Estruturas de orçamento (`daily_budget`, `lifetime_budget`) e regras de CBO.
   * Estratégias de Lance e Categorias Especiais.

2. **[Conjuntos de Anúncios (Ad Sets)](variaveis-conjunto.md)**
   * Limitações de metas de otimização (`optimization_goal`) de acordo com o objetivo da campanha.
   * Vinculação de eventos de faturamento (`billing_event`).
   * Configuração de objetos de destino (`destination_type`) e objetos promovidos (`promoted_object`).

3. **[Padrões de Campanha por Objetivo](padroes-campanha.md)**
   * Regras de negócio e boas práticas por tipo de campanha.
   * **[Conversão no Site](campanha-conversao-site.md)**: Variáveis e regras de imagens, vídeos e Pixel.
   * **[Visitas ao Perfil do Instagram](padroes-campanha.md#visita-ao-perfil-instagram-instagram-profile-visit)**: Configuração de visitas.

---

## Estrutura Geral de Criativos (`/adcreatives`) e Anúncios (`/ads`)

Os criativos são imutáveis após a criação na API. Para atualizar parâmetros como `url_tags`, deve ser criado um clone atualizado que substitui o criativo no anúncio final.

### Modelos de `object_story_spec`

#### Imagem Simples
```json
{
  "page_id": "PAGE_ID",
  "instagram_user_id": "IG_USER_ID",
  "link_data": {
    "link": "https://seusite.com",
    "message": "Texto de legenda",
    "name": "Título do link",
    "description": "Descrição auxiliar",
    "image_hash": "HASH_DA_IMAGEM",
    "call_to_action": {"type": "LEARN_MORE"}
  }
}
```

#### Carrossel
```json
{
  "page_id": "PAGE_ID",
  "link_data": {
    "message": "Texto de legenda",
    "link": "https://seusite.com",
    "child_attachments": [
      {
        "link": "https://seusite.com/card1",
        "image_hash": "HASH1",
        "name": "Título Card 1",
        "call_to_action": {"type": "LEARN_MORE"}
      },
      {
        "link": "https://seusite.com/card2",
        "image_hash": "HASH2",
        "name": "Título Card 2"
      }
    ],
    "multi_share_end_card": false,
    "multi_share_optimized": false
  }
}
```

#### Vídeo
```json
{
  "page_id": "PAGE_ID",
  "video_data": {
    "video_id": "VIDEO_ID",
    "message": "Legenda do post",
    "title": "Título do Vídeo",
    "call_to_action": {"type": "LEARN_MORE", "value": {"link": "https://seusite.com"}}
  }
}
```

---

## Otimizações Automáticas (`degrees_of_freedom_spec`)
Para anúncios de carrossel ou mídias sequenciais, desative otimizações automáticas do Meta que distorcem o formato:

```json
{
  "creative_features_spec": {
    "carousel_to_video": {"enroll_status": "OPT_OUT"},
    "image_touchups": {"enroll_status": "OPT_OUT"},
    "standard_enhancements": {"enroll_status": "OPT_OUT"}
  }
}
```

---

## Links Úteis de Documentação Oficial

* [Meta Marketing API - Ad Campaign Group](https://developers.facebook.com/docs/marketing-api/reference/ad-campaign-group/)
* [Meta Marketing API - Campaign Copies (Duplicação)](https://developers.facebook.com/docs/marketing-api/reference/ad-campaign-group/copies/)
* [Meta Marketing API - Automated Rules](https://developers.facebook.com/docs/marketing-api/ad-rules/guides/trigger-based-rules/?locale=pt_BR)
* [Meta Marketing API - Bidding & Budgets](https://developers.facebook.com/docs/marketing-api/bidding/overview/budgets)
* [Meta Marketing API - Bid Strategies](https://developers.facebook.com/docs/marketing-api/bidding/overview/bid-strategy)

---

## 7. Mapeamento de Erros e Resolução de Problemas (Troubleshooting)

Este espaço serve para registrar falhas retornadas pela API do Meta Ads durante execuções reais, permitindo que a IA e o usuário atualizem as soluções de forma colaborativa.

### Diretrizes de Fluxo e Autoalimentação:
1. **Identificação do Erro:** Quando um script local ou requisição HTTP falhar, a mensagem exata de erro retornada pela API do Meta deve ser capturada.
2. **Pesquisa Autônoma:** Caso o erro ou parâmetro não conste nestes documentos de referência, a IA deve buscar soluções na internet ou documentação oficial da Meta antes de responder.
3. **Registro Obrigatório:** Assim que uma nova restrição, bug ou erro de validação for corrigido ou compreendido, ele deve ser documentado nesta seção com a causa raiz e a solução.

### Histórico de Erros Mapeados:

*(Novos erros identificados em execuções devem ser catalogados abaixo)*

| Código/Mensagem de Erro | Componente | Causa Provável | Ação Corretiva |
|---|---|---|---|
| *"Seu anúncio deve ser associado a uma conta do Instagram"* | Criativo / Ad | Ausência do parâmetro `instagram_user_id` para posicionamentos no Instagram. | Adicionar `--instagram-user-id` com o ID da conta do cliente no nível do criativo. |
| *Anúncio desconfigurado/quebrado em blocos de coleção* | Ad / Criativo | Otimização automática ativa (`degrees_of_freedom_spec`). | Enviar `degrees_of_freedom_spec` com `OPT_OUT` para `carousel_to_video`, `image_touchups` e `standard_enhancements`. |
| *Erro de URL obrigatória no card final* | Criativo (Carrossel) | `multi_share_end_card` definido como `true` em campanhas sem URL de destino (ex: perfil do Instagram). | Definir `multi_share_end_card` como `false` e `multi_share_optimized` como `false`. |

