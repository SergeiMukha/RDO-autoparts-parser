import time
import requests

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

class Parser:
    def __init__(self):
        self.driver = webdriver.Chrome = webdriver.Chrome()

    def get_part_link(self, art):
        self.driver.get(f"https://www.rdoequipment.com/search?query={art}")

        try: WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "part_item")))
        except TimeoutException: return None
        
        link = self.driver.find_element(By.CLASS_NAME, "part_item").find_element(By.TAG_NAME, "a").get_attribute("href")

        if(art not in link): return None
        else: return link

    def get_page_data(self, link, art):
        self.driver.get(link)

        try:
            img_link = WebDriverWait(self.driver, 2).until(EC.presence_of_element_located((By.XPATH, "//div[@class='pd_imagery']/div/div/div/ul/li[1]/img"))).get_attribute("src")

            self._download_photo(img_link, art.replace("/", "-"))
        except TimeoutException: img_link = None

        print(img_link)

    
    # Downloads photo from the page
    def _download_photo(self, link: str, filename: str):
        img_data = requests.get(link).content
        with open(f'images/{filename}.jpg', 'wb') as f:
            f.write(img_data)