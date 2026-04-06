"""
Base de Conhecimento — Sistema Especialista de Segurança Digital
AEMS / Projeto de Extensão

Regras SE...ENTÃO (IF...THEN) para o motor de Encadeamento Direto.
Perguntas alinhadas ao seguranca_digital.pl (q1..q10).

Níveis de severidade herdados do Prolog:
  alto  → 10–15 pts
  medio →  5–8  pts
"""

from dataclasses import dataclass
from typing import Callable


@dataclass
class Regra:
    """Regra de inferência no formato SE...ENTÃO."""

    nome: str
    descricao: str
    condicao: Callable[[dict[str, bool]], bool]
    conclusao: str
    pontos: int
    recomendacao: str
    categoria: str  # 'alto' | 'medio'


# ---------------------------------------------------------------------------
# Perguntas exibidas no frontend (mesma ordem do Prolog: q1..q10)
# ---------------------------------------------------------------------------

PERGUNTAS: list[dict[str, str]] = [
    {"id": "reutiliza_senha",      "texto": "Você usa a mesma senha (ou senhas muito parecidas) em mais de um lugar?"},
    {"id": "usa_dois_fatores",     "texto": "Sites de e-mail / redes sociais pedem um código extra (2FA) ao entrar?"},
    {"id": "anota_senha",          "texto": "Você anota suas senhas em papéis, cadernos ou Bloco de Notas sem proteção?"},
    {"id": "clica_link_suspeito",  "texto": "Se receber mensagem urgente sobre prêmio ou bloqueio, você clica no link?"},
    {"id": "atualiza_sistema",     "texto": "Quando aparece aviso de atualização, você atualiza o sistema logo?"},
    {"id": "tem_backup",           "texto": "Se seu celular sumisse hoje, seus arquivos estariam salvos em outro lugar?"},
    {"id": "usa_wifi_aberto",      "texto": "Você usa Wi-Fi aberto de praças/shoppings/aeroportos sem proteção extra?"},
    {"id": "verifica_permissoes",  "texto": "Antes de instalar um app, você verifica se ele pede permissões desnecessárias?"},
    {"id": "tem_bloqueio_tela",    "texto": "Seu celular e computador bloqueiam a tela e pedem senha/digital para abrir?"},
    {"id": "evita_pirata",         "texto": "Você evita baixar filmes, jogos e programas de sites desconhecidos ou piratas?"},
]

# Resposta que indica comportamento seguro (True = Sim é seguro)
RESPOSTA_SEGURA_SIM: dict[str, bool] = {
    "reutiliza_senha":      False,
    "usa_dois_fatores":     True,
    "anota_senha":          False,
    "clica_link_suspeito":  False,
    "atualiza_sistema":     True,
    "tem_backup":           True,
    "usa_wifi_aberto":      False,
    "verifica_permissoes":  True,
    "tem_bloqueio_tela":    True,
    "evita_pirata":         True,
}


# ---------------------------------------------------------------------------
# Base de Regras
# ---------------------------------------------------------------------------

