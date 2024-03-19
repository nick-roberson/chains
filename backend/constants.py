import os

# Open AI API Key
OPENAI_API_KEY_VAR: str = "OPENAI_API_KEY"
OPENAI_API_KEY: str = os.environ.get(OPENAI_API_KEY_VAR, None)

# Data Paths
TEXTS_DATA_PATH: str = "backend/knowledge_base/"

# Storage Paths
PERSIST_DIR = "backend/persist/"

# Host and Port
HOST_NAME: str = "localhost"
HOST_PORT: int = 8000
