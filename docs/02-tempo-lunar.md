# 02 — O Tempo Lunar

O tempo não é cenário. É **vetor**: dentro do mapa, é ele que dá direção ao indivíduo.
Tudo que ele percebe, crê, esquece e decide carrega carimbo lunar.

## 1. Escala `PROPOSTO`

```
tick        = unidade atômica de decisão (1 ciclo percepção→deliberação→ação)
dia         = 24 ticks
mês lunar   = 29,53059 dias  (mês sinódico real)
fase        = 1/8 do mês ≈ 3,69 dias
ano lunar   = 12 meses ≈ 354,37 dias
```

Não arredondar o mês para 29 ou 30. A fração é o que produz a deriva da §3, e a deriva é o
primeiro problema real que o indivíduo terá para resolver.

## 2. O que o ciclo lunar modula `PROPOSTO`

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

## 3. A deriva — e por que ela é o presente mais valioso do projeto `PROPOSTO`

Decisão de dois relógios:

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

## 4. Notação

Todo registro no diário e toda procedência de crença usam:

```
A{ano}.M{mês}.F{fase}.D{dia}.T{tick}      ex.: A0.M3.F5.D22.T14
```

Monotônico, legível, e ordena por comparação de string.
