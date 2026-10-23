"""Configuración de variables de entorno."""
import os

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


def _texto(nombre, defecto=""):
    return (os.environ.get(nombre) or defecto).strip()


def _bandera(nombre, defecto="0"):
    return _texto(nombre, defecto).lower() in ("1", "true", "si", "sí", "yes")


TELEGRAM_BOT_TOKEN = _texto("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = _texto("TELEGRAM_CHAT_ID")
OPENAI_API_KEY = _texto("OPENAI_API_KEY")
ALPHAVANTAGE_API_KEY = _texto("ALPHAVANTAGE_API_KEY")
MODELO = _texto("MODELO", "gpt-5.5")
MODO_CLASE = _bandera("MODO_CLASE", "1")
MODO_SIMULACION = _bandera("MODO_SIMULACION") or not (OPENAI_API_KEY and ALPHAVANTAGE_API_KEY)
MAX_ANALISIS_POR_RUN = int(_texto("MAX_ANALISIS_POR_RUN", "3"))
CARPETA_SALIDAS = _texto("CARPETA_SALIDAS", "salidas")
