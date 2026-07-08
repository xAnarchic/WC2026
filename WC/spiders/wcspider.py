import time

import scrapy
import re

import selenium.common.exceptions
from scrapy import Request
from selenium import webdriver
from selenium.common import ElementClickInterceptedException, exceptions
from selenium.webdriver.common.by import By

from selenium.webdriver.common.keys import Keys

from bs4 import BeautifulSoup
import selenium.webdriver.remote.webelement as webele


from WC.items import Wcteam, Wcplayer

from selenium.webdriver.remote.errorhandler import ErrorCode
import selenium.webdriver.common.action_chains as action


import sys

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
                yield wcteam


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


        names1 = soup1.find_all("div", class_g = "player-badge-card_playerName__NHS1e")
        positions = soup1.find_all("div", class_ = "player-badge-card_playerPosition__+uSwv")

        for x,y in zip(names1, positions):
            wcplayer = Wcplayer()

            name = x.find("span", class_ = "d-md-none").et_text()
            pos = y.find("span", class_="d-md-none").get_text()

            wcplayer["player"] = name
            wcplayer["player_position"] = pos
            wcplayer["country"] = country
            yield wcplayer


class WCspiderstats(scrapy.Spider):
    name = "statsspider"
    allowed_domains = "fifa.com"
    start_urls = ["https://www.fifa.com/en/tournaments/mens/worldcup/canadamexicousa2026/statistics/player-statistics"]

    def __init__(self):

        service = webdriver.EdgeService() # Ensure ChromeDriver is installed
        options = webdriver.EdgeOptions()
        options.add_argument("–headless") # Run without opening a browser
        self.driver = webdriver.Edge(service=service, options=options)


    def parse(self, response):

        self.driver.get(response.url)
        self.driver.fullscreen_window()

        #Loading time for initial page
        time.sleep(7)

        #Reject cookies
        pop_up_ele = self.driver.find_element(By.ID, "onetrust-reject-all-handler")
        pop_up_ele.click()

        #Click, scroll and parse each category of stats

        #Identifies buttons for each category of stats
        buttons_for_categories_elements = self.driver.find_elements(By.CLASS_NAME, "fdsp-reset-button")

        #Iterates over each button atop the page, skipping the "All teams" button
        for button_element in buttons_for_categories_elements[:-1]:

            #Move to top of the page
            self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.HOME)

            #Click on category and allow for time to load the data
            button_element.click()
            time.sleep(5)

            button_element_str = ''.join(button_element.text)

            print(f"--- Parsing the page looking at {button_element_str} data ---")

            #Load all available data on the page
            self.loading_and_scrolling(response)

            #Parse data for each category of stats, only once the page has been fully scrolled (meaning all data
            #can be accessed

            #For the "adidas Golden boot" category
            if button_element_str == "adidas Golden Boot":
                self.parsing_golden_boot(response)
                print("Finished parsing golden boot stats, ready to continue? y/n?")
                if input() == "y":
                    continue
                else:
                    sys.exit()

            elif button_element_str == "Attacking":
                self.parsing_attacking(response)
                print("Finished parsing attacking stats, ready to continue? y/n?")
                if input() == "y":
                    continue
                else:
                    sys.exit()

            elif button_element_str == "Distribution":
                pass

            elif button_element_str == "Defending":
                pass

            elif button_element_str == "Discipline":
                pass

            elif button_element_str == "Goalkeeping":
                pass

            elif button_element_str == "Movement":
                pass

            elif button_element_str == "Physical":
                pass
            else:
                print("All data collected")
                sys.exit()

    #Scrolls down the page, loading additional data
    def loading_and_scrolling(self, response, times_loaded= 0):

        time.sleep(5)

        #Locate the "load more" button at the bottom of the page
        element = self.driver.find_element(By.CSS_SELECTOR, "span.button-label")

        #So long as the "load more" button is on the page, scroll down to it
        while element is not None:
            times_loaded += 1
            # time.sleep(5)
            action.ActionChains(self.driver).scroll_to_element(element)
            element.click()
            time.sleep(3)

            #Check to see if there's another "load more button"
            try:
                element = self.driver.find_element(By.CSS_SELECTOR, "span.button-label")
            #No button means no more scrolling should be attempted
            except exceptions.NoSuchElementException:
                break

            #Track how many times additional data was loaded on the page
            print(f"Loaded additional data {times_loaded} times")

    #Parse the "adidas Golden boot" stats category
    def parsing_golden_boot(self, response):

        #Capture all name, team, position, goal, assist and minutes played data
        names = self.driver.find_elements(By.CSS_SELECTOR, "div.main-text")
        teams = self.driver.find_elements(By.CSS_SELECTOR, "span.dsk-description")
        positions = self.driver.find_elements(By.CSS_SELECTOR, "span.dsk-description-info")

        #Gather goal, assist and minutes played data altogether in a single list under the same CSS selector
        goals_assists_mins = self.driver.find_elements(By.CSS_SELECTOR, "span.value")

        #Initialise slicing values for the goals, assists, minutes list as well as the empty list to store their values,
        #as integers instead of strings, into
        a,b = 0,3
        gam = []

        #Convert goals, assists, minutes played data from their collected string form into integers, storing them
        for gam_data in goals_assists_mins:
            gam.append(int(gam_data.text))

        #Map data from the individual name, team and position lists to their respective players
        for w,x,y in zip(names, teams, positions):
            #Ensure the latter index of the slice remains valid
            if b <= len(gam):
                #Display the data for each respective player
                print(w.text,x.text,y.text,gam[a:b])
                #Increment the slicing indexes by 3, to collect the next 3 pieces of goals/assists/minutes played data
                a += 3
                b += 3

    #Parse the "Attacking" stats category
    def parsing_attacking(self, response):

        # Capturing data
        player_names = self.driver.find_elements(By.CSS_SELECTOR, "div.main-text")
        all_attacking_stats = self.driver.find_elements(By.CSS_SELECTOR, "span.value")

        stats_int = []
        for stat in all_attacking_stats:
            stats_int.append(int(stat.text))

        a = 0
        for player in player_names:
            if a != len(stats_int):
                assists = stats_int[a]
                on_target_attempts = stats_int[a+1]
                total_goal_attempts = stats_int[a+2]
                #Skipping "attempts at goal conversion rate %", can calculate instead of scraping
                attempts_in_box = stats_int[a+4]
                attempts_outside_box = stats_int[a+5]
                total_header_attempts = stats_int[a+6]
                expected_goals = stats_int[a+7]
                expected_goal_efficiency = stats_int[a+8]
                corners = stats_int[a+9]

                print(player, assists, on_target_attempts, total_goal_attempts, attempts_in_box, attempts_outside_box, total_header_attempts, expected_goals,
                      expected_goal_efficiency, corners)

                a += 10





