from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def extract_article_details(url):
    options = webdriver.ChromeOptions()
    options.headless = True
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    articles_data = []

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

                    title_element = article.find_element(By.CLASS_NAME, 'CoveoResultLink')
                    description_element = article.find_element(By.CLASS_NAME, 'result-body')
                    date_element = article.find_element(By.CLASS_NAME, 'date')
                    authors_element = article.find_element(By.CLASS_NAME, 'author')

                    title = title_element.text if title_element else 'No title'
                    description = description_element.text if description_element else 'No description'
                    date = date_element.text if date_element else 'No date'
                    authors = authors_element.text if authors_element else 'No authors'

                    # Adding article data to the list
                    articles_data.append({
                        'title': title,
                        'description': description,
                        'date': date,
                        'authors': authors
                    })

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

    return articles_data


# Example usage
if __name__ == "__main__":
    url = "https://rpc.cfainstitute.org/en/research-foundation/publications#sort=%40officialz32xdate%20descending&numberOfResults=50&f:SeriesContent=[Research%20Foundation]"
    articles = extract_article_details(url)

    # Print the articles data
    for article in articles:
        print(article)
