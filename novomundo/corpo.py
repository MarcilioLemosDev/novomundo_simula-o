"""CORPO — o instrumento que toca o mundo.

Percepção com raio finito, os cinco verbos, o relógio próprio com o 3× do
movimento, o sexo e a gestação de nove meses lunares.

O corpo não morre (`01`, §6). O que ele impõe é limite, não fim — e todo limite é
declarado e conhecido pelo dono (A6).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

from .espirito import A6, A7, Espirito
from .temperamento import Sexo
from .tempo import TICKS_DE_GESTACAO, DILATACAO_MOVIMENTO, Instante, RelogioProprio

RAIO_BASE = 2
RAIO_EXTRA_LUA_CHEIA = 3


class Verbo(Enum):
    """Os cinco verbos do escopo inicial (`03`, §3)."""

    MOVER = "andar"
    OLHAR = "olhar"
    COLETAR = "prover-se"
    MARCAR = "marcar"
    ESPERAR = "esperar"
    EMBARCAR = "embarcar"
    LER = "ler"
    CONTEMPLAR = "contemplar"
    DIVERTIR = "divertir-se"

    @property
    def custa_dilatado(self) -> bool:
        """Andar faz o tempo correr 3×. O trem, não — é o que ele compra de volta."""
        return self is Verbo.MOVER


@dataclass(frozen=True)
class Acao:
    verbo: Verbo
    alvo: str | None = None
    porque: str = ""
    custo_ticks: int = 1
    dilatado: bool | None = None

    @property
    def dilata(self) -> bool:
        """O trem declara `dilatado=False`: viajar nele não cobra o triplo."""
        return self.verbo.custa_dilatado if self.dilatado is None else self.dilatado

    @property
    def ticks(self) -> int:
        return self.custo_ticks * (DILATACAO_MOVIMENTO if self.dilata else 1)


@dataclass(frozen=True)
class Sensacao:
    """O que chegou pela janela, tipado e datado. Nada entra sem carimbo de tempo."""

    tipo: str
    conteudo: str
    onde: tuple[int, int]
    quando: Instante
    nitidez: float


@dataclass
class Gestacao:
    """Nove meses lunares, medidos no relógio do **mundo** e não no dela.

    Gestação é biologia do mundo, não contagem própria. Consequência correta e
    divertida: uma mulher que viaja muito, com o tempo correndo 3×, vive a própria
    gravidez como mais curta do que ela é (`07`, §7).
    """

    concebida_em: Instante
    do_pai: str

    def pronta(self, agora: Instante) -> bool:
        return agora.tick - self.concebida_em.tick >= TICKS_DE_GESTACAO

    def falta(self, agora: Instante) -> int:
        return max(0, TICKS_DE_GESTACAO - (agora.tick - self.concebida_em.tick))


class Corpo:
    """O corpo de um indivíduo. Difere por sexo; sujeito ao 3× do movimento."""

    def __init__(
        self,
        espirito: Espirito,
        sexo: Sexo,
        nascimento: Instante,
        posicao: tuple[str, str] = ("Brasília", "Praça de Brasília"),
        orcamento_atencao: int = 8,
    ) -> None:
        self._espirito = espirito
        self.sexo = sexo
        self.posicao = posicao
        self.relogio = RelogioProprio(nascimento)
        self.orcamento_atencao = orcamento_atencao
        self.gestacao: Gestacao | None = None
        self.energia: float = 1.0

    # -------------------------------------------------------------- percepção

    def raio(self, agora: Instante) -> int:
        """Varia com a fase da lua: cheia enxerga longe, nova enxerga perto."""
        return RAIO_BASE + int(agora.luminosidade * RAIO_EXTRA_LUA_CHEIA)

    def perceber(self, mundo, agora: Instante) -> list[Sensacao]:
        """Amostra o mundo pela janela finita. O que não alcança, ele não sabe —
        e sabe que não sabe.

        O corpo não interpreta o mapa: pergunta ao mundo o que se vê de onde ele
        está. A posição é um símbolo que só o mundo entende, e por isso trocar a
        grade abstrata pelas capitais reais não custou uma linha da alma.
        """
        return mundo.perceber(self.posicao, self.raio(agora), agora)

    def olhar_fundo(self, mundo, agora: Instante) -> list[Sensacao]:
        """OLHAR: alcançar além do que a janela passiva mostra."""
        return mundo.olhar_alem(self.posicao, agora)

    # ------------------------------------------------------------------ agir

    def agir(self, acao: Acao) -> int:
        """Executa e consome tempo próprio. Devolve os ticks próprios gastos."""
        gastos = self.relogio.viver(acao.custo_ticks, movendo=acao.dilata)
        # A7: escassez reduz o orçamento, nunca a qualidade.
        self.energia = max(0.0, self.energia - (0.03 if acao.dilata else 0.005))
        return gastos

    @property
    def atencao_disponivel(self) -> int:
        """A7: cansado, ele pensa **menos** — não pior."""
        return max(1, int(self.orcamento_atencao * max(0.25, self.energia)))

    def descansar(self) -> None:
        """Parar repõe o orçamento. Nunca repõe a qualidade, porque ela não caiu (A7)."""
        self.energia = min(1.0, self.energia + 0.08)

    # ------------------------------------------------------------- reprodução

    def conceber(self, do_pai: str, agora: Instante) -> Gestacao:
        if self.sexo is not Sexo.MULHER:
            raise ValueError("só a mulher gesta")
        if self.gestacao is not None:
            raise ValueError("já está gestando")
        self.gestacao = Gestacao(concebida_em=agora, do_pai=do_pai)
        return self.gestacao

    def dar_a_luz(self, agora: Instante) -> Gestacao | None:
        if self.gestacao is None or not self.gestacao.pronta(agora):
            return None
        parto, self.gestacao = self.gestacao, None
        return parto

    # ------------------------------------------------------------------- A6

    def limites(self, agora: Instante) -> str:
        return (
            f"{self.sexo.value} · em {self.posicao[1]}, {self.posicao[0]} · "
            f"enxergo até {self.raio(agora)} destinos daqui · "
            f"atenção {self.atencao_disponivel}/{self.orcamento_atencao} · "
            f"energia {self.energia:.0%} · "
            f"idade {self.relogio.idade_em_anos:.2f} anos lunares"
        )

    def auditar(self, agora: Instante) -> None:
        self._espirito.exigir(A6, self.raio(agora) > 0, "raio de percepção nulo")
        self._espirito.exigir(
            A7, self.atencao_disponivel >= 1, "a escassez zerou a atenção em vez de reduzi-la"
        )
