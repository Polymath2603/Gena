# Gena AI - Clean Architecture

## File Structure

```
gena_core.py          # Core AI (personality, memory, logic)
engine_ollama.py      # Ollama backend
engine_llamacpp.py    # llama.cpp backend
gena.py              # Main script (import ONE engine here)
gena_memory.json     # Auto-created memory file
```

**Clean separation:** Core logic never touches backends!

---

## Quick Start

### 1. Choose Your Engine

Edit `gena.py` and uncomment ONE engine:

**Option A: Ollama** (easier, already working)
```python
from engine_ollama import OllamaEngine
engine = OllamaEngine(model="hf.co/Qwen/Qwen2.5-1.5B-Instruct-GGUF:Q4_K_M")
```

**Option B: llama.cpp** (faster, less RAM)
```python
from engine_llamacpp import LlamaCppEngine
engine = LlamaCppEngine(
    model_path="~/.ollama/models/blobs/sha256-6a1a2eb...",
    port=8080,
    auto_start=True
)
```

### 2. Run

```bash
python gena.py
```

Done! No bloated multi-backend code.

---

## Switch Engines

Just edit one line in `gena.py`:

```python
# Switch from Ollama to llama.cpp
# from engine_ollama import OllamaEngine
# engine = OllamaEngine(...)

from engine_llamacpp import LlamaCppEngine
engine = LlamaCppEngine(...)
```

Save, restart. That's it!

---

## Customization

### Change Ollama Settings

Edit `engine_ollama.py`:
```python
def __init__(self, model="your-model", host="http://localhost:11434"):
    self.model = model
    self.timeout = 120  # Change timeout
    # etc...
```

### Change llama.cpp Settings

Edit `engine_llamacpp.py`:
```python
def start_server(self):
    cmd = [
        "llama-server",
        "-m", self.model_path,
        "-c", "2048",  # Context size
        "-t", "4",     # Threads
        # Add more flags...
    ]
```

### Change Personality

Edit `gena_core.py`:
```python
self.system_prompt = """Your custom personality here!"""
```

---

## Add More Engines

Want to add another backend? Create `engine_yourbackend.py`:

```python
class YourEngine:
    def __init__(self, ...):
        # Setup
        pass
    
    def generate(self, prompt):
        # Return response string
        return "response"
```

Import it in `gena.py`:
```python
from engine_yourbackend import YourEngine
engine = YourEngine(...)
```

---

## Why This Is Better

✅ **No noodly code** - each file has ONE job
✅ **Easy to understand** - clear separation
✅ **Easy to extend** - add engines without touching core
✅ **Easy to switch** - change one import line
✅ **No dependencies in core** - `gena_core.py` is clean
✅ **Reusable** - use same core with any engine

---

## File Breakdown

### `gena_core.py`
- Personality
- Memory management
- Tool orchestration (future)
- NO backend code!

### `engine_ollama.py`
- ONLY Ollama API calls
- ~30 lines
- No personality/memory logic

### `engine_llamacpp.py`
- ONLY llama.cpp API calls
- Auto server management
- No personality/memory logic

### `gena.py`
- Glues core + engine
- CLI interface
- That's it!

---

## Current Setup

Your files:
```
gena_core.py         ← Core AI logic
engine_ollama.py     ← Ollama backend (FIXED for your timeouts!)
engine_llamacpp.py   ← llama.cpp backend
gena.py             ← Main script (using Ollama by default)
```

Just run:
```bash
python gena.py
```

Should work NOW with fixed timeouts! 🌸
