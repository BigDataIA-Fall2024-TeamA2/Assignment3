import json
import logging
import os
from urllib.parse import urlparse

from dags.data_ingestion.utils import (
    upload_file_to_s3,
    SCRAPED_RESOURCES_PATH,
    BASE_RESOURCES_PATH,
)

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def update_article_links(
    articles,
    image_directory,
    pdf_directory,
    bucket_name,
    image_s3_prefix,
    pdf_s3_prefix,
):
    for article in articles:
        # Update image URL
        if article["image_url"] and article["image_url"] != "No image":
            image_filename = os.path.basename(urlparse(article["image_url"]).path)
            local_image_path = os.path.join(image_directory, image_filename)
            s3_image_path = f"{image_s3_prefix}/{image_filename}"
            if os.path.exists(local_image_path):
                s3_image_url = upload_file_to_s3(local_image_path, s3_image_path)
                if s3_image_url:
                    article["image_url"] = s3_image_url
            else:
                logger.warning(f"Image file not found: {local_image_path}")

        # Update PDF URL
        if article["pdf_url"] and article["pdf_url"] != "No PDF found":
            pdf_filename = os.path.basename(urlparse(article["pdf_url"]).path)
            local_pdf_path = os.path.join(pdf_directory, pdf_filename)
            s3_pdf_path = f"{pdf_s3_prefix}/{pdf_filename}"
            if os.path.exists(local_pdf_path):
                s3_pdf_url = upload_file_to_s3(local_pdf_path, s3_pdf_path)
                if s3_pdf_url:
                    article["pdf_url"] = s3_pdf_url
            else:
                logger.warning(f"PDF file not found: {local_pdf_path}")

    return articles


def main():
    try:
        # Load the existing JSON file
        input_file = os.path.join(BASE_RESOURCES_PATH, "articles_data.json")
        with open(input_file, "r", encoding="utf-8") as f:
            articles = json.load(f)

        logger.info(f"Loaded {len(articles)} articles from {input_file}")

        # Local directories for images and PDFs
        image_directory = os.path.join(SCRAPED_RESOURCES_PATH, "images")
        pdf_directory = os.path.join(SCRAPED_RESOURCES_PATH, "pdfs")

        # S3 bucket details
        bucket_name = "damg7245-a3-store"
        image_s3_prefix = "cfa-publications/images"
        pdf_s3_prefix = "cfa-publications/pdfs"

        # Update article links and upload to S3
        updated_articles = update_article_links(
            articles,
            image_directory,
            pdf_directory,
            bucket_name,
            image_s3_prefix,
            pdf_s3_prefix,
        )

        # Save the updated articles data to a new JSON file
        output_file = os.path.join(BASE_RESOURCES_PATH, "updated_articles_data.json")
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(updated_articles, f, ensure_ascii=False, indent=4)

        logger.info(f"Updated articles data saved to {output_file}")

    except json.JSONDecodeError as e:
        logger.error(f"JSON decoding error: {e}")
        with open(input_file, "r", encoding="utf-8") as f:
            problematic_content = f.read()
        logger.error(
            f"Problematic JSON content: {problematic_content[:500]}..."
        )  # Log the first 500 characters
    except Exception as e:
        logger.error(f"An error occurred: {e}", exc_info=True)


if __name__ == "__main__":
    main()
