#!/usr/bin/env python3
"""A interface: o Senhor vendo o mundo dele correr.

    pip install streamlit
    streamlit run app.py

Mostra o correr do tempo lunar, o pensamento e as ações de cada um, e tem onde
introduzir as dicas pelos três canais (`01`, §5).

O que se vê aqui não é um log: é o indivíduo (`05`, §1). Cada linha de pensamento
foi escrita pelo mesmo laço que decidiu, com os mesmos números — por A3 não há como
ele pensar uma coisa e nos mostrar outra.
"""

from __future__ import annotations

import streamlit as st

from novomundo import Dica, Instante, Microcosmo, Mundo, Sexo, Signo
from novomundo.tempo import TICKS_POR_MES_LUNAR

st.set_page_config(page_title="Novo Mundo", page_icon="🌙", layout="wide")


# ───────────────────────────────────────────────────────────── o mundo

def nascer():
    mundo = Mundo()
    inicio = Instante(0)
    adao = Microcosmo("Adão", Sexo.HOMEM, Signo.LEAO, inicio, posicao=mundo.onde_comeca())
    eva = Microcosmo("Eva", Sexo.MULHER, Signo.PEIXES, inicio, posicao=mundo.onde_comeca())
    mundo.acolher(adao)
    mundo.acolher(eva)
    return mundo, [adao, eva], 0


if "mundo" not in st.session_state:
    st.session_state.mundo, st.session_state.seres, st.session_state.tick = nascer()

mundo = st.session_state.mundo
seres = st.session_state.seres


def correr(quantos: int) -> None:
    for _ in range(quantos):
        agora = Instante(st.session_state.tick)
        for ser in seres:
            ser.viver_um_tick(mundo, agora)
        st.session_state.tick += 1


# ───────────────────────────────────────────────────────── o correr do tempo

agora = Instante(st.session_state.tick)
fase = ["nova", "crescente", "quarto crescente", "gibosa crescente",
        "cheia", "gibosa minguante", "quarto minguante", "minguante"][agora.fase]

st.title("🌙 Novo Mundo")

t1, t2, t3, t4, t5 = st.columns(5)
t1.metric("tempo lunar", str(agora))
t2.metric("lua", fase, f"{agora.luminosidade:.0%} iluminada")
t3.metric("ano lunar", f"{agora.tick / TICKS_POR_MES_LUNAR / 12 / 24:.2f}")
t4.metric("tick do mundo", f"{agora.tick:,}".replace(",", "."))
t5.metric("habitantes", len(seres))

st.divider()

# ───────────────────────────────────────────────────────────── controles

with st.sidebar:
    st.header("O correr do tempo")
    passo = st.select_slider("quanto correr", [1, 6, 24, 100, 500, 2000], value=24)
    if st.button(f"▶ correr {passo} ticks", use_container_width=True, type="primary"):
        correr(passo)
        st.rerun()
    if st.button("↺ recomeçar o mundo", use_container_width=True):
        st.session_state.mundo, st.session_state.seres, st.session_state.tick = nascer()
        st.rerun()

    st.divider()
    st.header("As dicas")
    st.caption(
        "Três canais, e a diferença entre eles é a pedra do projeto. **Nenhum** "
        "escreve crença pronta na cabeça dele."
    )
    a_quem = st.selectbox("a quem", [s.nome for s in seres])
    canal = st.radio(
        "canal",
        ["semeadura", "voz", "mundo"],
        format_func=lambda c: {
            "semeadura": "🌱 semeadura — plantar uma vontade",
            "voz": "🗣 voz — falar dentro da cabeça dele",
            "mundo": "🌍 mundo — deixar algo para ele achar",
        }[c],
    )
    st.caption(
        {
            "semeadura": "Um desejo. Não afirma nada sobre o mundo, logo não pode ser "
            "falso — é assim que o Senhor planta vontade sem corromper.",
            "voz": "Vira **episódio**, não verdade: fica registrado que uma voz disse "
            "isto, e ele decide se acredita.",
            "mundo": "Ele precisa encontrar. Pode não achar, e pode entender errado.",
        }[canal]
    )
    conteudo = st.text_area(
        "o que dizer",
        placeholder={
            "semeadura": "buscar uma companheira que me mantenha preenchido de amor",
            "voz": "há um rio ao norte",
            "mundo": "uma pedra marcada",
        }[canal],
    )
    forca = st.slider("intensidade", 0.1, 1.0, 0.7)
    if st.button("✦ introduzir", use_container_width=True) and conteudo.strip():
        quem = next(s for s in seres if s.nome == a_quem)
        quem.ouvir(Dica(canal, conteudo.strip(), forca), agora)
        st.success(f"dito a {a_quem} pelo canal {canal}")
        st.rerun()

