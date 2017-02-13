#!/usr/bin/env python
# -*- coding:utf-8 -*-
#from scrapy.spiders import CrawlSpider, Rule
from scrapy.spiders import Rule
from scrapy_redis.spiders import RedisCrawlSpider
from scrapy.linkextractors import LinkExtractor
# Redis去重
from example.items import youyuanItem
from scrapy.dupefilters import RFPDupeFilter


class youyuanSpider(RedisCrawlSpider):
    name = 'youyuan'
    #allowed_domains = ['www.youyuan.com']
    #start_urls = ['http://www.youyuan.com/find/beijing/mm18-25/advance-0-0-0-0-0-0-0/p1/']
    redis_key = "youyuan:start_urls"

    #一级跳板：find页面匹配规则
    list_page_lx = LinkExtractor(allow=(r'http://www.youyuan.com/find/.+'))

    #二级跳板：匹配北京、18-25女性搜索页面匹配规则在，
    page_lx = LinkExtractor(allow=(r'http://www.youyuan.com/find/beijing/mm18-25/advance-0-0-0-0-0-0-0/p\d+/'))

    #个人主页：每个人的个人主页匹配规则
    profile_page_lx = LinkExtractor(allow = (r'http://www.youyuan.com/\d+-profile/'))

    rules = (
                Rule(list_page_lx, follow=True),
                Rule(page_lx, follow=True),
                Rule(profile_page_lx, callback = 'parse_profile_page', follow=False),
    )

    def __init__(self, *args, **kwargs):
        domain = kwargs.pop('domain', '')
        self.allowed_domains = filter(None, domain.split(','))
        super(youyuanSpider, self).__init__(*args, **kwargs)


    def parse_profile_page(self, response):
        item = youyuanItem()
        item['header_url'] = self.get_header_url(response)
        item['pic_url'] = self.get_pic_url(response)
        item['username'] = self.get_username(response)
        item['requer'] = self.get_requer(response)
        item['age'] = self.get_age(response)
        item['source'] = "youyuan"
        item['source_url'] = response.url

        yield item

    # 头像地址
    def get_header_url(self, response):
        header = response.xpath("//dl[@class=\'personal_cen\']/dt/img/@src").extract()
        if len(header) > 0:
            header_url = header[0]
        else:
            header_url = "NULL"
        #print header_url
        return header_url.strip()

    # 相册里每个照片的url地址
    def get_pic_url(self, response):
        pic_urls = []
        urls = response.xpath("//div[@class=\'ph_show\']//li[@class=\'smallPhoto\']/@data_url_full").extract()
        for pic_url in urls:
            pic_urls.append(pic_url)
        if len(pic_urls) < 1:
            return "NULL"
        return "|".join(pic_urls)

    # 获取用户名
    def get_username(self, response):
        usernames = response.xpath("//dl[@class=\'personal_cen\']/dd//strong/text()").extract()
        if len(usernames) > 0:
            username = usernames[0]
        else:
            username = "NULL"
        #print username
        return username.strip()

    # 获取内心独白
    def get_requer(self, response):
        requers = response.xpath("//ul[@class=\'requre\']/li/p/text()").extract()
        if len(requers) > 0:
            requer = requers[0]
        else:
            requer = "NULL"
        #print requer
        return requer.strip()

    # 获取年龄
    def get_age(self, response):
        ages = response.xpath("//dl[@class=\'personal_cen\']/dd//p/text()").extract()
        if len(ages) > 0:
            age = ages[0]
            age = age.split(" ")[1][:-1]
        else:
            age = "NULL"
        #print age
        return age







