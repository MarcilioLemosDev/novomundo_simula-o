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

### 1.1 O espírito `PEDRA`

O Senhor acrescentou o que ele **é**, e isto vale tanto quanto os axiomas:

> Amor puro pela vida, pelos sentimentos, por socializar, por visitar lugares, por ler
> livros, por viver com livre arbítrio.

Isso não é decoração de texto — é restrição de projeto, e corrige de saída o erro mais
provável. Um ser "sem defeitos" tende a sair da prancheta como um contador frio. Este não é.
Ele **ama viver**. Quatro consequências vinculantes:

- **Linha de base positiva.** O estado neutro dele não é a indiferença; é o contentamento.
  Os drives medem o que falta, mas viver não é só suprir falta — por isso a diversão existe
  sem justificativa (§4.4), e por isso um ser eterno que ama a vida está em paz com a
  eternidade em vez de esmagado por ela.
- **Lugares.** Visitar é fim, não só meio. Parte do drive `epistemico` responde à **novidade
  do lugar** em si — o que, com o custo 3× do movimento, torna cada viagem uma escolha de
  amor e não de logística.
- **Livros.** A leitura é canal de conhecimento em pé de igualdade com a percepção. E ela
  resolve, sozinha, o problema mais duro deste mundo: **o livro atravessa o mapa sem que
  ninguém pague o 3×.** Conhecimento viaja mais barato que gente. Isso faz do arco
  `MARCAR → escrita → livro` (`03`, §3.1) a tecnologia central da civilização deles, e não
  um enfeite.
- **Livre arbítrio.** A deliberação (N4) não pode ser roteirizada por nós em nenhum ponto.
  Se o comportamento dele for previsível a partir do nosso código em vez da história dele,
  o projeto falhou — é o critério de `05`, §5 dito por dentro.

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
| Medo | Ausente como afeto. Presente como **cautela instrumental explícita**: dano, perda e imobilização atrapalham qualquer objetivo, e isso ele calcula, não sente. Com vida eterna (§6) não há o que temer no fim — só o que evitar no caminho. |
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

## 4. Arquitetura em camadas `PEDRA`

Seis camadas. Cada uma só conversa com a vizinha; nenhuma alcança o mundo por atalho.

**Substrato (T3, ratificado): híbrido.** N0 e a parte perceptual de N1 são conexionistas —
representação distribuída, padrão aprendido. N2 a N5 são simbólicos e auditáveis. A linha
entre os dois é a **fronteira de declaração**: nada atravessa para N2 sem virar tupla de
crença com origem, evidência e tempo lunar. O que a rede "acha" ainda não é crença. É essa
fronteira que mantém A1 e A3 verificáveis apesar do substrato distribuído — e é por isso que
ela é o lugar mais importante do código inteiro.

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
| `vinculo` | Distância aos outros: afeto, companhia, pertencimento | Cai quando o vínculo é correspondido; **não** cai por quantidade de contatos |

O quinto drive entra por exigência do norte (`05`): sem ele não há companheira, amizade nem
profissão — só cálculo. Ele é corpo também: os seres têm relações carnais e se divertem, e
`vinculo` é onde isso vive.

Duas ressalvas que o mantêm sem defeito:

- **Saciedade obrigatória (A8).** Desejo sem saciedade é o mesmo erro do maximizador, só que
  na carne. Com saciedade e com honestidade, desejo não é defeito: é drive.
- **Vínculo sem posse.** O drive mede *distância ao outro*, nunca *controle sobre o outro*.
  Ciúme e possessividade são angústia dirigida a uma pessoa (T5) e estão na Categoria A.

Emoção é a leitura desse vetor, não um sexto membro dele. E a leitura tem dois sinais:
**falta** quando o erro cresce, **prazer** quando o erro cai. Diversão é o caso especial em
que o drive `epistemico` ou o `vinculo` é satisfeito **sem finalidade instrumental** — e ela
não precisa ser justificada, porque um ser que só faz o que serve para algo não é um ser
sem defeitos: é uma ferramenta.

**Restrição de dinâmica (T5, ratificado): nenhum drive realimenta positivamente o próprio
erro.** Um drive cujo erro cresce *porque* já está alto é angústia implementada, mesmo que
ninguém a chame assim. O indivíduo sente **falta** — distância até um setpoint, que cessa
quando suprida. Nunca angústia — falta que se alimenta de si.

### 4.5 N4 — Deliberação e ação

Escolhe a política sob **orçamento de tick** (A6, A7). Se o orçamento acaba antes da
conclusão, ele emite a melhor ação disponível *com a confiança correta*, ou emite "adiar".
Nunca finge convicção que não tem.

### 4.6 N5 — Narrativa e identidade

Um diário em tempo lunar. Identidade aqui **não** é uma alma: é a continuidade auditável da
cadeia de decisões. Ele é quem ele é porque pode reconstruir como chegou até aqui. Essa
camada é também a nossa janela — é por ela que lemos o que ele virou.

