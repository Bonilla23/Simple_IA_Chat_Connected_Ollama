"""Cliente mínimo para comunicarse con Ollama.

Diseño:
- Usa la librería `ollama` si está disponible.
- Si falla, usa la CLI `ollama run` mediante subprocess.

Compatible con las versiones actuales de la API de Ollama.
"""
from __future__ import annotations

import subprocess
from typing import List, Dict, Optional


class ChatError(Exception):
    """Error lanzado cuando la petición al modelo falla."""


class OllamaClient:
    """Cliente para comunicarse con Ollama (biblioteca o CLI).

    Métodos:
    - chat(model, messages) -> str: recibe `messages` como lista de dicts
      con keys `role` y `content`, y devuelve el texto de respuesta.
    """

    def __init__(self) -> None:
        """Inicializa el cliente intentando importar la librería `ollama`."""
        try:
            import ollama  # type: ignore
            self._lib = ollama
            self._use_lib = True
        except Exception:
            self._lib = None
            self._use_lib = False

    def chat(self, model: str, messages: List[Dict[str, str]], timeout: Optional[int] = 60) -> str:
        """Enviar una conversación al modelo y devolver el texto de respuesta.

        `messages` debe ser una lista de diccionarios: {"role": "user|assistant", "content": "..."}
        Lanza ChatError en caso de fallo.
        """
        # Construimos el prompt concatenando el historial en formato simple
        prompt_lines = []
        for m in messages:
            role = m.get("role", "user")
            content = m.get("content", "")
            prompt_lines.append(f"[{role}] {content}")
        prompt = "\n".join(prompt_lines)

        # --- Intentar con la librería `ollama` si está disponible ---
        if self._use_lib and self._lib is not None:
            try:
                # Usamos la API moderna de chat
                if hasattr(self._lib, "chat"):
                    response = self._lib.chat(model=model, messages=messages)
                    # ChatResponse (objeto) → extraemos el contenido de texto
                    if hasattr(response, "message") and hasattr(response.message, "content"):
                        return response.message.content.strip()
                    elif isinstance(response, dict):
                        return response.get("message", {}).get("content", "").strip()
                    elif isinstance(response, str):
                        return response.strip()
                    else:
                        return str(response)
                # API alternativa generate()
                elif hasattr(self._lib, "generate"):
                    result = self._lib.generate(model=model, prompt=prompt)
                    if isinstance(result, dict):
                        return result.get("response", "").strip()
                    return str(result).strip()
            except Exception as e:
                raise ChatError(f"Error al usar la librería Ollama: {e}") from e

        # --- Fallback: usar CLI de Ollama mediante subprocess ---
        try:
            cmd = ["ollama", "run", model]
            result = subprocess.run(
                cmd,
                input=prompt.encode("utf-8"),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=timeout,
            )
            if result.returncode != 0:
                raise ChatError(
                    f"CLI ollama devolvió código {result.returncode}: {result.stderr.decode('utf-8')}"
                )
            return result.stdout.decode("utf-8").strip()
        except Exception as e:
            raise ChatError(f"Fallo al ejecutar CLI de Ollama: {e}") from e
