# Curriculum Architect Deployment Guide

This guide covers deploying the Curriculum Architect application to various cloud platforms.

## Prerequisites

- Docker and Docker Compose installed
- Git repository access
- Cloud platform accounts (Vercel, Render, etc.)
- API keys for required services

## Local Development Setup

### 1. Clone and Setup

```bash
git clone <repository-url>
cd curriculum-architect
```

### 2. Environment Configuration

Copy and configure environment files:

```bash
# Backend
cp backend/env.example backend/.env
# Edit backend/.env with your configuration

# Frontend
cp frontend/env.example frontend/.env.local
# Edit frontend/.env.local with your configuration
```

### 3. Required Environment Variables

#### Backend (.env)
```bash
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/curriculum_architect

# Security
SECRET_KEY=your-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# AI/LLM
OPENAI_API_KEY=your-openai-api-key

# Vector Database
WEAVIATE_URL=http://localhost:8080

# Email Service (Optional)
SENDGRID_API_KEY=your-sendgrid-api-key
FROM_EMAIL=noreply@curriculumarchitect.com

# Firebase (Optional)
FIREBASE_CREDENTIALS=path/to/firebase-credentials.json

# Redis (Optional)
REDIS_URL=redis://localhost:6379
```

#### Frontend (.env.local)
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_WEBSOCKET_URL=ws://localhost:8000/ws
```

### 4. Start Development Environment

```bash
# Using Docker Compose (Recommended)
docker-compose up -d

# Or start services individually
docker-compose up -d postgres weaviate redis
cd backend && uvicorn main:app --reload
cd frontend && npm run dev
```

## Production Deployment

### Option 1: Docker Compose (Self-Hosted)

#### 1. Prepare Production Environment

```bash
# Create production environment files
cp backend/env.example backend/.env.prod
cp frontend/env.example frontend/.env.prod

# Update with production values
# - Use production database URLs
# - Set strong SECRET_KEY
# - Configure production API keys
```

#### 2. Build and Deploy

```bash
# Build production images
docker-compose -f docker-compose.prod.yml build

# Deploy
docker-compose -f docker-compose.prod.yml up -d
```

#### 3. Production Docker Compose

Create `docker-compose.prod.yml`:

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: curriculum_architect
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - app_network

  weaviate:
    image: semitechnologies/weaviate:1.22.4
    environment:
      QUERY_DEFAULTS_LIMIT: 25
      AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED: 'true'
      PERSISTENCE_DATA_PATH: '/var/lib/weaviate'
      DEFAULT_VECTORIZER_MODULE: 'text2vec-openai'
      ENABLE_MODULES: 'text2vec-openai'
      CLUSTER_HOSTNAME: 'node1'
      OPENAI_APIKEY: ${OPENAI_API_KEY}
    volumes:
      - weaviate_data:/var/lib/weaviate
    networks:
      - app_network

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data
    networks:
      - app_network

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile.prod
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - WEAVIATE_URL=http://weaviate:8080
      - REDIS_URL=redis://redis:6379
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - SECRET_KEY=${SECRET_KEY}
    depends_on:
      - postgres
      - weaviate
      - redis
    networks:
      - app_network
    restart: unless-stopped

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile.prod
    environment:
      - NEXT_PUBLIC_API_URL=${NEXT_PUBLIC_API_URL}
      - NEXT_PUBLIC_WEBSOCKET_URL=${NEXT_PUBLIC_WEBSOCKET_URL}
    depends_on:
      - backend
    networks:
      - app_network
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - frontend
      - backend
    networks:
      - app_network
    restart: unless-stopped

volumes:
  postgres_data:
  weaviate_data:
  redis_data:

networks:
  app_network:
    driver: bridge
```

### Option 2: Cloud Platform Deployment

#### Vercel (Frontend)

1. **Connect Repository**
   ```bash
   # Install Vercel CLI
   npm i -g vercel

   # Deploy frontend
   cd frontend
   vercel --prod
   ```

2. **Environment Variables**
   - Set `NEXT_PUBLIC_API_URL` to your backend URL
   - Set `NEXT_PUBLIC_WEBSOCKET_URL` to your WebSocket URL

