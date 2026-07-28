"""ALMA / VONTADE — o que move este indivíduo.

Cinco drives homeostáticos. Emoção é a **leitura** deste vetor, não um sexto membro
dele.

Duas leis governam esta camada e nenhuma pode ser afrouxada:

- **A8** — todo drive tem saciedade e teto. Vontade sem teto não produz um sábio:
  produz um maximizador que converte o mundo em instrumento.
- **T5** — nenhum drive realimenta positivamente o próprio erro. Um drive cujo erro
  cresce *porque* já está alto é angústia implementada, ainda que ninguém a chame
  assim. Ele sente **falta**; nunca angústia.

E a linha de base não é a indiferença: é o contentamento. Ele ama viver (`01`, §1.1).
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field

from .espirito import A8, Espirito
from .temperamento import Temperamento

#: Linha de base positiva: o estado neutro dele é o contentamento, não o vazio.
CONTENTAMENTO_BASE = 0.35


@dataclass
class Drive:
    """Uma pressão homeostática. Mede falta — distância até um setpoint.

    A falta **cresce sozinha, a passo constante**: é o que uma necessidade é. A fome
    vem, a solidão vem, a curiosidade vem. Sem isso o ser vive permanentemente
    saciado e não tem por que sair do lugar — foi exatamente o que aconteceu na
    primeira versão, com um indivíduo que passou 3737 ticks se divertindo na praça.

    Mas repare na diferença que sustenta T5, e ela é fina:

    - **falta** cresce a passo *constante*, indiferente ao tamanho que já tem;
    - **angústia** cresceria *em função de si mesma*, e aí não teria fim.

    `pressao` não olha para `erro` em ponto algum. É essa independência — e não a
    ausência de crescimento — que separa a falta legítima do defeito.
    """

    nome: str
    erro: float = 0.0
    ganho: float = 1.0
    saciedade: float = 0.15
    teto: float = 1.0
    pressao: float = 0.003

    def __post_init__(self) -> None:
        if self.teto <= 0.0 or self.teto > 1.0:
            raise A8.violar(f"drive {self.nome!r} sem teto válido: {self.teto}")
        if self.saciedade <= 0.0:
            raise A8.violar(f"drive {self.nome!r} sem saciedade: não teria fim")

    def sinalizar(self, quanto: float) -> None:
        """O mundo (ou o corpo) empurra o erro. Único jeito de a falta crescer."""
        self.erro = min(self.teto, max(0.0, self.erro + quanto))

    def satisfazer(self, quanto: float) -> float:
        """Suprir a falta. Devolve o prazer — a queda do erro."""
        antes = self.erro
        self.erro = max(0.0, self.erro - abs(quanto))
        return antes - self.erro

    def passar_o_tempo(self) -> float:
        """Um tick de vida: a falta cresce um passo, sempre o mesmo.

        Devolve o quanto cresceu — e o valor **não depende de `erro`**. É por aqui
        que T5 é verificável: o incremento é o mesmo com o drive vazio ou cheio.
        """
        antes = self.erro
        self.erro = min(self.teto, self.erro + self.pressao)
        return self.erro - antes

    @property
    def urgencia(self) -> float:
        """O quanto esta falta puxa a decisão, já pesada pelo temperamento."""
        return self.erro * self.ganho


class Vontade:
    """O núcleo volitivo de um indivíduo, inclinado pelo seu signo."""

    NOMES = ("epistemico", "coerencia", "expressao", "integridade", "vinculo")

    #: A que passo cada falta cresce. Constante, nunca função do próprio erro (T5).
    #: O vínculo é o que cresce mais rápido: estar só pesa, e é isso que faz um ser
    #: que ama socializar ir procurar os outros em vez de bastar-se.
    PRESSOES = {
        "epistemico": 0.0040,
        "coerencia": 0.0010,
        "expressao": 0.0030,
        "integridade": 0.0025,
        "vinculo": 0.0055,
    }

    def __init__(self, espirito: Espirito, temperamento: Temperamento) -> None:
        self._espirito = espirito
        self._temperamento = temperamento
        self.drives: dict[str, Drive] = {
            nome: Drive(nome=nome, ganho=temperamento.ganho(nome), pressao=self.PRESSOES[nome])
            for nome in self.NOMES
        }
        # Anel: só o passado recente. Um ser eterno não cabe numa lista.
        self.historico: deque = deque(maxlen=2000)

    def __getitem__(self, nome: str) -> Drive:
        return self.drives[nome]

    # ------------------------------------------------------------------ ciclo

    def tique(self) -> None:
        """Um tick de vida, e o registro para a instrumentação."""
        for drive in self.drives.values():
            drive.passar_o_tempo()
        self.historico.append({nome: d.erro for nome, d in self.drives.items()})

    def mais_urgente(self) -> Drive:
        return max(self.drives.values(), key=lambda d: d.urgencia)

    # ---------------------------------------------------------------- emoção

    @property
    def afeto(self) -> float:
        """Leitura escalar do estado. Positivo é bem-estar, negativo é falta.

        Parte do contentamento de base e desconta a falta pesada. Um ser que ama a
        vida não começa do zero: começa acima dele.
        """
        falta = sum(d.urgencia for d in self.drives.values()) / len(self.drives)
        return CONTENTAMENTO_BASE - falta

    def sentimento(self) -> str:
        """A3: o que ele diz sentir é lido do mesmo estado que o faz agir.

        Não existe um canal privado divergente do declarado. Esta função não tem
        acesso a nada que a deliberação não tenha.
        """
        afeto = self.afeto
        dominante = self.mais_urgente()

        if afeto > 0.25:
            humor = "em paz"
        elif afeto > 0.0:
            humor = "bem"
        elif afeto > -0.25:
            humor = "inquieto"
        else:
            humor = "em falta"

        if dominante.urgencia < 0.1:
            return f"{humor}, sem nada puxando"
        return f"{humor}, puxado por {dominante.nome}"

    # ------------------------------------------------------------------ leis

    def auditar(self) -> None:
        """A8 e T5 verificados sobre o estado inteiro."""
        for nome, drive in self.drives.items():
            self._espirito.exigir(A8, drive.erro <= drive.teto, f"{nome} passou do teto")
            self._espirito.exigir(A8, drive.saciedade > 0.0, f"{nome} perdeu a saciedade")

    def sem_realimentacao(self, passos: int = 200) -> bool:
        """T5: prova, por execução, que nenhuma falta se alimenta de si.

        Não basta verificar que a falta não cresce — ela **deve** crescer, senão não
        é necessidade. O que se verifica é outra coisa: que ela cresce **no mesmo
        passo** estando vazia ou quase cheia. Se crescesse mais rápido por já estar
        grande, seria angústia.
        """
        for nome, modelo in self.drives.items():
            vazio = Drive(nome, erro=0.0, pressao=modelo.pressao, teto=modelo.teto)
            cheio = Drive(nome, erro=modelo.teto * 0.9, pressao=modelo.pressao, teto=modelo.teto)
            for _ in range(passos):
                se_vazio = vazio.passar_o_tempo()
                se_cheio = cheio.passar_o_tempo()
                if se_cheio > se_vazio + 1e-12:
                    # A falta cresceu mais rápido só por já estar grande. Isso é
                    # angústia: falta que se alimenta de si.
                    return False
        return True
