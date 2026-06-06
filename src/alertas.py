"""
src/alertas.py — Thresholds e lógica de decisão do AgroSat (Trilha 1).

IMPORTANTE: A decisão de alertar é feita em Python — não na IA.
A IA interpreta e contextualiza; o if/else decide.

Níveis: NORMAL | ATENCAO | CRITICO | EMERGENCIA
"""

from dataclasses import dataclass, field
from typing import Any


ATENCAO: dict[str, dict[str, float]] = {
    "ndvi_sensor_saude":    {"min": 75.0,  "max": 100.0},
    "temperatura_payload":  {"min": 2.0,   "max": 48.0},
    "armazenamento":        {"min": 0.0,   "max": 75.0},
    "janela_downlink":      {"min": 8.0,   "max": 120.0},
    "estabilidade_atitude": {"min": 0.0,   "max": 6.0},
}

CRITICO: dict[str, dict[str, float]] = {
    "ndvi_sensor_saude":    {"min": 50.0,  "max": 100.0},
    "temperatura_payload":  {"min": -5.0,  "max": 55.0},
    "armazenamento":        {"min": 0.0,   "max": 85.0},
    "janela_downlink":      {"min": 5.0,   "max": 120.0},
    "estabilidade_atitude": {"min": 0.0,   "max": 9.0},
}

EMERGENCIA: dict[str, dict[str, float]] = {
    "ndvi_sensor_saude":    {"min": 25.0,  "max": 100.0},
    "temperatura_payload":  {"min": -15.0, "max": 65.0},
    "armazenamento":        {"min": 0.0,   "max": 95.0},
    "janela_downlink":      {"min": 2.0,   "max": 120.0},
    "estabilidade_atitude": {"min": 0.0,   "max": 14.0},
}

ACOES_AUTOMATIZADAS: dict[str, str] = {
    "ndvi_sensor_saude": (
        "SENSOR NDVI: modo de autocalibração ativado. "
        "Imagens desta passagem marcadas como baixa confiabilidade. "
        "Analistas de seguro agricola notificados para nao usar este lote."
    ),
    "temperatura_payload": (
        "PAYLOAD TERMICO: obstrucao do radiador verificada remotamente. "
        "Modo de operacao reduzido ativado — desligando canais espectrais nao essenciais."
    ),
    "armazenamento": (
        "ARMAZENAMENTO CRITICO: downlink prioritario agendado para a proxima janela. "
        "Imagens de menor prioridade marcadas para descarte se necessario."
    ),
    "janela_downlink": (
        "DOWNLINK IMINENTE: fila de transmissao otimizada para priorizar imagens NDVI "
        "das regioes de maior interesse agricola. Estacao terrestre notificada."
    ),
    "estabilidade_atitude": (
        "ATITUDE INSTAVEL: reaction wheels reconfigurados. "
        "Imageamento suspenso ate estabilizacao. Produtos geoespaciais desta orbita invalidados."
    ),
}

IMPACTO_TERRESTRE: dict[str, str] = {
    "ndvi_sensor_saude": (
        "Produtores rurais recebem mapas de vegetacao imprecisos, "
        "comprometendo decisoes de irrigacao e aplicacao de defensivos. "
        "Seguradoras nao conseguem calcular indices de produtividade para indenizacoes."
    ),
    "temperatura_payload": (
        "Superaquecimento do payload optico distorce a calibracao espectral — "
        "valores NDVI ficam sistematicamente errados, levando o produtor a "
        "aplicar insumos em excesso ou em falta."
    ),
    "armazenamento": (
        "Imagens de passagens sobre lavouras nao sao armazenadas a tempo — "
        "janelas de imageamento criticas (plantio, floracao) sao perdidas "
        "permanentemente, prejudicando o planejamento da safra."
    ),
    "janela_downlink": (
        "Atraso na entrega das imagens NDVI ao produtor. "
        "Decisoes de manejo ficam desatualizadas; em caso de praga ou seca, "
        "o produtor age tarde, com perdas economicas diretas na safra."
    ),
    "estabilidade_atitude": (
        "Imagens borradas invalidam o calculo do NDVI. "
        "Seguradoras agricolas nao conseguem validar sinistros por indice de vegetacao, "
        "atrasando indenizacoes a produtores afetados por eventos climaticos."
    ),
}


@dataclass
class Alerta:
    parametro: str
    valor: float
    severidade: str
    mensagem: str
    acao_automatizada: str = ""
    impacto_terrestre: str = ""


@dataclass
class ResultadoAvaliacao:
    status_geral: str
    alertas: list = field(default_factory=list)
    acoes_executadas: list = field(default_factory=list)
    resumo: str = ""


def _checar_parametro(nome: str, valor: float):
    for nivel, tabela in [("EMERGENCIA", EMERGENCIA), ("CRITICO", CRITICO), ("ATENCAO", ATENCAO)]:
        lim = tabela[nome]
        if valor < lim["min"] or valor > lim["max"]:
            acao = ACOES_AUTOMATIZADAS.get(nome, "") if nivel in ("CRITICO", "EMERGENCIA") else ""
            return Alerta(
                parametro=nome,
                valor=valor,
                severidade=nivel,
                mensagem=_msg(nome, valor, nivel),
                acao_automatizada=acao,
                impacto_terrestre=IMPACTO_TERRESTRE.get(nome, ""),
            )
    return None


