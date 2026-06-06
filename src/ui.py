"""
src/ui.py — Interface CLI estilo Claude Code para o Mission Control AI — AgroSat.

Usa Rich (painéis, cores, tabelas) + prompt-toolkit (input editável com histórico).
Comandos suportados:
  /help            → tabela de comandos
  /status          → snapshot da telemetria atual
  /about           → informações do projeto
  /clear           → limpa a tela e exibe o banner
  /exit            → encerra o sistema
  /anomalia ndvi   → força anomalia no sensor NDVI (para demonstração)
  /anomalia temp   → força anomalia na temperatura do payload
  /anomalia storage→ força anomalia no armazenamento
  /anomalia downlink → força anomalia na janela de downlink
  /anomalia atitude → força anomalia na estabilidade de atitude
  /anomalia todos  → força emergência em todos os parâmetros
  /crise           → atalho para /anomalia todos
  /resetar         → reinicia a telemetria para valores normais
"""

import pyfiglet
from datetime import datetime

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.rule import Rule
from rich.align import Align
from rich.live import Live
from rich.spinner import Spinner

from prompt_toolkit import PromptSession
from prompt_toolkit.styles import Style
from prompt_toolkit.history import InMemoryHistory

from src import telemetria as tel

console = Console()

# Estilo do prompt ❯
_prompt_style = Style.from_dict({"prompt": "#06B6D4 bold"})
_session = PromptSession(
    history=InMemoryHistory(),
    style=_prompt_style,
)


# ──────────────────────────────────────────────────────────────────────────────
# Banner
# ──────────────────────────────────────────────────────────────────────────────

def show_banner() -> None:
    """Exibe o banner ASCII + card de boas-vindas."""
    try:
        linha1 = pyfiglet.figlet_format("Global Solution", font="ansi_shadow")
        linha2 = pyfiglet.figlet_format("Mission Control", font="ansi_shadow")
    except Exception:
        linha1 = "Global Solution\n"
        linha2 = "Mission Control AI\n"

    console.print()
    console.print(Align.center(Text(linha1, style="bold #A855F7")))
    console.print(Align.center(Text(linha2, style="bold #06B6D4")))
    console.print(
        Align.center(
            Text("── 2026.1  ·  AgroSat  ·  Prompt Engineering & AI  ·  FIAP ──",
                 style="italic #8484A0")
        )
    )
    console.print()

    card = Table.grid(padding=(0, 1))
    card.add_column(style="#8484A0")
    card.add_row("🌾  Trilha    :", "[bold #06B6D4]AgroSat — Sensoriamento Agrícola[/bold #06B6D4]")
    card.add_row("🛰  Satélite  :", "AgroSat-1 (CBERS-4A sim.) — LEO 614 km")
    card.add_row("🤖  Modelo    :", "gpt-oss:120b via Ollama Cloud")
    card.add_row("💬  Ajuda     :", "digite /help para ver todos os comandos")

    console.print(
        Panel(card, title="◆ MISSION CONTROL AI", border_style="#06B6D4",
              padding=(1, 3))
    )
    console.print()


# ──────────────────────────────────────────────────────────────────────────────
# Exibição de respostas
# ──────────────────────────────────────────────────────────────────────────────

def show_response(text: str, titulo: str = "◆ Mission Control AI") -> None:
    """Renderiza a resposta da IA em painel com timestamp."""
    agora = datetime.now().strftime("%H:%M:%S")
    console.print(
        Panel(
            Text(text),
            title=titulo,
            subtitle=f"[#8484A0]{agora}[/#8484A0]",
            border_style="#06B6D4",
            padding=(1, 2),
        )
    )


def show_telemetria(texto: str) -> None:
    """Exibe painel de telemetria com borda verde."""
    console.print(
        Panel(
            texto,
            title="◆ TELEMETRIA — AgroSat-1",
            border_style="bold green",
            padding=(1, 2),
        )
    )


def show_thinking() -> "Live":
    """Retorna um contexto Live com spinner para usar enquanto a IA processa."""
    spinner = Spinner("dots", text=Text(" Consultando IA...", style="#8484A0"))
    return Live(spinner, console=console, refresh_per_second=12)


def show_error(msg: str) -> None:
    console.print(f"[bold red]⚠ {msg}[/bold red]")


def show_warning(msg: str) -> None:
    console.print(f"[bold yellow]⚠ {msg}[/bold yellow]")


def show_info(msg: str) -> None:
    console.print(f"[#8484A0]{msg}[/#8484A0]")


# ──────────────────────────────────────────────────────────────────────────────
# Tabela de ajuda
# ──────────────────────────────────────────────────────────────────────────────

