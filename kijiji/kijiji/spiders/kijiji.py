# -*- coding: utf-8 -*-
import scrapy

from ..items import KijijiItem
from scrapy.crawler import CrawlerProcess


class KijijiSpider(scrapy.Spider):
    name = 'kijiji'
    allowed_domains = ['kijiji.ca']
    start_urls = ['https://www.kijiji.ca/b-chambres-a-louer-colocataire/ville-de-montreal/c36l1700281r10.0?ll=45.510311,-73.579954&address=H2W1S4&ad=offering&minNumberOfImages=4&price=300__450']

    def parse(self, response):
        # count = 0
        # for x in response.css('.clearfix'):
        #     count = count + 1
        #     self.log("NUMBER of COUNT {cnt}".format(cnt=count))
        #     self.log( self.ad_id(x))
        #     #yield x

#        for ad in response.css('div ::attr(data-ad-id)'):

        for ad in response.css('div.title'):
            item = KijijiItem()
            item['title'] = ad.css('a::text').extract_first()
            item['href'] = ad.css('a::attr(href)').extract_first()
            yield response.follow(item['href'], callback=self.parse_ad, meta={'item': item})

        # follow pagination links
        #next_page = self._get_next_page(response)
        #yield response.follow(next_page, self.parse) if next_page is not None

        #self.log(sum(1 for _ in response.css('.clearfix')))

    @staticmethod
    def _get_next_page(s):
        return s.css('.page-link~ .prevnext-link ::attr(data-href)').extract_first()

    @staticmethod
    def _get_ad_id(s):
        return s.css('div ::attr(data-ad-id)').extract()

    @staticmethod
    def _get_price(s):
        return s.css("span[class*='currentPrice'] ::text").extract_first()

    @staticmethod
    def _get_latitude(s):
        return s.css("meta[property='og:latitude'] ::attr(content)").extract_first()

    @staticmethod
    def _get_longitude(s):
        return s.css("meta[property='og:longitude'] ::attr(content)").extract_first()

    @staticmethod
    def _get_date_posted(s):
        return s.css("div[class*='datePosted'] ::attr(datetime)").extract_first()

    def parse_ad(self, response):
        item = response.meta['item']
        item['description'] = response.css('#vip-body div div div  div p').extract_first()
        item['price'] = self._get_price(response)
        item['latitude'] = self._get_latitude(response)
        item['longitude'] = self._get_longitude(response)
        item['date_posted'] = self._get_date_posted(response)
        yield item


