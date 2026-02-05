# Qwen Local Code Assistant

A powerful, privacy-first local coding assistant powered by Qwen3-Coder-Next and Ollama. Get Claude Code-like capabilities running entirely on your machine!

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Ollama](https://img.shields.io/badge/Ollama-0.15.5+-green.svg)](https://ollama.com)

## 🌟 Features

- 📂 **Full Codebase Understanding** - 256K token context window
- 💻 **Multi-File Editing** - Modify multiple files in a single conversation
- 🔍 **Smart Code Search** - Find and navigate complex projects
- 🐛 **Debugging Assistant** - Analyze and fix bugs
- 🧪 **Test Generation** - Create comprehensive test suites
- 📝 **Documentation** - Generate docstrings and READMEs
- 🔐 **100% Private** - Your code never leaves your machine
- 💰 **Zero Cost** - No subscriptions or API fees

## 🎥 Demo

![Demo](https://via.placeholder.com/800x400.png?text=Demo+Screenshot)

*Example: Creating a FastAPI project with a single command*

## 🚀 Quick Start

### Prerequisites

- **RAM:** 46GB minimum (64GB recommended)
- **Disk Space:** 60GB free
- **OS:** macOS, Linux, or Windows
- **Python:** 3.8+

### Installation

```bash
# 1. Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# 2. Pull the model (takes 10-30 minutes)
ollama pull qwen3-coder-next:q4_K_M

# 3. Clone this repository
git clone https://github.com/yourusername/qwen-code-assistant
cd qwen-code-assistant

# 4. Set up Python environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 5. Install dependencies
pip install -r requirements.txt

# 6. Run the assistant!
python assistant.py
```

## 📖 Usage

### Basic Usage

```bash
python assistant.py
```

### Example Interactions

**Create a new project:**
```
You: Create a FastAPI project with user authentication, including database models, API endpoints, and tests.
```

**Debug code:**
```
You: I'm getting a KeyError in this function. Can you help me debug it?
[paste code or provide filepath]
```

**Refactor code:**
```
You: Refactor app/services/user.py to follow SOLID principles and add type hints.
```

**Generate tests:**
```
You: Create pytest tests for the authentication module with at least 80% coverage.
```

### Available Commands

| Command | Description |
|---------|-------------|
| `/reset` | Clear conversation history |
| `/cd <dir>` | Change working directory |
| `/pwd` | Show current directory |
| `/help` | Show help message |
| `/exit` or `/quit` | Exit the assistant |

## 🛠️ Available Tools

The assistant has access to these tools:

| Tool | Description |
|------|-------------|
| `read_file` | Read file contents |
| `write_file` | Create or update files |
| `execute_command` | Run shell commands |
| `list_files` | Browse directories |
| `search_code` | Search for patterns in code |

## 📁 Project Structure

```
qwen-code-assistant/
├── assistant.py           # Main assistant code
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── examples/             # Usage examples
│   ├── create_project.md
│   ├── debugging.md
│   └── refactoring.md
└── docs/                 # Additional documentation
    ├── architecture.md
    └── advanced-usage.md
```

## 💡 Tips for Best Results

### 1. Be Specific

❌ **Vague:** "Make a website"  
✅ **Specific:** "Create a React component for a user profile card with avatar, name, email, and a follow button"

### 2. Provide Context

✅ "Using the FastAPI project in ./backend, add a new endpoint for user registration with email validation"

### 3. Work Iteratively

```
You: Create a user model
[Review the output]
You: Add email validation
[Review again]
You: Add password hashing
```

### 4. Use Project Instructions

Create a `QWEN.md` file in your project root:

```markdown
# Project: MyApp

## Tech Stack
- FastAPI backend
- PostgreSQL database
- React frontend

## Code Style
- Use Black for formatting
- Type hints required
- Minimum 80% test coverage
```

Then reference it:
```
You: Read QWEN.md before making changes to the authentication system.
```

## ⚙️ Configuration

### Change Model

Edit `assistant.py` or pass as argument:

```python
# Use higher quality model (needs 85GB RAM)
assistant = QwenCodeAssistant(model="qwen3-coder-next:q8_0")

# Use faster, smaller model (needs ~8GB RAM)
assistant = QwenCodeAssistant(model="qwen3-coder:7b")
```

### Model Variants

| Variant | Size | RAM Needed | Speed | Quality |
|---------|------|------------|-------|---------|
| `q4_K_M` | 48GB | 46GB | ⚡⚡⚡ | ⭐⭐⭐ |
| `latest` | 52GB | 52GB | ⚡⚡ | ⭐⭐⭐⭐ |
| `q8_0` | 85GB | 85GB | ⚡ | ⭐⭐⭐⭐⭐ |

### Adjust Memory Usage

Limit conversation history in `assistant.py`:

```python
def __init__(self, model: str = "qwen3-coder-next:q4_K_M"):
    self.model = model
    self.conversation_history: List[Dict] = []
    self.max_history = 20  # Keep only last 20 messages
```

## 🔧 Troubleshooting

### Model Not Found
```bash
ollama list  # Check installed models
ollama pull qwen3-coder-next:q4_K_M  # Pull if missing
```

### Out of Memory
```bash
# Use smaller model
ollama pull qwen3-coder:7b
```

### Ollama Not Running
```bash
# Start Ollama service
ollama serve
```

### Slow Performance
```bash
# Preload model
ollama run qwen3-coder-next:q4_K_M "Ready" --keepalive 24h
```

## 📊 Performance

### Typical Resource Usage

```
RAM:     46 GB / 64 GB  (72%)
CPU:     30-40% (during inference)
Disk:    ~52 GB
Network: 0 (fully offline)
```

### Response Times

- **First response:** 2-5 seconds (model loading)
- **Subsequent:** 10-30 tokens/second
- **Tool execution:** Varies by operation

## 🆚 Comparison

| Feature | Qwen Local | Claude Code | GitHub Copilot |
|---------|-----------|-------------|----------------|
| **Cost** | Free | $20-30/mo | $10/mo |
| **Privacy** | 100% Local | Cloud | Cloud |
| **Offline** | ✅ Yes | ❌ No | ❌ No |
| **Context** | 256K | ~200K | Limited |
| **Tools** | ✅ Yes | ✅ Yes | ❌ No |
| **Customizable** | ✅ Yes | Limited | ❌ No |

## 📚 Examples

### Example 1: Create FastAPI Project

```
You: Create a complete FastAPI project with:
- User registration and login
- JWT authentication
- SQLAlchemy models
- Pydantic schemas
- Proper project structure
- Tests
```

**Result:** Complete project structure with all files created.

See [examples/create_project.md](examples/create_project.md) for full example.

### Example 2: Debug Code

```
You: This function throws a KeyError. Can you fix it?

def get_user_email(users, user_id):
    return users[user_id]['email']
```

**Result:** Fixed code with error handling and explanation.

See [examples/debugging.md](examples/debugging.md) for full example.

### Example 3: Refactor Code

```
You: Refactor this monolithic function to follow SOLID principles.
[paste code]
```

**Result:** Clean, modular code with separated concerns.

See [examples/refactoring.md](examples/refactoring.md) for full example.

## 🔒 Security

- ✅ All operations are local - no cloud API calls
- ✅ Dangerous commands are blocked (rm -rf /, etc.)
- ✅ File operations limited to working directory
- ✅ No automatic code execution
- ⚠️ Review generated code before committing
- ⚠️ Use version control for safety

## 🤝 Contributing

Contributions are welcome! Please feel free to:

- 🐛 Report bugs
- 💡 Suggest features
- 🔧 Submit pull requests
- 📖 Improve documentation

### Development Setup

```bash
git clone https://github.com/yourusername/qwen-code-assistant
cd qwen-code-assistant
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

## 🙏 Acknowledgments

- **Alibaba Qwen Team** - For the amazing Qwen3-Coder-Next model
- **Ollama** - For making local LLMs accessible
- **The Open Source Community** - For continuous improvements

## 📚 Resources

- [Full Tutorial Article](https://medium.com/@yourusername/build-local-claude-code)
- [Ollama Documentation](https://ollama.com)
- [Qwen3-Coder-Next Model Card](https://huggingface.co/Qwen/Qwen3-Coder-Next)
- [Architecture Documentation](docs/architecture.md)
- [Advanced Usage Guide](docs/advanced-usage.md)

## 💬 Support

- **Issues:** [GitHub Issues](https://github.com/yourusername/qwen-code-assistant/issues)
- **Discussions:** [GitHub Discussions](https://github.com/yourusername/qwen-code-assistant/discussions)
- **Community:** [Ollama Discord](https://discord.gg/ollama)

## 🗺️ Roadmap

- [ ] Streaming responses
- [ ] Web UI interface
- [ ] VS Code extension
- [ ] Git integration
- [ ] Project templates
- [ ] Multi-language support
- [ ] Conversation persistence
- [ ] Code metrics dashboard

---

**Built with ❤️ for developers who value privacy and control**

⭐ Star this repo if you find it useful!

---

## Quick Links

- [Installation](#installation)
- [Usage](#usage)
- [Examples](examples/)
- [Documentation](docs/)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
