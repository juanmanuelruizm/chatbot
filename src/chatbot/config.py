"""Configuración central del agente.

Todos los parámetros tienen un valor por defecto razonable y pueden
sobrescribirse mediante variables de entorno (opcionalmente cargadas desde
un fichero ``.env`` en la raíz del proyecto). Centralizar la configuración
evita constantes dispersas por el código y facilita ajustar el comportamiento
sin tocar la lógica.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

# Raíz del proyecto: src/chatbot/config.py -> ../../
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Carga opcional de variables desde un .env (sin fallar si python-dotenv no está).
try:
    from dotenv import load_dotenv

    load_dotenv(PROJECT_ROOT / ".env")
except ModuleNotFoundError:  # pragma: no cover - dependencia opcional
    pass


def _env(name: str, default: str) -> str:
    value = os.environ.get(name)
    return value if value is not None and value.strip() != "" else default


def _env_int(name: str, default: int) -> int:
    raw = os.environ.get(name)
    if raw is None or raw.strip() == "":
        return default
    try:
        return int(raw)
    except ValueError:
        return default


@dataclass(frozen=True)
class Settings:
    """Parámetros de configuración del agente."""

    # --- Modelos (Ollama) ---
    model: str = field(default_factory=lambda: _env("CHATBOT_MODEL", "qwen2.5:7b"))
    embedding_model: str = field(
        default_factory=lambda: _env("CHATBOT_EMBEDDING_MODEL", "qwen2.5:7b")
    )

    # --- Agent loop ---
    max_tool_rounds: int = field(
        default_factory=lambda: _env_int("CHATBOT_MAX_TOOL_ROUNDS", 10)
    )

    # --- Tools ---
    web_max_results: int = field(
        default_factory=lambda: _env_int("CHATBOT_WEB_MAX_RESULTS", 5)
    )
    code_timeout_seconds: int = field(
        default_factory=lambda: _env_int("CHATBOT_CODE_TIMEOUT", 10)
    )
    rag_top_k: int = field(default_factory=lambda: _env_int("CHATBOT_RAG_TOP_K", 5))

    # --- RAG / chunking ---
    chunk_size: int = field(default_factory=lambda: _env_int("CHATBOT_CHUNK_SIZE", 500))
    chunk_overlap: int = field(
        default_factory=lambda: _env_int("CHATBOT_CHUNK_OVERLAP", 100)
    )
    collection_name: str = field(
        default_factory=lambda: _env("CHATBOT_COLLECTION", "documents")
    )

    # --- Rutas ---
    documents_dir: Path = field(
        default_factory=lambda: Path(
            _env("CHATBOT_DOCUMENTS_DIR", str(PROJECT_ROOT / "documents"))
        )
    )
    chroma_dir: Path = field(
        default_factory=lambda: Path(
            _env("CHATBOT_CHROMA_DIR", str(PROJECT_ROOT / "chroma_db"))
        )
    )

    # Directorio base permitido para las tools de ficheros (sandbox).
    # Por defecto, el directorio de trabajo actual.
    allowed_base_dir: Path = field(
        default_factory=lambda: Path(
            _env("CHATBOT_ALLOWED_BASE_DIR", os.getcwd())
        ).resolve()
    )


settings = Settings()
