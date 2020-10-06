import requests
from bs4 import BeautifulSoup
import re
import csv

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver


options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox')
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')

driver = webdriver.Chrome(options=options)

brewery_page = "https://www.greatamericanbeerfestival.com/breweries-beers/beers-at-the-festival/"

driver.get(brewery_page)

table_div = WebDriverWait(driver, 8).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, "div#breweryDealContainer")))

driver.execute_script(
    "return arguments[0].scrollIntoView(true);", table_div)

# --- 2) Pass to Soup ---

page_source = driver.page_source

soup = BeautifulSoup(page_source, "html.parser")

# --- 2) SCRAPE BREWERIES ---

table = soup.find("table", id="brewery-table")
body = table.find("tbody")


with open("breweries.txt", mode="w", encoding='utf-8') as csv_file:
    brewery_writer = csv.writer(
        csv_file, delimiter=",")

    for data_row in body.find_all("tr"):
        name = [td.text for td in data_row.find_all("td.sorting_1")]
        deal = [td.text for td in data_row.find_all("td.deal")]
        brewery_writer.writerow([name])

driver.quit()
