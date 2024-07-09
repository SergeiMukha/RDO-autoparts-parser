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

    def get_page_data(self, link):
        self.driver.get(link)

        try: WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "splide__slide")))
        except TimeoutException: return None

        img = self.driver.find_element(By.CLASS_NAME, "splide__slide").find_element(By.TAG_NAME, "img").get_attribute("src")
        print(img)