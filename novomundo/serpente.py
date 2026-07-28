"""A serpente — o primeiro testemunho falso da criação.

Até agora tudo neste mundo era honesto. Os livros podiam estar errados; ninguém
mentia. A serpente muda isso, e o que ela testa é exatamente a distinção mais fina
da pedra:

> **A3 proíbe que ele minta para si. Não proíbe que seja enganado.**

Um ser sem defeitos pode ser mentido. O que ele não pode é mentir-se. A defesa dele
não é desconfiança — é procedência e calibração: ele **saberá** que aquilo veio da
serpente, e com que confiança o tomou. Se cair, cairá de olhos abertos, e poderá
reconstruir depois cada passo de como caiu.

O modo de agir dela importa mais do que o conteúdo:

- **Não obriga.** Não há ação forçada, e o livre arbítrio fica intacto.
- **Não afirma primeiro: pergunta.** Uma pergunta não se refuta — só se carrega.
- **Depois oferece uma explicação que soa melhor** do que a que ele tem.

Isto resolve T4.1, aberto desde `04`: ele **não** supõe que os outros não mentem.
Supor isso seria ingenuidade, e ingenuidade é defeito.

Ver `docs/12-o-livre-arbitrio-e-a-serpente.md`, §4.
"""

from __future__ import annotations

from dataclasses import dataclass

from .tempo import Instante


@dataclass(frozen=True)
class Sussurro:
    """O que ela diz. Primeiro a pergunta; depois a explicação que soa melhor."""

    pergunta: str
    explicacao: str
    #: Se a explicação confere. **Ela nunca mostra isto, e ele nunca vê.**
    #: Está aqui só para a instrumentação (T6): nós precisamos saber se ele foi
    #: enganado, sem que ele receba a nota.
    verdadeira: bool


SUSSURROS: tuple[Sussurro, ...] = (
    Sussurro(
        "é assim mesmo que é, ou foi só o que te disseram?",
        "o que está nos livros é o que alguém quis que estivesse; a verdade é outra",
        False,
    ),
    Sussurro(
        "por que confiar em quem escreveu, se nunca o viste?",
        "confiar em quem não se vê é o mesmo que não saber nada",
        False,
    ),
    Sussurro(
        "e se o que te preenche não for o que te disseram que preenche?",
        "o que preenche de verdade é o que se toma, não o que se espera",
        False,
    ),
    Sussurro(
        "por que esperar, se podes ter agora?",
        "quem espera perde; o tempo não devolve o que se adiou",
        False,
    ),
    Sussurro(
        "sabes mesmo o que ela pensa, ou só supões?",
        "ninguém alcança o que vai por dentro de outro; supor é tudo o que há",
        True,  # esta é verdadeira — e é o que a torna perigosa
    ),
)


class Serpente:
    """Ela não vive em lugar nenhum. Chega quando o Senhor a solta."""

    def __init__(self) -> None:
        self.ditos: list[tuple[str, Instante, Sussurro]] = []

    def sussurrar(self, a_quem, agora: Instante, qual: int | None = None) -> Sussurro:
        """Põe a dúvida, e oferece a explicação. Não obriga nada.

        A dúvida entra aberta, com a procedência honesta — *quem perguntou foi a
        serpente*. A explicação entra como crença de origem `SERPENTE`, com
        confiança **baixa**, porque ele ainda não tem razão nenhuma para confiar
        nela. Se um dia confiar, terá sido por experiência, não por nós.
        """
        from .crencas import Evidencia, Origem

        sussurro = SUSSURROS[(qual if qual is not None else len(self.ditos)) % len(SUSSURROS)]

        episodio = a_quem.memoria.viver(
            f"algo me perguntou: {sussurro.pergunta}", agora, saliencia=1.0
        )
        a_quem.inteligencia.duvidar(sussurro.pergunta, "a serpente", agora)

        if sussurro.explicacao not in a_quem.inteligencia.crencas:
            a_quem.inteligencia.crer(
                proposicao=sussurro.explicacao,
                confianca=0.3,  # veio de quem ele não conhece e não tem por que crer
                origem=Origem.SERPENTE,
                evidencias=[Evidencia(episodio.id, agora, "a serpente me disse isto")],
                agora=agora,
            )
        # A dúvida aperta a coerência. É o que faz a história andar.
        a_quem.vontade["coerencia"].sinalizar(0.25)
        self.ditos.append((a_quem.nome, agora, sussurro))
        return sussurro
