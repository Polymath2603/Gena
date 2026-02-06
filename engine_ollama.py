"""
Ollama Backend Engine for Gena AI
Handles all Ollama API interactions and configuration
"""

import requests
import re


class OllamaEngine:
    """Ollama backend implementation with full configuration"""
    
    def __init__(self, 
                 model="qwen2.5-1.5b-instruct",
                 host="http://localhost:11434",
                 temperature=0.8,
                 top_p=0.9,
                 num_predict=200,
                 num_ctx=2048,
                 num_thread=4,
                 timeout=120):
        """
        Initialize Ollama engine
        
        Args:
            model: Model name in Ollama
            host: Ollama server URL
            temperature: Sampling temperature (0-1, higher = more random)
            top_p: Nucleus sampling threshold
            num_predict: Max tokens to generate
            num_ctx: Context window size
            num_thread: Number of CPU threads
            timeout: Request timeout in seconds
        """
        self.model = model
        self.host = host
        self.temperature = temperature
        self.top_p = top_p
        self.num_predict = num_predict
        self.num_ctx = num_ctx
        self.num_thread = num_thread
        self.timeout = timeout
        
        # Stop sequences to prevent hallucination
        self.stop_sequences = [
            "User:", "You:", "\nU:", "\nYou:", "\nGena:", 
            "U:", "G:", "Human:", "\nHuman:"
        ]
    
    def generate(self, prompt):
        """
        Generate response from Ollama
        
        Args:
            prompt: Full prompt with system + context + user message
            
        Returns:
            Generated response text
        """
        try:
            response = requests.post(
                f"{self.host}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": self.temperature,
                        "top_p": self.top_p,
                        "num_predict": self.num_predict,
                        "num_ctx": self.num_ctx,
                        "num_thread": self.num_thread,
                        "stop": self.stop_sequences
                    }
                },
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                text = response.json().get("response", "").strip()
                
                # Clean up any conversation artifacts that slipped through
                text = re.sub(r'\n[UG]:', '', text)  # Remove U: or G: at line starts
                text = re.sub(r'\s+', ' ', text)  # Normalize whitespace
                
                return text.strip()
            else:
                return f"Hmm, error {response.status_code}..."
        
        except requests.exceptions.ConnectionError:
            return "Can't connect to Ollama! Is it running? (ollama serve)"
        except requests.exceptions.Timeout:
            return "Timeout! That took too long..."
        except Exception as e:
            return f"Error: {str(e)}"
    
    def check_available(self):
        """Check if Ollama server is available"""
        try:
            response = requests.get(f"{self.host}/api/tags", timeout=2)
            return response.status_code == 200
        except:
            return False
    
    def list_models(self):
        """List available models in Ollama"""
        try:
            response = requests.get(f"{self.host}/api/tags", timeout=5)
            if response.status_code == 200:
                models = response.json().get("models", [])
                return [model["name"] for model in models]
            return []
        except:
            return []
    
    def update_config(self, **kwargs):
        """Update engine configuration dynamically"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
