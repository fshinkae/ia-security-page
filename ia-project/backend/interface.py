"""
Interface de Linha de Comando (CLI) — Sistema Especialista de Segurança Digital
AEMS / Projeto de Extensão

Fluxo:
  1. Exibe cabeçalho e instruções.
  2. Coleta as 10 respostas do usuário (sim/não).
  3. Alimenta o motor de inferência com os fatos.
  4. Exibe relatório completo: pontuação, nível de risco, falhas detectadas,
     recomendações e contexto estatístico da base de dados mockada.

Execute com:
    python interface.py
"""

import os
import sys
from pathlib import Path

# Garante que o diretório do pacote está no path ao executar diretamente
sys.path.insert(0, str(Path(__file__).parent))

from base_conhecimento import PERGUNTAS, RESPOSTA_SEGURA_SIM
from motor_inferencia import MotorInferencia, LABELS_RISCO, analisar_csv

# Caminho para o CSV de dados mockados (sobe um nível a partir de backend/)
CSV_PATH: Path = Path(__file__).parent.parent / "dados_mockados.csv"

# ---------------------------------------------------------------------------
# Códigos de cor ANSI
# ---------------------------------------------------------------------------

RESET   = "\033[0m"
BOLD    = "\033[1m"
RED     = "\033[91m"
YELLOW  = "\033[93m"
GREEN   = "\033[92m"
CYAN    = "\033[96m"
DIM     = "\033[2m"


# ---------------------------------------------------------------------------
# Utilitários de exibição
# ---------------------------------------------------------------------------

def limpar_tela() -> None:
    """Limpa o terminal (compatível com Windows e Unix)."""
    os.system("cls" if os.name == "nt" else "clear")


def cor_por_nivel(nivel: str) -> str:
    """Retorna o código de cor ANSI correspondente ao nível de risco."""
    return {
        "baixo": GREEN,
        "medio": YELLOW,
        "alto":  RED,
    }.get(nivel, RESET)


def _barra_progresso(valor: int, maximo: int, largura: int = 30) -> str:
    """Gera uma barra de progresso ASCII simples."""
    preenchido = int(largura * valor / max(maximo, 1))
    return "█" * preenchido + "░" * (largura - preenchido)


