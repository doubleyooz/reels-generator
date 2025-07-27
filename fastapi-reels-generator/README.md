# FastAPI Reels Generator

FastAPI Reels Generator is an open-source project designed to create and manage Instagram Reels content. Built with FastAPI, PostgreSQL, and SQLAlchemy, it provides a robust backend for user authentication (via Google OAuth) and Reels management, allowing users to generate and store short-form video metadata. The project uses Alembic for database migrations and supports a scalable architecture for social media content creation.

## Features
- **User Authentication**: Secure Google OAuth integration for user login and registration.
- **Reels Management**: Store and manage Reels metadata (title, file, audio, images, and creation timestamp) in a PostgreSQL database.
- **UUID-based IDs**: Unique identifiers for users and Reels, ensuring scalability and uniqueness.
- **Asynchronous Backend**: Built with FastAPI and async SQLAlchemy for high-performance API endpoints.
- **Database Migrations**: Managed with Alembic for seamless schema updates.

## Tech Stack
- **Backend**: FastAPI (Python)
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy (async)
- **Migrations**: Alembic
- **Authentication**: Google OAuth
- **Environment**: Python 3.12, virtualenv

## Prerequisites
- Python 3.12+
- PostgreSQL 13+
- Redis (optional, for session management)
- Google Cloud Console project with OAuth 2.0 credentials
- FFmpeg (optional, for video processing)

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/doubleyooz/reels-generator.git
   cd reels-generator/fastapi-reels-generator

To run this project use "source .venv/bin/activate" then fastapi run main.py "uvicorn src.main:app --reload"

to download dependencies use "pip install --break-system-packages -r requirements.txt"