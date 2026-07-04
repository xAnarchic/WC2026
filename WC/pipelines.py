# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# useful for handling different item types with a single interface
import _mysql_connector
import mysql.connector as connector
from mysql.connector import errorcode
from WC.items import Wcteam, Wcplayer


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

        teams_table = """CREATE TABLE IF NOT EXISTS teams1(
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

        players_table = """CREATE TABLE IF NOT EXISTS players1(
                                        name VARCHAR(255),
                                        position VARCHAR(255),
                                        country VARCHAR(255)
                                            )"""

        player_stats = """



                                    """

        self.connection.cursor().execute(teams_table)
        self.connection.cursor().execute(players_table)


    #Handling items separately

    def process_item(self,item):

        self.table_creation()

        # print("----------------------------")
        # print(item, "+++", type(item), type(wcteam1), type(wcplayer1))
        #Currently makes tables but need to get the item handling to work

        player_stats = """



                                            """
        wcteam = Wcteam()
        wcplayer = Wcplayer()

        #Problem with getting items to their respective methods
        if type(item) == type(wcteam):
            print(item, "+++++++++++++++++")
            # return self.process_wcteam(wcteam = item)
        elif type(item) == type(wcplayer):
            print(item, "////////////////")
            # yield self.process_wcplayer(wcplayer = item)

    #Handling wcteam items
    def process_wcteam(self, wcteam):

        add_teams = ("INSERT INTO teams1"
                    "(country, group_name, group_pos, games_played, wins, draws, losses, goals_scored, goals_conceded, points)"
                    "VALUES (%(country)s, %(group_name)s, %(group_pos)s, "
                     "%(games_played)s, %(wins)s, %(draws)s, %(losses)s, "
                     "%(goals_scored)s, %(goals_conceded)s, %(points)s)")

        team_dict = dict(wcteam)
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

    # #Handling wcplayer items
    def process_wcplayer(self, wcplayer):

        add_players = ("INSERT INTO players1"
                       "(name, position, country)"
                       "VALUES (%(name)s, %(position)s, %(country)s)")


        player_dict = dict(wcplayer)

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


    def close_spider(self, spider):
        self.connection.cursor().close()
        self.connection.close()