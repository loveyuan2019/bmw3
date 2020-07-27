# -*- coding: utf-8 -*-
import scrapy
from bmw.items import BmwItem
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor

class BmwSpiderSpider(CrawlSpider):
    name = 'bmw_spider'
    allowed_domains = ['car.autohome.com.cn']
    start_urls = ['https://car.autohome.com.cn/pic/series/65.html']
    rules={
        Rule(LinkExtractor(allow=r"https://car.autohome.com.cn/pic/series/65.+"),callback="parse_page",follow=True),
    }

    def parse_page(self, response):
        category=response.xpath(r"//div[@class='uibox']/div/text()").get() #拿到分类名称
        srcs=response.xpath(r"//div[contains(@class,'uibox-con')]/ul/li//img/@src").getall()    #注意里面的用法，很重要
        srcs=list(map(lambda x: x.replace("240x180_0_q95_c42_",""),srcs))       #去掉240x180_0_q95_c42_，得到高清照片网址
        # print(srcs)
        srcs=list(map(lambda x: response.urljoin(x),srcs))      #链接前面加上https:并成为一个列表 
        yield BmwItem(category=category,image_urls=srcs)
        
        # pass
    def test_parse(self,response):
        uiboxes=response.xpath(r"//div[@class='uibox']")[1:]
        for uibox in uiboxes:
            category=uibox.xpath(r".//div[@class='uibox-title']/a/text()").get()
            # print(category)
            urls=uibox.xpath(r".//ul/li/a/img/@src").getall()
            # print(urls)
            urls=list(map(lambda url: response.urljoin(url),urls))
            # print(urls)
            item=BmwItem(category=category,image_urls=urls)
            yield item



