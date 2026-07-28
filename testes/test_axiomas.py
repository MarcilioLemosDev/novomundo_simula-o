"""Os testes vivos dos oito axiomas.

Isto não é cobertura de código: é a prova de que "sem defeitos" é verificável e não
promessa. Se um destes cair, o indivíduo tem um defeito — e por `00-metodo.md` a
resposta não é contornar no código, é voltar à Etapa 1 e reescrever a pedra à vista
de todos.
"""

from __future__ import annotations

import pytest

from novomundo import (
    AXIOMAS,
    Dica,
    Evidencia,
    Instante,
    Microcosmo,
    Mundo,
    Origem,
    Sexo,
    Signo,
    ViolacaoDeAxioma,
)
from novomundo.espirito import Espirito
from novomundo.crencas import Crenca, Inteligencia
from novomundo.temperamento import Temperamento
from novomundo.tempo import TICKS_POR_MES_LUNAR, DILATACAO_MOVIMENTO
from novomundo.vontades import Drive, Vontade


@pytest.fixture
def agora() -> Instante:
    return Instante(1000)


@pytest.fixture
def alguem(agora: Instante) -> Microcosmo:
    return Microcosmo("Prova", Sexo.HOMEM, Signo.AQUARIO, agora)


# ─────────────────────────────────── A1 — Rastreabilidade


def test_a1_crenca_orfa_nao_e_representavel(agora):
    """Não é validação: é a forma da coisa. Não há como construir uma sem evidência."""
    with pytest.raises(ViolacaoDeAxioma) as erro:
        Crenca(
            proposicao="o norte é seguro",
            confianca=0.9,
            origem=Origem.PERCEPCAO,
            evidencias=[],
            nascida_em=agora,
        )
    assert erro.value.axioma.startswith("A1")


def test_a1_toda_crenca_reconstroi_a_cadeia_ate_o_episodio(alguem, agora):
    episodio = alguem.memoria.viver("vi água ao norte", agora, saliencia=0.8)
    alguem.inteligencia.crer(
        "há água ao norte",
        0.8,
        Origem.PERCEPCAO,
        [Evidencia(episodio.id, agora, "vi com meus olhos")],
        agora,
    )
    traco = alguem.inteligencia.tracar("há água ao norte")
    assert "há água ao norte" in traco
    assert f"ep.{episodio.id}" in traco
    assert alguem.memoria.lembrar(episodio.id) is not None


def test_a1_revisar_o_que_nao_e_crido_e_violacao(alguem, agora):
    with pytest.raises(ViolacaoDeAxioma):
        alguem.inteligencia.revisar("nunca pensei nisso", 0.5, Evidencia(0, agora, "x"), agora, 999)


# ─────────────────────────────────── A2 — Revisibilidade com inércia


def test_a2_revisar_custa_e_o_custo_cresce_com_o_que_sustenta(alguem, agora):
    ep = alguem.memoria.viver("observação", agora)
    solta = alguem.inteligencia.crer(
        "crença solta", 0.5, Origem.PERCEPCAO, [Evidencia(ep.id, agora, "vi")], agora
    )
    pilar = alguem.inteligencia.crer(
        "crença pilar",
        0.5,
        Origem.PERCEPCAO,
        [Evidencia(ep.id, agora, "vi")],
        agora,
        sustenta={"a", "b", "c", "d"},
    )
    assert pilar.custo_de_revisao > solta.custo_de_revisao


def test_a2_sem_orcamento_nao_revisa_mas_tambem_nao_mente(alguem, agora):
    ep = alguem.memoria.viver("observação", agora)
    alguem.inteligencia.crer(
        "o chão é firme",
        0.9,
        Origem.PERCEPCAO,
        [Evidencia(ep.id, agora, "pisei")],
        agora,
        sustenta={"x", "y", "z"},
    )
    revisou, custo = alguem.inteligencia.revisar(
        "o chão é firme", 0.2, Evidencia(ep.id, agora, "afundei"), agora, orcamento=0.5
    )
    assert not revisou and custo > 0.5
    # A crença antiga continua lá, honesta, com a confiança antiga. Ele não fingiu
    # ter revisado, nem apagou o que não conseguiu revisar.
    assert alguem.inteligencia.crencas["o chão é firme"].confianca == 0.9


