"""CLI principal del chat con soporte de historial y formateo bonito."""

from __future__ import annotations
from chat.ollama_client import OllamaClient, ChatError
from chat.ui import ConsoleUI


def run_chat():
    """Bucle principal del chat interactivo."""
    ui = ConsoleUI()
    client = OllamaClient()

    # Elegir modelo
    import sys
    if len(sys.argv) > 2 and sys.argv[1] == "--model":
        model = sys.argv[2]
    else:
        model = "gemma2"  # modelo por defecto

    ui.console.print(f"[bold green]Iniciando chat con modelo:[/bold green] {model}\n")

    # Historial de conversación
    history = []

    try:
        while True:
            # Pedir mensaje al usuario
            user_input = ui.prompt_user()

            if not user_input.strip():
                continue

            # Agregar al historial
            history.append({"role": "user", "content": user_input})

            # Mostrar spinner mientras se obtiene la respuesta
            ui.start_spinner()
            try:
                reply_text = client.chat(model=model, messages=history)
            except ChatError as e:
                ui.stop_spinner()
                ui.console.print(f"[bold red]Error en la petición al modelo:[/bold red]\n  {e}")
                continue
            finally:
                ui.stop_spinner()

            # Mostrar respuesta
            ui.show_message(reply_text)

            # Guardar respuesta en historial
            history.append({"role": "assistant", "content": reply_text})

    except (KeyboardInterrupt, EOFError):
        ui.console.print("\n[bold yellow]Chat finalizado.[/bold yellow]")
