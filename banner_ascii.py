"""
banner_ascii.py — Gerador de banner ASCII para Mission Control AI / AgroSat.

Uso:
    python banner_ascii.py               # Banner padrão
    python banner_ascii.py -fonts        # Lista as 570+ fontes disponíveis
    python banner_ascii.py -font slant -text "AgroSat"
    python banner_ascii.py -demo         # Demonstra 8 fontes diferentes
"""

import sys
import pyfiglet
from rich.console import Console
from rich.align import Align
from rich.text import Text
from rich.panel import Panel

console = Console()


def show_banner(font: str = "ansi_shadow") -> None:
    """Exibe o banner principal em ASCII art."""
    try:
        linha1 = pyfiglet.figlet_format("Global Solution", font=font)
        linha2 = pyfiglet.figlet_format("Mission Control AI", font=font)
    except Exception:
        linha1 = "Global Solution\n"
        linha2 = "Mission Control AI\n"

    console.print(Align.center(Text(linha1, style="bold #A855F7")))
    console.print(Align.center(Text(linha2, style="bold #06B6D4")))
    console.print(
        Align.center(
            Text(
                "── 2026.1 · Prompt Engineering and AI · FIAP · AgroSat ──",
                style="italic #8484A0",
            )
        )
    )


def list_fonts() -> None:
    """Lista fontes disponíveis no PyFiglet."""
    fonts = pyfiglet.FigletFont.getFonts()
    console.print(
        Panel(
            f"[bold #06B6D4]{len(fonts)} fontes disponíveis no PyFiglet:[/bold #06B6D4]",
            border_style="#A855F7",
        )
    )
    for i in range(0, min(len(fonts), 160), 4):
        chunk = fonts[i:i+4]
        console.print("  ".join(f"[#8484A0]{f:<22}[/#8484A0]" for f in chunk))
    console.print(f"\n[italic #8484A0]Total: {len(fonts)} fontes.[/italic #8484A0]")


def demo_fonts() -> None:
    """Demonstra 8 fontes diferentes."""
    demo_list = ["ansi_shadow", "slant", "big", "banner3", "doom", "larry3d", "block", "digital"]
    console.print(Panel("[bold #A855F7]DEMO — 8 fontes[/bold #A855F7]", border_style="#06B6D4"))
    for font_name in demo_list:
        try:
            art = pyfiglet.figlet_format("AGRO", font=font_name)
            console.rule(f"[bold #06B6D4]{font_name}[/bold #06B6D4]")
            console.print(Text(art, style="#A855F7"))
        except Exception:
            console.print(f"[yellow]Fonte '{font_name}' indisponível.[/yellow]")


def main() -> None:
    args = sys.argv[1:]

    if not args:
        show_banner()
        return
    if "-fonts" in args:
        list_fonts()
        return
    if "-demo" in args:
        demo_fonts()
        return

    font = "ansi_shadow"
    text_override = None

    if "-font" in args:
        idx = args.index("-font")
        if idx + 1 < len(args):
            font = args[idx + 1]
    if "-text" in args:
        idx = args.index("-text")
        if idx + 1 < len(args):
            text_override = args[idx + 1]

    if text_override:
        try:
            art = pyfiglet.figlet_format(text_override, font=font)
            console.print(Align.center(Text(art, style="bold #06B6D4")))
        except Exception as e:
            console.print(f"[red]Erro ao gerar banner: {e}[/red]")
    else:
        show_banner(font=font)


if __name__ == "__main__":
    main()