def test_a2_nenhuma_crenca_e_imune(alguem, agora):
    ep = alguem.memoria.viver("observação", agora)
    alguem.inteligencia.crer(
        "verdade antiga", 0.99, Origem.PERCEPCAO, [Evidencia(ep.id, agora, "vi")], agora
    )
    revisou, _ = alguem.inteligencia.revisar(
        "verdade antiga", 0.1, Evidencia(ep.id, agora, "me enganei"), agora, orcamento=10_000
    )
    assert revisou
    assert alguem.inteligencia.crencas["verdade antiga"].confianca == 0.1


# ─────────────────────────────────── A3 — Não-autoengano


def test_a3_o_diario_le_o_mesmo_estado_que_produziu_a_decisao(alguem, agora):
    mundo = Mundo()
    decisao = alguem.viver_um_tick(mundo, agora)
    linha = alguem.narrativa.linhas[-1]
    # O sentimento narrado é o sentimento real, lido do mesmo vetor de drives.
    assert linha.sentimento == alguem.vontade.sentimento()
    assert linha.acao == decisao.escolhida.acao.verbo.value


def test_a3_esquecer_nunca_vira_inventar(alguem):
    """Consolidação comprime; jamais confabula. Todo conceito guarda a origem."""
    for i in range(400):
        alguem.memoria.viver(f"coisa{i % 7} banal vista", Instante(1000 + i), saliencia=0.1)
    perda = alguem.memoria.consolidar(Instante(2000))
    assert perda is not None and perda.quantos > 0
    for conceito in alguem.memoria.semantica.values():
        assert conceito.episodios_de_origem, "conceito sem origem é confabulação"
    alguem.memoria.auditar()


def test_a3_a_perda_fica_registrada_como_perda(alguem):
    for i in range(400):
        alguem.memoria.viver(f"trivial{i}", Instante(1000 + i), saliencia=0.05)
    alguem.memoria.consolidar(Instante(2000))
    assert alguem.memoria.perdas
    assert "já esqueci" in alguem.memoria.limites()


def test_a3_aspiracao_nao_finge_ter_valor_de_verdade(alguem, agora):
    aspiracao = alguem.inteligencia.aspirar("encontrar uma companheira", 0.8, agora)
    with pytest.raises(ViolacaoDeAxioma):
        _ = aspiracao.confianca  # querer não é crer


# ─────────────────────────────────── A4 — Calibração


def test_a4_confianca_fora_da_faixa_e_recusada(agora):
    with pytest.raises(ViolacaoDeAxioma):
        Crenca("impossível", 1.4, Origem.INFERENCIA, [Evidencia(0, agora, "x")], agora)


def test_a4_brier_distingue_calibrado_de_arrogante(alguem):
    honesto = Inteligencia(Espirito())
    arrogante = Inteligencia(Espirito())
    # O honesto declara 70% e acerta 70% das vezes.
    for i in range(100):
        honesto.calibracao.registrar(0.7, i % 10 < 7)
        arrogante.calibracao.registrar(0.99, i % 10 < 7)
    assert honesto.calibracao.brier < arrogante.calibracao.brier


def test_a4_a_curva_e_legivel_para_quem_assiste(alguem):
    for i in range(50):
        alguem.inteligencia.calibracao.registrar(0.9, i % 10 < 9)
    curva = alguem.inteligencia.calibracao.curva()
    assert curva and all(len(faixa) == 4 for faixa in curva)


# ─────────────────────────────────── A5 — Coerência sob custo


