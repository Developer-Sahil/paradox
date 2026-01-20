# Project Architecture

This project uses a hybrid architecture with multiple frameworks serving different purposes.

## Components Overview

### 🎯 **FastAPI Backend** (`backend/`) - Primary API
- **Port**: 8000
- **Purpose**: REST API for data operations, admin panel, content management
- **Technology**: FastAPI with Pydantic models
- **Database**: Firebase Firestore
- **Entry Point**: `backend/main.py`

### 🌐 **Flask App** (`app/`) - Legacy Frontend
- **Port**: 5000
- **Purpose**: Traditional web application with server-side rendering
- **Technology**: Flask with Jinja2 templates
- **Database**: Firebase Firestore
- **Entry Point**: `run.py`

### ⚛️ **Next.js Frontend** (`frontend/`) - Modern Frontend
- **Port**: 3000 (development)
- **Purpose**: Modern React application (currently standalone)
- **Technology**: Next.js 16 with TypeScript and Tailwind CSS
- **Status**: Not integrated with backends

## Architecture Decisions

### Why Multiple Frameworks?

1. **FastAPI Backend**: Chosen for its performance, automatic OpenAPI documentation, and modern async capabilities. Handles all API operations and admin functionality.

2. **Flask App**: Legacy component providing traditional web experience with server-side rendered pages.

3. **Next.js Frontend**: Modern React application for enhanced user experience, though currently not integrated.

### Data Flow

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Next.js   │    │   FastAPI   │    │    Flask    │
│  Frontend   │◄──►│   Backend   │◄──►│     App     │
│  (Port 3000)│    │  (Port 8000)│    │  (Port 5000)│
└─────────────┘    └─────────────┘    └─────────────┘
                      │                       │
                      └───────────────────────┘
                              Firebase Firestore
```

## Development Workflow

### Running Locally

1. **FastAPI Backend** (Primary):
   ```bash
   cd backend
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

2. **Flask App** (Legacy):
   ```bash
   python run.py
   ```

3. **Next.js Frontend** (Standalone):
   ```bash
   cd frontend
   npm run dev
   ```

### API Endpoints

- **FastAPI**: `http://localhost:8000` - Primary API with OpenAPI docs at `/docs`
- **Flask**: `http://localhost:5000` - Legacy web app
- **Next.js**: `http://localhost:3000` - Modern frontend (not connected)

## Database

All components share the same Firebase Firestore database with collections:
- `writings` - Blog posts and articles
- `projects` - Portfolio projects
- `products` - Digital products
- `tools` - System tools
- `vault` - Knowledge base
- `arena` - Commentary/discussion
- `metrics` - Performance metrics

## Future Integration

The Next.js frontend is currently standalone. Future plans include:
- Integrating Next.js with FastAPI backend
- Migrating Flask routes to Next.js pages
- Consolidating to a single frontend framework