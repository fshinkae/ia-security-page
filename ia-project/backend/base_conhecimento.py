"""
Base de Conhecimento — Sistema Especialista de Segurança Digital
AEMS / Projeto de Extensão — IA aplicada à Educação

Contém as perguntas, opções de resposta e as regras SE...ENTÃO (IF...THEN)
utilizadas pelo motor de inferência com Encadeamento Direto (Forward Chaining).

As regras de Nível 1 avaliam cada comportamento individualmente.
As regras de Nível 2 são derivadas das conclusões do Nível 1, demonstrando
o encadeamento de fatos novos a partir de fatos anteriores.

Pesos de risco são calibrados conforme as categorias do arquivo
seguranca_digital.pl (alto → 10-15 pts, médio → 5-8 pts).
"""

from dataclasses import dataclass
from typing import Callable


# ---------------------------------------------------------------------------
# Estrutura de uma Regra
# ---------------------------------------------------------------------------

@dataclass
class Regra:
    """
    Representa uma regra de inferência no formato SE...ENTÃO.

    Atributos:
        nome         : Identificador único da regra (ex: 'R01_senha_reutilizada').
        descricao    : Enunciado legível da regra em linguagem natural.
        condicao     : Função que recebe a memória de trabalho (dict) e retorna
                       True quando a regra deve disparar.
        conclusao    : Chave do novo fato inserido na memória ao disparar.
        pontos       : Pontos de risco acumulados quando a regra dispara.
        recomendacao : Orientação prática exibida no relatório final.
        categoria    : Categoria de risco ('alto' ou 'medio'), alinhada ao .pl.
    """

    nome: str
    descricao: str
    condicao: Callable[[dict[str, bool]], bool]
    conclusao: str
    pontos: int
    recomendacao: str
    categoria: str  # 'alto' | 'medio'


# ---------------------------------------------------------------------------
# Perguntas exibidas ao usuário (mesma ordem do Prolog: q1..q10)
# ---------------------------------------------------------------------------

PERGUNTAS: dict[str, str] = {
    "reutiliza_senha":      "Você usa a mesma senha (ou senhas muito parecidas) em mais de um lugar?",
    "usa_dois_fatores":     "Sites de e-mail / redes sociais pedem um código extra (2FA) ao entrar?",
    "anota_senha":          "Você anota suas senhas em papéis, cadernos ou Bloco de Notas sem proteção?",
    "clica_link_suspeito":  "Se receber mensagem urgente sobre prêmio ou bloqueio, você clica no link?",
    "atualiza_sistema":     "Quando aparece aviso de atualização, você atualiza o sistema logo?",
    "tem_backup":           "Se seu celular sumisse hoje, seus arquivos estariam salvos em outro lugar?",
    "usa_wifi_aberto":      "Você usa Wi-Fi aberto de praças/shoppings/aeroportos sem proteção extra?",
    "verifica_permissoes":  "Antes de instalar um app, você verifica se ele pede permissões desnecessárias?",
    "tem_bloqueio_tela":    "Seu celular e computador bloqueiam a tela e pedem senha/digital para abrir?",
    "evita_pirata":         "Você evita baixar filmes, jogos e programas de sites desconhecidos ou piratas?",
}

# Mapeamento: True = resposta SIM é a resposta segura, False = NÃO é segura
RESPOSTA_SEGURA_SIM: dict[str, bool] = {
    "reutiliza_senha":      False,   # resposta segura = NÃO reutilizar
    "usa_dois_fatores":     True,    # resposta segura = SIM ter 2FA
    "anota_senha":          False,   # resposta segura = NÃO anotar
    "clica_link_suspeito":  False,   # resposta segura = NÃO clicar
    "atualiza_sistema":     True,    # resposta segura = SIM atualizar
    "tem_backup":           True,    # resposta segura = SIM ter backup
    "usa_wifi_aberto":      False,   # resposta segura = NÃO usar Wi-Fi aberto
    "verifica_permissoes":  True,    # resposta segura = SIM verificar
    "tem_bloqueio_tela":    True,    # resposta segura = SIM ter bloqueio
    "evita_pirata":         True,    # resposta segura = SIM evitar pirata
}


# ---------------------------------------------------------------------------
# Fábrica da Base de Regras
# ---------------------------------------------------------------------------

