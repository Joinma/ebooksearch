# -*- coding: utf-8 -*-
import scrapy
from urllib import parse
import re

from scrapy.loader import ItemLoader

from ebooksearch.items import IshareItem


class IshareSpider(scrapy.Spider):
    name = 'ishare'
    allowed_domains = ['ishare.iask.sina.com.cn']
    start_urls = ['http://ishare.iask.sina.com.cn']

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)Chrome/63.0.3239.84 Safari/537.36'
    }

    def parse(self, response):
        all_urls = response.css("a::attr(href)").extract(); # 拿到所有的url
        all_urls = [parse.urljoin(response.url, url) for url in all_urls]
        all_urls = filter(lambda x: True if x.startswith("http") else False, all_urls) # 过滤不是http开头的url
        for url in all_urls:
            match_obj = re.match(r'(.*iask.sina.com.cn/c/(\d+).html$)', url) # 匹配资料url
            if match_obj:
                # 如果匹配到url，进行详情页提取
                yield scrapy.Request(url=url, headers=self.headers, callback=self.category_parse)
            else:
                pass
                #匹配不到，继续跟踪
                # yield scrapy.Request(url=url, headers=self.headers, callback=self.parse)

    def category_parse(self, response):
        # 没有这个轮播图的才是真正要爬取的页面
        if "education-banner" not in response.text:
            all_urls = response.css("::attr(href)").extract(); # 拿到类别页中所有的url
            all_urls = [parse.urljoin(response.url, url) for url in all_urls]  # 为url添加域名
            # http: // ishare.iask.sina.com.cn / f / j63XA46zwy.html
            for url in all_urls:
                match_obj = re.match(r'(.*/f/(\d+).html$)', url)  # 详情页url
                if match_obj:
                    # 如果匹配到的url不为空，提取详情
                    request_url = match_obj.group(1)
                    request_id = match_obj.group(2)
                    yield scrapy.Request(url=url, headers=self.headers, callback=self.detail_parse)


    def detail_parse(self, response):
        # 资料详情提取
        pass