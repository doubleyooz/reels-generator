from src.app.auth import controller as auth_controller
from src.app.users import controller as users_controller
from src.app.reels import controller as reels_controller
from fastapi import FastAPI

app = FastAPI()
app.include_router(auth_controller.router)
app.include_router(reels_controller.router)
app.include_router(users_controller.router)

@app.get("/")
def read_root():
    return {"Hello": "World"}