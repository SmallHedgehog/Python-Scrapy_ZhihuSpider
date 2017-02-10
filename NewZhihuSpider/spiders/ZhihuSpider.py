# coding: utf-8

from scrapy import log
from scrapy.spiders import CrawlSpider
from scrapy.selector import Selector
from scrapy.http import Request, FormRequest

from NewZhihuSpider.items import NewzhihuspiderItem

from bs4 import BeautifulSoup

class ZhihuSpider(CrawlSpider):
    name = "zhihu"
    allowed_domains = ["www.zhihu.com"]
    start_url = "https://www.zhihu.com/people/caifei-yang"

    def __init__(self, *args, **kwargs):
        super(ZhihuSpider, self).__init__(*args, **kwargs)
        self.xsrf = ''

    def start_requests(self):
        """ 登录页面， 获取xrsf """
        return [Request(
            url="https://www.zhihu.com/#signin",
            meta={"cookiejar": 1},
            callback=self.post_login
        )]

    def post_login(self, response):
        """ 解析登录页面， 发送登录表单 """
        self.xsrf = Selector(response).xpath('//input[@name="_xsrf"]/@value').extract()[0]

        print self.xsrf

        #return [FormRequest.from_response(
        #    url="https://www.zhihu.com/login/email",
        #    method="POST",
        #    meta={'cookiejar': response.meta['cookiejar']},
        #    fromdata={
        #        '_xsrf': self.xsrf,
        #        'email': 'yangcaifei0713@163.com',
        #        'password': 'YY1995713',
        #    },
        #    callback=self.after_login
        #)]

        return [FormRequest("https://www.zhihu.com/login/email",
                            meta={'cookiejar': response.meta['cookiejar']},
                            method='post',
                            formdata={
                                '_xsrf': self.xsrf,
                                'email': 'yangcaifei0713@163.com',
                                'password': 'YY1995713'
                            },
                            callback=self.after_login,
                )]

    def after_login(self, response):
        """ 登录完成后从第一个用户开始爬数据 """
        return [Request(
            self.start_url,
            meta={'cookiejar': response.meta['cookiejar']},
            callback=self.parse_people,
            errback=self.parse_err
        )]

    def parse_people(self, response):
        """ 解析用户主页 """
        selector = Selector(response)
        soup = BeautifulSoup(response.body)
        # print soup.prettify()
        # id
        name = selector.xpath('//div[@class="ProfileHeader-contentHead"]/h1[@class="ProfileHeader-title"]/span[@class="ProfileHeader-name"]/text()').extract_first()
        # job
        job = selector.xpath('//div[@class="ProfileHeader-contentHead"]/h1[@class="ProfileHeader-title"]/span[@class="RichText ProfileHeader-headline"]/text()').extract_first()
        print name, job

        follow_urls = soup.find_all("a", class_="Button NumberBoard-item Button--plain")
        # print len(follow_urls)
        for urlWithTag in follow_urls:
            # print urlWithTag.attrs['href']
            url = urlWithTag.attrs['href']
            complete_url = 'https://{}{}'.format(self.allowed_domains[0], url)
            # print complete_url
            yield Request(complete_url,
                          meta={'cookiejar': response.meta['cookiejar']},
                          callback=self.parse_follow,
                          errback=self.parse_err
                          )

        item = NewzhihuspiderItem(
            name = name,
            Job = job
        )
        yield item

    def parse_follow(self, response):
        """ 解析follow数据 """
        selector = Selector(response)
        soup = BeautifulSoup(response.body)
        # print soup.prettify()

        people_links = selector.xpath('//a[@class="UserLink-link"]/@href').extract()
        index = 0
        while index < len(people_links):
            # print people_links[index]
            url = people_links[index]
            index = index + 2
            complete_url = 'https://{}{}'.format(self.allowed_domains[0], url)
            print complete_url
            yield Request(complete_url,
                          meta={'cookiejar': response.meta['cookiejar']},
                          callback=self.parse_people,
                          errback=self.parse_err
                          )

    def parse_err(self, response):
        log.ERROR('crawl {} failed'.format(response.url))