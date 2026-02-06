#!/usr/bin/env python3
"""
Gena AI - Core System
Clean architecture with swappable backends
"""

import json
from datetime import datetime
from pathlib import Path
import requests
import sys


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
Style: Natural, concise, occasional emojis (sparingly!). Speak normally without quirky symbols like ~.
Rules: Never make up info. Never simulate the user's responses. Stop after YOUR response only.

TOOLS AVAILABLE:
- execute_python(code) - Run Python code for math/calculations
- learn_fact(topic, fact) - Remember important facts
- learn_procedure(name, steps) - Learn how to do tasks

To use a tool, respond with: TOOL[tool_name](args)
Example: TOOL[execute_python](2 + 2)"""

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
            "learned_facts": {},
            "learned_procedures": {},
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
        
        # Show learned facts
        if self.memory['learned_facts']:
            context += f"Facts I know: {len(self.memory['learned_facts'])} topics\n"
        
        # Show learned procedures
        if self.memory['learned_procedures']:
            context += f"Procedures I learned: {', '.join(self.memory['learned_procedures'].keys())}\n"
        
        # Last 2 exchanges only
        if self.memory['conversation_history']:
            context += "Recent:\n"
            for entry in self.memory['conversation_history'][-4:]:
                context += f"{entry}\n"
        
        return context
    
    def execute_python(self, code):
        """Execute Python code safely"""
        try:
            # Safe builtins
            safe_globals = {
                '__builtins__': {
                    'abs': abs, 'min': min, 'max': max, 'sum': sum,
                    'round': round, 'len': len, 'range': range,
                    'str': str, 'int': int, 'float': float,
                    'list': list, 'dict': dict, 'print': print
                }
            }
            
            # Import safe modules
            import math
            safe_globals['math'] = math
            
            # Capture output
            from io import StringIO
            old_stdout = sys.stdout
            sys.stdout = StringIO()
            
            # Execute
            exec_globals = safe_globals.copy()
            exec(code, exec_globals)
            
            # Get output
            output = sys.stdout.getvalue()
            sys.stdout = old_stdout
            
            # Get result from last expression
            result = eval(code, exec_globals) if output == "" else output
            
            return f"Result: {result}"
        except Exception as e:
            sys.stdout = old_stdout
            return f"Error: {str(e)}"
    
    def learn_fact(self, topic, fact):
        """Learn and remember a fact"""
        self.memory['learned_facts'][topic] = {
            "content": fact,
            "learned_at": datetime.now().isoformat()
        }
        self.save_memory()
        return f"Got it! I'll remember that about {topic}."
    
    def learn_procedure(self, name, steps):
        """Learn a procedure"""
        self.memory['learned_procedures'][name] = {
            "steps": steps,
            "learned_at": datetime.now().isoformat()
        }
        self.save_memory()
        return f"Yay! I learned how to {name}!"
    
    def process_tools(self, response):
        """Check if response contains tool calls and execute them"""
        if "TOOL[" not in response:
            return response
        
        # Extract tool calls
        import re
        pattern = r'TOOL\[(\w+)\]\(([^)]+)\)'
        matches = re.findall(pattern, response)
        
        if not matches:
            return response
        
        # Execute tools
        results = []
        for tool_name, args in matches:
            if tool_name == "execute_python":
                result = self.execute_python(args)
                results.append(result)
            elif tool_name == "learn_fact":
                # Parse topic, fact
                parts = args.split(',', 1)
                if len(parts) == 2:
                    topic = parts[0].strip().strip('"').strip("'")
                    fact = parts[1].strip().strip('"').strip("'")
                    result = self.learn_fact(topic, fact)
                    results.append(result)
            elif tool_name == "learn_procedure":
                # Parse name, steps
                parts = args.split(',', 1)
                if len(parts) == 2:
                    name = parts[0].strip().strip('"').strip("'")
                    steps = parts[1].strip().strip('"').strip("'")
                    result = self.learn_procedure(name, steps)
                    results.append(result)
        
        # Remove tool calls from response
        clean_response = re.sub(pattern, '', response)
        
        # Append results
        if results:
            clean_response += "\n" + "\n".join(results)
        
        return clean_response.strip()
    
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
        
        # Process any tool calls
        response = self.process_tools(response)
        
        # Save response
        self.memory['conversation_history'].append(f"[{timestamp}] G: {response}")
        
        # Keep only last 10 exchanges
        if len(self.memory['conversation_history']) > 20:
            self.memory['conversation_history'] = self.memory['conversation_history'][-20:]
        
        self.save_memory()
        return response
