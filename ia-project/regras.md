# Regras do Sistema Especialista de Segurança Digital

**Projeto:** Sistema Especialista Educacional — Segurança Digital
**Instituição:** AEMS — Associação Educacional Magsul
**Paradigma:** Encadeamento Direto (Forward Chaining)
**Implementação:** Python 3.12+ (`base_conhecimento.py`, `motor_inferencia.py`)

---

## 1. Introdução

Este documento descreve em linguagem natural todas as regras de inferência
do sistema especialista. As regras seguem o padrão **SE (condição) → ENTÃO (conclusão)**,
onde cada conclusão pode se tornar um novo fato e servir de premissa para
regras subsequentes — caracterizando o **Encadeamento Direto**.

---

## 2. Regras de Nível 1 — Análise Individual de Comportamentos

Cada regra avalia uma resposta direta do usuário e insere uma conclusão
(fato derivado) na memória de trabalho. Os pesos de risco refletem a
categoria de severidade definida em `seguranca_digital.pl`.

| ID  | Categoria Prolog          | Condição (SE)                                                   | Conclusão (ENTÃO)                        | Pontos | Severidade |
|-----|---------------------------|-----------------------------------------------------------------|------------------------------------------|--------|------------|
| R01 | `reutilizacao_senha`      | Usuário reutiliza senhas em múltiplos serviços                  | `risco_credencial_comprometida`          | 15 pts | Alto       |
| R02 | `autenticacao_dois_fatores`| Usuário **não** utiliza 2FA em contas principais               | `risco_acesso_nao_autorizado`            | 12 pts | Alto       |
| R03 | `armazenamento_senha`     | Usuário anota senhas em papel ou arquivo desprotegido           | `risco_exposicao_credencial_fisica`      | 10 pts | Alto       |
| R04 | `phishing`                | Usuário clica em links recebidos sem verificar a origem         | `risco_phishing`                         | 15 pts | Alto       |
| R05 | `atualizacao_sistema`     | Usuário **não** mantém sistema e aplicativos atualizados        | `risco_vulnerabilidade_software`         | 8 pts  | Médio      |
| R06 | `backup_dados`            | Usuário **não** realiza backup regular dos dados                | `risco_perda_dados`                      | 5 pts  | Médio      |
| R07 | `wifi_publico`            | Usuário usa redes Wi-Fi públicas/abertas sem proteção           | `risco_interceptacao_rede`               | 12 pts | Alto       |
| R08 | `permissoes_app`          | Usuário **não** verifica permissões de apps antes de instalar   | `risco_app_malicioso`                    | 5 pts  | Médio      |
| R09 | `bloqueio_tela`           | Usuário **não** possui bloqueio de tela (senha/biometria/PIN)   | `risco_acesso_fisico`                    | 8 pts  | Médio      |
| R10 | `downloads_seguros`       | Usuário instala softwares piratas ou de fontes desconhecidas    | `risco_malware`                          | 10 pts | Alto       |

**Pontuação máxima (Nível 1):** 100 pts

---

## 3. Regras de Nível 2 — Análise Composta (Encadeamento Direto)

Estas regras **não avaliam respostas do usuário diretamente**.
Elas avaliam *conclusões derivadas pelas Regras de Nível 1*, demonstrando
o encadeamento real: novos fatos geram novas inferências.

| ID  | Premissas (fatos derivados)                                          | Conclusão (ENTÃO)                      | Pontos | Descrição                                                             |
|-----|----------------------------------------------------------------------|----------------------------------------|--------|-----------------------------------------------------------------------|
| R11 | `risco_credencial_comprometida` (R01) **E** `risco_acesso_nao_autorizado` (R02) | `perfil_conta_altamente_vulneravel` | 10 pts | Senhas fracas + ausência de 2FA = conta praticamente sem proteção     |
| R12 | `risco_phishing` (R04) **E** `risco_vulnerabilidade_software` (R05)  | `perfil_alto_risco_ataque_digital`    | 10 pts | Phishing + sistema desatualizado = vetores de ataque combinados       |
| R13 | `risco_acesso_fisico` (R09) **E** `risco_exposicao_credencial_fisica` (R03) | `risco_comprometimento_fisico_total` | 8 pts  | Dispositivo desbloqueado + senha anotada = acesso total por terceiros |

