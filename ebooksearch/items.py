# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join


class EbooksearchItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class IshareItemLoader(ItemLoader):
    # 自定义ItemLoader
    default_output_processor = TakeFirst()


#爱问分享资料
class IshareItem(scrapy.Item):

    url_obj_id = scrapy.Field()
    title = scrapy.Field()
    upload_people = scrapy.Field()
    score = scrapy.Field()
    load_num = scrapy.Field()
    upload_time = scrapy.Field()
    crawl_time = scrapy.Field()
    url = scrapy.Field()
    source_website = scrapy.Field()
    type = scrapy.Field()
    comment_num = scrapy.Field()
    read_num = scrapy.Field()
    collect_num = scrapy.Field()


