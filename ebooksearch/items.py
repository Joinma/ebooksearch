# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst, Join
from scrapy.loader import ItemLoader


class EbooksearchItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class IshareItemLoader(ItemLoader):
    # 自定义itemLoader
    default_output_processor = TakeFirst()


# 爱问分享资料
class IshareItem(scrapy.Item):
    # 自定义一个item给pipelines
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
    size = scrapy.Field()
    comment_num = scrapy.Field()
    read_num = scrapy.Field()
    collect_num = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
            insert into `ishare` (url_obj_id, title, upload_people, score, load_num, read_num, comment_num, collect_num, upload_time, crawl_time, url, source_website, type, size) 
              VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE title=VALUES(title), load_num=VALUES(load_num),
              score=VALUES(score),read_num=VALUES(read_num),comment_num=VALUES(comment_num),collect_num=VALUES(collect_num), crawl_time=VALUES(crawl_time),
              type=VALUES(type)
        """

        params = (self["url_obj_id"], self["title"], self["upload_people"], self["score"],
                  self["load_num"], self["read_num"], self["comment_num"], self["collect_num"],
                  self["upload_time"], self["crawl_time"], self["url"], self["source_website"],
                  self["type"], self["size"])

        return insert_sql, params