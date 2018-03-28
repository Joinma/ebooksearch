# -*- coding: utf-8 -*-
import scrapy
from urllib import parse
import re

class IshareSpider(scrapy.Spider):
    name = 'ishare'
    allowed_domains = ['ishare.iask.sina.com.cn']
    start_urls = ['http://ishare.iask.sina.com.cn']

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)Chrome/63.0.3239.84 Safari/537.36'
    }

    def parse(self, response):
        all_urls = response.css("a::attr(href)").extract();
        all_urls = [parse.urljoin(response.url,url) for url in all_urls]
        all_urls = filter(lambda x: True if x.startswith("http") else False, all_urls)
        for url in all_urls:
            match_obj = re.match(r'(.*iask.sina.com.cn/c/(\d+).html$)', url)  # 'http://ishare.iask.sina.com.cn/c/9001.html'
            if match_obj:
                # 如果匹配到url，进行详情页提取
                yield scrapy.Request(url=url, headers=self.headers, callback=self.category_parse)

    def category_parse(self, response):
        # 没有这个轮播图的才是真正要爬取的页面
        if "education-banner" not in response.text:
            pass