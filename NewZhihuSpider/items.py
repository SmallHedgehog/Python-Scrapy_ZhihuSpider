# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NewzhihuspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    # id
    name = scrapy.Field()
    # Job
    Job = scrapy.Field()
    # 居住地
    location = scrapy.Field()
    # 所在行业
    work = scrapy.Field()
    # 教育经历
    education = scrapy.Field()