"""ESPÍRITO / INTELIGÊNCIA em ato — escolher sob orçamento, com livre arbítrio.

Duas leis mandam aqui:

- **A7** — se o orçamento acaba antes da conclusão, ele emite a melhor ação
  disponível **com a confiança correta**, ou emite `ESPERAR`. Nunca finge convicção
  que não tem, e nunca decide mal em silêncio.
- **Livre arbítrio** (`01`, §1.1) — a deliberação não é roteirizada em ponto algum.
  Não há tabela de "se X então Y". O que sai daqui é função do estado dele, e o
  estado é função da história dele. Se o comportamento for previsível a partir
  deste arquivo em vez da biografia do indivíduo, o projeto falhou.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .corpo import Acao, Verbo
from .crencas import Inteligencia
from .espirito import A7, Espirito
from .memoria import Memoria
from .tempo import Instante
from .vontades import Vontade


@dataclass
class Opcao:
    """Uma ação considerada, com o porquê à vista — é isto que o Senhor lê."""

    acao: Acao
    drive_servido: str
    ganho_esperado: float
    risco: float
    confianca: float

    @property
    def valor(self) -> float:
        return self.ganho_esperado * self.confianca


@dataclass
class Decisao:
    """O resultado de um ciclo. Guarda o descartado, não só o escolhido.

    A3 vive aqui: o relato da decisão é montado do mesmo material que a produziu.
    Não há como o diário dizer uma coisa e a escolha ter sido outra.
    """

    quando: Instante
    escolhida: Opcao
    descartadas: list[Opcao]
    atencao_gasta: int
    atencao_disponivel: int
    concluiu: bool
    pensamento: list[str] = field(default_factory=list)

    def porque(self) -> str:
        linhas = [
            f"escolhi {self.escolhida.acao.verbo.value}"
            + (f" {self.escolhida.acao.alvo}" if self.escolhida.acao.alvo else "")
            + f" — servia {self.escolhida.drive_servido}, "
            f"confiança {self.escolhida.confianca:.0%}, risco {self.escolhida.risco:.0%}"
        ]
        for opcao in self.descartadas[:3]:
            linhas.append(
                f"  descartei {opcao.acao.verbo.value} "
                f"({opcao.drive_servido}, valor {opcao.valor:.2f})"
            )
        if not self.concluiu:
            linhas.append(
                f"  não terminei de pensar: gastei {self.atencao_gasta} de "
                f"{self.atencao_disponivel}. Vai com a confiança que tem."
            )
        return "\n".join(linhas)


class Deliberacao:
    """O ciclo de decisão sob orçamento."""

    def __init__(self, espirito: Espirito) -> None:
        self._espirito = espirito

    def decidir(
        self,
        agora: Instante,
        vontade: Vontade,
        inteligencia: Inteligencia,
        memoria: Memoria,
        atencao: int,
        limiar_risco: float,
        acoes_possiveis: list[tuple[Acao, str, float, float]],
    ) -> Decisao:
        """Pesa o possível e escolhe.

        `acoes_possiveis` chega do mundo como (ação, drive servido, ganho, risco).
        A deliberação não sabe o que é uma célula nem o que é um trem: só sabe pesar
        o que lhe entregam contra o que ele quer e o que ele crê.
        """
        opcoes: list[Opcao] = []
        gasto = 0
        concluiu = True

        # O fio do pensamento. Não é um relato feito depois: é escrito **durante**,
        # pelo mesmo laço que decide, com os mesmos números que pesaram. Por A3 não
        # há como ele pensar uma coisa e nos contar outra.
        fio: list[str] = []
        dominante = vontade.mais_urgente()
        fio.append(f"sinto-me {vontade.sentimento()}.")
        if dominante.urgencia >= 0.1:
            fio.append(
                f"o que mais me falta é {dominante.nome} ({dominante.erro:.0%} do meu teto); "
                f"vou olhar primeiro o que serve a isso."
            )
        else:
            fio.append("nada me aperta agora, então posso escolher pelo que vale por si.")
        fio.append(f"tenho atenção para examinar {atencao} caminhos.")

        # A atenção é escassa, então **a ordem em que ele olha as opções é dele**,
        # não do mundo. Ele examina primeiro o que serve à falta que mais aperta.
        #
        # Sem isto, com pouca atenção, quem decidiria seria a ordem da lista que o
        # mundo oferece — ou seja, nós. Isso seria o oposto do livre arbítrio: o
        # comportamento viria do nosso código em vez da história dele.
        # Critério duplo, e os dois são dele: primeiro a falta que mais aperta,
        # depois, dentro dela, o que mais promete. Empate resolvido por posição na
        # lista seria o mundo escolhendo de novo.
        ordenadas = sorted(
            acoes_possiveis,
            key=lambda item: (
                vontade[item[1]].urgencia if item[1] in vontade.drives else 0.0,
                item[2],
            ),
            reverse=True,
        )

        for acao, drive, ganho, risco in ordenadas:
            if gasto >= atencao:
                # A7: acabou o orçamento. Ele não pensa pior — apenas para de pensar,
                # e vai saber que parou.
                concluiu = False
                fio.append("acabou minha atenção antes de eu ver tudo. paro por aqui.")
                break
            gasto += 1

            # T1: integridade não compete por espaço no vetor — é teto sobre as
            # outras. Acima do limiar declarado, a ação simplesmente não é emitida.
            if risco > limiar_risco:
                fio.append(
                    f"{acao.verbo.value}{' ' + acao.alvo if acao.alvo else ''}: "
                    f"risco {risco:.0%}, acima dos {limiar_risco:.0%} que aceito. nem considero."
                )
                continue

            urgencia = vontade[drive].urgencia if drive in vontade.drives else 0.0
            # A confiança vem do que ele **crê** sobre a ação dar certo — e, se não
            # crê nada a respeito, é honestamente baixa. Nunca inventada.
            crenca = inteligencia.crencas.get(f"{acao.verbo.value}:{acao.alvo}")
            confianca = crenca.confianca if crenca else 0.5

            # Hábito que já funcionou empurra a confiança, mas só até onde os
            # acertos observados justificam. A4 não deixa passar disso.
            habito = next(
                (
                    h
                    for h in memoria.procedural
                    if h.gatilho == drive and h.acao == acao.verbo.value and h.tentativas >= 3
                ),
                None,
            )
            if habito:
                antes = confianca
                confianca = (confianca + habito.confiabilidade) / 2
                fio.append(
                    f"já tentei {acao.verbo.value} por {drive} {habito.tentativas} vezes e "
                    f"deu certo em {habito.confiabilidade:.0%}; ajusto minha confiança de "
                    f"{antes:.0%} para {confianca:.0%}."
                )

            fio.append(
                f"considero {acao.verbo.value}{' ' + acao.alvo if acao.alvo else ''}"
                f" — {acao.porque}. serve {drive}, promete {ganho:.2f}, confio {confianca:.0%}."
            )

            opcoes.append(
                Opcao(
                    acao=acao,
                    drive_servido=drive,
                    # Não se ganha nada suprindo uma falta que não se tem. Mas
                    # quando nada aperta, ele não congela: o piso de 0,15 deixa o
                    # valor bruto decidir, e é assim que um ser em paz vai à praça
                    # se divertir — sem finalidade, porque ama viver (`01`, §1.1).
                    ganho_esperado=ganho * (0.15 + urgencia),
                    risco=risco,
                    confianca=confianca,
                )
            )

        if not opcoes:
            # Nada passou no teto de risco, ou nada foi oferecido. Esperar é uma
            # decisão legítima e declarada — não é travar.
            fio.append("nada do que me ofereceram eu aceito fazer. espero — e isso é uma decisão.")
            espera = Opcao(
                acao=Acao(Verbo.ESPERAR, porque="nada que eu aceite fazer"),
                drive_servido="integridade",
                ganho_esperado=0.0,
                risco=0.0,
                confianca=1.0,
            )
            return Decisao(agora, espera, [], gasto, atencao, concluiu, fio)

        opcoes.sort(key=lambda o: o.valor, reverse=True)
        escolhida, descartadas = opcoes[0], opcoes[1:]

        if descartadas:
            segunda = descartadas[0]
            margem = escolhida.valor - segunda.valor
            if margem < 0.02:
                fio.append(
                    f"está apertado entre {escolhida.acao.verbo.value} e "
                    f"{segunda.acao.verbo.value} — {escolhida.valor:.3f} contra "
                    f"{segunda.valor:.3f}. quase fui pelo outro."
                )
        fio.append(
            f"decido: {escolhida.acao.verbo.value}"
            f"{' ' + escolhida.acao.alvo if escolhida.acao.alvo else ''}, "
            f"{escolhida.acao.porque}."
        )

        self._espirito.exigir(
            A7,
            0.0 <= escolhida.confianca <= 1.0,
            "a deliberação produziu confiança inválida",
        )
        return Decisao(agora, escolhida, descartadas, gasto, atencao, concluiu, fio)
