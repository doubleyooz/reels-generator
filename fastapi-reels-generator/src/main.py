from fastapi import FastAPI
from contextlib import asynccontextmanager
from dotenv import load_dotenv

from src.app.auth import controller as auth_controller
from src.app.users import controller as users_controller
from src.app.reels import controller as reels_controller
from src.db.database import Database

import os

load_dotenv()

# Lifespan event handler to manage database lifecycle
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize database and set app.state.db
    app.state.db = Database()
    await app.state.db.init_db()
    yield
    # Shutdown: Close database connections
    await app.state.db.close()

app = FastAPI(lifespan=lifespan)

# Include routers
app.include_router(auth_controller.router)
app.include_router(users_controller.router)
app.include_router(reels_controller.router)

@app.get("/")
def read_root():
    return {"Hello": "World"}