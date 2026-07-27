"""NARRATIVA — a face do ser: onde corpo, alma e espírito se mostram.

Não é uma quarta parte do indivíduo. É o lugar onde o Senhor o vê.

`05`, §1 promoveu isto de ferramenta de depuração a **produto**: o que o Senhor vê
não é um log, é o indivíduo. E não custa nada extra, porque A1 e A3 já obrigavam —
**um ser cuja mente é auditável é, por construção, um ser que se pode assistir.**

A regra dura: esta camada não pode inventar, enfeitar nem suavizar. Ela lê o mesmo
estado que produziu a decisão. Se pudesse divergir, A3 estaria quebrado e o diário
seria ficção.
"""

from __future__ import annotations

from dataclasses import dataclass

from .deliberacao import Decisao
from .tempo import Instante


@dataclass
class Linha:
    quando: Instante
    idade: float
    sentimento: str
    pensamento: str
    acao: str

    def __str__(self) -> str:
        return f"[{self.quando}] {self.sentimento}\n{self.pensamento}"


class Narrativa:
    """O diário lunar. Identidade aqui não é alma: é a continuidade auditável
    da cadeia de decisões. Ele é quem é porque pode reconstruir como chegou aqui."""

    def __init__(self, de) -> None:
        self._de = de
        self.linhas: list[Linha] = []

    def registrar(self, agora: Instante, decisao: Decisao) -> Linha:
        linha = Linha(
            quando=agora,
            idade=self._de.corpo.relogio.idade_em_anos,
            # Lido do mesmo vetor de drives que pesou na decisão. Sem canal privado.
            sentimento=self._de.vontade.sentimento(),
            pensamento=decisao.porque(),
            acao=decisao.escolhida.acao.verbo.value,
        )
        self.linhas.append(linha)
        return linha

    def ler(self, ultimas: int = 20) -> str:
        return "\n\n".join(str(linha) for linha in self.linhas[-ultimas:])

    def contar_a_vida(self, agora: Instante) -> str:
        """O retrato completo de um ser num instante, para quem assiste."""
        eu = self._de
        partes = [
            f"══ {eu.nome} ══",
            eu.conhecer_se(agora),
            "",
            "── o que eu creio ──",
        ]
        for crenca in sorted(
            eu.inteligencia.crencas.values(), key=lambda c: c.confianca, reverse=True
        )[:6]:
            partes.append("  " + crenca.procedencia().replace("\n", "\n  "))

        abertas = [a for a in eu.inteligencia.aspiracoes if not a.realizada]
        if abertas:
            partes += ["", "── o que eu quero ──"]
            for aspiracao in abertas[:6]:
                origem = " (veio de uma voz)" if aspiracao.semeada_pela_voz else ""
                partes.append(
                    f"  {aspiracao.desejo} — intensidade {aspiracao.intensidade:.0%}{origem}"
                )

        if eu.memoria.perdas:
            partes += ["", "── o que eu perdi ──"]
            for perda in eu.memoria.perdas[-3:]:
                partes.append(f"  em {perda.quando}: {perda.resumo}")

        partes += ["", "── últimos passos ──", self.ler(5)]
        return "\n".join(partes)