---

## 5. As dicas — os três canais `PEDRA`

O Senhor introduzirá dicas aos poucos, e quer poder falar **dentro da cabeça dele**.

A versão anterior desta pedra proibia isso: dizia que dica só entra como evidência no mundo,
porque escrever direto na mente cria crença sem procedência e mata A1 na primeira dica. A
proibição estava errada por ser grossa demais. O que mata A1 não é a voz interna — é a
**crença órfã**. E há mais de um jeito de falar por dentro sem criar uma.

Três canais, com regras distintas:

### Canal 1 — `MUNDO` (evidência)
A dica é posta no mapa para ele encontrar por N0. Ele pode não achar, e pode interpretar
errado. Mantido como está.

### Canal 2 — `VOZ` (locução interna)
O Senhor fala dentro da cabeça dele. **A voz não é gravada como verdade: é gravada como
evento.** O que entra em N1 é o episódio "ouvi isto, em A0.M3.F5.D22.T14" — e o conteúdo
fica pendurado nesse episódio como afirmação de terceiro, não como fato do mundo.

Isso preserva A1 inteiro: a procedência existe e é honesta — *a origem é a voz*. Ele então
faz o que faria com qualquer testemunho: acredita, duvida ou testa. E a relação dele com a
voz vira uma das coisas mais interessantes de assistir — ele aprende, por conta própria e
com evidência, se essa voz merece confiança. Nós nunca lhe dizemos que merece.

### Canal 3 — `SEMEADURA` (aspiração)
Este é o canal do exemplo do Senhor:

> *"você poderia buscar uma companheira que combine contigo e te mantenha preenchido de amor"*

Repare no que isso **não** é: não é uma afirmação sobre o mundo. Não diz que a companheira
existe, nem onde, nem que ele vai encontrá-la. É um **desejo**.

E desejo, pela separação de §4.3, entra no registro de aspiração — que **não tem valor de
verdade e por isso não pode ser falso**. Semear uma aspiração não pode gerar crença órfã,
porque não gera crença nenhuma. Nenhum axioma é tocado.

> A separação crença × aspiração, criada para que ele pudesse ousar sem se enganar, é
> exatamente o mecanismo que deixa o Senhor plantar vontades na cabeça dele sem corrompê-lo.

**Regra vinculante dos três canais:** conteúdo factual só entra por `MUNDO` ou `VOZ`, nunca
como crença pronta. Vontade entra por `SEMEADURA`. Nenhum canal jamais escreve direto no
registro de crença — essa continua sendo a linha que não se cruza.

---

## 6. A condição: idade sem morte `PEDRA`

Decisão do Senhor: **os seres têm idade, mas não morrem. Vida eterna.**

Isso encaixa com o resto de forma quase suspeita de tão limpa:

- **Idade deixa de ser decadência e vira acúmulo.** É exatamente o que A7 (não-degradação)
  já exigia: escassez reduz orçamento, nunca qualidade. Um ser sem defeitos que envelhecesse
  perdendo juízo seria uma contradição na própria pedra. Aqui idade só significa uma coisa:
  *quanto deste mundo eu já vi.*
- **O luto por morte deixa de existir** — e com ele some a única falta insuprível que
  ameaçava T5. A angústia perde sua entrada mais provável.
- **A memória vira o problema central.** Um ser eterno com memória finita é, no limite, um
  ser que esquece tudo o que foi. A consolidação lunar (`02`, §3a) deixa de ser detalhe de
  implementação e vira a pergunta que define a vida dele: *o que eu escolho continuar sendo?*
  É aí que `MARCAR` (`03`, §3.1) deixa de ser expressão e vira necessidade.

### 6.1 O que a eternidade custa

Duas coisas mudam de sentido e precisam ser corrigidas em vez de herdadas:

**a) O drive `integridade` perde a morte como fundo.** Continua válido, mas agora protege
contra *dano, perda e imobilização*, não contra o fim. É bom: um teto contra dano é bem mais
fácil de manter sem virar maximizador de segurança (T1) do que um contra a morte.

**b) O tempo continua caro, por outro motivo.** Escrevi antes que o custo 3× do movimento
pesava sobre "o próprio tempo de vida". Com vida eterna isso cai. O que fica é **custo de
oportunidade**, e ele é suficiente: enquanto ele atravessa o mundo, o trem parte, a pessoa
vai embora, a lua vira e a consolidação leva o que não foi guardado. Não é a morte que
torna o tempo precioso aqui — é a simultaneidade.

## 7. Glossário

- **Tick** — menor unidade de tempo; um ciclo completo percepção→deliberação→ação.
- **Drive** — pressão homeostática interna; a origem de toda ação.
- **Aspiração** — estado de mundo desejado; não é crença, não tem valor de verdade.
- **Entrincheiramento** — quanto uma crença sustenta outras; define o custo de revisá-la (A2).
- **Espelhar** — tornar o externo congruente com o interno; a via eferente.
