# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import MySQLdb
from twisted.enterprise import adbapi
import MySQLdb.cursors


class EbooksearchPipeline(object):
    def process_item(self, item, spider):
        return item


# 异步插入数据库
class MysqlTwistedPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparams = dict(
            host=settings["MYSQL_HOST"],
            db=settings["MYSQL_DBNAME"],
            user=settings["MYSQL_USER"],
            passwd=settings["MYSQL_PASSWORK"],
            charset="utf8",
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True
        )
        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparams)
        return cls(dbpool)

    def process_item(self, item, spider):
        # 使用twisted将MySQL插入变成异步执行
        query = self.dbpool.runInteraction(self.do_insert, item)  # do_insert  自定义函数
        query.addErrback(self.handle_error, item, spider)  # 异常处理

    def do_insert(self, cursor, item):
        # 进行具体的数据插入操作 根据不同的item 构建不同的sql语句并插入到mysql中
        insert_sql, params = item.get_insert_sql()
        print(insert_sql)
        print(params)
        cursor.execute(insert_sql, params)

    def handle_error(self, failure, item, spider):
        # # 错误处理 处理异步插入的异常
        print(failure)