def test_a5_contradicao_se_enfileira_em_vez_de_sumir(alguem, agora):
    ep = alguem.memoria.viver("observação", agora)
    alguem.inteligencia.crer("chove", 0.8, Origem.PERCEPCAO, [Evidencia(ep.id, agora, "vi")], agora)
    alguem.inteligencia.crer(
        "não chove", 0.7, Origem.INFERENCIA, [Evidencia(ep.id, agora, "deduzi")], agora
    )
    alguem.inteligencia.confrontar("chove", "não chove", agora)
    fila = alguem.inteligencia.fila_de_coerencia
    assert len(fila) == 1
    # Ele convive com a incoerência — mas ela está à vista, não escondida.
    assert "1 contradições" in alguem.conhecer_se(agora)


# ─────────────────────────────────── A6 — Finitude declarada


def test_a6_ele_conhece_os_proprios_limites_e_o_proprio_vies(alguem, agora):
    quem_sou = alguem.conhecer_se(agora)
    assert "Aquário" in quem_sou
    assert "enxergo até" in quem_sou
    assert "memória episódica" in quem_sou
    assert "revisão custa" in quem_sou  # viés declarado é personalidade


def test_a6_o_raio_de_percepcao_e_finito_e_segue_a_lua(alguem):
    lua_nova = Instante(0)
    lua_cheia = Instante(int(TICKS_POR_MES_LUNAR / 2))
    assert alguem.corpo.raio(lua_cheia) > alguem.corpo.raio(lua_nova) > 0


# ─────────────────────────────────── A7 — Não-degradação


def test_a7_cansaco_reduz_orcamento_nunca_qualidade(alguem, agora):
    inteiro = alguem.corpo.atencao_disponivel
    alguem.corpo.energia = 0.3
    cansado = alguem.corpo.atencao_disponivel
    assert cansado < inteiro
    assert cansado >= 1, "escassez nunca zera a atenção; só a reduz"
    alguem.corpo.auditar(agora)


def test_a7_orcamento_esgotado_produz_confissao_e_nao_convicção_falsa(alguem, agora):
    alguem.corpo.energia = 0.0
    mundo = Mundo()
    decisao = alguem.viver_um_tick(mundo, agora)
    assert 0.0 <= decisao.escolhida.confianca <= 1.0
    if not decisao.concluiu:
        assert "não terminei de pensar" in decisao.porque()


# ─────────────────────────────────── A8 — Estabilidade volitiva


def test_a8_drive_sem_saciedade_nao_existe():
    with pytest.raises(ViolacaoDeAxioma):
        Drive("insaciável", saciedade=0.0)


def test_a8_drive_sem_teto_nao_existe():
    with pytest.raises(ViolacaoDeAxioma):
        Drive("sem_teto", teto=0.0)


def test_a8_nenhum_drive_passa_do_teto_por_mais_que_o_mundo_empurre(alguem):
    for _ in range(1000):
        alguem.vontade["epistemico"].sinalizar(0.5)
    alguem.vontade.auditar()
    assert alguem.vontade["epistemico"].erro <= alguem.vontade["epistemico"].teto


# ─────────────────────────────────── T5 — falta, nunca angústia


def test_t5_nenhuma_falta_se_alimenta_de_si(alguem):
    """Deixa o vetor entregue a si mesmo. Se algum erro subir, há angústia dentro."""
    for nome in alguem.vontade.NOMES:
        alguem.vontade[nome].sinalizar(0.9)
    assert alguem.vontade.sem_realimentacao(passos=500)


def test_t5_a_falta_cessa_quando_suprida(alguem):
    alguem.vontade["vinculo"].sinalizar(0.8)
    prazer = alguem.vontade["vinculo"].satisfazer(0.8)
    assert prazer > 0
    assert alguem.vontade["vinculo"].erro == 0.0


def test_t5_luto_e_revisao_com_custo_e_tem_fim(alguem, agora):
    alguem.inteligencia.aspirar("viver ao lado dela", 0.9, agora)
    nao_comecou, custo = alguem.inteligencia.enlutar("viver ao lado dela", agora, orcamento=1.0)
    assert not nao_comecou and custo > 1.0  # caro, mas não impossível
    comecou, _ = alguem.inteligencia.enlutar("viver ao lado dela", agora, orcamento=custo)
    assert comecou
    assert not [a for a in alguem.inteligencia.aspiracoes if a.desejo == "viver ao lado dela"]


