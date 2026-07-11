# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# useful for handling different item types with a single interface
import _mysql_connector
import mysql.connector as connector
from mysql.connector import errorcode
from WC.items import Wcteam, Wcplayer, Goldenbootdata, Attacking, Distribution, Defending, Discipline, Goalkeeping, Movement, Physical
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

        golden_boot_table = """CREATE TABLE IF NOT EXISTS golden_boot(
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

        distribution_table = """CREATE TABLE IF NOT EXISTS distribution(
                                        name VARCHAR(255),
                                        passes VARCHAR(255),
                                        passing_accuracy_percentage VARCHAR(255),
                                        crosses VARCHAR(255),
                                        crossing_accuracy_percentage VARCHAR(255), 
                                        defensive_linebreaks_att VARCHAR(255),
                                        defensive_linebreak_acc VARCHAR(255),
                                        switches_att VARCHAR(255),
                                        switch_acc VARCHAR(255) 
                                            )"""

        defending_table = """CREATE TABLE IF NOT EXISTS defending(
                                        name VARCHAR(255),
                                        own_goals VARCHAR(255),
                                        forced_turnovers VARCHAR(255),
                                        def_pressures VARCHAR(255),
                                        direct_def_pressures VARCHAR(255)
                                            )"""

        discipline_table = """CREATE TABLE IF NOT EXISTS discipline(
                                        name VARCHAR(255),
                                        fouls_against VARCHAR(255),
                                        fouls_for VARCHAR(255),
                                        yellow_cards VARCHAR(255),
                                        red_cards VARCHAR(255), 
                                        indirect_reds VARCHAR(255)
                                            )"""

        goalkeeping_table = """CREATE TABLE IF NOT EXISTS goalkeeping(
                                        name VARCHAR(255),
                                        saves VARCHAR(255),
                                        gk_actions_in_box VARCHAR(255),
                                        gk_actions_outside_box VARCHAR(255)
                                            )"""

        movement_table = """CREATE TABLE IF NOT EXISTS movement(
                                        name VARCHAR(255),
                                        total_offers_to_receive_ball VARCHAR(255),
                                        offers_behind_def_line VARCHAR(255),
                                        offers_between_def_units VARCHAR(255),
                                        offers_ahead_def_line VARCHAR(255), 
                                        offers_inside_shape VARCHAR(255),
                                        receptions_in_behind VARCHAR(255),
                                        receptions_between_mid_and_def_lines VARCHAR(255),
                                        receptions_under_pressure VARCHAR(255), 
                                        player_involvements VARCHAR(255)
                                            )"""

        physical_table = """CREATE TABLE IF NOT EXISTS physical(
                                        name VARCHAR(255),
                                        average_speed VARCHAR(255),
                                        high_speed_running VARCHAR(255),
                                        sprints VARCHAR(255),
                                        total_distance VARCHAR(255)
                                            )"""

        self.connection.cursor().execute(teams_table)
        self.connection.cursor().execute(players_table)
        self.connection.cursor().execute(golden_boot_table)
        self.connection.cursor().execute(attacking_table)
        self.connection.cursor().execute(distribution_table)
        self.connection.cursor().execute(defending_table)
        self.connection.cursor().execute(discipline_table)
        self.connection.cursor().execute(goalkeeping_table)
        self.connection.cursor().execute(movement_table)
        self.connection.cursor().execute(physical_table)



    #Handling items separately

    def process_item(self,item):

        self.table_creation()

        wcteam = Wcteam()
        wcplayer = Wcplayer()
        golden_boot = Goldenbootdata()
        attacking = Attacking()
        defending = Defending()
        distribution = Distribution()
        discipline = Discipline()
        goalkeeping = Goalkeeping()
        movement = Movement()
        physical = Physical()



        #Problem with getting items to their respective methods
        if type(item) == type(wcteam):
            return self.process_wcteam(item)
        elif type(item) == type(wcplayer):
            return self.process_wcplayer(item)
        elif type(item) == type(golden_boot):
            return self.process_golden_boot(item)
        elif type(item) == type(attacking):
            return self.process_attacking(item)
        elif type(item) == type(distribution):
            return self.process_distribution(item)
        elif type(item) == type(defending):
            return self.process_defending(item)
        elif type(item) == type(discipline):
            return self.process_discipline(item)
        elif type(item) == type(goalkeeping):
            return self.process_goalkeeping(item)
        elif type(item) == type(movement):
            return self.process_movement(item)
        elif type(item) == type(physical):
            return self.process_physical(item)

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

    #Handling wcplayer items
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

    #Handling golden_boot items
    def process_golden_boot(self, item):

        add_golden_boot = ("INSERT INTO golden_boot"
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

    #Handling attacking items
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

    #Handling distribution items
    def process_distribution(self, item):

        add_distribution = ("INSERT INTO distribution"
                       "(name, passes, passing_accuracy_percentage, crosses, crossing_accuracy_percentage, defensive_linebreaks_att,"
                         "defensive_linebreak_acc, switches_att, switch_acc)"
                       "VALUES (%(name)s, %(passes)s, %(passing_accuracy_percentage)s, %(crosses)s, %(crossing_accuracy_percentage)s,"
                           "%(defensive_linebreaks_att)s, %(defensive_linebreak_acc)s, %(switches_att)s, %(switch_acc)s)")

        distribution_dict = dict(item)

        distribution_data = {
            "name": distribution_dict["player"],
            "passes": distribution_dict["passes"],
            "passing_accuracy_percentage": distribution_dict["passing_accuracy_percentage"],
            "crosses": distribution_dict["crosses"],
            "crossing_accuracy_percentage": distribution_dict["crossing_accuracy_percentage"],
            "defensive_linebreaks_att": distribution_dict["defensive_linebreaks_att"],
            "defensive_linebreak_acc": distribution_dict["defensive_linebreak_acc"],
            "switches_att": distribution_dict["switches_att"],
            "switch_acc": distribution_dict["switch_acc"]
        }

        try:
            self.connection.cursor().execute(add_distribution, distribution_data)

        except _mysql_connector.MySQLError as e:
            print(f"Error importing data for golden boot: {e}")
            raise CloseSpider

        self.connection.commit()

    #Handling defending items
    def process_defending(self, item):

        add_defending = ("INSERT INTO defending"
                       "(name, own_goals, forced_turnovers, def_pressures, direct_def_pressures)"
                       "VALUES (%(name)s, %(own_goals)s, %(forced_turnovers)s, %(def_pressures)s, %(direct_def_pressures)s)")

        defending_dict = dict(item)

        defending_data = {
            "name": defending_dict["player"],
            "own_goals": defending_dict["own_goals"],
            "forced_turnovers": defending_dict["forced_turnovers"],
            "def_pressures": defending_dict["def_pressures"],
            "direct_def_pressures": defending_dict["direct_def_pressures"]
        }

        try:
            self.connection.cursor().execute(add_defending, defending_data)

        except _mysql_connector.MySQLError as e:
            print(f"Error importing data for golden boot: {e}")
            raise CloseSpider

        self.connection.commit()

    #Handling discipline items
    def process_discipline(self, item):

        add_discipline = ("INSERT INTO discipline"
                       "(name, fouls_against, fouls_for, yellow_cards, red_cards, indirect_reds)"
                       "VALUES (%(name)s, %(fouls_against)s, %(fouls_for)s, %(yellow_cards)s, %(red_cards)s,"
                           "%(indirect_reds)s)")

        discipline_dict = dict(item)

        discipline_data = {
            "name": discipline_dict["player"],
            "fouls_against": discipline_dict["fouls_against"],
            "fouls_for": discipline_dict["fouls_for"],
            "yellow_cards": discipline_dict["yellow_cards"],
            "red_cards": discipline_dict["red_cards"],
            "indirect_reds": discipline_dict["indirect_reds"],

        }

        try:
            self.connection.cursor().execute(add_discipline, discipline_data)

        except _mysql_connector.MySQLError as e:
            print(f"Error importing data for golden boot: {e}")
            raise CloseSpider

        self.connection.commit()

        def process_distribution(self, item):

            add_attacking = ("INSERT INTO distribution"
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

    #Handling goalkeeping items
    def process_goalkeeping(self, item):

        add_goalkeeping = ("INSERT INTO goalkeeping"
                       "(name, saves, gk_actions_in_box, gk_actions_outside_box)"
                       "VALUES (%(name)s, %(saves)s, %(gk_actions_in_box)s, %(gk_actions_outside_box)s)")

        goalkeeping_dict = dict(item)

        goalkeeping_data = {
            "name": goalkeeping_dict["player"],
            "saves": goalkeeping_dict["saves"],
            "gk_actions_in_box": goalkeeping_dict["gk_actions_in_box"],
            "gk_actions_outside_box": goalkeeping_dict["gk_actions_outside_box"]
        }

        try:
            self.connection.cursor().execute(add_goalkeeping, goalkeeping_data)

        except _mysql_connector.MySQLError as e:
            print(f"Error importing data for golden boot: {e}")
            raise CloseSpider

        self.connection.commit()

    #Handling movement items
    def process_movement(self, item):

        add_movement = ("INSERT INTO movement"
                       "(name, total_offers_to_receive_ball, offers_behind_def_line, offers_between_def_units, offers_ahead_def_line, offers_inside_shape,"
                         "receptions_in_behind, receptions_between_mid_and_def_lines, receptions_under_pressure, player_involvements)"
                       "VALUES (%(name)s, %(total_offers_to_receive_ball)s, %(offers_behind_def_line)s, %(offers_between_def_units)s, %(offers_ahead_def_line)s,"
                           "%(offers_inside_shape)s, %(receptions_in_behind)s, %(receptions_between_mid_and_def_lines)s, %(receptions_under_pressure)s,"
                         "%(player_involvements)s)")

        movement_dict = dict(item)

        movement_data = {
            "name": movement_dict["player"],
            "assists": movement_dict["assists"],
            "on_target_attempts": movement_dict["on_target_attempts"],
            "total_goal_attempts": movement_dict["total_goal_attempts"],
            "attempts_in_box": movement_dict["attempts_in_box"],
            "attempts_outside_box": movement_dict["attempts_outside_box"],
            "total_header_attempts": movement_dict["total_header_attempts"],
            "expected_goals": movement_dict["expected_goals"],
            "expected_goal_efficiency": movement_dict["expected_goal_efficiency"],
            "corners": movement_dict["corners"]
        }

        try:
            self.connection.cursor().execute(add_movement, movement_data)

        except _mysql_connector.MySQLError as e:
            print(f"Error importing data for golden boot: {e}")
            raise CloseSpider

        self.connection.commit()

    #Handling physical items
    def process_physical(self, item):

        add_physical = ("INSERT INTO physical"
                       "(name, average_speed, high_speed_running, sprints, total_distance)"
                       "VALUES (%(name)s, %(average_speed)s, %(high_speed_running)s, %(sprints)s, %(total_distance)s)")

        physical_dict = dict(item)

        physical_data = {
            "name": physical_dict["player"],
            "average_speed": physical_dict["average_speed"],
            "high_speed_running": physical_dict["high_speed_running"],
            "sprints": physical_dict["sprints"],
            "total_distance": physical_dict["total_distance"]
        }

        try:
            self.connection.cursor().execute(add_physical, physical_data)

        except _mysql_connector.MySQLError as e:
            print(f"Error importing data for golden boot: {e}")
            raise CloseSpider

        self.connection.commit()


    def close_spider(self, spider):
        self.connection.cursor().close()
        self.connection.close()