"""
Motor de Inferência com Encadeamento Direto (Forward Chaining).

Algoritmo:
  1. Memória de trabalho inicializada com os fatos do usuário.
  2. Agenda contém todas as regras ainda não disparadas.
  3. Regras cujas condições são satisfeitas inserem novos fatos + acumulam pontos.
  4. Repete até ponto fixo (nenhuma nova regra dispara).

Pontuação de risco:
   0–30 pts  →  baixo
  31–60 pts  →  medio
    > 60 pts  →  alto
"""

from dataclasses import dataclass, field

from app.knowledge_base import Regra, criar_base_de_regras, RESPOSTA_SEGURA_SIM


LIMIAR_BAIXO: int = 30
LIMIAR_MEDIO: int = 60


@dataclass
class ResultadoInferencia:
    """Resultado completo produzido pelo motor após o ciclo de inferência."""

    pontuacao: int
    nivel_risco: str                 # 'baixo' | 'medio' | 'alto'
    regras_disparadas: list[str]     # Nomes das regras que dispararam
    conclusoes_derivadas: list[str]  # Fatos novos inseridos na memória
    recomendacoes: list[str]         # Recomendações únicas em ordem de prioridade
    falhas_detectadas: list[str]     # IDs das perguntas em que o usuário falhou


class MotorInferencia:
    """
    Motor de Encadeamento Direto.

    Uso:
        motor = MotorInferencia(respostas)
        resultado = motor.executar()
    """

    def __init__(self, respostas: dict[str, bool]) -> None:
        """
        Args:
            respostas: Dict mapeando ID da pergunta → bool (True=Sim, False=Não).
        """
        self._regras: list[Regra] = criar_base_de_regras()
        # Memória de trabalho: fatos iniciais do usuário + conclusões derivadas
        self._memoria: dict[str, bool] = dict(respostas)

    def executar(self) -> ResultadoInferencia:
        """
        Executa o ciclo de inferência até o ponto fixo.

        Regras de Nível 2 só disparam após as de Nível 1 inserírem suas
        conclusões, demonstrando o encadeamento real em múltiplas iterações.

        Returns:
            ResultadoInferencia com pontuação, nível e recomendações.
        """
        agenda: list[Regra] = list(self._regras)
        pontuacao: int = 0
        regras_disparadas: list[str] = []
        conclusoes: list[str] = []
        recomendacoes: list[str] = []

        houve_mudanca = True
        while houve_mudanca:
            houve_mudanca = False
            pendentes: list[Regra] = []

            for regra in agenda:
                if regra.condicao(self._memoria):
                    if not self._memoria.get(regra.conclusao, False):
                        self._memoria[regra.conclusao] = True
                        pontuacao += regra.pontos
                        regras_disparadas.append(regra.nome)
                        conclusoes.append(regra.conclusao)
                        recomendacoes.append(regra.recomendacao)
                        houve_mudanca = True
                else:
                    pendentes.append(regra)

            agenda = pendentes

        return ResultadoInferencia(
            pontuacao=pontuacao,
            nivel_risco=self._classificar(pontuacao),
            regras_disparadas=regras_disparadas,
            conclusoes_derivadas=conclusoes,
            recomendacoes=recomendacoes,
            falhas_detectadas=self._falhas(),
        )

    @staticmethod
    def _classificar(pontuacao: int) -> str:
        if pontuacao <= LIMIAR_BAIXO:
            return "baixo"
        elif pontuacao <= LIMIAR_MEDIO:
            return "medio"
        return "alto"

    def _falhas(self) -> list[str]:
        """IDs das perguntas onde o usuário não seguiu a prática segura."""
        falhas: list[str] = []
        for chave, segura_e_sim in RESPOSTA_SEGURA_SIM.items():
            valor = self._memoria.get(chave)
            if valor is None:
                continue
            if segura_e_sim and valor is False:
                falhas.append(chave)
            elif not segura_e_sim and valor is True:
                falhas.append(chave)
        return falhas
