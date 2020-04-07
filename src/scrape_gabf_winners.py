from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import pandas as pd

if __name__ == "__main__":
    # initialize webdriver
    driver = webdriver.Chrome()
    driver.get('https://www.greatamericanbeerfestival.com/the-competition/winners/')

    time.sleep(3)

    year_drop_down = driver.find_element_by_xpath('//li[@id="year"]/a/span')
    year_drop_down.click()

    time.sleep(3)

    all_years = driver.find_element_by_xpath("//li[@data-year='0']")
    all_years.click()

    time.sleep(3)

    # pull page source code
    page_html = driver.page_source

    driver.quit()

    # parse with BeautifulSoup
    soup = BeautifulSoup(page_html, 'html.parser')

    header_elms = soup.find("thead").find("tr").find_all("th") 
    headers = [header.text for header in header_elms] 

    table_elm = soup.find('table', {'id': "winners_table"}).find("tbody").find_all("tr")
    row_elms = [row_elm.find_all("td") for row_elm in table_elm]
    clean_rows =  [[val.text.strip() for val in row] for row in row_elms] 

    gabf_df = pd.DataFrame(data=clean_rows, columns=headers)
    gabf_df.to_csv("data/gabf_winners.csv")