#### Render (Backend)

1. **Create New Web Service**
   - Connect your Git repository
   - Set build command: `pip install -r requirements.txt`
   - Set start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

2. **Environment Variables**
   ```bash
   DATABASE_URL=postgresql://user:password@host:5432/db
   SECRET_KEY=your-production-secret-key
   OPENAI_API_KEY=your-openai-api-key
   WEAVIATE_URL=https://your-weaviate-instance.com
   ```

#### Railway (Full Stack)

1. **Deploy Backend**
   ```bash
   # Install Railway CLI
   npm i -g @railway/cli

   # Deploy backend
   cd backend
   railway login
   railway init
   railway up
   ```

2. **Deploy Frontend**
   ```bash
   cd frontend
   railway init
   railway up
   ```

### Option 3: Kubernetes Deployment

#### 1. Create Kubernetes Manifests

```yaml
# k8s/namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: curriculum-architect

---
# k8s/postgres.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: postgres
  namespace: curriculum-architect
spec:
  replicas: 1
  selector:
    matchLabels:
      app: postgres
  template:
    metadata:
      labels:
        app: postgres
    spec:
      containers:
      - name: postgres
        image: postgres:15
        env:
        - name: POSTGRES_DB
          value: curriculum_architect
        - name: POSTGRES_USER
          valueFrom:
            secretKeyRef:
              name: db-secret
              key: username
        - name: POSTGRES_PASSWORD
          valueFrom:
            secretKeyRef:
              name: db-secret
              key: password
        ports:
        - containerPort: 5432
        volumeMounts:
        - name: postgres-storage
          mountPath: /var/lib/postgresql/data
      volumes:
      - name: postgres-storage
        persistentVolumeClaim:
          claimName: postgres-pvc

---
# k8s/backend.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend
  namespace: curriculum-architect
spec:
  replicas: 3
  selector:
    matchLabels:
      app: backend
  template:
    metadata:
      labels:
        app: backend
    spec:
      containers:
      - name: backend
        image: curriculum-architect-backend:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: app-secret
              key: database-url
        - name: SECRET_KEY
          valueFrom:
            secretKeyRef:
              name: app-secret
              key: secret-key
        - name: OPENAI_API_KEY
          valueFrom:
            secretKeyRef:
              name: app-secret
              key: openai-api-key
```

#### 2. Deploy to Kubernetes

```bash
# Create namespace
kubectl apply -f k8s/namespace.yaml

# Create secrets
kubectl create secret generic db-secret \
  --from-literal=username=user \
  --from-literal=password=password \
  -n curriculum-architect

kubectl create secret generic app-secret \
  --from-literal=database-url=postgresql://user:password@postgres:5432/curriculum_architect \
  --from-literal=secret-key=your-secret-key \
  --from-literal=openai-api-key=your-openai-api-key \
  -n curriculum-architect

# Deploy services
kubectl apply -f k8s/
```

## Database Setup

### PostgreSQL

1. **Create Database**
   ```sql
   CREATE DATABASE curriculum_architect;
   CREATE USER curriculum_user WITH PASSWORD 'secure_password';
   GRANT ALL PRIVILEGES ON DATABASE curriculum_architect TO curriculum_user;
   ```

2. **Run Migrations**
   ```bash
   cd backend
   alembic upgrade head
   ```

### Weaviate

1. **Deploy Weaviate**
   ```bash
   # Using Docker
   docker run -d \
     --name weaviate \
     -p 8080:8080 \
     -e QUERY_DEFAULTS_LIMIT=25 \
     -e AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED=true \
     -e PERSISTENCE_DATA_PATH=/var/lib/weaviate \
     -e DEFAULT_VECTORIZER_MODULE=text2vec-openai \
     -e ENABLE_MODULES=text2vec-openai \
     -e OPENAI_APIKEY=your-openai-api-key \
     semitechnologies/weaviate:1.22.4
   ```

## SSL/HTTPS Configuration

### Using Let's Encrypt

1. **Install Certbot**
   ```bash
   sudo apt-get update
   sudo apt-get install certbot
   ```

