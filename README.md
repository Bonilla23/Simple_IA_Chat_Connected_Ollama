# Ollama Terminal Chat

Aplicación en terminal desarrollada en Python para interactuar con modelos locales de Ollama mediante una interfaz sencilla y legible en consola.  
El proyecto utiliza `uv` como gestor de paquetes y ejecución, junto con las librerías `ollama` y `rich`.

---

## Características

- Interfaz de chat en consola.
- Compatible con cualquier modelo disponible en Ollama (por ejemplo, `llama3`, `gemma3`, `mistral`).
- Renderizado de texto con formato Markdown (negritas, listas, bloques de código).
- Indicador de carga con tiempo transcurrido mientras se espera la respuesta del modelo.
- Manejo de errores con limpieza del historial en caso de fallo.
- Estructura modular separada por responsabilidades (CLI, UI y cliente Ollama).

---

## Requisitos

- Python 3.10 o superior.
- Tener instalado Ollama (CLI o librería).
  - Puede descargarse desde: [https://ollama.com/download](https://ollama.com/download)

---

## Instalación con uv

Si no se dispone de `uv`, puede instalarse con:

```bash
pip install uv
```

## Para ejecutar la aplicación:

```bash
uv run python main.py --model gemma3
```
