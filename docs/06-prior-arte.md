# 06 — Arte Prévia: o que existe e o que serve

O Senhor pediu que se buscasse um repositório com um modelo neural deste calibre para
espelhar e ajustar. Fui buscar. O resultado honesto:

> **Não existe um repositório para espelhar. Existem três para saquear.**

E há um motivo estrutural para não existir, que vale mais do que a busca em si — está na §4.

---

## 1. Generative Agents / Smallville — Stanford + Google

`joonspk-research/generative_agents` · Apache-2.0 · Python · [repo](https://github.com/joonspk-research/generative_agents) · [paper](https://arxiv.org/pdf/2304.03442)

Vinte e cinco agentes numa vila 2D. Planejam o dia, conversam, formam relações, coordenam
festas. Os comportamentos sociais são **emergentes, não programados**. Tem mapa 2D e frontend
Django que mostra os bonecos andando em tempo real.

É, de longe, o que mais se parece com o norte do Senhor (`05`) — é literalmente "ver meu
boneco vivendo e se relacionando".

**Mas não serve como base, e a razão é dura:** cada pensamento é uma chamada de LLM. Isso
não é um detalhe de implementação — é a **negação exata da nossa pedra**. Confabulação,
crença sem procedência e descalibração não são bugs de um LLM: são o modo de operação dele.
Espelhar Smallville seria construir um ser feito inteiramente da Categoria A de `01`, §2.1.
Além disso, custa dinheiro por tick e trava no rate limit — inviável para um mundo que roda
em séculos lunares.

**O que se saqueia:** o *memory stream* com recuperação por recência + importância +
relevância, o mecanismo de *reflection* (destilar episódios em conclusões — é a nossa
consolidação lunar), e sobretudo **o frontend**: eles resolveram o problema de deixar uma
mente visível, que `05`, §1 elevou a requisito.

## 2. MicroPsi / Teoria Psi — Joscha Bach, sobre Dietrich Dörner

`joschabach/motivation_machine` · [repo](https://github.com/joschabach/motivation_machine) · [paper](https://agi-conf.org/2015/wp-content/uploads/2015/07/agi15_bach.pdf)

Este é o parente próximo do nosso N3. Arquitetura **neuro-simbólica** — exatamente o híbrido
que o Senhor ratificou em T3 — com agentes situados num mundo, movidos por necessidades
homeostáticas, e com **emoção modelada como modulação de percepção, ação, planejamento e
memória**, e não como um módulo à parte.

Isso é, palavra por palavra, o que escrevemos em `01`, §4.4 antes de eu ter ido buscar. A
convergência é boa notícia: significa que o desenho do núcleo volitivo não é invenção
solitária, tem trinta anos de literatura atrás dele.

As necessidades do Psi são cinco: segurança, dominância, competência, ordem e afiliação.
Vale comparar com os nossos cinco drives — *afiliação* é o nosso `vinculo`, *competência*
tem parentesco com o `epistemico`. **Dominância nós não queremos**, e essa recusa é uma
decisão de projeto que precisa ser consciente, não distração.

**O que se saqueia:** o modelo de motivação inteiro — urgência, força de necessidade,
saciedade, e a modulação afetiva derivada. É a peça mais madura e diretamente aproveitável
de toda a arte prévia.

## 3. ACT-R e SOAR — as arquiteturas cognitivas clássicas

Décadas de maturidade em algo que precisamos e que nenhum dos dois anteriores tem: o **ciclo
de deliberação sob orçamento** (nosso N4) e memória declarativa versus procedimental
(nosso N1). São pesadas e nada divertidas de assistir, mas o que elas acertaram, acertaram
faz quarenta anos.

**O que se saqueia:** a estrutura do ciclo de decisão e a separação declarativo/procedimental.

---

## 4. O que ninguém tem — e é justamente o nosso projeto

Nenhuma das três implementa:

| | Ausente na arte prévia |
|---|---|
| **A1** | Procedência obrigatória de toda crença |
| **A3** | Não-autoengano verificável |
| **A4** | Calibração como critério de aprovação |
| **§4.3** | Separação entre crença e aspiração |
| **T5** | Proibição de realimentação positiva do erro (angústia) |

E não é omissão: **ninguém tenta isso porque ninguém está construindo um ser sem defeitos.**
A literatura de arquitetura cognitiva quer *reproduzir* o humano, defeitos inclusive — em
ACT-R, modelar o erro humano é o objetivo, é assim que se valida o modelo contra dados
experimentais. Nós queremos o contrário.

Esse é o valor original do projeto do Senhor, e é a razão de não haver o que espelhar.

---

## 5. Recomendação `PROPOSTO`

**Não fazer fork de nada. Construir do zero, roubando por peça:**

```
N0  percepção        → nosso, simples
N1  memória          → memory stream do Generative Agents (sem o LLM)
                       + declarativo/procedimental do ACT-R
N2  crenças          → NOSSO. Não existe equivalente. É o coração.
N3  drives           → modelo de motivação do MicroPsi, adaptado
N4  deliberação      → ciclo sob orçamento do ACT-R/SOAR
N5  narrativa        → NOSSO, com o frontend do Smallville como referência de forma
```

Justificativa: fork traz junto a filosofia de quem escreveu. Fork do Smallville importa a
confabulação; fork do MicroPsi importa a dominância. As duas contaminações são invisíveis
até tarde demais, e neste projeto o primeiro indivíduo é o molde de todos (`03`, §4) — não
há morte nem seleção para limpar um erro herdado depois.

Sobre LLM, para não ficar ambíguo: ele **não entra no laço de pensamento do indivíduo**.
Se um dia servir, será fora do laço — para verter o estado interno já decidido em fala
legível, nunca para decidir. A decisão é do modelo; a palavra pode ser emprestada.
