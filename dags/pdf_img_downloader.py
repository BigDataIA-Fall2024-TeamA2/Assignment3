import os
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Create folders for PDFs and Images
os.makedirs('pdfs', exist_ok=True)
os.makedirs('images', exist_ok=True)

def sanitize_filename(filename):
    # Remove invalid characters from the filename
    return filename.split('?')[0]

def download_file(url, folder):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Check for HTTP errors

        # Sanitize the file name
        file_name = os.path.join(folder, sanitize_filename(url.split('/')[-1]))

        with open(file_name, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f'Downloaded: {file_name}')
    except Exception as e:
        print(f'Error downloading {url}: {e}')

def extract_pdf_and_image_urls(url):
    options = webdriver.ChromeOptions()
    options.headless = True
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        driver.get(url)

        while True:
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, 'RPCAllsiteSearchResultList'))
            )

            articles = driver.find_elements(By.CLASS_NAME, 'RPCAllsiteSearchResultList')

            for index in range(len(articles)):
                try:
                    article = articles[index]

                    # Extract the article URL
                    article_url = article.find_element(By.CLASS_NAME, 'CoveoResultLink').get_attribute('href')
                    pdf_url = get_pdf_link(driver, article_url)
                    image_url = extract_image_url(article)

                    # Download the PDF and Image URL
                    if pdf_url and pdf_url != "No PDF found":
                        download_file(pdf_url, 'pdfs')
                    if image_url and image_url != 'No image':
                        download_file(image_url, 'images')

                except Exception as e:
                    print(f'Error processing article: {e}')

            # Check if there is a next page
            try:
                next_button = driver.find_element(By.CSS_SELECTOR, '.coveo-pager-next')
                driver.execute_script("arguments[0].scrollIntoView();", next_button)
                next_button.click()
                WebDriverWait(driver, 10).until(
                    EC.staleness_of(articles[0])  # Wait for the page to load new results
                )
            except Exception as e:
                print("No more pages or error navigating:", e)
                break

    finally:
        driver.quit()

def get_pdf_link(driver, article_url):
    try:
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[1])
        driver.get(article_url)

        pdf_link = None
        links = driver.find_elements(By.TAG_NAME, 'a')
        for link in links:
            href = link.get_attribute('href')
            if href and href.endswith('.pdf'):
                pdf_link = href
                break

        driver.close()
        driver.switch_to.window(driver.window_handles[0])

        return pdf_link if pdf_link else "No PDF found"
    except Exception as e:
        print(f"Error finding PDF link: {e}")
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        return "No PDF found"

def extract_image_url(article):
    try:
        image_element = article.find_element(By.TAG_NAME, 'img')
        return image_element.get_attribute('src') if image_element else 'No image'
    except Exception:
        return 'No image'

# Example usage of the extractor
if __name__ == "__main__":
    url = "https://rpc.cfainstitute.org/en/research-foundation/publications#sort=%40officialz32xdate%20descending&numberOfResults=50&f:SeriesContent=[Research%20Foundation]"
    extract_pdf_and_image_urls(url)
