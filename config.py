import os
from pathlib import Path

STORAGE_FOLDER = str(Path.cwd() / "storage")
Path(STORAGE_FOLDER).mkdir(parents=True, exist_ok=True)

DB_PORT=5432
DB_NAME="document_library"
DB_USER="postgres"
DB_PASSWORD=12345
CHUNK_SIZE = 800
MAX_FILE_SIZE = 10 * 1024 * 1024 