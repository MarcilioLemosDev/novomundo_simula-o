# 02 — O Tempo Lunar

O tempo não é cenário. É **vetor**: dentro do mapa, é ele que dá direção ao indivíduo.
Tudo que ele percebe, crê, esquece e decide carrega carimbo lunar.

## 1. Escala `PEDRA`

O calendário é lunar, **mas tem dias**. O dia é a unidade que ele vive; o mês é a unidade
que ele pensa.

```
tick        = unidade atômica de decisão (1 ciclo percepção→deliberação→ação)
dia         = 24 ticks
mês lunar   = 29,53059 dias  (mês sinódico real)
fase        = 1/8 do mês ≈ 3,69 dias
ano lunar   = 12 meses ≈ 354,37 dias
```

Não arredondar o mês para 29 ou 30. A fração é o que produz a deriva da §4, e a deriva é o
primeiro problema real que o indivíduo terá para resolver.

---

## 2. Dilatação por movimento `PEDRA`

> **Todo movimento no mapa faz o tempo dele correr 3× mais rápido.**

```
MOVER      → relógio avança 3 ticks
demais ações → relógio avança 1 tick
```

Isso reordena a economia inteira do indivíduo. Deslocar-se deixa de ser o custo trivial que
é na maioria das simulações e passa a ser **a coisa mais cara que ele pode fazer**. Olhar,
marcar, coletar e esperar são baratos; ir até lá é caro.

Os seres não morrem (`01`, §6), então o que se paga não é tempo de vida — é **custo de
oportunidade**. Enquanto ele atravessa o mundo, o trem parte, a pessoa muda de lugar, a lua
vira e a consolidação leva o que não foi guardado. Numa vida eterna o tempo continua
precioso por simultaneidade, não por escassez.

Consequência direta e desejada: ele é empurrado a **pensar antes de andar**. Um indivíduo
que busca conhecimento e paga triplo por locomoção tem que aprender a extrair o máximo de
onde já está, e a planejar rotas em vez de vagar. A parcimônia emerge da física do mundo,
não de uma regra de comportamento que nós escrevemos.

### 2.1 Os dois relógios `PROPOSTO`

A dilatação abre uma porta que seria desperdício não atravessar.

- `t_mundo` — tempo do mundo. É o que rege a lua de verdade.
- `t_proprio` — tempo vivido pelo indivíduo. Avança 3× durante movimento.

Se a contagem interna dele nasce de `t_proprio`, mas a lua que ele **vê** nasce de
`t_mundo`, então **a conta dele corre à frente do céu, na proporção exata do quanto ele
andou**.

Isso lhe dá uma segunda anomalia, e ela é pedagogicamente superior à primeira: é
**correlacionada com as próprias escolhas dele**. Quanto mais viaja, mais seu calendário
mente. É descobrível, é reproduzível, e ensina a lição epistêmica mais importante que existe:

> **quando o relógio de dentro discorda do céu de fora, o céu está certo.**

Um humano defeituoso confia na sensação interna contra a evidência externa. O indivíduo tem
que aprender o contrário — e não por decreto nosso, mas por ter perdido coisas.

Recomendo adotar. Se em vez disso o `3×` for apenas taxa de simulação (tempo do mundo
correndo mais rápido durante deslocamento, com um relógio só), o mecanismo de custo da §2
permanece idêntico e apenas os dois relógios caem. Aguardo a palavra do Senhor.

---

## 3. O que o ciclo lunar modula `PROPOSTO`

Se a lua não modula nada, ela é decoração e o projeto fica mais pobre por tê-la. Proposta
de três acoplamentos, todos com sentido funcional:

**a) Consolidação de memória.** A destilação episódico→semântico (N1) acontece na virada
para a lua nova. Entre uma consolidação e outra o indivíduo acumula bruto; na virada, ele
comprime. Isso dá ao mês lunar um significado interno real: é o período do seu pensamento.

**b) Luminosidade → raio de percepção.** O raio de N0 varia com a fase. Lua cheia enxerga
longe e barato; lua nova enxerga perto. Isso cria ritmo natural de exploração e recolhimento
sem precisar programar "rotina" nenhuma — ela **emerge**.

**c) Horizonte de planejamento.** O planejamento de N4 se ancora na fase seguinte. Ele
naturalmente pensa em blocos de ~3,69 dias.

## 4. A deriva — e por que ela é o presente mais valioso do projeto `PROPOSTO`

Esta deriva é independente da de §2.1 e tem outra causa — aqui não é o relógio dele que
corre, é o próprio calendário lunar que não fecha com o ano do mundo:

- **O mundo** roda em tempo físico contínuo (e, se houver estações no mapa, elas são solares).
- **O indivíduo** só tem o calendário lunar puro — porque a lua é o que ele *vê*.

Doze meses lunares dão 354 dias. O ano solar dá ~365. **A cada ano o calendário dele
escorrega ~11 dias contra o mundo.**

Ele não é avisado disso.

O que acontece então é o coração da Etapa 2: um agente cuja definição é *buscar
conhecimento* recebe, de graça, seu primeiro enigma legítimo — suas previsões começam a
falhar de um jeito lento, sistemático e detectável. Se a arquitetura presta, ele vai:

1. registrar erro de previsão sazonal (N2, com procedência — A1);
2. sentir a contradição acumular na fila de A5;
3. gastar o custo de revisão de A2 sobre uma crença muito entrincheirada — o próprio calendário;
4. e, se for capaz disso, **inventar o mês intercalar** — descobrir o calendário lunissolar sozinho.

Esse é o melhor teste possível dos oito axiomas: não é um benchmark que nós escrevemos, é
um problema que o mundo tem e que ele precisa achar. Se ele resolver, o modelo presta. Se
ele nunca perceber, sabemos exatamente qual camada falhou.

**Recomendação forte: manter a deriva e não contar a ele.**

## 5. Notação

Todo registro no diário e toda procedência de crença usam:

```
A{ano}.M{mês}.F{fase}.D{dia}.T{tick}      ex.: A0.M3.F5.D22.T14
```

Monotônico, legível, e ordena por comparação de string.