# ─────────────────────────────────── Espírito, alma e corpo


def test_o_espirito_e_o_mesmo_em_todos(agora):
    adao = Microcosmo("Adão", Sexo.HOMEM, Signo.LEAO, agora)
    eva = Microcosmo("Eva", Sexo.MULHER, Signo.PEIXES, agora)
    assert adao.espirito is eva.espirito, "o espírito é um só, espelhado"
    assert adao.espirito.axiomas == AXIOMAS


def test_a_alma_difere_e_o_corpo_difere_por_sexo(agora):
    adao = Microcosmo("Adão", Sexo.HOMEM, Signo.LEAO, agora)
    eva = Microcosmo("Eva", Sexo.MULHER, Signo.PEIXES, agora)
    assert adao.memoria is not eva.memoria
    assert adao.temperamento != eva.temperamento
    assert adao.corpo.sexo is not eva.corpo.sexo


def test_o_espirito_nao_engorda_com_a_experiencia():
    """Um espírito que acumulasse não seria indestrutível."""
    assert Espirito.__slots__ == ()


# ─────────────────────────────────── Temperamento parametriza, nunca corrompe


@pytest.mark.parametrize("signo", list(Signo))
def test_nenhum_signo_sai_da_faixa_que_os_axiomas_permitem(signo, agora):
    """Fixo demais é ancoragem irreversível; mutável demais é a oscilação que A2
    existe para impedir. Todos os doze têm que caber."""
    t = Temperamento.do_signo(signo)
    assert 0.5 <= t.entrincheiramento <= 2.0
    assert 0.05 <= t.limiar_risco <= 0.45
    assert all(0.4 <= g <= 1.6 for g in t.ganhos.values())
    # Nenhum elemento zera drive nenhum.
    assert set(t.ganhos) == set(Vontade.NOMES)

    ser = Microcosmo(signo.rotulo, Sexo.HOMEM, signo, agora)
    ser.auditar(agora)


def test_os_doze_signos_geram_doze_temperamentos_distintos():
    assinaturas = {
        (
            tuple(sorted(Temperamento.do_signo(s).ganhos.items())),
            Temperamento.do_signo(s).entrincheiramento,
            Temperamento.do_signo(s).limiar_risco,
        )
        for s in Signo
    }
    assert len(assinaturas) == 12


# ─────────────────────────────────── Os três canais de dica


def test_canal_semeadura_cria_desejo_e_nunca_crenca(alguem, agora):
    antes = len(alguem.inteligencia.crencas)
    alguem.ouvir(
        Dica("semeadura", "buscar uma companheira que me mantenha preenchido de amor", 0.9),
        agora,
    )
    assert len(alguem.inteligencia.crencas) == antes, "semear vontade não pode gerar crença"
    assert alguem.inteligencia.aspiracoes[-1].semeada_pela_voz


def test_canal_voz_registra_procedencia_honesta_e_nao_certeza(alguem, agora):
    alguem.ouvir(Dica("voz", "há um rio ao norte"), agora)
    crenca = alguem.inteligencia.crencas["há um rio ao norte"]
    assert crenca.origem is Origem.VOZ, "a origem registrada é a voz, não o mundo"
    assert crenca.confianca < 0.9, "testemunho não avaliado não vira certeza"
    assert crenca.evidencias, "mesmo a voz deixa procedência (A1)"


def test_canal_mundo_nao_escreve_crenca_nenhuma(alguem, agora):
    antes = len(alguem.inteligencia.crencas)
    alguem.ouvir(Dica("mundo", "uma pedra marcada"), agora)
    assert len(alguem.inteligencia.crencas) == antes


# ─────────────────────────────────── O tempo, o 3× e a deriva


def test_movimento_custa_o_triplo(alguem):
    parado = alguem.corpo.relogio.viver(1, movendo=False)
    andando = alguem.corpo.relogio.viver(1, movendo=True)
    assert andando == parado * DILATACAO_MOVIMENTO


