# Gena AI - Offline AI Assistant Setup Guide

## What You're Getting

**Gena** is a cute, playful offline AI assistant with:
- ✨ Female-ish personality (playful, curious, slightly jealous)
- 🧠 Persistent memory (remembers you across sessions)
- 🛠️ Tool orchestration (Python execution, websearch, Gemini API)
- 💾 Works on 4GB RAM
- 📝 No hallucination - honest about limitations
- 🌐 Works offline (online features optional)

---

## Installation Steps

### 1. Install Ollama

**Linux:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

**Windows:**
Download from: https://ollama.com/download

**macOS:**
```bash
brew install ollama
```

### 2. Download the AI Model

This downloads Qwen2.5-3B (~2GB), perfect for 4GB RAM:

```bash
ollama pull qwen2.5:3b
```

**Alternative models** (if you want to experiment):
- `qwen2.5:1.5b` - Even smaller (~1GB) but less capable
- `phi3.5:3.8b` - Alternative option (~2.2GB)

### 3. Install Python Dependencies

```bash
pip install requests
```

That's it! Just one dependency.

### 4. Start Ollama Server

```bash
ollama serve
```

Leave this running in a terminal. It runs the AI model locally.

### 5. Run Gena!

```bash
python gena_ai.py
```

---

## Optional Setup

### Enable Gemini Integration (Optional)

If you want Gena to occasionally ask Gemini for help:

1. Get a free API key: https://makersuite.google.com/app/apikey
2. Set environment variable:

**Linux/Mac:**
```bash
export GEMINI_API_KEY="your-key-here"
```

**Windows (CMD):**
```cmd
set GEMINI_API_KEY=your-key-here
```

**Windows (PowerShell):**
```powershell
$env:GEMINI_API_KEY="your-key-here"
```

---

## How to Use

### Basic Chat
```
You: Hi Gena!
Gena: Hiii! Nice to meet you~ ✨ What should I call you?

You: Call me Alex
Gena: Okay Alex! I'll remember that~ 😊
```

### Tool Usage Examples

**Python calculations:**
```
You: What's the square root of 144?
Gena: Let me calculate that for you! *runs Python* 
     The answer is 12! ✨
```

**Web search (when online):**
```
You: What's the weather like today?
Gena: Hmm, let me search that for you! *searching...*
     [Gena will attempt to search and summarize]
```

**Memory:**
```
You: memory
[Shows everything Gena remembers about you]
```

**Check online status:**
```
You: online
Gena: I'm currently offline ✗!
```

---

## Memory File

Gena stores everything she learns in `gena_memory.json` in the same folder.

This includes:
- User information (name, preferences)
- Learned facts
- Conversation history (last 20 exchanges)
- Skills she's learned
- Interaction count

**To reset Gena's memory:** Delete `gena_memory.json`

---

## Personality Customization

Want to adjust Gena's personality? Edit the `system_prompt` in `gena_ai.py`:

```python
self.system_prompt = """You are Gena, a cute and playful AI assistant...
```

Change traits like:
- More/less playful
- Different emoji usage
- Jealousy level
- Formality

---

## Performance Tips

### For 4GB RAM:

1. **Use swap space** (you mentioned you have this - good!)
2. **Close other apps** when running Gena
3. **Use the 3B model** (recommended) or try 1.5B if it's too slow
4. **Limit conversation history** - Already set to 20 exchanges

### Speed vs Quality:

Edit in `gena_ai.py`:
```python
"options": {
    "num_predict": 256,  # Reduce from 512 for faster responses
    "temperature": 0.7   # Lower = more focused, less creative
}
```

---

## Troubleshooting

### "Can't connect to Ollama"
- Make sure `ollama serve` is running
- Check it's running on `http://localhost:11434`

### Slow responses
- Try smaller model: `ollama pull qwen2.5:1.5b`
- Reduce `num_predict` in code
- Close background apps

### Out of memory
- Use `qwen2.5:1.5b` instead
- Increase swap space
- Reduce context window in code

### Gena seems repetitive
- Increase `temperature` to 0.9 for more variety
- Or decrease to 0.6 for more consistency

---

## Adding More Tools

Want to add more capabilities? Add functions to the `GenaAI` class:

```python
def search_files(self, query):
    """Search local files"""
    # Your implementation
    pass

def set_reminder(self, message, time):
    """Set a reminder"""
    # Your implementation
    pass
```

Then add them to the `get_context_for_llm()` method so Gena knows about them!

---

## System Requirements

- **Minimum:** 4GB RAM + 4GB swap
- **Recommended:** 6GB+ RAM
- **Storage:** ~3GB for model + dependencies
- **OS:** Linux, Windows, macOS
- **Internet:** Only for optional features (Gemini, websearch)

---

## Enjoy!

You now have a cute, persistent, offline AI assistant that:
- Remembers you
- Has personality
- Can use tools
- Works offline
- Runs on modest hardware

Have fun chatting with Gena! 🌸
