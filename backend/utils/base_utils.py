import logging
import os
from openai import OpenAI
import boto3
from botocore.exceptions import ClientError
from passlib.context import CryptContext

from backend.config import settings

LOCAL_EXTRACTS_DIRECTORY = os.path.join("resources", "extracts")

logger = logging.getLogger(__name__)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(plain_password: str) -> str:
    return pwd_context.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def ensure_directory_exists(directory):
    os.makedirs(directory, exist_ok=True)


def get_s3_client():
    return boto3.client("s3", aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY, region_name=settings.AWS_REGION)

# def get_openai_client() -> OpenAI:
#     """
#     Creates and returns an OpenAI client instance using API key from settings
    
#     Returns:
#         OpenAI: Configured OpenAI client instance
#     """
#     api_key = settings.OPENAI_API_KEY
#     if not api_key:
#         raise ValueError("OPENAI_API_KEY not found in settings")
        
#     return OpenAI(api_key=api_key)