# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import csv
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class NewzhihuspiderPipeline(object):
    def __init__(self):
        self.csvfile= file('ProfileCSV.csv', 'wb')
        self.writer = csv.writer(self.csvfile)
        self.writer.writerow(['Name', 'Description'])

    def process_item(self, item, spider):
        self.writer.writerow([item['name'], item['Job']])
        return item