def criar_base_de_regras() -> list[Regra]:
    """
    Retorna a lista completa de regras de inferência.

    Estrutura:
      - Regras R01–R10: Nível 1 (análise individual por comportamento).
      - Regras R11–R13: Nível 2 (composição — disparam sobre conclusões
        derivadas pelas regras de Nível 1, implementando encadeamento real).

    Returns:
        Lista de objetos Regra ordenados por prioridade de avaliação.
    """
    return [

        # ══════════════════════════════════════════════════════════════════
        # NÍVEL 1 — Regras Primárias (disparam sobre fatos do usuário)
        # ══════════════════════════════════════════════════════════════════

        Regra(
            nome="R01_senha_reutilizada",
            descricao=(
                "SE o usuário reutiliza senhas em múltiplos serviços "
                "ENTÃO existe risco de credencial comprometida"
            ),
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
            descricao=(
                "SE o usuário não utiliza autenticação de dois fatores (2FA) "
                "ENTÃO existe risco de acesso não autorizado"
            ),
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
            descricao=(
                "SE o usuário anota senhas em papel ou arquivo desprotegido "
                "ENTÃO existe risco de exposição física de credencial"
            ),
            condicao=lambda f: f.get("anota_senha") is True,
            conclusao="risco_exposicao_credencial_fisica",
            pontos=10,
            categoria="alto",
            recomendacao=(
                "Nunca anote senhas em locais acessíveis. "
                "Use um gerenciador de senhas criptografado para substituir os anotados."
            ),
        ),

        Regra(
            nome="R04_clique_link_suspeito",
            descricao=(
                "SE o usuário clica em links sem verificar a origem "
                "ENTÃO existe risco de phishing / engenharia social"
            ),
            condicao=lambda f: f.get("clica_link_suspeito") is True,
            conclusao="risco_phishing",
            pontos=15,
            categoria="alto",
            recomendacao=(
                "Nunca clique em links de mensagens urgentes. "
                "Acesse o site oficial diretamente pelo navegador "
                "e verifique o remetente antes de qualquer ação."
            ),
        ),

        Regra(
            nome="R05_sistema_desatualizado",
            descricao=(
                "SE o usuário não mantém o sistema atualizado "
                "ENTÃO existe risco de vulnerabilidade de software"
            ),
            condicao=lambda f: f.get("atualiza_sistema") is False,
            conclusao="risco_vulnerabilidade_software",
            pontos=8,
            categoria="medio",
            recomendacao=(
                "Atualize sistema operacional e aplicativos assim que disponível. "
                "Atualizações corrigem falhas de segurança exploradas por atacantes."
            ),
        ),

        Regra(
            nome="R06_sem_backup",
            descricao=(
                "SE o usuário não realiza backup regular "
                "ENTÃO existe risco de perda permanente de dados"
            ),
            condicao=lambda f: f.get("tem_backup") is False,
            conclusao="risco_perda_dados",
            pontos=5,
            categoria="medio",
            recomendacao=(
                "Configure backup automático em nuvem (Google Drive, iCloud) "
                "e/ou em dispositivo externo (HD, pen drive) com cópias semanais."
            ),
        ),

        Regra(
            nome="R07_wifi_aberto",
            descricao=(
                "SE o usuário utiliza redes Wi-Fi públicas sem proteção "
                "ENTÃO existe risco de interceptação de dados (ataque MITM)"
            ),
            condicao=lambda f: f.get("usa_wifi_aberto") is True,
            conclusao="risco_interceptacao_rede",
            pontos=12,
            categoria="alto",
            recomendacao=(
                "Evite acessar contas bancárias ou dados sensíveis em Wi-Fi público. "
                "Se necessário, use uma VPN confiável para criptografar o tráfego."
            ),
        ),

        Regra(
            nome="R08_sem_verificacao_permissoes",
            descricao=(
                "SE o usuário não verifica permissões de aplicativos "
                "ENTÃO existe risco de instalação de app malicioso"
            ),
            condicao=lambda f: f.get("verifica_permissoes") is False,
            conclusao="risco_app_malicioso",
            pontos=5,
            categoria="medio",
            recomendacao=(
                "Revise as permissões solicitadas antes de instalar qualquer app. "
                "Desconfie de apps que pedem acesso à câmera, contatos ou localização "
                "sem justificativa clara."
            ),
        ),

        Regra(
            nome="R09_sem_bloqueio_tela",
            descricao=(
                "SE o usuário não possui bloqueio de tela ativo "
                "ENTÃO existe risco de acesso físico não autorizado"
            ),
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
            descricao=(
                "SE o usuário instala softwares de fontes não oficiais ou piratas "
                "ENTÃO existe risco de malware / ransomware"
            ),
            condicao=lambda f: f.get("evita_pirata") is False,
            conclusao="risco_malware",
            pontos=10,
            categoria="alto",
            recomendacao=(
                "Instale apenas softwares de lojas e sites oficiais verificados. "
                "Softwares piratas frequentemente contêm malware ou ransomware embutido."
            ),
        ),

        # ══════════════════════════════════════════════════════════════════
        # NÍVEL 2 — Regras Compostas (encadeamento sobre conclusões do N1)
        # ══════════════════════════════════════════════════════════════════

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
                "ALERTA: Suas contas estão em risco crítico de invasão. "
                "Troque todas as senhas imediatamente, use credenciais únicas "
                "e ative o 2FA em todas as contas importantes."
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
                "Você está exposto a ataques digitais combinados (phishing + exploração de falhas). "
                "Atualize todos os sistemas agora e adote cautela máxima com links recebidos."
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
                "Dispositivos desbloqueados + senhas anotadas = acesso total para quem pegar seu celular. "
                "Ative o bloqueio de tela e use um gerenciador de senhas imediatamente."
            ),
        ),
    ]