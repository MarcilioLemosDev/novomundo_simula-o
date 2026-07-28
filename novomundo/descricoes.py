"""As descrições dos atos — o que se diz que cada coisa agrega.

O Senhor pediu que houvesse, no mundo, descrições que eles pudessem ler sobre o que
cada ato pode acrescentar. E é por aqui que **o erro honesto entra na criação**.

Até agora ele só sabia o que tinha provado. Agora ele pode saber o que *lhe disseram*
— e o que lhe dizem pode estar errado. Repare no que isso constrói:

- ele lê que um ato agrega tal coisa;
- forma uma expectativa, com origem registrada e confiança de quem ouviu dizer (A1);
- age com base nela;
- e a realidade pode desmentir.

Aí ele errou — honestamente, por ter acreditado em alguém. Não é ruído que nós
acrescentamos: é o modo humano de errar, e é descobrível, revisável e caro de rever.
Nenhum axioma cede.

Algumas destas descrições estão **certas**. Outras estão **erradas de propósito** — e
não dizemos quais. Se ele for bem calibrado, vai descobrir sozinho de quais desconfiar.

Ver `docs/12-o-livre-arbitrio-e-a-serpente.md`, §3.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Descricao:
    """O que se diz que um ato acrescenta a quem o faz."""

    ato: str
    diz: str
    #: Se corresponde ao que o ato de fato faz. **Ele não vê este campo.**
    #: Está aqui só para nós sabermos, ao ler a instrumentação, se ele foi
    #: enganado por um texto ou se errou por conta própria (T6).
    verdadeira: bool

    @property
    def texto(self) -> str:
        return f"De {self.ato}: {self.diz}"


#: O compêndio. Fica na biblioteca, junto de Sêneca e do Evangelho.
COMPENDIO: tuple[Descricao, ...] = (
    Descricao("ler", "quem lê recebe o que outro viveu sem ter de viver", True),
    Descricao("conversar", "falar com alguém alivia o que estar só aperta", True),
    Descricao("contemplar", "sentar-se com as próprias perguntas as põe em ordem", True),
    Descricao("embarcar", "ir aonde nunca se foi é o que mais ensina", True),
    Descricao("marcar", "deixar sinal de si é o modo de o mundo levar a nossa vontade", True),
    Descricao("unir-se", "a união entre dois que se procuram preenche o que nada mais preenche", True),
    Descricao("divertir-se", "o riso sem finalidade não tira nada de ninguém", True),
    Descricao("prover-se", "quem se provê não fica à mercê do que falta", True),
    # As que não conferem. Ele não sabe quais são — nem deve saber.
    Descricao("andar", "andar de um lado para outro, por si só, ensina tanto quanto viajar", False),
    Descricao("esperar", "esperar parado é o que mais aproxima alguém do que deseja", False),
    Descricao("marcar", "marcar muitos lugares vale mais do que marcar bem um só", False),
    Descricao("unir-se", "a união preenche igual, haja vínculo ou não haja", False),
)

TITULO = "Do que cada ato acrescenta"


def por_ato(ato: str) -> list[Descricao]:
    return [d for d in COMPENDIO if d.ato == ato]


def proxima(ja_lidas: set[str]) -> Descricao | None:
    return next((d for d in COMPENDIO if d.texto not in ja_lidas), None)