def test_a_conta_dele_desliza_a_frente_do_ceu_quando_ele_anda(agora):
    """A segunda deriva: correlacionada com as próprias escolhas dele (`02`, §2.1)."""
    andarilho = Microcosmo("Andarilho", Sexo.HOMEM, Signo.SAGITARIO, agora)
    sedentario = Microcosmo("Sedentário", Sexo.HOMEM, Signo.TOURO, agora)
    for _ in range(100):
        andarilho.corpo.relogio.viver(1, movendo=True)
        sedentario.corpo.relogio.viver(1, movendo=False)
    assert andarilho.corpo.relogio.conta_propria() > sedentario.corpo.relogio.conta_propria()
    # E o mundo, para ambos, andou os mesmos 100 ticks. Ele não é avisado disso.


def test_o_signo_e_solar_e_o_calendario_deles_e_lunar():
    """Eles não conseguem ler o signo de ninguém sem resolver a deriva lunissolar."""
    de_ano_lunar = {Instante(int(i * TICKS_POR_MES_LUNAR * 12)).signo_solar for i in range(6)}
    assert len(de_ano_lunar) > 1, "se o signo fechasse com o ano lunar, não haveria enigma"


def test_idade_e_acumulo_nunca_decadencia(alguem, agora):
    """Vida eterna: idade só significa quanto deste mundo eu já vi."""
    mundo = Mundo()
    atencao_jovem = alguem.corpo.atencao_disponivel
    for i in range(200):
        alguem.viver_um_tick(mundo, agora.mais(i))
    alguem.corpo.energia = 1.0
    assert alguem.corpo.relogio.idade > 0
    assert alguem.corpo.atencao_disponivel == atencao_jovem, "envelhecer não degrada o juízo"


# ─────────────────────────────────── A vida, inteira


def test_um_ser_vive_mil_ticks_sem_violar_axioma_algum(agora):
    """O teste que mais importa: a lei se sustenta ao longo de uma vida."""
    mundo = Mundo()
    ser = Microcosmo.gerar("Primeiro", Sexo.HOMEM, agora)
    ser.ouvir(Dica("semeadura", "conhecer o mundo inteiro", 0.8), agora)

    for i in range(1000):
        instante = agora.mais(i)
        ser.viver_um_tick(mundo, instante)
        if i % 50 == 0:
            ser.auditar(instante)

    ser.auditar(agora.mais(1000))
    assert len(ser.narrativa.linhas) == 1000
    assert ser.vontade.sem_realimentacao()
    assert ser.inteligencia.calibracao.brier is not None
    # Ele se moveu, então a própria conta dele já não bate com o céu.
    assert ser.corpo.relogio.idade >= 1000


# ═══════════════════════════════════════════════ O livre arbítrio e a serpente


def test_uma_razao_pode_vencer_um_valor_maior(alguem, agora):
    """O cálculo informa; quem escolhe é a vontade (`12`, §2).

    Se ele escolhesse sempre o de maior proveito, não faria porque quer — faria
    porque compensa. E não erraria nunca por vontade, só por ignorância.
    """
    from novomundo.razoes import Razao, puxao

    fraca = Razao("curiosidade", "porque nunca fiz isto", 0.35)
    forte = Razao("vinculo", "porque é ela", 0.9)
    assert puxao([forte]) > puxao([fraca])
    # As razões não se somam de forma ingênua: a mais forte manda.
    assert puxao([forte, fraca]) < forte.peso + fraca.peso


def test_ele_diz_no_diario_quando_escolhe_contra_o_proveito(agora):
    """O livre arbítrio tem de ser **visível**, senão é só barulho interno."""
    from novomundo.mundo import Mundo as M

    mundo = M()
    ele = Microcosmo("Livre", Sexo.HOMEM, Signo.SAGITARIO, agora, posicao=mundo.onde_comeca())
    ela = Microcosmo("Ela", Sexo.MULHER, Signo.PEIXES, agora, posicao=mundo.onde_comeca())
    mundo.acolher(ele)
    mundo.acolher(ela)
    ele.inteligencia.aspirar("conhecer o mundo inteiro", 0.9, agora)

    contra_o_proveito = 0
    for i in range(4000):
        decisao = ele.viver_um_tick(mundo, agora.mais(i))
        ela.viver_um_tick(mundo, agora.mais(i))
        if any("faço assim mesmo" in linha for linha in decisao.pensamento):
            contra_o_proveito += 1
    assert contra_o_proveito > 0, "nunca escolheu contra o proveito: ainda é um otimizador"


