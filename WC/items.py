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
    # goals = scrapy.Field()
    # assists = scrapy.Field()
