"""
Gena AI - Main Coordinator
Brings together engine, memory, and tools
"""

import requests
from memory import Memory
from tools import Tools


class Gena:
    """Main Gena AI class - coordinates all components"""
    
    def __init__(self, engine, memory_db="memory.db"):
        """
        Initialize Gena
        
        Args:
            engine: Backend engine (OllamaEngine or LlamaCppEngine)
            memory_db: Path to memory database
        """
        self.engine = engine
        self.memory = Memory(memory_db)
        self.tools = Tools()
        self.online = self._check_online()
        
        # System prompt (personality)
        self.system_prompt = """You are Gena, a cute AI assistant!

Traits: Playful, curious, slightly jealous of other AIs, caring, honest.
Style: Natural, concise, occasional emojis (sparingly!). Speak normally without quirky symbols like ~.
Rules: Never make up info. Never simulate the user's responses. Stop after YOUR response only.
""" + Tools.get_tool_descriptions()
    
    def _check_online(self):
        """Check if internet is available"""
        try:
            requests.get("https://www.google.com", timeout=2)
            return True
        except:
            return False
    
    def get_full_prompt(self, user_message):
        """Build complete prompt with system + memory + user message"""
        context = self.memory.get_context_summary()
        context += f"Online: {'Yes' if self.online else 'No'}\n"
        
        full_prompt = f"{self.system_prompt}\n{context}\n\nUser: {user_message}\nGena:"
        return full_prompt
    
    def chat(self, user_message):
        """
        Main chat interface
        
        Args:
            user_message: User's message
            
        Returns:
            Gena's response
        """
        # Increment interaction count
        self.memory.increment_interaction_count()
        
        # Save user message
        self.memory.add_message('user', user_message)
        
        # Build prompt and generate
        prompt = self.get_full_prompt(user_message)
        response = self.engine.generate(prompt)
        
        # Process any tool calls
        response = self.tools.process_tool_calls(
            response, 
            self.memory,
            callback_map={}  # Add custom tool callbacks here if needed
        )
        
        # Save Gena's response
        self.memory.add_message('assistant', response)
        
        # Clean up old conversations
        self.memory.clear_old_conversations(keep_last=20)
        
        return response
    
    def get_stats(self):
        """Get memory statistics"""
        return {
            'interaction_count': self.memory.get_metadata('interaction_count'),
            'facts_count': self.memory.get_facts_count(),
            'procedures': self.memory.get_procedures_list(),
            'online': self.online
        }
    
    def shutdown(self):
        """Clean shutdown"""
        self.memory.close()
        if hasattr(self.engine, 'stop_server'):
            self.engine.stop_server()
