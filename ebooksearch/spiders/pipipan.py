# -*- coding: utf-8 -*-
from urllib import parse

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class PipipanSpider(CrawlSpider):
    name = 'pipipan'
    allowed_domains = ['edu.pipipan.com']
    start_urls = ['http://edu.pipipan.com/']

    rules = (
        Rule(LinkExtractor(allow=r'class/\d+'), follow=True),
        Rule(LinkExtractor(allow=r'edu/.*'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        # 解析分类
        all_category_url = response.css(".sub-nav a::attr(href)").extract()
        all_category_url = [parse.urljoin(response.url, url) for url in all_category_url]
        for category_url in all_category_url:
            scrapy.Request(category_url, callback=self.parse_category_detail)


    def parse_category_detail(self, response):
        # 分类详情
        all_category_detail_url = response.css(".sub-nav a::attr(href)").extract()
        all_category_detail_url = [parse.urljoin(response.url, url) for url in all_category_detail_url]
        for category_detail_url in all_category_detail_url:
            scrapy.Request(category_detail_url, callback=self.parse_detail)

    def parse_detail(self, response):
        # 提取书籍信息
        pass