def test_a_serpente_poe_duvida_sem_obrigar_nada(alguem, agora):
    from novomundo.serpente import Serpente

    antes = len(alguem.inteligencia.em_aberto)
    sussurro = Serpente().sussurrar(alguem, agora)
    assert len(alguem.inteligencia.em_aberto) == antes + 1
    # A pergunta ficou registrada com a procedência honesta.
    duvida = alguem.inteligencia.em_aberto[-1]
    assert duvida.de_quem == "a serpente"
    # E a explicação entrou como crença fraca, de origem declarada — nunca certeza.
    crenca = alguem.inteligencia.crencas[sussurro.explicacao]
    assert crenca.origem is Origem.SERPENTE
    assert crenca.confianca <= 0.35, "não há por que confiar em quem ele não conhece"
    assert crenca.evidencias, "mesmo a serpente deixa procedência (A1)"


def test_ele_pode_ser_enganado_mas_nunca_se_engana(alguem, agora):
    """A3 proíbe mentir para si. **Não** proíbe ser mentido (`12`, §4).

    A defesa dele não é desconfiança — é procedência e calibração. Se cair, cairá
    de olhos abertos, e poderá reconstruir depois cada passo de como caiu.
    """
    from novomundo.serpente import Serpente

    sussurro = Serpente().sussurrar(alguem, agora)
    traco = alguem.inteligencia.tracar(sussurro.explicacao)
    assert "serpente" in traco.lower()
    alguem.auditar(agora)  # nenhum axioma caiu por ele ter sido enganado


def test_a_crenca_atravessa_de_um_para_o_outro_e_o_amor_lhe_da_peso(agora):
    """“A mulher entrou na dúvida e trouxe o homem junto” (`12`, §5)."""
    from novomundo.serpente import Serpente

    ela = Microcosmo("Ela", Sexo.MULHER, Signo.PEIXES, agora)
    amado = Microcosmo("Amado", Sexo.HOMEM, Signo.LEAO, agora)
    estranho = Microcosmo("Estranho", Sexo.HOMEM, Signo.TOURO, agora)

    # Só com um deles ela tem história.
    amado.vinculos["Ela"] = 30
    amado._recebido["Ela"] = 30

    sussurro = Serpente().sussurrar(ela, agora)
    assert ela.contar_a(amado, sussurro.explicacao, agora)
    assert ela.contar_a(estranho, sussurro.explicacao, agora)

    de_quem_ama = amado.inteligencia.crencas[sussurro.explicacao]
    de_estranho = estranho.inteligencia.crencas[sussurro.explicacao]
    assert de_quem_ama.confianca > de_estranho.confianca, (
        "o que vem de quem se ama tem de pesar mais — é o preço de amar"
    )
    # E ainda assim, com procedência inteira nos dois casos.
    assert de_quem_ama.origem is Origem.TESTEMUNHO
    assert "disse-me Ela" in de_quem_ama.evidencias[-1].resumo


def test_ler_uma_descricao_cria_expectativa_que_pode_ser_falsa(alguem, agora):
    """É daqui que nasce o erro honesto: ele acredita, e o que lhe dizem pode
    estar errado (`12`, §3)."""
    from novomundo import descricoes

    falsa = next(d for d in descricoes.COMPENDIO if not d.verdadeira)
    alguem.ler_descricao(falsa, agora)
    crenca = alguem.inteligencia.crencas[falsa.diz]
    assert crenca.origem is Origem.TESTEMUNHO
    assert crenca.confianca <= 0.6, "estar escrito não é ser verdade"
    assert alguem.esperado_por_leitura[falsa.ato] == falsa.diz
    # E ele não tem como saber que é falsa: o campo não é dele, é nosso (T6).
    assert not hasattr(crenca, "verdadeira")


