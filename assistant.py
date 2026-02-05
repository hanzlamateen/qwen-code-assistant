#!/usr/bin/env python3
"""
Local Coding Assistant powered by Qwen3-Coder-Next

A privacy-first coding assistant that runs entirely on your local machine.
Uses Ollama and Qwen3-Coder-Next for powerful AI-assisted development.

Author: Your Name
License: MIT
"""

import os
import json
import subprocess
from typing import List, Dict, Optional
from ollama import chat
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()


class QwenCodeAssistant:
    """Main coding assistant class with tool-calling capabilities."""
    
    def __init__(self, model: str = "qwen3-coder-next:q4_K_M"):
        """
        Initialize the coding assistant.
        
        Args:
            model: The Ollama model to use (default: qwen3-coder-next:q4_K_M)
        """
        self.model = model
        self.conversation_history: List[Dict] = []
        self.working_directory = os.getcwd()
        
        # Verify Ollama is running
        self._verify_ollama()
        
    def _verify_ollama(self):
        """Verify that Ollama is running and the model is available."""
        try:
            import requests
            response = requests.get("http://localhost:11434/api/tags")
            if response.status_code != 200:
                console.print("[red]❌ Ollama service is not running![/red]")
                console.print("Please start Ollama: [yellow]ollama serve[/yellow]")
                exit(1)
        except Exception as e:
            console.print(f"[red]❌ Cannot connect to Ollama: {e}[/red]")
            console.print("Please make sure Ollama is installed and running.")
            exit(1)
    
    def read_file(self, filepath: str) -> str:
        """
        Read a file from the filesystem.
        
        Args:
            filepath: Path to the file to read
            
        Returns:
            File contents or error message
        """
        try:
            full_path = os.path.join(self.working_directory, filepath)
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return content
        except FileNotFoundError:
            return f"Error: File not found: {filepath}"
        except PermissionError:
            return f"Error: Permission denied: {filepath}"
        except Exception as e:
            return f"Error reading file {filepath}: {str(e)}"
    
    def write_file(self, filepath: str, content: str) -> str:
        """
        Write content to a file.
        
        Args:
            filepath: Path to the file to write
            content: Content to write to the file
            
        Returns:
            Success message or error
        """
        try:
            full_path = os.path.join(self.working_directory, filepath)
            directory = os.path.dirname(full_path)
            
            if directory and not os.path.exists(directory):
                os.makedirs(directory, exist_ok=True)
            
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return f"✓ Successfully wrote to {filepath} ({len(content)} bytes)"
        except PermissionError:
            return f"Error: Permission denied: {filepath}"
        except Exception as e:
            return f"Error writing file {filepath}: {str(e)}"
    
    def execute_command(self, command: str) -> str:
        """
        Execute a shell command safely.
        
        Args:
            command: The shell command to execute
            
        Returns:
            Command output or error message
        """
        # Safety check - prevent dangerous commands
        dangerous_patterns = ['rm -rf /', 'mkfs', 'dd if=', ':(){:|:&};:']
        if any(pattern in command.lower() for pattern in dangerous_patterns):
            return "Error: Command blocked for safety reasons"
        
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30,
                cwd=self.working_directory
            )
            
            output = []
            if result.stdout:
                output.append(result.stdout)
            if result.stderr:
                output.append(f"STDERR: {result.stderr}")
            if result.returncode != 0:
                output.append(f"Exit code: {result.returncode}")
            
            return "\n".join(output) if output else "Command executed successfully (no output)"
        
        except subprocess.TimeoutExpired:
            return "Error: Command timed out after 30 seconds"
        except Exception as e:
            return f"Error executing command: {str(e)}"
    
    def list_files(self, directory: str = ".") -> str:
        """
        List files in a directory.
        
        Args:
            directory: Directory to list (default: current directory)
            
        Returns:
            List of files or error message
        """
        try:
            target_dir = os.path.join(self.working_directory, directory)
            
            if not os.path.exists(target_dir):
                return f"Error: Directory not found: {directory}"
            
            files = []
            dirs_to_skip = {
                'node_modules', '.git', '__pycache__', 'venv', '.venv',
                '.idea', '.vscode', 'dist', 'build', '.egg-info'
            }
            
            for root, dirs, filenames in os.walk(target_dir):
                # Remove directories we want to skip
                dirs[:] = [d for d in dirs if d not in dirs_to_skip]
                
                for filename in filenames:
                    if filename.startswith('.'):
                        continue
                    filepath = os.path.relpath(
                        os.path.join(root, filename),
                        self.working_directory
                    )
                    files.append(filepath)
            
            if not files:
                return f"No files found in {directory}"
            
            # Limit output to first 100 files
            if len(files) > 100:
                files = files[:100]
                files.append(f"... and {len(files) - 100} more files")
            
            return "\n".join(sorted(files))
        
        except Exception as e:
            return f"Error listing files: {str(e)}"
    
    def search_code(self, query: str, file_pattern: str = "*.py") -> str:
        """
        Search for a pattern in code files.
        
        Args:
            query: Search term
            file_pattern: File pattern to search (e.g., *.py, *.js)
            
        Returns:
            Search results or error message
        """
        try:
            import glob
            results = []
            pattern = f"**/{file_pattern}"
            
            for filepath in glob.glob(pattern, recursive=True):
                # Skip common directories
                if any(skip in filepath for skip in [
                    'node_modules', '.git', '__pycache__', 'venv', '.venv'
                ]):
                    continue
                
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                        if query.lower() in content.lower():
                            lines = content.split('\n')
                            matches = []
                            for i, line in enumerate(lines, 1):
                                if query.lower() in line.lower():
                                    matches.append(f"  Line {i}: {line.strip()}")
                                    if len(matches) >= 3:  # Limit to 3 matches per file
                                        break
                            
                            if matches:
                                results.append(f"\n{filepath}:\n" + "\n".join(matches))
                except Exception:
                    continue
            
            if not results:
                return f"No matches found for '{query}' in {file_pattern} files"
            
            # Limit to first 10 files
            if len(results) > 10:
                results = results[:10]
                results.append(f"\n... and more matches")
            
            return "\n".join(results)
        
        except Exception as e:
            return f"Error searching code: {str(e)}"
    
    def get_available_tools(self) -> List[Dict]:
        """
        Define tools available to the assistant.
        
        Returns:
            List of tool definitions in Ollama format
        """
        return [
            {
                'type': 'function',
                'function': {
                    'name': 'read_file',
                    'description': 'Read the contents of a file from the filesystem',
                    'parameters': {
                        'type': 'object',
                        'properties': {
                            'filepath': {
                                'type': 'string',
                                'description': 'Path to the file to read (relative to working directory)'
                            }
                        },
                        'required': ['filepath']
                    }
                }
            },
            {
                'type': 'function',
                'function': {
                    'name': 'write_file',
                    'description': 'Write content to a file. Creates directories if needed.',
                    'parameters': {
                        'type': 'object',
                        'properties': {
                            'filepath': {
                                'type': 'string',
                                'description': 'Path to the file to write (relative to working directory)'
                            },
                            'content': {
                                'type': 'string',
                                'description': 'Content to write to the file'
                            }
                        },
                        'required': ['filepath', 'content']
                    }
                }
            },
            {
                'type': 'function',
                'function': {
                    'name': 'execute_command',
                    'description': 'Execute a shell command. Use for running tests, installing packages, git operations, etc.',
                    'parameters': {
                        'type': 'object',
                        'properties': {
                            'command': {
                                'type': 'string',
                                'description': 'The shell command to execute'
                            }
                        },
                        'required': ['command']
                    }
                }
            },
            {
                'type': 'function',
                'function': {
                    'name': 'list_files',
                    'description': 'List files in a directory (recursively, excluding common build/cache folders)',
                    'parameters': {
                        'type': 'object',
                        'properties': {
                            'directory': {
                                'type': 'string',
                                'description': 'Directory to list files from (default: current directory)'
                            }
                        }
                    }
                }
            },
            {
                'type': 'function',
                'function': {
                    'name': 'search_code',
                    'description': 'Search for a pattern in code files',
                    'parameters': {
                        'type': 'object',
                        'properties': {
                            'query': {
                                'type': 'string',
                                'description': 'Search term or pattern to find'
                            },
                            'file_pattern': {
                                'type': 'string',
                                'description': 'File pattern to search (e.g., *.py, *.js, *.java). Default: *.py'
                            }
                        },
                        'required': ['query']
                    }
                }
            }
        ]
    
    def execute_tool(self, tool_name: str, arguments: Dict) -> str:
        """
        Execute a tool and return the result.
        
        Args:
            tool_name: Name of the tool to execute
            arguments: Arguments to pass to the tool
            
        Returns:
            Tool execution result
        """
        if tool_name == 'read_file':
            return self.read_file(arguments['filepath'])
        elif tool_name == 'write_file':
            return self.write_file(arguments['filepath'], arguments['content'])
        elif tool_name == 'execute_command':
            return self.execute_command(arguments['command'])
        elif tool_name == 'list_files':
            directory = arguments.get('directory', '.')
            return self.list_files(directory)
        elif tool_name == 'search_code':
            query = arguments['query']
            file_pattern = arguments.get('file_pattern', '*.py')
            return self.search_code(query, file_pattern)
        else:
            return f"Error: Unknown tool '{tool_name}'"
    
    def chat(self, user_message: str, max_iterations: int = 10) -> str:
        """
        Send a message to the assistant and get a response.
        Handles tool calling automatically.
        
        Args:
            user_message: The user's message/request
            max_iterations: Maximum number of tool-calling iterations (default: 10)
            
        Returns:
            The assistant's final response
        """
        # Add user message to conversation
        self.conversation_history.append({
            'role': 'user',
            'content': user_message
        })
        
        # Iteration loop for tool calling
        for iteration in range(max_iterations):
            try:
                # Get response from model
                response = chat(
                    model=self.model,
                    messages=self.conversation_history,
                    tools=self.get_available_tools()
                )
                
                # Add assistant response to history
                self.conversation_history.append(response['message'])
                
                # Check if the model wants to use tools
                if not response['message'].get('tool_calls'):
                    # No tool calls - return the final response
                    return response['message'].get('content', '(No response)')
                
                # Process tool calls
                for tool_call in response['message']['tool_calls']:
                    function_name = tool_call['function']['name']
                    arguments = tool_call['function']['arguments']
                    
                    # Show tool usage to user
                    console.print(
                        f"[yellow]🔧 Using tool:[/yellow] {function_name}",
                        style="bold"
                    )
                    
                    # Execute the tool
                    result = self.execute_tool(function_name, arguments)
                    
                    # Add tool result to conversation
                    self.conversation_history.append({
                        'role': 'tool',
                        'content': result
                    })
                
            except KeyboardInterrupt:
                raise
            except Exception as e:
                error_msg = f"Error during chat: {str(e)}"
                console.print(f"[red]{error_msg}[/red]")
                return error_msg
        
        return "⚠️ Max iterations reached. The task may be too complex or the assistant may need more guidance."
    
    def reset_conversation(self):
        """Clear conversation history."""
        self.conversation_history = []
        console.print("[green]✓ Conversation history cleared[/green]")
    
    def set_working_directory(self, directory: str):
        """
        Change the working directory.
        
        Args:
            directory: New working directory path
        """
        if os.path.exists(directory) and os.path.isdir(directory):
            self.working_directory = os.path.abspath(directory)
            console.print(f"[green]✓ Working directory changed to: {self.working_directory}[/green]")
        else:
            console.print(f"[red]✗ Directory not found: {directory}[/red]")


