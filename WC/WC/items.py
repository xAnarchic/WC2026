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
    player =  scrapy.Field()
    team = scrapy.Field()
    position = scrapy.Field()
    goals = scrapy.Field()
    assists = scrapy.Field()
    minutes = scrapy.Field()

class Attacking(scrapy.Item):
    player =  scrapy.Field()
    assists = scrapy.Field()
    on_target_attempts = scrapy.Field()
    total_goal_attempts = scrapy.Field()
    attempts_in_box = scrapy.Field()
    attempts_outside_box = scrapy.Field()
    total_header_attempts = scrapy.Field()
    expected_goals = scrapy.Field()
    expected_goal_efficiency = scrapy.Field()
    corners = scrapy.Field()
