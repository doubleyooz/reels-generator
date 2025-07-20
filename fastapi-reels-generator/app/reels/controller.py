from fastapi import APIRouter, Depends, status, FastAPI
from typing import List
from sqlalchemy.exc import IntegrityError
from app.db.database import Database
from app.reels.service import ReelService
from app.reels.schema import Reel, ReelCreateModel, ReelUpdateModel
from app.reels.exception import ReelBadRequest, ReelNotFound

async def get_reel_service(app: FastAPI = Depends(lambda: app)) -> ReelService:
    """Dependency to provide ReelService with initialized Database."""
    return ReelService(app.state.db)

router = APIRouter(prefix="/reels", tags=["reels"])

@router.get("/", response_model=List[Reel])
async def find_all(reel_service: ReelService = Depends(get_reel_service)):
    """Retrieve all reels."""
    return await reel_service.find_all()

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Reel)
async def create(reel_data: ReelCreateModel, reel_service: ReelService = Depends(get_reel_service)):
    """Create a new reel."""
    try:
        return await reel_service.create(reel_data)
    except IntegrityError:
        raise ReelBadRequest()

@router.get("/{reel_id}", response_model=Reel)
async def find_by_id(reel_id: int, reel_service: ReelService = Depends(get_reel_service)):
    """Retrieve a reel by ID."""
    reel = await reel_service.find_by_id(reel_id)
    if reel is None:
        raise ReelNotFound(reel_id)
    return reel

@router.patch("/{reel_id}", response_model=Reel)
async def update(
    reel_id: int,
    reel_update_data: ReelUpdateModel,
    reel_service: ReelService = Depends(get_reel_service),
):
    """Update a reel by ID."""
    reel = await reel_service.update(reel_id, reel_update_data)
    if reel is None:
        raise ReelNotFound(reel_id)
    return reel

@router.delete("/{reel_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(reel_id: int, reel_service: ReelService = Depends(get_reel_service)):
    """Delete a reel by ID."""
    success = await reel_service.delete(reel_id)
    if not success:
        raise ReelNotFound(reel_id)
    return {}