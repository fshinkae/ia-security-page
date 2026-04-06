"""
Flask — Sistema Especialista de Segurança Digital (AEMS)

Rotas disponíveis:
  GET  /api/perguntas              → lista as 10 perguntas do questionário
  POST /api/diagnostico            → executa o motor de inferência e salva no Supabase
  GET  /api/diagnosticos           → lista diagnósticos salvos (paginado)
  GET  /api/diagnosticos/<id>      → retorna um diagnóstico pelo UUID
  GET  /api/estatisticas           → estatísticas agregadas dos diagnósticos
"""

import os
from datetime import datetime, timezone

from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_cors import CORS
from pydantic import ValidationError

from app.database import get_client
from app.inference import MotorInferencia
from app.knowledge_base import PERGUNTAS
from app.models import RespostasInput

load_dotenv()

TABLE = "diagnosticos"

LABELS_RISCO: dict[str, str] = {
    "baixo": "BAIXO RISCO",
    "medio": "MÉDIO RISCO",
    "alto":  "ALTO RISCO",
}

app = Flask(__name__)

_origins_raw = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://localhost:4173")
origins = [o.strip() for o in _origins_raw.split(",") if o.strip()]
CORS(app, origins=origins, methods=["GET", "POST"], allow_headers=["Content-Type"])


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _row_para_dict(row: dict) -> dict:
    """Serializa uma linha do Supabase para resposta JSON completa."""
    return {
        "id":                  row["id"],
        "nome":                row.get("nome"),
        "pontuacao":           row["pontuacao"],
        "nivel_risco":         row["nivel_risco"],
        "label_risco":         LABELS_RISCO[row["nivel_risco"]],
        "regras_disparadas":   row["regras_disparadas"],
        "conclusoes_derivadas":row["conclusoes_derivadas"],
        "recomendacoes":       row["recomendacoes"],
        "falhas_detectadas":   row["falhas_detectadas"],
        "criado_em":           row["criado_em"],
    }


def _row_para_list_item(row: dict) -> dict:
    return {
        "id":          row["id"],
        "nome":        row.get("nome"),
        "pontuacao":   row["pontuacao"],
        "nivel_risco": row["nivel_risco"],
        "label_risco": LABELS_RISCO[row["nivel_risco"]],
        "criado_em":   row["criado_em"],
    }


# ---------------------------------------------------------------------------
# Rotas
# ---------------------------------------------------------------------------

@app.get("/api/perguntas")
def listar_perguntas():
    """Retorna as 10 perguntas para o frontend renderizar o formulário."""
    return jsonify(PERGUNTAS)


@app.post("/api/diagnostico")
def criar_diagnostico():
    """
    Recebe as respostas do usuário, executa o motor de Encadeamento Direto,
    persiste no Supabase e retorna o relatório completo.

    Body JSON:
      { "nome": "João (opcional)", "respostas": { "reutiliza_senha": true, ... } }
    """
    body = request.get_json(silent=True)
    if not body:
        return jsonify({"erro": "Body JSON inválido ou ausente"}), 400

    try:
        entrada = RespostasInput.model_validate(body)
    except ValidationError as e:
        erros = [{"campo": err["loc"], "msg": err["msg"]} for err in e.errors()]
        return jsonify({"erro": "Dados inválidos", "detalhes": erros}), 422

    # Executa o motor de inferência
    motor = MotorInferencia(entrada.respostas)
    resultado = motor.executar()

    # Deduplica recomendações mantendo ordem de prioridade
    vistas: set[str] = set()
    recs_unicas: list[str] = []
    for rec in resultado.recomendacoes:
        if rec not in vistas:
            vistas.add(rec)
            recs_unicas.append(rec)

    row = {
        "nome":                entrada.nome,
        "respostas":           entrada.respostas,
        "pontuacao":           resultado.pontuacao,
        "nivel_risco":         resultado.nivel_risco,
        "regras_disparadas":   resultado.regras_disparadas,
        "conclusoes_derivadas":resultado.conclusoes_derivadas,
        "recomendacoes":       recs_unicas,
        "falhas_detectadas":   resultado.falhas_detectadas,
        "criado_em":           datetime.now(timezone.utc).isoformat(),
    }

    sb = get_client()
    result = sb.table(TABLE).insert(row).execute()

    if not result.data:
        return jsonify({"erro": "Erro ao salvar diagnóstico no Supabase"}), 500

    return jsonify(_row_para_dict(result.data[0])), 201


