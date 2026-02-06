#!/bin/bash

echo "=========================================="
echo "Financial Health Assessment Tool"
echo "Starting Application..."
echo "=========================================="

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found!"
    echo "Creating .env from .env.example..."
    cp .env.example .env
    echo "✅ .env file created"
    echo ""
    echo "⚠️  IMPORTANT: Please edit .env and add your API keys:"
    echo "   - GEMINI_API_KEY (Get from: https://aistudio.google.com/apikey)"
    echo "   - JWT_SECRET_KEY (Generate: openssl rand -hex 32)"
    echo "   - ENCRYPTION_KEY (Generate with Python)"
    echo "   - AES_ENCRYPTION_KEY (Generate: openssl rand -hex 32)"
    echo ""
    read -p "Press Enter after updating .env file..."
fi

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker Desktop first."
    exit 1
fi

echo "🐳 Starting Docker containers..."
docker-compose up --build -d

echo ""
echo "=========================================="
echo "✅ Application Started!"
echo "=========================================="
echo ""
echo "📍 Access Points:"
echo "   Frontend:  http://localhost:3000"
echo "   Backend:   http://localhost:8000"
echo "   API Docs:  http://localhost:8000/docs"
echo "   Database:  localhost:5432"
echo ""
echo "📊 View Logs:"
echo "   All:       docker-compose logs -f"
echo "   Backend:   docker-compose logs -f backend"
echo "   Frontend:  docker-compose logs -f frontend"
echo ""
echo "🛑 Stop Application:"
echo "   docker-compose down"
echo ""
echo "=========================================="
