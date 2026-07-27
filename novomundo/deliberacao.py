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
from .experiencia import Experiencia
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
    por_experiencia: bool = True

    @property
    def valor(self) -> float:
        return self.ganho_esperado * self.confianca


@dataclass
class Intencao:
    """Uma decisão que ele segura ao longo do tempo.

    Sem isto, ele redecide do zero a cada tick — e um ser que redecide tudo a cada
    instante não vai a lugar nenhum: anda para o templo, muda de ideia, volta,
    torna a querer, anda de novo. Foi o que se viu: seis mil passos com o templo
    debaixo dos pés e nunca lá dentro.

    É a diferença entre reagir e **querer**. Um ser humano forma um propósito e o
    carrega enquanto ele valer — e o abandona quando deixa de valer, não a cada
    respiração.
    """

    para_onde: str
    por_que: str
    drive: str
    formada_em: Instante
    passos: int = 0

    def ainda_vale(self, vontade, limite: int = 12) -> bool:
        """Vale enquanto a falta que a gerou continuar apertando, e enquanto não
        virar teimosia. Persistir para sempre seria outro defeito."""
        if self.passos >= limite:
            return False
        drive = vontade.drives.get(self.drive)
        return bool(drive and drive.erro > 0.15)


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
    intencao: Intencao | None = None

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
        experiencia: Experiencia,
        onde: str,
        atencao: int,
        limiar_risco: float,
        acoes_possiveis: list[tuple[Acao, str, float]],
        intencao: Intencao | None = None,
    ) -> Decisao:
        """Pesa o possível e escolhe.

        `acoes_possiveis` chega do mundo como (ação, drive que a ação toca, risco).
        **O mundo não diz quanto vale.** Valor não é propriedade do mundo: é o que
        aquilo já fez por ele, medido na própria carne (`09`, §1).

        A deliberação não sabe o que é uma biblioteca nem o que é um trem. Sabe pesar
        o que lhe entregam contra o que lhe falta e contra o que ele viveu.
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

        # ── A INTENÇÃO QUE ELE CARREGA ──────────────────────────────────────
        # Antes de olhar o que há, ele lembra do que estava indo fazer. Se ainda
        # vale, segue — porque querer é atravessar o tempo, não recomeçar a cada
        # instante.
        if intencao is not None and intencao.ainda_vale(vontade):
            for acao, drive, risco in acoes_possiveis:
                if acao.alvo == intencao.para_onde and risco <= limiar_risco:
                    intencao.passos += 1
                    fio.append(
                        f"eu estava indo {intencao.por_que}. ainda quero. sigo — "
                        f"{intencao.passos}º passo."
                    )
                    escolhida = Opcao(acao, drive, 0.0, risco, 0.6, True)
                    return Decisao(agora, escolhida, [], 1, atencao, True, fio, intencao)
        elif intencao is not None:
            fio.append(f"eu ia {intencao.por_que}, mas já não me puxa. deixo pra lá.")

        # A atenção é escassa, então **a ordem em que ele olha as opções é dele**,
        # não do mundo. Ele examina primeiro o que serve à falta que mais aperta.
        #
        # Sem isto, com pouca atenção, quem decidiria seria a ordem da lista que o
        # mundo oferece — ou seja, nós. Isso seria o oposto do livre arbítrio: o
        # comportamento viria do nosso código em vez da história dele.
        # Critério duplo, e os dois são dele: primeiro a falta que mais aperta,
        # depois, dentro dela, o que mais promete. Empate resolvido por posição na
        # lista seria o mundo escolhendo de novo.
        def lembrar_o_quanto_vale(item) -> tuple[float, float]:
            """A lembrança é barata; deliberar é caro.

            Ele **lembra** de relance o que cada coisa costuma lhe fazer — isso não
            consome atenção — e só examina de perto as mais promissoras. Sem este
            passo, com atenção baixa, quem escolhia era a ordem da lista: um ser
            passou 7929 ticks andando entre a praça e o templo sem nunca chegar a
            olhar o "divertir-se" que estava logo abaixo na lista.
            """
            acao, drive, _risco = item
            urgencia = vontade[drive].urgencia if drive in vontade.drives else 0.0
            # O alvo faz parte da experiência: ler Sêneca não é ler o Evangelho, e
            # conversar com ela não é conversar com qualquer um.
            chave = (acao.verbo.value, acao.alvo or onde)
            if experiencia.conhece(chave):
                promessa = sum(
                    q * vontade[d].erro * vontade[d].ganho
                    for d, q in experiencia.esperado(chave).items()
                    if d in vontade.drives
                )
            else:
                # O que ele nunca provou chama pela curiosidade, e chama forte.
                promessa = vontade["epistemico"].erro * vontade["epistemico"].ganho * 0.5

            # Empatados, ele prefere o ato que **chega** ao que apenas caminha para
            # lá. Andar até o templo e contemplar servem à mesma falta, mas só um
            # dos dois a resolve. Sem isto, um ser com a coerência no talo andava
            # seis mil vezes com o templo debaixo dos pés.
            chega_ao_fim = acao.verbo is not Verbo.MOVER
            return (urgencia, promessa, chega_ao_fim)

        ordenadas = sorted(acoes_possiveis, key=lembrar_o_quanto_vale, reverse=True)

        for acao, drive, risco in ordenadas:
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

            # ── A RECOMPENSA REAL ────────────────────────────────────────────
            # Não há número vindo do mundo. O que ele espera ganhar é o que esta
            # ação, neste lugar, já baixou das faltas que ele tem AGORA.
            chave = (acao.verbo.value, acao.alvo or onde)
            ja_vivido = experiencia.esperado(chave)
            por_experiencia = experiencia.conhece(chave)

            if por_experiencia:
                ganho = sum(
                    queda * vontade[d].erro * vontade[d].ganho
                    for d, queda in ja_vivido.items()
                    if d in vontade.drives
                )
                # Confiança = quanto ele já viu disto. Pouca amostra, pouca certeza.
                # É A4 nascendo da experiência em vez de ser declarada por nós.
                vezes = experiencia.vezes(chave)
                confianca = min(0.95, 0.35 + 0.12 * vezes)
            else:
                # Nunca tentou. Não sabe se presta — e **não saber é uma falta**.
                # É por isto que ele experimenta o novo: não por bônus de exploração
                # que nós demos, mas porque ignorar dói de verdade nele.
                ganho = vontade["epistemico"].erro * vontade["epistemico"].ganho * 0.5
                confianca = 0.5

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
                f" — {acao.porque}. "
                + (
                    f"das outras vezes isto me baixou {sum(ja_vivido.values()):.2f} de falta; "
                    f"do jeito que estou hoje, valeria {ganho:.2f}."
                    if por_experiencia
                    else "nunca tentei. não sei o que me faz — e é justamente por isso."
                )
            )

            opcoes.append(
                Opcao(
                    acao=acao,
                    drive_servido=drive,
                    # Não se ganha nada suprindo uma falta que não se tem. Mas
                    # quando nada aperta, ele não congela: o piso de 0,15 deixa o
                    # valor bruto decidir, e é assim que um ser em paz vai à praça
                    # se divertir — sem finalidade, porque ama viver (`01`, §1.1).
                    ganho_esperado=ganho,
                    risco=risco,
                    confianca=confianca,
                    por_experiencia=por_experiencia,
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

        # Se o que ele decidiu foi *ir* a algum lugar, isso vira propósito e ele o
        # carrega. Não é um plano elaborado: é a teimosia mínima que separa querer
        # de reagir.
        nova = None
        if escolhida.acao.verbo is Verbo.MOVER and escolhida.acao.alvo:
            nova = Intencao(
                para_onde=escolhida.acao.alvo,
                por_que=escolhida.acao.porque,
                drive=escolhida.drive_servido,
                formada_em=agora,
            )
            fio.append(f"e guardo isto como propósito: {escolhida.acao.porque}.")

        self._espirito.exigir(
            A7,
            0.0 <= escolhida.confianca <= 1.0,
            "a deliberação produziu confiança inválida",
        )
        return Decisao(agora, escolhida, descartadas, gasto, atencao, concluiu, fio, nova)
