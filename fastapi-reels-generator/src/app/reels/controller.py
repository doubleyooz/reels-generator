from fastapi import APIRouter, Depends, status, FastAPI
from typing import List
from sqlalchemy.exc import IntegrityError
from src.db.database import Database
from src.app.reels.service import ReelService
from src.app.reels.schema import ReelCreateModel, ReelUpdateModel, ReelResponse
from src.app.reels.exception import ReelBadRequestException, ReelNotFoundException

async def get_reel_service(app: FastAPI = Depends(lambda: app)) -> ReelService:
    """Dependency to provide ReelService with initialized Database."""
    return ReelService(app.state.db)

router = APIRouter(prefix="/reels", tags=["reels"])

@router.get("/", response_model=List[ReelResponse])
async def find_all(reel_service: ReelService = Depends(get_reel_service)):
    """Retrieve all reels."""
    return await reel_service.find_all()

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ReelResponse)
async def create(reel_data: ReelCreateModel, reel_service: ReelService = Depends(get_reel_service)):
    """Create a new reel."""
    try:
        return await reel_service.create(reel_data)
    except IntegrityError:
        raise ReelBadRequestException()

@router.get("/{_id}", response_model=ReelResponse)
async def find_by_id(_id: int, reel_service: ReelService = Depends(get_reel_service)):
    """Retrieve a reel by ID."""
    reel = await reel_service.find_by_id(_id)
    if reel is None:
        raise ReelNotFoundException(_id)
    return reel

@router.patch("/{_id}", response_model=ReelResponse)
async def update(
    _id: int,
    reel_update_data: ReelUpdateModel,
    reel_service: ReelService = Depends(get_reel_service),
):
    """Update a reel by ID."""
    reel = await reel_service.update(_id, reel_update_data)
    if reel is None:
        raise ReelNotFoundException(_id)
    return reel

@router.delete("/{_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(_id: int, reel_service: ReelService = Depends(get_reel_service)):
    """Delete a reel by ID."""
    success = await reel_service.delete(_id)
    if not success:
        raise ReelNotFoundException(_id)
    return {}