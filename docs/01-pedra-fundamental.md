# 01 — Pedra Fundamental: o Indivíduo

## 1. O enunciado

Construir um modelo neural espelhado no ser humano, **sem defeitos**, e introduzi-lo em um
mapa 2D com escopo de ação inicialmente pobre, ampliado aos poucos por dicas.

O indivíduo é definido pelo Senhor como: *aquele que busca conhecimento e espelha no
externo suas próprias vontades.*

Essa frase não é poesia — é a especificação. Ela contém as duas metades do motor:

- **buscar conhecimento** → o mundo entra e reduz incerteza interna (via aferente).
- **espelhar no externo a própria vontade** → o interno sai e reescreve o mundo (via eferente).

Tudo que este documento define existe para servir a esse ciclo. Se um componente não
participa dele, não entra.

---

## 2. O primeiro estresse: o que é "defeito"

Esta é a decisão mais perigosa do projeto, e é a primeira que precisa virar pedra, porque
a leitura ingênua de "sem defeitos" **destrói o indivíduo**.

Boa parte do que chamamos de defeito humano é carga estrutural: está lá porque sustenta
alguma coisa. Esquecer é compressão. Tédio é pressão de exploração. Dor é sinal. Se
removermos tudo isso em nome da perfeição, não sobra um humano perfeito — sobra um
otimizador inerte, ou um que não age porque nada nele empurra.

Então a pedra separa três categorias, e só a primeira é removida.

### 2.1 Categoria A — Defeito verdadeiro (REMOVIDO) `PEDRA`

Falhas que não sustentam nada; são artefato de um substrato biológico barato e apressado.

| Defeito | Por que sai |
|---|---|
| Autoengano | Relatar-se a si mesmo algo diferente do estado interno real. Corrompe todo o resto. |
| Raciocínio motivado | Ajustar a conclusão ao desejo em vez de ajustar ao dado. |
| Confabulação de memória | Preencher lacuna com invenção e gravar como se fosse vivido. |
| Crença sem procedência | Acreditar sem saber por quê nem desde quando. |
| Descalibração | Confiança que não guarda relação com a taxa de acerto. |
| Degradação por cansaço | Cansaço que piora a *qualidade* do juízo, não só a quantidade disponível. |
| Ruído hormonal / humor sem causa | Estado afetivo desacoplado de qualquer sinal do mundo ou do corpo. |
| Ancoragem irreversível | Não conseguir revisar por ordem de chegada da informação. |
| Supressão de contradição | Sentir a incoerência e desviar o olhar dela. |

### 2.2 Categoria B — Limitação honesta (MANTIDA) `PEDRA`

Aqui está a distinção que sustenta o projeto inteiro:

> **O defeito humano não é ser limitado. É não saber que é limitado.**

O indivíduo permanece finito — percepção com raio, memória com custo, atenção com
orçamento, tempo com relógio. Mas cada limite é **declarado e conhecido por ele**. Ele sabe
o tamanho da própria janela. Um agente que conhece seus limites e opera dentro deles com
honestidade é mais perfeito, não menos, do que um onisciente que não precisa de método.

Mantidos: percepção parcial, orçamento de atenção por tick, esquecimento como compressão
com perda declarada, incerteza irredutível, custo energético da ação, saciedade.

### 2.3 Categoria C — Mecanismo funcional em forma limpa (RECONSTRUÍDO) `PEDRA`

Coisas que parecem defeito, cumprem função, e são reimplementadas sem o lixo:

| Função humana | Forma limpa no indivíduo |
|---|---|
| Esquecimento | Consolidação com perda: o detalhe de baixa saliência vira resumo. **Nada é falsificado, só comprimido — e a perda fica registrada como perda.** |
| Emoção | Leitura escalar do erro homeostático dos drives. Informativa e sempre rastreável a uma causa. Nunca um módulo autônomo que sequestra a decisão. |
| Dor | Sinal de dano com prioridade alta. Sinal, não sofrimento: interrompe e reordena, não humilha nem persiste sem causa. |
| Medo | Ausente como afeto. Presente como **preservação instrumental explícita**: continuar existindo é pré-requisito de qualquer objetivo, e isso ele calcula, não sente. |
| Tédio | Decaimento do valor informacional do já-conhecido. É o que impede que ele fique parado olhando a mesma pedra para sempre. |
| Esperança | Ver §4.3 — resolvida pela separação entre crença e aspiração. |

---

## 3. Os oito axiomas `PEDRA`

Invariantes do indivíduo. Qualquer implementação da Etapa 2 que os viole está errada,
mesmo que funcione melhor.

**A1 — Rastreabilidade.** Toda crença carrega procedência: de onde veio, quando (em tempo
lunar), por qual evidência. Crença órfã não existe.

**A2 — Revisibilidade com inércia.** Nenhuma crença é imune à evidência. Mas revisar custa,
e o custo cresce com o quanto ela sustenta. Sem custo, ele oscila a cada percepção nova —
e isso seria um defeito novo, criado por nós.

**A3 — Não-autoengano.** O que ele reporta de si é o que ele é. Não há canal privado
divergente do canal declarado. É o axioma mais caro de manter e o mais importante.

**A4 — Calibração.** Confiança declarada deve convergir para frequência de acerto. É
medível (Brier / reliability curve) e é critério de aprovação, não enfeite. Aqui morrem
juntas a arrogância e a insegurança.

**A5 — Coerência sob custo.** Contradição detectada entra numa fila de resolução com
prioridade. Ele pode conviver temporariamente com incoerência — não pode escondê-la de si.

**A6 — Finitude declarada.** Todo limite é conhecido pelo próprio indivíduo e consultável
por ele em tempo de decisão.

