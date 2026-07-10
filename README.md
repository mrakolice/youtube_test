# YouTube Clone Project

## Project Overview

This is a YouTube-like video streaming platform built with FastAPI and Vue 3, featuring:

- **User Authentication**: JWT-based authentication system
- **Video Management**: Upload, process, and stream videos in multiple qualities
- **View Tracking**: Real-time view counter with Kafka event processing
- **Like/Dislike System**: User reactions on videos
- **Microservices Architecture**: Separate services for auth, videos, views, and likes
- **High Scalability**: Handles millions of concurrent views using Redis caching and Kafka for event streaming

## Tech Stack

### Backend
- **Framework**: FastAPI (async Python)
- **Database**: PostgreSQL with SQLModel ORM
- **Migrations**: Alembic
- **Message Queue**: Apache Kafka
- **Caching**: Redis
- **Authentication**: JWT tokens
- **Testing**: pytest with async support

### Frontend
- **Framework**: Vue 3 with Composition API
- **State Management**: Pinia
- **HTTP Client**: Axios
- **Styling**: CSS with component-scoped styles
- **Build Tool**: Vite
- **Testing**: Vitest

### Infrastructure
- **Containerization**: Docker & Docker Compose
- **Package Management**: uv (Python), pnpm (Node)
- **Orchestration**: Docker Compose

## Project Structure

```
youtube_test/
├── backend/
│   ├── services/
│   │   ├── auth/          # Authentication service
│   │   ├── videos/        # Video management service
│   │   ├── views/         # View tracking service
│   │   └── likes/         # Like/dislike service
│   └── shared/            # Shared utilities
├── frontend/              # Vue 3 application
├── docker-compose.yml     # Service orchestration
├── Makefile              # Build and run commands
└── .env                  # Environment variables
```

## Getting Started

### Prerequisites

- Docker & Docker Compose
- Python 3.11+
- Node 18+
- Make

### Installation

1. **Clone the repository**
```bash
cd youtube_test
```

2. **Set up environment**
```bash
make setup-env
```

3. **Build Docker images**
```bash
make build
```

4. **Start all services**
```bash
make up
```

The application will be available at:
- Frontend: http://localhost:3000
- Auth Service: http://localhost:8001
- Video Service: http://localhost:8002
- View Service: http://localhost:8003
- Like Service: http://localhost:8004

## Available Commands

### Development
```bash
# Start all services
make up

# Stop all services
make down

# View logs
make logs
make logs-auth
make logs-video

# Run individual services locally (without Docker)
make auth-service
make video-service
make view-service
make like-service
```

### Database
```bash
# Run migrations
make migrate-up

# Rollback migrations
make migrate-down

# Create migration
make migrate-create SERVICE=auth NAME=add_user_table

# Seed database
make seed-db
make seed-test-db
```

### Testing
```bash
# Run all tests
make test-all

# Run specific service tests
make test-auth
make test-videos
make test-views
make test-likes

# Run specific test
make test-one SERVICE=auth TEST=test_auth
```

### Code Quality
```bash
# Lint code
make lint

# Format code
make format

# Type checking
make type-check

# Clean up
make clean
make docker-clean
```

## API Endpoints

### Auth Service
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - User login
- `GET /api/auth/me` - Get current user
- `PUT /api/auth/me` - Update user profile

### Video Service
- `POST /api/videos/upload` - Upload new video
- `GET /api/videos/{video_id}` - Get video details
- `GET /api/videos/` - List videos

### View Service
- `POST /api/views/record` - Record video view
- `GET /api/views/{video_id}/count` - Get view count

### Like Service
- `POST /api/likes/add-reaction` - Add like/dislike
- `GET /api/likes/{video_id}/stats` - Get like/dislike stats

## Architecture

### Microservices

Each service is independently deployable with its own:
- Database schema (PostgreSQL)
- API endpoints
- Alembic migrations
- Tests
- Docker container

### Communication

- **Synchronous**: REST API calls between services
- **Asynchronous**: Kafka topics for event streaming
  - `video.processed` - Video processing events
  - `view.recorded` - View tracking events
  - `like.recorded` - Like/dislike events

### Caching

Redis is used for:
- Session management
- View count caching
- Rate limiting

## Testing Strategy

- **Integration Tests**: Test against real database
- **Parallel Execution**: Tests run concurrently with pytest-xdist
- **Database Transactions**: Each test runs in its own transaction
- **Mock Data**: Structured test fixtures and mock data

## Deployment Notes

For production deployment:

1. Update `JWT_SECRET_KEY` in .env
2. Configure PostgreSQL with proper backups
3. Set up Kafka cluster for high availability
4. Enable Redis persistence
5. Configure CORS appropriately
6. Use environment-specific settings
7. Set up SSL/TLS certificates

## Security Considerations

- Passwords are hashed with bcrypt
- JWT tokens with expiration
- SQL injection prevention via ORM
- CORS configuration
- Input validation on all endpoints
- Rate limiting recommended
- API key authentication for production

## Development Workflow

1. Create feature branch
2. Make changes in service folders
3. Write tests
4. Run `make test-all` to verify
5. Commit and push

## Troubleshooting

### Database Connection Issues
```bash
# Check if PostgreSQL is running
docker-compose ps

# View database logs
docker-compose logs postgres
```

### Port Already in Use
```bash
# Kill process on port
lsof -ti:3000 | xargs kill -9  # Frontend
lsof -ti:8001 | xargs kill -9  # Auth service
```

### Migration Issues
```bash
# Reset database (WARNING: deletes data)
make docker-clean
make build
make up
make migrate-up
```

## Contributing

1. Follow the existing code structure
2. Use absolute imports
3. Write tests for new features
4. Keep components modular and reusable
5. Document public APIs

## License

MIT License - See LICENSE file for details

## Support

For issues and questions, please create an issue in the repository.
