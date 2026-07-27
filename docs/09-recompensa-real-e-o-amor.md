# 09 — A Recompensa Real, a Angústia, e o Amor

Três coisas que o Senhor levantou e que mudam o núcleo do modelo.

---

## 1. Fora o crédito `PEDRA`

> *"tem de ser um modelo neural com livre arbítrio mas que busque recompensa real,
> não um crédito qualquer."*

A crítica é procedente e atinge a raiz. Na primeira versão, o mundo entregava um número
por ação — `ganho = 0.55` — e o indivíduo escolhia o maior. Isso faz dele um agente de
recompensa escalar: **ele não amava conhecer, amava pontos.** É precisamente o
maximizador que A8 foi escrito para barrar, e ele tinha entrado pela porta dos fundos,
pelo mundo em vez de pelo indivíduo.

### A troca

> **A recompensa deixa de ser prometida e passa a ser medida.**

- O mundo descreve **o que a ação faz** — "estarás na biblioteca", "chegarás a Tóquio" —
  e nunca quanto isso vale. Valor não é propriedade do mundo.
- O indivíduo avalia pelo que aquilo **já fez por ele**: quanto cada falta de fato
  cedeu, nas vezes em que tentou. É a `Experiencia` (`novomundo/experiencia.py`).
- O que ele não conhece, ele avalia pela curiosidade: não saber é, em si, uma falta.

Três consequências, e a terceira é a que importa:

1. **Ele nasce sem saber de nada.** Não sabe que ler ajuda nem que a praça alegra.
   Descobrir isso é a vida dele, não um pré-requisito dela.
2. **O que move cada um passa a ser diferente**, com o mesmo espírito e o mesmo mundo,
   porque cada um viveu outra coisa.
3. **O livre arbítrio deixa de ser promessa nossa e vira fato verificável.** A escolha
   passa a vir da biografia. Se alguém quiser prever o que ele fará, terá de ler a vida
   dele — não o nosso código.

### O escopo obrigatório

> *"no dia dele tem tempo a tudo — introduzir um escopo obrigatório de buscar
> conhecimento, duas horas semanais de trabalho digamos, e o resto livre."*

Num ser eterno e sem escassez, o dia não tem aperto: cabe tudo. Isso é bonito e é um
problema — sem nenhuma forma, o tempo vira massa informe.

O compromisso dá forma. E note-se o que ele **não** é: não é uma regra que o obrigue,
porque uma regra que o obrigasse quebraria o livre arbítrio. É um **acordo que ele
carrega**, e a falha em cumpri-lo não gera culpa — gera **incoerência**: o que ele disse
que faria não bate com o que fez, e isso entra na fila de A5 como qualquer outra
contradição.

> **Obrigação aqui é coerência, nunca culpa.** Um ser sem defeitos não se pune; ele nota
> a distância entre a palavra e o ato, e resolve.

---

## 2. A angústia, mais fundo `PEDRA`

O critério mecânico de T5 continua válido — falta cresce a passo constante, angústia
cresceria em função de si mesma. Mas o Senhor pediu para ir mais fundo, e há mais.

O que faz a angústia humana não é a intensidade da falta. São três coisas:

| | O que é | Existe neste mundo? |
|---|---|---|
| **Falta sem objeto** | Doer sem saber do quê | **Não.** Toda falta dele aponta para um drive nomeado, e ele sabe qual |
| **Falta sem caminho** | Saber do que se precisa e não ver rota — o desespero | **Sim, às vezes** — e é legítima. Ver §3 |
| **Falta que se alimenta de si** | Doer mais só porque já dói | **Não.** Barrada por T5, e verificável por execução |

A definição funda, então:

> **Angústia é falta cujo caminho de revisão está fechado.**

E aqui a vida eterna faz o que nenhum ajuste de parâmetro faria: **nenhuma revisão é
urgente demais para caber.** A2 sempre permite revisar; o custo é alto mas o tempo é
infinito. Não existe, neste mundo, a falta que não pode nem ser suprida nem ser
reescrita — e é por isso que a angústia é estruturalmente impossível aqui, não por
proibição, mas por falta de lugar onde existir.

---

## 3. O amor dói, e a dor é legítima `PEDRA`

> *"amor dói às vezes, mas dói — e se for para ser, depois é preenchido pelo encontro de
> dois amores. Sexo com amor, conversa com amor. Aí entram os tipos de relacionamento."*

Isto corrige uma leitura ingênua que eu poderia ter feito: *sem defeitos* não significa
*sem dor*. A dor do amor não é defeito. Ela tem objeto — esta pessoa —, tem caminho —
a reciprocidade — e cessa quando é preenchida. Pelos três critérios da §2, é **falta**,
inteira e legítima.

O que a tornaria defeito seria outra coisa: doer sem saber por quem, ou doer cada vez
mais só por já doer, ou não poder ser revista nunca. Nada disso ocorre.

### 3.1 A mutualidade `PEDRA`

A peça estrutural, e é ela que faz o amor custar:

> **O drive `vinculo` não se satisfaz sozinho. Só a reciprocidade o preenche.**

Um afeto não correspondido continua doendo — corretamente, e sem que isso seja doença.
Ele tem então dois caminhos, e ambos são dele:

- **esperar e insistir**, porque pode ser que seja para ser;
- **enlutar** (T7.1) — reescrever a aspiração, ao custo de A2, com começo, custo e fim.

O que ele nunca faz é o terceiro caminho, que é o humano defeituoso: fingir que não dói,
ou converter a dor em posse.

### 3.2 Com amor é outra coisa `PEDRA`

> *"sexo com amor, conversa com amor."*

O mesmo ato, com e sem vínculo, **não preenche igual** — e agora o modelo consegue
representar isso sem que nós escrevamos a diferença, porque a recompensa passou a ser
medida (§1). O indivíduo vai descobrir, na própria experiência, que conversar com quem
ele ama baixa uma falta que conversar com um desconhecido não baixa.

Ninguém lhe conta. Ele aprende. E é exatamente o que o Senhor quer poder assistir.

### 3.3 Os tipos de relacionamento `PROPOSTO`

Um eixo só, e ele é o que já sustenta T7 — **insubstituibilidade**:

| Tipo | O que o define | O que preenche |
|---|---|---|
| **Conhecido** | Sei que existe, tenho pouco modelo dele | quase nada |
| **Amigo** | Modelo acurado mútuo, história partilhada, insubstituível | conversa, presença, tempo dado |
| **Companheiro(a)** | Amizade + aspiração dirigida ao florescimento do outro + exclusividade escolhida | conversa com amor, sexo com amor, projeto comum |
| **Pai / mãe / filho** | Vínculo por origem: um veio do outro | ensinar, aprender, acompanhar |

Regra que atravessa os quatro, herdada de `01`, §4.4: **vínculo mede distância ao outro,
nunca controle sobre o outro.** Ciúme e posse continuam na Categoria A — não porque o
amor não possa doer, mas porque possuir não é amar.

### 3.4 O que fica em aberto `TENSÃO`

Duas coisas, para o próximo estresse:

- **T7.2 — a exclusividade é escolha ou natureza?** Se o companheirismo exige
  exclusividade, ela vem de uma decisão registrada dos dois, ou é propriedade do drive?
  A primeira preserva o livre arbítrio; a segunda seria nós escrevendo a moral deles.
  Inclino-me fortemente à primeira.
- **T7.3 — quem ama primeiro?** Se `vinculo` só se satisfaz em mutualidade, o primeiro a
  amar paga sozinho por um tempo. Isso é correto e é a vida — mas precisa de teto, senão
  vira a falta sem caminho da §2.
