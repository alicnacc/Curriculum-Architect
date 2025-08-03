# Curriculum Architect API Documentation

## Overview

The Curriculum Architect API is a RESTful service built with FastAPI that provides endpoints for user authentication, curriculum management, progress tracking, and AI-powered learning features.

## Base URL

```
http://localhost:8000/api/v1
```

## Authentication

The API uses JWT (JSON Web Tokens) for authentication. Include the token in the Authorization header:

```
Authorization: Bearer <your-jwt-token>
```

## Endpoints

### Authentication

#### POST /users/register
Register a new user.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Response:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "created_at": "2024-01-01T00:00:00Z"
}
```

#### POST /users/login
Authenticate a user and receive a JWT token.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

#### GET /users/me
Get current user information.

**Headers:**
```
Authorization: Bearer <jwt-token>
```

**Response:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "created_at": "2024-01-01T00:00:00Z"
}
```

### User Profile

#### PUT /users/me/profile
Update user learning profile.

**Headers:**
```
Authorization: Bearer <jwt-token>
```

**Request Body:**
```json
{
  "learning_style": "visual",
  "pace": "moderate",
  "interests": ["machine learning", "data science"],
  "goals": ["Learn Python", "Build ML models"]
}
```

**Response:**
```json
{
  "id": 1,
  "user_id": 1,
  "learning_style": "visual",
  "pace": "moderate",
  "interests": ["machine learning", "data science"],
  "goals": ["Learn Python", "Build ML models"],
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

#### GET /users/me/profile
Get current user's learning profile.

**Headers:**
```
Authorization: Bearer <jwt-token>
```

**Response:**
```json
{
  "id": 1,
  "user_id": 1,
  "learning_style": "visual",
  "pace": "moderate",
  "interests": ["machine learning", "data science"],
  "goals": ["Learn Python", "Build ML models"],
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

### Curriculum Management

#### POST /curriculum/generate
Generate a new personalized curriculum using AI.

**Headers:**
```
Authorization: Bearer <jwt-token>
```

**Request Body:**
```json
{
  "title": "Machine Learning Fundamentals",
  "description": "Learn the basics of machine learning and data science"
}
```

**Response:**
```json
{
  "id": 1,
  "user_id": 1,
  "title": "Machine Learning Fundamentals",
  "description": "Learn the basics of machine learning and data science",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": null
}
```

#### GET /curriculum/
Get all curriculums for the current user.

**Headers:**
```
Authorization: Bearer <jwt-token>
```

**Response:**
```json
[
  {
    "id": 1,
    "user_id": 1,
    "title": "Machine Learning Fundamentals",
    "description": "Learn the basics of machine learning and data science",
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": null
  }
]
```

#### GET /curriculum/{curriculum_id}
Get a specific curriculum with all modules and resources.

**Headers:**
```
Authorization: Bearer <jwt-token>
```

**Response:**
```json
{
  "id": 1,
  "user_id": 1,
  "title": "Machine Learning Fundamentals",
  "description": "Learn the basics of machine learning and data science",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": null,
  "modules": [
    {
      "id": 1,
      "curriculum_id": 1,
      "title": "Introduction to Python",
      "description": "Learn Python basics for data science",
      "order": 1,
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": null,
      "resources": [
        {
          "id": 1,
          "module_id": 1,
          "title": "Python Basics Tutorial",
          "description": "Comprehensive Python tutorial for beginners",
          "url": "https://example.com/python-basics",
          "resource_type": "video",
          "status": "pending",
          "order": 1,
          "created_at": "2024-01-01T00:00:00Z",
          "updated_at": null
        }
      ]
    }
  ]
}
```

#### DELETE /curriculum/{curriculum_id}
Delete a curriculum.

**Headers:**
```
Authorization: Bearer <jwt-token>
```

**Response:**
```json
{
  "message": "Curriculum deleted successfully"
}
```

### Progress Tracking

#### POST /progress/update
Update the progress of a learning resource.

**Headers:**
```
Authorization: Bearer <jwt-token>
```

**Request Body:**
```json
{
  "resource_id": 1,
  "status": "completed"
}
```

**Response:**
```json
{
  "message": "Progress updated successfully"
}
```

#### GET /progress/summary
Get a summary of the user's learning progress.

**Headers:**
```
Authorization: Bearer <jwt-token>
```

**Response:**
```json
{
  "total_resources": 10,
  "completed_resources": 3,
  "in_progress_resources": 2,
  "pending_resources": 5,
  "completion_percentage": 30.0,
  "learning_style": "visual",
  "pace": "moderate"
}
```

### AI Agent Chat

#### POST /agent/chat
Chat with the AI learning companion.

**Headers:**
```
Authorization: Bearer <jwt-token>
```

**Request Body:**
```json
{
  "message": "I need help understanding machine learning basics",
  "curriculum_id": 1
}
```

**Response:**
```json
{
  "response": "I'll help you understand machine learning basics! Let me create a personalized learning path starting with fundamental concepts..."
}
```

#### WebSocket /agent/ws/{user_id}
Real-time chat with the AI agent via WebSocket.

**Connection:**
```
ws://localhost:8000/api/v1/agent/ws/1
```

**Message Format:**
```json
{
  "message": "Hello, I need help with my learning",
  "curriculum_id": 1
}
```

**Response Format:**
```json
{
  "response": "Hello! I'm here to help you with your learning journey..."
}
```

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Email already registered"
}
```

### 401 Unauthorized
```json
{
  "detail": "Invalid authentication credentials"
}
```

### 404 Not Found
```json
{
  "detail": "Curriculum not found"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Failed to generate curriculum: OpenAI API error"
}
```

## Data Models

### User
```json
{
  "id": 1,
  "email": "user@example.com",
  "created_at": "2024-01-01T00:00:00Z"
}
```

### UserProfile
```json
{
  "id": 1,
  "user_id": 1,
  "learning_style": "visual",
  "pace": "moderate",
  "interests": ["machine learning", "data science"],
  "goals": ["Learn Python", "Build ML models"],
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

### Curriculum
```json
{
  "id": 1,
  "user_id": 1,
  "title": "Machine Learning Fundamentals",
  "description": "Learn the basics of machine learning and data science",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": null
}
```

### CurriculumModule
```json
{
  "id": 1,
  "curriculum_id": 1,
  "title": "Introduction to Python",
  "description": "Learn Python basics for data science",
  "order": 1,
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": null
}
```

### LearningResource
```json
{
  "id": 1,
  "module_id": 1,
  "title": "Python Basics Tutorial",
  "description": "Comprehensive Python tutorial for beginners",
  "url": "https://example.com/python-basics",
  "resource_type": "video",
  "status": "pending",
  "order": 1,
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": null
}
```

## Environment Variables

### Required
- `DATABASE_URL`: PostgreSQL connection string
- `SECRET_KEY`: JWT secret key
- `OPENAI_API_KEY`: OpenAI API key for AI features
- `WEAVIATE_URL`: Weaviate vector database URL

### Optional
- `SENDGRID_API_KEY`: For email notifications
- `FIREBASE_CREDENTIALS`: For push notifications
- `REDIS_URL`: For background tasks

## Rate Limiting

The API implements rate limiting to prevent abuse:
- 100 requests per minute per user
- 1000 requests per hour per user

## WebSocket Events

### Connection
```javascript
const ws = new WebSocket('ws://localhost:8000/api/v1/agent/ws/1');
```

### Send Message
```javascript
ws.send(JSON.stringify({
  message: "Hello, I need help",
  curriculum_id: 1
}));
```

### Receive Message
```javascript
ws.onmessage = function(event) {
  const data = JSON.parse(event.data);
  console.log(data.response);
};
```

## Testing

You can test the API using the interactive documentation at:
```
http://localhost:8000/docs
```

Or using curl:

```bash
# Register a user
curl -X POST "http://localhost:8000/api/v1/users/register" \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "password123"}'

# Login
curl -X POST "http://localhost:8000/api/v1/users/login" \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "password123"}'

# Use the token for authenticated requests
curl -X GET "http://localhost:8000/api/v1/users/me" \
  -H "Authorization: Bearer <your-token>"
``` 