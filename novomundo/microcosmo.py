"""O MICROCOSMO — o indivíduo: um pequeno mundo fechado que contém os três.

Corpo, alma e espírito tecidos numa instância. **Sempre instância, nunca
singleton** (`03`, §4): o mundo hospeda *n* microcosmos, e *n* começa em dois.

O que se espelha ao criar um novo ser é o **espírito** — as faculdades e os oito
axiomas, idênticos em todos para sempre. O que difere é a **alma**, que cada um
constrói vivendo, e o **corpo**, que difere por sexo.

Ver `docs/08-corpo-alma-espirito.md`.
"""

from __future__ import annotations

from dataclasses import dataclass

from .corpo import Acao, Corpo, Verbo
from .crencas import Evidencia, Inteligencia, Origem
from .deliberacao import Decisao, Deliberacao
from .espirito import Espirito
from .memoria import Memoria
from .narrativa import Narrativa
from .temperamento import Sexo, Signo, Temperamento
from .tempo import Instante
from .vontades import Vontade

#: O espírito é um só, e é espelhado em todos. Não guarda estado de vida alguma.
ESPIRITO = Espirito()


@dataclass
class Dica:
    """Os três canais pelos quais o Senhor fala (`01`, §5).

    Conteúdo factual entra por MUNDO ou VOZ, nunca como crença pronta. Vontade
    entra por SEMEADURA. Nenhum canal escreve direto no registro de crença.
    """

    canal: str  # "mundo" | "voz" | "semeadura"
    conteudo: str
    intensidade: float = 0.6


