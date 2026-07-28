"""As razões — o que faz alguém agir por querer, e não por compensar.

O cálculo informa. Quem escolhe é a vontade.

Antes desta camada, o indivíduo escolhia sempre o de maior valor esperado. Um ser
assim nunca erra por vontade — erra só por ignorância — e não faz *porque quer*:
faz porque compensa. É um otimizador educado, não um ser livre.

Uma razão não é um número. É um motivo que ele sustenta, e **pode vencer um valor
maior**: ele pode escolher o que rende menos, sabendo que rende menos, e o diário
dirá exatamente isso.

Isto não é ruído. Ruído não é liberdade — um dado jogado não é mais livre do que uma
conta. É outra coisa: ele age por um motivo, e o motivo é dele.

Ver `docs/12-o-livre-arbitrio-e-a-serpente.md`, §2.
"""

from __future__ import annotations

from dataclasses import dataclass


def onde_tipo(onde: str) -> str:
    """O tipo do lugar, a partir do nome. "Praça de Lima" → "praça"."""
    return onde.split(" de ")[0].strip().lower() if onde else ""


@dataclass(frozen=True)
class Razao:
    """Um motivo para fazer algo que não é o proveito de fazê-lo."""

    tipo: str
    dito: str  # como ele diz isso a si mesmo, no diário
    peso: float  # o quanto puxa. Pode ultrapassar a diferença de valor.

    def __str__(self) -> str:
        return self.dito


def razoes_para(acao, drive: str, quem, onde: str) -> list[Razao]:
    """Que motivos este ser tem para fazer isto, além do que aquilo lhe rende.

    Lê o estado dele — aspirações, vínculos, fé, o que leu, o que nunca fez. Nada
    aqui é uma regra de comportamento: são as razões que a vida dele já criou.
    """
    razoes: list[Razao] = []
    alvo = acao.alvo or ""

    # ── porque eu quero ────────────────────────────────────────────────────
    # A aspiração não tem valor de verdade e não paga nada. Move mesmo assim —
    # é para isso que ela existe (`01`, §4.3).
    for aspiracao in quem.inteligencia.aspiracoes:
        if aspiracao.realizada or not aspiracao.alvos:
            continue
        # Casa pelo que ele **entendeu** do desejo, não pela letra da frase. Antes
        # era comparação de palavras soltas, e o resultado era zero: o Senhor
        # plantava uma vontade e ela não puxava ação nenhuma.
        if (
            acao.verbo.value in aspiracao.alvos
            or alvo in aspiracao.alvos
            or onde_tipo(onde) in aspiracao.alvos
        ):
            razoes.append(
                Razao("querer", f"porque eu quero: {aspiracao.desejo}", aspiracao.intensidade)
            )
            break

    # ── porque ela está lá ─────────────────────────────────────────────────
    # O vínculo puxa para onde está quem se ama, ainda que ali não haja proveito.
    for nome, dei in quem.vinculos.items():
        if nome and (nome in alvo or nome in acao.porque):
            recebi = quem._recebido.get(nome, 0)
            razoes.append(
                Razao("vinculo", f"porque é {nome}", min(0.9, 0.2 + 0.02 * min(dei, recebi)))
            )
            break

    # ── porque prometi ─────────────────────────────────────────────────────
    for compromisso in getattr(quem, "compromissos", []):
        if compromisso.devendo and compromisso.serve(acao):
            razoes.append(
                Razao(
                    "promessa",
                    f"porque prometi: {compromisso.o_que} (devo {compromisso.faltando})",
                    0.55,
                )
            )
            break

    # ── porque nunca fiz ───────────────────────────────────────────────────
    if not quem.experiencia.conhece((acao.verbo.value, alvo or onde)):
        razoes.append(Razao("curiosidade", "porque nunca fiz isto", 0.35))

    # ── porque li que ──────────────────────────────────────────────────────
    # Aqui entra o erro honesto: ele leu que aquilo agrega, e pode não agregar.
    esperado = quem.esperado_por_leitura.get(acao.verbo.value)
    if esperado:
        razoes.append(Razao("leitura", f"porque li que {esperado}", 0.45))

    # ── porque confio nEle ─────────────────────────────────────────────────
    if quem.inteligencia.fe is not None and acao.verbo.value in ("contemplar", "conversar"):
        razoes.append(
            Razao("fe", f"porque confio em {quem.inteligencia.fe.em_quem}",
                  0.3 * quem.inteligencia.fe.firmeza)
        )

    return razoes


def puxao(razoes: list[Razao]) -> float:
    """O quanto as razões juntas puxam. Não somam de forma ingênua: a mais forte
    manda, e as outras acrescentam pouco — como acontece com gente."""
    if not razoes:
        return 0.0
    pesos = sorted((r.peso for r in razoes), reverse=True)
    return pesos[0] + sum(p * 0.25 for p in pesos[1:])
