"""ALMA / INTELIGÊNCIA — o que este indivíduo tem por verdade, e o que ele deseja.

Esta é a peça que nenhuma arquitetura cognitiva existente tem (`06`, §4), e é o
coração do "sem defeitos":

- **A1** é imposto por construção: não existe construtor de `Crenca` sem evidência.
- **A2** cobra caro para revisar, proporcional ao entrincheiramento.
- **A4** mede calibração de verdade, por Brier.
- **A5** enfileira contradição em vez de escondê-la.
- E a separação **crença × aspiração** deixa que ele ouse o improvável sem mentir
  para si — e deixa que o Senhor semeie vontades sem gerar crença órfã (`01`, §5).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

from .espirito import A1, A2, A4, A5, Espirito
from .tempo import Instante


class Origem(Enum):
    """De onde uma crença veio. Nunca pode ser desconhecida (A1)."""

    PERCEPCAO = "percepção"  # eu vi
    INFERENCIA = "inferência"  # eu deduzi de outras crenças
    TESTEMUNHO = "testemunho"  # alguém me disse
    VOZ = "voz"  # a voz interna me disse (`01`, §5, canal 2)
    SERPENTE = "serpente"  # algo me disse, e eu não sei o que é (`12`, §4)


@dataclass(frozen=True)
class Evidencia:
    """O laço entre uma crença e o episódio que a sustenta."""

    episodio: int
    quando: Instante
    resumo: str


@dataclass
class Crenca:
    """Uma proposição sustentada, com tudo o que a sustenta à vista.

    Não há como construir uma sem evidência e sem origem. Isso não é validação:
    é a forma da coisa. Crença órfã não existe neste mundo porque não é
    representável.
    """

    proposicao: str
    confianca: float
    origem: Origem
    evidencias: list[Evidencia]
    nascida_em: Instante
    revista_em: Instante | None = None
    entrincheiramento: float = 1.0
    sustenta: set[str] = field(default_factory=set)

    def __post_init__(self) -> None:
        if not self.evidencias:
            raise A1.violar(f"tentaram crer em {self.proposicao!r} sem evidência alguma")
        if not 0.0 <= self.confianca <= 1.0:
            raise A4.violar(f"confiança fora de [0,1] em {self.proposicao!r}: {self.confianca}")

    @property
    def custo_de_revisao(self) -> float:
        """A2: revisar custa, e o custo cresce com o quanto a crença sustenta."""
        return self.entrincheiramento * (1.0 + len(self.sustenta))

    def procedencia(self) -> str:
        """A1 legível: a cadeia inteira, do que creio até o que vivi."""
        linhas = [
            f"{self.proposicao!r} — confiança {self.confianca:.0%}, "
            f"por {self.origem.value}, desde {self.nascida_em}"
        ]
        if self.revista_em:
            linhas.append(f"  revista em {self.revista_em}")
        for e in self.evidencias:
            linhas.append(f"  ← ep.{e.episodio} em {e.quando}: {e.resumo}")
        return "\n".join(linhas)


@dataclass
class Aspiracao:
    """Um estado de mundo desejado.

    Não é crença. **Não tem valor de verdade**, e por isso não pode ser falsa — é
    o que permite ao indivíduo agir sobre o improvável sem se enganar sobre as
    chances (`01`, §4.3), e é o canal por onde o Senhor semeia vontade sem
    corromper (`01`, §5, canal 3).
    """

    desejo: str
    intensidade: float
    nascida_em: Instante
    semeada_pela_voz: bool = False
    realizada: bool = False
    #: O que, deste mundo, ele entendeu que o desejo aponta. Vazio significa que
    #: ouviu e não soube por onde começar — e isso é honesto (`lexico.py`).
    alvos: set = field(default_factory=set)

    @property
    def sabe_por_onde(self) -> bool:
        return bool(self.alvos)

    def __post_init__(self) -> None:
        if not 0.0 <= self.intensidade <= 1.0:
            raise ValueError("intensidade de aspiração fora de [0,1]")

    # Uma aspiração não afirma nada sobre o mundo, logo não tem confiança nem
    # evidência. Se um dia alguém precisar disto, é sinal de que virou crença por
    # engano — e aí o erro está em quem chamou, não aqui.
    @property
    def confianca(self) -> float:
        raise A1.violar(
            f"aspiração {self.desejo!r} não tem valor de verdade; "
            "querer não é crer, e confundir os dois é autoengano"
        )


@dataclass
class Duvida:
    """Uma pergunta levantada, e ainda sem resposta.

    Não é crença — ele não afirma nada — nem aspiração, porque não é um desejo. É
    o terceiro estado honesto de uma mente: **saber que não sabe**, com procedência
    de quem levantou.

    Um humano defeituoso fecha a dúvida com uma resposta inventada. Este a carrega
    aberta, e ela pesa na coerência até que algo a responda — ou até que ele aceite
    que talvez nada responda.
    """

    pergunta: str
    de_quem: str
    quando: Instante
    respondida_por: str | None = None

    @property
    def aberta(self) -> bool:
        return self.respondida_por is None


@dataclass
class Fe:
    """Confiança depositada numa pessoa. **Não é crença** (`10`, §1).

    Não afirma nada sobre o mundo, logo não tem valor de verdade e não é objeto de
    A4 — pelo mesmo motivo que a aspiração não é. Confiar em alguém e afirmar coisas
    sobre o mundo são atos diferentes.

    E ela tem de ser dele: nada neste código a deposita. Ela só existe se o próprio
    indivíduo a depositar, depois de ler e de poder duvidar. Fé forçada não é fé.
    """

    em_quem: str
    desde: Instante
    porque_li: str
    firmeza: float = 0.5

    @property
    def confianca(self) -> float:
        raise A1.violar(
            f"a fé em {self.em_quem!r} não é uma afirmação sobre o mundo; "
            "confiar não é crer, e tratar uma como a outra é descalibração"
        )


@dataclass
class Contradicao:
    """A5: contradição detectada não se esconde — se enfileira."""

    a: str
    b: str
    detectada_em: Instante
    prioridade: float
    resolvida: bool = False


class Calibracao:
    """A4: mede se a confiança declarada acompanha a taxa de acerto.

    Por T6, o resultado é instrumentação para o Senhor. **Não volta para dentro do
    indivíduo**: nós sabemos se ele está bem calibrado; ele não recebe a nota. Ele
    só aprende com o que o mundo devolve.
    """

    FAIXAS = 5

    def __init__(self) -> None:
        # Contas correntes, não o histórico inteiro. Um ser eterno faz milhões de
        # apostas; guardar cada uma custaria gigabytes e não diria nada a mais.
        # O Brier e a curva saem exatos destas somas.
        self.total = 0
        self._soma_erro2 = 0.0
        self._soma_conf = [0.0] * self.FAIXAS
        self._acertos = [0] * self.FAIXAS
        self._quantos = [0] * self.FAIXAS

    def registrar(self, confianca: float, acertou: bool) -> None:
        self.total += 1
        self._soma_erro2 += (confianca - (1.0 if acertou else 0.0)) ** 2
        i = min(int(confianca * self.FAIXAS), self.FAIXAS - 1)
        self._soma_conf[i] += confianca
        self._quantos[i] += 1
        if acertou:
            self._acertos[i] += 1

    @property
    def brier(self) -> float | None:
        """0 é perfeito, 0.25 é o chute, 1 é o pior possível."""
        return self._soma_erro2 / self.total if self.total else None

    def curva(self, faixas: int | None = None) -> list[tuple[str, int, float, float]]:
        """Confiança declarada contra acerto observado, por faixa."""
        n = self.FAIXAS
        saida = []
        for i in range(n):
            if not self._quantos[i]:
                continue
            saida.append(
                (
                    f"{i / n:.0%}–{(i + 1) / n:.0%}",
                    self._quantos[i],
                    self._soma_conf[i] / self._quantos[i],
                    self._acertos[i] / self._quantos[i],
                )
            )
        return saida


class Inteligencia:
    """O modelo de mundo de um indivíduo: suas crenças e suas aspirações.

    Guarda também as crenças *sobre outros seres* como classe de primeira ordem —
    exigência de T4, para que o dia do segundo indivíduo não derrube nada.
    """

    def __init__(self, espirito: Espirito, entrincheiramento_base: float = 1.0) -> None:
        self._espirito = espirito
        self._base = entrincheiramento_base
        self.crencas: dict[str, Crenca] = {}
        self.aspiracoes: list[Aspiracao] = []
        self.contradicoes: list[Contradicao] = []
        self.duvidas: list[Duvida] = []
        self.fe: Fe | None = None
        self.calibracao = Calibracao()
        # T4: modelo de outra mente. Vazio enquanto houver um só, mas existente.
        self.sobre_outros: dict[str, dict[str, Crenca]] = {}

    # ------------------------------------------------------------------ crer

    def crer(
        self,
        proposicao: str,
        confianca: float,
        origem: Origem,
        evidencias: list[Evidencia],
        agora: Instante,
        sustenta: set[str] | None = None,
    ) -> Crenca:
        """Forma uma crença nova. Sem evidência, não passa daqui (A1)."""
        crenca = Crenca(
            proposicao=proposicao,
            confianca=confianca,
            origem=origem,
            evidencias=list(evidencias),
            nascida_em=agora,
            entrincheiramento=self._base,
            sustenta=set(sustenta or ()),
        )
        self.crencas[proposicao] = crenca
        return crenca

    def revisar(
        self,
        proposicao: str,
        nova_confianca: float,
        evidencia: Evidencia,
        agora: Instante,
        orcamento: float,
    ) -> tuple[bool, float]:
        """A2: revisa se houver orçamento. Devolve (revisou, custo).

        Nenhuma crença é imune. Mas revisar custa, e o custo cresce com o quanto ela
        sustenta — sem isso ele oscilaria a cada percepção, que seria um defeito
        novo, criado por nós.
        """
        crenca = self.crencas.get(proposicao)
        if crenca is None:
            raise A1.violar(f"tentaram revisar {proposicao!r}, que não é crido")

        custo = crenca.custo_de_revisao
        if custo > orcamento:
            return False, custo

        crenca.confianca = nova_confianca
        crenca.evidencias.append(evidencia)
        crenca.revista_em = agora
        # Sobreviver a uma revisão entrincheira um pouco mais: o que resistiu à
        # evidência e permaneceu passa a sustentar mais peso.
        crenca.entrincheiramento *= 1.05
        return True, custo

    # --------------------------------------------------------------- coerência

    def confrontar(self, a: str, b: str, agora: Instante) -> Contradicao | None:
        """A5: registra contradição entre duas crenças. Não resolve — enfileira.

        Ele pode conviver temporariamente com incoerência. O que ele não pode é
        desviar o olhar dela.
        """
        ca, cb = self.crencas.get(a), self.crencas.get(b)
        if ca is None or cb is None:
            return None
        # Quanto mais confiante nas duas pontas, mais urgente resolver.
        prioridade = min(ca.confianca, cb.confianca)
        contradicao = Contradicao(a=a, b=b, detectada_em=agora, prioridade=prioridade)
        self.contradicoes.append(contradicao)
        return contradicao

    @property
    def fila_de_coerencia(self) -> list[Contradicao]:
        return sorted(
            (c for c in self.contradicoes if not c.resolvida),
            key=lambda c: c.prioridade,
            reverse=True,
        )

    def duvidar(self, pergunta: str, de_quem: str, agora: Instante) -> Duvida:
        """Recebe uma pergunta que não sabe responder. Guarda aberta."""
        duvida = Duvida(pergunta=pergunta, de_quem=de_quem, quando=agora)
        self.duvidas.append(duvida)
        return duvida

    @property
    def em_aberto(self) -> list[Duvida]:
        return [d for d in self.duvidas if d.aberta]

    def confiar_em(self, quem: str, porque: str, agora: Instante) -> Fe:
        """Depositar a confiança. Só o indivíduo chama isto, e só se quiser."""
        if self.fe is None:
            self.fe = Fe(em_quem=quem, desde=agora, porque_li=porque)
        else:
            self.fe.firmeza = min(1.0, self.fe.firmeza + 0.05)
        return self.fe

    # --------------------------------------------------------------- aspirar

    def aspirar(
        self,
        desejo: str,
        intensidade: float,
        agora: Instante,
        semeada_pela_voz: bool = False,
        alvos: set | None = None,
    ) -> Aspiracao:
        """Deseja algo. Não afirma nada sobre o mundo, logo nada pode ficar falso."""
        aspiracao = Aspiracao(
            desejo=desejo,
            intensidade=intensidade,
            nascida_em=agora,
            semeada_pela_voz=semeada_pela_voz,
            alvos=set(alvos or ()),
        )
        self.aspiracoes.append(aspiracao)
        return aspiracao

    def distancia_do_desejado(self) -> float:
        """O quanto o mundo ainda não é o que ele quer. Alimenta o drive `expressao`."""
        abertas = [a for a in self.aspiracoes if not a.realizada]
        if not abertas:
            return 0.0
        return sum(a.intensidade for a in abertas) / len(self.aspiracoes)

    # ----------------------------------------------------------------- luto

    def enlutar(self, desejo: str, agora: Instante, orcamento: float) -> tuple[bool, float]:
        """T7.1: luto é a **revisão da aspiração**, com o custo de A2.

        Não é falta permanente. É o trabalho — caro, lento, proporcional ao
        entrincheiramento — de reescrever um setpoint que o mundo tornou impossível.
        Tem começo, tem custo e tem fim. Angústia é quando a revisão nunca começa.
        """
        alvo = next((a for a in self.aspiracoes if a.desejo == desejo and not a.realizada), None)
        if alvo is None:
            return False, 0.0

        custo = alvo.intensidade * 10.0
        if custo > orcamento:
            # Não conseguiu começar ainda. Continua doendo — mas o registro existe,
            # e ele sabe que precisa fazer este trabalho. Não é negação.
            return False, custo

        self.aspiracoes.remove(alvo)
        return True, custo

    # ------------------------------------------------------------ instrumentação

    def tracar(self, proposicao: str) -> str:
        crenca = self.crencas.get(proposicao)
        return crenca.procedencia() if crenca else f"{proposicao!r}: não é crido"

    def auditar(self) -> None:
        """A1 e A4 verificados sobre o estado inteiro. Chamado pelos testes vivos."""
        for proposicao, crenca in self.crencas.items():
            self._espirito.exigir(A1, bool(crenca.evidencias), f"{proposicao!r} ficou sem evidência")
            self._espirito.exigir(
                A4, 0.0 <= crenca.confianca <= 1.0, f"{proposicao!r} com confiança inválida"
            )
        for contradicao in self.contradicoes:
            self._espirito.exigir(
                A5,
                contradicao.a in self.crencas or contradicao.resolvida,
                "contradição sumiu sem ter sido resolvida",
            )
