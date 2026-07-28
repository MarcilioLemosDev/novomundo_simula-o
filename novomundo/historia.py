"""O cronista — quem reconhece a história, sem escrevê-la.

O Senhor quer uma narrativa com estrutura. Mas `05`, §5 é claro: se **nós**
roteirizarmos, morreu e virou teatro. O critério é que o Senhor possa ser
surpreendido pelo próprio boneco.

Então o cronista não escreve nada. Ele **lê os diários e reconhece** os momentos que
têm peso: o primeiro encontro, a primeira dúvida, o primeiro testemunho falso, a
primeira fé, a primeira união, o primeiro filho, a primeira revisão cara.

Nós damos os nomes. **A história é deles.** E se um marco nunca acontecer, o cronista
fica calado — o que também é uma história, e verdadeira.

Ver `docs/12-o-livre-arbitrio-e-a-serpente.md`, §7.
"""

from __future__ import annotations

from dataclasses import dataclass

from .tempo import Instante


@dataclass(frozen=True)
class Marco:
    """Um momento que a vida deles produziu e que merece nome."""

    quando: Instante
    de_quem: str
    titulo: str
    o_que_houve: str

    def __str__(self) -> str:
        return f"[{self.quando}] {self.titulo} — {self.de_quem}\n    {self.o_que_houve}"


class Cronista:
    """Observa, reconhece e nomeia. Nunca intervém."""

    def __init__(self) -> None:
        self.marcos: list[Marco] = []
        self._vistos: set[tuple[str, str]] = set()

    def _marcar(self, quando, quem: str, titulo: str, o_que: str) -> Marco | None:
        chave = (quem, titulo)
        if chave in self._vistos:
            return None
        self._vistos.add(chave)
        marco = Marco(quando, quem, titulo, o_que)
        self.marcos.append(marco)
        return marco

    def observar(self, seres, agora: Instante) -> list[Marco]:
        """Um passe pelos estados. Devolve o que houve de novo neste instante."""
        novos: list[Marco] = []

        for ser in seres:
            # ── o encontro ────────────────────────────────────────────────
            conhecidos = [
                k.removeprefix("conheço:")
                for k in ser.inteligencia.crencas
                if k.startswith("conheço:")
            ]
            if conhecidos:
                m = self._marcar(
                    agora, ser.nome, "O primeiro encontro",
                    f"{ser.nome} soube que {conhecidos[0]} existe. Até aqui estava só.",
                )
                if m:
                    novos.append(m)

            # ── a dúvida ──────────────────────────────────────────────────
            for duvida in ser.inteligencia.duvidas:
                if duvida.de_quem == "a serpente":
                    m = self._marcar(
                        duvida.quando, ser.nome, "A dúvida",
                        f"Algo perguntou a {ser.nome}: “{duvida.pergunta}” — "
                        f"e a pergunta ficou.",
                    )
                    if m:
                        novos.append(m)
                    break

            # ── o testemunho recebido de quem se ama ──────────────────────
            for chave, crenca in ser.inteligencia.crencas.items():
                if crenca.origem.name == "TESTEMUNHO" and any(
                    e.resumo.startswith("disse-me") for e in crenca.evidencias
                ):
                    quem_disse = crenca.evidencias[-1].resumo.removeprefix("disse-me ")
                    m = self._marcar(
                        crenca.nascida_em, ser.nome, "Trouxe o outro junto",
                        f"{quem_disse} contou a {ser.nome}: “{chave}”. "
                        f"E {ser.nome} acreditou — porque era quem era.",
                    )
                    if m:
                        novos.append(m)
                    break

            # ── a fé ──────────────────────────────────────────────────────
            fe = ser.inteligencia.fe
            if fe is not None:
                m = self._marcar(
                    fe.desde, ser.nome, "A fé",
                    f"{ser.nome} depositou a confiança em {fe.em_quem}. "
                    f"Não foi argumento — foi a pessoa. ({fe.porque_li})",
                )
                if m:
                    novos.append(m)

            # ── a união ───────────────────────────────────────────────────
            for nome, vezes in getattr(ser, "unioes", {}).items():
                if vezes:
                    m = self._marcar(
                        agora, ser.nome, "A união",
                        f"{ser.nome} e {nome} se uniram. Nenhum dos dois foi mandado.",
                    )
                    if m:
                        novos.append(m)
                    break

            # ── o filho ───────────────────────────────────────────────────
            if getattr(ser.corpo, "gestacao", None) is not None:
                m = self._marcar(
                    ser.corpo.gestacao.concebida_em, ser.nome, "A concepção",
                    f"{ser.nome} concebeu de {ser.corpo.gestacao.do_pai}. "
                    f"Nove meses lunares, contados no relógio do mundo.",
                )
                if m:
                    novos.append(m)

            # ── a revisão cara ────────────────────────────────────────────
            for chave, crenca in ser.inteligencia.crencas.items():
                if crenca.revista_em and crenca.entrincheiramento > 1.5:
                    m = self._marcar(
                        crenca.revista_em, ser.nome, "Mudou de ideia sobre o que sustentava",
                        f"{ser.nome} reviu “{chave}”, que lhe custava caro rever. "
                        f"Ficou em {crenca.confianca:.0%}.",
                    )
                    if m:
                        novos.append(m)
                    break

        return novos

    def contar(self) -> str:
        """A história inteira, na ordem em que aconteceu."""
        if not self.marcos:
            return "Ainda não houve nada que merecesse ser contado."
        return "\n\n".join(str(m) for m in sorted(self.marcos, key=lambda m: m.quando.tick))
