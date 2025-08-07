import boto3
import uuid

from fastapi import UploadFile
from botocore.exceptions import ClientError

from asyncio import get_event_loop
from concurrent.futures import ThreadPoolExecutor

from typing import Optional
from src.db.interfaces.file_uploader import FileUploaderInterface
from src.env import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_S3_BUCKET_NAME, AWS_S3_REGION_NAME

class S3FileUploader(FileUploaderInterface):
    """S3 implementation of the FileUploaderInterface."""

    def __init__(self):
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            region_name=AWS_S3_REGION_NAME
        )

    async def upload_file(self, file: UploadFile, file_id: uuid.UUID, destination: str) -> str:
        """
        Upload a file to S3 and return the object key.
        
        Args:
            file: The file to upload.
            file_id: The UUID for the file (e.g., reel ID).
            destination: The S3 prefix (e.g., 'reels').
        
        Returns:
            The S3 object key (e.g., 'reels/<file_id>/<filename>').
        
        Raises:
            Exception: If the upload fails.
        """
        try:
            s3_key = f"{destination}/{file_id}/{file.filename}"
            loop = get_event_loop()
            with ThreadPoolExecutor() as pool:
                await loop.run_in_executor(
                    pool,
                    lambda: self.s3_client.upload_fileobj(
                        file.file,
                        AWS_S3_BUCKET_NAME,
                        s3_key,
                        ExtraArgs={'ContentType': file.content_type}
                    )
                )
            return s3_key
        except ClientError as e:
            raise Exception(f"S3 upload failed: {str(e)}")

    async def get_file_url(self, object_key: str, expires_in: int = 3600) -> Optional[str]:
        """
        Generate a presigned URL for accessing the file in S3.
        
        Args:
            object_key: The S3 object key.
            expires_in: URL expiration time in seconds.
        
        Returns:
            The presigned URL or None if generation fails.
        """
        try:
            url = self.s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': AWS_S3_BUCKET_NAME, 'Key': object_key},
                ExpiresIn=expires_in
            )
            return url
        except ClientError as e:
            print(f"Failed to generate presigned URL: {str(e)}")
            return None