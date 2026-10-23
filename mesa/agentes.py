import json
import requests
from . import config

DESCARGO = "Nota educativa, no es recomendación de inversión."
FIRMA_VERA = "✍️ Vera · Comunicadora"


def llamar_openai(instrucciones, mensaje, max_tokens=900):
    from openai import OpenAI
    respuesta = OpenAI(api_key=config.OPENAI_API_KEY).responses.create(model=config.MODELO, instructions=instrucciones, input=mensaje, max_output_tokens=max_tokens)
    return respuesta.output_text.strip()


def extraer_json(texto):
    inicio, fin = texto.find("{"), texto.rfind("}")
    if inicio < 0 or fin < inicio:
        raise ValueError("OpenAI no devolvió JSON")
    return json.loads(texto[inicio:fin + 1])


def a_numero(valor):
    try:
        return float(str(valor).replace(",", "").replace("%", ""))
    except (TypeError, ValueError):
        return None


def ficha_demo(ticker, motivo="SIMULACIÓN"):
    return {"ticker": ticker, "precio": "250.5", "max_52s": "300", "min_52s": "200", "beta": "0.7", "fuente": "DEMO (" + motivo + ")"}


def agente_recolector(ticker):
    if config.MODO_SIMULACION:
        return ficha_demo(ticker), []
    try:
        base = "https://www.alphavantage.co/query"
        quote = requests.get(base, params={"function": "GLOBAL_QUOTE", "symbol": ticker, "apikey": config.ALPHAVANTAGE_API_KEY}, timeout=15).json().get("Global Quote", {})
        overview = requests.get(base, params={"function": "OVERVIEW", "symbol": ticker, "apikey": config.ALPHAVANTAGE_API_KEY}, timeout=15).json()
        return {"ticker": ticker, "precio": quote.get("05. price"), "max_52s": overview.get("52WeekHigh"), "min_52s": overview.get("52WeekLow"), "beta": overview.get("Beta"), "fuente": "Alpha Vantage (API directa)"}, ["GLOBAL_QUOTE", "OVERVIEW"]
    except Exception:
        return ficha_demo(ticker, "sin conexión"), []


def calcular_indicadores(ficha):
    precio, alto, bajo, beta = map(a_numero, (ficha.get("precio"), ficha.get("max_52s"), ficha.get("min_52s"), ficha.get("beta")))
    posicion = round((precio - bajo) * 100 / (alto - bajo), 1) if None not in (precio, alto, bajo) and alto != bajo else None
    color = "⚪" if beta is None else "🟢" if beta < .8 else "🟡" if beta < 1.3 else "🔴"
    return {"posicion_rango_52s_pct": posicion, "semaforo_beta": color + " beta " + str(beta if beta is not None else "sin dato")}


def agente_analista(ficha):
    indicadores = calcular_indicadores(ficha)
    if config.MODO_SIMULACION:
        return {"ficha": ficha, "indicadores": indicadores, "lectura": "Análisis simulado"}
    datos = extraer_json(llamar_openai("Eres analista financiero educativo. Responde JSON.", json.dumps({"ficha": ficha, "indicadores": indicadores}, ensure_ascii=False)))
    return {"ficha": ficha, "indicadores": indicadores, **datos}


def agente_comunicador(analisis):
    if config.MODO_SIMULACION:
        return FIRMA_VERA + "\n" + analisis["ficha"]["ticker"] + ": análisis simulado.\n" + DESCARGO
    nota = llamar_openai("Redacta una nota financiera educativa breve.", json.dumps(analisis, ensure_ascii=False))
    return FIRMA_VERA + "\n" + nota + "\n" + DESCARGO
