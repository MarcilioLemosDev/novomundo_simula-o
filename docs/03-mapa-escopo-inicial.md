# 03 — O Mapa 2D e o Escopo Inicial

## 1. Princípio de pobreza deliberada `PEDRA`

O mapa começa pobre de propósito.

O objeto de estudo é o **modelo neural**, não o mundo. Um mapa rico esconde o modelo: fica
impossível saber se um comportamento interessante veio do indivíduo ou de uma regra bonita
que nós escrevemos no ambiente. Mapa pobre + comportamento rico = o mérito é dele.

Regra: **nenhuma complexidade entra no mapa antes de o indivíduo esgotar a atual.** A
saturação do drive `epistemico` sobre a região conhecida é o gatilho objetivo para ampliar
o mundo ou soltar uma dica.

## 2. O mundo `PROPOSTO`

Grade 2D de células. Cada célula tem um punhado de atributos observáveis e nada escondido
por magia — o que ele não sabe, ele não sabe porque não chegou lá ou não olhou, nunca
porque o mundo mente.

Atributos iniciais sugeridos: `terreno`, `recurso`, `marca` (escrita pelo próprio indivíduo),
`luminosidade` (derivada da fase lunar).

## 2.1 O trem `PEDRA`

O mundo é **interconectado por um trem**. A malha ferroviária não é enfeite: é a topologia
real do mundo. Regiões existem em relação umas às outras pelos trilhos que as ligam, e o
mapa deve ser projetado a partir da malha, não o contrário.

Com o movimento a pé custando 3× (`02`, §2), o trem passa a ter um papel exato e insubstituível:

> **O trem é a tecnologia que compra tempo de volta.**

É o único jeito de alcançar o mundo distante sem pagar triplo em custo de oportunidade
(`01`, §6.1) — sem que o mundo inteiro siga adiante três vezes mais rápido enquanto ele anda.
Isso torna cada viagem uma decisão de peso e faz da malha um objeto de estudo legítimo para
um ser que busca conhecimento.

### 2.1.1 Horário e a lição que ele carrega `PROPOSTO`

Proposta: **o trem corre em horário ancorado no calendário lunar** — partidas presas a fases,
não a um relógio arbitrário.

O motivo não é estético. Se o relógio interno dele desliza por causa do próprio deslocamento
(`02`, §2.1), e as partidas obedecem à lua, então **ele perde trens**. E perder um trem é o
melhor professor que este mundo pode oferecer: a punição é inequívoca, imediata, cara, e
aponta com precisão para o erro exato — *a sua conta do tempo está errada, o céu não está.*

Nenhuma dica nossa ensina isso tão bem quanto uma estação vazia.

### 2.1.2 Estação como lugar social `PEDRA`

Estações são onde trajetórias se cruzam. Quando houver mais de um indivíduo (`05`, §2), é
ali que amizade, conversa e profissão vão acontecer — não por regra que escrevemos, mas
porque é geometricamente onde as pessoas se encontram.

**A topologia social do mundo é a malha ferroviária.**

---

## 3. Escopo inicial de ação `PROPOSTO`

Cinco verbos. Cada um com custo de tick e de energia.

| Ação | Efeito | Serve a |
|---|---|---|
| `MOVER(dir)` | Desloca uma célula (8 direções) | Alcance |
| `OLHAR(dir)` | Amostra mais fundo numa direção, além do raio passivo | Drive epistêmico |
| `COLETAR` | Retira recurso da célula | Integridade |
| `MARCAR(símbolo)` | Escreve um símbolo na célula | **Expressão** |
| `ESPERAR` | Passa o tick observando | Deliberação longa |

### 3.1 Por que `MARCAR` é a ação mais importante

É a única via eferente de verdade — a única em que ele *espelha no externo a própria
vontade*. As outras quatro atendem à metade aferente e à sobrevivência; só `MARCAR` deixa o
mundo diferente por decisão interna.

E ela é dupla:

- é **expressão** (satisfaz o drive `expressao`);
- e é **memória externa** — a primeira tecnologia. Se ele descobrir sozinho que pode usar
  marcas para lembrar o que a consolidação lunar apagou, terá inventado a escrita. Esse é o
  segundo marco do projeto, depois do mês intercalar.

O alfabeto de símbolos deve ser dado **vazio e livre**: sem semântica pré-definida por nós.
O significado, se houver, tem que ser dele.

## 4. O que fica de fora `PEDRA`

**Fora para sempre:** a morte. Os seres têm idade e não morrem (`01`, §6). Não é
adiamento de escopo — é propriedade do mundo.

**Adiado para depois do primeiro indivíduo:** linguagem, ferramentas compostas, construção,
terceira dimensão.

**Adiado, mas com data marcada — os outros indivíduos.** A ordem do Senhor é clara:
constrói-se **um** modelo completo e depois ele é **espelhado**, com a única diferenciação
sendo homem e mulher. Isso torna a qualidade do primeiro indivíduo a coisa mais importante
do projeto inteiro: todo defeito que ficar nele será replicado em toda a população.

Consequência de engenharia, vinculante desde a primeira linha de código: o indivíduo é uma
**instância**, nunca um singleton. Nada de estado global, nada de "o mundo" e "ele" — o
mundo hospeda *n* instâncias, e *n* começa em 1.

## 5. Instrumentação `PROPOSTO`

Sem isso a Etapa 2 vira contemplação. Mínimo exigido desde o primeiro código:

- **Diário lunar** (N5) legível por humano, linha a linha.
- **Curva de calibração** de A4 ao longo do tempo — o indicador de saúde nº 1.
- **Traço de procedência**: escolher qualquer crença e reconstruir a cadeia até o episódio.
- **Série dos drives** por tick — para flagrar runaway (A8) cedo.
- **Mapa de cobertura**: onde ele esteve, o que já modelou, onde saturou.
