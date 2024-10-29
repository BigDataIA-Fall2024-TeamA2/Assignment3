import os
import json
import boto3
from botocore.exceptions import NoCredentialsError
from urllib.parse import quote, urlparse


def upload_file_to_s3(local_path, bucket_name, s3_path):
    s3_client = boto3.client('s3')
    try:
        s3_client.upload_file(local_path, bucket_name, s3_path)
        return s3_path
    except FileNotFoundError:
        print(f"File not found: {local_path}")
    except NoCredentialsError:
        print("Credentials not available")
    except Exception as e:
        print(f"Error uploading {local_path}: {str(e)}")
    return None

def update_article_links(articles, image_directory, pdf_directory, bucket_name, image_s3_prefix, pdf_s3_prefix):
    for article in articles:
        # Update image URL
        if article['image_url'] != 'No image':
            image_filename = os.path.basename(urlparse(article['image_url']).path)
            local_image_path = os.path.join(image_directory, image_filename)
            s3_image_path = f"{image_s3_prefix}/{image_filename}"
            if os.path.exists(local_image_path):
                s3_image_url = upload_file_to_s3(local_image_path, bucket_name, s3_image_path)
                if s3_image_url:
                    article['image_url'] = s3_image_url
            else:
                print(f"Image file not found: {local_image_path}")

        # Update PDF URL
        if article['pdf_url'] != "No PDF found":
            pdf_filename = os.path.basename(urlparse(article['pdf_url']).path)
            local_pdf_path = os.path.join(pdf_directory, pdf_filename)
            s3_pdf_path = f"{pdf_s3_prefix}/{pdf_filename}"
            if os.path.exists(local_pdf_path):
                s3_pdf_url = upload_file_to_s3(local_pdf_path, bucket_name, s3_pdf_path)
                if s3_pdf_url:
                    article['pdf_url'] = s3_pdf_url
            else:
                print(f"PDF file not found: {local_pdf_path}")

    return articles

def main():
    # Load the existing JSON file
    input_file = 'articles_data.json'
    with open(input_file, 'r', encoding='utf-8') as f:
        articles = json.load(f)

    # Local directories for images and PDFs
    image_directory = r"D:\Projects\Assignment3\dags\images"
    pdf_directory = r"D:\Projects\Assignment3\dags\pdfs"

    # S3 bucket details
    bucket_name = "damg7245-a3-store"
    image_s3_prefix = "cfa-publications/images"
    pdf_s3_prefix = "cfa-publications/pdfs"

    # Update article links and upload to S3
    updated_articles = update_article_links(articles, image_directory, pdf_directory, bucket_name, image_s3_prefix, pdf_s3_prefix)

    # Save the updated articles data to a new JSON file
    output_file = 'updated_articles_data.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(updated_articles, f, ensure_ascii=False, indent=4)

    print(f"Updated articles data saved to {output_file}")

if __name__ == "__main__":
    main()
