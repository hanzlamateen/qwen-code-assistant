#!/bin/bash

# Qwen Local Code Assistant - Setup Script
# This script automates the installation process

set -e  # Exit on error

echo "=================================="
echo "Qwen Local Code Assistant Setup"
echo "=================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Ollama is installed
echo "Checking for Ollama..."
if ! command -v ollama &> /dev/null; then
    echo -e "${YELLOW}Ollama not found. Installing...${NC}"
    curl -fsSL https://ollama.com/install.sh | sh
    echo -e "${GREEN}✓ Ollama installed${NC}"
else
    echo -e "${GREEN}✓ Ollama is already installed${NC}"
fi

# Check if Ollama is running
echo ""
echo "Checking if Ollama service is running..."
if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo -e "${YELLOW}Starting Ollama service...${NC}"
    ollama serve &
    sleep 3
    echo -e "${GREEN}✓ Ollama service started${NC}"
else
    echo -e "${GREEN}✓ Ollama service is running${NC}"
fi

# Check Python version
echo ""
echo "Checking Python version..."
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}✗ Python 3 is not installed${NC}"
    echo "Please install Python 3.8 or higher from https://python.org"
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo -e "${GREEN}✓ Python $PYTHON_VERSION found${NC}"

# Create virtual environment
echo ""
echo "Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
else
    echo -e "${YELLOW}Virtual environment already exists${NC}"
fi

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source venv/bin/activate
echo -e "${GREEN}✓ Virtual environment activated${NC}"

# Install dependencies
echo ""
echo "Installing Python dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt
echo -e "${GREEN}✓ Dependencies installed${NC}"

# Check available disk space
echo ""
echo "Checking disk space..."
AVAILABLE_SPACE=$(df -h . | awk 'NR==2 {print $4}')
echo "Available disk space: $AVAILABLE_SPACE"

# Ask about model installation
echo ""
echo "=================================="
echo "Model Installation"
echo "=================================="
echo ""
echo "The Qwen3-Coder-Next model requires:"
echo "  - 48GB download"
echo "  - 46GB RAM minimum"
echo "  - 10-30 minutes download time"
echo ""
read -p "Do you want to download the model now? (y/n) " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "Downloading Qwen3-Coder-Next model..."
    echo "This will take 10-30 minutes depending on your internet speed..."
    ollama pull qwen3-coder-next:q4_K_M
    echo -e "${GREEN}✓ Model downloaded successfully${NC}"
else
    echo -e "${YELLOW}⚠ Skipping model download${NC}"
    echo "You can download it later with: ollama pull qwen3-coder-next:q4_K_M"
fi

# Make assistant executable
echo ""
echo "Making assistant executable..."
chmod +x assistant.py
echo -e "${GREEN}✓ Assistant is executable${NC}"

# Setup complete
echo ""
echo "=================================="
echo -e "${GREEN}✓ Setup Complete!${NC}"
echo "=================================="
echo ""
echo "To start using the assistant:"
echo ""
echo "  1. Activate the virtual environment:"
echo "     source venv/bin/activate"
echo ""
echo "  2. Run the assistant:"
echo "     python assistant.py"
echo ""
echo "Or simply run:"
echo "  ./assistant.py"
echo ""
echo "For help, type /help in the assistant"
echo ""
echo "Documentation:"
echo "  - README.md - Quick start guide"
echo "  - docs/architecture.md - System architecture"
echo "  - docs/advanced-usage.md - Advanced features"
echo "  - examples/ - Usage examples"
echo ""
echo "Happy coding! 🚀"
