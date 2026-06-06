"""
src/telemetria.py — Geração de dados simulados de telemetria para AgroSat.

Trilha 1 — Sensoriamento Agrícola
Satélite simulado: satélite de sensoriamento multiespectral em órbita baixa (LEO),
similar ao CBERS-4A ou Planet Labs.

Parâmetros monitorados:
  - ndvi_sensor_saude   : saúde do sensor NDVI multiespectral (0-100 %)
  - temperatura_payload : temperatura do payload óptico (°C)
  - armazenamento       : capacidade de armazenamento utilizada (%)
  - janela_downlink     : tempo restante até próxima janela de downlink (min)
  - estabilidade_atitude: erro de apontamento do satélite (arcseg)

Personas atendidas:
  - Engenheiro de operações do satélite
  - Produtor rural consumidor do dado NDVI
  - Analista de seguro agrícola baseado em índice
"""

import random
from datetime import datetime
from typing import Any


# Ranges de operação normal
RANGES_NORMAIS: dict[str, tuple[float, float]] = {
    "ndvi_sensor_saude":    (80.0, 100.0),
    "temperatura_payload":  (5.0,  45.0),
    "armazenamento":        (0.0,  70.0),
    "janela_downlink":      (10.0, 120.0),
    "estabilidade_atitude": (0.0,  5.0),
}

_estado: dict[str, float] = {}
_ciclo: int = 0


def _inicializar() -> None:
    global _estado
    _estado = {
        "ndvi_sensor_saude":    random.uniform(88.0, 100.0),
        "temperatura_payload":  random.uniform(12.0, 35.0),
        "armazenamento":        random.uniform(15.0, 55.0),
        "janela_downlink":      random.uniform(20.0, 90.0),
        "estabilidade_atitude": random.uniform(0.5, 3.5),
    }


def _drift(valor: float, amplitude: float, minimo: float, maximo: float) -> float:
    novo = valor + random.uniform(-amplitude, amplitude)
    return round(max(minimo, min(maximo, novo)), 2)


def coletar(forcar_anomalia: str | None = None) -> dict[str, Any]:
    """
    Coleta (simula) a leitura atual dos sensores do AgroSat.

    forcar_anomalia: 'ndvi_sensor_saude' | 'temperatura_payload' |
                     'armazenamento' | 'janela_downlink' |
                     'estabilidade_atitude' | 'todos'
    """
    global _estado, _ciclo

    if not _estado:
        _inicializar()

    _ciclo += 1

    _estado["ndvi_sensor_saude"]    = _drift(_estado["ndvi_sensor_saude"],    1.5,  0.0,  100.0)
    _estado["temperatura_payload"]  = _drift(_estado["temperatura_payload"],  3.0, -20.0,  80.0)
    _estado["armazenamento"]        = _drift(_estado["armazenamento"],         3.5,  0.0,  100.0)
    _estado["janela_downlink"]      = _drift(_estado["janela_downlink"],       5.0,  0.0,  120.0)
    _estado["estabilidade_atitude"] = _drift(_estado["estabilidade_atitude"], 0.5,  0.0,   20.0)

    if forcar_anomalia:
        _aplicar_anomalia(forcar_anomalia)

    dados = dict(_estado)
    dados["timestamp"]        = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    dados["ciclo_orbital"]    = _ciclo
    dados["satelite"]         = "AgroSat-1 (CBERS-4A sim.)"
    dados["orbita"]           = "LEO 614 km — incl. 97.8 deg — SSO"
    dados["area_imageada"]    = _gerar_area_imageada()
    dados["cobertura_nuvens"] = round(random.uniform(0.0, 40.0), 1)

    return dados


def _gerar_area_imageada() -> str:
    regioes = [
        "Chapada dos Parecis (MT) — soja",
        "Triangulo Mineiro (MG) — cafe e milho",
        "Oeste da Bahia (BA) — soja e algodao",
        "Sul do Maranhao (MA) — soja (MATOPIBA)",
        "Sudoeste do Parana (PR) — trigo e soja",
        "Planalto Gaucho (RS) — soja e arroz",
        "Cerrado Goiano (GO) — cana e soja",
        "Vale do Sao Francisco (PE/BA) — fruticultura irrigada",
    ]
    return random.choice(regioes)


def _aplicar_anomalia(tipo: str) -> None:
    global _estado
    if tipo in ("ndvi_sensor_saude", "todos"):
        _estado["ndvi_sensor_saude"]    = round(random.uniform(0.0, 35.0), 2)
    if tipo in ("temperatura_payload", "todos"):
        _estado["temperatura_payload"]  = round(random.uniform(58.0, 75.0), 2)
    if tipo in ("armazenamento", "todos"):
        _estado["armazenamento"]        = round(random.uniform(88.0, 100.0), 2)
    if tipo in ("janela_downlink", "todos"):
        _estado["janela_downlink"]      = round(random.uniform(0.0, 4.0), 2)
    if tipo in ("estabilidade_atitude", "todos"):
        _estado["estabilidade_atitude"] = round(random.uniform(12.0, 20.0), 2)


def resetar() -> None:
    global _estado, _ciclo
    _estado = {}
    _ciclo  = 0
    _inicializar()


def formatar_painel(dados: dict[str, Any]) -> str:
    linhas = [
        f"Satelite     : {dados.get('satelite', 'N/A')}",
        f"Orbita       : {dados.get('orbita', 'N/A')}",
        f"Area imageada: {dados.get('area_imageada', 'N/A')}",
        f"Nuvens       : {dados.get('cobertura_nuvens', '?')} %",
        f"Ciclo        : #{dados.get('ciclo_orbital', '?')} -- {dados.get('timestamp', '')}",
        "-" * 56,
        f"NDVI Sensor (saude)  : {dados['ndvi_sensor_saude']:>7.1f} %",
        f"Temp. Payload         : {dados['temperatura_payload']:>7.1f} grC",
        f"Armazenamento         : {dados['armazenamento']:>7.1f} %",
        f"Janela Downlink       : {dados['janela_downlink']:>7.1f} min",
        f"Estabilidade Atitude  : {dados['estabilidade_atitude']:>7.1f} arcseg",
    ]
    return "\n".join(linhas)
