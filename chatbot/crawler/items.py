# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

# Each crawled Ara article is saved as an AraArticle object. After crawling, each crawled article is dumped into a json file in the form
# of a dictionary with keys 'board', 'article_id', 'article_url', 'title', 'time' and 'content'.
class AraArticle(scrapy.Item):
    board = scrapy.Field()
    article_id = scrapy.Field()
    article_url = scrapy.Field()
    title = scrapy.Field()
    time = scrapy.Field()
    content = scrapy.Field()
