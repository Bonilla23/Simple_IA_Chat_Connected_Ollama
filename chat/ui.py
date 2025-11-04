"""Interfaz de usuario para el chat en terminal usando Rich, con formato mejorado."""

from __future__ import annotations
import time
from rich.console import Console
from rich.markdown import Markdown
from rich.prompt import Prompt
from rich.spinner import Spinner
from rich.panel import Panel
from threading import Thread, Event


class ConsoleUI:
    """Controla la interfaz en terminal: entrada, spinner y salida Markdown."""

    def __init__(self) -> None:
        self.console = Console()
        self._stop_event = Event()

    def prompt_user(self) -> str:
        """Solicita un mensaje al usuario."""
        self.console.print("\n[bold bright_white]───────────────────────────────────────────────[/bold bright_white]")
        return Prompt.ask("[bold green]Tu mensaje[/bold green] (o Ctrl-C / Ctrl-D para salir)")

    def show_message(self, text: str) -> None:
        """Muestra la respuesta del modelo renderizando Markdown con formato elegante."""
        if not text.strip():
            self.console.print("[bold red]⚠ No se recibió texto del modelo.[/bold red]")
            return

        # Panel con borde y color
        self.console.print(
            Panel.fit(
                Markdown(text, style="white", code_theme="monokai"),
                title="[bold cyan]Asistente[/bold cyan]",
                border_style="cyan",
                padding=(1, 2),
            )
        )

    def spinner(self, message: str = "Obteniendo respuesta del modelo..."):
        """Muestra un spinner animado mientras se obtiene la respuesta."""
        spinner = Spinner("dots", text=message)
        start_time = time.time()
        with self.console.status(spinner, spinner_style="cyan") as status:
            while not self._stop_event.is_set():
                elapsed = time.time() - start_time
                status.update(f"{message} — [dim]{elapsed:.1f}s transcurridos[/dim]")
                time.sleep(0.1)

    def start_spinner(self, message: str = "Obteniendo respuesta del modelo..."):
        """Inicia el spinner en un hilo separado."""
        self._stop_event.clear()
        self._spinner_thread = Thread(target=self.spinner, args=(message,), daemon=True)
        self._spinner_thread.start()

    def stop_spinner(self):
        """Detiene el spinner y espera a que el hilo termine."""
        self._stop_event.set()
        if hasattr(self, "_spinner_thread"):
            self._spinner_thread.join(timeout=0.2)
