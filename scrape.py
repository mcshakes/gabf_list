import requests
from bs4 import BeautifulSoup
import re
import csv
import pandas as pd

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

all_brewery_rows = list()

for data_row in body.find_all("tr"):
    row_list = list()

    single_brew_info = data_row.find(
        "td", "sorting_1")

    name_tag = single_brew_info.find("a").text  # COMPLETE

    extra_data = single_brew_info.find("a").get(
        "href").split("dir/")[0]

    # if address_data[1]:
    #     address_data = address_data[1].lstrip().split("+")
    # else:
    #     address_data = single_brew_info.find("a").get(
    #         "href").split("dir/")

    #     # import ipdb
    #     # ipdb.set_trace()

    # address = address_data[0]
    # city = address_data[1]
    # state = address_data[2]
    # zipcode = address_data[3]

    deal = data_row.find_all("td")[1].text

    row_list.extend([name_tag, extra_data, deal])
    all_brewery_rows.append(row_list)

# print(all_brewery_rows)

column_titles = ["Name", "Metadata", "Deal"]

brew = pd.DataFrame(all_brewery_rows, columns=column_titles)
brew.to_csv("breweries.csv")

driver.quit()
