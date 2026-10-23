"""Pruebas de la Mesa Financiera sin usar llaves ni servicios externos."""
import json
import os

import pytest

os.environ["MODO_SIMULACION"] = "1"

from mesa import agentes, config, pipeline as pl


@pytest.fixture(autouse=True)
def simulacion(monkeypatch, tmp_path):
    monkeypatch.setattr(config, "MODO_SIMULACION", True)
        monkeypatch.setattr(config, "CARPETA_SALIDAS", str(tmp_path))
        
        
        @pytest.mark.parametrize("beta,color", [(0.5, "🟢"), (0.8, "🟡"), (1.2, "🟡"), (1.3, "🔴"), (None, "⚪")])
        def test_semaforo_beta(beta, color):
            assert agentes.calcular_indicadores({"beta": beta})["semaforo_beta"].startswith(color)
            
            
            def test_formula_posicion_rango_52_semanas():
                ind = agentes.calcular_indicadores({"precio": "250.5", "max_52s": "300", "min_52s": "200", "beta": "0.7"})
                    assert ind["posicion_rango_52s_pct"] == 50.5
                    
                    
                    @pytest.mark.parametrize("entrada,esperado", [(" aapl ", "AAPL"), ("brk.b", "BRK.B")])
                    def test_ticker_valido(entrada, esperado):
                        assert pl.normalizar_ticker(entrada) == esperado
                        
                        
                        @pytest.mark.parametrize("entrada", ["", "AAPL; rm -rf", "ACCIONMUYLARGAXYZ"])
                        def test_ticker_invalido(entrada):
                            with pytest.raises(ValueError):
                                    pl.normalizar_ticker(entrada)
                                    
                                    
                                    def test_extraer_json():
                                        assert agentes.extraer_json('antes {"a": 1} después')["a"] == 1
                                        
                                        
                                        def test_alpha_vantage_caido_usa_demo(monkeypatch):
                                            monkeypatch.setattr(config, "MODO_SIMULACION", False)
                                                monkeypatch.setattr(agentes.requests, "get", lambda *args, **kwargs: (_ for _ in ()).throw(ConnectionError()))
                                                    ficha, consultas = agentes.agente_recolector("AAPL")
                                                        assert "DEMO" in ficha["fuente"] and consultas == []
                                                        
                                                        
                                                        def test_cadena_completa_guarda_evidencia():
                                                            avisos = []
                                                                resultado = pl.pipeline("MSFT", avisar=avisos.append)
                                                                    assert resultado["entrega_2_analisis"]["ficha"] == resultado["entrega_1_ficha"]
                                                                        assert agentes.DESCARGO in resultado["entrega_3_nota"]
                                                                            with open(resultado["archivo"], encoding="utf-8") as archivo:
                                                                                    assert json.load(archivo)["ticker"] == "MSFT"
                                                                                        assert any("Entrega 1→2" in aviso for aviso in avisos)
                                                                                        """