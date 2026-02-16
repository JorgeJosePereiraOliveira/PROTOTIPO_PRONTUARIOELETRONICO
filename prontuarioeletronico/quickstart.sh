#!/bin/bash
# Quick Start Guide - Prontuário Eletrônico

echo "================================================"
echo "Prontuário Eletrônico - Quick Start"
echo "================================================"
echo ""

# Check Python version
echo "Checking Python installation..."
python --version

# Create virtual environment
echo ""
echo "Creating virtual environment..."
python -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install -r requirements.txt

# Run tests
echo ""
echo "Running tests..."
python -m pytest tests.py -v

# Start development server
echo ""
echo "Starting development server..."
echo "API will be available at: http://localhost:8000"
echo "Swagger UI at: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python -m uvicorn src.infra.api.main:app --reload --host 0.0.0.0 --port 8000
