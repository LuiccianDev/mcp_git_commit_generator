
# 🏗️ Estructura del Proyecto: FastMCP Git Commit Generator

Este proyecto implementa un **servidor MCP** para generar mensajes de commit automatizados, integrando:

- ✅ Análisis de `git diff` y estado del repositorio.
- 🤖 Integración con LLMs locales (como LM Studio, Ollama, o API personalizada).
- 📄 Plantillas de commits en JSON por estilo o equipo.
- 🖥️ Cliente CLI para uso directo desde terminal.

---

## 📁 ESTRUCTURA DE CARPETAS

```
mcp_commit_generator/
│
├── main.py                     # Entrada principal - ejecuta el servidor FastMCP
│
├── server/
│   ├── fast_server.py          # Decoradores MCP y lógica de herramientas
│   ├── git_utils.py            # Funciones para interactuar con git (status, diff)
│   ├── analyzer.py             # Análisis de cambios y generación base de commits
│   └── config_loader.py        # Lectura y validación de archivos de configuración JSON
│
├── llm/
│   ├── llm_client.py           # Cliente para interactuar con modelos LLM locales
│   └── prompts.py              # Prompts base y plantillas para generar commits AI
│
├── cli/
│   └── cli.py                  # Interfaz CLI para interactuar con el servidor FastMCP
│
├── templates/
│   └── default_template.json   # Plantilla JSON para formateo de commits
│
├── tests/
│   └── test_git_utils.py       # Tests unitarios (pytest)
│
├── .mcp-commit.json            # Configuración por proyecto (opcional)
├── requirements.txt            # Dependencias del proyecto
└── README.md                   # Instrucciones de instalación y uso
```

---

## 🔧 COMPONENTES CLAVE

### 1. `main.py`
Inicia el servidor MCP usando FastMCP. Carga las herramientas disponibles y gestiona el ciclo de vida del servidor.

---

### 2. `/server/`
Contiene toda la lógica principal:

- `fast_server.py`: Herramientas MCP registradas con decoradores (`@mcp.tool()`).
- `git_utils.py`: Comandos para obtener `diff`, `status`, ramas, etc.
- `analyzer.py`: Lógica para analizar cambios y generar mensaje base.
- `config_loader.py`: Lee `.mcp-commit.json` y plantillas de commits.

---

### 3. `/llm/`
Interfaz con modelos de lenguaje:

- `llm_client.py`: Envía prompts a un modelo como LM Studio u Ollama.
- `prompts.py`: Contiene templates para generar buenos prompts a partir del diff.

---

### 4. `/cli/`
CLI para interactuar desde terminal o shell scripts:

```bash
mcp-commit generate --type feat --scope auth
mcp-commit status
```

---

### 5. `/templates/`
Plantillas de estilos de commit personalizadas. Ejemplos:

```json
{
  "style": "conventional",
  "formats": {
    "feat": "feat({scope}): {description}",
    "fix": "fix({scope}): {description}"
  },
  "rules": {
    "lowercase_first_letter": true,
    "description_max_length": 50,
    "remove_period": true
  }
}
```

---

### 6. `/tests/`
Módulo de pruebas unitarias usando `pytest`.

---

### 7. `.mcp-commit.json`
Archivo de configuración personalizado por proyecto. Puedes definir:

```json
{
  "style": "emoji",
  "use_llm": true,
  "llm_model": "llama3",
  "auto_stage": false,
  "include_untracked": true
}
```

---

## 🚀 SUGERENCIA DE FLUJO DE DESARROLLO

1. Implementa `llm_client.py` (integración con LM Studio u Ollama).
2. Añade un `prompt_builder()` en `prompts.py`.
3. Refactoriza `generate_commit_message()` para usar LLM o fallback a análisis clásico.
4. Carga y aplica plantillas desde `templates/`.
5. Desarrolla el CLI con `argparse`.
6. Documenta todo en `README.md`.

---

## 📦 DEPENDENCIAS

```txt
# requirements.txt
mcp
openai    # (opcional, si usas API remota)
requests  # para LLM locales vía REST
```

---

## 📌 LICENCIA

Este proyecto es de código abierto. Puedes usarlo, modificarlo o integrarlo en tus herramientas de desarrollo continuo.
