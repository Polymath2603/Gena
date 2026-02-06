"""
Tools System for Gena AI
All available tools and their implementations
"""

import sys
from io import StringIO


class Tools:
    """Available tools for Gena"""
    
    @staticmethod
    def get_tool_descriptions():
        """Return tool descriptions for system prompt"""
        return """
TOOLS AVAILABLE:
- execute_python(code) - Run Python code for math/calculations
- learn_fact(topic, fact) - Remember important facts
- learn_procedure(name, steps) - Learn how to do tasks step-by-step

To use a tool, respond with: TOOL[tool_name](args)
Example: TOOL[execute_python](2 + 2)
"""
    
    @staticmethod
    def execute_python(code):
        """Execute Python code safely for calculations"""
        try:
            # Safe builtins only
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
            old_stdout = sys.stdout
            sys.stdout = StringIO()
            
            try:
                # Execute code
                exec_globals = safe_globals.copy()
                exec(code, exec_globals)
                
                # Get output
                output = sys.stdout.getvalue()
                
                # Try to get result from evaluation
                if output == "":
                    result = eval(code, exec_globals)
                else:
                    result = output
                
                return f"Result: {result}"
            finally:
                sys.stdout = old_stdout
                
        except Exception as e:
            if sys.stdout != sys.__stdout__:
                sys.stdout = sys.__stdout__
            return f"Error: {str(e)}"
    
    @staticmethod
    def process_tool_calls(response, memory, callback_map):
        """
        Process tool calls in response
        
        Args:
            response: LLM response text
            memory: Memory instance for learn_fact/learn_procedure
            callback_map: Dict mapping tool names to callbacks
        
        Returns:
            Cleaned response with tool results appended
        """
        if "TOOL[" not in response:
            return response
        
        import re
        pattern = r'TOOL\[(\w+)\]\(([^)]+)\)'
        matches = re.findall(pattern, response)
        
        if not matches:
            return response
        
        # Execute tools
        results = []
        for tool_name, args in matches:
            if tool_name == "execute_python":
                result = Tools.execute_python(args)
                results.append(result)
            
            elif tool_name == "learn_fact":
                if memory and hasattr(memory, 'learn_fact'):
                    # Parse topic, fact from args
                    parts = args.split(',', 1)
                    if len(parts) == 2:
                        topic = parts[0].strip().strip('"').strip("'")
                        fact = parts[1].strip().strip('"').strip("'")
                        result = memory.learn_fact(topic, fact)
                        results.append(result)
            
            elif tool_name == "learn_procedure":
                if memory and hasattr(memory, 'learn_procedure'):
                    # Parse name, steps from args
                    parts = args.split(',', 1)
                    if len(parts) == 2:
                        name = parts[0].strip().strip('"').strip("'")
                        steps = parts[1].strip().strip('"').strip("'")
                        result = memory.learn_procedure(name, steps)
                        results.append(result)
            
            # Custom callbacks
            elif tool_name in callback_map:
                result = callback_map[tool_name](args)
                results.append(result)
        
        # Remove tool calls from response
        clean_response = re.sub(pattern, '', response)
        
        # Append results
        if results:
            clean_response += "\n" + "\n".join(results)
        
        return clean_response.strip()
