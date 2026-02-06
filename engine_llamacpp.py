"""
llama.cpp Backend Engine for Gena
"""

import requests
import subprocess
import time


class LlamaCppEngine:
    """llama.cpp backend implementation"""
    
    def __init__(self, model_path=None, port=8080, auto_start=True):
        self.model_path = model_path
        self.port = port
        self.host = f"http://localhost:{port}"
        self.timeout = 120
        self.process = None
        
        if auto_start and model_path:
            self.start_server()
    
    def start_server(self):
        """Start llama-server if not running"""
        # Check if already running
        try:
            requests.get(f"{self.host}/health", timeout=1)
            print(f"✓ llama.cpp server already running on port {self.port}")
            return True
        except:
            pass
        
        # Start server
        try:
            cmd = [
                "llama-server",
                "-m", self.model_path,
                "-c", "2048",
                "--port", str(self.port),
                "-t", "4",
                "--log-disable"
            ]
            
            print(f"Starting llama.cpp server...")
            self.process = subprocess.Popen(
                cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            
            # Wait for server
            for i in range(30):
                try:
                    requests.get(f"{self.host}/health", timeout=1)
                    print("✓ llama.cpp server ready!")
                    return True
                except:
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
        """Generate response from llama.cpp"""
        try:
            # Simple completion endpoint (faster than chat)
            response = requests.post(
                f"{self.host}/completion",
                json={
                    "prompt": prompt,
                    "n_predict": 200,
                    "temperature": 0.8,
                    "top_p": 0.9,
                    "stop": ["User:", "\n\n"]
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
    
    def stop_server(self):
        """Stop llama-server"""
        if self.process:
            self.process.terminate()
            self.process.wait()
            print("✓ llama.cpp server stopped")
