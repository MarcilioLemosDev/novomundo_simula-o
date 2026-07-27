"""ALMA — a experiência: o que cada coisa de fato fez por mim.

Esta camada existe para tirar o **crédito** do modelo.

Antes, o mundo entregava um número por ação (`ganho=0.55`) e o indivíduo escolhia o
maior. Isso é um agente de recompensa escalar: ele não amava conhecer, amava pontos —
e um ser que persegue pontos é exatamente o maximizador que A8 foi escrito para
barrar.

Aqui a recompensa passa a ser **real e medida**: quanto uma ação de fato baixou cada
falta dele, na experiência dele. Ninguém lhe diz que ler é bom. Ele lê, sente a falta
de conhecimento ceder, e é *isso* que fica.

Consequências que valem mais que a elegância:

- **Ele nasce sem saber de nada.** Não sabe que ler ajuda, nem que a praça alegra.
  Tem de descobrir — e descobrir é a vida dele, não um pré-requisito dela.
- **O que move cada um passa a ser diferente**, mesmo com o mesmo espírito: dois seres
  com histórias distintas aprenderam coisas distintas sobre o que os preenche.
- **O livre arbítrio deixa de ser promessa.** A escolha vem da biografia, não de uma
  tabela nossa.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Marca:
    """A média corrente do que uma ação fez por uma falta."""

    soma: float = 0.0
    vezes: int = 0

    def somar(self, queda: float) -> None:
        self.soma += queda
        self.vezes += 1

    @property
    def media(self) -> float:
        return self.soma / self.vezes if self.vezes else 0.0


class Experiencia:
    """O que eu aprendi, na carne, sobre o que me faz bem.

    A chave é `(verbo, onde)` — o mesmo ato em lugares diferentes é outra coisa.
    Ler na biblioteca e ler no mercado não são a mesma experiência, e ele descobre
    isso do único jeito honesto: tentando.
    """

    def __init__(self) -> None:
        self.aprendido: dict[tuple[str, str], dict[str, Marca]] = {}

    def registrar(self, chave: tuple[str, str], quedas: dict[str, float]) -> None:
        """Guarda o que de fato caiu. Inclusive zero — descobrir que algo não
        preenche é aprendizado tão bom quanto o contrário."""
        por_drive = self.aprendido.setdefault(chave, {})
        for drive, queda in quedas.items():
            por_drive.setdefault(drive, Marca()).somar(queda)

    def conhece(self, chave: tuple[str, str]) -> bool:
        return chave in self.aprendido

    def vezes(self, chave: tuple[str, str]) -> int:
        marcas = self.aprendido.get(chave)
        return max((m.vezes for m in marcas.values()), default=0) if marcas else 0

    def esperado(self, chave: tuple[str, str]) -> dict[str, float]:
        """O que ele espera que esta ação faça — pela média do que ela já fez."""
        return {d: m.media for d, m in self.aprendido.get(chave, {}).items()}

    def o_que_me_move(self, quantos: int = 5) -> list[tuple[str, str, float]]:
        """O que este ser, por experiência própria, descobriu que o preenche.

        É a resposta à pergunta *o que move alguém pelo amor, pela diversão, pelo
        conhecimento* — e ela é diferente para cada um, porque cada um viveu outra
        coisa. Ninguém escreveu isto: ele aprendeu.
        """
        linhas = [
            (f"{verbo} em {onde}", drive, marca.media)
            for (verbo, onde), drives in self.aprendido.items()
            for drive, marca in drives.items()
            if marca.media > 0.0
        ]
        linhas.sort(key=lambda t: t[2], reverse=True)
        return linhas[:quantos]
