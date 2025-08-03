#!/bin/bash

# Curriculum Architect Setup Script
echo "🚀 Setting up Curriculum Architect..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Create environment files
echo "📝 Creating environment files..."

# Backend environment
if [ ! -f backend/.env ]; then
    cp backend/env.example backend/.env
    echo "✅ Created backend/.env"
else
    echo "⚠️  backend/.env already exists"
fi

# Frontend environment
if [ ! -f frontend/.env.local ]; then
    cp frontend/env.example frontend/.env.local
    echo "✅ Created frontend/.env.local"
else
    echo "⚠️  frontend/.env.local already exists"
fi

# Install frontend dependencies
echo "📦 Installing frontend dependencies..."
cd frontend
npm install
cd ..

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p backend/logs
mkdir -p frontend/.next

# Set up database
echo "🗄️  Setting up database..."
docker-compose up -d postgres
echo "⏳ Waiting for database to be ready..."
sleep 10

# Run database migrations (if using Alembic)
echo "🔄 Running database migrations..."
cd backend
# Uncomment when Alembic is set up
# alembic upgrade head
cd ..

# Start all services
echo "🚀 Starting all services..."
docker-compose up -d

echo ""
echo "🎉 Setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Update environment variables in backend/.env and frontend/.env.local"
echo "2. Add your OpenAI API key to backend/.env"
echo "3. Configure SendGrid and Firebase credentials if needed"
echo ""
echo "🌐 Access the application:"
echo "   Frontend: http://localhost:3000"
echo "   Backend API: http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"
echo ""
echo "📚 For more information, see README.md" 