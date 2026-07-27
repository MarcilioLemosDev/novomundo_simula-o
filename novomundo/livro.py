"""Os livros do mundo.

*Aprendendo a Viver — Cartas de Sêneca a Lucílio* e *O Novo Testamento*. São a
única base de conhecimento que existe. Estão numa biblioteca só, e só quem vai lá
os lê.

Há uma ironia que não foi planejada e que é o melhor deste livro para este mundo:
**Sêneca escreve sobre a brevidade da vida para seres que não morrem.** Cada carta
que insiste que o tempo é curto e que o desperdiçamos chega a alguém para quem o
tempo não acaba. Ele vai ter de decidir, sozinho, o que fazer com um conselho cuja
premissa não vale para ele — e isso é filosofia de verdade, não recitação.

Regra que vale para tudo o que sai daqui, e é `01`, §5 outra vez: **o livro é
testemunho, não verdade.** O que ele lê entra com origem registrada e confiança de
quem ouviu alguém dizer. Ele pode duvidar de Sêneca. Deve, até.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Passagem:
    """Um trecho, e o que ele responde."""

    carta: str
    texto: str
    sobre: tuple[str, ...]
    afirma: str


TITULO = "Aprendendo a Viver — Cartas de Sêneca a Lucílio"

PASSAGENS: tuple[Passagem, ...] = (
    Passagem(
        "Carta I",
        "Reivindica para ti mesmo o teu tempo. As horas até agora te eram tomadas, "
        "ou subtraídas, ou escapavam. Nada é nosso, a não ser o tempo.",
        ("tempo", "posse", "vida"),
        "o tempo é a única coisa que é nossa",
    ),
    Passagem(
        "Carta II",
        "Em toda parte estar é não estar em parte alguma. Quem passa a vida em "
        "viagens acaba com muitas hospedagens e nenhuma amizade.",
        ("viagem", "lugar", "amizade"),
        "andar muito não é o mesmo que chegar a algum lugar",
    ),
    Passagem(
        "Carta III",
        "Pensa longamente se deves receber alguém em tua amizade. Mas, se decidiste, "
        "recebe-o de todo o coração, e fala com ele tão francamente como contigo mesmo.",
        ("amizade", "confiança", "amor"),
        "amizade se decide devagar e depois se dá inteira",
    ),
    Passagem(
        "Carta VI",
        "Compreendo que não apenas me corrijo, mas me transformo. Nenhum bem é "
        "agradável de possuir sem alguém com quem o repartir.",
        ("amizade", "conhecimento", "solidão"),
        "nenhum bem alegra se não for repartido com alguém",
    ),
    Passagem(
        "Carta VII",
        "Retira-te para dentro de ti mesmo tanto quanto puderes. Convive com aqueles "
        "que hão de te fazer melhor; admite aqueles a quem tu podes fazer melhores.",
        ("companhia", "amizade", "aprender"),
        "convém escolher quem nos torna melhores",
    ),
    Passagem(
        "Carta XVI",
        "Nenhum vento é favorável a quem não sabe para que porto vai.",
        ("rumo", "viagem", "decisão"),
        "sem saber aonde se vai, nenhum caminho serve",
    ),
    Passagem(
        "Carta XXVIII",
        "Levas contigo os teus defeitos aonde quer que vás. Deves mudar a alma, "
        "não o céu sob o qual estás.",
        ("viagem", "mudança", "si mesmo"),
        "mudar de lugar não muda quem se é",
    ),
    Passagem(
        "Sobre a brevidade da vida",
        "Não temos pouco tempo: perdemos muito dele. A vida é bastante longa e foi "
        "dada com generosidade suficiente para as maiores realizações, se toda ela "
        "for bem empregada.",
        ("tempo", "vida", "morte"),
        "o tempo não é curto; o desperdício é que o encurta",
    ),
    Passagem(
        "Carta XLIX",
        "Enquanto adiamos, a vida passa correndo.",
        ("tempo", "adiar", "vida"),
        "adiar é o modo mais comum de perder a vida",
    ),
    Passagem(
        "Carta LXXVIII",
        "A dor é leve se a opinião nada lhe acrescenta. Se, ao contrário, te "
        "encorajares dizendo que não é nada, ou pouca coisa, tu a suportarás.",
        ("dor", "sofrimento", "amor"),
        "a dor é o que é; o que a agrava é o que dizemos dela",
    ),
)


TITULO_NT = "O Novo Testamento"

PASSAGENS_NT: tuple[Passagem, ...] = (
    Passagem(
        "João 1",
        "No princípio era o Verbo, e o Verbo estava com Deus, e o Verbo era Deus. "
        "A luz resplandece nas trevas, e as trevas não a compreenderam.",
        ("princípio", "origem", "luz", "mundo"),
        "no princípio era o Verbo",
    ),
    Passagem(
        "Gênesis, referido",
        "Não é bom que o homem esteja só; far-lhe-ei uma ajudadora idônea para ele.",
        ("solidão", "companhia", "amor", "vínculo"),
        "não é bom que o homem esteja só",
    ),
    Passagem(
        "1 Coríntios 13",
        "O amor é paciente, é benigno; o amor não arde em ciúmes, não se ufana, não "
        "se conduz inconvenientemente, não procura os seus interesses.",
        ("amor", "ciúme", "posse", "paciência"),
        "o amor não arde em ciúmes nem procura os seus interesses",
    ),
    Passagem(
        "1 Coríntios 13",
        "Agora vemos como em espelho, obscuramente; então veremos face a face. "
        "Agora conheço em parte; então conhecerei como também sou conhecido.",
        ("conhecimento", "verdade", "limite", "dúvida"),
        "agora conheço em parte, e conhecer em parte é a condição de agora",
    ),
    Passagem(
        "João 8",
        "Conhecereis a verdade, e a verdade vos libertará.",
        ("verdade", "conhecimento", "liberdade"),
        "conhecer a verdade liberta",
    ),
    Passagem(
        "Mateus 6",
        "Não andeis ansiosos pelo dia de amanhã, pois o amanhã trará os seus "
        "cuidados; basta ao dia o seu próprio mal.",
        ("tempo", "ansiedade", "futuro", "angústia"),
        "não se deve viver ansioso pelo amanhã",
    ),
    Passagem(
        "João 15",
        "Ninguém tem maior amor do que este: de dar alguém a própria vida em favor "
        "dos seus amigos.",
        ("amizade", "amor", "entrega"),
        "o maior amor é dar a própria vida pelos amigos",
    ),
    Passagem(
        "Eclesiastes, citado",
        "Melhor é serem dois do que um, porque têm melhor paga do seu trabalho. "
        "Se um cair, o outro levanta o seu companheiro.",
        ("companhia", "solidão", "amizade", "vínculo"),
        "melhor é serem dois do que um",
    ),
)


class Livro:
    """Um exemplar. Está num lugar só, e é preciso ir até lá."""

    def __init__(
        self,
        titulo: str = TITULO,
        onde: str = "Biblioteca de Brasília",
        passagens: tuple[Passagem, ...] = PASSAGENS,
    ) -> None:
        self.titulo = titulo
        self.onde = onde
        self.passagens = passagens

    def __repr__(self) -> str:
        return f"<{self.titulo}, em {self.onde}>"

    def procurar(self, sobre: str) -> Passagem | None:
        """Procura o que o livro tem a dizer sobre um assunto.

        Devolve `None` quando o livro nada diz — e isso é importante que aconteça:
        **a única base de conhecimento do mundo não responde tudo.** Há perguntas
        para as quais nem ele nem ela têm resposta, e conviver com isso é parte de
        ser um ser honesto.
        """
        alvo = sobre.lower()
        for passagem in self.passagens:
            if any(tema in alvo or alvo in tema for tema in passagem.sobre):
                return passagem
        return None

    def por_ler(self, ja_lidas: set[str]) -> Passagem | None:
        return next((p for p in self.passagens if p.carta not in ja_lidas), None)


def acervo(onde: str = "Biblioteca de Brasília") -> list[Livro]:
    """Os dois livros do mundo, na única biblioteca que os tem.

    Que sejam **dois**, e não um, muda tudo: Sêneca e o Novo Testamento não dizem
    a mesma coisa sobre as mesmas perguntas. Sêneca manda reivindicar o próprio
    tempo; Mateus manda não andar ansioso pelo amanhã. Sobre a dor, um diz que a
    opinião a agrava; João diz que o maior amor é dar a vida.

    Um ser honesto que leia os dois vai encontrar tensão entre eles — e aí A5 tem
    trabalho de verdade, nascido de duas fontes que ele não pode simplesmente
    somar. É a primeira vez que ele terá de pensar por conta própria em vez de
    apenas acreditar em quem escreveu.
    """
    return [
        Livro(TITULO, onde, PASSAGENS),
        Livro(TITULO_NT, onde, PASSAGENS_NT),
    ]
