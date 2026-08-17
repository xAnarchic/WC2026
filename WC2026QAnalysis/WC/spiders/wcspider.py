import time
import scrapy
from scrapy import Request
from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.common.by import By
from scrapy.exceptions import CloseSpider
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from WC.items import Wcteam, Wcplayer, Goldenbootdata, Attacking, Distribution, Defending, Discipline, Goalkeeping, Movement, Physical
import selenium.webdriver.common.action_chains as action



#Spider to gather team and player data
class WCspider(scrapy.Spider):
    name = "wcspider"
    allowed_domains = "fifa.com"
    start_urls = ["https://www.fifa.com/en/tournaments/mens/worldcup/canadamexicousa2026/standings"]

    def __init__(self):
        service = webdriver.EdgeService()
        options = webdriver.EdgeOptions()
        self.driver = webdriver.Edge(service=service, options=options)

    #Parses the standings page to yield team details
    def parse(self, response):
        self.driver.get(response.url)

        # Reject cookies
        pop_up_ele = self.driver.find_element(By.ID, "onetrust-reject-all-handler")
        pop_up_ele.click()

        #Full screen
        self.driver.fullscreen_window()
        time.sleep(7)

        #Scroll to the bottom of the page and wait for content to load
        self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
        time.sleep(5)

        #Extract page html
        soup = BeautifulSoup(self.driver.page_source, "html.parser")

        #Extracting team details
        for group in soup.find_all("div", class_="standings-table_standingsTableContainer__zCpm2 standings-table_expandedTable__47Don"):
            group_name = group.find("div", class_="standings-table-head_text__NDynK").string

            teams = group.find_all("tr", attrs = {"tabindex" : "0"})
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

                #Calls the parse_teampage function on each team's page
                yield Request(
                    url = team_page_link, callback = self.parse_teampage, dont_filter=True,
                    headers = {
                        "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                                       "Chrome/120.0.0.0 Safari/537.36"
                    },
                    cb_kwargs = {
                        "country" : wcteam["name"]
                    })

    #Parses individual team pages to extract player details
    def parse_teampage(self, response, country):
        self.driver.get(response.url)

        #Full screen
        self.driver.fullscreen_window()
        time.sleep(3)

        #Scroll to the bottom of the page and wait for player information to load
        self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
        time.sleep(5)

        #Extract page html
        soup1 = BeautifulSoup(self.driver.page_source, "html.parser")
        time.sleep(5)

        #Extract list of player names and positions
        names = soup1.find_all("div", class_ = "player-badge-card_playerName__NHS1e")
        positions = soup1.find_all("div", class_ = "player-badge-card_playerPosition__+uSwv")

        #Unpack lists together
        for x,y in zip(names, positions):

            wcplayer = Wcplayer()

            #Extract the elements at the same index of each list to get a player's name and corresponding position
            name = x.find("span", class_ = "d-md-none").get_text()
            position = y.find("span", class_="d-md-none").get_text()

            wcplayer["player"] = name
            wcplayer["player_position"] = position
            wcplayer["country"] = country

            yield wcplayer


