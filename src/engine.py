
import os
from pathlib import Path
from datetime import datetime
from collections import deque

from ollama import Client
from dotenv import load_dotenv

from src import telemetria, alertas

load_dotenv()

# ──────────────────────────────────────────────────────────────────────────────
# Identificação da trilha
# ──────────────────────────────────────────────────────────────────────────────
TRILHA = "agrosat"

# ──────────────────────────────────────────────────────────────────────────────
# Cliente Ollama Cloud
# ──────────────────────────────────────────────────────────────────────────────
_api_key = os.environ.get("OLLAMA_API_KEY", "")

client = Client(
    host="https://ollama.com",
    headers={"Authorization": f"Bearer {_api_key}"},
)


# ──────────────────────────────────────────────────────────────────────────────
# Função llm() — ponto único de integração com a IA
# (não altere esta função; chame-a de dentro do MissionEngine.analyze())
# ──────────────────────────────────────────────────────────────────────────────
def llm(prompt: str, system: str | None = None,
        max_tokens: int = 900, temperature: float = 0.3) -> str:

    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    try:
        resposta = client.chat(
            model="gpt-oss:120b",
            messages=messages,
            options={"num_predict": max_tokens, "temperature": temperature},
            stream=False,
        )
        return resposta["message"]["content"].strip()
    except Exception as e:
        return f"[ERRO AO CONSULTAR IA] {e}"


# ──────────────────────────────────────────────────────────────────────────────
# Carregamento do system prompt
# ──────────────────────────────────────────────────────────────────────────────
def load_system_prompt() -> str:
    """Lê o system prompt do arquivo prompts/system_prompt.md."""
    path = Path("prompts/system_prompt.md")
    if path.exists():
        return path.read_text(encoding="utf-8")
    # Fallback genérico (nunca deve ser usado se o arquivo existir)
    return (
        "Você é o sistema de análise operacional do satélite AgroSat-1. "
        "Interprete dados de telemetria agrícola e explique o impacto terrestre "
        "de cada anomalia para produtores rurais e analistas de seguro agrícola."
    )