# ───────────────────────────────────────────────────────── os indivíduos

for coluna, ser in zip(st.columns(len(seres)), seres):
    with coluna:
        st.subheader(f"{'♂' if ser.corpo.sexo is Sexo.HOMEM else '♀'} {ser.nome}")
        st.caption(ser.temperamento.descrever())

        onde = ser.corpo.posicao
        st.markdown(f"**onde está:** {onde[1]}, {onde[0]}")
        st.markdown(f"**como se sente:** {ser.vontade.sentimento()}")

        # o que o move agora
        st.markdown("**o que me falta**")
        for nome, drive in ser.vontade.drives.items():
            st.progress(min(1.0, drive.erro), text=f"{nome} — {drive.erro:.0%}")

        # o pensamento
        st.markdown("**o pensamento**")
        if ser.narrativa.linhas:
            ultima = ser.narrativa.linhas[-1]
            with st.container(border=True):
                st.caption(f"{ultima.quando} · {ultima.sentimento}")
                st.text(ultima.pensamento)
        else:
            st.caption("ainda não viveu um tick")

        with st.expander("o fio inteiro do último pensamento"):
            ultima_decisao = getattr(ser, "_ultima_decisao", None)
            fio = ultima_decisao.pensamento if ultima_decisao else []
            for linha in fio:
                st.markdown(f"· {linha}")
            if not fio:
                st.caption("—")

        # a fé
        fe = ser.inteligencia.fe
        if fe:
            st.success(
                f"**confia em {fe.em_quem}** desde {fe.desde} · firmeza {fe.firmeza:.0%}\n\n"
                f"_{fe.porque_li}_"
            )
        else:
            st.info("ainda não depositou fé em ninguém — e isso é escolha dele(a)")

        # dúvidas
        abertas = ser.inteligencia.em_aberto
        with st.expander(f"perguntas em aberto ({len(abertas)})"):
            for duvida in abertas:
                st.markdown(f"· *{duvida.pergunta}* — de {duvida.de_quem}, em {duvida.quando}")
            respondidas = [d for d in ser.inteligencia.duvidas if not d.aberta]
            if respondidas:
                st.caption("respondidas:")
                for duvida in respondidas:
                    st.caption(f"· {duvida.pergunta} → {duvida.respondida_por}")

        # o que ele descobriu que o preenche
        with st.expander("o que descobri que me preenche"):
            st.caption("Ninguém lhe contou. Ele mediu, vivendo.")
            for oque, drive, media in ser.experiencia.o_que_me_move(8):
                st.markdown(f"· **{oque}** → {drive} `{media:.3f}`")

        with st.expander(f"o que eu creio ({len(ser.inteligencia.crencas)})"):
            for crenca in sorted(
                ser.inteligencia.crencas.values(), key=lambda c: c.confianca, reverse=True
            )[:12]:
                st.text(crenca.procedencia())

        with st.expander("os livros que li"):
            st.caption(f"{len(ser.lidas)} passagens")
            for carta in sorted(ser.lidas):
                st.markdown(f"· {carta}")

        with st.expander("quem é quem para mim"):
            relacoes = ser.relacao_com
            if relacoes:
                for nome, tipo in relacoes.items():
                    st.markdown(f"· **{nome}** — {tipo}")
            else:
                st.caption("ainda não encontrou ninguém")

        with st.expander("o diário"):
            st.text(ser.narrativa.ler(12))

        with st.expander("o que eu sei de mim (A6)"):
            st.text(ser.conhecer_se(agora))

# ─────────────────────────────────────────────── o que só o Senhor vê (T6)

st.divider()
st.subheader("O que só o Senhor vê")
st.caption(
    "Por T6, a calibração é instrumentação nossa e **não volta para dentro deles**. "
    "Nós sabemos se estão bem calibrados; eles não recebem a nota."
)
for coluna, ser in zip(st.columns(len(seres)), seres):
    with coluna:
        brier = ser.inteligencia.calibracao.brier
        if brier is None:
            st.caption(f"{ser.nome}: ainda não apostou em nada")
            continue
        st.metric(f"{ser.nome} · Brier", f"{brier:.4f}", "0 é perfeito · 0,25 é o chute")
        st.caption(
            f"relógio do mundo diz {agora} · a conta dele diz "
            f"{ser.corpo.relogio.conta_propria()} — e ele não é avisado disso"
        )
