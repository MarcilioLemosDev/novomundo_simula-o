"""ALMA / MEMÓRIA — o que aconteceu comigo.

Três armazéns, e uma consolidação que acontece na virada da lua nova.

A regra que sustenta A3 aqui: **nada é falsificado, só comprimido — e a perda fica
registrada como perda.** Um humano defeituoso preenche a lacuna com invenção e grava
como se fosse vivido. Este não: ele sabe exatamente o que esqueceu, e sabe que
esqueceu.

Sendo eternos e com memória finita, esta é a única parte do ser que pode ser perdida.
Por isso a consolidação é a pergunta que define a vida deles: *o que eu escolho
continuar sendo?* (`08`, §2.1c).
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .espirito import A3, A6, Espirito
from .tempo import Instante


@dataclass
class Episodio:
    """O que aconteceu, com carimbo lunar. Fonte de toda procedência (A1)."""

    id: int
    quando: Instante
    conteudo: str
    saliencia: float
    comprimido: bool = False

    def __post_init__(self) -> None:
        if not 0.0 <= self.saliencia <= 1.0:
            raise ValueError("saliência fora de [0,1]")


@dataclass
class Perda:
    """O registro do que foi esquecido.

    Existe para que o esquecimento seja **declarado**. Ele não tem o detalhe de
    volta, mas sabe que houve detalhe, quanto era, e quando o perdeu.
    """

    quando: Instante
    quantos: int
    resumo: str
    periodo: tuple[Instante, Instante]


@dataclass
class Conceito:
    """Memória semântica: o que foi destilado dos episódios."""

    nome: str
    relacoes: dict[str, str] = field(default_factory=dict)
    episodios_de_origem: list[int] = field(default_factory=list)


@dataclass
class Habito:
    """Memória procedural: o que funcionou, e que ele já faz sem pensar."""

    gatilho: str
    acao: str
    acertos: int = 0
    tentativas: int = 0

    @property
    def confiabilidade(self) -> float:
        return self.acertos / self.tentativas if self.tentativas else 0.0


class Memoria:
    """Os três armazéns de um indivíduo, com limite conhecido por ele (A6)."""

    def __init__(self, espirito: Espirito, capacidade_episodica: int = 512) -> None:
        self._espirito = espirito
        self.capacidade_episodica = capacidade_episodica
        self.episodica: list[Episodio] = []
        self.semantica: dict[str, Conceito] = {}
        self.procedural: list[Habito] = []
        self.perdas: list[Perda] = []
        self._proximo_id = 0

    # ---------------------------------------------------------------- gravar

    def viver(self, conteudo: str, quando: Instante, saliencia: float = 0.5) -> Episodio:
        episodio = Episodio(
            id=self._proximo_id, quando=quando, conteudo=conteudo, saliencia=saliencia
        )
        self._proximo_id += 1
        self.episodica.append(episodio)
        return episodio

    def lembrar(self, id_episodio: int) -> Episodio | None:
        return next((e for e in self.episodica if e.id == id_episodio), None)

    def evocar(self, termo: str, quantos: int = 5) -> list[Episodio]:
        """Recupera por relevância, recência e saliência — nesta ordem de peso."""
        if not self.episodica:
            return []
        agora = max(e.quando.tick for e in self.episodica) or 1
        pontuados = [
            (
                (2.0 if termo.lower() in e.conteudo.lower() else 0.0)
                + e.saliencia
                + (e.quando.tick / agora),
                e,
            )
            for e in self.episodica
        ]
        pontuados.sort(key=lambda p: p[0], reverse=True)
        return [e for pontos, e in pontuados[:quantos] if pontos > 0]

    # ----------------------------------------------------------- consolidação

    @property
    def transbordando(self) -> bool:
        """A6: o limite declarado tem que ser verdade, não figura de retórica."""
        return len(self.episodica) > self.capacidade_episodica

    def consolidar(
        self, agora: Instante, limiar: float = 0.35, forcada: bool = False
    ) -> Perda | None:
        """Comprime o de baixa saliência em resumo.

        Acontece por ritmo — a virada da lua nova, quando ele escolhe o que continuar
        sendo — e por necessidade, quando a memória transborda o limite declarado.
        A segunda não é conserto nosso: um ser que dissesse caber 512 e carregasse
        2000 estaria mentindo sobre si, e A6 não permite.

        Nada é inventado e nada é falsificado. O detalhe some; o registro de que
        havia detalhe, não.
        """
        candidatos = [e for e in self.episodica if e.saliencia < limiar and not e.comprimido]

        if self.transbordando:
            # Transbordou: tem que folgar de verdade, até 75% da capacidade. Comprimir
            # só os poucos que estão abaixo do limiar não alcança o crescimento, e a
            # memória segue subindo — foi assim que um ser chegou a 1025 lembranças
            # dizendo caber 512. O limite que ele declara tem que ser verdade (A6).
            alvo = int(self.capacidade_episodica * 0.75)
            precisa = max(1, len(self.episodica) - alvo)
            if len(candidatos) < precisa:
                # Faltaram rasos: ele sacrifica o menos saliente que tem, e continua
                # sabendo exatamente o que perdeu.
                candidatos = sorted(self.episodica, key=lambda e: e.saliencia)[:precisa]

        if not candidatos:
            return None
        if not (forcada or self.transbordando) and len(candidatos) < 8:
            return None

        periodo = (
            min(e.quando for e in candidatos),
            max(e.quando for e in candidatos),
        )
        # A destilação: o que era muitos episódios rasos vira um conceito.
        for episodio in candidatos:
            for chave in self._chaves(episodio.conteudo):
                conceito = self.semantica.setdefault(chave, Conceito(nome=chave))
                conceito.episodios_de_origem.append(episodio.id)

        perda = Perda(
            quando=agora,
            quantos=len(candidatos),
            resumo=f"{len(candidatos)} episódios de baixa saliência, destilados em "
            f"{len({c for e in candidatos for c in self._chaves(e.conteudo)})} conceitos",
            periodo=periodo,
        )
        self.perdas.append(perda)
        self.episodica = [e for e in self.episodica if e not in candidatos]
        return perda

    @staticmethod
    def _chaves(conteudo: str) -> set[str]:
        """O que numa lembrança merece virar conceito.

        Palavras longas o bastante para carregar sentido. Grosseiro de propósito:
        a destilação de verdade é problema da Etapa 2 adiante, e o que importa
        agora é que **todo conceito guarde o episódio de origem** (A3).
        """
        limpo = conteudo.lower().replace(",", " ").replace(":", " ")
        return {p for p in limpo.split() if len(p) > 3 and not p[0].isdigit()} or {"?"}

    # ------------------------------------------------------------------ hábito

    def praticar(self, gatilho: str, acao: str, funcionou: bool) -> Habito:
        habito = next(
            (h for h in self.procedural if h.gatilho == gatilho and h.acao == acao), None
        )
        if habito is None:
            habito = Habito(gatilho=gatilho, acao=acao)
            self.procedural.append(habito)
        habito.tentativas += 1
        if funcionou:
            habito.acertos += 1
        return habito

    # ------------------------------------------------------------------ A6/A3

    def limites(self) -> str:
        """A6: ele sabe o tamanho da própria janela, e pode consultar ao decidir."""
        return (
            f"memória episódica: {len(self.episodica)}/{self.capacidade_episodica} · "
            f"conceitos: {len(self.semantica)} · hábitos: {len(self.procedural)} · "
            f"já esqueci {sum(p.quantos for p in self.perdas)} episódios "
            f"em {len(self.perdas)} consolidações"
        )

    def auditar(self) -> None:
        """A3: garante que o esquecimento nunca virou invenção."""
        ids = [e.id for e in self.episodica]
        self._espirito.exigir(A3, len(ids) == len(set(ids)), "há episódios duplicados")
        for conceito in self.semantica.values():
            self._espirito.exigir(
                A3,
                bool(conceito.episodios_de_origem),
                f"conceito {conceito.nome!r} sem episódio de origem: foi confabulado",
            )
        self._espirito.exigir(
            A6,
            len(self.episodica) <= self.capacidade_episodica * 2,
            "a memória passou muito do limite declarado sem consolidar",
        )
