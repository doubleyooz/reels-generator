from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from starlette.middleware.sessions import SessionMiddleware
from dotenv import load_dotenv

from src.app.auth import controller as auth_controller
from src.app.users import controller as users_controller
from src.app.reels import controller as reels_controller
from src.db.database import Database
from src.env import CLIENT, UPLOAD_DIR, SESSION_SECRET_KEY

import os

load_dotenv()

# Lifespan event handler to manage database lifecycle
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize database and set app.state.db
    app.state.db = Database()
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    await app.state.db.init_db()
    yield
    # Shutdown: Close database connections
    await app.state.db.close()
    CORSMiddleware
origins = [
    CLIENT,
]



app = FastAPI(lifespan=lifespan)

app.add_middleware(SessionMiddleware, secret_key=SESSION_SECRET_KEY)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# app.exception_handler(RequestValidationError)(custom_validation_exception_handler)
# Include routers
app.include_router(auth_controller.router)
app.include_router(users_controller.router)
app.include_router(reels_controller.router)

@app.get("/")
def read_root():
    return {"Hello": "World"}