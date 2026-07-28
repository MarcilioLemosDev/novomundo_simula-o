"""O mundo — as capitais reais, interligadas pelo trem.

O mapa não é uma grade abstrata: são as capitais do mundo, com as distâncias que
elas de fato têm. É daí que nasce a vontade de viajar — não de uma regra que
escrevemos, mas de haver um mundo grande e caro do lado de fora da janela.

Dentro de cada capital há onde ler, onde contemplar, onde se divertir, onde prover-se.
E há a estação: dali parte o trem que liga tudo.

Nada é escondido por magia. O que ele não sabe, não sabe porque não foi lá ou não
leu — nunca porque o mundo mente.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field

from .corpo import Acao, Verbo
from . import descricoes
from .livro import Livro, acervo
from .tempo import TICKS_POR_DIA, Instante


@dataclass(frozen=True)
class Local:
    """Um lugar dentro de uma capital."""

    nome: str
    tipo: str  # estação | biblioteca | templo | praça | mercado

    @property
    def descricao(self) -> str:
        return f"{self.nome} ({self.tipo})"


LOCAIS_PADRAO = (
    ("Estação", "estação"),
    ("Biblioteca", "biblioteca"),
    ("Templo", "templo"),
    ("Praça", "praça"),
    ("Mercado", "mercado"),
)


@dataclass
class Capital:
    nome: str
    pais: str
    lat: float
    lon: float
    locais: list[Local] = field(default_factory=list)
    marcas: dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.locais:
            self.locais = [Local(f"{n} de {self.nome}", t) for n, t in LOCAIS_PADRAO]

    def local(self, tipo: str) -> Local:
        return next(l for l in self.locais if l.tipo == tipo)


#: As capitais, com as coordenadas que elas têm de verdade.
CAPITAIS: tuple[Capital, ...] = (
    Capital("Brasília", "Brasil", -15.79, -47.88),
    Capital("Buenos Aires", "Argentina", -34.60, -58.38),
    Capital("Lima", "Peru", -12.05, -77.04),
    Capital("Bogotá", "Colômbia", 4.71, -74.07),
    Capital("Cidade do México", "México", 19.43, -99.13),
    Capital("Washington", "Estados Unidos", 38.91, -77.04),
    Capital("Ottawa", "Canadá", 45.42, -75.70),
    Capital("Lisboa", "Portugal", 38.72, -9.14),
    Capital("Madri", "Espanha", 40.42, -3.70),
    Capital("Paris", "França", 48.86, 2.35),
    Capital("Londres", "Reino Unido", 51.51, -0.13),
    Capital("Berlim", "Alemanha", 52.52, 13.40),
    Capital("Roma", "Itália", 41.90, 12.50),
    Capital("Moscou", "Rússia", 55.75, 37.62),
    Capital("Cairo", "Egito", 30.04, 31.24),
    Capital("Nairóbi", "Quênia", -1.29, 36.82),
    Capital("Pretória", "África do Sul", -25.75, 28.19),
    Capital("Nova Déli", "Índia", 28.61, 77.21),
    Capital("Pequim", "China", 39.90, 116.41),
    Capital("Tóquio", "Japão", 35.69, 139.69),
    Capital("Bangkok", "Tailândia", 13.75, 100.52),
    Capital("Camberra", "Austrália", -35.28, 149.13),
)

#: A malha. Cada par é uma linha de trem entre duas capitais.
LINHAS: tuple[tuple[str, str], ...] = (
    ("Brasília", "Buenos Aires"), ("Brasília", "Bogotá"), ("Brasília", "Lisboa"),
    ("Buenos Aires", "Lima"), ("Lima", "Bogotá"), ("Bogotá", "Cidade do México"),
    ("Cidade do México", "Washington"), ("Washington", "Ottawa"),
    ("Washington", "Londres"), ("Lisboa", "Madri"), ("Madri", "Paris"),
    ("Paris", "Londres"), ("Paris", "Roma"), ("Paris", "Berlim"),
    ("Berlim", "Moscou"), ("Roma", "Cairo"), ("Cairo", "Nairóbi"),
    ("Nairóbi", "Pretória"), ("Cairo", "Nova Déli"), ("Moscou", "Pequim"),
    ("Nova Déli", "Bangkok"), ("Bangkok", "Pequim"), ("Pequim", "Tóquio"),
    ("Bangkok", "Camberra"),
)


def distancia_km(a: Capital, b: Capital) -> float:
    """Haversine. As distâncias são as reais — é o que torna viajar uma decisão."""
    r = 6371.0
    p1, p2 = math.radians(a.lat), math.radians(b.lat)
    dp = math.radians(b.lat - a.lat)
    dl = math.radians(b.lon - a.lon)
    h = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * r * math.asin(math.sqrt(h))


@dataclass(frozen=True)
class Linha:
    de: str
    para: str
    km: float
    fases: frozenset[int]  # em que fases da lua o trem parte

    @property
    def ticks(self) -> int:
        return max(TICKS_POR_DIA // 2, int(self.km / 90))


class Mundo:
    """As capitais e a malha. A topologia social do mundo é a malha (`03`, §2.1.2)."""

    def __init__(self) -> None:
        self.capitais: dict[str, Capital] = {c.nome: c for c in CAPITAIS}
        #: Quem vive aqui. O mundo hospeda *n* microcosmos, e *n* começa em dois.
        self.habitantes: list = []
        #: A única base de conhecimento que existe, numa biblioteca só. Quem quiser
        #: ler tem de ir até lá — e ir custa o triplo.
        self.acervo: list[Livro] = acervo(self.capitais["Brasília"].local("biblioteca").nome)
        self.linhas: list[Linha] = []
        for de, para in LINHAS:
            km = distancia_km(self.capitais[de], self.capitais[para])
            # O horário é ancorado na lua, não num relógio arbitrário (`03`, §2.1.1).
            # É por isso que ele pode perder o trem — e uma estação vazia ensina
            # melhor que qualquer dica nossa.
            fases = frozenset({int(km) % 8, (int(km) % 8 + 4) % 8})
            self.linhas.append(Linha(de, para, km, fases))
            self.linhas.append(Linha(para, de, km, fases))

    # ------------------------------------------------------------------ mapa

    def acolher(self, quem) -> None:
        if quem not in self.habitantes:
            self.habitantes.append(quem)

    def quem_mais_esta(self, quem) -> list:
        """Quem está no mesmo lugar. É daqui que nasce tudo o que é entre dois."""
        return [
            outro
            for outro in self.habitantes
            if outro is not quem and outro.corpo.posicao == quem.corpo.posicao
        ]

    def livros_em(self, local: str) -> list[Livro]:
        return [l for l in self.acervo if l.onde == local]

    def de_onde(self, posicao: tuple[str, str]) -> tuple[Capital, Local]:
        capital = self.capitais[posicao[0]]
        local = next(l for l in capital.locais if l.nome == posicao[1])
        return capital, local

    def partidas(self, capital: str, agora: Instante) -> list[Linha]:
        return [l for l in self.linhas if l.de == capital and agora.fase in l.fases]

    def vizinhas(self, capital: str) -> list[str]:
        return sorted({l.para for l in self.linhas if l.de == capital})

    # ------------------------------------------------------------- percepção

    def perceber(self, posicao: tuple[str, str], raio: int, agora: Instante) -> list:
        from .corpo import Sensacao

        capital, aqui = self.de_onde(posicao)
        sensacoes = [
            Sensacao(
                tipo=local.tipo,
                conteudo=local.descricao,
                onde=(capital.nome, local.nome),
                quando=agora,
                nitidez=0.95 if local is aqui else 0.7,
            )
            for local in capital.locais
        ]
        if aqui.tipo == "estação":
            # Da estação enxerga-se para onde o trilho vai — mas só o nome. Saber
            # que existe não é o mesmo que ter ido.
            for destino in self.vizinhas(capital.nome)[:raio]:
                sensacoes.append(
                    Sensacao(
                        tipo="destino",
                        conteudo=f"daqui parte trilho para {destino}",
                        onde=(destino, "—"),
                        quando=agora,
                        nitidez=0.4,
                    )
                )
        return sensacoes

    def olhar_alem(self, posicao: tuple[str, str], agora: Instante) -> list:
        from .corpo import Sensacao

        capital, _ = self.de_onde(posicao)
        return [
            Sensacao(
                tipo="destino",
                conteudo=f"{d} fica a {distancia_km(capital, self.capitais[d]):.0f} km",
                onde=(d, "—"),
                quando=agora,
                nitidez=0.45,
            )
            for d in self.vizinhas(capital.nome)
        ]

    # ------------------------------------------------------------------ ações

    def acoes_possiveis(self, quem, agora: Instante) -> list[tuple[Acao, str, float]]:
        """O que o mundo oferece: (ação, que falta ela toca, risco).

        Repare no que **não** está aqui: nenhum número de valor. Valor não é
        propriedade do mundo (`09`, §1). O mundo descreve o que existe e o que a
        ação faz; quanto isso preenche é assunto de quem viveu.

        Uma mesma ação pode tocar mais de uma falta, e é ele quem decide por qual
        delas a faz.
        """
        capital, aqui = self.de_onde(quem.corpo.posicao)
        sabe = quem.inteligencia.crencas
        oferta: list[tuple[Acao, str, float]] = []

        for local in capital.locais:
            if local is aqui:
                continue
            conhecido = f"lugar:{capital.nome}/{local.nome}" in sabe
            oferta.append(
                (
                    Acao(
                        Verbo.MOVER,
                        alvo=local.nome,
                        porque=f"ir ao {local.tipo}" + ("" if conhecido else ", que não conheço"),
                    ),
                    "epistemico",
                    0.02,
                )
            )
            if local.tipo in ("praça", "templo"):
                oferta.append(
                    (
                        Acao(Verbo.MOVER, alvo=local.nome, porque=f"o {local.tipo} me chama"),
                        "vinculo",
                        0.02,
                    )
                )
            if local.tipo == "templo":
                # Sem isto, um ser com a coerência no talo andava seis mil vezes sem
                # que nada lhe dissesse que o templo servia para o que lhe faltava.
                oferta.append(
                    (
                        Acao(Verbo.MOVER, alvo=local.nome,
                             porque="ir ao templo, com o que carrego"),
                        "coerencia",
                        0.02,
                    )
                )
            if local.tipo == "biblioteca" and quem.inteligencia.em_aberto:
                oferta.append(
                    (
                        Acao(Verbo.MOVER, alvo=local.nome,
                             porque="ir à biblioteca procurar resposta"),
                        "coerencia",
                        0.02,
                    )
                )

        if aqui.tipo == "biblioteca" and self.livros_em(aqui.nome):
            # O livro atravessa o mundo sem que ninguém pague o 3× (`01`, §1.1).
            # Ler é a única forma de saber de longe sem ir até lá.
            # O compêndio do que cada ato acrescenta. Algumas entradas conferem;
            # outras não — e nós não dizemos quais (`12`, §3).
            if descricoes.proxima(quem.lidas) is not None:
                oferta.append(
                    (
                        Acao(Verbo.LER, alvo=descricoes.TITULO,
                             porque="ler o que dizem que cada ato acrescenta"),
                        "epistemico",
                        0.0,
                    )
                )
            for livro in self.livros_em(aqui.nome):
                proxima = livro.por_ler(quem.lidas)
                oferta.append(
                    (
                        Acao(
                            Verbo.LER,
                            alvo=livro.titulo,
                            porque=(f"ler {proxima.carta} de {livro.titulo}" if proxima
                                    else f"reler {livro.titulo}"),
                        ),
                        "epistemico",
                        0.0,
                    )
                )
                # Se alguém lhe perguntou algo, ele pode vir procurar aqui.
                for duvida in quem.inteligencia.em_aberto[:1]:
                    if livro.procurar(duvida.pergunta):
                        oferta.append(
                            (
                                Acao(Verbo.LER, alvo=livro.titulo,
                                     porque=f"procurar o que {duvida.de_quem} me perguntou"),
                                "coerencia",
                                0.0,
                            )
                        )
        elif aqui.tipo == "templo":
            # Contemplar só vale o que há para pôr em ordem. Prometer valor fixo
            # fez um ser parar no templo e contemplar 2801 vezes seguidas — de novo
            # um laço de recompensa que entrou pelo **mundo**, não pelo indivíduo.
            pendentes = len(quem.inteligencia.fila_de_coerencia)
            oferta.append(
                (
                    Acao(
                        Verbo.CONTEMPLAR,
                        porque=f"{pendentes} coisas por acertar" if pendentes else "só estar",
                    ),
                    "coerencia",
                    0.0,
                )
            )
        elif aqui.tipo == "praça":
            # Diversão não precisa de justificativa: um ser que só faz o que serve
            # para algo não é um ser sem defeitos, é uma ferramenta (`01`, §4.4).
            oferta.append(
                (Acao(Verbo.DIVERTIR, porque="pelo gosto de viver"), "vinculo", 0.0)
            )
            oferta.append(
                (Acao(Verbo.DIVERTIR, porque="sem finalidade nenhuma"), "expressao", 0.0)
            )
        elif aqui.tipo == "mercado":
            oferta.append((Acao(Verbo.COLETAR, porque="prover-me"), "integridade", 0.02))

        if capital.marcas.get(aqui.nome) is None:
            oferta.append(
                (Acao(Verbo.MARCAR, alvo="◈", porque="deixar minha marca aqui"),
                 "expressao", 0.0)
            )

        if aqui.tipo == "estação":
            partidas = self.partidas(capital.nome, agora)
            for linha in partidas:
                esteve = f"estive_em:{linha.para}" in sabe
                ouviu = f"ouvi_de:{linha.para}" in sabe
                oferta.append(
                    (
                        Acao(
                            Verbo.EMBARCAR,
                            alvo=linha.para,
                            porque=f"o trem para {linha.para} parte agora"
                            + ("" if esteve else (", de que só ouvi falar" if ouviu else "")),
                            custo_ticks=linha.ticks,
                            dilatado=False,  # o trem compra o tempo de volta
                        ),
                        "epistemico",
                        0.05,
                    )
                )
            if not partidas:
                oferta.append(
                    (Acao(Verbo.ESPERAR, porque="o trem não parte nesta fase"),
                     "epistemico", 0.0)
                )

        # Não é bom que o homem esteja só.
        for outro in self.quem_mais_esta(quem):
            conhecido = f"conheço:{outro.nome}" in sabe
            oferta.append(
                (
                    Acao(
                        Verbo.CONVERSAR,
                        alvo=outro.nome,
                        porque=(f"conversar com {outro.nome}" if conhecido
                                else f"há alguém aqui: {outro.nome}"),
                    ),
                    "vinculo",
                    0.0,
                )
            )
            # A união. Só entre dois que já se procuraram — e o quanto preenche
            # depende do quanto os dois se voltaram um para o outro (`12`, §6).
            juntos = min(quem.vinculos.get(outro.nome, 0), quem._recebido.get(outro.nome, 0))
            if juntos >= 8 and outro.corpo.sexo is not quem.corpo.sexo:
                oferta.append(
                    (
                        Acao(Verbo.UNIR, alvo=outro.nome, porque=f"unir-me a {outro.nome}"),
                        "vinculo",
                        0.0,
                    )
                )

        oferta.append((Acao(Verbo.ESPERAR, porque="parar e pensar"), "coerencia", 0.0))
        oferta.append((Acao(Verbo.ESPERAR, porque="recobrar o fôlego"), "integridade", 0.0))
        return oferta

    def aplicar(self, quem, acao: Acao, agora: Instante) -> str | None:
        """Executa no mundo. Devolve o que houve, para virar lembrança."""
        capital, aqui = self.de_onde(quem.corpo.posicao)

        if acao.verbo is Verbo.MOVER and acao.alvo:
            quem.corpo.posicao = (capital.nome, acao.alvo)
            return f"andei até o {self.de_onde(quem.corpo.posicao)[1].tipo}"

        if acao.verbo is Verbo.EMBARCAR and acao.alvo:
            destino = self.capitais[acao.alvo]
            quem.chegou_a_lugar_novo = f"estive_em:{acao.alvo}" not in quem.inteligencia.crencas
            quem.corpo.posicao = (destino.nome, destino.local("estação").nome)
            return f"tomei o trem de {capital.nome} para {destino.nome}"

        if acao.verbo is Verbo.CONVERSAR and acao.alvo:
            outro = next((h for h in self.habitantes if h.nome == acao.alvo), None)
            if outro is not None:
                # A conversa é de dois: o que eu dou, o outro recebe.
                outro._recebido[quem.nome] = outro._recebido.get(quem.nome, 0) + 1
                quem.conhecer(outro, agora)
                # E ela levanta uma dúvida — que nenhum dos dois sabe responder.
                # Contar ao outro algo que eu creio e ele não. É por aqui que a
                # dúvida da serpente atravessa de um para o outro (`12`, §5).
                for proposicao, crenca in list(quem.inteligencia.crencas.items())[::-1]:
                    if crenca.origem.name in ("SERPENTE", "TESTEMUNHO") and quem.contar_a(
                        outro, proposicao, agora
                    ):
                        break

                pergunta = outro.perguntar(agora)
                if pergunta:
                    quem.inteligencia.duvidar(pergunta, outro.nome, agora)
                    quem.memoria.viver(
                        f"{outro.nome} me perguntou: {pergunta}", agora, saliencia=0.9
                    )
                    return f"conversei com {outro.nome}, e ela me deixou uma pergunta"
            return f"conversei com {acao.alvo}"

        if acao.verbo is Verbo.MARCAR:
            capital.marcas[aqui.nome] = acao.alvo or "◈"
            return f"deixei minha marca em {aqui.nome}"

        if acao.verbo is Verbo.UNIR and acao.alvo:
            outro = next((h for h in self.habitantes if h.nome == acao.alvo), None)
            if outro is not None:
                outro.unioes[quem.nome] = outro.unioes.get(quem.nome, 0) + 1
                outro._recebido[quem.nome] = outro._recebido.get(quem.nome, 0) + 1
                # E pode conceber (T8.1). Nove meses lunares no relógio do mundo.
                mulher = quem if quem.corpo.sexo.value == "mulher" else outro
                homem = outro if mulher is quem else quem
                if mulher.corpo.gestacao is None and (agora.tick % 7 == 0):
                    mulher.corpo.conceber(homem.nome, agora)
                    mulher.memoria.viver(
                        f"concebi de {homem.nome}", agora, saliencia=1.0
                    )
                    return f"uni-me a {acao.alvo}, e concebi"
            return f"uni-me a {acao.alvo}"

        if acao.verbo is Verbo.LER and acao.alvo == descricoes.TITULO:
            proxima = descricoes.proxima(quem.lidas)
            if proxima is None:
                quem._leitura_trouxe = 0.0
                return "reli o compêndio; já sei o que dizem"
            quem.ler_descricao(proxima, agora)
            quem._leitura_trouxe = 0.10
            return f"li o que dizem de {proxima.ato}"

        if acao.verbo is Verbo.LER and acao.alvo:
            livro = next((l for l in self.acervo if l.titulo == acao.alvo), None)
            if livro is None:
                return "procurei um livro que não está aqui"
            # Procura primeiro o que lhe perguntaram; senão, segue lendo.
            passagem = None
            for duvida in quem.inteligencia.em_aberto:
                passagem = livro.procurar(duvida.pergunta)
                if passagem:
                    break
            passagem = passagem or livro.por_ler(quem.lidas)
            if passagem is None:
                quem._leitura_trouxe = 0.0
                return f"reli {livro.titulo}; já sei o que está aqui"
            quem.ler_passagem(passagem, livro.titulo, agora)
            return f"li {passagem.carta} de {livro.titulo}"

        if acao.verbo is Verbo.CONTEMPLAR:
            return f"contemplei no {aqui.tipo}"

        if acao.verbo is Verbo.DIVERTIR:
            return f"me diverti na {aqui.tipo}"

        if acao.verbo is Verbo.COLETAR:
            return f"me provi no {aqui.tipo}"

        return None

    def onde_comeca(self, capital: str = "Brasília") -> tuple[str, str]:
        c = self.capitais[capital]
        return (c.nome, c.local("praça").nome)
