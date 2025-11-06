#!/bin/bash

# Document Reader MVP - Quick Start Script

echo "📘 Document Reader MVP - Quick Start"
echo "===================================="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Please run: python3 -m venv venv"
    exit 1
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Check if dependencies are installed
if ! python -c "import nltk, streamlit" 2>/dev/null; then
    echo "📦 Installing dependencies..."
    pip install -r requirements.txt
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "Choose an interface:"
echo "1. CLI (Command Line)"
echo "2. Web (Streamlit)"
echo ""

read -p "Enter choice (1 or 2): " choice

case $choice in
    1)
        echo "🚀 Starting CLI interface..."
        python cli.py
        ;;
    2)
        echo "🚀 Starting web interface..."
        echo "   Opening browser to http://localhost:8501"
        streamlit run streamlit_app.py
        ;;
    *)
        echo "❌ Invalid choice. Run the script again."
        ;;
esac
