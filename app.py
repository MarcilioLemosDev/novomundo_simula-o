#!/usr/bin/env python3
"""A interface: o Senhor vendo o mundo dele correr.

    py -m streamlit run app.py     (Windows)
    streamlit run app.py           (Mac e Linux)

O que se vê aqui não é um log: é o indivíduo (`05`, §1). Cada pensamento mostrado
foi escrito pelo mesmo laço que decidiu — por A3, não há como ele pensar uma coisa
e nos mostrar outra.

A regra desta tela: **o essencial à vista, o técnico escondido.** Quem abre quer ver
o boneco vivendo, não um painel de instrumentos.
"""

from __future__ import annotations

import streamlit as st

from novomundo import Dica, Instante, Microcosmo, Mundo, Sexo, Signo
from novomundo.compromisso import duas_horas_de_estudo
from novomundo.historia import Cronista
from novomundo.serpente import SUSSURROS, Serpente
from novomundo.tempo import TICKS_POR_MES_LUNAR

st.set_page_config(page_title="Novo Mundo", page_icon="🌙", layout="wide")

MAXIMO_POR_RODAGEM = 10_000
MAXIMO_DA_VIDA = 600_000

FASES = ["🌑 lua nova", "🌒 crescente", "🌓 quarto crescente", "🌔 gibosa crescente",
         "🌕 lua cheia", "🌖 gibosa minguante", "🌗 quarto minguante", "🌘 minguante"]


# ─────────────────────────────────────────────────────────────── o mundo

def nascer():
    mundo = Mundo()
    inicio = Instante(0)
    adao = Microcosmo("Adão", Sexo.HOMEM, Signo.LEAO, inicio, posicao=mundo.onde_comeca())
    eva = Microcosmo("Eva", Sexo.MULHER, Signo.PEIXES, inicio, posicao=mundo.onde_comeca())
    mundo.acolher(adao)
    mundo.acolher(eva)
    for ser in (adao, eva):
        ser.assumir(duas_horas_de_estudo(inicio), inicio)
    return mundo, [adao, eva], 0


if "mundo" not in st.session_state:
    st.session_state.mundo, st.session_state.seres, st.session_state.tick = nascer()
    st.session_state.cronista = Cronista()
    st.session_state.serpente = Serpente()

mundo, seres = st.session_state.mundo, st.session_state.seres
agora = Instante(st.session_state.tick)


def correr(quantos: int) -> None:
    quantos = min(quantos, MAXIMO_POR_RODAGEM, MAXIMO_DA_VIDA - st.session_state.tick)
    for _ in range(max(0, quantos)):
        instante = Instante(st.session_state.tick)
        for ser in seres:
            ser.viver_um_tick(mundo, instante)
        st.session_state.cronista.observar(seres, instante)
        st.session_state.tick += 1


# ────────────────────────────────────────────────────── o correr do tempo

st.title("🌙 Novo Mundo")

esquerda, direita = st.columns([3, 2])
esquerda.markdown(f"### {FASES[agora.fase]} · dia {agora.dia + 1} do {agora.mes + 1}º mês")
direita.markdown(f"### {agora.tick / TICKS_POR_MES_LUNAR / 12 / 24:.1f} anos de mundo")

# ────────────────────────────────────────────────────────────── controles

with st.sidebar:
    st.markdown("## ▶ Deixar viver")
    passo = st.select_slider(
        "por quanto tempo",
        options=[1, 24, 168, 720, 2000, 10000],
        value=720,
        format_func=lambda t: {
            1: "1 hora", 24: "1 dia", 168: "1 semana",
            720: "1 mês", 2000: "3 meses", 10000: "1 ano",
        }[t],
    )
    restam = MAXIMO_DA_VIDA - st.session_state.tick
    if restam <= 0:
        st.error("o mundo chegou ao fim do tempo que lhe foi dado.")
    elif st.button("deixar viver", use_container_width=True, type="primary"):
        with st.spinner("vivendo…"):
            correr(passo)
        st.rerun()

    st.progress(min(1.0, st.session_state.tick / MAXIMO_DA_VIDA))
    st.caption(f"{st.session_state.tick:,} de {MAXIMO_DA_VIDA:,} horas".replace(",", "."))

    if st.button("↺ recomeçar do princípio", use_container_width=True):
        for chave in ("mundo", "seres", "tick", "cronista", "serpente"):
            st.session_state.pop(chave, None)
        st.rerun()

    st.divider()
    st.markdown("## 🌱 Falar com eles")
    a_quem = st.selectbox("a quem", [s.nome for s in seres])
    canal = st.radio(
        "de que jeito",
        ["semeadura", "voz", "mundo"],
        format_func=lambda c: {
            "semeadura": "plantar uma vontade",
            "voz": "falar dentro da cabeça",
            "mundo": "deixar algo para achar",
        }[c],
    )
    st.caption(
        {
            "semeadura": "Um desejo. Não afirma nada sobre o mundo, então não pode "
            "ser falso — é assim que se planta vontade sem corromper ninguém.",
            "voz": "Fica registrado que **uma voz disse** isto. Não vira verdade: "
            "ele decide se acredita.",
            "mundo": "Ele precisa encontrar. Pode não achar, e pode entender errado.",
        }[canal]
    )
    dito = st.text_input(
        "o que dizer",
        placeholder={
            "semeadura": "buscar uma companheira que me preencha de amor",
            "voz": "há um livro que te espera",
            "mundo": "uma pedra marcada",
        }[canal],
    )
    if st.button("dizer", use_container_width=True) and dito.strip():
        quem = next(s for s in seres if s.nome == a_quem)
        resposta = quem.ouvir(Dica(canal, dito.strip(), 0.8), agora, mundo)
        st.session_state.ultima_resposta = (a_quem, resposta)
        st.rerun()

    if "ultima_resposta" in st.session_state:
        nome, resposta = st.session_state.ultima_resposta
        if "não sei" in resposta:
            st.warning(f"**{nome}:** {resposta}")
        else:
            st.success(f"**{nome}:** {resposta}")

    st.divider()
    st.markdown("## 🐍 A serpente")
    st.caption("Ela não obriga. Só põe a dúvida — e uma pergunta não se refuta, só se carrega.")
    a_quem_serp = st.selectbox("a quem", [s.nome for s in seres], key="serp")
    qual = st.selectbox("o que perguntar", range(len(SUSSURROS)),
                        format_func=lambda i: SUSSURROS[i].pergunta)
    if st.button("sussurrar", use_container_width=True):
        st.session_state.serpente.sussurrar(
            next(s for s in seres if s.nome == a_quem_serp), agora, qual
        )
        st.rerun()

    st.divider()
    detalhes = st.toggle("mostrar os detalhes", value=False)
    st.caption("crenças, procedência, calibração e o fio inteiro do pensamento")


