# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MacroScrapyItem(scrapy.Item):
    # define the fields for your item here like:
    file_urls = scrapy.Field()
    original_file_name = scrapy.Field()
    files = scrapy.Field

class QuoteItem(scrapy.Item):
    # define the fields for your item here like:
    text = scrapy.Field()
    author = scrapy.Field()
    tags = scrapy.Field()
