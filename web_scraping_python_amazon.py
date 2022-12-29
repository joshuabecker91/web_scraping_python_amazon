import csv
from bs4 import BeautifulSoup
from selenium import webdriver
# pip install bs4
# pip install selenium
# pip install msedge-selenium-tools selenium==3.141
# https://sites.google.com/chromium.org/driver/ download chromedriver and put in sibling directory

# Ignore bluetooth and other device messages --------------------------------------------------------------

options = webdriver.ChromeOptions() 
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(options=options)

# ---------------------------------------------------------------------------------------------------------

url = 'https://www.amazon.com'
driver.get(url)

def get_url(search_term, page):
    """Generate a url from search term"""
    search_term = search_term.replace(' ', '+')
    url = f'https://www.amazon.com/s?k={search_term}&page={page}&ref=nb_sb_noss_2'
    return url

# url = get_url('ultrawide monitor')
# print(url)

# driver.get(url)

# Extract the collection ----------------------------------------------------------------------------------

# soup = BeautifulSoup(driver.page_source, 'html.parser')
# results = soup.find_all('div', {'data-component-type': 's-search-result'})
# print(len(results))

# Prototype the extraction of a single record -------------------------------------------------------------

# item = results[0]
# atag = item.h2.a
# description = atag.text.strip()
# url = 'https://www.amazon.com' + atag.get('href')
# price_parent = item.find('span', 'a-price')
# price = price_parent.find('span', 'a-offscreen').text
# rating = item.i.text
# review_count = item.find('span', {'class': 'a-size-base', 'class': 's-underline-text'}).text.replace('(', '').replace(')', '')
# print(description, url, price, rating, review_count)

# ---------------------------------------------------------------------------------------------------------

def extract_record(item):
    """Extract and return data from a single record"""
    # description and url
    atag = item.h2.a
    description = atag.text.strip()
    url = 'https://www.amazon.com' + atag.get('href')
    
    try:
        # price
        price_parent = item.find('span', 'a-price')
        price = price_parent.find('span', 'a-offscreen').text
    except AttributeError:
        return
    
    try:
        # rating
        rating = item.i.text
        review_count = item.find('span', {'class': 'a-size-base', 'class': 's-underline-text'}).text.replace('(', '').replace(')', '')
    except AttributeError:
        rating = ''
        review_count = ''

    result = (description, price, rating, review_count, url)
    
    return result

# ---------------------------------------------------------------------------------------------------------

records = []

def main(search_term):
    record = []
    for page in range(1,21):
        url = get_url(search_term, page)
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        results = soup.find_all('div', {'data-component-type': 's-search-result'})
        print("successfully scraped: ", len(results), " results")

        for item in results:
            record = extract_record(item)
            if record:
                records.append(extract_record(item))

    driver.close()

    with open('results.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Description', 'Price', 'Rating', 'Review Count', 'Url'])
        writer.writerows(records)

# ---------------------------------------------------------------------------------------------------------

search = input("Please enter search term: ")

main(search)