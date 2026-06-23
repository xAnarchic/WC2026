# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import mysql.connector as connector
from mysql.connector import errorcode
from items import WcItem

class WcPipeline:
    def process_item(self, WcItem):
        # item = ItemAdapter(WcItem)
        #
        return WcItem

class ImportToMySQLPipeline:
    def __init__(self):
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

        teams_table = """CREATE TABLE IF NOT EXISTS teams(
                            id int NOT NULL auto_increment,
                            country VARCHAR(255),
                            group VARCHAR(255),
                            group_pos INT,
                            primary key (id)
                                )"""

        players_table = """CREATE TABLE IF NOT EXISTS players(
                                name VARCHAR(255),
                                country VARCHAR(255),
                                goals INT,
                                assists INT
                                    )"""

        add_teams = ("INSERT INTO teams"
                    "(country, group, group_pos, games_played, wins, draws, losses,"
                     " goals_scored, goals_conceded, points)"
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")

        add_players = ("INSERT INTO players"
                       "(name, position, country)"
                       "VALUES (%s, %s, %s)")

        team_data = {
            "country" : WcItem[0],
            "group" : WcItem[1],
            "group_pos" : WcItem[2],
            "games_played": WcItem[3],
            "wins" : WcItem[4],
            "draws": WcItem[5],
            "losses": WcItem[6],
            "goals_scored": WcItem[7],
            "goals_conceded": WcItem[8],
            "points": WcItem[9],

                        }

        player_data = {
            "name": WcItem[10],
            "position": WcItem[11],
            "country": WcItem[12]
        }

        self.cursor.execute(teams_table)
        self.cursor.execute(players_table)
        self.cursor.execute(add_teams, team_data)
        self.cursor.execute(add_players, player_data)


    def close_spider(self, spider):
        self.cursor.close()
        self.connection.close()