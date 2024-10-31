import base64
import logging
import os
from functools import lru_cache

import boto3
from botocore.exceptions import ClientError, NoCredentialsError

BASE_RESOURCES_PATH = os.path.join("sources", "resources")
SCRAPED_RESOURCES_PATH = os.path.join(BASE_RESOURCES_PATH, "scraped")
CACHED_RESOURCES_PATH = os.path.join(BASE_RESOURCES_PATH, "cached")

logger = logging.getLogger(__name__)


def ensure_directory_exists(directory):
    os.makedirs(directory, exist_ok=True)


def load_aws_tokens():
    if all(
        [
            k in os.environ
            for k in ["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY", "AWS_REGION"]
        ]
    ):
        return {
            "aws_access_key_id": os.environ["AWS_ACCESS_KEY_ID"],
            "aws_secret_access_key": os.environ["AWS_SECRET_ACCESS_KEY"],
            "region_name": os.environ["AWS_REGION"],
        }
    raise ValueError("Missing AWS Credentials in environment")


def load_s3_bucket():
    if "AWS_S3_BUCKET" in os.environ:
        return os.environ["AWS_S3_BUCKET"]
    raise ValueError("Missing AWS S3 Bucket")


@lru_cache
def get_s3_client():
    return boto3.client("s3", **load_aws_tokens())


def fetch_file_from_s3(key: str):
    s3_client = get_s3_client()
    filename = os.path.basename(key)
    local_filepath = os.path.join(CACHED_RESOURCES_PATH, filename)
    try:
        _ = s3_client.head_object(Bucket=load_s3_bucket(), Key=filename)
        s3_client.download_file(load_s3_bucket(), filename)
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
        print(f"File not found: {local_file_path}")
    except NoCredentialsError:
        print("Credentials not available")
    except Exception as e:
        print(f"Error uploading {local_file_path}: {str(e)}")
    return None
