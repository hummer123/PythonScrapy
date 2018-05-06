# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.http import Request
from urllib import parse


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):
        """
        #解析当前响应response，并解析response中的url进行article解析
        :param response:
        :return:
        """
        article_list = response.xpath('//div[@class = "post-thumb"]')
        for article in article_list:
            article_url = article.xpath('a/@href').extract()[0]
            # article_img_url = article.xpath('a/img/@src').extract()[0]
            yield Request(url=parse.urljoin(response.url, article_url), callback=self.parse_detale)
        """
        #解析article列表中下一页url
        """
        article_next_url = response.xpath('//a[@class = "next page-numbers"]/@href').extract()[0]
        print(">>> article = ", article_next_url)
        if article_next_url:
            yield Request(url=parse.urljoin(response.url, article_next_url), callback=self.parse)

    def parse_detale(self, response):
        rsp_xpath = response.xpath('//div[contains(@class, "type-post")]')
        title = rsp_xpath.xpath('//*[@class = "entry-header"]/h1/text()').extract()[0]
        praise_nums = int(rsp_xpath.xpath('//span[contains(@class, "vote-post-up")]//h10/text()').extract()[0])
        collect_nums = rsp_xpath.xpath('//span[contains(@class, "bookmark-btn")]/text()').extract()[0]
        match_collect = re.match(r'.*?(\d+).*', collect_nums)
        if match_collect:
            collect_nums = int(match_collect.group(1))
        else:
            collect_nums = 0

        comment_nums = rsp_xpath.xpath('//a[@href = "#article-comment"]/span/text()').extract()[0]
        match_comment = re.match(r'.*(\d+).*', comment_nums)
        if match_comment:
            comment_nums = int(match_comment.group(1))
        else:
            comment_nums = 0

        content = rsp_xpath.xpath('//div[@class = "entry"]').extract()[0]
        pass
