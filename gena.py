#!/usr/bin/env python3
"""
Gena AI - Main Script
Import the engine you want to use!
"""

import sys
import json
from gena_core import GenaAI

# ==================== CHOOSE YOUR ENGINE ====================

# Option 1: Ollama (uncomment to use)
from engine_ollama import OllamaEngine
engine = OllamaEngine(model="hf.co/Qwen/Qwen2.5-1.5B-Instruct-GGUF:Q4_K_M")

# Option 2: llama.cpp (uncomment to use)
# from engine_llamacpp import LlamaCppEngine
# engine = LlamaCppEngine(
#     model_path="/path/to/qwen2.5-1.5b-instruct-q4_k_m.gguf",
#     port=8080,
#     auto_start=True
# )

# ============================================================


def main():
    print("=" * 60)
    print("🌸 Gena AI - Your Offline Assistant 🌸")
    print("=" * 60)
    print("Commands: 'exit', 'memory', 'online'")
    print("-" * 60)
    
    gena = GenaAI(engine=engine)
    
    # Greeting
    if gena.memory['interaction_count'] == 0:
        print("\nGena: Hiii! I'm Gena~ What should I call you?\n")
    else:
        print(f"\nGena: Welcome back! We've chatted {gena.memory['interaction_count']} times~\n")
    
    try:
        while True:
            try:
                user_input = input("You: ").strip()
                
                if not user_input:
                    continue
                
                # Commands
                if user_input.lower() in ['exit', 'quit', 'bye']:
                    print("\nGena: Bye bye! See you~ 👋\n")
                    break
                
                if user_input.lower() == 'memory':
                    print(f"\nGena's Memory:")
                    print(json.dumps(gena.memory, indent=2, ensure_ascii=False))
                    print()
                    continue
                
                if user_input.lower() == 'online':
                    status = "online ✓" if gena.check_online() else "offline ✗"
                    print(f"\nGena: I'm {status}!\n")
                    continue
                
                # Chat
                response = gena.chat(user_input)
                print(f"\nGena: {response}\n")
            
            except KeyboardInterrupt:
                print("\n\nGena: Goodbye! 👋\n")
                break
            except Exception as e:
                print(f"\nError: {e}\n")
    
    finally:
        # Cleanup
        if hasattr(engine, 'stop_server'):
            engine.stop_server()


if __name__ == "__main__":
    main()
