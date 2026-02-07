#!/usr/bin/env python3
"""
Gena AI - CLI Interface
Pure text interface - no core logic here!
"""

import sys
import json
from gena import Gena

# ==================== ENGINE CONFIGURATION ====================

from engine_ollama import OllamaEngine
engine = OllamaEngine(
    model="qwen2.5:0.5b-instruct",
    temperature=0.8,
    num_predict=200,
    num_ctx=2048,
    num_thread=4
)

# ==============================================================


def main():
    """Main CLI loop - PURE INTERFACE ONLY"""
    print("=" * 60)
    print("🌸 Gena AI - Text Interface 🌸")
    print("=" * 60)
    print("\nCommands: exit, memory, online, teach, recall <n>, stats, help")
    print("-" * 60)
    
    # Initialize Gena
    gena = Gena(engine=engine)
    
    # Greeting
    print(f"\nGena: {gena.get_greeting()}\n")
    
    try:
        while True:
            try:
                user_input = input("You: ").strip()
                if not user_input:
                    continue
                
                cmd = user_input.lower()
                
                # Exit
                if cmd in ['exit', 'quit', 'bye']:
                    print("\nGena: Bye bye! See you next time! 👋\n")
                    break
                
                # Memory
                if cmd == 'memory':
                    print(f"\n{'='*60}\nMEMORY\n{'='*60}")
                    print(json.dumps(gena.export_memory(), indent=2))
                    print("=" * 60 + "\n")
                    continue
                
                # Online
                if cmd == 'online':
                    print(f"\nGena: I'm {'online ✓' if gena.online else 'offline ✗'}!\n")
                    continue
                
                # Stats
                if cmd == 'stats':
                    stats = gena.get_stats()
                    print(f"\n{'='*60}\nSTATS\n{'='*60}")
                    print(f"Chats: {stats['interaction_count']}")
                    print(f"Facts: {stats['facts_count']}")
                    print(f"Procedures: {', '.join(stats['procedures']) if stats['procedures'] else 'none'}")
                    print(f"Online: {'✓' if stats['online'] else '✗'}")
                    print("=" * 60 + "\n")
                    continue
                
                # Help
                if cmd == 'help':
                    print("\nCommands:")
                    print("  exit       - End chat")
                    print("  memory     - Show memory")
                    print("  online     - Check connection")
                    print("  teach      - Teach procedure")
                    print("  recall <n> - Show procedure")
                    print("  stats      - Show stats\n")
                    continue
                
                # Teach
                if cmd == 'teach':
                    name = input("Name: ").strip()
                    if not name:
                        continue
                    print("Steps (one per line, 'done' to finish):")
                    steps = []
                    while True:
                        step = input("  ").strip()
                        if step.lower() == 'done':
                            break
                        if step:
                            steps.append(step)
                    if steps:
                        print(f"\nGena: {gena.teach_procedure(name, steps)}\n")
                    continue
                
                # Recall
                if cmd.startswith('recall '):
                    name = user_input[7:].strip()
                    proc = gena.recall_procedure(name)
                    if proc:
                        print(f"\nGena: Here's how to {name}:")
                        for i, step in enumerate(proc['steps'], 1):
                            print(f"  {i}. {step}")
                        print()
                    else:
                        print(f"\nGena: I don't know how to {name}!\n")
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
        gena.shutdown()


if __name__ == "__main__":
    main()
