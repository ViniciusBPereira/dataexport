import logging
import os
import time
from logging.handlers import RotatingFileHandler

# Garante que a pasta logs existe
os.makedirs("logs", exist_ok=True)

# Define nível de log pelo ambiente (default: INFO)
log_level = os.getenv("LOG_LEVEL", "INFO").upper()

# Handler para arquivo com rotação
file_handler = RotatingFileHandler(
    "logs/data_export.log",
    maxBytes=10 * 1024 * 1024,  # 10 MB
    backupCount=5,
    encoding="utf-8"
)

# Handler para console
console_handler = logging.StreamHandler()
console_handler.setLevel(getattr(logging, log_level, logging.INFO))

# Formato do log
formatter = logging.Formatter(
    "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)

# Força uso de UTC (troque por time.localtime se preferir horário local)
logging.Formatter.converter = time.gmtime

file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Configuração final
logging.basicConfig(
    level=getattr(logging, log_level, logging.INFO),
    handlers=[file_handler, console_handler]
)

# Logger principal
logger = logging.getLogger("DataExport")
