"""Arquétipos, temperamentos e signo.

A regra que sustenta tudo: **temperamento parametriza, nunca corrompe.** Nenhum
signo suspende um axioma. E o indivíduo conhece o próprio temperamento (A6) —
viés declarado é personalidade, viés oculto é defeito.

Ver `docs/07-arquetipos-e-temperamentos.md`.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

# Faixas que os axiomas permitem. Nenhum temperamento pode sair delas: fixo demais
# é ancoragem irreversível (Categoria A), mutável demais é a oscilação que A2 existe
# para impedir.
GANHO_MIN, GANHO_MAX = 0.4, 1.6
ENTRINCHEIRAMENTO_MIN, ENTRINCHEIRAMENTO_MAX = 0.5, 2.0
LIMIAR_RISCO_MIN, LIMIAR_RISCO_MAX = 0.05, 0.45


class Elemento(Enum):
    """Inclina os ganhos dos drives. Nenhum elemento zera drive nenhum."""

    FOGO = "fogo"
    TERRA = "terra"
    AR = "ar"
    AGUA = "agua"


class Modalidade(Enum):
    """É, literalmente, o entrincheiramento de A2."""

    CARDEAL = "cardeal"
    FIXO = "fixo"
    MUTAVEL = "mutavel"


class Sexo(Enum):
    HOMEM = "homem"
    MULHER = "mulher"


class Signo(Enum):
    ARIES = ("Áries", Elemento.FOGO, Modalidade.CARDEAL)
    TOURO = ("Touro", Elemento.TERRA, Modalidade.FIXO)
    GEMEOS = ("Gêmeos", Elemento.AR, Modalidade.MUTAVEL)
    CANCER = ("Câncer", Elemento.AGUA, Modalidade.CARDEAL)
    LEAO = ("Leão", Elemento.FOGO, Modalidade.FIXO)
    VIRGEM = ("Virgem", Elemento.TERRA, Modalidade.MUTAVEL)
    LIBRA = ("Libra", Elemento.AR, Modalidade.CARDEAL)
    ESCORPIAO = ("Escorpião", Elemento.AGUA, Modalidade.FIXO)
    SAGITARIO = ("Sagitário", Elemento.FOGO, Modalidade.MUTAVEL)
    CAPRICORNIO = ("Capricórnio", Elemento.TERRA, Modalidade.CARDEAL)
    AQUARIO = ("Aquário", Elemento.AR, Modalidade.FIXO)
    PEIXES = ("Peixes", Elemento.AGUA, Modalidade.MUTAVEL)

    def __init__(self, rotulo: str, elemento: Elemento, modalidade: Modalidade) -> None:
        self.rotulo = rotulo
        self.elemento = elemento
        self.modalidade = modalidade

    @classmethod
    def do_indice(cls, indice: int) -> "Signo":
        return list(cls)[indice % 12]


# Elemento -> ganho por drive. Todos os cinco existem em todos; o que muda é o peso.
_INCLINACAO_ELEMENTO: dict[Elemento, dict[str, float]] = {
    Elemento.FOGO: {"epistemico": 1.0, "coerencia": 0.8, "expressao": 1.5, "integridade": 0.7, "vinculo": 1.0},
    Elemento.TERRA: {"epistemico": 0.9, "coerencia": 1.2, "expressao": 0.8, "integridade": 1.5, "vinculo": 0.9},
    Elemento.AR: {"epistemico": 1.5, "coerencia": 1.3, "expressao": 1.0, "integridade": 0.8, "vinculo": 1.0},
    Elemento.AGUA: {"epistemico": 1.0, "coerencia": 0.9, "expressao": 1.0, "integridade": 0.9, "vinculo": 1.5},
}

# Modalidade -> (entrincheiramento, facilidade de formar crença nova).
_INCLINACAO_MODALIDADE: dict[Modalidade, tuple[float, float]] = {
    Modalidade.CARDEAL: (1.0, 1.4),  # forma fácil, abandona direção com dificuldade
    Modalidade.FIXO: (1.8, 0.8),  # sustenta, aprofunda, revisa devagar e caro
    Modalidade.MUTAVEL: (0.6, 1.2),  # adapta, reconfigura, revisa rápido e barato
}


def _travar(valor: float, minimo: float, maximo: float) -> float:
    return max(minimo, min(maximo, valor))


@dataclass(frozen=True)
class Temperamento:
    """O vetor de parâmetros que faz de duas instâncias do mesmo modelo duas pessoas.

    É dado ao construir o indivíduo. Não há código diferente por signo — há um
    `Temperamento` diferente. É assim que "constrói-se um e espelha-se" se cumpre
    ao pé da letra.
    """

    signo: Signo
    ganhos: dict[str, float] = field(default_factory=dict)
    entrincheiramento: float = 1.0
    facilidade_de_crer: float = 1.0
    limiar_risco: float = 0.25
    orcamento_atencao: int = 8

    @classmethod
    def do_signo(cls, signo: Signo) -> "Temperamento":
        ganhos = {
            nome: _travar(valor, GANHO_MIN, GANHO_MAX)
            for nome, valor in _INCLINACAO_ELEMENTO[signo.elemento].items()
        }
        entrincheiramento, facilidade = _INCLINACAO_MODALIDADE[signo.modalidade]

        # Fogo arrisca mais; terra, menos. Sempre dentro da faixa que A6 e T1 permitem.
        risco_base = {
            Elemento.FOGO: 0.40,
            Elemento.AR: 0.28,
            Elemento.AGUA: 0.20,
            Elemento.TERRA: 0.12,
        }[signo.elemento]

        return cls(
            signo=signo,
            ganhos=ganhos,
            entrincheiramento=_travar(entrincheiramento, ENTRINCHEIRAMENTO_MIN, ENTRINCHEIRAMENTO_MAX),
            facilidade_de_crer=facilidade,
            limiar_risco=_travar(risco_base, LIMIAR_RISCO_MIN, LIMIAR_RISCO_MAX),
            orcamento_atencao=8,
        )

    def ganho(self, drive: str) -> float:
        return self.ganhos.get(drive, 1.0)

    def descrever(self) -> str:
        """O que ele sabe sobre si mesmo (A6). Ele pode ler isto ao decidir."""
        return (
            f"{self.signo.rotulo} · {self.signo.elemento.value}/{self.signo.modalidade.value} · "
            f"revisão custa {self.entrincheiramento:.1f}x · "
            f"aceito risco até {self.limiar_risco:.0%} · "
            f"atenção {self.orcamento_atencao} por tick"
        )
