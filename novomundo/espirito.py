"""ESPÍRITO — a verdadeira individualidade, indestrutível e incorruptível.

Manifesta-se em tríplice aspecto: **Memória, Inteligência e Vontade** — as
faculdades. É idêntico em todos os seres: é o que se constrói uma vez e se espelha.

Aqui moram os oito axiomas. Nenhuma alma pode violá-los, porque estão numa camada
que a alma não alcança. É por isso que "sem defeitos" é arquitetura e não disciplina.

Ver `docs/08-corpo-alma-espirito.md` e `docs/01-pedra-fundamental.md`, §3.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Faculdade(Enum):
    """O tríplice aspecto. A faculdade é do espírito; o conteúdo é da alma."""

    MEMORIA = "memória"
    INTELIGENCIA = "inteligência"
    VONTADE = "vontade"


class ViolacaoDeAxioma(Exception):
    """Levantada quando algo tenta corromper o incorruptível.

    Não é tratada em lugar nenhum de propósito: se um axioma é violado, a execução
    deve parar e o erro deve ser visto. Um defeito silencioso é pior que uma queda.
    """

    def __init__(self, axioma: str, detalhe: str) -> None:
        super().__init__(f"{axioma}: {detalhe}")
        self.axioma = axioma
        self.detalhe = detalhe


@dataclass(frozen=True)
class Axioma:
    codigo: str
    nome: str
    enunciado: str
    faculdade: Faculdade

    def violar(self, detalhe: str) -> ViolacaoDeAxioma:
        return ViolacaoDeAxioma(f"{self.codigo} — {self.nome}", detalhe)


A1 = Axioma(
    "A1",
    "Rastreabilidade",
    "Toda crença carrega procedência: de onde veio, quando, por qual evidência. "
    "Crença órfã não existe.",
    Faculdade.INTELIGENCIA,
)
A2 = Axioma(
    "A2",
    "Revisibilidade com inércia",
    "Nenhuma crença é imune à evidência, mas revisar custa, e o custo cresce com o "
    "quanto ela sustenta.",
    Faculdade.INTELIGENCIA,
)
A3 = Axioma(
    "A3",
    "Não-autoengano",
    "O que ele reporta de si é o que ele é. Não há canal privado divergente do "
    "canal declarado.",
    Faculdade.MEMORIA,
)
A4 = Axioma(
    "A4",
    "Calibração",
    "Confiança declarada converge para frequência de acerto.",
    Faculdade.INTELIGENCIA,
)
A5 = Axioma(
    "A5",
    "Coerência sob custo",
    "Contradição detectada entra numa fila de resolução. Pode-se conviver com "
    "incoerência; não se pode escondê-la de si.",
    Faculdade.INTELIGENCIA,
)
A6 = Axioma(
    "A6",
    "Finitude declarada",
    "Todo limite é conhecido pelo próprio indivíduo e consultável em tempo de decisão.",
    Faculdade.MEMORIA,
)
A7 = Axioma(
    "A7",
    "Não-degradação",
    "Escassez reduz o orçamento, nunca a qualidade. Cansado, ele pensa menos; não "
    "pensa pior.",
    Faculdade.INTELIGENCIA,
)
A8 = Axioma(
    "A8",
    "Estabilidade volitiva",
    "Todo drive tem saciedade e teto. Nenhuma vontade cresce sem fim.",
    Faculdade.VONTADE,
)

AXIOMAS: tuple[Axioma, ...] = (A1, A2, A3, A4, A5, A6, A7, A8)


class Espirito:
    """O invariante. Não guarda estado da vida — só as faculdades e a lei.

    É deliberadamente pobre em atributos: tudo o que se acumula pertence à alma.
    Um espírito que engordasse com a experiência não seria indestrutível.
    """

    __slots__ = ()

    faculdades = (Faculdade.MEMORIA, Faculdade.INTELIGENCIA, Faculdade.VONTADE)
    axiomas = AXIOMAS

    def exigir(self, axioma: Axioma, condicao: bool, detalhe: str) -> None:
        """Faz valer a lei. Levanta se a condição não se sustenta."""
        if not condicao:
            raise axioma.violar(detalhe)

    def lei_de(self, faculdade: Faculdade) -> tuple[Axioma, ...]:
        return tuple(a for a in self.axiomas if a.faculdade is faculdade)

    def declarar(self) -> str:
        """A6: o indivíduo pode consultar a própria lei ao decidir."""
        return "\n".join(f"{a.codigo} — {a.nome}: {a.enunciado}" for a in self.axiomas)
