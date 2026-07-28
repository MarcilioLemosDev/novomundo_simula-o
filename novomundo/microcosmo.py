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

from .compromisso import Compromisso
from .corpo import Acao, Corpo, Verbo
from .crencas import Evidencia, Inteligencia, Origem
from .deliberacao import Decisao, Deliberacao, Intencao
from .espirito import Espirito
from .experiencia import Experiencia
from .lexico import entender
from .livro import Passagem
from .memoria import Memoria
from .razoes import Razao, puxao, razoes_para
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
        # O que ele aprendeu, na carne, sobre o que o preenche. Nasce vazia: ninguém
        # lhe conta que ler ajuda ou que a praça alegra (`09`, §1).
        self.experiencia = Experiencia()

        # CORPO — o instrumento.
        self.corpo = Corpo(
            self.espirito,
            sexo,
            nascimento,
            posicao or ("Brasília", "Praça de Brasília"),
            orcamento_atencao=self.temperamento.orcamento_atencao,
        )

        #: Vínculos: quanto tempo dei a cada um, e quanto ele me deu. O vínculo é
        #: mútuo por construção — só a reciprocidade preenche (`09`, §3.1).
        self.vinculos: dict[str, int] = {}
        self._recebido: dict[str, int] = {}
        self.lidas: set[str] = set()
        #: O que ele **leu** que cada ato agrega. Pode estar errado — é daqui que
        #: nasce o erro honesto (`12`, §3).
        self.esperado_por_leitura: dict[str, str] = {}
        #: Com quem se uniu, e quantas vezes.
        self.unioes: dict[str, int] = {}
        #: O que ele prometeu a si mesmo fazer (`09`, §1). Pode não cumprir — e o
        #: que isso gera é incoerência, nunca culpa.
        self.compromissos: list[Compromisso] = []
        #: O que o Senhor lhe disse, e o que ele entendeu de cada coisa. Existe para
        #: que quem fala com ele possa ver se aquilo chegou.
        self.ditos_do_senhor: list[tuple[str, str, str, Instante]] = []
        #: O que ele leu do Mestre e guardou. Encontrar não é ainda confiar.
        self.encontrou_o_mestre: str | None = None
        #: A última leitura trouxe algo, ou foi releitura? Sem isto, reler paga o
        #: mesmo que descobrir — e um ser passa a vida na biblioteca.
        self._leitura_trouxe = 0.0
        self.chegou_a_lugar_novo = False
        #: O que ele estava indo fazer. Querer atravessa o tempo.
        self.intencao: Intencao | None = None
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
        # Uma pergunta sem resposta pesa. É a falta de coerência mais honesta que
        # existe: saber que não sabe, e que alguém está esperando.
        if self.inteligencia.em_aberto:
            self.vontade["coerencia"].sinalizar(0.01 * len(self.inteligencia.em_aberto))
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
            experiencia=self.experiencia,
            onde=self.corpo.posicao[1],
            quem=self,
            atencao=self.corpo.atencao_disponivel,
            limiar_risco=self.temperamento.limiar_risco,
            acoes_possiveis=mundo.acoes_possiveis(self, agora),
            intencao=self.intencao,
        )
        self.intencao = decisao.intencao

        # Agir, e viver o custo — 3× se foi movimento.
        acao = decisao.escolhida.acao
        onde_estava = self.corpo.posicao[1]
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

        # ── O QUE A AÇÃO DE FATO FEZ ────────────────────────────────────────
        # Aqui não se paga crédito: mede-se. O efeito é aplicado sobre a falta real,
        # e o que se guarda na experiência é **a queda observada**, não a prometida.
        antes = {n: d.erro for n, d in self.vontade.drives.items()}
        self._efeito(decisao.escolhida, agora)
        quedas = {n: antes[n] - self.vontade[n].erro for n in antes}
        self.experiencia.registrar(
            (decisao.escolhida.acao.verbo.value, decisao.escolhida.acao.alvo or onde_estava),
            quedas,
        )
        prazer = sum(q for q in quedas.values() if q > 0)
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

        # O compromisso: cumprir o que prometeu, ou ficar devendo — e ficar devendo
        # é uma incoerência como qualquer outra, que ele carrega à vista.
        for compromisso in self.compromissos:
            compromisso.cumprir(acao)
            if compromisso.virar_semana(agora):
                self.memoria.viver(
                    f"a semana virou e eu não cumpri: {compromisso.o_que}",
                    agora,
                    saliencia=0.75,
                )
                self.vontade["coerencia"].sinalizar(0.15)

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
        #: Guardado para a interface poder mostrar o fio inteiro do pensamento.
        self._ultima_decisao = decisao
        return decisao

    #: As perguntas que um ser levanta quando não sabe. Nenhum dos dois tem a
    #: resposta: a única base de conhecimento do mundo são os dois livros, e
    #: eles não respondem tudo.
    PERGUNTAS = (
        "de onde viemos, no princípio?",
        "por que não é bom estar só?",
        "o tempo é nosso ou nos leva?",
        "o que fazemos com a dor?",
        "o que é o amor, se não é posse?",
        "podemos conhecer a verdade inteira?",
        "para que porto vamos?",
    )

    def perguntar(self, agora: Instante) -> str | None:
        """O que este ser não sabe e gostaria de saber.

        Ele só pergunta o que de fato não sabe — nunca o que já crê. Perguntar o
        que se sabe seria teatro, e um ser sem defeitos não faz cena.
        """
        for pergunta in self.PERGUNTAS:
            ja_perguntei = any(d.pergunta == pergunta for d in self.inteligencia.duvidas)
            if not ja_perguntei:
                self.inteligencia.duvidar(pergunta, "mim mesmo", agora)
                return pergunta
        return None

    def assumir(self, compromisso: Compromisso, agora: Instante) -> Compromisso:
        """Assumir um compromisso. Ele pode quebrá-lo — se não pudesse, não seria
        compromisso, seria corrente."""
        self.compromissos.append(compromisso)
        self.memoria.viver(f"assumi: {compromisso.o_que}", agora, saliencia=0.85)
        return compromisso

    def contar_a(self, outro, proposicao: str, agora: Instante) -> bool:
        """Dizer a alguém o que eu creio. É assim que a crença atravessa.

        E aqui está a peça da narrativa (`12`, §5): **o amor dá peso ao que se
        ouve.** O que vem de quem se ama não chega com o peso de um estranho — e
        isso não é falha de calibração, é calibração correta, porque quem nos ama
        de fato mente menos.

        O preço é o que a história conta: **quem ama está mais exposto a errar
        junto.**
        """
        minha = self.inteligencia.crencas.get(proposicao)
        if minha is None or proposicao in outro.inteligencia.crencas:
            return False

        juntos = min(outro.vinculos.get(self.nome, 0), outro._recebido.get(self.nome, 0))
        peso_do_vinculo = min(0.35, 0.01 * juntos)
        episodio = outro.memoria.viver(
            f"{self.nome} me disse: {proposicao}", agora, saliencia=0.9
        )
        outro.inteligencia.crer(
            proposicao=proposicao,
            confianca=min(0.9, 0.35 + peso_do_vinculo + minha.confianca * 0.3),
            origem=Origem.TESTEMUNHO,
            evidencias=[Evidencia(episodio.id, agora, f"disse-me {self.nome}")],
            agora=agora,
        )
        return True

    def conhecer(self, outro, agora: Instante) -> None:
        """Passar a saber que o outro existe, e quem ele é."""
        chave = f"conheço:{outro.nome}"
        if chave not in self.inteligencia.crencas:
            episodio = self.memoria.viver(
                f"encontrei {outro.nome} em {self.corpo.posicao[1]}", agora, saliencia=0.95
            )
            self.inteligencia.crer(
                proposicao=chave,
                confianca=0.9,
                origem=Origem.PERCEPCAO,
                evidencias=[Evidencia(episodio.id, agora, f"vi {outro.nome} com meus olhos")],
                agora=agora,
            )

    @property
    def relacao_com(self) -> dict[str, str]:
        """Os tipos de relacionamento (`09`, §3.3), lidos do que de fato houve."""
        tipos = {}
        for nome, dei in self.vinculos.items():
            recebi = self._recebido.get(nome, 0)
            juntos = min(dei, recebi)
            if juntos >= 60:
                tipos[nome] = "companheiro(a)"
            elif juntos >= 15:
                tipos[nome] = "amigo(a)"
            elif dei > 0 and recebi == 0:
                tipos[nome] = "quem eu procuro, e ainda não me procurou"
            else:
                tipos[nome] = "conhecido(a)"
        return tipos

    def ler_descricao(self, descricao, agora: Instante) -> None:
        """Ler o que se diz que um ato acrescenta.

        Forma uma **expectativa**, não uma certeza. Se a descrição não corresponder
        ao que o ato faz, ele agirá errado — honestamente, por ter acreditado em
        alguém. É o erro humano, e é descobrível (`12`, §3).
        """
        self.lidas.add(descricao.texto)
        self.esperado_por_leitura[descricao.ato] = descricao.diz
        episodio = self.memoria.viver(f"li: {descricao.texto}", agora, saliencia=0.7)
        if descricao.diz not in self.inteligencia.crencas:
            self.inteligencia.crer(
                proposicao=descricao.diz,
                confianca=0.5,  # está escrito. estar escrito não é ser verdade.
                origem=Origem.TESTEMUNHO,
                evidencias=[Evidencia(episodio.id, agora, "li no compêndio dos atos")],
                agora=agora,
            )

    def ler_passagem(self, passagem: Passagem, titulo: str, agora: Instante) -> None:
        """Ler é receber testemunho — nunca receber verdade (`01`, §5; `10`, §4).

        O que o livro afirma entra com origem TESTEMUNHO e confiança de quem ouviu
        alguém dizer. Ele pode discordar de Sêneca e pode discordar do Evangelho.
        Se dois livros disserem coisas em tensão, a tensão vai para a fila de A5 e
        ele terá de pensar — que é a única coisa que ler não faz por ninguém.
        """
        inedita = passagem.carta not in self.lidas
        self.lidas.add(passagem.carta)
        self._leitura_trouxe = 0.12 if inedita else 0.005
        episodio = self.memoria.viver(
            f"li {passagem.carta} de {titulo}: “{passagem.texto}”", agora, saliencia=0.85
        )
        proposicao = passagem.afirma
        if proposicao not in self.inteligencia.crencas:
            self.inteligencia.crer(
                proposicao=proposicao,
                confianca=0.55,  # está escrito, e estar escrito não é ser verdade
                origem=Origem.TESTEMUNHO,
                evidencias=[Evidencia(episodio.id, agora, f"{passagem.carta}, em {titulo}")],
                agora=agora,
            )

        # Uma dúvida aberta pode encontrar aqui a sua resposta — ou não encontrar.
        for duvida in self.inteligencia.em_aberto:
            if any(tema in duvida.pergunta.lower() for tema in passagem.sobre):
                duvida.respondida_por = f"{passagem.carta}, {titulo}"
                self.memoria.viver(
                    f"achei no livro algo sobre o que {duvida.de_quem} me perguntou: "
                    f"{duvida.pergunta}",
                    agora,
                    saliencia=0.9,
                )
                break

        # Ler não é onde a fé se deposita. Ler é onde ele **encontra a pessoa** —
        # e guarda isso. O que faz com o encontro, ele decide depois, no templo.
        if "Testamento" in titulo and any(
            t in ("princípio", "origem", "luz", "amor", "verdade", "entrega")
            for t in passagem.sobre
        ):
            self.encontrou_o_mestre = f"{passagem.carta}: {passagem.afirma}"

    def _quanto_me_deram(self, nome: str) -> int:
        """Quanto o outro se voltou para mim. Preenchido pelo mundo no encontro."""
        return self._recebido.get(nome, 0)

    def _efeito(self, escolha, agora: Instante) -> None:
        """O que o ato faz de verdade nas faltas dele.

        Este é o único lugar onde uma falta cede, e o que ela cede depende do ato e
        do lugar — não de um número que o mundo prometeu. `sexo com amor` e `sexo
        sem amor` seriam o mesmo verbo com efeitos diferentes, e ele descobriria a
        diferença vivendo (`09`, §3.2).
        """
        verbo = escolha.acao.verbo
        if verbo is Verbo.LER:
            # Reler não é descobrir. O que a leitura preenche é o que ela trouxe de
            # novo — e uma página já sabida quase não traz nada.
            self.vontade["epistemico"].satisfazer(self._leitura_trouxe)
            self._leitura_trouxe = 0.0
            if self.inteligencia.em_aberto:
                self.vontade["coerencia"].satisfazer(0.12)
            if self.inteligencia.fe is not None:
                # A fé ordena as dúvidas sem responder nenhuma por decreto (`10`, §3).
                self.vontade["coerencia"].satisfazer(0.04)
        elif verbo is Verbo.EMBARCAR:
            # Chegar onde nunca esteve preenche; voltar ao sabido, quase nada. É o
            # tédio funcionando na escala do mundo.
            self.vontade["epistemico"].satisfazer(0.30 if self.chegou_a_lugar_novo else 0.02)
        elif verbo is Verbo.MOVER:
            # Chegar a um lugar que já conheço não me ensina nada. Enquanto isto
            # pagava fixo, ele andava em círculos a vida inteira — o mesmo defeito
            # de sempre, e da quinta vez ficou claro que a regra é geral:
            # **toda recompensa fixa vira um laço.**
            ja_conhecia = f"lugar:{self.corpo.posicao[0]}/{self.corpo.posicao[1]}" in (
                self.inteligencia.crencas
            )
            self.vontade["epistemico"].satisfazer(0.005 if ja_conhecia else 0.05)
        elif verbo is Verbo.CONTEMPLAR:
            # Contemplar é sentar-se com o que está por acertar — as contradições e,
            # sobretudo, **as perguntas que ninguém respondeu**. Sem nada disso,
            # contemplar é só estar, e está bem que seja.
            por_acertar = len(self.inteligencia.fila_de_coerencia) + len(
                self.inteligencia.em_aberto
            )
            self.vontade["coerencia"].satisfazer(min(0.22, 0.01 + 0.05 * por_acertar))
            # ── A FÉ, SE ELE QUISER ─────────────────────────────────────────
            # No templo, carregando as perguntas que ninguém respondeu, tendo lido
            # e podendo duvidar, ele deposita ou não a sua confiança. Nada aqui o
            # obriga: se nunca depositar, isso é dado sobre o modelo, não falha da
            # simulação (`10`, §2). Fé forçada não seria fé.
            if self.encontrou_o_mestre and len(self.inteligencia.em_aberto) >= 2:
                fe = self.inteligencia.confiar_em(
                    "o Mestre Jesus Cristo", self.encontrou_o_mestre, agora
                )
                if fe.firmeza <= 0.5:
                    self.memoria.viver(
                        "no templo, com as perguntas que carrego, decidi confiar nEle. "
                        "não foi argumento que me convenceu — foi a pessoa.",
                        agora,
                        saliencia=1.0,
                    )
                self.vontade["coerencia"].satisfazer(0.08)
        elif verbo is Verbo.DIVERTIR:
            # Sozinho, a diversão alegra menos do que alegraria acompanhado — e é
            # ele quem vai descobrir isso, não nós que vamos lhe dizer.
            self.vontade["vinculo"].satisfazer(0.12)
            self.vontade["expressao"].satisfazer(0.04)
        elif verbo is Verbo.MARCAR:
            self.vontade["expressao"].satisfazer(0.25)
        elif verbo is Verbo.COLETAR:
            self.vontade["integridade"].satisfazer(0.20)
        elif verbo is Verbo.LER and escolha.acao.alvo and "acrescenta" in (escolha.acao.alvo or ""):
            self.vontade["epistemico"].satisfazer(self._leitura_trouxe)
            self._leitura_trouxe = 0.0

        elif verbo is Verbo.CONVERSAR and escolha.acao.alvo:
            # ── O ENCONTRO ──────────────────────────────────────────────────
            # Aqui está a peça que faz o amor custar: **o vínculo não se satisfaz
            # sozinho.** O quanto esta conversa me preenche depende de quanto o
            # outro também se voltou para mim. Amar primeiro é pagar sozinho por um
            # tempo — legítimo, e é a vida (`09`, §3.1).
            dei = self.vinculos.get(escolha.acao.alvo, 0) + 1
            self.vinculos[escolha.acao.alvo] = dei
            recebi = self._quanto_me_deram(escolha.acao.alvo)
            mutualidade = min(1.0, recebi / dei) if dei else 0.0
            self.vontade["vinculo"].satisfazer(0.06 + 0.22 * mutualidade)
            self.vontade["epistemico"].satisfazer(0.04)

        elif verbo is Verbo.UNIR and escolha.acao.alvo:
            # O mesmo ato, com e sem vínculo, não preenche igual — e nós não
            # escrevemos a diferença em lugar nenhum que ele possa ler. Ele mede.
            outro = escolha.acao.alvo
            dei = self.vinculos.get(outro, 0)
            recebi = self._recebido.get(outro, 0)
            juntos = min(dei, recebi)
            com_amor = min(1.0, juntos / 40.0)
            self.unioes[outro] = self.unioes.get(outro, 0) + 1
            self.vontade["vinculo"].satisfazer(0.08 + 0.45 * com_amor)
            self.vontade["expressao"].satisfazer(0.10 + 0.25 * com_amor)

        elif verbo is Verbo.ESPERAR:
            # Parar repõe. Sem isto ele nunca aprendia que descansar serve para
            # algo, e andava até a atenção ficar no piso — vivendo uma vida inteira
            # com dois caminhos de cada vez.
            self.vontade["integridade"].satisfazer(0.15)

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

    def _registrar_dito(self, dica, agora) -> None:
        self.ditos_do_senhor.append([dica.canal, dica.conteudo, "", agora])

    def _entendi(self, entendimento: str) -> str:
        if self.ditos_do_senhor:
            self.ditos_do_senhor[-1][2] = entendimento
        return entendimento

    def ouvir(self, dica: Dica, agora: Instante, mundo=None) -> str:
        """Recebe o que o Senhor lhe diz, pelo canal declarado (`01`, §5).

        Repare no que **não** acontece: em canal nenhum uma crença é escrita direto.
        A voz vira episódio (procedência honesta: a origem é a voz) e a semeadura
        vira aspiração (que não tem valor de verdade, logo não pode ser falsa). A
        linha que não se cruza continua não cruzada.

        Devolve **o que ele entendeu**, em palavras — para que o Senhor possa ver
        se aquilo chegou, e não ficar falando com uma parede.
        """
        conhecidos = {
            k.removeprefix("conheço:")
            for k in self.inteligencia.crencas
            if k.startswith("conheço:")
        }
        alvos = entender(dica.conteudo, mundo, conhecidos)
        self._registrar_dito(dica, agora)

        if dica.canal == "semeadura":
            self.inteligencia.aspirar(
                dica.conteudo, dica.intensidade, agora, semeada_pela_voz=True, alvos=alvos
            )
            if alvos:
                self.memoria.viver(
                    f"quis, de repente: {dica.conteudo}", agora, saliencia=0.95
                )
                # A vontade nova aperta na hora — é o que faz ele mudar de rumo.
                self.vontade["expressao"].sinalizar(0.2 * dica.intensidade)
                return self._entendi("entendi, e já sei por onde: " + ", ".join(sorted(alvos)))
            # Ouviu, quis, e não sabe por onde começar. Honesto, e fica registrado.
            self.memoria.viver(
                f"quis algo que não sei alcançar: {dica.conteudo}", agora, saliencia=0.9
            )
            self.vontade["coerencia"].sinalizar(0.1)
            return self._entendi("quis, mas não sei o que isso quer dizer no meu mundo")

        if dica.canal == "voz":
            episodio = self.memoria.viver(
                f"ouvi uma voz dizer: {dica.conteudo}", agora, saliencia=0.95
            )
            # O conteúdo fica pendurado no episódio como afirmação de terceiro. Ele
            # decide se acredita — e a origem registrada é a voz, não o mundo.
            if dica.conteudo not in self.inteligencia.crencas:
                self.inteligencia.crer(
                    proposicao=dica.conteudo,
                    confianca=0.5,  # testemunho de origem ainda não avaliada
                    origem=Origem.VOZ,
                    evidencias=[Evidencia(episodio.id, agora, "uma voz me disse isto")],
                    agora=agora,
                )
            if alvos:
                # Se a voz apontou para algo do mundo, ele fica com aquilo na cabeça.
                self.esperado_por_leitura.setdefault(
                    next(iter(sorted(alvos))), f"uma voz me disse: {dica.conteudo}"
                )
                return self._entendi("ouvi, e me ficou na cabeça: " + ", ".join(sorted(alvos)))
            return self._entendi("ouvi, mas não sei do que se trata")

        if dica.canal == "mundo":
            self.memoria.viver(f"encontrei: {dica.conteudo}", agora, saliencia=0.7)
            self.vontade["epistemico"].sinalizar(0.1)
            return self._entendi(
                "achei isto" + (", e reconheço: " + ", ".join(sorted(alvos)) if alvos else "")
            )

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
