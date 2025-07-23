from fastapi import APIRouter, Depends, Request, status, File, UploadFile, Form
from typing import Annotated, List
from sqlalchemy.exc import IntegrityError
from src.db.database import Database
from src.app.reels.service import ReelService
from src.app.reels.schema import ReelCreateModel, ReelUpdateModel, ReelResponse
from src.app.reels.exception import ReelBadRequestException, ReelNotFoundException, ReelUnprocessableEntityException
from src.env import UPLOAD_DIR
from src.rate_limiter import limiter

import os
import uuid

async def get_reel_service(request: Request) -> ReelService:
    """Dependency to provide ReelService with initialized Database."""
    return ReelService(request.app.state.db)


router = APIRouter(prefix="/reels", tags=["reels"])

@router.get("/", response_model=List[ReelResponse])
async def find_all(reel_service: ReelService = Depends(get_reel_service)):
    """Retrieve all reels."""
    return await reel_service.find_all()

@limiter.limit("5/minute")
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ReelResponse)
async def create(
    request: Request,
    title: Annotated[str, Form()],
    user_id: Annotated[str, Form()],  # Accept as string
    video: UploadFile = File(...),
    audio: UploadFile = File(...),
    images: List[UploadFile] = File(default=[]),
    reel_service: ReelService = Depends(get_reel_service),
):
    """Create a new reel."""
    try:
        # Log raw request headers for debugging
        print(f"Title: {title}")
        print(f"User ID: {user_id}")
        print(f"Video: {video.filename}")
        print(f"Audio: {audio.filename}")
        print(f"Images: {[image.filename for image in images]}")
        
        # Save file
        file_filename = f"{uuid.uuid4()}_{video.filename}"
        file_path = os.path.join(UPLOAD_DIR, file_filename)
        with open(file_path, "wb") as f:
            f.write(video.file.read())

        # Save audio
        audio_filename = f"{uuid.uuid4()}_{audio.filename}"
        audio_path = os.path.join(UPLOAD_DIR, audio_filename)
        with open(audio_path, "wb") as f:
            f.write(audio.file.read())

        # Save images
        image_paths = []
        for image in images:
            image_filename = f"{uuid.uuid4()}_{image.filename}"
            image_path = os.path.join(UPLOAD_DIR, image_filename)
            with open(image_path, "wb") as f:
                f.write(image.file.read())
            image_paths.append(image_path)

        # Create ReelCreateModel
        reel_data = ReelCreateModel(
            title=title,
            file=file_path,
            audio=audio_path,
            images=image_paths,
            user_id=user_id,
        )
        print(f"Received reel_data: {reel_data}")
        print(f"File path: {file_path}")
        print(f"Audio path: {audio_path}")
        print(f"Image paths: {image_paths}")

        return await reel_service.create(reel_data)
    except IntegrityError as e:
        print(f"IntegrityError: {e}")
        raise ReelBadRequestException()
    except Exception as e:
        print(f"ValidationError: {e}")
        raise ReelUnprocessableEntityException(str(e))

@router.get("/{_id}", response_model=ReelResponse)
async def find_by_id(_id: uuid.UUID, reel_service: ReelService = Depends(get_reel_service)):
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
async def delete(_id: uuid.UUID, reel_service: ReelService = Depends(get_reel_service)):
    """Delete a reel by ID."""
    success = await reel_service.delete(_id)
    if not success:
        raise ReelNotFoundException()
    return {}