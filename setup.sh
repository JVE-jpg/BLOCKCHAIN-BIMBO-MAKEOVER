#!/bin/bash

echo "🎨 Blockchain Bimbo Makeover - Setup Script"
echo "============================================"
echo "NOTE: This script is for macOS/Linux only."
echo "Windows users: Run the commands in setup_windows.bat"
echo ""

# Check Python version
echo "Checking Python version..."
python3 --version

if [ $? -ne 0 ]; then
    echo "❌ Python 3 not found. Please install Python 3.8 or higher."
    echo ""
    echo "Installation instructions:"
    echo "  macOS: brew install python3"
    echo "  Linux: sudo apt install python3 python3-pip"
    exit 1
fi

echo "✅ Python 3 found"
echo ""

# Install dependencies
echo "Installing Python dependencies..."
pip3 install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    echo ""
    echo "Try manually:"
    echo "  pip3 install -r requirements.txt"
    exit 1
fi

echo "✅ Dependencies installed"
echo ""

# Create .env if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "✅ .env file created"
    echo ""
    echo "⚠️  IMPORTANT: Edit the .env file and fill in your credentials:"
    echo ""
    echo "Required variables:"
    echo "  • ETH_PRIVATE_KEY        (66 chars, starts with 0x)"
    echo "  • ZORA_CONTRACT_ADDRESS  (42 chars, starts with 0x)"
    echo "  • WATCH_FOLDERS          (absolute paths)"
    echo ""
    echo "Edit now? Run:"
    echo "  nano .env    (or your preferred editor)"
    echo ""
else
    echo "✅ .env file already exists"
    echo ""
fi

echo "============================================"
echo "✨ Setup complete!"
echo "============================================"
echo ""
echo "Next steps:"
echo ""
echo "1. Edit your configuration:"
echo "   nano .env"
echo ""
echo "2. Fund your wallet:"
echo "   • USDC/ETH for Arweave uploads"
echo "   • ETH on ZORA chain (bridge at: bridge.zora.energy)"
echo ""
echo "3. Run the application:"
echo "   python3 blockchain_bimbo.py"
echo ""
echo "The script will validate your config and show clear errors"
echo "if anything is missing or incorrect."
echo ""