def show_help() -> None:
    t = Table(title="Comandos disponíveis", border_style="#06B6D4",
              show_header=True, header_style="bold #06B6D4")
    t.add_column("Comando",       style="#A855F7", min_width=22)
    t.add_column("Descrição",     style="white")

    t.add_row("/help",             "Exibe esta tabela de comandos")
    t.add_row("/status",           "Mostra telemetria atual com alertas")
    t.add_row("/about",            "Informações do projeto e da trilha")
    t.add_row("/clear",            "Limpa a tela e reexibe o banner")
    t.add_row("/exit",             "Encerra o Mission Control AI")
    t.add_row("─" * 22,           "─" * 44)
    t.add_row("/anomalia ndvi",    "Força falha no sensor NDVI (simulação)")
    t.add_row("/anomalia temp",    "Força sobreaquecimento do payload")
    t.add_row("/anomalia storage", "Força armazenamento cheio")
    t.add_row("/anomalia downlink","Força janela de downlink iminente")
    t.add_row("/anomalia atitude", "Força instabilidade de atitude")
    t.add_row("/anomalia todos",   "Força emergência em todos os parâmetros")
    t.add_row("/crise",            "Atalho para /anomalia todos")
    t.add_row("/resetar",          "Reinicia telemetria para valores normais")
    t.add_row("─" * 22,           "─" * 44)
    t.add_row("[qualquer texto]",  "Pergunta livre analisada pela IA")

    console.print(t)


# ──────────────────────────────────────────────────────────────────────────────
# About
# ──────────────────────────────────────────────────────────────────────────────

def show_about() -> None:
    texto = (
        "[bold #A855F7]Trilha 1 — AgroSat · Sensoriamento Agrícola[/bold #A855F7]\n\n"
        "Simula a operação de um satélite de sensoriamento multiespectral (CBERS-4A / Planet Labs)\n"
        "monitorando lavouras brasileiras em tempo real via IA generativa.\n\n"
        "[bold #06B6D4]Parâmetros monitorados:[/bold #06B6D4]\n"
        "  🌿 Saúde do sensor NDVI      • 🌡 Temperatura do payload óptico\n"
        "  💾 Capacidade de armazenamento • 📡 Janela de downlink\n"
        "  🎯 Estabilidade de atitude\n\n"
        "[bold #06B6D4]Personas atendidas:[/bold #06B6D4]\n"
        "  👷 Engenheiro de operações do satélite\n"
        "  🌾 Produtor rural consumidor do dado NDVI\n"
        "  📋 Analista de seguro agrícola baseado em índice\n\n"
        "[bold #06B6D4]Stack:[/bold #06B6D4] Python 3.10+ · Ollama Cloud (gpt-oss:120b) · "
        "Rich · prompt-toolkit · pyfiglet\n\n"
        "[#8484A0]FIAP · Ciência da Computação · Global Solution 2026.1[/#8484A0]"
    )
    console.print(Panel(texto, title="◆ Sobre o projeto", border_style="#A855F7", padding=(1, 2)))


# ──────────────────────────────────────────────────────────────────────────────
# Loop principal da CLI
# ──────────────────────────────────────────────────────────────────────────────

def run_cli(engine) -> None:
    """Loop principal da CLI. Recebe o MissionEngine e gerencia toda a interação."""
    show_banner()

    # Aviso se a engine não está pronta (sem chave)
    if not engine.is_ready():
        console.print(
            Panel(
                "[bold yellow]⚠ Engine status: AGUARDANDO CONFIGURAÇÃO[/bold yellow]\n\n"
                "Crie o arquivo [bold].env[/bold] com sua OLLAMA_API_KEY.\n"
                "Veja [bold].env.example[/bold] para referência.\n"
                "Digite /help para ver os comandos disponíveis.",
                border_style="yellow", padding=(1, 2),
            )
        )

    while True:
        try:
            user_input = _session.prompt("❯ ").strip()
        except (KeyboardInterrupt, EOFError):
            show_info("\nEncerrando Mission Control AI. Até a próxima missão. 🛰")
            break

        if not user_input:
            continue

        cmd = user_input.lower()

        # ── Comandos de sistema ───────────────────────────────────────────────
        if cmd == "/exit":
            show_info("Encerrando Mission Control AI. Até a próxima missão. 🛰")
            break

        if cmd == "/help":
            show_help()
            continue

        if cmd == "/about":
            show_about()
            continue

        if cmd == "/clear":
            console.clear()
            show_banner()
            continue

        if cmd == "/status":
            show_info("Coletando telemetria...")
            snapshot = engine.status_snapshot()
            show_telemetria(snapshot)
            continue

        if cmd == "/resetar":
            tel.resetar()
            show_info("✓ Telemetria reiniciada para valores normais.")
            continue

        # ── Perguntas e comandos de anomalia (vão para o engine) ─────────────
        with show_thinking():
            resposta = engine.analyze(user_input)

        show_response(resposta)
