# Use com responsabilidade

> Leia esta página **antes** de deixar a IA mexer na sua conta. São dois minutos, e eles
> separam "ferramenta poderosa" de "conta restringida".

Esta pasta gerencia campanhas no Facebook e no Instagram pelo SDK oficial da Meta
(`facebook-business`) — **54 operações** em 9 scripts:

| Script | O que faz |
|---|---|
| `read.py` | 22 operações de leitura (campanhas, conjuntos, anúncios, criativos, públicos) |
| `insights.py` | 5 operações de métricas e relatórios |
| `targeting.py` | 9 operações de busca de interesses, comportamentos e geolocalização |
| `create.py` | 8 operações de criação (campanha, conjunto, anúncio, criativo, mídia, público) |
| `update.py` | 4 operações de edição |
| `delete.py` | 2 operações de exclusão |
| `advanced.py` | duplicação de campanha/conjunto/anúncio e troca de `url_tags` |
| `dataset.py` | pixels: listar, criar, stats de evento e diagnóstico de saúde |
| `setup.py` | o diagnóstico: confere dependência, token e conexão. Não muda nada |

## Disclaimer: use com responsabilidade

Essa skill foi **vibe-codada com Claude Code** a partir da documentação oficial do [facebook-business SDK](https://github.com/facebook/facebook-python-business-sdk) e da [Meta Marketing API](https://developers.facebook.com/docs/marketing-api/). Ela é um projeto experimental que estamos começando a testar agora.

**Pontos importantes antes de usar:**

- **Use por sua conta e risco.** Nós não garantimos que o uso dessa skill não vai resultar em restrições, bloqueios ou qualquer problema na sua conta de anúncios. A Meta tem políticas próprias sobre automação e pode mudar as regras a qualquer momento.
- **Leia as políticas da Meta.** Antes de usar qualquer automação, entenda os [Termos de Serviço da Meta](https://www.facebook.com/policies/ads/) e as [regras de rate limiting da Marketing API](https://developers.facebook.com/docs/marketing-api/overview/rate-limiting/). A skill inclui delays entre operações de escrita, mas isso não é garantia de nada.
- **Revise o código.** Essa skill tem acesso de leitura e escrita na sua conta de anúncios. Antes de usar, avalie o código dos scripts pra entender o que cada operação faz. É open source justamente pra isso.
- **Campanhas sempre nascem pausadas.** Por segurança, toda criação via skill é feita com status PAUSED. Mas operações de edição e exclusão agem diretamente nos objetos. Tenha cuidado.
- **Sem garantia de funcionamento.** O SDK e a API da Meta mudam com frequência. Algo que funciona hoje pode quebrar amanhã. Se algo parar de funcionar, provavelmente é uma mudança na API, não no seu setup.

Em resumo: é uma ferramenta poderosa, mas você é o responsável pelo que acontece na sua conta. Use com consciência, teste em contas de teste primeiro se possível, e não faça nada que você não faria manualmente no Ads Manager.

---

## E uma última, que vale mais que todas

**Comece lendo, não escrevendo.** Passe os primeiros dias só puxando relatório e conferindo
número. Quando `insights.py` já for rotina, aí sim deixe a IA criar campanha — sempre pausada,
sempre revisada por você no Gerenciador antes de ativar.

