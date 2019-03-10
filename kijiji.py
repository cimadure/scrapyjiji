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
            self.log(count)
            yield x

    @staticmethod
    def ad_id(s):
        return s.css('div ::attr(data-ad-id)').extract_first()


if __name__ == "__main__":
    # Entry point
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })

    process.crawl(KijijiSpider)
    process.start()
