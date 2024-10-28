import os
import boto3
from botocore.exceptions import NoCredentialsError

def upload_files_to_s3(local_dir, bucket_name, s3_prefix=''):
    s3_client = boto3.client('s3')

    for root, dirs, files in os.walk(local_dir):
        for file in files:
            local_path = os.path.join(root, file)
            relative_path = os.path.relpath(local_path, local_dir)
            s3_path = os.path.join(s3_prefix, relative_path).replace("\\", "/")

            try:
                print(f"Uploading {local_path} to {bucket_name}/{s3_path}")
                s3_client.upload_file(local_path, bucket_name, s3_path)
                print(f"Successfully uploaded {file}")
            except FileNotFoundError:
                print(f"File not found: {local_path}")
            except NoCredentialsError:
                print("Credentials not available")
                return False
            except Exception as e:
                print(f"Error uploading {file}: {str(e)}")

    return True

def main():
    # Local directories for images and PDFs
    image_directory = "D:\Projects\Assignment3\dags\images"
    pdf_directory = "D:\Projects\Assignment3\dags\pdfs"

    # S3 bucket details
    bucket_name = "damg7245-a3-store"
    image_s3_prefix = "cfa-publications/images"
    pdf_s3_prefix = "cfa-publications/pdfs"

    # Check if directories exist
    if not os.path.exists(image_directory):
        print(f"Error: Directory {image_directory} does not exist.")
        return

    if not os.path.exists(pdf_directory):
        print(f"Error: Directory {pdf_directory} does not exist.")
        return

    # Upload images
    print(f"Starting upload of images from {image_directory} to S3 bucket {bucket_name}/{image_s3_prefix}")
    upload_files_to_s3(image_directory, bucket_name, image_s3_prefix)

    # Upload PDFs
    print(f"Starting upload of PDFs from {pdf_directory} to S3 bucket {bucket_name}/{pdf_s3_prefix}")
    upload_files_to_s3(pdf_directory, bucket_name, pdf_s3_prefix)

if __name__ == "__main__":
    main()
