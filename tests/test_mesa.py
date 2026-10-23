import os

os.environ["MODO_SIMULACION"] = "1"

from mesa import agentes, pipeline


def test_indicadores():
    datos = agentes.calcular_indicadores({"precio": "250", "max_52s": "300", "min_52s": "200", "beta": "0.7"})
    assert datos["posicion_rango_52s_pct"] == 50.0
    assert datos["semaforo_beta"].startswith("🟢")


def test_pipeline_simulado():
    resultado = pipeline.pipeline("AAPL", avisar=lambda _: None, guardar=False)
    assert resultado["entrega_1_ficha"]["ticker"] == "AAPL"
    assert agentes.DESCARGO in resultado["entrega_3_nota"]
