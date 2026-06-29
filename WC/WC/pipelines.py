# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import _mysql_connector
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import mysql.connector as connector
from mysql.connector import errorcode
from .items import Wcteam, Wcplayer

# class WcPipeline:
#     def process_item(self, Wcteam = None):
#         if Wcteam is None:
#             Wcteam = (10*[0])
#         # else:
#         #     Wcteam = ItemAdapter(Wcteam)
#
#         return Wcteam

    # def process_item1(self, Wcplayer = None):
    #     if Wcplayer is None:
    #         Wcplayer = (3 * [0])
    #     else:
    #         Wcplayer = ItemAdapter(Wcplayer)
    #
    #     return Wcplayer

class ImportToMySQLPipeline:
    def __init__(self):
        #handle both incoming items in process_item method
        #reroute to different methods depending on the item to be processed

        try:
            self.connection = connector.Connect(
                host = 'localhost',
                user = 'root',
                password = 'root',      # enter account password
                database = 'wc2026'   # enter name of database
            )
        except connector.Error as err:
            if err.errno == connector.errorcode.ER_ACCESS_DENIED_ERROR:
                print('Cannot sign in')
            else:
                print({err})

        self.cursor = self.connection.cursor()

    # def process_spider_output(self, wcteam, wcplayer):

        #Neatness: make diff funcs to make table + import data
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

        player_stats = """
        
        
                            
                            """


        add_players = ("INSERT INTO players"
                       "(name, position, country)"
                       "VALUES (%s, %s, %s);")



        # player_data = (
        #     Wcplayer[0],
        #     Wcplayer[1],
        #     Wcplayer[2]
        #                 )

        player_stats = {



        }

        self.cursor.execute(teams_table)
        self.cursor.execute(players_table)

        # try:
        #     self.cursor.execute(add_players, player_data)
        #     self.cursor.execute(add_teams, team_data)
        #
        # except _mysql_connector.MySQLError as error:
        #     print(f"Error importing data: {error}")
        #     pass
        #
        # self.connection.commit()

    def process_wcteam(self, Wcteam):
        add_teams = ("INSERT INTO teams"
                    "(country, group_name, group_pos, games_played, wins, draws, losses, goals_scored, goals_conceded, points)"
                    "VALUES (%(country)s, %(group_name)s, %(group_pos)s, "
                     "%(games_played)s, %(wins)s, %(draws)s, %(losses)s, "
                     "%(goals_scored)s, %(goals_conceded)s, %(points)s)")

        # print(tuple(Wcteam))
        # print(dict(Wcteam)["country"],"+++++++")
        # print(Wcteam["country"], "--------")

        team_dict = dict(Wcteam)
        print("testing", team_dict["name"])
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
            self.cursor.execute(add_teams, team_data)

        except _mysql_connector.MySQLError as error:
            print(f"Error importing data: {error}")
            pass

        self.connection.commit()


    def close_spider(self, spider):
        self.cursor.close()
        self.connection.close()