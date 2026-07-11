# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Wcteam(scrapy.Item):
    name = scrapy.Field()
    group_name = scrapy.Field()
    pos = scrapy.Field()
    played = scrapy.Field()
    wins = scrapy.Field()
    draws = scrapy.Field()
    losses = scrapy.Field()
    goals_scored = scrapy.Field()
    goals_allowed = scrapy.Field()
    pts = scrapy.Field()
    pass

class Wcplayer(scrapy.Item):
    player = scrapy.Field()
    player_position = scrapy.Field()
    country = scrapy.Field()

class Goldenbootdata(scrapy.Item):
    player = scrapy.Field()
    team = scrapy.Field()
    position = scrapy.Field()
    goals = scrapy.Field()
    assists = scrapy.Field()
    minutes = scrapy.Field()

class Attacking(scrapy.Item):
    player = scrapy.Field()
    assists = scrapy.Field()
    on_target_attempts = scrapy.Field()
    total_goal_attempts = scrapy.Field()
    attempts_in_box = scrapy.Field()
    attempts_outside_box = scrapy.Field()
    total_header_attempts = scrapy.Field()
    expected_goals = scrapy.Field()
    expected_goal_efficiency = scrapy.Field()
    corners = scrapy.Field()

class Distribution(scrapy.Item):
    player = scrapy.Field()
    passes = scrapy.Field()
    passing_accuracy_percentage = scrapy.Field()
    crosses = scrapy.Field()
    crossing_accuracy_percentage = scrapy.Field()
    defensive_linebreaks_att = scrapy.Field()
    defensive_linebreak_acc = scrapy.Field()
    switches_att = scrapy.Field()
    switch_acc = scrapy.Field()

class Defending(scrapy.Item):
    player = scrapy.Field()
    own_goals = scrapy.Field()
    forced_turnovers = scrapy.Field()
    def_pressures = scrapy.Field()
    direct_def_pressures = scrapy.Field()

class Discipline(scrapy.Item):
    player = scrapy.Field()
    fouls_against = scrapy.Field()
    fouls_for = scrapy.Field()
    yellow_cards = scrapy.Field()
    red_cards = scrapy.Field()
    indirect_reds = scrapy.Field()

class Goalkeeping(scrapy.Item):
    player = scrapy.Field()
    saves = scrapy.Field()
    gk_actions_in_box = scrapy.Field()
    gk_actions_outside_box = scrapy.Field()

class Movement(scrapy.Item):
    player = scrapy.Field()
    total_offers_to_receive_ball = scrapy.Field()
    offers_behind_def_line = scrapy.Field()
    offers_between_def_units = scrapy.Field()
    offers_ahead_def_line = scrapy.Field()
    offers_inside_shape = scrapy.Field()
    receptions_in_behind = scrapy.Field()
    receptions_between_mid_and_def_lines = scrapy.Field()
    receptions_under_pressure = scrapy.Field()
    player_involvements = scrapy.Field()

class Physical(scrapy.Item):
    player = scrapy.Field()
    average_speed = scrapy.Field()
    high_speed_running = scrapy.Field()
    sprints = scrapy.Field()
    total_distance = scrapy.Field()