def exibir_cabecalho() -> None:
    print(f"{CYAN}{BOLD}")
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║  SISTEMA ESPECIALISTA DE SEGURANÇA DIGITAL — AEMS / TADS   ║")
    print("║  Diagnóstico de Risco • Encadeamento Direto (Forward Chain) ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    print(f"{RESET}")
    print(
        f"{DIM}Responda com  {BOLD}s{RESET}{DIM} (sim)  ou  {BOLD}n{RESET}{DIM} (não). "
        f"Não há respostas certas ou erradas — seja honesto(a).{RESET}\n"
    )


# ---------------------------------------------------------------------------
# Coleta de respostas
# ---------------------------------------------------------------------------

def fazer_perguntas() -> dict[str, bool]:
    """
    Exibe as perguntas interativamente e retorna um dicionário de fatos
    booleanos (True = Sim, False = Não).

    Returns:
        Dict mapeando chave da pergunta → bool.
    """
    fatos: dict[str, bool] = {}
    total = len(PERGUNTAS)

    for i, (chave, pergunta) in enumerate(PERGUNTAS.items(), start=1):
        prefixo = f"{CYAN}[{i:02d}/{total:02d}]{RESET}"

        while True:
            resposta = input(f"{prefixo} {pergunta}\n         → ").strip().lower()

            if resposta in ("s", "sim"):
                fatos[chave] = True
                break
            elif resposta in ("n", "nao", "não"):
                fatos[chave] = False
                break
            else:
                print(f"         {YELLOW}⚠  Digite 's' para Sim ou 'n' para Não.{RESET}")

        print()

    return fatos


# ---------------------------------------------------------------------------
# Exibição do relatório
# ---------------------------------------------------------------------------

def exibir_relatorio(
    resultado,
    stats: dict[str, int | float],
) -> None:
    """
    Imprime o relatório de diagnóstico formatado no terminal.

    Args:
        resultado : ResultadoInferencia retornado pelo motor.
        stats     : Estatísticas da base de dados mockada (CSV).
    """
    cor   = cor_por_nivel(resultado.nivel_risco)
    label = LABELS_RISCO[resultado.nivel_risco]
    total_csv = sum(v for k, v in stats.items() if k != "media_pontuacao") or 1

    # ── Cabeçalho do relatório ─────────────────────────────────────────────
    print(f"\n{BOLD}{CYAN}{'═' * 64}{RESET}")
    print(f"{BOLD}  RELATÓRIO DE DIAGNÓSTICO — SEGURANÇA DIGITAL{RESET}")
    print(f"{BOLD}{CYAN}{'═' * 64}{RESET}\n")

    # ── Pontuação e nível ──────────────────────────────────────────────────
    barra = _barra_progresso(resultado.pontuacao, 128, largura=20)
    print(f"  Pontuação de Risco : {BOLD}{resultado.pontuacao} pts{RESET}  {cor}{barra}{RESET}")
    print(f"  Nível de Risco     : {cor}{BOLD}{label}{RESET}\n")

    # ── Fatores de risco (regras que dispararam) ───────────────────────────
    print(f"{BOLD}  Fatores de risco identificados  ({len(resultado.regras_disparadas)} regra(s)):{RESET}")
    if resultado.regras_disparadas:
        for regra in resultado.regras_disparadas:
            # Destaca regras de Nível 2 (compostas)
            prefixo_icon = f"{RED}✗{RESET}"
            print(f"    {prefixo_icon} {regra}")
    else:
        print(f"    {GREEN}✓  Nenhum fator de risco detectado.{RESET}")

    # ── Perguntas em que o usuário falhou ──────────────────────────────────
    if resultado.falhas_detectadas:
        print(f"\n{BOLD}  Áreas com comportamento de risco:{RESET}")
        for falha in resultado.falhas_detectadas:
            pergunta_resumida = PERGUNTAS.get(falha, falha)[:60]
            print(f"    {YELLOW}•{RESET} {pergunta_resumida}...")

    # ── Recomendações práticas ─────────────────────────────────────────────
    print(f"\n{BOLD}  Recomendações práticas:{RESET}")

    # Remove duplicatas mantendo a ordem de prioridade
    vistas: set[str] = set()
    idx = 1
    for rec in resultado.recomendacoes:
        if rec not in vistas:
            vistas.add(rec)
            print(f"\n  {BOLD}{idx}.{RESET} {rec}")
            idx += 1

    if idx == 1:
        print(f"  {GREEN}✓  Continue com seus excelentes hábitos de segurança!{RESET}")

    # ── Contexto estatístico (CSV) ─────────────────────────────────────────
    print(f"\n{BOLD}{CYAN}{'─' * 64}{RESET}")
    print(
        f"{BOLD}  Contexto — Base de dados AEMS "
        f"(n={total_csv} usuários):{RESET}"
    )
    for nivel_key, label_nivel in [("alto", "Alto Risco"), ("medio", "Médio Risco"), ("baixo", "Baixo Risco")]:
        qtd = stats.get(nivel_key, 0)
        perc = int(qtd) / total_csv * 100
        barra_csv = _barra_progresso(int(perc), 100, largura=20)
        cor_b = cor_por_nivel(nivel_key)
        print(
            f"    {cor_b}{label_nivel:12s}{RESET}  "
            f"{qtd:2d} usuários  {cor_b}{barra_csv}{RESET}  {perc:.0f}%"
        )

    media_pontuacao = stats.get("media_pontuacao", 0.0)
    print(
        f"\n  Pontuação média de segurança na base: "
        f"{BOLD}{media_pontuacao}/10{RESET} "
        f"{DIM}(escala original do CSV){RESET}"
    )

    # ── Conclusão contextualizada ──────────────────────────────────────────
    print(f"\n{BOLD}{CYAN}{'═' * 64}{RESET}")
    _exibir_conclusao(resultado.nivel_risco)
    print(f"{BOLD}{CYAN}{'═' * 64}{RESET}\n")


def _exibir_conclusao(nivel: str) -> None:
    """Exibe mensagem de encerramento contextualizada ao nível de risco."""
    mensagens = {
        "baixo": (
            f"  {GREEN}{BOLD}Parabéns!{RESET} Você demonstra ótimos hábitos de segurança digital.\n"
            f"  Continue se mantendo atualizado(a) sobre novas ameaças."
        ),
        "medio": (
            f"  {YELLOW}{BOLD}Atenção!{RESET} Você já tem boas práticas, mas há pontos a melhorar.\n"
            f"  Aplique as recomendações acima para reduzir sua exposição."
        ),
        "alto": (
            f"  {RED}{BOLD}ALERTA!{RESET} Seus hábitos digitais precisam de ajustes urgentes.\n"
            f"  Implemente as recomendações acima o quanto antes para se proteger."
        ),
    }
    print(mensagens.get(nivel, ""))


# ---------------------------------------------------------------------------
# Ponto de entrada
# ---------------------------------------------------------------------------

def main() -> None:
    """Função principal: orquestra o fluxo completo da aplicação CLI."""
    limpar_tela()
    exibir_cabecalho()

    # 1. Coleta respostas do usuário
    fatos = fazer_perguntas()

    # 2. Inicializa e alimenta o motor de inferência
    motor = MotorInferencia()
    for chave, valor in fatos.items():
        motor.adicionar_fato(chave, valor)

    # 3. Executa o ciclo de encadeamento direto
    resultado = motor.executar()

    # 4. Carrega estatísticas comparativas do CSV
    stats = analisar_csv(CSV_PATH)

    # 5. Exibe relatório final
    exibir_relatorio(resultado, stats)


if __name__ == "__main__":
    main()
