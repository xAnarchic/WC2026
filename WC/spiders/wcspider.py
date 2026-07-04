import time

import scrapy
import re

from scrapy import Request
from selenium import webdriver


from selenium.webdriver.common.by import By

from selenium.webdriver.common.keys import Keys

from bs4 import BeautifulSoup

from WC.items import Wcteam, Wcplayer

from itemadapter import ItemAdapter

# from WC.WC.items import Wcteam, Wcplayer


class WCspider(scrapy.Spider):
    name = "wcspider"
    allowed_domains = "fifa.com"
    start_urls = ["https://www.fifa.com/en/tournaments/mens/worldcup/canadamexicousa2026/standings"]

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

        for group in soup.find_all("div", class_="standings-table_standingsTableContainer__zCpm2 standings-table_expandedTable__47Don"):
            group_name = group.find("div", class_="standings-table-head_text__NDynK").string
            # yield group_name

            teams = group.find_all("tr", attrs = {"tabindex" : "0"})
                #check if other teams are present
            for team in teams:
                wcteam = Wcteam()

                wcteam["group_name"] = group_name
                wcteam["pos"] = team.find("td", class_="standings-table-row_index__lfMgF d-xs-table-cell d-md-table-cell d-md-1024-table-cell").string
                wcteam["name"] = team.find("span", class_="d-none d-md-1024-block").string
                team_stats = team.find_all("td", class_="standings-table-row_stats__8X9fU d-xs-table-cell d-md-table-cell d-md-1024-table-cell")
                wcteam["played"] = team_stats[0].string
                wcteam["wins"] = team_stats[1].string
                wcteam["draws"] = team_stats[2].string
                wcteam["losses"] = team_stats[3].string
                team_goal_stats = team.find_all("td", class_="standings-table-row_stats__8X9fU d-none d-md-table-cell d-md-1024-table-cell")
                wcteam["goals_scored"] = team_goal_stats[0].string
                wcteam["goals_allowed"] = team_goal_stats[1].string
                wcteam["pts"] = team.find("td", class_="standings-table-row_stats__8X9fU standings-table-row_points__A+pD8 d-xs-table-cell d-md-table-cell d-md-1024-table-cell").string
                yield wcteam, print("hi")


                team_page_link = "https://www.fifa.com" +  team.find("a", class_="table-team-name_teamLink__qDRZ4").get('href')

                yield Request(url = team_page_link, callback = self.parse_teampage, dont_filter=True,
                              headers = {
                    "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                                   "Chrome/120.0.0.0 Safari/537.36"}
                              ,cb_kwargs = {
                                  "country" : wcteam["name"]
                              }
                )



        # self.driver.quit() # Close browser session


    def parse_teampage(self, response, country):
        self.driver.get(response.url)
        self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)

        time.sleep(3)  # Allow time for content to load

        soup1 = BeautifulSoup(self.driver.page_source, "html.parser")


        names1 = soup1.find_all("div", class_ = "player-badge-card_playerName__NHS1e")
        positions = soup1.find_all("div", class_ = "player-badge-card_playerPosition__+uSwv")

        for x,y in zip(names1, positions):
            wcplayer = Wcplayer()

            name = x.find("span", class_ = "d-md-none").get_text()
            pos = y.find("span", class_="d-md-none").get_text()

            wcplayer["player"] = name
            wcplayer["player_position"] = pos
            wcplayer["country"] = country
            yield wcplayer, print("hi")