def main():
    """Main interactive loop."""
    
    # Welcome message
    console.print(Panel.fit(
        "[bold cyan]Qwen Local Code Assistant[/bold cyan]\n"
        "Powered by Qwen3-Coder-Next & Ollama\n\n"
        "[dim]Your privacy-first AI coding companion[/dim]\n\n"
        "Commands:\n"
        "  [yellow]/reset[/yellow]  - Clear conversation history\n"
        "  [yellow]/cd <dir>[/yellow] - Change working directory\n"
        "  [yellow]/pwd[/yellow] - Show current directory\n"
        "  [yellow]/help[/yellow] - Show help message\n"
        "  [yellow]/exit[/yellow] or [yellow]/quit[/yellow] - Exit the assistant",
        title="🤖 Welcome",
        border_style="cyan"
    ))
    
    # Initialize assistant
    try:
        assistant = QwenCodeAssistant()
    except Exception as e:
        console.print(f"[red]Failed to initialize assistant: {e}[/red]")
        return
    
    console.print(f"\n[dim]Working directory: {assistant.working_directory}[/dim]\n")
    
    # Main loop
    while True:
        try:
            # Get user input
            user_input = console.input("\n[bold green]You:[/bold green] ").strip()
            
            # Handle empty input
            if not user_input:
                continue
            
            # Handle commands
            if user_input in ['/exit', '/quit']:
                console.print("\n[yellow]👋 Goodbye! Happy coding![/yellow]")
                break
            
            elif user_input == '/reset':
                assistant.reset_conversation()
                continue
            
            elif user_input == '/pwd':
                console.print(f"[cyan]Current directory:[/cyan] {assistant.working_directory}")
                continue
            
            elif user_input.startswith('/cd '):
                new_dir = user_input[4:].strip()
                assistant.set_working_directory(new_dir)
                continue
            
            elif user_input == '/help':
                console.print(Panel.fit(
                    "[bold]Available Commands:[/bold]\n\n"
                    "  [yellow]/reset[/yellow]     - Clear conversation history\n"
                    "  [yellow]/cd <dir>[/yellow]  - Change working directory\n"
                    "  [yellow]/pwd[/yellow]       - Show current directory\n"
                    "  [yellow]/help[/yellow]      - Show this help message\n"
                    "  [yellow]/exit[/yellow]      - Exit the assistant\n\n"
                    "[bold]What I can do:[/bold]\n\n"
                    "  • Read and write files in your project\n"
                    "  • Execute shell commands (tests, git, etc.)\n"
                    "  • Search and navigate your codebase\n"
                    "  • Debug and explain code\n"
                    "  • Refactor and improve code quality\n"
                    "  • Generate tests and documentation\n"
                    "  • Create new projects and features\n\n"
                    "[bold]Tips:[/bold]\n\n"
                    "  • Be specific in your requests\n"
                    "  • Provide context about your project\n"
                    "  • Work iteratively for complex tasks\n"
                    "  • Use /reset if conversation gets too long",
                    title="Help",
                    border_style="blue"
                ))
                continue
            
            # Regular chat message - get response from assistant
            with console.status("[bold blue]Thinking...", spinner="dots"):
                response = assistant.chat(user_input)
            
            # Display response
            console.print("\n[bold blue]Assistant:[/bold blue]")
            console.print(Markdown(response))
            
        except KeyboardInterrupt:
            console.print("\n[yellow]⚠️  Interrupted. Type /exit to quit or continue chatting.[/yellow]")
            continue
        
        except Exception as e:
            console.print(f"\n[red]Error: {str(e)}[/red]")
            console.print("[dim]Please try again or type /help for assistance.[/dim]")


if __name__ == "__main__":
    main()
