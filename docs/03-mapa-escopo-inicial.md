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

## 4. O que fica de fora agora `PEDRA`

Não entram na primeira rodada: outros indivíduos, linguagem, ferramentas compostas,
construção, morte por velhice, terceira dimensão.

Todos são reservados — mas a arquitetura de N0–N5 deve ser escrita já prevendo o dia em que
existir um segundo indivíduo, porque essa é a única ampliação que muda tudo (ver
`04-tensoes-abertas.md`, T4).

## 5. Instrumentação `PROPOSTO`

Sem isso a Etapa 2 vira contemplação. Mínimo exigido desde o primeiro código:

- **Diário lunar** (N5) legível por humano, linha a linha.
- **Curva de calibração** de A4 ao longo do tempo — o indicador de saúde nº 1.
- **Traço de procedência**: escolher qualquer crença e reconstruir a cadeia até o episódio.
- **Série dos drives** por tick — para flagrar runaway (A8) cedo.
- **Mapa de cobertura**: onde ele esteve, o que já modelou, onde saturou.
