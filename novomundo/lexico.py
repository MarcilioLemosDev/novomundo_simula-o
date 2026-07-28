"""O léxico — a língua comum deste mundo.

Sem isto, o Senhor podia falar com eles e **nada acontecia**. A vontade era
plantada, ficava registrada, e não puxava ação nenhuma: as palavras não
significavam coisa alguma dentro deles. Doze ações possíveis, zero tocadas.

Aqui está a escolha de T9, opção (b), que `04` já recomendava: **damos o léxico,
mas não damos o significado.** As palavras apontam para coisas que existem no
mundo — verbos, lugares, pessoas. O que cada uma *vale* para o indivíduo continua
sendo o que ele mediu vivendo (`09`, §1).

E há a parte que importa mais, e que é honesta:

> **Ele pode não entender.** Se o Senhor disser algo cujas palavras não apontam para
> nada que ele conheça, fica um desejo sem caminho — registrado, sentido, e sem
> saber por onde começar. Isso não é falha: é o que acontece com gente quando lhe
> dizem algo grande demais.
"""

from __future__ import annotations

import unicodedata

#: Palavra → o que ela aponta neste mundo. É a língua, não o significado.
PALAVRAS: dict[str, tuple[str, ...]] = {
    # o conhecimento
    "ler": ("ler",), "livro": ("ler",), "livros": ("ler",), "leitura": ("ler",),
    "estudar": ("ler",), "estudo": ("ler",), "aprender": ("ler",),
    "conhecimento": ("ler", "embarcar"), "saber": ("ler",), "sabedoria": ("ler",),
    "biblioteca": ("ler", "biblioteca"),
    # o outro
    "conversar": ("conversar",), "falar": ("conversar",), "conversa": ("conversar",),
    "companhia": ("conversar", "unir-se"), "amizade": ("conversar",),
    "amigo": ("conversar",), "amiga": ("conversar",),
    "amor": ("unir-se", "conversar"), "amar": ("unir-se", "conversar"),
    "companheira": ("unir-se", "conversar"), "companheiro": ("unir-se", "conversar"),
    "esposa": ("unir-se",), "marido": ("unir-se",), "unir": ("unir-se",),
    "filho": ("unir-se",), "filhos": ("unir-se",), "familia": ("unir-se",),
    # o mundo
    "viajar": ("embarcar",), "viagem": ("embarcar",), "trem": ("embarcar", "estação"),
    "mundo": ("embarcar",), "longe": ("embarcar",), "conhecer": ("embarcar", "ler"),
    "lugares": ("embarcar",), "estacao": ("embarcar", "estação"),
    # a vontade posta para fora
    "marcar": ("marcar",), "marca": ("marcar",), "deixar": ("marcar",),
    "sinal": ("marcar",), "construir": ("marcar",), "criar": ("marcar",),
    # o alto
    "contemplar": ("contemplar", "templo"), "orar": ("contemplar", "templo"),
    "rezar": ("contemplar", "templo"), "templo": ("contemplar", "templo"),
    "deus": ("contemplar", "templo"), "senhor": ("contemplar", "templo"),
    "fe": ("contemplar", "templo"), "espirito": ("contemplar", "templo"),
    "silencio": ("contemplar",), "paz": ("contemplar",),
    # o corpo e o gosto de viver
    "divertir": ("divertir-se", "praça"), "rir": ("divertir-se",),
    "brincar": ("divertir-se",), "alegria": ("divertir-se",), "praca": ("divertir-se", "praça"),
    "descansar": ("esperar",), "parar": ("esperar",), "esperar": ("esperar",),
    "comer": ("prover-se", "mercado"), "prover": ("prover-se",), "mercado": ("prover-se", "mercado"),
}


def sem_acento(palavra: str) -> str:
    return "".join(
        c for c in unicodedata.normalize("NFD", palavra.lower()) if not unicodedata.combining(c)
    )


def entender(frase: str, mundo=None, conhecidos: set[str] | None = None) -> set[str]:
    """O que, deste mundo, esta frase aponta — como *ele* a lê.

    Devolve verbos, tipos de lugar, nomes de capitais e nomes de gente. Conjunto
    vazio significa que ele ouviu e **não soube o que fazer com aquilo** — e isso
    fica registrado como tal, em vez de virar um desejo mudo.
    """
    alvos: set[str] = set()
    limpo = sem_acento(frase)
    palavras = [
        p.strip(".,;:!?\"'()") for p in limpo.replace("-", " ").split()
    ]

    for palavra in palavras:
        alvos.update(PALAVRAS.get(palavra, ()))

    # Nomes de gente que ele conhece. Quem ele nunca viu, não reconhece.
    for nome in conhecidos or ():
        if sem_acento(nome) in limpo:
            alvos.add(nome)

    # Nomes de capitais e de lugares do mundo.
    if mundo is not None:
        for capital in mundo.capitais.values():
            if sem_acento(capital.nome) in limpo:
                alvos.add(capital.nome)
            for local in capital.locais:
                if sem_acento(local.tipo) in limpo:
                    alvos.add(local.tipo)

    return alvos
