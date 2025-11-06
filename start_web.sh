#!/bin/bash

# Launch Streamlit Web Interface

echo "🚀 Starting Document Reader Web Interface..."
echo "============================================"
echo ""
echo "📘 Document Reader MVP will open in your browser"
echo "🌐 URL: http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

cd /home/zayan/Documents/pythonProject/doc-reader
source venv/bin/activate
streamlit run streamlit_app.py
