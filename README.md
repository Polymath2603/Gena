# Gena AI - Clean Architecture

## Project Structure

```
Gena2/
├── engine_ollama.py       # Ollama backend with all config
├── engine_llamacpp.py     # llama.cpp backend with all config
├── tools.py               # All tools & descriptions
├── memory.py              # SQLite memory management
├── gena.py                # Main coordinator (imports all above)
├── gena_cli.py            # CLI interface (run this!)
├── memory.db              # SQLite database (auto-created)
└── models/
    └── chat/
        └── *.gguf         # Your GGUF models here
```

---

## Quick Start

### 1. Put Your Model

```bash
mkdir -p models/chat
# Copy your GGUF model to models/chat/
```

### 2. Choose Engine

Edit `gena_cli.py`, lines 12-16:

**Ollama:**
```python
from engine_ollama import OllamaEngine
engine = OllamaEngine(model="qwen2.5-1.5b-instruct")
```

**llama.cpp:**
```python
from engine_llamacpp import LlamaCppEngine
engine = LlamaCppEngine(
    model_path="models/chat/qwen2.5-1.5b-instruct-q4_k_m.gguf",
    auto_start=True
)
```

### 3. Run

```bash
python gena_cli.py
```

---

## Features

### ✅ Clean Separation
- **Engine**: Handles LLM backend only
- **Memory**: Handles all data storage only
- **Tools**: Handles capabilities only
- **Gena**: Coordinates everything
- **CLI**: User interface only

### ✅ SQLite Memory
All data in `memory.db`:
- User info (name, preferences)
- Learned facts
- Learned procedures
- Conversation history
- Settings & metadata

### ✅ Tools System
- Python execution (math)
- Learn facts
- Learn procedures
- Easy to extend

### ✅ Swappable Engines
Switch between Ollama/llama.cpp by changing ONE import!

---

## Configuration

### Ollama Settings

Edit `gena_cli.py`:
```python
engine = OllamaEngine(
    model="qwen2.5-1.5b-instruct",  # Model name
    temperature=0.8,                 # Randomness (0-1)
    num_predict=200,                 # Max tokens
    num_ctx=2048,                    # Context size
    num_thread=4                     # CPU threads
)
```

### llama.cpp Settings

```python
engine = LlamaCppEngine(
    model_path="models/chat/model.gguf",
    port=8080,
    temperature=0.8,
    max_tokens=200,
    context_size=2048,
    num_threads=4,
    auto_start=True  # Auto-start server
)
```

---

## Usage

### Commands

```
exit/quit      - Exit
memory         - View all memory
online         - Check connection
teach <n>   - Teach procedure
recall <n>  - View procedure
stats          - Show statistics
help           - Show help
```

### Teaching Procedures

```
You: teach make coffee
Procedure name: make coffee
Teaching 'make coffee'. Enter steps:
  Step: Boil water
  Step: Add coffee
  Step: done

Gena: Yay! I learned how to make coffee!
```

### Using Tools

Gena automatically uses tools when needed:

```
You: What's 25 * 48?
Gena: *calculates* 1,200!

You: My favorite color is blue
Gena: Got it! I'll remember that about favorite color.
```

---

## Memory Database

View with any SQLite browser or:
```bash
sqlite3 memory.db
.tables
SELECT * FROM user_info;
SELECT * FROM facts;
SELECT * FROM procedures;
```

---

## Extending

### Add New Tool

Edit `tools.py`:
```python
@staticmethod
def your_tool(args):
    # Implementation
    return "result"

# Add to process_tool_calls()
elif tool_name == "your_tool":
    result = Tools.your_tool(args)
    results.append(result)

# Add to get_tool_descriptions()
- your_tool(args) - Description
```

### Add New Engine

Create `engine_yourbackend.py`:
```python
class YourEngine:
    def __init__(self, ...):
        pass
    
    def generate(self, prompt):
        # Return response
        return "response"
```

Import in `gena_cli.py`:
```python
from engine_yourbackend import YourEngine
engine = YourEngine(...)
```

---

## File Breakdown

| File | Lines | Purpose |
|------|-------|---------|
| `engine_ollama.py` | ~110 | Ollama API only |
| `engine_llamacpp.py` | ~140 | llama.cpp only |
| `tools.py` | ~120 | Tools logic only |
| `memory.py` | ~320 | SQLite DB only |
| `gena.py` | ~90 | Coordinator only |
| `gena_cli.py` | ~180 | CLI only |

**Total: ~960 lines** vs old noodly 2000+ lines!

---

## Troubleshooting

### Can't connect to Ollama
```bash
ollama serve  # Start Ollama
```

### llama.cpp won't start
```bash
# Install llama.cpp first
sudo apt install llama.cpp
# Or compile from source
```

### Memory errors
```bash
# Reset memory
rm memory.db
```

### Import errors
```bash
# All files must be in same directory
# Check Python path
```

---

## Why This Structure?

**Before:** Everything in one big file = messy
**After:** Each file has ONE job = clean

Want to:
- Switch engines? Edit 1 line
- Add tools? Edit tools.py only
- Change storage? Edit memory.py only
- New interface? Create new CLI file

Perfect separation! 🌸
