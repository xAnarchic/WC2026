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


# Ensure JavaScript-loaded content is fully visible by scrolling

        self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)

        time.sleep(7) # Allow time for content to load


# Parse page source with BeautifulSoup

        soup = BeautifulSoup(self.driver.page_source, "html.parser")


# Extract product details

        for team in soup.find_all("tr", class_="standings-table-row_tableRow__IZhv4"):

            team_page_link = "fifa.com" +  team.find("a", class_="table-team-name_teamLink__qDRZ4").get('href')
#"fifa.com" +
            # yield team_page_link
            # rand_text = response.css("div.standings-table-head_text__NDynK::text")
            yield Request(url = team_page_link, callback = self.parse_team)
            # yield rand_text


            ###### Need to properly understand how response and request objects work in scrapy + how to use them to move between diff functions using callbacks

            #
            # yield {
            #
            #     "team_name": team.find("span", class_ = "d-none d-md-1024-block").get_text(),
            #     "group_rank": team.find("td", class_= "standings-table-row_index__lfMgF d-xs-table-cell d-md-table-cell").get_text(),
            #
            #     }




        self.driver.quit() # Close browser session
        # yield {'response': response}

    def parse_team(self, response):
        print("--------------------------------------")
        self.driver.get(response.url)

        # Ensure JavaScript-loaded content is fully visible by scrolling

        self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)

        time.sleep(7)  # Allow time for content to load

        # Parse page source with BeautifulSoup

        soup1 = BeautifulSoup(self.driver.page_source, "html.parser")

        #1: check main article for "squad" in title
        #2: check the 4 articles to the side of it
        #3: open "see more" link, then check the articles there
        #4: filler vals if still not found



        # WcItem['squad_link'] = soup1.find('')

        yield WcItem