# ──────────────────────────────────────────────────────────────────────────────
# MissionEngine — motor central
# ──────────────────────────────────────────────────────────────────────────────
class MissionEngine:

    # Quantos ciclos anteriores de telemetria manter na memória
    HISTORICO_MAX = 5

    def __init__(self) -> None:
        self.trilha        = TRILHA
        self.system_prompt = load_system_prompt()
        self._historico_telemetria: deque[dict] = deque(maxlen=self.HISTORICO_MAX)
        self._historico_chat: list[dict]        = []   # memória da conversa
        self._ultimo_resultado: alertas.ResultadoAvaliacao | None = None
        self._ultimo_dados:     dict | None     = None
        self._pronto           = bool(_api_key)        # False se sem chave

    # ── Métodos públicos ──────────────────────────────────────────────────────

    def is_ready(self) -> bool:

        return self._pronto

    def status_snapshot(self) -> str:

        dados     = telemetria.coletar()
        resultado = alertas.avaliar(dados)
        self._atualizar_estado(dados, resultado)

        painel   = telemetria.formatar_painel(dados)
        alertas_ = alertas.formatar_alertas_terminal(resultado)
        return f"{painel}\n\n{alertas_}"

    def analyze(self, pergunta_usuario: str) -> str:

        if not self._pronto:
            return self._msg_sem_chave()

        # Comandos especiais de simulação (úteis para o vídeo de demonstração)
        anomalia = self._extrair_comando_anomalia(pergunta_usuario)
        dados     = telemetria.coletar(forcar_anomalia=anomalia)
        resultado = alertas.avaliar(dados)
        self._atualizar_estado(dados, resultado)

        prompt = self._montar_prompt(pergunta_usuario, dados, resultado)
        resposta = llm(prompt, system=self.system_prompt)

        # Armazena no histórico de chat (para memória de contexto)
        self._historico_chat.append({
            "ciclo":    dados["ciclo_orbital"],
            "status":  resultado.status_geral,
            "pergunta": pergunta_usuario,
            "resposta": resposta[:300],   # resumo para não explodir o contexto
        })
        if len(self._historico_chat) > 10:
            self._historico_chat.pop(0)

        return resposta

    def forcar_cenario(self, tipo_anomalia: str) -> str:

        if not self._pronto:
            return self._msg_sem_chave()
        dados     = telemetria.coletar(forcar_anomalia=tipo_anomalia)
        resultado = alertas.avaliar(dados)
        self._atualizar_estado(dados, resultado)
        prompt = self._montar_prompt(
            f"Analise em detalhes a anomalia crítica em '{tipo_anomalia}' "
            f"e explique o impacto imediato para os usuários terrestres do AgroSat.",
            dados, resultado,
        )
        return llm(prompt, system=self.system_prompt)

    # ── Métodos privados ──────────────────────────────────────────────────────

    def _atualizar_estado(self, dados: dict,
                          resultado: alertas.ResultadoAvaliacao) -> None:
        self._ultimo_dados     = dados
        self._ultimo_resultado = resultado
        self._historico_telemetria.append({
            "ciclo":     dados["ciclo_orbital"],
            "timestamp": dados["timestamp"],
            "status":    resultado.status_geral,
            "alertas":   len(resultado.alertas),
            # snapshot mínimo dos valores
            "ndvi":      dados.get("ndvi_sensor_saude"),
            "temp":      dados.get("temperatura_payload"),
            "storage":   dados.get("armazenamento"),
            "downlink":  dados.get("janela_downlink"),
            "atitude":   dados.get("estabilidade_atitude"),
        })

    def _montar_prompt(self, pergunta: str, dados: dict,
                       resultado: alertas.ResultadoAvaliacao) -> str:

        secoes = [resultado.resumo]

        # Memória: histórico de telemetria dos últimos ciclos
        if len(self._historico_telemetria) > 1:
            secoes.append("\nHISTORICO DE CICLOS ANTERIORES (ultimos ate 5):")
            for h in list(self._historico_telemetria)[:-1]:  # exclui o atual
                secoes.append(
                    f"  Ciclo #{h['ciclo']} ({h['timestamp']}) | "
                    f"STATUS: {h['status']} | "
                    f"Alertas: {h['alertas']} | "
                    f"NDVI: {h['ndvi']}% | Temp: {h['temp']}grC | "
                    f"Storage: {h['storage']}% | Downlink: {h['downlink']}min | "
                    f"Atitude: {h['atitude']} arcseg"
                )

        # Memória: histórico de chat recente
        if self._historico_chat:
            secoes.append("\nHISTORICO RECENTE DA CONVERSA:")
            for h in self._historico_chat[-3:]:  # só os 3 últimos
                secoes.append(f"  [Ciclo #{h['ciclo']}] Operador: {h['pergunta'][:120]}")
                secoes.append(f"  [Ciclo #{h['ciclo']}] Sistema: {h['resposta'][:200]}...")

        secoes.append(f"\nPERGUNTA DO OPERADOR: {pergunta}")

        return "\n".join(secoes)

    @staticmethod
    def _extrair_comando_anomalia(texto: str) -> str | None:

        texto_lower = texto.lower()
        mapa = {
            "/anomalia ndvi":     "ndvi_sensor_saude",
            "/anomalia temp":     "temperatura_payload",
            "/anomalia storage":  "armazenamento",
            "/anomalia downlink": "janela_downlink",
            "/anomalia atitude":  "estabilidade_atitude",
            "/anomalia todos":    "todos",
            "/crise":             "todos",
        }
        for cmd, tipo in mapa.items():
            if cmd in texto_lower:
                return tipo
        return None

    @staticmethod
    def _msg_sem_chave() -> str:
        return (
            "[CONFIGURACAO PENDENTE]\n\n"
            "A chave OLLAMA_API_KEY nao foi encontrada no arquivo .env.\n\n"
            "Para configurar:\n"
            "  1. Crie uma conta gratuita em https://ollama.com\n"
            "  2. Gere uma API Key no painel\n"
            "  3. Copie .env.example para .env\n"
            "  4. Cole sua chave em OLLAMA_API_KEY=sua_chave_aqui\n"
            "  5. Reinicie o sistema: python main.py"
        )
