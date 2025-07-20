from app.users import controller as users_controller
from app.reels import controller as reels_controller
from fastapi import FastAPI

app = FastAPI()
app.include_router(reels_controller.router)


@app.get("/")
def read_root():
    return {"Hello": "World"}