class WCspiderstats(scrapy.Spider):
    name = "statsspider"
    allowed_domains = "fifa.com"
    start_urls = ["https://www.fifa.com/en/tournaments/mens/worldcup/canadamexicousa2026/statistics/player-statistics"]

    def __init__(self):
        service = webdriver.EdgeService()
        options = webdriver.EdgeOptions()
        self.driver = webdriver.Edge(service=service, options=options)

    #Click, scroll and parse each category of stats
    def parse(self, response):
        self.driver.get(response.url)

        #Full screen
        self.driver.fullscreen_window()
        time.sleep(7)

        #Reject cookies
        pop_up_ele = self.driver.find_element(By.ID, "onetrust-reject-all-handler")
        pop_up_ele.click()

        #Identifies buttons for each category of stats
        buttons_for_categories_elements = self.driver.find_elements(By.CLASS_NAME, "fdsp-reset-button")

        #Iterates over each button atop the page, skipping the "All teams" button
        for button_element in buttons_for_categories_elements[0:-2]:

            #Move to top of the page
            self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.HOME)

            #Click on category and allow for time to load the data
            button_element.click()
            time.sleep(10)

            #Identifying the page being currently parsed
            button_element_str = ''.join(button_element.text)
            print(f"--- Parsing the page looking at {button_element_str} stats ---")

            #Load all available data on the page by clicking the "load more" button and scrolling to the
            #bottom of the page
            self.loading_and_scrolling(response)
            print(f"Done scrolling for {button_element_str}")

            #Parse data for each category of stats, depending on the category page most recently scrolled
            if button_element_str == "adidas Golden Boot":
                yield from self.parsing_golden_boot(response)

            elif button_element_str == "Attacking":
                yield from self.parsing_attacking(response)

            elif button_element_str == "Distribution":
                yield from self.parsing_distribution(response)

            elif button_element_str == "Defending":
                yield from self.parsing_defending(response)

            elif button_element_str == "Discipline":
                yield from self.parsing_discipline(response)

            elif button_element_str == "Goalkeeping":
                yield from self.parsing_goalkeeping(response)

            elif button_element_str == "Movement":
                yield from self.parsing_movement(response)

            elif button_element_str == "Physical":
                yield from self.parsing_physical(response)

            else:
                print("All data collected")
                raise CloseSpider("")


    #Clicks the "load more" button and scrolls down the page until there is no more data to load
    def loading_and_scrolling(self, response, times_loaded= 0):

        # time.sleep(5) increased the sleep before this function's call to 10s to reduce code redundancy

        #Locate the "load more" button at the bottom of the page
        element = self.driver.find_element(By.CSS_SELECTOR, "span.button-label")

        #So long as the "load more" button is on the page, scroll down to it
        while element is not None:
            times_loaded += 1
            action.ActionChains(self.driver).scroll_to_element(element)
            element.click()

            #Pause to allow the data to load before searching for the next "load more" button
            time.sleep(3)

            #Check to see if there's another "load more button"
            try:
                element = self.driver.find_element(By.CSS_SELECTOR, "span.button-label")

            #No button means no more scrolling should be attempted
            except exceptions.NoSuchElementException:
                print("Broke loop- there is no more data to load")
                break

            #Track how many times more data was loaded on the page
            print(f"Loaded more data {times_loaded} times")

    #Parse the "adidas Golden boot" stats category
    def parsing_golden_boot(self, response):

        #Give time to scrape data
        time.sleep(10)

        #Create a separate list of player names, their teams and positions
        names = self.driver.find_elements(By.CSS_SELECTOR, "div.main-text")
        teams = self.driver.find_elements(By.CSS_SELECTOR, "span.dsk-description")
        positions = self.driver.find_elements(By.CSS_SELECTOR, "span.dsk-description-info")

        #Collect goal, assist and minutes played data collectively in a single list
        goals_assists_mins = self.driver.find_elements(By.CSS_SELECTOR, "span.value")


        #Initialise index value for the goal, assist, minutes played list
        a = 0

        #Empty list to store their values as integers instead of strings into
        gam = []

        #Convert goals, assists, minutes played data from their collected string form into integers, storing them
        for gam_data in goals_assists_mins:
            gam.append(int(gam_data.text))

        #Map data from the individual name, team and position lists to their respective players
        for name, team, position in zip(names, teams, positions):

            #Ensure indexing remains valid
            if a != len(gam):
                golden_boot = Goldenbootdata()
                golden_boot["player"] = name.text
                golden_boot["team"] = team.text
                golden_boot["position"] = position.text
                golden_boot["goals"] = gam[a]
                golden_boot["assists"] = gam[a+1]
                golden_boot["minutes"] = gam[a+2]

                yield golden_boot

                #Increment index variable by 3 to collect the next 3 pieces of goals/assists/minutes played data
                a += 3

        #Pause to allow processes to complete before proceeding to next category
        time.sleep(5)


    #Parse the "Attacking" stats category
    def parsing_attacking(self, response):

        #Capturing data, maybe add the country + position data too
        #Give time to scrape data
        time.sleep(10)
        player_names = self.driver.find_elements(By.CSS_SELECTOR, "div.main-text")
        all_attacking_stats = self.driver.find_elements(By.CSS_SELECTOR, "span.value")

        stats_str = []
        for stat in all_attacking_stats:
            stats_str.append(stat.text)

        a = 0
        for player in player_names:
            if a != len(stats_str):
                attacking = Attacking()
                attacking["player"] = player.text
                attacking["assists"] = stats_str[a]
                attacking["on_target_attempts"] = stats_str[a+1]
                attacking["total_goal_attempts"] = stats_str[a+2]
                attacking["attempts_in_box"] = stats_str[a+4]
                attacking["attempts_outside_box"] = stats_str[a+5]
                attacking["total_header_attempts"] = stats_str[a+6]
                attacking["expected_goals"] = stats_str[a+7]
                attacking["expected_goal_efficiency"] = stats_str[a+8]
                attacking["corners"] = stats_str[a+9]

                yield attacking
                a += 10

        time.sleep(5)

        print("Took a pause of 5 secs at the end of the parse instead of using an input")

        # if input() == "r":
        #     pass
        # else:
        #     raise CloseSpider("")

    #Parse the "Distribution" stats category
    def parsing_distribution(self, response):

        #Collecting data
        players = self.driver.find_elements(By.CSS_SELECTOR, "div.main-text")
        all_data = self.driver.find_elements(By.CSS_SELECTOR, "span.value")

        all_data_str = []
        for stat in all_data:
            all_data_str.append(stat.text)

        a = 0
        for player in players:
            if a != len(players):
                distribution = Distribution()
                distribution["player"] = player.text
                distribution["passes"] = all_data_str[a]
                distribution["passing_accuracy_percentage"] = all_data_str[a+1]
                distribution["crosses"] = all_data_str[a+2]
                distribution["crossing_accuracy_percentage"] = all_data_str[a+3]
                distribution["defensive_linebreaks_att"] = all_data_str[a+4]
                distribution["defensive_linebreak_acc"] = all_data_str[a+5]
                distribution["switches_att"] = all_data_str[a+6]
                distribution["switch_acc"] = all_data_str[a+7]

                yield distribution
                a += 8

        time.sleep(5)

        print("Took a pause of 5 secs at the end of the parse instead of using an input")

        # print("Make sure it's on screen, then press r")
        # if input() == "r":
        #     pass
        # else:
        #     raise CloseSpider("")

    #Parse the "Defending" stats category
    def parsing_defending(self, response):

        #Collecting data
        players = self.driver.find_elements(By.CSS_SELECTOR, "div.main-text")
        all_data = self.driver.find_elements(By.CSS_SELECTOR, "span.value")

        all_data_str = []
        for stat in all_data:
            all_data_str.append(stat.text)

        a = 0
        for player in players:
            if a != len(players):
                defending = Defending()
                defending["player"] = player.text
                defending["own_goals"] = all_data_str[a]
                defending["forced_turnovers"] = all_data_str[a+1]
                defending["def_pressures"] = all_data_str[a+2]
                defending["direct_def_pressures"] = all_data_str[a+3]

                yield defending
                a += 4

        time.sleep(5)

        print("Took a pause of 5 secs at the end of the parse instead of using an input")

        # print("Make sure it's on screen, then press r")
        # if input() == "r":
        #     pass
        # else:
        #     raise CloseSpider("")

    #Parse the "Discipline" stats category
    def parsing_discipline(self, response):

        #Collecting data
        players = self.driver.find_elements(By.CSS_SELECTOR, "div.main-text")
        all_data = self.driver.find_elements(By.CSS_SELECTOR, "span.value")

        all_data_str = []
        for stat in all_data:
            all_data_str.append(stat.text)

        a = 0
        for player in players:
            if a != len(players):
                discipline = Discipline()
                discipline["player"] = player.text
                discipline["fouls_against"] = all_data_str[a]
                discipline["fouls_for"] = all_data_str[a+1]
                discipline["yellow_cards"] = all_data_str[a+2]
                discipline["red_cards"] = all_data_str[a+3]
                discipline["indirect_reds"] = all_data_str[a+4]

                yield discipline
                a += 5

        time.sleep(5)

        print("Took a pause of 5 secs at the end of the parse instead of using an input")

        # print("Make sure it's on screen, then press r")
        # if input() == "r":
        #     pass
        # else:
        #     raise CloseSpider("")

    #Parse the "Goalkeeping" stats category
    def parsing_goalkeeping(self, response):

        #Collecting data
        players = self.driver.find_elements(By.CSS_SELECTOR, "div.main-text")
        all_data = self.driver.find_elements(By.CSS_SELECTOR, "span.value")

        all_data_str = []
        for stat in all_data:
            all_data_str.append(stat.text)

        a = 0
        for player in players:
            if a != len(players):
                goalkeeping = Goalkeeping()
                goalkeeping["player"] = player.text
                goalkeeping["saves"] = all_data_str[a]
                goalkeeping["gk_actions_in_box"] = all_data_str[a+1]
                goalkeeping["gk_actions_outside_box"] = all_data_str[a+2]

                yield goalkeeping
                a += 3

        time.sleep(5)

        print("Took a pause of 5 secs at the end of the parse instead of using an input")

        # print("Make sure it's on screen, then press r")
        # if input() == "r":
        #     pass
        # else:
        #     raise CloseSpider("")

    #Parse the "Movement" stats category
    def parsing_movement(self, response):

        #Collecting data
        players = self.driver.find_elements(By.CSS_SELECTOR, "div.main-text")
        all_data = self.driver.find_elements(By.CSS_SELECTOR, "span.value")

        all_data_str = []
        for stat in all_data:
            all_data_str.append(stat.text)

        a = 0
        for player in players:
            if a != len(players):
                movement = Movement()
                movement["player"] = player.text
                movement["total_offers_to_receive_ball"] = all_data_str[a]
                movement["offers_behind_def_line"] = all_data_str[a+1]
                movement["offers_between_def_units"] = all_data_str[a+2]
                movement["offers_ahead_def_line"] = all_data_str[a+3]
                movement["offers_inside_shape"] = all_data_str[a+4]
                movement["receptions_in_behind"] = all_data_str[a+5]
                movement["receptions_between_mid_and_def_lines"] = all_data_str[a+6]
                movement["receptions_under_pressure"] = all_data_str[a+7]
                movement["player_involvements"] = all_data_str[a+8]

                yield movement
                a += 9

        time.sleep(5)

        print("Took a pause of 5 secs at the end of the parse instead of using an input")

        # print("Make sure it's on screen, then press r")
        # if input() == "r":
        #     pass
        # else:
        #     raise CloseSpider("")

    # #Parse the "Physical" stats category
    def parsing_physical(self, response):

        #Collecting data
        players = self.driver.find_elements(By.CSS_SELECTOR, "div.main-text")
        all_data = self.driver.find_elements(By.CSS_SELECTOR, "span.value")

        all_data_str = []
        for stat in all_data:
            all_data_str.append(stat.text)

        a = 0
        for player in players:
            if a != len(players):
                physical = Physical()

                physical["player"] = player.text
                physical["average_speed"] = all_data_str[a]
                physical["high_speed_running"] = all_data_str[a+1]
                physical["sprints"] = all_data_str[a+2]
                physical["total_distance"] = all_data_str[a+3]

                yield physical
                a += 4

        time.sleep(5)

        print("Took a pause of 5 secs at the end of the parse instead of using an input")

        # print("Make sure it's on screen, then press r")
        # if input() == "r":
        #     pass
        # else:
        #     raise CloseSpider("")



