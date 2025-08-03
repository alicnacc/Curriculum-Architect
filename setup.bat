@echo off
echo 🚀 Setting up Curriculum Architect...

REM Check if Docker is installed
docker --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker is not installed. Please install Docker Desktop first.
    pause
    exit /b 1
)

REM Check if Docker Compose is installed
docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker Compose is not installed. Please install Docker Compose first.
    pause
    exit /b 1
)

echo 📝 Creating environment files...

REM Backend environment
if not exist "backend\.env" (
    copy "backend\env.example" "backend\.env"
    echo ✅ Created backend\.env
) else (
    echo ⚠️  backend\.env already exists
)

REM Frontend environment
if not exist "frontend\.env.local" (
    copy "frontend\env.example" "frontend\.env.local"
    echo ✅ Created frontend\.env.local
) else (
    echo ⚠️  frontend\.env.local already exists
)

echo 📦 Installing frontend dependencies...
cd frontend
call npm install
cd ..

echo 📁 Creating necessary directories...
if not exist "backend\logs" mkdir "backend\logs"
if not exist "frontend\.next" mkdir "frontend\.next"

echo 🗄️  Setting up database...
docker-compose up -d postgres
echo ⏳ Waiting for database to be ready...
timeout /t 10 /nobreak >nul

echo 🚀 Starting all services...
docker-compose up -d

echo.
echo 🎉 Setup complete!
echo.
echo 📋 Next steps:
echo 1. Update environment variables in backend\.env and frontend\.env.local
echo 2. Add your OpenAI API key to backend\.env
echo 3. Configure SendGrid and Firebase credentials if needed
echo.
echo 🌐 Access the application:
echo    Frontend: http://localhost:3000
echo    Backend API: http://localhost:8000
echo    API Docs: http://localhost:8000/docs
echo.
echo 📚 For more information, see README.md
pause 