from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def extract_article_details(article):
    try:
        title_element = article.find_element(By.CLASS_NAME, 'CoveoResultLink')
        description_element = article.find_element(By.CLASS_NAME, 'result-body')
        date_element = article.find_element(By.CLASS_NAME, 'date')
        authors_element = article.find_element(By.CLASS_NAME, 'author')

        title = title_element.text if title_element else 'No title'
        description = description_element.text if description_element else 'No description'
        date = date_element.text if date_element else 'No date'
        authors = authors_element.text if authors_element else 'No authors'

        return {'title': title, 'description': description, 'date': date, 'authors': authors}
    except Exception as e:
        print(f'Error extracting details: {e}')
        return {'title': 'Error', 'description': 'Error', 'date': 'Error', 'authors': 'Error'}

def extract_image_url(article):
    try:
        image_element = article.find_element(By.TAG_NAME, 'img')
        return image_element.get_attribute('src') if image_element else 'No image'
    except Exception:
        return 'No image'

def get_pdf_link(driver, article_url):
    try:
        # Open a new tab and switch to it
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[1])
        driver.get(article_url)

        # Look for a direct link to a PDF file
        pdf_link = None
        links = driver.find_elements(By.TAG_NAME, 'a')
        for link in links:
            href = link.get_attribute('href')
            if href and href.endswith('.pdf'):
                pdf_link = href
                break

        # Close the tab and switch back to the main window
        driver.close()
        driver.switch_to.window(driver.window_handles[0])

        return pdf_link if pdf_link else "No PDF found"
    except Exception as e:
        print(f"Error finding PDF link: {e}")
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        return "No PDF found"

def scrape_articles(url):
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
                    # Re-fetch the article list to avoid stale element reference
                    articles = driver.find_elements(By.CLASS_NAME, 'RPCAllsiteSearchResultList')
                    article = articles[index]

                    details = extract_article_details(article)
                    image_url = extract_image_url(article)
                    article_url = article.find_element(By.CLASS_NAME, 'CoveoResultLink').get_attribute('href')
                    pdf_url = get_pdf_link(driver, article_url)

                    print(f"Title: {details['title']}")
                    print(f"Image URL: {image_url}")
                    print(f"Description: {details['description']}")
                    print(f"Date: {details['date']}")
                    print(f"Authors: {details['authors']}")
                    print(f"PDF URL: {pdf_url}\n")

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

def main():
    url = "https://rpc.cfainstitute.org/en/research-foundation/publications#sort=%40officialz32xdate%20descending&numberOfResults=50&f:SeriesContent=[Research%20Foundation]"
    scrape_articles(url)

if __name__ == "__main__":
    main()
