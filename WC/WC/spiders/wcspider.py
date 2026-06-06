import time

import scrapy
import re

from scrapy import Request
from selenium import webdriver


from selenium.webdriver.common.by import By

from selenium.webdriver.common.keys import Keys

from bs4 import BeautifulSoup

from WC.items import WcItem


class WCspider(scrapy.Spider):
    name = "wcspider"
    allowed_domains = "fifa.com"
    start_urls = ["https://www.fifa.com/en/tournaments/mens/worldcup/canadamexicousa2026/standings"]


    # def parse(self, response):
    #
    #     teams = response.css('')

# driver = webdriver.Edge()
# driver.get("https://www.fifa.com/en/tournaments/mens/worldcup/canadamexicousa2026/standings")
# time.sleep(10) # Allow time for content to load




    def __init__(self):


        service = webdriver.EdgeService() # Ensure ChromeDriver is installed

        options = webdriver.EdgeOptions()

        options.add_argument("–headless") # Run without opening a browser

        self.driver = webdriver.Edge(service=service, options=options)


    def parse(self, response):

        self.driver.get(response.url)
        self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
        time.sleep(5) # Allow time for content to load

        soup = BeautifulSoup(self.driver.page_source, "html.parser")

        for team in soup.find_all("tr", class_="standings-table-row_tableRow__IZhv4"):

            team_page_link = "https://www.fifa.com" +  team.find("a", class_="table-team-name_teamLink__qDRZ4").get('href')
            #self.driver.quit()
            # self.driver.get(team_page_link)
            # self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
            # team_soup = BeautifulSoup(self.driver.page_source, "html.parser")
            #
            # articles = "https://www.fifa.com" + team_soup.find("a", class_ = "ff-mb-0 carousel-header_seeAll__Aif3S").get('href')

            yield Request(url = team_page_link, callback = self.parse_teampage, dont_filter=True, headers = {
                "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"})


        # self.driver.quit() # Close browser session


    def parse_teampage(self, response):
        self.driver.get(response.url)
        self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)

        time.sleep(3)  # Allow time for content to load

        soup1 = BeautifulSoup(self.driver.page_source, "html.parser")

        #1: check main article for "squad" in title
        #2: check the 4 articles to the side of it
        #3: open "see more" link, then check the articles there
        #4: filler vals if still not found

        names1 = soup1.find_all("div", class_ = "player-badge-card_playerName__NHS1e")
        positions = soup1.find_all("div", class_ = "player-badge-card_playerPosition__+uSwv")

        name_list = []
        pos_list = []

        for x,y in zip(names1, positions):
            name = x.find("span", class_ = "d-md-none").get_text()
            pos = y.find("span", class_="d-md-none").get_text()

            yield {
                "name" : name,
                "position" : pos
            }
        # for names in names1:
        #     name = names.find("span", class_ = "d-md-none").get_text()
        # for position in positions:
        #     pos = position.find("span", class_ = "d-md-none").get_text()



        # print(name_list)
        # print(pos_list)
            # WcItem['squad_link'] = soup1.find('')

            #yield WcItem