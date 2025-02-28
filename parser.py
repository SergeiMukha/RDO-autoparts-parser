import time
import random
import requests

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

class RdoParser:
    def __init__(self):
        self.driver: webdriver.Chrome = webdriver.Chrome()

        self.driver.get("https://www.rdoequipment.com")
        self._accept_cookies()

    def get_part_link(self, art):
        self.driver.get(f"https://www.rdoequipment.com/search?query={art}")

        try: 
            link = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "part_title"))).get_attribute("href")
        except TimeoutException: return None

        if(art.lower() not in link): return None
        else: return link

    def get_page_data(self, link, art):
        self.driver.get(link)
        
        time.sleep(random.randint(3, 4))

        try:
            models_element = self.driver.find_element(By.ID, "product-info").find_element(By.TAG_NAME, "p")

            if("fits on" not in models_element.text.lower()): raise Exception()
            models = ", ".join(models_element.text.split("\n")[1:])
        except Exception as ex:
            models = None

        try:
            img_container = WebDriverWait(self.driver, 2).until(EC.presence_of_element_located((By.CLASS_NAME, "images_wrap")))

            # If there is a couple of elements then we have to grab the primary one in 650x650 resolution
            try:
                primary_image_container = img_container.find_element(By.CLASS_NAME, "pd_images_primary")
                img_link = primary_image_container.find_element(By.TAG_NAME, "img").get_attribute("src")
            except NoSuchElementException:
                img_link = img_container.find_element(By.TAG_NAME, "img").get_attribute("src")
            
            if img_link == "https://www.rdoequipment.com/images/default-source/parts-images/default_image_703x381.png": raise TimeoutException()
            if "650x650" not in img_link: print("Bad size")

            self._download_photo(img_link, art.replace("/", "-"))
        except TimeoutException: img_link = None

        return {
            "models": models,
            "img": img_link
        }

    # Accept cookies
    def _accept_cookies(self):
        try:
            accept_button = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.ID, "onetrust-accept-btn-handler")))
            accept_button.click()
        except TimeoutError:
            print("Couldn't accept cookies")

    # Downloads photo from the page
    def _download_photo(self, link: str, filename: str):
        img_data = requests.get(link).content
        with open(f'images/{filename}.jpg', 'wb') as f:
            f.write(img_data)