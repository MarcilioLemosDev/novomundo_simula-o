# 00 — Método de Desenvolvimento

Este repositório respeita três etapas. Nenhum artefato entra fora da etapa a que pertence.

## Etapa 1 — Entendimento

Momento de discussão e de **estresse**. Aqui não se escreve código: escreve-se a pedra.

O produto desta etapa é a *base de pedra informativa* — o conjunto de decisões, axiomas,
definições e tensões que conduzirão o projeto inteiro. O que for gravado aqui só muda por
decisão explícita e registrada, nunca por conveniência de implementação.

Regra da etapa: **toda decisão precisa sobreviver ao estresse antes de virar pedra.**
Estressar significa perguntar o que quebra, o que é ilusão de solução, e o que só parece
resolvido porque ainda não foi tocado.

Estado de um item nesta etapa:
- `PEDRA` — decidido, ratificado, vinculante.
- `PROPOSTO` — recomendação minha, aguardando ratificação do Senhor.
- `TENSÃO` — conflito real e ainda não resolvido; ver `04-tensoes-abertas.md`.

## Etapa 2 — Construção livre

Liberdade de implementação **dentro** da pedra. Nesta etapa se erra, se joga fora, se
refaz, se experimenta. Não há compromisso com elegância nem com permanência: há
compromisso com aprender o que o modelo faz de verdade quando roda.

Único limite: nada construído aqui pode violar um axioma marcado `PEDRA`. Se a construção
mostrar que um axioma é impossível ou errado, isso não se contorna no código — volta-se à
Etapa 1, estressa-se, e a pedra é reescrita à vista de todos.

## Etapa 3 — Implantação final

Consolidação. Sai o que foi descartável, fica o que provou. Aqui se busca estabilidade,
reprodutibilidade e a capacidade de rodar a simulação por longos horizontes de tempo lunar
sem intervenção.

## Ordem de leitura da pedra

1. `01-pedra-fundamental.md` — o que é o indivíduo e o que "sem defeitos" significa.
2. `02-tempo-lunar.md` — o vetor tempo.
3. `03-mapa-escopo-inicial.md` — o mundo 2D e o escopo inicial de ação.
4. `04-tensoes-abertas.md` — o que ainda não sobreviveu ao estresse.