def _msg(param, valor, sev):
    tabela = {
        "ndvi_sensor_saude": {
            "ATENCAO":    f"Saude do sensor NDVI em {valor:.1f}% — degradacao incipiente.",
            "CRITICO":    f"Sensor NDVI com {valor:.1f}% de integridade — calibracao comprometida.",
            "EMERGENCIA": f"FALHA CRITICA DO SENSOR NDVI: {valor:.1f}% — imageamento multiespectral invalido.",
        },
        "temperatura_payload": {
            "ATENCAO":    f"Temperatura do payload em {valor:.1f} grC — fora da faixa ideal.",
            "CRITICO":    f"Payload em {valor:.1f} grC — risco de distorcao espectral.",
            "EMERGENCIA": f"SOBREAQUECIMENTO DO PAYLOAD: {valor:.1f} grC — dano permanente iminente.",
        },
        "armazenamento": {
            "ATENCAO":    f"Armazenamento em {valor:.1f}% — aproximando do limite.",
            "CRITICO":    f"Armazenamento critico: {valor:.1f}% — downlink urgente necessario.",
            "EMERGENCIA": f"ARMAZENAMENTO ESGOTADO: {valor:.1f}% — imagens sendo descartadas.",
        },
        "janela_downlink": {
            "ATENCAO":    f"Proxima janela de downlink em {valor:.1f} min — preparar fila.",
            "CRITICO":    f"Downlink em {valor:.1f} min — priorizacao urgente de imagens.",
            "EMERGENCIA": f"DOWNLINK IMINENTE: {valor:.1f} min — risco de perda de imagens NDVI.",
        },
        "estabilidade_atitude": {
            "ATENCAO":    f"Erro de apontamento: {valor:.1f} arcseg — qualidade de imagem reduzida.",
            "CRITICO":    f"Instabilidade de atitude: {valor:.1f} arcseg — imagens borradas.",
            "EMERGENCIA": f"PERDA DE CONTROLE DE ATITUDE: {valor:.1f} arcseg — imageamento suspenso.",
        },
    }
    return tabela.get(param, {}).get(sev, f"{param}: {valor} ({sev})")


def avaliar(dados: dict) -> ResultadoAvaliacao:
    """Avalia telemetria completa e retorna status, alertas e resumo."""
    params = [
        "ndvi_sensor_saude",
        "temperatura_payload",
        "armazenamento",
        "janela_downlink",
        "estabilidade_atitude",
    ]

    alertas = []
    for p in params:
        if p not in dados:
            continue
        a = _checar_parametro(p, float(dados[p]))
        if a:
            alertas.append(a)

    sevs = [a.severidade for a in alertas]
    if "EMERGENCIA" in sevs:
        status = "EMERGENCIA"
    elif "CRITICO" in sevs:
        status = "CRITICO"
    elif "ATENCAO" in sevs:
        status = "ATENCAO"
    else:
        status = "NORMAL"

    acoes = [a.acao_automatizada for a in alertas
             if a.severidade in ("CRITICO", "EMERGENCIA") and a.acao_automatizada]

    resumo = _montar_resumo(status, alertas, acoes, dados)
    return ResultadoAvaliacao(status_geral=status, alertas=alertas,
                              acoes_executadas=acoes, resumo=resumo)


def _montar_resumo(status, alertas, acoes, dados):
    linhas = [
        f"STATUS GERAL DA MISSAO AGROSAT: {status}",
        f"Ciclo orbital: #{dados.get('ciclo_orbital','?')} — {dados.get('timestamp','')}",
        f"Area imageada: {dados.get('area_imageada','N/A')}",
        f"Cobertura de nuvens: {dados.get('cobertura_nuvens','?')} %",
        "",
        "TELEMETRIA ATUAL:",
        f"  NDVI Sensor (saude)   : {dados.get('ndvi_sensor_saude','N/A')} %",
        f"  Temperatura Payload   : {dados.get('temperatura_payload','N/A')} grC",
        f"  Armazenamento         : {dados.get('armazenamento','N/A')} %",
        f"  Janela Downlink       : {dados.get('janela_downlink','N/A')} min",
        f"  Estabilidade Atitude  : {dados.get('estabilidade_atitude','N/A')} arcseg",
        "",
    ]
    if alertas:
        linhas.append(f"ALERTAS ATIVOS ({len(alertas)}):")
        for a in alertas:
            linhas.append(f"  [{a.severidade}] {a.mensagem}")
            if a.impacto_terrestre:
                linhas.append(f"    IMPACTO NA TERRA: {a.impacto_terrestre}")
    else:
        linhas.append("ALERTAS: Nenhum — todos os sistemas operando normalmente.")
    if acoes:
        linhas.append("")
        linhas.append("ACOES AUTOMATIZADAS EXECUTADAS:")
        for ac in acoes:
            linhas.append(f"  > {ac}")
    return "\n".join(linhas)


def formatar_alertas_terminal(resultado: ResultadoAvaliacao) -> str:
    mapa = {
        "NORMAL":    "bold green",
        "ATENCAO":   "bold yellow",
        "CRITICO":   "bold red",
        "EMERGENCIA":"bold white on red",
    }
    cor = mapa.get(resultado.status_geral, "white")
    linhas = [f"[{cor}] STATUS: {resultado.status_geral} [/{cor}]"]
    for a in resultado.alertas:
        c = mapa.get(a.severidade, "white")
        linhas.append(f"  [{c}][{a.severidade}][/{c}] {a.mensagem}")
    if resultado.acoes_executadas:
        linhas.append("\n[bold #06B6D4]ACOES AUTOMATIZADAS:[/bold #06B6D4]")
        for ac in resultado.acoes_executadas:
            linhas.append(f"  [#06B6D4]> {ac}[/#06B6D4]")
    return "\n".join(linhas)
