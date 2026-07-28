"""O compromisso — o que dá forma a um dia que cabe tudo.

> *"No dia dele tem tempo a tudo. Introduzir um escopo obrigatório de buscar
> conhecimento, duas horas semanais de trabalho digamos, e o resto livre."*

Num ser eterno e sem escassez, o dia não tem aperto: cabe tudo. Isso é bonito e é um
problema — sem nenhuma forma, o tempo vira massa informe.

Mas repare no que o compromisso **não** é: não é uma regra que o obrigue. Uma regra
que o obrigasse quebraria o livre arbítrio, e o livre arbítrio é a pedra. É um
**acordo que ele carrega**, e ele pode não cumprir.

E o que acontece quando não cumpre não é culpa:

> **Obrigação aqui é coerência, nunca culpa.**

Um ser sem defeitos não se pune. Ele nota a distância entre o que disse que faria e o
que fez — e isso é uma incoerência como qualquer outra, que vai para a fila de A5 e
pesa no drive `coerencia` até ser resolvida ou revista.

Ver `docs/09-recompensa-real-e-o-amor.md`, §1.
"""

from __future__ import annotations

from dataclasses import dataclass

from .tempo import TICKS_POR_DIA, Instante

#: Uma semana lunar é uma fase: 1/8 do mês sinódico.
TICKS_POR_SEMANA = int(29.53059 * TICKS_POR_DIA / 8)


@dataclass
class Compromisso:
    """O que ele se comprometeu a fazer, e quanto ainda deve neste ciclo."""

    o_que: str
    verbo: str
    horas_por_semana: int
    assumido_em: Instante
    cumprido_no_ciclo: int = 0
    ciclo: int = 0

    def virar_semana(self, agora: Instante) -> bool:
        """Fecha o ciclo se a semana lunar virou. Devolve se ficou devendo."""
        ciclo_agora = (agora.tick - self.assumido_em.tick) // TICKS_POR_SEMANA
        if ciclo_agora == self.ciclo:
            return False
        ficou_devendo = self.cumprido_no_ciclo < self.horas_por_semana
        self.ciclo = ciclo_agora
        self.cumprido_no_ciclo = 0
        return ficou_devendo

    def cumprir(self, acao) -> bool:
        if self.serve(acao):
            self.cumprido_no_ciclo += 1
            return True
        return False

    def serve(self, acao) -> bool:
        return acao.verbo.value == self.verbo

    @property
    def faltando(self) -> int:
        return max(0, self.horas_por_semana - self.cumprido_no_ciclo)

    @property
    def devendo(self) -> bool:
        return self.faltando > 0

    def __str__(self) -> str:
        return f"{self.o_que} — {self.cumprido_no_ciclo}/{self.horas_por_semana} nesta semana"


def duas_horas_de_estudo(agora: Instante) -> Compromisso:
    """O escopo obrigatório do Senhor: duas horas semanais de busca de conhecimento."""
    return Compromisso(
        o_que="buscar conhecimento duas horas por semana",
        verbo="ler",
        horas_por_semana=2,
        assumido_em=agora,
    )
