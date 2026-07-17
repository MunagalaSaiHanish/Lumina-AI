"""
Central configuration for Lumixa AI.
Every configurable value in the application
should live here.
Services import from this file instead of
hardcoding values.
"""
# Embeddings
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# Chunking
CHUNK_SIZE = 500
CHUNK_OVERLAP = 100

# Retrieval
TOP_K = 5

# LLM
LLM_MODEL = "qwen/qwen3-32b"
TEMPERATURE = 0.2
MAX_TOKENS = 1500

# Future Features
ENABLE_RERANKING = False
ENABLE_QUERY_EXPANSION = False
ENABLE_HYBRID_SEARCH = False