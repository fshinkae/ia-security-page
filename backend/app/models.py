"""
Modelos Pydantic para validação de entrada da API Flask.

Usado apenas para validar o corpo do POST /api/diagnostico.
Respostas são retornadas como dicts simples via jsonify.
"""

from pydantic import BaseModel, Field, field_validator


class RespostasInput(BaseModel):
    """Corpo do POST /api/diagnostico."""

    nome: str | None = Field(default=None)
    respostas: dict[str, bool] = Field(
        description="Mapa de ID da pergunta → bool (True=Sim, False=Não)"
    )

    @field_validator("respostas")
    @classmethod
    def validar_perguntas(cls, v: dict[str, bool]) -> dict[str, bool]:
        from app.knowledge_base import RESPOSTA_SEGURA_SIM
        ids_validos = set(RESPOSTA_SEGURA_SIM.keys())
        ids_recebidos = set(v.keys())
        desconhecidos = ids_recebidos - ids_validos
        if desconhecidos:
            raise ValueError(f"IDs de pergunta desconhecidos: {desconhecidos}")
        ausentes = ids_validos - ids_recebidos
        if ausentes:
            raise ValueError(f"Respostas ausentes para: {ausentes}")
        return v