2. **Obtain Certificate**
   ```bash
   sudo certbot certonly --standalone -d yourdomain.com
   ```

3. **Configure Nginx**
   ```nginx
   server {
       listen 443 ssl;
       server_name yourdomain.com;

       ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
       ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

       location / {
           proxy_pass http://frontend:3000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }

       location /api {
           proxy_pass http://backend:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

## Monitoring and Logging

### Application Monitoring

1. **Health Checks**
   ```bash
   # Backend health check
   curl http://localhost:8000/health

   # Frontend health check
   curl http://localhost:3000/api/health
   ```

2. **Log Monitoring**
   ```bash
   # View application logs
   docker-compose logs -f backend
   docker-compose logs -f frontend

   # View specific service logs
   docker-compose logs -f postgres
   ```

### Performance Monitoring

1. **Database Monitoring**
   ```sql
   -- Check database performance
   SELECT * FROM pg_stat_activity;
   SELECT * FROM pg_stat_database;
   ```

2. **Application Metrics**
   ```bash
   # Monitor API response times
   curl -w "@curl-format.txt" -o /dev/null -s "http://localhost:8000/api/v1/health"
   ```

## Backup and Recovery

### Database Backup

```bash
# Create backup
pg_dump -h localhost -U user curriculum_architect > backup.sql

# Restore backup
psql -h localhost -U user curriculum_architect < backup.sql
```

### Application Backup

```bash
# Backup configuration
tar -czf config-backup.tar.gz backend/.env frontend/.env.local

# Backup data volumes
docker run --rm -v curriculum_architect_postgres_data:/data -v $(pwd):/backup alpine tar czf /backup/postgres-backup.tar.gz -C /data .
```

## Troubleshooting

### Common Issues

1. **Database Connection Issues**
   ```bash
   # Check database connectivity
   docker-compose exec postgres psql -U user -d curriculum_architect -c "SELECT 1;"
   ```

2. **Weaviate Connection Issues**
   ```bash
   # Check Weaviate health
   curl http://localhost:8080/v1/.well-known/ready
   ```

3. **Frontend Build Issues**
   ```bash
   # Clear Next.js cache
   cd frontend
   rm -rf .next
   npm run build
   ```

### Performance Optimization

1. **Database Optimization**
   ```sql
   -- Create indexes for better performance
   CREATE INDEX idx_users_email ON users(email);
   CREATE INDEX idx_curriculum_user_id ON curriculums(user_id);
   ```

2. **Caching Strategy**
   ```python
   # Implement Redis caching for frequently accessed data
   import redis
   
   redis_client = redis.Redis(host='localhost', port=6379, db=0)
   
   def get_cached_curriculum(curriculum_id):
       cached = redis_client.get(f"curriculum:{curriculum_id}")
       if cached:
           return json.loads(cached)
       # Fetch from database and cache
   ```

## Security Considerations

1. **Environment Variables**
   - Never commit `.env` files to version control
   - Use strong, unique secrets for production
   - Rotate secrets regularly

2. **Network Security**
   - Use HTTPS in production
   - Implement rate limiting
   - Configure CORS properly

3. **Database Security**
   - Use strong passwords
   - Limit database access
   - Enable SSL connections

4. **API Security**
   - Validate all inputs
   - Implement proper authentication
   - Use HTTPS for all API calls

## Scaling Considerations

1. **Horizontal Scaling**
   ```yaml
   # Scale backend services
   kubectl scale deployment backend --replicas=5
   ```

2. **Load Balancing**
   ```nginx
   upstream backend {
       server backend1:8000;
       server backend2:8000;
       server backend3:8000;
   }
   ```

3. **Database Scaling**
   - Consider read replicas for PostgreSQL
   - Implement connection pooling
   - Use database clustering for high availability

## Cost Optimization

1. **Resource Management**
   - Monitor resource usage
   - Scale down during low traffic
   - Use spot instances where possible

2. **CDN Usage**
   - Serve static assets via CDN
   - Cache API responses
   - Optimize image delivery

3. **Database Optimization**
   - Archive old data
   - Use appropriate instance sizes
   - Monitor query performance 