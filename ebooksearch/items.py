# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
import datetime
import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst, Join
from scrapy.loader import ItemLoader
from w3lib.html import remove_tags
import re
import time
from decimal import *

from ebooksearch.utils.common import get_md5


class EbooksearchItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class IshareItemLoader(ItemLoader):
    # 自定义新浪爱问分享的ItemLoader
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
            insert into `ishare` (url_obj_id, title, upload_people, score, load_num, read_num, comment_num, collect_num, upload_time, crawl_time, url, source_website, type) 
              VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE title=VALUES(title), load_num=VALUES(load_num),
              score=VALUES(score),read_num=VALUES(read_num),comment_num=VALUES(comment_num),collect_num=VALUES(collect_num), crawl_time=VALUES(crawl_time),
              type=VALUES(type)
        """

        score = 0.0
        load_num = int(self["load_num"])
        comment_num = int(self["comment_num"])
        read_num = int(self["read_num"])
        collect_num = int(self["collect_num"])
        type = self["type"].split(".")[1]
        type_match = re.match(".+\.(.+)", self["type"])
        if type_match:
            type = type_match.group(1)
        else:
            type = "None"
        upload_time_str = self["upload_time"]
        upload_time = time.strptime(upload_time_str, "%Y-%m-%d")
        upload_time_int = round(time.mktime(upload_time) * 1000)

        params = (self["url_obj_id"], self["title"], self["upload_people"], score,
                  load_num, read_num, comment_num, collect_num,
                  upload_time_int, self["crawl_time"], self["url"], self["source_website"],
                  type)

        return insert_sql, params


# 城通网盘
class PipipanItemLoader(ItemLoader):
    # 自定义城通网盘的ItemLoader
    default_output_processor = TakeFirst()


def format_upload_time(value):
    # 处理上传时间
    match_obj2 = re.match(r'(\d+)小时.*', value)
    match_obj1 = re.match(r'(^昨天((\d+):(\d+)))', value)
    match_obj3 = re.match(r'(^前天((\d+):(\d+)))', value)
    match_obj4 = re.match(r'(\d+)天前.*', value)
    match_obj5 = re.match(r'\d+-\d+-\d+', value)
    
    if match_obj1:
        upload_time = match_obj1.group(1) * 3600000
        return upload_time
    elif match_obj2:
        hour = match_obj2.group(2)
        minute = match_obj2.group(3)
        today = datetime.date.today()
        # 0点时间戮
        today_timestamp = int(time.mktime(today.timetuple()))
        yestoday_timestamp = today_timestamp - 3600000 * 24
        upload_time = yestoday_timestamp + hour * 3600000 + minute * 60000
        return upload_time
    elif match_obj4:
        upload_time = match_obj4.group(1) * 3600000 * 24
        return upload_time
    elif match_obj5:
        upload_time = time.strptime(value, "%Y-%m-%d")
        return round(time.mktime(upload_time) * 1000)
    else:
        return round(time.time() * 1000)


def get_size(value):
    size = value.replace("\r", "").replace("\n", "").replace("\t", "")
    return size


def get_type(value):
    match_obj = re.match(".*\.(.*)", value)
    if match_obj:
        type = match_obj.group(1)
    else:
        type = "unknown"
    return type


# 城通网盘
class PipipanItem(scrapy.Item):
    url_obj_id = scrapy.Field()
    title = scrapy.Field()
    read_num = scrapy.Field()
    upload_time = scrapy.Field(
        input_processor = MapCompose(format_upload_time)
    )
    crawl_time = scrapy.Field()
    url = scrapy.Field()
    source_website = scrapy.Field()
    type = scrapy.Field(
        input_processor=MapCompose(get_type)
    )
    size = scrapy.Field(
        input_processor=MapCompose(get_size)
    )
    tag = scrapy.Field(
        input_processor=Join(",")
    )
    description = scrapy.Field(
        input_processor=MapCompose(remove_tags)
    )

    def get_insert_sql(self):

        description = self["description"]
        if description:
            print("description: " + description)
            insert_sql = """
                insert into `pipipan` (url_obj_id, title, read_num, upload_time, crawl_time, 
                url, source_website, type, size, tag, description) 
                  VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) 
                  ON DUPLICATE KEY UPDATE title=VALUES(title),read_num=VALUES(read_num),
                  crawl_time=VALUES(crawl_time), tag=values(tag)
            """

            params = (self["url_obj_id"], self["title"], self["read_num"], self["upload_time"], self["crawl_time"],
                      self["url"], self["source_website"], self["type"], self["size"], self["tag"], self["description"])
        else:
            insert_sql = """
                            insert into `pipipan` (url_obj_id, title, read_num, upload_time, crawl_time, 
                            url, source_website, type, size, tag) 
                              VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) 
                              ON DUPLICATE KEY UPDATE title=VALUES(title),read_num=VALUES(read_num),
                              crawl_time=VALUES(crawl_time), tag=values(tag)
                        """

            params = (self["url_obj_id"], self["title"], self["read_num"], self["upload_time"], self["crawl_time"],
                      self["url"], self["source_website"], self["type"], self["size"], self["tag"])
            
        return insert_sql, params


# 我的小书屋
class MebookItemLoader(ItemLoader):
    # 自定义ItemLoader
    default_output_processor = TakeFirst()


class MebookItem(scrapy.Item):
    url_obj_id = scrapy.Field()
    title = scrapy.Field()
    upload_time = scrapy.Field(
        input_processor = Join(","),
        # output_processor = MapCompose(get_upload_time)
    )
    crawl_time = scrapy.Field()
    url = scrapy.Field()
    source_website = scrapy.Field()
    type = scrapy.Field()
    description = scrapy.Field()
    tag = scrapy.Field()

    def get_insert_sql(self):

        insert_sql = """
            insert into `mebook` (url_obj_id, title, upload_time, crawl_time, url, 
            source_website, type, description, tag) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) 
              ON DUPLICATE KEY UPDATE title=VALUES(title),crawl_time=VALUES(crawl_time), 
              tag=VALUES(tag), description=VALUES(description)
        """

        match_obj = re.match(".*?((\d+)年(\d+)月(\d+)日).*", self["upload_time"])
        if match_obj:
            date = match_obj.group(1).replace("年", "-").replace("月", "-").replace("日", "")
            upload_time = time.strptime(date, "%Y-%m-%d")
            upload_time = round(time.mktime(upload_time) * 1000)
        else:
            upload_time = round(time.time() * 1000)

        match_type = re.match(r'.*(》|）|\))([a-zA-Z].*)',self["type"])
        if match_type:
            type = match_type.group(2)
        else:
            type = "unknown"

        params = (self["url_obj_id"], self["title"], upload_time, self["crawl_time"],
                  self["url"], self["source_website"], type, self["description"], self["tag"])

        return insert_sql, params

