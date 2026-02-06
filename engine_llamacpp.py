"""
llama.cpp Backend Engine for Gena AI
Handles all llama.cpp server interactions and configuration
"""

import requests
import subprocess
import time
from pathlib import Path


class LlamaCppEngine:
    """llama.cpp backend implementation with full configuration"""
    
    def __init__(self,
                 model_path=None,
                 port=8080,
                 host="http://localhost",
                 temperature=0.8,
                 top_p=0.9,
                 max_tokens=200,
                 context_size=2048,
                 num_threads=4,
                 timeout=120,
                 auto_start=True):
        """
        Initialize llama.cpp engine
        
        Args:
            model_path: Path to GGUF model file
            port: Server port
            host: Server host
            temperature: Sampling temperature
            top_p: Nucleus sampling threshold
            max_tokens: Max tokens to generate
            context_size: Context window size
            num_threads: Number of CPU threads
            timeout: Request timeout
            auto_start: Auto-start server if not running
        """
        self.model_path = Path(model_path) if model_path else None
        self.port = port
        self.host = f"{host}:{port}"
        self.temperature = temperature
        self.top_p = top_p
        self.max_tokens = max_tokens
        self.context_size = context_size
        self.num_threads = num_threads
        self.timeout = timeout
        self.process = None
        
        # Stop sequences
        self.stop_sequences = ["User:", "You:", "\n\n"]
        
        if auto_start and model_path:
            self.start_server()
    
    def start_server(self):
        """Start llama-server if not already running"""
        # Check if already running
        if self.check_available():
            print(f"✓ llama.cpp server already running on port {self.port}")
            return True
        
        if not self.model_path or not self.model_path.exists():
            print(f"✗ Model file not found: {self.model_path}")
            return False
        
        try:
            cmd = [
                "llama-server",
                "-m", str(self.model_path),
                "-c", str(self.context_size),
                "--port", str(self.port),
                "-t", str(self.num_threads),
                "--log-disable"
            ]
            
            print(f"Starting llama.cpp server...")
            self.process = subprocess.Popen(
                cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            
            # Wait for server to start
            for i in range(30):
                if self.check_available():
                    print("✓ llama.cpp server ready!")
                    return True
                time.sleep(1)
            
            print("✗ Server failed to start")
            return False
            
        except FileNotFoundError:
            print("✗ llama-server not found! Install llama.cpp first.")
            return False
        except Exception as e:
            print(f"✗ Error: {e}")
            return False
    
    def generate(self, prompt):
        """
        Generate response from llama.cpp
        
        Args:
            prompt: Full prompt with system + context + user message
            
        Returns:
            Generated response text
        """
        try:
            # Use completion endpoint (simpler than chat)
            response = requests.post(
                f"{self.host}/completion",
                json={
                    "prompt": prompt,
                    "n_predict": self.max_tokens,
                    "temperature": self.temperature,
                    "top_p": self.top_p,
                    "stop": self.stop_sequences
                },
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                return response.json().get("content", "").strip()
            else:
                return f"llama.cpp error {response.status_code}"
        
        except requests.exceptions.ConnectionError:
            return "Can't connect to llama.cpp! Is the server running?"
        except requests.exceptions.Timeout:
            return "Timeout! Try shorter messages?"
        except Exception as e:
            return f"Error: {str(e)}"
    
    def check_available(self):
        """Check if llama.cpp server is available"""
        try:
            response = requests.get(f"{self.host}/health", timeout=1)
            return response.status_code == 200
        except:
            return False
    
    def stop_server(self):
        """Stop llama-server process"""
        if self.process:
            self.process.terminate()
            self.process.wait()
            print("✓ llama.cpp server stopped")
    
    def update_config(self, **kwargs):
        """Update engine configuration dynamically"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
