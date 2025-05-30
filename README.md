# Insurance Premium Calculator

[![Build Status](https://img.shields.io/badge/build-passing-brightgreen)](https://github.com/your-org/insurance-calculator/actions)
[![Docker Pulls](https://img.shields.io/docker/pulls/your-docker-repo/insurance-calculator)](https://hub.docker.com/r/your-docker-repo/insurance-calculator)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A modern, containerized full-stack web application for calculating real-time insurance premiums across multiple product lines (Auto, Home, Life). Built with industry best practices and designed for scalability and maintainability.

## 🚀 Features

- **Real-time Premium Calculations** - Instant quotes for Auto, Home, and Life insurance policies
- **Multi-factor Analysis** - Calculate premiums based on age, location, coverage levels, and risk factors
- **Data Persistence** - Complete audit trail of all quote requests and results
- **Rate Limiting & Resilience** - Intelligent handling of API rate limits with automatic retries
- **Interactive Dashboard** - Responsive single-page application with real-time validation
- **Auto-generated Documentation** - Interactive API docs via Swagger/OpenAPI
- **Production Ready** - Fully containerized with Docker for easy deployment

## 🛠️ Technology Stack

### Backend

- **[FastAPI](https://fastapi.tiangolo.com/)** - Modern Python web framework with automatic API documentation
- **[SQLAlchemy](https://www.sqlalchemy.org/)** - Python SQL toolkit and Object-Relational Mapping
- **[Alembic](https://alembic.sqlalchemy.org/)** - Database migration tool for SQLAlchemy
- **[PostgreSQL](https://www.postgresql.org/)** - Advanced open-source relational database

### Frontend

- **[Vue 3](https://vuejs.org/)** - Progressive JavaScript framework with Composition API
- **[Vite](https://vitejs.dev/)** - Next-generation frontend build tool
- **[Bootstrap 5](https://getbootstrap.com/)** - Modern CSS framework for responsive design
- **[Axios](https://axios-http.com/)** - Promise-based HTTP client

### DevOps & Infrastructure

- **[Docker](https://www.docker.com/)** - Containerization platform
- **[Docker Compose](https://docs.docker.com/compose/)** - Multi-container Docker application management

## 📋 Prerequisites

Ensure you have the following installed on your system:

- **Docker** ≥ 20.10 - [Download Docker](https://www.docker.com/get-started)
- **Docker Compose** ≥ 1.29 - [Install Docker Compose](https://docs.docker.com/compose/install/)

### For Local Development (Optional)

- **Node.js** ≥ 18.0 - [Download Node.js](https://nodejs.org/)
- **Python** ≥ 3.9 - [Download Python](https://www.python.org/downloads/)

## ⚙️ Configuration

### Environment Variables

Create the required environment files:

#### Backend Configuration (`backend/.env`)

```bash
# Database Configuration
DATABASE_URL=postgresql+psycopg2://fastapi_user:fastapi_password@postgres:5432/insurance_calculator

# RapidAPI Configuration
RAPIDAPI_KEY=your_rapidapi_key_here
RAPIDAPI_HOST=insurecom1.p.rapidapi.com

# Application Environment
ENV=development
DEBUG=true

# Security (generate secure random strings in production)
SECRET_KEY=your-secret-key-here
```

#### Frontend Configuration (`.env` in project root)

```bash
# API Configuration
VITE_API_BASE_URL=http://localhost:8000/api/v1

# Environment
VITE_ENV=development
```

> **Note:** Copy `backend/.env.example` to `backend/.env` and update the values according to your setup.

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/your-org/insurance-calculator.git
cd insurance-calculator
```

### 2. Set Up Environment Files

```bash
# Copy example environment file
cp backend/.env.example backend/.env

# Edit the environment files with your configuration
# Add your RapidAPI key and other required values
```

### 3. Build and Launch with Docker Compose

```bash
# Build and start all services
docker-compose up --build

# Or run in detached mode
docker-compose up --build -d
```

### 4. Access the Application

- **Frontend Application:** [http://localhost:5173](http://localhost:5173)
- **Backend API Documentation:** [http://localhost:8000/docs](http://localhost:8000/docs)
- **Alternative API Docs:** [http://localhost:8000/redoc](http://localhost:8000/redoc)

### 5. Initialize Database (if needed)

```bash
# Run database migrations
cd backend
alembic upgrade head
```

## 📖 API Documentation

The application provides comprehensive API documentation through FastAPI's automatic generation:

| Endpoint             | Method | Description                                       |
| -------------------- | ------ | ------------------------------------------------- |
| `/calculate-premium` | POST   | Calculate insurance premium for given parameters  |
| `/requests`          | GET    | Retrieve all quote requests with pagination       |
| `/results`           | GET    | Retrieve all quote results with filtering options |
| `/health`            | GET    | Health check endpoint for monitoring              |

### Example API Request

```bash
curl -X POST "http://localhost:8000/calculate-premium" \
  -H "Content-Type: application/json" \
  -d '{
    "insurance_type": "auto",
    "age": 30,
    "location": "New York",
    "coverage_amount": 100000
  }'
```

## 🛠️ Development

### Local Backend Development

```bash
# Navigate to backend directory
cd backend

# Install dependencies
pip install -r requirements.txt

# Run development server with hot reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Local Frontend Development

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build
```

### Database Migrations

#### Create New Migration

```bash
cd backend
alembic revision --autogenerate -m "Description of changes"
```

#### Apply Migrations

```bash
alembic upgrade head
```

#### Rollback Migration

```bash
alembic downgrade -1
```

## 🧪 Testing

### Backend Tests

```bash
cd backend

# Install dependencies (includes test dependencies)
pip install -r requirements.txt

# Run all tests (if test directory exists)
python -m pytest

# Run with coverage report
python -m pytest --cov=app

# Run specific test file
python -m pytest tests/test_routes.py -v
```

### Frontend Tests

```bash
cd frontend

# Run unit tests
npm test

# Run tests in watch mode
npm run test:watch

# Generate coverage report
npm run test:coverage
```

## 🐳 Docker Commands

### Useful Docker Compose Commands

```bash
# Start services in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Rebuild specific service
docker-compose up --build backend

# Execute command in running container
docker-compose exec backend bash
docker-compose exec frontend sh
```

### Database Access

```bash
# Connect to PostgreSQL database
docker-compose exec postgres psql -U fastapi_user -d insurance_calculator
```

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/amazing-feature`
3. **Commit** your changes: `git commit -m 'Add some amazing feature'`
4. **Push** to the branch: `git push origin feature/amazing-feature`
5. **Open** a Pull Request

### Development Guidelines

- Follow existing code style and conventions
- Add tests for new features (if test suite is implemented)
- Update documentation as needed
- Run linters before committing:

  ```bash
  # Backend linting (if configured)
  cd backend && python -m flake8 app/

  # Frontend linting
  cd frontend && npm run lint
  ```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/your-org/insurance-calculator/issues) page
2. Create a new issue with detailed information
3. Join our [Discussions](https://github.com/your-org/insurance-calculator/discussions) for community support

## 🏗️ Architecture

```
insurance-calculator/
├── backend/                 # FastAPI backend application
│   ├── app/
│   │   ├── __init__.py     # Python package initialization
│   │   ├── main.py         # FastAPI application entry point
│   │   ├── models.py       # SQLAlchemy database models
│   │   ├── routes.py       # API routes and endpoints
│   │   ├── schemas.py      # Pydantic models for request/response
│   │   ├── session.py      # Database session management
│   │   └── utils.py        # Utility functions and helpers
│   ├── alembic/            # Database migration scripts
│   ├── alembic.ini         # Alembic configuration file
│   ├── Dockerfile          # Backend container configuration
│   ├── requirements.txt    # Python dependencies
│   └── venv/               # Virtual environment (local development)
├── frontend/               # Vue.js frontend application
│   ├── src/
│   │   ├── api/            # API client and HTTP services
│   │   ├── components/     # Reusable Vue components
│   │   ├── router/         # Vue Router configuration
│   │   ├── views/          # Application pages/views
│   │   ├── App.vue         # Root Vue component
│   │   └── main.js         # Frontend application entry point
│   ├── node_modules/       # NPM dependencies (generated)
│   ├── Dockerfile          # Frontend container configuration
│   ├── index.html          # HTML entry point
│   ├── package.json        # NPM package configuration
│   ├── package-lock.json   # NPM dependency lock file
│   └── vite.config.js      # Vite build configuration
├── docker-compose.yml      # Multi-container orchestration
└── README.md               # Project documentation
```

---

**Made with ❤️ by [Edd Gachira](https://github.com/eddgachi)**