**Pontuação máxima adicional (Nível 2):** 28 pts
**Pontuação máxima total:** 128 pts

---

## 4. Classificação de Risco

| Faixa de Pontuação | Nível       | Interpretação                                              |
|--------------------|-------------|------------------------------------------------------------|
| 0 – 30 pts         | Baixo Risco | Comportamento predominantemente seguro. Manutenção preventiva. |
| 31 – 60 pts        | Médio Risco | Vulnerabilidades presentes. Ação corretiva necessária.     |
| > 60 pts           | Alto Risco  | Exposição crítica a múltiplas ameaças. Medidas urgentes.   |

---

## 5. Lógica de Encadeamento Direto — Fluxo de Execução

```
┌─────────────────────────────────────────────────────────────────┐
│  MEMÓRIA DE TRABALHO (Fatos iniciais do usuário)                │
│  reutiliza_senha=True, usa_dois_fatores=False, ...              │
└────────────────────────────┬────────────────────────────────────┘
                             │  Iteração 1
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│  AVALIA R01–R10 (Nível 1)                                       │
│  → Dispara R01: insere risco_credencial_comprometida = True     │
│  → Dispara R02: insere risco_acesso_nao_autorizado = True       │
│  → Dispara R04: insere risco_phishing = True                    │
│  → ... (demais regras de Nível 1 aplicáveis)                    │
└────────────────────────────┬────────────────────────────────────┘
                             │  Iteração 2 (novos fatos disponíveis)
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│  AVALIA R11–R13 (Nível 2 — sobre conclusões do Nível 1)         │
│  → R11 dispara: risco_credencial_comprometida AND               │
│                 risco_acesso_nao_autorizado → +10 pts           │
│  → R12 dispara: risco_phishing AND                              │
│                 risco_vulnerabilidade_software → +10 pts        │
└────────────────────────────┬────────────────────────────────────┘
                             │  Iteração 3 (ponto fixo — nada novo)
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│  RESULTADO FINAL                                                │
│  Pontuação acumulada → Classificação → Relatório               │
└─────────────────────────────────────────────────────────────────┘
```

---

## 6. Correspondência com a Base Prolog (`seguranca_digital.pl`)

| Pergunta Python         | Predicado Prolog           | Risco Associado (Prolog)  |
|-------------------------|----------------------------|---------------------------|
| `reutiliza_senha`       | `pergunta(q1, ...)`        | `invasao_conta`           |
| `usa_dois_fatores`      | `pergunta(q2, ...)`        | `invasao_conta`           |
| `anota_senha`           | `pergunta(q3, ...)`        | `roubo_senha`             |
| `clica_link_suspeito`   | `pergunta(q4, ...)`        | `engenharia_social`       |
| `atualiza_sistema`      | `pergunta(q5, ...)`        | `malware`                 |
| `tem_backup`            | `pergunta(q6, ...)`        | `perda_dados`             |
| `usa_wifi_aberto`       | `pergunta(q7, ...)`        | `interceptacao_dados`     |
| `verifica_permissoes`   | `pergunta(q8, ...)`        | `malware`                 |
| `tem_bloqueio_tela`     | `pergunta(q9, ...)`        | `acesso_fisico`           |
| `evita_pirata`          | `pergunta(q10, ...)`       | `malware`                 |

---

## 7. Referências

- Russell, S.; Norvig, P. *Artificial Intelligence: A Modern Approach*, 4ª ed. — Cap. 7 (Logical Agents).
- Giarratano, J.; Riley, G. *Expert Systems: Principles and Programming*, 4ª ed.
- CSV de dados: `dados_mockados.csv` — 50 perfis de usuários com hábitos e pontuação de segurança.
