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

    def acoes_possiveis(self, quem, agora: Instante) -> list[tuple[Acao, str, float, float]]:
        """O que o mundo oferece: (ação, drive servido, ganho, risco).

        O mundo **descreve afordâncias**; a escolha é dele. Uma mesma ação pode
        servir a mais de uma falta, e é ele quem decide por qual delas a faz.
        """
        capital, aqui = self.de_onde(quem.corpo.posicao)
        sabe = quem.inteligencia.crencas
        oferta: list[tuple[Acao, str, float, float]] = []

        for local in capital.locais:
            if local is aqui:
                continue
            conhecido = f"lugar:{capital.nome}/{local.nome}" in sabe
            oferta.append(
                (
                    Acao(Verbo.MOVER, alvo=local.nome, porque=f"ir ao {local.tipo}"),
                    "epistemico",
                    0.12 if conhecido else 0.45,  # o já sabido não paga mais: é o tédio
                    0.02,
                )
            )
            if local.tipo in ("praça", "templo"):
                oferta.append(
                    (
                        Acao(Verbo.MOVER, alvo=local.nome, porque=f"o {local.tipo} me chama"),
                        "vinculo",
                        0.32,
                        0.02,
                    )
                )

        if aqui.tipo == "biblioteca":
            # O livro atravessa o mundo sem que ninguém pague o 3× (`01`, §1.1).
            # Ler é a única forma de saber de longe sem ir até lá.
            por_ler = [c for c in self.capitais if f"ouvi_de:{c}" not in sabe]
            oferta.append(
                (
                    Acao(Verbo.LER, alvo=por_ler[0] if por_ler else None,
                         porque="ler é ir sem andar"),
                    "epistemico",
                    0.6 if por_ler else 0.1,
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
                    Acao(Verbo.CONTEMPLAR,
                         porque=f"{pendentes} coisas por acertar" if pendentes else "só estar"),
                    "coerencia",
                    min(0.6, 0.1 + 0.12 * pendentes),
                    0.0,
                )
            )
        elif aqui.tipo == "praça":
            # Diversão não precisa de justificativa: um ser que só faz o que serve
            # para algo não é um ser sem defeitos, é uma ferramenta (`01`, §4.4).
            oferta.append(
                (Acao(Verbo.DIVERTIR, porque="pelo gosto de viver"), "vinculo", 0.5, 0.0)
            )
            oferta.append(
                (Acao(Verbo.DIVERTIR, porque="sem finalidade nenhuma"), "expressao", 0.3, 0.0)
            )
        elif aqui.tipo == "mercado":
            oferta.append((Acao(Verbo.COLETAR, porque="prover-me"), "integridade", 0.45, 0.02))

        if capital.marcas.get(aqui.nome) is None:
            oferta.append(
                (Acao(Verbo.MARCAR, alvo="◈", porque="deixar minha marca aqui"),
                 "expressao", 0.5, 0.0)
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
                            porque=f"o trem para {linha.para} parte agora",
                            custo_ticks=linha.ticks,
                            dilatado=False,  # o trem compra o tempo de volta
                        ),
                        "epistemico",
                        0.25 if esteve else (0.9 if ouviu else 0.6),
                        0.05,
                    )
                )
            if not partidas:
                oferta.append(
                    (Acao(Verbo.ESPERAR, porque="o trem não parte nesta fase"),
                     "epistemico", 0.15, 0.0)
                )

        oferta.append((Acao(Verbo.ESPERAR, porque="parar e pensar"), "coerencia", 0.2, 0.0))
        oferta.append((Acao(Verbo.ESPERAR, porque="recobrar o fôlego"), "integridade", 0.28, 0.0))
        return oferta

    def aplicar(self, quem, acao: Acao, agora: Instante) -> str | None:
        """Executa no mundo. Devolve o que houve, para virar lembrança."""
        capital, aqui = self.de_onde(quem.corpo.posicao)

        if acao.verbo is Verbo.MOVER and acao.alvo:
            quem.corpo.posicao = (capital.nome, acao.alvo)
            return f"andei até o {self.de_onde(quem.corpo.posicao)[1].tipo}"

        if acao.verbo is Verbo.EMBARCAR and acao.alvo:
            destino = self.capitais[acao.alvo]
            quem.corpo.posicao = (destino.nome, destino.local("estação").nome)
            return f"tomei o trem de {capital.nome} para {destino.nome}"

        if acao.verbo is Verbo.MARCAR:
            capital.marcas[aqui.nome] = acao.alvo or "◈"
            return f"deixei minha marca em {aqui.nome}"

        if acao.verbo is Verbo.LER:
            return f"li sobre {acao.alvo}" if acao.alvo else "reli o que já sabia"

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
