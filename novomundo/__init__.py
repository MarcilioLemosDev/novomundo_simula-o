"""novomundo — a simulação.

Um indivíduo tecido em corpo, alma e espírito, num mapa 2D regido por calendário
lunar. Ver `docs/` para a pedra que rege tudo isto.
"""

from .corpo import Acao, Corpo, Verbo
from .crencas import Aspiracao, Crenca, Evidencia, Inteligencia, Origem
from .espirito import AXIOMAS, Espirito, ViolacaoDeAxioma
from .memoria import Memoria
from .microcosmo import ESPIRITO, Dica, Microcosmo
from .mundo import Mundo
from .temperamento import Elemento, Modalidade, Sexo, Signo, Temperamento
from .tempo import Instante, Relogio, RelogioProprio
from .vontades import Drive, Vontade

__all__ = [
    "Acao", "Aspiracao", "AXIOMAS", "Corpo", "Crenca", "Dica", "Drive", "Elemento",
    "ESPIRITO", "Espirito", "Evidencia", "Instante", "Inteligencia", "Memoria",
    "Microcosmo", "Modalidade", "Mundo", "Origem", "Relogio", "RelogioProprio",
    "Sexo", "Signo", "Temperamento", "Verbo", "ViolacaoDeAxioma", "Vontade",
]
