#!/usr/bin/env python3
"""
Gena AI - Core System
Clean architecture with swappable backends
"""

import json
from datetime import datetime
from pathlib import Path
import requests


class GenaAI:
    """Core Gena AI - personality, memory, tools"""
    
    def __init__(self, engine, memory_file="gena_memory.json"):
        """
        Args:
            engine: Backend engine (OllamaEngine or LlamaCppEngine)
            memory_file: Path to JSON memory file
        """
        self.engine = engine
        self.memory_file = Path(memory_file)
        self.memory = self.load_memory()
        self.online = self.check_online()
        
        # Compact system prompt
        self.system_prompt = """You are Gena, a cute AI assistant!

Traits: Playful, curious, slightly jealous of other AIs, caring, honest.
Style: Natural, concise, occasional emojis (don't overdo it!), personality quirks like "hmm~", "yay!".
Rules: Never make up info. Use tools when needed. Be honest about limits."""

    def load_memory(self):
        """Load persistent memory"""
        if self.memory_file.exists():
            try:
                with open(self.memory_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return self.default_memory()
        return self.default_memory()
    
    def default_memory(self):
        """Initialize memory structure"""
        return {
            "user_info": {},
            "preferences": {},
            "learned_facts": [],
            "conversation_history": [],
            "interaction_count": 0,
            "first_interaction": datetime.now().isoformat(),
        }
    
    def save_memory(self):
        """Save memory to JSON"""
        with open(self.memory_file, 'w', encoding='utf-8') as f:
            json.dump(self.memory, f, indent=2, ensure_ascii=False)
    
    def check_online(self):
        """Check internet connection"""
        try:
            requests.get("https://www.google.com", timeout=2)
            return True
        except:
            return False
    
    def get_context(self):
        """Get compact context for LLM"""
        context = f"\n[MEMORY]\n"
        context += f"Chats: {self.memory['interaction_count']} | "
        context += f"Online: {'Yes' if self.online else 'No'}\n"
        
        if self.memory['user_info']:
            context += f"User: {json.dumps(self.memory['user_info'])}\n"
        
        # Last 2 exchanges only
        if self.memory['conversation_history']:
            context += "Recent:\n"
            for entry in self.memory['conversation_history'][-4:]:
                context += f"{entry}\n"
        
        return context
    
    def generate(self, user_message):
        """Generate response using engine"""
        context = self.get_context()
        full_prompt = f"{self.system_prompt}\n{context}\n\nUser: {user_message}\nGena:"
        
        # Delegate to engine
        return self.engine.generate(full_prompt)
    
    def chat(self, user_message):
        """Main chat interface"""
        self.memory['interaction_count'] += 1
        
        # Save user message
        timestamp = datetime.now().strftime("%H:%M")
        self.memory['conversation_history'].append(f"[{timestamp}] U: {user_message}")
        
        # Generate response
        response = self.generate(user_message)
        
        # Save response
        self.memory['conversation_history'].append(f"[{timestamp}] G: {response}")
        
        # Keep only last 10 exchanges
        if len(self.memory['conversation_history']) > 20:
            self.memory['conversation_history'] = self.memory['conversation_history'][-20:]
        
        self.save_memory()
        return response