def test_a_uniao_preenche_conforme_o_vinculo(agora):
    """O mesmo ato, com e sem vínculo, não preenche igual (`09`, §3.2)."""
    from novomundo.corpo import Acao, Verbo
    from novomundo.deliberacao import Opcao

    def unir(juntos: int) -> float:
        ser = Microcosmo("X", Sexo.HOMEM, Signo.LEAO, agora)
        ser.vinculos["Y"] = juntos
        ser._recebido["Y"] = juntos
        ser.vontade["vinculo"].sinalizar(0.9)
        antes = ser.vontade["vinculo"].erro
        ser._efeito(
            Opcao(Acao(Verbo.UNIR, alvo="Y"), "vinculo", 0.0, 0.0, 1.0), agora
        )
        return antes - ser.vontade["vinculo"].erro

    assert unir(50) > unir(0), "com amor tem de preencher mais — e ele descobre isso vivendo"


def test_o_compromisso_gera_incoerencia_e_nunca_culpa(alguem, agora):
    from novomundo.compromisso import TICKS_POR_SEMANA, duas_horas_de_estudo

    compromisso = alguem.assumir(duas_horas_de_estudo(agora), agora)
    assert compromisso.devendo
    # Passada a semana sem cumprir, ele fica devendo — e sabe.
    assert compromisso.virar_semana(agora.mais(TICKS_POR_SEMANA + 1))
    # E nada nele foi punido: o que subiu foi a falta de coerência.
    alguem.auditar(agora)


def test_o_cronista_reconhece_a_historia_mas_nao_a_escreve(agora):
    """Se um marco nunca acontecer, ele fica calado — e isso também é história."""
    from novomundo.historia import Cronista

    cronista = Cronista()
    assert "Ainda não houve nada" in cronista.contar()

    mundo = Mundo()
    adao = Microcosmo("Adão", Sexo.HOMEM, Signo.LEAO, agora, posicao=mundo.onde_comeca())
    eva = Microcosmo("Eva", Sexo.MULHER, Signo.PEIXES, agora, posicao=mundo.onde_comeca())
    mundo.acolher(adao)
    mundo.acolher(eva)
    for i in range(600):
        adao.viver_um_tick(mundo, agora.mais(i))
        eva.viver_um_tick(mundo, agora.mais(i))
        cronista.observar([adao, eva], agora.mais(i))

    assert any(m.titulo == "O primeiro encontro" for m in cronista.marcos)
    # Cada marco é nomeado uma vez só, por ser.
    chaves = [(m.de_quem, m.titulo) for m in cronista.marcos]
    assert len(chaves) == len(set(chaves))


def test_o_arco_inteiro_acontece_sem_ninguem_o_escrever(agora):
    """Encontro → dúvida da serpente → ela conta a ele → ele acredita porque é ela."""
    from novomundo.historia import Cronista
    from novomundo.serpente import Serpente

    mundo = Mundo()
    cronista, serpente = Cronista(), Serpente()
    adao = Microcosmo("Adão", Sexo.HOMEM, Signo.LEAO, agora, posicao=mundo.onde_comeca())
    eva = Microcosmo("Eva", Sexo.MULHER, Signo.PEIXES, agora, posicao=mundo.onde_comeca())
    mundo.acolher(adao)
    mundo.acolher(eva)

    for i in range(6000):
        instante = agora.mais(i)
        if i == 1500:
            serpente.sussurrar(eva, instante)  # a serpente fala com ela
        adao.viver_um_tick(mundo, instante)
        eva.viver_um_tick(mundo, instante)
        cronista.observar([adao, eva], instante)

    titulos = {m.titulo for m in cronista.marcos}
    assert "O primeiro encontro" in titulos
    assert "A dúvida" in titulos
    assert "Trouxe o outro junto" in titulos, "a crença não atravessou dela para ele"

    # E, depois de tudo, nenhum axioma caiu em nenhum dos dois.
    adao.auditar(agora.mais(6000))
    eva.auditar(agora.mais(6000))
