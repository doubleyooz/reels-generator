from abc import ABC, abstractmethod
from fastapi import UploadFile
import uuid
from typing import Optional

class FileUploaderInterface(ABC):
    """Interface for file uploaders."""

    @abstractmethod
    async def upload_file(self, file: UploadFile, file_id: uuid.UUID, destination: str) -> str:
        """
        Upload a file to the storage service and return the object key or URL.
        
        Args:
            file: The file to upload.
            file_id: A unique ID for the file (e.g., reel ID).
            destination: The destination path or prefix (e.g., 'reels').
        
        Returns:
            The object key or URL of the uploaded file.
        
        Raises:
            Exception: If the upload fails.
        """
        pass

    @abstractmethod
    async def get_file_url(self, object_key: str, expires_in: int = 3600) -> Optional[str]:
        """
        Generate a presigned URL for accessing the file.
        
        Args:
            object_key: The key of the file in storage.
            expires_in: URL expiration time in seconds.
        
        Returns:
            The presigned URL or None if generation fails.
        """
        pass