def criar_base_de_regras() -> list[Regra]:
    """
    Retorna as 13 regras do sistema (10 de Nível 1 + 3 compostas de Nível 2).

    Nível 1 — dispara sobre fatos do usuário.
    Nível 2 — dispara sobre conclusões do Nível 1 (encadeamento real).
    """
    return [

        # ── Nível 1 — Análise individual ──────────────────────────────────

        Regra(
            nome="R01_senha_reutilizada",
            descricao="SE reutiliza senhas ENTÃO risco de credencial comprometida",
            condicao=lambda f: f.get("reutiliza_senha") is True,
            conclusao="risco_credencial_comprometida",
            pontos=15,
            categoria="alto",
            recomendacao=(
                "Use senhas únicas para cada conta. Um gerenciador de senhas "
                "(Bitwarden, 1Password) cria e armazena credenciais fortes com segurança."
            ),
        ),

        Regra(
            nome="R02_sem_dois_fatores",
            descricao="SE não usa 2FA ENTÃO risco de acesso não autorizado",
            condicao=lambda f: f.get("usa_dois_fatores") is False,
            conclusao="risco_acesso_nao_autorizado",
            pontos=12,
            categoria="alto",
            recomendacao=(
                "Ative o 2FA em todas as contas principais (e-mail, redes sociais, banco). "
                "Prefira apps autenticadores (Google Authenticator, Authy) a SMS."
            ),
        ),

        Regra(
            nome="R03_senha_anotada",
            descricao="SE anota senhas sem proteção ENTÃO risco de exposição física de credencial",
            condicao=lambda f: f.get("anota_senha") is True,
            conclusao="risco_exposicao_credencial_fisica",
            pontos=10,
            categoria="alto",
            recomendacao=(
                "Nunca anote senhas em locais acessíveis. "
                "Use um gerenciador de senhas criptografado."
            ),
        ),

        Regra(
            nome="R04_clique_link_suspeito",
            descricao="SE clica em links sem verificar ENTÃO risco de phishing",
            condicao=lambda f: f.get("clica_link_suspeito") is True,
            conclusao="risco_phishing",
            pontos=15,
            categoria="alto",
            recomendacao=(
                "Nunca clique em links de mensagens urgentes. "
                "Acesse o site oficial diretamente pelo navegador e confirme o remetente."
            ),
        ),

        Regra(
            nome="R05_sistema_desatualizado",
            descricao="SE não atualiza o sistema ENTÃO risco de vulnerabilidade de software",
            condicao=lambda f: f.get("atualiza_sistema") is False,
            conclusao="risco_vulnerabilidade_software",
            pontos=8,
            categoria="medio",
            recomendacao=(
                "Atualize sistema operacional e aplicativos assim que disponível. "
                "Atualizações corrigem falhas exploradas por atacantes."
            ),
        ),

        Regra(
            nome="R06_sem_backup",
            descricao="SE não tem backup ENTÃO risco de perda permanente de dados",
            condicao=lambda f: f.get("tem_backup") is False,
            conclusao="risco_perda_dados",
            pontos=5,
            categoria="medio",
            recomendacao=(
                "Configure backup automático em nuvem (Google Drive, iCloud) "
                "e/ou dispositivo externo com cópias semanais."
            ),
        ),

        Regra(
            nome="R07_wifi_aberto",
            descricao="SE usa Wi-Fi público sem proteção ENTÃO risco de interceptação (MITM)",
            condicao=lambda f: f.get("usa_wifi_aberto") is True,
            conclusao="risco_interceptacao_rede",
            pontos=12,
            categoria="alto",
            recomendacao=(
                "Evite acessar dados sensíveis em Wi-Fi público. "
                "Se necessário, use uma VPN confiável para criptografar o tráfego."
            ),
        ),

        Regra(
            nome="R08_sem_verificacao_permissoes",
            descricao="SE não verifica permissões de apps ENTÃO risco de app malicioso",
            condicao=lambda f: f.get("verifica_permissoes") is False,
            conclusao="risco_app_malicioso",
            pontos=5,
            categoria="medio",
            recomendacao=(
                "Revise as permissões antes de instalar qualquer app. "
                "Desconfie de acesso à câmera, contatos ou localização sem justificativa."
            ),
        ),

        Regra(
            nome="R09_sem_bloqueio_tela",
            descricao="SE não tem bloqueio de tela ENTÃO risco de acesso físico não autorizado",
            condicao=lambda f: f.get("tem_bloqueio_tela") is False,
            conclusao="risco_acesso_fisico",
            pontos=8,
            categoria="medio",
            recomendacao=(
                "Ative bloqueio de tela com senha, PIN ou biometria em todos os dispositivos. "
                "Configure bloqueio automático para no máximo 1 minuto de inatividade."
            ),
        ),

        Regra(
            nome="R10_software_pirata",
            descricao="SE instala software pirata ou de fonte desconhecida ENTÃO risco de malware",
            condicao=lambda f: f.get("evita_pirata") is False,
            conclusao="risco_malware",
            pontos=10,
            categoria="alto",
            recomendacao=(
                "Instale apenas softwares de lojas e sites oficiais verificados. "
                "Softwares piratas frequentemente contêm malware ou ransomware embutido."
            ),
        ),

        # ── Nível 2 — Regras compostas (encadeamento sobre conclusões N1) ──

        Regra(
            nome="R11_perfil_conta_altamente_vulneravel",
            descricao=(
                "SE risco_credencial_comprometida (R01) "
                "E risco_acesso_nao_autorizado (R02) "
                "ENTÃO perfil de conta altamente vulnerável"
            ),
            condicao=lambda f: (
                f.get("risco_credencial_comprometida") is True
                and f.get("risco_acesso_nao_autorizado") is True
            ),
            conclusao="perfil_conta_altamente_vulneravel",
            pontos=10,
            categoria="alto",
            recomendacao=(
                "ALERTA: Senhas reutilizadas + sem 2FA = suas contas estão em risco crítico. "
                "Troque todas as senhas e ative o 2FA imediatamente."
            ),
        ),

        Regra(
            nome="R12_perfil_alto_risco_digital",
            descricao=(
                "SE risco_phishing (R04) "
                "E risco_vulnerabilidade_software (R05) "
                "ENTÃO perfil de alto risco a ataques digitais combinados"
            ),
            condicao=lambda f: (
                f.get("risco_phishing") is True
                and f.get("risco_vulnerabilidade_software") is True
            ),
            conclusao="perfil_alto_risco_ataque_digital",
            pontos=10,
            categoria="alto",
            recomendacao=(
                "Phishing + sistema desatualizado: você está exposto a ataques combinados. "
                "Atualize todos os sistemas e nunca clique em links sem verificar a origem."
            ),
        ),

        Regra(
            nome="R13_risco_comprometimento_fisico_total",
            descricao=(
                "SE risco_acesso_fisico (R09) "
                "E risco_exposicao_credencial_fisica (R03) "
                "ENTÃO risco de comprometimento físico total"
            ),
            condicao=lambda f: (
                f.get("risco_acesso_fisico") is True
                and f.get("risco_exposicao_credencial_fisica") is True
            ),
            conclusao="risco_comprometimento_fisico_total",
            pontos=8,
            categoria="alto",
            recomendacao=(
                "Dispositivo desbloqueado + senha anotada = acesso total para quem pegar seu celular. "
                "Ative o bloqueio de tela e use um gerenciador de senhas."
            ),
        ),
    ]
