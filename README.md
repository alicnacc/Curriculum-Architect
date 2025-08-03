# Curriculum Architect

An AI-powered, multi-platform learning companion that creates personalized educational journeys for students.

## Features

- **Personalized Curriculum Generation**: AI-driven curriculum creation based on learning goals, style, and pace
- **Agentic AI Collaboration**: Intelligent agent that curates resources and adapts learning paths
- **Multi-Platform Delivery**: Email digests and push notifications for continuous learning
- **Real-time Progress Tracking**: Monitor and adjust learning progress dynamically
- **Modern Web Interface**: Clean, responsive UI built with Next.js and React

## Technology Stack

### Backend
- **Framework**: FastAPI (Python)
- **AI/LLM**: LangChain + LangGraph
- **Database**: PostgreSQL
- **Vector Database**: Weaviate
- **Multi-Platform**: langchain-mcp-adapters

### Frontend
- **Framework**: Next.js with React
- **Styling**: Tailwind CSS
- **State Management**: React Context + Redux Toolkit
- **Authentication**: JWT

## Project Structure

```
curriculum-architect/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/            # API endpoints
│   │   ├── core/           # Configuration and utilities
│   │   ├── models/         # Database models
│   │   ├── services/       # Business logic
│   │   └── agents/         # LangChain agents
│   ├── requirements.txt
│   └── main.py
├── frontend/               # Next.js frontend
│   ├── components/         # React components
│   ├── pages/             # Next.js pages
│   ├── hooks/             # Custom React hooks
│   ├── store/             # Redux store
│   └── styles/            # CSS styles
├── docker-compose.yml      # Development environment
└── README.md
```

## Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- Docker and Docker Compose
- PostgreSQL
- Weaviate

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Run database migrations:
```bash
alembic upgrade head
```

6. Start the backend server:
```bash
uvicorn main:app --reload
```

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Set up environment variables:
```bash
cp .env.example .env.local
# Edit .env.local with your configuration
```

4. Start the development server:
```bash
npm run dev
```

### Using Docker Compose

For a complete development environment:

```bash
docker-compose up -d
```

This will start:
- PostgreSQL database
- Weaviate vector database
- Backend API server
- Frontend development server

## API Documentation

Once the backend is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Environment Variables

### Backend (.env)
```
DATABASE_URL=postgresql://user:password@localhost:5432/curriculum_architect
WEAVIATE_URL=http://localhost:8080
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
OPENAI_API_KEY=your-openai-api-key
SENDGRID_API_KEY=your-sendgrid-api-key
FIREBASE_CREDENTIALS=path/to/firebase-credentials.json
```

### Frontend (.env.local)
```
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_WEBSOCKET_URL=ws://localhost:8000/ws
```

## Features in Detail

### 1. Personalized Curriculum Generation
- Input learning goals, current knowledge, and preferences
- AI generates structured curriculum with diverse resources
- Real-time adaptation based on progress and feedback

### 2. Agentic AI Collaboration
- LangGraph-based stateful agent
- Web search for fresh content
- Vector search for personalized recommendations
- Continuous monitoring and adaptation

### 3. Multi-Platform Delivery
- **Email**: Weekly progress digests via SendGrid
- **Push Notifications**: Daily learning prompts via Firebase

### 4. User Experience
- Clean, modern interface
- Responsive design
- Real-time chat with AI agent
- Progress visualization
- Interactive curriculum timeline

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT License - see LICENSE file for details. 