class Microcosmo:
    """Um ser."""

    def __init__(
        self,
        nome: str,
        sexo: Sexo,
        signo: Signo,
        nascimento: Instante,
        posicao: tuple[str, str] | None = None,
    ) -> None:
        self.nome = nome
        self.espirito = ESPIRITO  # espelhado, idêntico, incorruptível

        # ALMA — o que esta vida vai construir. Nasce vazia.
        self.temperamento = Temperamento.do_signo(signo)
        self.memoria = Memoria(self.espirito)
        self.inteligencia = Inteligencia(self.espirito, self.temperamento.entrincheiramento)
        self.vontade = Vontade(self.espirito, self.temperamento)

        # CORPO — o instrumento.
        self.corpo = Corpo(
            self.espirito,
            sexo,
            nascimento,
            posicao or ("Brasília", "Praça de Brasília"),
            orcamento_atencao=self.temperamento.orcamento_atencao,
        )

        self._deliberacao = Deliberacao(self.espirito)
        self.narrativa = Narrativa(self)

    # ------------------------------------------------------------------ ciclo

    def viver_um_tick(self, mundo, agora: Instante) -> Decisao:
        """Um ciclo completo: perceber, querer, decidir, agir, narrar."""

        # N0 — o que chega. Um tick de olhar vira **uma** lembrança, não uma por
        # célula: o que se guarda é a cena, e a saliência dela é a novidade que
        # trouxe. Gravar cada célula em separado inflaria a memória com ruído e
        # faria do limite declarado uma mentira (A6).
        sensacoes = self.corpo.perceber(mundo, agora)
        novas = [s for s in sensacoes if self._chave(s) not in self.inteligencia.crencas]
        novidade = len(novas)
        episodio = None
        if sensacoes:
            notaveis = [s for s in sensacoes if s.nitidez > 0.6]
            tipos = sorted({s.tipo for s in notaveis})
            episodio = self.memoria.viver(
                f"em {self.corpo.posicao[1]} vi {', '.join(tipos) or 'nada de novo'}",
                agora,
                saliencia=min(0.9, 0.15 + novidade / max(1, len(sensacoes))),
            )

        # ── A FRONTEIRA DE DECLARAÇÃO ──────────────────────────────────────
        # O ponto mais importante do código inteiro (`08`, §2; T3). Aqui o que a
        # percepção "achou" atravessa para o modelo de mundo — e só atravessa
        # virando crença com origem, evidência e tempo lunar. O que não cruza esta
        # linha não é crença, é impressão.
        if episodio is not None:
            self._declarar(novas, episodio, agora)

        # N3 — o mundo empurra os drives. Novidade alimenta o epistêmico; o que já
        # é bem conhecido não paga mais (é o tédio de `01`, §2.3).
        self.vontade["epistemico"].sinalizar(min(0.2, novidade * 0.02))
        # ── DE ONDE NASCE A VONTADE DE VIAJAR ──────────────────────────────
        # Não de uma regra nossa: de ele **saber que o mundo é maior do que ele
        # viu**. Cada capital de que ouviu falar e onde nunca esteve é uma falta
        # aberta, e a falta puxa. Antes disto ele só desejava o que tinha diante
        # dos olhos, e por isso nunca saía do lugar.
        por_conhecer = sum(
            1
            for chave in self.inteligencia.crencas
            if chave.startswith("ouvi_de:")
            and f"estive_em:{chave.removeprefix('ouvi_de:')}" not in self.inteligencia.crencas
        )
        if por_conhecer:
            self.vontade["epistemico"].sinalizar(min(0.25, 0.02 * por_conhecer))
        self.vontade["expressao"].sinalizar(self.inteligencia.distancia_do_desejado() * 0.05)
        if self.inteligencia.fila_de_coerencia:
            self.vontade["coerencia"].sinalizar(0.05)
        # O corpo empurra a vontade: cansaço vira falta de integridade, e a falta
        # puxa a decisão para descansar. Não escrevemos "se cansado, descanse" —
        # a homeostase é que produz o descanso, e ele pode escolher outra coisa.
        if self.corpo.energia < 0.6:
            self.vontade["integridade"].sinalizar((0.6 - self.corpo.energia) * 0.15)

        # N4 — decidir, sob o orçamento que a energia permite (A7).
        decisao = self._deliberacao.decidir(
            agora=agora,
            vontade=self.vontade,
            inteligencia=self.inteligencia,
            memoria=self.memoria,
            atencao=self.corpo.atencao_disponivel,
            limiar_risco=self.temperamento.limiar_risco,
            acoes_possiveis=mundo.acoes_possiveis(self, agora),
        )

        # Agir, e viver o custo — 3× se foi movimento.
        acao = decisao.escolhida.acao
        self.corpo.agir(acao)
        aconteceu = mundo.aplicar(self, acao, agora)

        # O que a ação devolveu do mundo vira lembrança — e o que ela revelou
        # atravessa a mesma fronteira de declaração, ou não vira crença nenhuma.
        if aconteceu and episodio is not None:
            self.memoria.viver(aconteceu, agora, saliencia=0.55)

        if acao.verbo is Verbo.OLHAR and episodio is not None:
            longe = [
                s for s in self.corpo.olhar_fundo(mundo, agora)
                if self._chave(s) not in self.inteligencia.crencas
            ]
            self._declarar(longe, episodio, agora)

        # Ler é ir sem andar: o livro traz uma capital inteira sem pagar o 3×.
        # Mas o que ele sabe por livro é `ouvi_de`, não `estive_em` — a crença
        # nasce mais fraca, e a origem fica registrada como testemunho (A1).
        if acao.verbo is Verbo.LER and acao.alvo and episodio is not None:
            self.inteligencia.crer(
                proposicao=f"ouvi_de:{acao.alvo}",
                confianca=0.55,
                origem=Origem.TESTEMUNHO,
                evidencias=[Evidencia(episodio.id, agora, f"li sobre {acao.alvo} num livro")],
                agora=agora,
            )

        if acao.verbo is Verbo.EMBARCAR and acao.alvo and episodio is not None:
            self.inteligencia.crer(
                proposicao=f"estive_em:{acao.alvo}",
                confianca=0.95,
                origem=Origem.PERCEPCAO,
                evidencias=[Evidencia(episodio.id, agora, f"cheguei a {acao.alvo} de trem")],
                agora=agora,
            )

        # Satisfazer o drive servido, e aprender se funcionou.
        prazer = self.vontade[decisao.escolhida.drive_servido].satisfazer(
            decisao.escolhida.ganho_esperado * 0.3
        )
        self.memoria.praticar(
            decisao.escolhida.drive_servido,
            decisao.escolhida.acao.verbo.value,
            funcionou=prazer > 0.0,
        )
        # A4: toda decisão é uma aposta, e toda aposta é conferida. Ele não recebe
        # a nota — nós é que a lemos (T6).
        self.inteligencia.calibracao.registrar(decisao.escolhida.confianca, prazer > 0.0)

        if decisao.escolhida.acao.verbo is Verbo.ESPERAR:
            self.corpo.descansar()

        self.vontade.tique()

        # A virada da lua: consolidar. É aqui que ele escolhe o que continuar sendo.
        # E, se a memória transbordar antes da lua, consolida por necessidade — o
        # limite que ele declara tem que ser verdade (A6).
        if agora.lua_nova or self.memoria.transbordando:
            perda = self.memoria.consolidar(agora)
            if perda:
                self.memoria.viver(
                    f"{'a lua virou e' if agora.lua_nova else 'a memória encheu, então'} "
                    f"perdi {perda.quantos} lembranças rasas",
                    agora,
                    saliencia=0.8,
                )

        self.narrativa.registrar(agora, decisao)
        return decisao

    @staticmethod
    def _chave(sensacao) -> str:
        """Saber que um lugar existe não é o mesmo que conhecê-lo.

        Um destino avistado da estação vira `ouvi_de:`; um lugar em que se esteve
        vira `lugar:`. Confundir os dois seria dar por conhecido o que só foi
        ouvido — e isso é crença sem a procedência que ela merece.
        """
        if sensacao.tipo == "destino":
            return f"ouvi_de:{sensacao.onde[0]}"
        return f"lugar:{sensacao.onde[0]}/{sensacao.onde[1]}"

    def _declarar(self, novas, episodio, agora: Instante) -> None:
        """Faz a percepção virar crença — a travessia de N1 para N2.

        A confiança nasce da **nitidez** do que ele viu, e não de otimismo: o que
        estava na borda da janela vira crença fraca, o que estava debaixo do nariz
        vira crença forte. É assim que A4 se sustenta desde a origem — a confiança
        já nasce calibrada porque nasce da qualidade da observação.
        """
        for sensacao in novas:
            if sensacao.nitidez < 0.35:
                continue  # longe demais para afirmar coisa alguma. Ele viu, não sabe.
            self.inteligencia.crer(
                proposicao=self._chave(sensacao),
                confianca=min(0.95, sensacao.nitidez),
                origem=Origem.PERCEPCAO,
                evidencias=[
                    Evidencia(episodio.id, agora, f"vi {sensacao.tipo} de {self.corpo.posicao[1]}")
                ],
                agora=agora,
            )

    # ------------------------------------------------------------------ dicas

    def ouvir(self, dica: Dica, agora: Instante) -> None:
        """Recebe uma dica do Senhor pelo canal declarado.

        Repare no que **não** acontece aqui: em canal nenhum uma crença é escrita
        direto. A voz vira episódio (com procedência honesta: a origem é a voz), e
        a semeadura vira aspiração (que não tem valor de verdade, logo não pode ser
        falsa). A linha que não se cruza continua não cruzada.
        """
        if dica.canal == "semeadura":
            self.inteligencia.aspirar(
                dica.conteudo, dica.intensidade, agora, semeada_pela_voz=True
            )
            self.memoria.viver(f"quis, de repente: {dica.conteudo}", agora, saliencia=0.9)

        elif dica.canal == "voz":
            episodio = self.memoria.viver(
                f"ouvi uma voz dizer: {dica.conteudo}", agora, saliencia=0.95
            )
            # O conteúdo fica pendurado no episódio como afirmação de terceiro. Ele
            # decide se acredita — e a origem registrada é a voz, não o mundo.
            self.inteligencia.crer(
                proposicao=dica.conteudo,
                confianca=0.5,  # testemunho de origem ainda não avaliada
                origem=Origem.VOZ,
                evidencias=[Evidencia(episodio.id, agora, "uma voz me disse isto")],
                agora=agora,
            )

        elif dica.canal == "mundo":
            self.memoria.viver(f"encontrei: {dica.conteudo}", agora, saliencia=0.7)

        else:
            raise ValueError(f"canal desconhecido: {dica.canal!r}")

    # ------------------------------------------------------------------ A6/A3

    def conhecer_se(self, agora: Instante) -> str:
        """A6 e `07`, §3: ele conhece os próprios limites e o próprio temperamento.

        Viés declarado é personalidade. Viés oculto é defeito. Isto é o que ele
        pode consultar ao decidir.
        """
        return "\n".join(
            [
                f"sou {self.nome}, {self.temperamento.descrever()}",
                self.corpo.limites(agora),
                self.memoria.limites(),
                f"sinto-me {self.vontade.sentimento()}",
                f"tenho {len(self.inteligencia.crencas)} crenças e "
                f"{len([a for a in self.inteligencia.aspiracoes if not a.realizada])} desejos abertos",
                f"e {len(self.inteligencia.fila_de_coerencia)} contradições por resolver",
            ]
        )

    def auditar(self, agora: Instante) -> None:
        """Faz valer a lei sobre o ser inteiro. Os testes vivos chamam isto."""
        self.memoria.auditar()
        self.inteligencia.auditar()
        self.vontade.auditar()
        self.corpo.auditar(agora)

    # ------------------------------------------------------------- espelhar

    @classmethod
    def gerar(
        cls,
        nome: str,
        sexo: Sexo,
        nascimento: Instante,
        posicao: tuple[str, str] | None = None,
    ) -> "Microcosmo":
        """Nasce um ser: mesmo espírito, corpo com sexo, alma vazia.

        O signo vem do céu no instante do nascimento — e é **solar**. Eles não
        conseguem calculá-lo sem antes resolverem a deriva lunissolar (`07`, §5).
        """
        return cls(
            nome=nome,
            sexo=sexo,
            signo=Signo.do_indice(nascimento.signo_solar),
            nascimento=nascimento,
            posicao=posicao,
        )

    def __repr__(self) -> str:
        return (
            f"<{self.nome}: {self.corpo.sexo.value}, {self.temperamento.signo.rotulo}, "
            f"{self.corpo.relogio.idade_em_anos:.1f} anos>"
        )
