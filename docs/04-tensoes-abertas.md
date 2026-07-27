# 04 — Tensões Abertas

O que ainda **não** sobreviveu ao estresse. Nada aqui vira código na Etapa 2 antes de ser
resolvido e promovido a `PEDRA`.

---

## T1 — Sem medo, o que impede a autodestruição? `TENSÃO`

O medo foi cortado como afeto (§2.3 da pedra). Mas o medo é o que segura um humano na
beira do penhasco. O substituto proposto é o drive `integridade`: preservação calculada,
não sentida.

**O problema:** todo drive de sobrevivência, se tiver ganho suficiente para funcionar,
tende a gerar acumulação e aversão a risco — e um indivíduo que evita risco não explora, e
um que não explora não busca conhecimento. Ou seja: T1 briga diretamente com a definição do
Senhor.

**Encaminhamento proposto:** `integridade` não é um drive competindo por espaço no vetor —
é uma **restrição rígida (teto) sobre as ações dos outros três**. Ele não *quer* sobreviver;
ele simplesmente não emite ações cuja probabilidade estimada de dano ultrapasse um limiar
conhecido por ele. Isso preserva a exploração, respeita A6 (o limiar é declarado) e não
cria um maximizador de segurança.

---

## T2 — Calibração perfeita mata a ousadia? `RESOLVIDO — ratificar`

Um agente que nunca se engana sobre probabilidades nunca tenta o improvável.

Resolvido em §4.3 pela separação **crença × aspiração**. A crença permanece honesta em 5%;
a aspiração não tem valor de verdade e por isso pode puxar a ação. Ele arrisca sem mentir.

Registrado aqui porque é a peça de engenharia mais delicada da pedra e precisa de
ratificação explícita antes de virar `PEDRA`.

---

## T3 — Quanto de "neural" é neural? `TENSÃO — decisão do Senhor`

"Modelo neural" ainda está indefinido, e a escolha muda tudo na Etapa 2:

- **(a) Simbólico-cognitivo** — N0–N5 como estruturas explícitas (grafos, tuplas, filas).
  A1 (rastreabilidade) e A3 (não-autoengano) saem quase de graça, porque tudo é inspecionável.
  Risco: comportamento pode ficar mecânico, sem a riqueza que se espera de algo "espelhado
  no humano".

- **(b) Conexionista** — redes de verdade, representação distribuída aprendida.
  Mais fiel ao nome. Mas A1 e A3 ficam **muito** difíceis: uma rede não tem procedência
  nativa, e "não mentir para si" é quase inverificável num espaço latente.

- **(c) Híbrido** — substrato conexionista para percepção e reconhecimento de padrão (N0,
  parte de N1), esqueleto simbólico auditável para crença, drive e decisão (N2–N5).

**Minha recomendação: (c).** É a única que honra o nome "neural" sem tornar os axiomas
inverificáveis. A auditabilidade não é um luxo aqui — é o que distingue "sem defeitos" de
"defeitos que não conseguimos ver".

---

## T4 — Um indivíduo ou uma espécie? `TENSÃO — decisão do Senhor`

Com um só indivíduo não há linguagem, não há cultura, não há outro para espelhar. "Espelhar
no externo suas próprias vontades" vira engenharia solitária — legítimo, mas é metade do
que a frase pode significar.

Com dois ou mais, aparece o problema mais rico do projeto: **um indivíduo sem defeitos
precisa modelar outro indivíduo**, e aí nascem confiança, mentira (que ele não pode
cometer — A3 —, mas pode *sofrer*), e a possibilidade de significado compartilhado nos
símbolos de `MARCAR`.

**Recomendação:** começar com **um** na Etapa 2, mas escrever N0–N5 já com a interface para
"outro agente" prevista, para que a passagem para espécie não exija reescrever a pedra.

Nota: A3 proíbe o indivíduo de mentir. Não decidimos ainda se ele deve *supor* que os
outros também não mentem. Se supuser, é ingênuo — e ingenuidade talvez seja um defeito.

---

## T5 — O sofrimento é um defeito? `TENSÃO`

Cortamos o sofrimento e mantivemos a dor como sinal. Mas parte do que move um humano a
buscar conhecimento é o desconforto de não saber — e desconforto prolongado *é* sofrimento.

Se o indivíduo nunca sofre, o drive `epistemico` precisa ser forte o bastante para
substituir aquilo sozinho. Se sofre, contradizemos "sem defeitos".

Não tenho resposta pronta. Formulação mínima que sobrevive por ora: **o indivíduo sente
falta, não angústia.** Falta é distância mensurável até um setpoint, ela cessa quando é
suprida, e ela não se realimenta sozinha. Angústia é falta que se alimenta de si — e essa
sim é defeito.

Precisa de mais estresse antes de virar pedra.

---

## T6 — Quem julga se ele está certo? `TENSÃO`

A4 exige medir calibração, e medir calibração exige uma verdade de referência. Nós temos
essa verdade (nós escrevemos o mundo). Mas se a usarmos para *corrigi-lo*, deixamos de
observar um indivíduo autônomo e passamos a treinar um aluno.

**Encaminhamento proposto:** a verdade de referência é usada **só para instrumentação**,
nunca realimentada para dentro do indivíduo. Nós sabemos se ele está bem calibrado; ele não
recebe essa nota. Ele só recebe o que o mundo devolve naturalmente — que é exatamente o que
a deriva lunar (`02`, §3) já lhe entrega de graça.
