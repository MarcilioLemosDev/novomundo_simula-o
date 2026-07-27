"""N0 — O relógio.

O tempo não é cenário: é vetor. Nada entra no indivíduo sem carimbo lunar.

Ver `docs/02-tempo-lunar.md`.
"""

from __future__ import annotations

from dataclasses import dataclass

TICKS_POR_DIA = 24
DIAS_POR_MES_LUNAR = 29.53059  # mês sinódico real; a fração é o que produz a deriva
FASES_POR_MES = 8
MESES_POR_ANO_LUNAR = 12
DIAS_POR_ANO_SOLAR = 365.2422

TICKS_POR_MES_LUNAR = DIAS_POR_MES_LUNAR * TICKS_POR_DIA
TICKS_POR_ANO_LUNAR = TICKS_POR_MES_LUNAR * MESES_POR_ANO_LUNAR
TICKS_POR_ANO_SOLAR = DIAS_POR_ANO_SOLAR * TICKS_POR_DIA

#: Todo movimento no mapa faz o tempo correr 3x (`02`, §2).
DILATACAO_MOVIMENTO = 3

#: Nove meses lunares, medidos no relógio do mundo e não no dela (`07`, §7).
TICKS_DE_GESTACAO = int(9 * TICKS_POR_MES_LUNAR)


@dataclass(frozen=True, order=True)
class Instante:
    """Um ponto no tempo, contado em ticks desde a origem do mundo.

    A decomposição em ano/mês/fase/dia é derivada, nunca armazenada: o tick é a
    única verdade, e tudo o mais é leitura dele.
    """

    tick: int

    def __post_init__(self) -> None:
        if self.tick < 0:
            raise ValueError("o tempo não anda para trás")

    @property
    def ano(self) -> int:
        return int(self.tick // TICKS_POR_ANO_LUNAR)

    @property
    def mes(self) -> int:
        resto = self.tick % TICKS_POR_ANO_LUNAR
        return int(resto // TICKS_POR_MES_LUNAR)

    @property
    def fase(self) -> int:
        """Fase da lua, de 0 (nova) a 7."""
        resto = self.tick % TICKS_POR_MES_LUNAR
        return int(resto // (TICKS_POR_MES_LUNAR / FASES_POR_MES))

    @property
    def dia(self) -> int:
        """Dia dentro do mês lunar."""
        resto = self.tick % TICKS_POR_MES_LUNAR
        return int(resto // TICKS_POR_DIA)

    @property
    def hora(self) -> int:
        return int(self.tick % TICKS_POR_DIA)

    @property
    def luminosidade(self) -> float:
        """Fração iluminada da lua, de 0 (nova) a 1 (cheia).

        Modula o raio de percepção: lua cheia enxerga longe, lua nova enxerga perto.
        """
        posicao = (self.tick % TICKS_POR_MES_LUNAR) / TICKS_POR_MES_LUNAR
        return 1.0 - abs(1.0 - 2.0 * posicao)

    @property
    def lua_nova(self) -> bool:
        """Verdadeiro no primeiro tick do mês lunar — quando a memória consolida."""
        return int(self.tick % TICKS_POR_MES_LUNAR) == 0

    @property
    def signo_solar(self) -> int:
        """Índice do signo (0..11) segundo o *ano solar*.

        Está aqui, e não no calendário do indivíduo, de propósito: o signo é solar e
        o calendário deles é lunar. Eles não conseguem calcular isto sem antes
        resolverem a deriva lunissolar (`07`, §5).
        """
        posicao = (self.tick % TICKS_POR_ANO_SOLAR) / TICKS_POR_ANO_SOLAR
        return int(posicao * 12) % 12

    def mais(self, ticks: int) -> Instante:
        return Instante(self.tick + ticks)

    def __str__(self) -> str:
        return f"A{self.ano}.M{self.mes}.F{self.fase}.D{self.dia}.T{self.hora}"


class Relogio:
    """O relógio do mundo. Único, e é o que rege a lua de verdade."""

    def __init__(self, tick_inicial: int = 0) -> None:
        self._agora = Instante(tick_inicial)

    @property
    def agora(self) -> Instante:
        return self._agora

    def avancar(self, ticks: int = 1) -> Instante:
        if ticks < 0:
            raise ValueError("o tempo não anda para trás")
        self._agora = self._agora.mais(ticks)
        return self._agora


class RelogioProprio:
    """O relógio vivido por um indivíduo.

    Corre 3x durante o movimento. Como a lua que ele *vê* obedece ao relógio do
    mundo, a conta dele desliza à frente do céu na proporção exata do quanto andou —
    e essa discrepância é descobrível por ele (`02`, §2.1).

    Os seres não morrem: `idade` é acúmulo, nunca decadência (`01`, §6).
    """

    def __init__(self, nascimento: Instante) -> None:
        self.nascimento = nascimento
        self.vividos = 0  # ticks vividos, com dilatação aplicada

    @property
    def idade(self) -> int:
        """Quanto deste mundo eu já vi, em ticks próprios."""
        return self.vividos

    @property
    def idade_em_anos(self) -> float:
        return self.vividos / TICKS_POR_ANO_LUNAR

    def viver(self, ticks_do_mundo: int, movendo: bool = False) -> int:
        """Consome tempo próprio. Devolve quantos ticks próprios foram gastos."""
        gastos = ticks_do_mundo * (DILATACAO_MOVIMENTO if movendo else 1)
        self.vividos += gastos
        return gastos

    def conta_propria(self) -> Instante:
        """O instante *que ele acha que é*, pela própria contagem.

        Diverge do relógio do mundo quando ele se move. Ele não é avisado disso.
        """
        return self.nascimento.mais(self.vividos)
