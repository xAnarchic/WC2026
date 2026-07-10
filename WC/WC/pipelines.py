# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# useful for handling different item types with a single interface
import _mysql_connector
import mysql.connector as connector
from mysql.connector import errorcode
from WC.items import Wcteam, Wcplayer, Goldenbootdata, Attacking
from scrapy.exceptions import CloseSpider


# class WcPipeline:
#     #Immediate team and player item processing
#     def process_item(self, item):
#         pass


class ImportToMySQLPipeline:
    #SQL database connection
    def __init__(self):

        try:
            self.connection = connector.connect(
                host = 'localhost',
                user = 'root',  #Replace this so user has to enter username
                password = 'root',      #Replace this so user has to enter pass
                database = 'wc2026'   #Replace this so user has to enter database name
            )

        except connector.Error as err:
            if err.errno == connector.errorcode.ER_ACCESS_DENIED_ERROR:
                print('Cannot sign in')
            elif err is None:
                print("Successful connection")
            else:
                print({err}, "----")


    #Creating tables within database
    def table_creation(self):

        teams_table = """CREATE TABLE IF NOT EXISTS teams(
                                    id INT NOT NULL auto_increment,
                                    country VARCHAR(255),
                                    group_name VARCHAR(255),
                                    group_pos INT,
                                    games_played INT,
                                    wins INT,
                                    draws INT,
                                    losses INT,
                                    goals_scored INT,
                                    goals_conceded INT,
                                    points INT,
                                    primary key (id)
                                        )"""

        players_table = """CREATE TABLE IF NOT EXISTS players(
                                        name VARCHAR(255),
                                        position VARCHAR(255),
                                        country VARCHAR(255)
                                            )"""

        golden_boot_table = """CREATE TABLE IF NOT EXISTS goldenboot(
                                        name VARCHAR(255),
                                        position VARCHAR(255),
                                        country VARCHAR(255),
                                        goals INT,
                                        assists INT, 
                                        minutes INT
                                            )"""

        attacking_table = """CREATE TABLE IF NOT EXISTS attacking(
                                        name VARCHAR(255),
                                        assists VARCHAR(255),
                                        on_target_attempts VARCHAR(255),
                                        total_goal_attempts VARCHAR(255),
                                        attempts_in_box VARCHAR(255), 
                                        attempts_outside_box VARCHAR(255),
                                        total_header_attempts VARCHAR(255),
                                        expected_goals VARCHAR(255),
                                        expected_goal_efficiency VARCHAR(255), 
                                        corners VARCHAR(255)
                                            )"""

        self.connection.cursor().execute(teams_table)
        self.connection.cursor().execute(players_table)
        self.connection.cursor().execute(golden_boot_table)
        self.connection.cursor().execute(attacking_table)



    #Handling items separately

    def process_item(self,item):

        self.table_creation()

        wcteam = Wcteam()
        wcplayer = Wcplayer()
        golden_boot = Goldenbootdata()
        attacking = Attacking()

        #Problem with getting items to their respective methods
        if type(item) == type(wcteam):
            print(item, "+++++++++++++++++")
            return self.process_wcteam(item)
        elif type(item) == type(wcplayer):
            print(item, "////////////////")
            return self.process_wcplayer(item)
        elif type(item) == type(golden_boot):
            print(item, "----------------")
            return self.process_golden_boot(item)
        elif type(item) == type(attacking):
            print(item, "----------------")
            return self.process_attacking(item)

    #Handling wcteam items
    def process_wcteam(self, item):

        add_teams = ("INSERT INTO teams1"
                    "(country, group_name, group_pos, games_played, wins, draws, losses, goals_scored, goals_conceded, points)"
                    "VALUES (%(country)s, %(group_name)s, %(group_pos)s, "
                     "%(games_played)s, %(wins)s, %(draws)s, %(losses)s, "
                     "%(goals_scored)s, %(goals_conceded)s, %(points)s)")

        team_dict = dict(item)
        team_data = {
            "country" : team_dict["name"],
            "group_name" : team_dict["group_name"],
            "group_pos": team_dict["pos"],
            "games_played": team_dict["played"],
            "wins": team_dict["wins"],
            "draws": team_dict["draws"],
            "losses": team_dict["losses"],
            "goals_scored": team_dict["goals_scored"],
            "goals_conceded": team_dict["goals_allowed"],
            "points": team_dict["pts"]
                                                }

        try:
            self.connection.cursor().execute(add_teams, team_data)

        except _mysql_connector.MySQLError as error:
            print(f"Error importing data: {error}")
            pass

        self.connection.commit()

    # #Handling wcplayer items
    def process_wcplayer(self, item):

        add_players = ("INSERT INTO players1"
                       "(name, position, country)"
                       "VALUES (%(name)s, %(position)s, %(country)s)")


        player_dict = dict(item)

        player_data = {
            "name": player_dict["player"],
            "position": player_dict["player_position"],
            "country": player_dict["country"]
                                                }

        try:
            self.connection.cursor().execute(add_players, player_data)

        except _mysql_connector.MySQLError as error:
            print(f"Error importing data: {error}")
            pass

        self.connection.commit()

        # #Handling wcplayer items
    def process_golden_boot(self, item):

        add_golden_boot = ("INSERT INTO goldenboot"
                       "(name, position, country, goals, assists, minutes)"
                       "VALUES (%(name)s, %(position)s, %(country)s, %(goals)s, %(assists)s,"
                           "%(minutes)s)")

        golden_boot_dict = dict(item)

        golden_boot_data = {
            "name": golden_boot_dict["player"],
            "position": golden_boot_dict["position"],
            "country": golden_boot_dict["team"],
            "goals": golden_boot_dict["goals"],
            "assists": golden_boot_dict["assists"],
            "minutes": golden_boot_dict["minutes"]
        }

        try:
            self.connection.cursor().execute(add_golden_boot, golden_boot_data)

        except _mysql_connector.MySQLError as e:
            print(f"Error importing data for golden boot: {e}")
            raise CloseSpider

        self.connection.commit()

    def process_attacking(self, item):

        add_attacking = ("INSERT INTO attacking"
                       "(name, assists, on_target_attempts, total_goal_attempts, attempts_in_box, attempts_outside_box,"
                         "total_header_attempts, expected_goals, expected_goal_efficiency, corners)"
                       "VALUES (%(name)s, %(assists)s, %(on_target_attempts)s, %(total_goal_attempts)s, %(attempts_in_box)s,"
                           "%(attempts_outside_box)s, %(total_header_attempts)s, %(expected_goals)s, %(expected_goal_efficiency)s,"
                         "%(corners)s)")

        attacking_dict = dict(item)

        attacking_data = {
            "name": attacking_dict["player"],
            "assists": attacking_dict["assists"],
            "on_target_attempts": attacking_dict["on_target_attempts"],
            "total_goal_attempts": attacking_dict["total_goal_attempts"],
            "attempts_in_box": attacking_dict["attempts_in_box"],
            "attempts_outside_box": attacking_dict["attempts_outside_box"],
            "total_header_attempts": attacking_dict["total_header_attempts"],
            "expected_goals": attacking_dict["expected_goals"],
            "expected_goal_efficiency": attacking_dict["expected_goal_efficiency"],
            "corners": attacking_dict["corners"]
        }

        try:
            self.connection.cursor().execute(add_attacking, attacking_data)

        except _mysql_connector.MySQLError as e:
            print(f"Error importing data for golden boot: {e}")
            raise CloseSpider

        self.connection.commit()


    def close_spider(self, spider):
        self.connection.cursor().close()
        self.connection.close()