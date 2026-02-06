"""
Ollama Backend Engine for Gena
"""

import requests


class OllamaEngine:
    """Ollama backend implementation"""
    
    def __init__(self, model="hf.co/Qwen/Qwen2.5-1.5B-Instruct-GGUF:Q4_K_M", 
                 host="http://localhost:11434"):
        self.model = model
        self.host = host
        self.timeout = 120
    
    def generate(self, prompt):
        """Generate response from Ollama"""
        try:
            response = requests.post(
                f"{self.host}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.8,
                        "top_p": 0.9,
                        "num_predict": 200,
                        "num_ctx": 2048,
                        "num_thread": 4,
                        "stop": ["User:", "You:", "\nU:", "\nYou:", "\nGena:", "U:", "G:"]  # Stop before continuing conversation
                    }
                },
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                text = response.json().get("response", "").strip()
                # Remove any conversation artifacts that slipped through
                import re
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
