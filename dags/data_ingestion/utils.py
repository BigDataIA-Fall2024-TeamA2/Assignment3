import logging
import os
from functools import lru_cache

import boto3
from botocore.exceptions import ClientError, NoCredentialsError
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

BASE_RESOURCES_PATH = os.path.join("resources")
SCRAPED_RESOURCES_PATH = os.path.join(BASE_RESOURCES_PATH, "scraped")
CACHED_RESOURCES_PATH = os.path.join(BASE_RESOURCES_PATH, "cached")

logger = logging.getLogger(__name__)


def _ensure_directory_exists(directory):
    os.makedirs(directory, exist_ok=True)


def ensure_resource_dir_exists():
    _ensure_directory_exists(os.path.join(CACHED_RESOURCES_PATH, "pdfs"))
    _ensure_directory_exists(os.path.join(CACHED_RESOURCES_PATH, "images"))


def load_aws_tokens():
    required_keys = ["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY", "AWS_REGION"]
    if all(key in os.environ for key in required_keys):
        return {
            "aws_access_key_id": os.environ["AWS_ACCESS_KEY_ID"],
            "aws_secret_access_key": os.environ["AWS_SECRET_ACCESS_KEY"],
            "region_name": os.environ["AWS_REGION"],
        }
    raise ValueError("Missing AWS Credentials in environment")


def load_s3_bucket():
    bucket = os.environ.get("AWS_S3_BUCKET")
    if bucket:
        return bucket
    raise ValueError("Missing AWS S3 Bucket")


@lru_cache
def get_s3_client():
    return boto3.client("s3", **load_aws_tokens())


def fetch_file_from_s3(key: str, dest_filename: str | None):
    s3_client = get_s3_client()

    filename = (
        os.path.basename(key)
        if not dest_filename
        else f"{dest_filename}{os.path.splitext(key)[1]}"
    )
    local_filepath = os.path.join(CACHED_RESOURCES_PATH, filename)
    # Check locally before downloading
    if os.path.exists(local_filepath):
        return local_filepath
    else:
        try:
            _ = s3_client.head_object(Bucket=load_s3_bucket(), Key=key)
            s3_client.download_file(load_s3_bucket(), key, local_filepath)
            logger.info(f"Downloaded file {key} from S3")
            return local_filepath
        except ClientError as e:
            if e.response["Error"]["Code"] == "404":  # File not found
                logger.error(f"File {key} not found on S3")
                return False
            else:
                logger.error("")
                return False


def upload_file_to_s3(local_file_path: str, key: str):
    s3_client = get_s3_client()
    bucket_name = load_s3_bucket()

    try:
        s3_client.upload_file(local_file_path, bucket_name, key)
        return key
    except FileNotFoundError:
        logger.error(f"File not found: {local_file_path}")
    except NoCredentialsError:
        logger.error("Credentials not available")
    except Exception as e:
        logger.error(f"Error uploading {local_file_path}: {str(e)}")
    return None
