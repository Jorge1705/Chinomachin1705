"""Comunicación segura con Telegram."""
import requests
from . import config

LIMITE_MENSAJE = 4000
TIMEOUT = 20

def _url(metodo):
    if not config.TELEGRAM_BOT_TOKEN:
        raise RuntimeError("Falta TELEGRAM_BOT_TOKEN")
    return f"https://api.telegram.org/bot{config.TELEGRAM_BOT_TOKEN}/{metodo}"

def _datos(respuesta):
    respuesta.raise_for_status()
    datos = respuesta.json()
    if not datos.get("ok"):
        raise RuntimeError("Telegram rechazó la solicitud")
    return datos

def enviar(chat_id, texto):
    return _datos(requests.post(_url("sendMessage"), data={"chat_id": chat_id, "text": str(texto)[:LIMITE_MENSAJE]}, timeout=TIMEOUT))

def verificar_bot():
    return _datos(requests.get(_url("getMe"), timeout=TIMEOUT))["result"]["username"]

def preparar_polling():
    _datos(requests.get(_url("deleteWebhook"), timeout=TIMEOUT))

def obtener_mensajes(offset=None, espera=0):
    parametros = {"timeout": min(max(int(espera), 0), 30)}
    if offset is not None:
        parametros["offset"] = int(offset)
    return _datos(requests.get(_url("getUpdates"), params=parametros, timeout=parametros["timeout"] + TIMEOUT))["result"]

def confirmar_leidos(ultimo_update_id):
    obtener_mensajes(offset=int(ultimo_update_id) + 1)

def chat_autorizado(chat_id):
    return bool(config.TELEGRAM_CHAT_ID) and str(chat_id) == config.TELEGRAM_CHAT_ID
