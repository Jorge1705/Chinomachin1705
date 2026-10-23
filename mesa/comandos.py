"""Comandos del bot privado."""
from .pipeline import normalizar_ticker, pipeline
from .telegram_io import chat_autorizado, enviar

AYUDA = "🤖 Mesa Financiera. Usa: /analiza AAPL"

def es_analisis(texto):
    return (texto or "").strip().lower().startswith("/analiza")

def atender(mensaje):
    chat_id = (mensaje.get("chat") or {}).get("id")
    if chat_id is None or not chat_autorizado(chat_id):
        return None
    texto = (mensaje.get("text") or "").strip()
    if not es_analisis(texto):
        enviar(chat_id, AYUDA)
        return None
    try:
        ticker = normalizar_ticker(texto.split()[1] if len(texto.split()) > 1 else "")
    except ValueError:
        enviar(chat_id, "Escribe un ticker válido. Ejemplo: /analiza MSFT")
        return None
    resultado = pipeline(ticker, avisar=lambda avance: enviar(chat_id, avance))
    enviar(chat_id, resultado["entrega_3_nota"])
    return resultado