@app.get("/api/diagnosticos")
def listar_diagnosticos():
    """
    Lista diagnósticos salvos, do mais recente ao mais antigo.
    Query params: pagina (int), por_pagina (int), nivel (baixo|medio|alto)
    """
    try:
        pagina    = max(1, int(request.args.get("pagina", 1)))
        por_pagina = min(100, max(1, int(request.args.get("por_pagina", 10))))
    except ValueError:
        return jsonify({"erro": "pagina e por_pagina devem ser inteiros"}), 400

    nivel = request.args.get("nivel")
    if nivel and nivel not in ("baixo", "medio", "alto"):
        return jsonify({"erro": "nivel deve ser 'baixo', 'medio' ou 'alto'"}), 400

    skip = (pagina - 1) * por_pagina
    fim  = skip + por_pagina - 1

    sb = get_client()
    query = (
        sb.table(TABLE)
        .select("id, nome, pontuacao, nivel_risco, criado_em", count="exact")
        .order("criado_em", desc=True)
        .range(skip, fim)
    )
    if nivel:
        query = query.eq("nivel_risco", nivel)

    result = query.execute()

    return jsonify({
        "total":      result.count or 0,
        "pagina":     pagina,
        "por_pagina": por_pagina,
        "resultados": [_row_para_list_item(r) for r in result.data],
    })


@app.get("/api/diagnosticos/<diagnostico_id>")
def obter_diagnostico(diagnostico_id: str):
    """Busca um diagnóstico pelo UUID."""
    sb = get_client()
    result = (
        sb.table(TABLE)
        .select("*")
        .eq("id", diagnostico_id)
        .maybe_single()
        .execute()
    )

    if result.data is None:
        return jsonify({"erro": "Diagnóstico não encontrado"}), 404

    return jsonify(_row_para_dict(result.data))


@app.get("/api/estatisticas")
def obter_estatisticas():
    """
    Retorna totais e médias dos diagnósticos.
    Usa a RPC stats_diagnosticos() do Supabase; cai para agregação Python se falhar.
    """
    sb = get_client()

    try:
        rows = sb.rpc("stats_diagnosticos").execute().data
    except Exception:
        raw = sb.table(TABLE).select("nivel_risco, pontuacao").execute().data or []
        agrupado: dict[str, dict] = {}
        for r in raw:
            n = r["nivel_risco"]
            if n not in agrupado:
                agrupado[n] = {"nivel_risco": n, "quantidade": 0, "soma_pontuacao": 0}
            agrupado[n]["quantidade"] += 1
            agrupado[n]["soma_pontuacao"] += r["pontuacao"]
        rows = list(agrupado.values())

    por_nivel: dict[str, int] = {"baixo": 0, "medio": 0, "alto": 0}
    total = 0
    soma_total = 0.0

    for row in rows or []:
        nivel = row["nivel_risco"]
        qtd   = row["quantidade"]
        if nivel in por_nivel:
            por_nivel[nivel] = qtd
            total += qtd
            soma_total += row["soma_pontuacao"]

    media = round(soma_total / total, 1) if total > 0 else 0.0
    percentual = {
        k: round(v / total * 100, 1) if total > 0 else 0.0
        for k, v in por_nivel.items()
    }

    return jsonify({
        "total":               total,
        "por_nivel":           por_nivel,
        "media_pontuacao":     media,
        "percentual_por_nivel":percentual,
    })
