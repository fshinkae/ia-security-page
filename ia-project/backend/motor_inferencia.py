"""
Motor de Inferência com Encadeamento Direto (Forward Chaining)
AEMS / Projeto de Extensão — Sistema Especialista de Segurança Digital

Algoritmo de Forward Chaining implementado:
  1. A memória de trabalho é inicializada com os fatos do usuário
     (respostas booleanas às 10 perguntas).
  2. Todas as regras são avaliadas contra os fatos presentes.
  3. Regras cujas condições são satisfeitas e cujas conclusões ainda não
     estão na memória são disparadas: o novo fato é inserido e os pontos
     são acumulados.
  4. O ciclo se repete até que nenhuma nova regra dispare (ponto fixo).
  5. A pontuação acumulada determina o nível de risco final.

Pontuação de risco:
  0  – 30 pts → BAIXO RISCO
  31 – 60 pts → MÉDIO RISCO
  > 60 pts    → ALTO RISCO
"""

import csv
from dataclasses import dataclass, field
from pathlib import Path

from base_conhecimento import Regra, criar_base_de_regras


# ---------------------------------------------------------------------------
# Thresholds de classificação de risco
# ---------------------------------------------------------------------------

LIMIAR_BAIXO: int = 30
LIMIAR_MEDIO: int = 60

LABELS_RISCO: dict[str, str] = {
    "baixo": "BAIXO RISCO",
    "medio": "MÉDIO RISCO",
    "alto":  "ALTO RISCO",
}


# ---------------------------------------------------------------------------
# Estrutura de resultado
# ---------------------------------------------------------------------------

@dataclass
class ResultadoInferencia:
    """Encapsula o resultado completo produzido pelo motor após a inferência."""

    pontuacao: int
    nivel_risco: str                   # 'baixo' | 'medio' | 'alto'
    regras_disparadas: list[str]       # Nomes das regras que dispararam
    conclusoes_derivadas: list[str]    # Fatos novos inseridos na memória
    recomendacoes: list[str]           # Recomendações únicas em ordem de prioridade
    falhas_detectadas: list[str]       # Perguntas em que o usuário falhou


# ---------------------------------------------------------------------------
# Motor de Inferência
# ---------------------------------------------------------------------------

class MotorInferencia:
    """
    Motor de Encadeamento Direto (Forward Chaining).

    Uso:
        motor = MotorInferencia()
        motor.adicionar_fato("reutiliza_senha", True)
        ...
        resultado = motor.executar()
    """

    def __init__(self) -> None:
        self._regras: list[Regra] = criar_base_de_regras()
        # Memória de trabalho: contém fatos do usuário + conclusões derivadas
        self._memoria: dict[str, bool] = {}
        self._pontuacao: int = 0

    def adicionar_fato(self, chave: str, valor: bool) -> None:
        """
        Insere um fato inicial na memória de trabalho.

        Args:
            chave : Identificador do fato (ex: 'reutiliza_senha').
            valor : True para Sim, False para Não.
        """
        self._memoria[chave] = valor

    def executar(self) -> ResultadoInferencia:
        """
        Executa o ciclo de inferência até o ponto fixo.

        O algoritmo segue o padrão de Encadeamento Direto:
          - Mantém uma agenda com as regras ainda não disparadas.
          - Itera sobre a agenda até não haver mais disparos.
          - Regras de Nível 2 só disparam depois que as de Nível 1
            inseriram suas conclusões na memória, demonstrando o
            encadeamento real de fatos.

        Returns:
            ResultadoInferencia com pontuação, nível, regras e recomendações.
        """
        agenda: list[Regra] = list(self._regras)
        regras_disparadas: list[str] = []
        conclusoes: list[str] = []
        recomendacoes: list[str] = []

        houve_mudanca: bool = True

        while houve_mudanca:
            houve_mudanca = False
            regras_pendentes: list[Regra] = []

            for regra in agenda:
                if regra.condicao(self._memoria):
                    # Dispara apenas se a conclusão ainda não está na memória
                    if not self._memoria.get(regra.conclusao, False):
                        self._memoria[regra.conclusao] = True
                        self._pontuacao += regra.pontos
                        regras_disparadas.append(regra.nome)
                        conclusoes.append(regra.conclusao)
                        recomendacoes.append(regra.recomendacao)
                        houve_mudanca = True
                else:
                    # Mantém na agenda regras que ainda podem disparar em
                    # iterações futuras (quando novos fatos forem inseridos)
                    regras_pendentes.append(regra)

            agenda = regras_pendentes

        falhas = self._identificar_falhas()
        nivel = self._classificar_nivel()

        return ResultadoInferencia(
            pontuacao=self._pontuacao,
            nivel_risco=nivel,
            regras_disparadas=regras_disparadas,
            conclusoes_derivadas=conclusoes,
            recomendacoes=recomendacoes,
            falhas_detectadas=falhas,
        )

    def _classificar_nivel(self) -> str:
        """Classifica o nível de risco com base na pontuação acumulada."""
        if self._pontuacao <= LIMIAR_BAIXO:
            return "baixo"
        elif self._pontuacao <= LIMIAR_MEDIO:
            return "medio"
        else:
            return "alto"

    def _identificar_falhas(self) -> list[str]:
        """
        Retorna os identificadores de fatos iniciais (perguntas) em que o
        usuário respondeu de forma insegura, para exibição no relatório.
        """
        from base_conhecimento import RESPOSTA_SEGURA_SIM

        falhas: list[str] = []
        for chave, segura_e_sim in RESPOSTA_SEGURA_SIM.items():
            valor_usuario = self._memoria.get(chave)
            if valor_usuario is None:
                continue
            # Falha = usuário respondeu diferente da resposta segura
            if segura_e_sim and valor_usuario is False:
                falhas.append(chave)
            elif not segura_e_sim and valor_usuario is True:
                falhas.append(chave)

        return falhas


# ---------------------------------------------------------------------------
# Utilitário: análise do CSV de dados mockados
# ---------------------------------------------------------------------------

def analisar_csv(caminho: Path) -> dict[str, int | float]:
    """
    Lê o CSV de dados mockados e retorna estatísticas de distribuição de
    nível de segurança, usadas como contexto comparativo no relatório.

    O CSV usa "nivel_seguranca" (perspectiva de segurança: alto = seguro),
    que é o inverso do nível de risco. A função mapeia:
      nivel_seguranca='baixo' → nivel_risco='alto'
      nivel_seguranca='medio' → nivel_risco='medio'
      nivel_seguranca='alto'  → nivel_risco='baixo'

    Args:
        caminho: Path para o arquivo CSV.

    Returns:
        Dict com contagens por nível de risco e pontuação média.
    """
    contagem: dict[str, int] = {"baixo": 0, "medio": 0, "alto": 0}
    pontuacoes: list[float] = []

    mapa_inverso: dict[str, str] = {
        "alto":  "baixo",   # segurança alta = risco baixo
        "medio": "medio",
        "baixo": "alto",    # segurança baixa = risco alto
    }

    try:
        with caminho.open(newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                nivel_seg = row.get("nivel_seguranca", "").strip().lower()
                nivel_risco = mapa_inverso.get(nivel_seg, "")
                if nivel_risco:
                    contagem[nivel_risco] += 1

                try:
                    pontuacoes.append(float(row.get("pontuacao", 0)))
                except ValueError:
                    pass

    except FileNotFoundError:
        return {"baixo": 0, "medio": 0, "alto": 0, "media_pontuacao": 0.0}

    media = round(sum(pontuacoes) / len(pontuacoes), 1) if pontuacoes else 0.0
    return {**contagem, "media_pontuacao": media}
