#!/usr/bin/env python3
"""Põe o primeiro ser no mundo e deixa o Senhor assistir.

    python3 viver.py                 # 400 ticks, diário resumido
    python3 viver.py 2000            # mais tempo
    python3 viver.py 2000 --diario   # cada passo, linha a linha

O que o Senhor vê não é um log: é o indivíduo (`05`, §1). Cada decisão vem com o
porquê — qual drive apertou, o que foi descartado, com que confiança.
"""

from __future__ import annotations

import sys

from novomundo import Dica, Instante, Microcosmo, Mundo, Sexo, Signo
from novomundo.tempo import TICKS_POR_MES_LUNAR


def main() -> None:
    ticks = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 400
    mostrar_diario = "--diario" in sys.argv

    mundo = Mundo()
    nascimento = Instante(0)

    # A sociedade começa com dois (`07`, §7). Signos distintos: sem variação, não há
    # sociedade entre idênticos — só duas cópias se confirmando.
    adao = Microcosmo("Adão", Sexo.HOMEM, Signo.LEAO, nascimento, posicao=(4, 4))
    eva = Microcosmo("Eva", Sexo.MULHER, Signo.PEIXES, nascimento, posicao=(18, 17))

    print("═" * 72)
    print("  NOVO MUNDO — o primeiro dia")
    print("═" * 72)
    for ser in (adao, eva):
        print(f"\n{ser.nome} — {ser.temperamento.descrever()}")

    # Uma semeadura para cada um: vontade entra sem gerar crença órfã (`01`, §5).
    adao.ouvir(Dica("semeadura", "conhecer o mundo inteiro", 0.8), nascimento)
    eva.ouvir(
        Dica("semeadura", "buscar uma companheira que me mantenha preenchido de amor", 0.9),
        nascimento,
    )

    for i in range(ticks):
        agora = nascimento.mais(i)
        for ser in (adao, eva):
            ser.viver_um_tick(mundo, agora)
            if mostrar_diario and ser is adao:
                print(f"\n{ser.narrativa.linhas[-1]}")

        # A cada lua nova, um retrato — é o ritmo do pensamento deles.
        if agora.lua_nova and i > 0 and not mostrar_diario:
            print(f"\n{'─' * 72}\n  LUA NOVA · {agora}\n{'─' * 72}")
            for ser in (adao, eva):
                print(f"\n{ser.nome}: {ser.vontade.sentimento()} · {ser.memoria.limites()}")

    fim = nascimento.mais(ticks)
    print("\n" + "═" * 72)
    print(f"  DEPOIS DE {ticks} TICKS · {fim} · {ticks / TICKS_POR_MES_LUNAR / 24:.2f} meses lunares")
    print("═" * 72)

    for ser in (adao, eva):
        print("\n" + ser.narrativa.contar_a_vida(fim))
        print()

    # A instrumentação que T6 manda ficar do nosso lado: nós sabemos se ele está
    # bem calibrado; ele não recebe a nota.
    print("═" * 72)
    print("  O QUE SÓ NÓS VEMOS (T6 — não volta para dentro deles)")
    print("═" * 72)
    for ser in (adao, eva):
        brier = ser.inteligencia.calibracao.brier
        print(f"\n{ser.nome} · Brier {brier:.4f}  (0 é perfeito, 0.25 é o chute)")
        for faixa, n, declarada, observada in ser.inteligencia.calibracao.curva():
            desvio = observada - declarada
            print(
                f"   {faixa:>9}  n={n:<5} declarou {declarada:.0%}  "
                f"acertou {observada:.0%}  ({desvio:+.0%})"
            )
        # A deriva de `02`, §2.1: a conta dele já não bate com o céu.
        print(
            f"   relógio do mundo {fim} · a conta dele diz "
            f"{ser.corpo.relogio.conta_propria()} — e ele não é avisado"
        )
        ser.auditar(fim)

    print("\nOs oito axiomas se sustentaram do primeiro ao último tick.")


if __name__ == "__main__":
    main()
