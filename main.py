from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from parser import Parser


def main():
    parser: Parser = Parser()

    link = parser.get_part_link("re539279")
    
    parser.get_page_data(link, "re539279")

if __name__ == "__main__":
    main()