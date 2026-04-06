"""
Conexão síncrona com Supabase via supabase-py (Client).

Flask é síncrono por padrão, então usamos create_client (sync).
O cliente é inicializado uma única vez e reutilizado entre requisições.
"""

import os

from dotenv import load_dotenv
from supabase import Client, create_client

load_dotenv()

SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY: str = os.getenv("SUPABASE_SERVICE_KEY", "")

_client: Client | None = None


def get_client() -> Client:
    """Retorna o cliente Supabase, criando-o na primeira chamada."""
    global _client
    if _client is None:
        _client = create_client(SUPABASE_URL, SUPABASE_KEY)
    return _client
