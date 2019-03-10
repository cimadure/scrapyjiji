# -*- coding: utf-8 -*-
import scrapy

from scrapy.crawler import CrawlerProcess


class KijijiSpider(scrapy.Spider):
    name = 'kijiji'
    allowed_domains = ['kijiji.ca']
    start_urls = ['https://www.kijiji.ca/b-chambres-a-louer-colocataire/ville-de-montreal/c36l1700281r10.0?ll=45.510311,-73.579954&address=H2W1S4&ad=offering&minNumberOfImages=4&price=300__450']

    def parse(self, response):
        count = 0
        for x in response.css('.clearfix'):
            count = count + 1
            self.log("NUMBER of COUNT {cnt}".format(cnt=count))

        # follow pagination links
        for href in response.css('.page-link~ .prevnext-link attr(data-href)'):
            self.log(href)
            #yield response.follow(href, self.parse)

            #yield x
        self.log(sum(1 for _ in response.css('.clearfix')))

    @staticmethod
    def _get_next_page(s):
        return s.css('.page-link~ .prevnext-link ::attr(data-href)').extract_first()

    @staticmethod
    def ad_id(s):
        return s.css('div ::attr(data-ad-id)').extract()