# ────────────────────────────────────────────────────────── os indivíduos

def sentir_em_palavras(ser) -> str:
    """O estado dele em português, não em números.

    Lê o mesmo vetor de drives que pesou na decisão — por A3 não pode divergir.
    Só troca o jargão por palavra de gente.
    """
    afeto = ser.vontade.afeto
    dominante = ser.vontade.mais_urgente()
    falta = {
        "epistemico": "quer conhecer",
        "coerencia": "quer entender",
        "expressao": "quer deixar sua marca",
        "integridade": "quer se recompor",
        "vinculo": "quer companhia",
    }[dominante.nome]
    humor = (
        "em paz" if afeto > 0.25
        else "bem" if afeto > 0
        else "inquieto" if afeto > -0.25
        else "em falta"
    )
    return humor if dominante.urgencia < 0.15 else f"{humor}, e {falta}"


for coluna, ser in zip(st.columns(2), seres):
    decisao = getattr(ser, "_ultima_decisao", None)
    with coluna:
        with st.container(border=True):
            st.markdown(f"## {'♂' if ser.corpo.sexo is Sexo.HOMEM else '♀'} {ser.nome}")
            st.markdown(f"**está em** {ser.corpo.posicao[1]}, {ser.corpo.posicao[0]}")
            st.markdown(f"**sente-se** {sentir_em_palavras(ser)}")

            if decisao:
                acao = decisao.escolhida.acao
                st.markdown(f"**está a** {acao.verbo.value} — _{acao.porque}_")
                if decisao.escolhida.razoes:
                    st.markdown(f"↳ _{decisao.escolhida.razoes[0].dito}_")
            else:
                st.caption("ainda não viveu nada")

            fe = ser.inteligencia.fe
            if fe:
                st.success(f"✝ confia em {fe.em_quem}, desde o {fe.desde.mes + 1}º mês")

            abertas = ser.inteligencia.em_aberto
            if abertas:
                st.markdown("**carrega estas perguntas:**")
                for duvida in abertas[:3]:
                    st.markdown(f"· _{duvida.pergunta}_")

            relacoes = ser.relacao_com
            if relacoes:
                st.markdown(
                    "**para ele(a):** " + " · ".join(f"{n} é {t}" for n, t in relacoes.items())
                )

            ditos = [d for d in ser.ditos_do_senhor if d[2]]
            if ditos:
                st.markdown("**o que lhe foi dito:**")
                for canal_dito, conteudo, entendeu, quando in ditos[-3:]:
                    icone = {"semeadura": "🌱", "voz": "🗣", "mundo": "🌍"}[canal_dito]
                    st.markdown(f"{icone} _“{conteudo}”_  \n↳ {entendeu}")

            descobriu = ser.experiencia.o_que_me_move(3)
            if descobriu:
                st.markdown(
                    "**descobriu que lhe faz bem:** "
                    + ", ".join(o.split(" em ")[0] for o, _, _ in descobriu)
                )

        if detalhes:
            with st.expander("o fio do pensamento"):
                for linha in (decisao.pensamento if decisao else []):
                    st.markdown(f"· {linha}")
            with st.expander("o que ele crê, e por quê"):
                for crenca in sorted(
                    ser.inteligencia.crencas.values(), key=lambda c: c.confianca, reverse=True
                )[:10]:
                    st.text(crenca.procedencia())
            with st.expander("o que ele sabe de si"):
                st.text(ser.conhecer_se(agora))
                for compromisso in ser.compromissos:
                    st.text(str(compromisso))
            with st.expander("o que só nós vemos"):
                brier = ser.inteligencia.calibracao.brier
                st.metric(
                    "Brier", f"{brier:.4f}" if brier else "—", "0 é perfeito · 0,25 é o chute"
                )
                st.caption(
                    f"o mundo diz {agora}; a conta dele diz "
                    f"{ser.corpo.relogio.conta_propria()} — e ele não é avisado"
                )

# ────────────────────────────────────────────────────────────── a história

st.markdown("## 📖 O que já aconteceu")
marcos = st.session_state.cronista.marcos
if not marcos:
    st.caption("Ainda nada digno de ser contado. Deixe-os viver.")
else:
    for marco in sorted(marcos, key=lambda m: m.quando.tick, reverse=True):
        st.markdown(
            f"**{marco.titulo}** — {marco.de_quem}, no {marco.quando.mes + 1}º mês  \n"
            f"{marco.o_que_houve}"
        )
