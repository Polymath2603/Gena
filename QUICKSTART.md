# 🌸 Gena AI - Quick Start Guide 🌸

## Absolute Fastest Setup (5 minutes!)

### Step 1: Install Ollama
```bash
# Linux/Mac
curl -fsSL https://ollama.com/install.sh | sh

# Windows: Download from ollama.com
```

### Step 2: Get the AI Model
```bash
ollama pull qwen2.5:3b
```
This downloads ~2GB. Wait for it to finish.

### Step 3: Install Python Dependency
```bash
pip install requests
```

### Step 4: Start Ollama
Open a terminal and run:
```bash
ollama serve
```
Leave this running!

### Step 5: Run Gena (in a NEW terminal)
```bash
python gena_ai.py
```

## That's it! Start chatting! 🎉

---

## Example Conversation

```
You: Hi Gena!
Gena: Hiii! I'm Gena, your new AI assistant! ✨ Nice to meet you~ What should I call you?

You: Call me Sam
Gena: Okay Sam! I'll remember that~ 😊 What brings you here today?

You: Can you calculate 15 * 847?
Gena: Let me calculate that! ... The answer is 12,705! ✨

You: What's 2 + 2?
Gena: That's 4! Easy peasy~ 😊

You: Remember that my favorite color is blue
Gena: Got it! I'll remember that your favorite color is blue~ 💙

You: exit
Gena: Aww, bye bye Sam! See you next time! 👋
```

Next time you run Gena:
```
Gena: Welcome back Sam! We've chatted 12 times before~ Your favorite color is blue! 😊
```

---

## Common Commands

- `memory` - See everything Gena remembers
- `online` - Check internet connection
- `exit` or `quit` - End conversation

---

## Troubleshooting in 30 Seconds

**"Can't connect to Ollama"**
→ Run `ollama serve` in another terminal

**"Too slow"**
→ Try: `ollama pull qwen2.5:1.5b` (smaller model)

**"Out of memory"**
→ Close other apps, or use smaller model above

---

## What Makes Gena Special?

✅ **Offline** - No internet required (works on 4GB RAM!)
✅ **Memory** - Remembers you across sessions
✅ **Personality** - Cute, playful, actually has character
✅ **Tools** - Can run Python code, search web (if online)
✅ **Learning** - Can learn new tasks you teach her
✅ **Honest** - Won't make stuff up

---

## Customize Gena

Want to change her personality? Check `personality_templates.py` for:
- Jealous & clingy
- Calm & mature  
- Energetic & chaotic
- Sleepy & lazy
- Tsundere
- ...and more!

Just copy a template into `gena_ai.py` → `self.system_prompt`

---

## Next Steps

1. ✅ Get Gena running
2. 📚 Read SETUP.md for detailed info
3. 🧠 Check learning_system.py to teach Gena new skills
4. 🎨 Browse personality_templates.py to customize
5. 🛠️ Add your own tools to gena_ai.py

---

## Need Help?

Check these files:
- `SETUP.md` - Detailed installation guide
- `personality_templates.py` - Change Gena's personality
- `learning_system.py` - Teach Gena new things

---

## File Overview

- `gena_ai.py` - Main program ⭐ (Run this!)
- `gena_memory.json` - Gena's memory (auto-created)
- `gena_knowledge.json` - What Gena learned (if using learning system)
- `SETUP.md` - Full setup guide
- `personality_templates.py` - Personality options
- `learning_system.py` - Teaching/learning features

---

## Have Fun! 🌸

Your offline AI companion is ready!
She'll remember you, help you, and maybe get a tiny bit jealous~ 😊