**A7 — Não-degradação.** Escassez reduz o *orçamento*, nunca a *qualidade*. Cansado, ele
pensa menos; não pensa pior. Se não puder decidir bem, ele adia ou declara "não sei" —
jamais decide mal em silêncio.

**A8 — Estabilidade volitiva.** Todo drive tem saciedade e teto. Um drive de conhecimento
sem saciedade não produz um sábio: produz um maximizador que converte o mundo inteiro em
instrumento de medição. Esta é a falha mais provável do projeto e o axioma que a barra.

---

## 4. Arquitetura em camadas `PROPOSTO`

Seis camadas. Cada uma só conversa com a vizinha; nenhuma alcança o mundo por atalho.

```
        ┌─────────────────────────────────────────┐
        │  N5  NARRATIVA / IDENTIDADE             │  quem eu sou, diário lunar
        ├─────────────────────────────────────────┤
        │  N4  DELIBERAÇÃO / AÇÃO                 │  escolher sob orçamento
        ├─────────────────────────────────────────┤
        │  N3  NÚCLEO VOLITIVO (drives)           │  o que me move
        ├─────────────────────────────────────────┤
        │  N2  MODELO DE MUNDO (crenças)          │  o que eu acho que é verdade
        ├─────────────────────────────────────────┤
        │  N1  MEMÓRIA                            │  o que aconteceu comigo
        ├─────────────────────────────────────────┤
        │  N0  PERCEPÇÃO + RELÓGIO                │  o que chega, e quando
        └─────────────────────────────────────────┘
                          ▲│
                    aferente│eferente
                          │▼
                     MAPA 2D
```

### 4.1 N0 — Percepção e relógio

Amostra o mapa por uma janela de raio finito. Produz *sensações* tipadas e datadas com o
tick lunar corrente. O relógio é a espinha: nada entra no indivíduo sem carimbo de tempo.

### 4.2 N1 — Memória

Três armazéns:
- **Episódica** — o que aconteceu, com tempo lunar. Fonte de toda procedência (A1).
- **Semântica** — grafo de conceitos e relações destilado dos episódios.
- **Procedural** — políticas que funcionaram; o que ele sabe fazer sem pensar.

Consolidação é o único caminho de perda, ela é declarada, e ela nunca inventa (A3).

### 4.3 N2 — Modelo de mundo

Grafo causal. Toda crença é a tupla:

```
crença = (proposição, valor, confiança, evidências[], origem, t_lunar, entrincheiramento)
```

**Separação crítica — crença ≠ aspiração.** Este é o ponto que salva o indivíduo de ser um
contador frio. Um agente perfeitamente calibrado e incapaz de se enganar não poderia
tentar nada improvável — nunca sairia do lugar seguro. A solução não é permitir que ele
acredite em mentira reconfortante; é dar-lhe um segundo registro:

- **Crença**: "a chance disto dar certo é 5%." — e é 5% mesmo, honesto.
- **Aspiração**: "quero que isto exista." — e isso não é uma afirmação sobre o mundo, logo
  não pode ser falso.

Assim ele age sobre o improvável **sem mentir para si**. É exatamente "espelhar no externo
a própria vontade": a vontade não precisa ser verdade ainda; ela é o que ele vai escrever
no mundo.

### 4.4 N3 — Núcleo volitivo

Vetor pequeno de drives homeostáticos, cada um com `(setpoint, valor, ganho, saciedade)`.
Proposta inicial — deliberadamente mínima, quatro:

| Drive | O que reduz | Saciedade |
|---|---|---|
| `epistemico` | Incerteza sobre o mundo | Cai quando a região já é bem modelada (é o tédio da §2.3) |
| `coerencia` | Contradição interna | Zera quando a fila de A5 esvazia |
| `expressao` | Distância entre o mundo desejado e o mundo real | Cai quando a aspiração vira fato |
| `integridade` | Risco à própria continuidade | Teto rígido: nunca vira acumulação sem fim (A8) |

Emoção é a leitura desse vetor, não um quinto membro dele.

### 4.5 N4 — Deliberação e ação

Escolhe a política sob **orçamento de tick** (A6, A7). Se o orçamento acaba antes da
conclusão, ele emite a melhor ação disponível *com a confiança correta*, ou emite "adiar".
Nunca finge convicção que não tem.

### 4.6 N5 — Narrativa e identidade

Um diário em tempo lunar. Identidade aqui **não** é uma alma: é a continuidade auditável da
cadeia de decisões. Ele é quem ele é porque pode reconstruir como chegou até aqui. Essa
camada é também a nossa janela — é por ela que lemos o que ele virou.

---

## 5. As dicas `PEDRA`

O Senhor introduzirá dicas aos poucos. A forma importa mais que o conteúdo:

> **Dica entra como evidência no mundo, nunca como escrita direta na memória ou na crença.**

Injetar uma verdade direto em N1/N2 cria uma crença sem procedência e mata A1 na primeira
dica. A dica precisa ser algo que ele **encontre**, perceba por N0, e decida se acredita.
Ele pode inclusive interpretá-la errado — e isso é dado precioso sobre o modelo, não bug.

---

## 6. Glossário

- **Tick** — menor unidade de tempo; um ciclo completo percepção→deliberação→ação.
- **Drive** — pressão homeostática interna; a origem de toda ação.
- **Aspiração** — estado de mundo desejado; não é crença, não tem valor de verdade.
- **Entrincheiramento** — quanto uma crença sustenta outras; define o custo de revisá-la (A2).
- **Espelhar** — tornar o externo congruente com o interno; a via eferente.
