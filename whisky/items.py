# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class Whisky(Item):
    # define the fields for your item here like:
    source = Field()
    source_url = Field()
    start_date = Field()
    end_date = Field()
    bottle_size = Field()
    distilleries = Field()
    distillery_status = Field()
    images = Field()
    country = Field()
    region = Field()
    age = Field()
    lot_num = Field()
    current_bid = Field()
    winning_bid = Field()
    sold_on = Field()
    reserve = Field()
    currency = Field()
    url = Field()
