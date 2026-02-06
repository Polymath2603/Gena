#!/usr/bin/env python3
"""
Gena AI - CLI Interface
Beautiful command-line chat interface
"""

import sys
import json
from gena import Gena

# ==================== ENGINE CONFIGURATION ====================

# Choose your engine here:

# Option 1: Ollama (default)
from engine_ollama import OllamaEngine
engine = OllamaEngine(
    model="qwen2.5-1.5b-instruct",  # or "hf.co/Qwen/Qwen2.5-1.5B-Instruct-GGUF:Q4_K_M"
    temperature=0.8,
    num_predict=200,
    num_ctx=2048,
    num_thread=4
)

# Option 2: llama.cpp (uncomment to use)
# from engine_llamacpp import LlamaCppEngine
# engine = LlamaCppEngine(
#     model_path="models/chat/qwen2.5-1.5b-instruct-q4_k_m.gguf",
#     port=8080,
#     temperature=0.8,
#     max_tokens=200,
#     context_size=2048,
#     num_threads=4,
#     auto_start=True
# )

# ==============================================================


def print_header():
    """Print welcome header"""
    print("=" * 60)
    print("🌸 Gena AI - Your Offline Assistant 🌸")
    print("=" * 60)
    print("\nCommands:")
    print("  exit/quit        - End conversation")
    print("  memory           - Show what I remember")
    print("  online           - Check connection status")
    print("  teach <name>     - Teach me a procedure")
    print("  recall <name>    - Show learned procedure")
    print("  stats            - Show my statistics")
    print("  help             - Show this help")
    print("-" * 60)


def print_memory(gena):
    """Display memory contents"""
    print("\n" + "=" * 60)
    print("GENA'S MEMORY")
    print("=" * 60)
    
    data = gena.memory.export_all()
    print(json.dumps(data, indent=2, ensure_ascii=False))
    print("=" * 60 + "\n")


def print_stats(gena):
    """Display statistics"""
    stats = gena.get_stats()
    print("\n" + "=" * 60)
    print("STATISTICS")
    print("=" * 60)
    print(f"Total conversations: {stats['interaction_count']}")
    print(f"Facts learned: {stats['facts_count']}")
    print(f"Procedures learned: {len(stats['procedures'])}")
    if stats['procedures']:
        print(f"  - {', '.join(stats['procedures'])}")
    print(f"Online status: {'✓ Connected' if stats['online'] else '✗ Offline'}")
    print("=" * 60 + "\n")


def teach_procedure(gena):
    """Interactive procedure teaching"""
    name = input("Procedure name: ").strip()
    if not name:
        print("Cancelled.\n")
        return
    
    print(f"Teaching '{name}'. Enter steps (one per line). Type 'done' when finished:")
    steps = []
    while True:
        step = input("  Step: ").strip()
        if step.lower() == 'done':
            break
        if step:
            steps.append(step)
    
    if steps:
        result = gena.memory.learn_procedure(name, steps)
        print(f"\nGena: {result}\n")
    else:
        print("\nNo steps provided!\n")


def recall_procedure(gena, name):
    """Display learned procedure"""
    proc = gena.memory.get_procedure(name)
    if proc:
        print(f"\nGena: Here's how to {name}:")
        for i, step in enumerate(proc, 1):
            print(f"  {i}. {step}")
        print()
    else:
        print(f"\nGena: I don't know how to {name} yet!\n")


def print_help():
    """Display help"""
    print("\n" + "=" * 60)
    print("HELP")
    print("=" * 60)
    print("Commands:")
    print("  exit, quit, bye  - Exit Gena")
    print("  memory           - View all stored memory")
    print("  online           - Check internet connection")
    print("  teach <name>     - Teach a procedure step by step")
    print("  recall <name>    - View a learned procedure")
    print("  stats            - View statistics")
    print("  help             - Show this help")
    print("\nJust chat normally for everything else!")
    print("=" * 60 + "\n")


def main():
    """Main CLI loop"""
    print_header()
    
    # Initialize Gena
    print("\nInitializing Gena...")
    gena = Gena(engine=engine, memory_db="memory.db")
    
    # Greeting
    count = gena.memory.get_metadata('interaction_count')
    if int(count) == 0:
        print("\nGena: Hiii! I'm Gena! What should I call you?\n")
    else:
        print(f"\nGena: Welcome back! We've chatted {count} times before!\n")
    
    try:
        while True:
            try:
                user_input = input("You: ").strip()
                
                if not user_input:
                    continue
                
                # Commands
                cmd_lower = user_input.lower()
                
                if cmd_lower in ['exit', 'quit', 'bye']:
                    print("\nGena: Bye bye! See you next time! 👋\n")
                    break
                
                if cmd_lower == 'memory':
                    print_memory(gena)
                    continue
                
                if cmd_lower == 'online':
                    status = "online ✓" if gena.online else "offline ✗"
                    print(f"\nGena: I'm {status}!\n")
                    continue
                
                if cmd_lower == 'stats':
                    print_stats(gena)
                    continue
                
                if cmd_lower == 'help':
                    print_help()
                    continue
                
                if cmd_lower.startswith('teach'):
                    teach_procedure(gena)
                    continue
                
                if cmd_lower.startswith('recall '):
                    name = user_input[7:].strip()
                    recall_procedure(gena, name)
                    continue
                
                # Regular chat
                response = gena.chat(user_input)
                print(f"\nGena: {response}\n")
            
            except KeyboardInterrupt:
                print("\n\nGena: Goodbye! 👋\n")
                break
            except Exception as e:
                print(f"\nError: {e}\n")
                import traceback
                traceback.print_exc()
    
    finally:
        # Cleanup
        gena.shutdown()


if __name__ == "__main__":
    main()
