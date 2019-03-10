#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
# Copyright (C) 2016 Sebastien Bourdelin <sebastien.bourdelin@gmail.com>
#

import scrapy
import re
import geocoder
import folium
import datetime

from scrapy.crawler import CrawlerProcess
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher

# Settings
MAX_POST_DAYS = 15


MAP_ZOOM         = 13
MIN_PRICE        = 0
MAX_PRICE        = 700
GREEN_PRICE      = 400
ORANGE_PRICE       = 550
MAX_PAGE         = 10

if False:
    MAP_LATLNG       = [46.810811, -71.215439] # your city latitude and longitude
    START_URL        = "http://www.kijiji.ca/b-appartement-condo/ville-de-quebec/c37l1700124?ad=offering&siteLocale=en_CA"
    LINKS_NEXT_PAGE  = "http://www.kijiji.ca/b-appartement-condo/ville-de-quebec"
    LINKS_TO_FOLLOW  = "http://www.kijiji.ca/v-appartement-condo-.*"
else:
    MAP_LATLNG       = [45.545046, -73.716665]# your city latitude and longitude
    START_URL       = "http://www.kijiji.ca/b-chambres-a-louer-colocataire/grand-montreal/c36l80002?ad=offering&siteLocale=en_CA"
    LINKS_NEXT_PAGE = "http://www.kijiji.ca/b-chambres-a-louer-colocataire/grand-montreal"
    LINKS_TO_FOLLOW = "http://www.kijiji.ca/v-chambres-a-louer-colocataire/.*"

#http://www.kijiji.ca/v-chambres-a-louer-colocataire/ville-de-montreal/transport-small-moving/1173170938?enableSearchNavigationFlag=true

MAPQUEST_API_KEY = ""

class Appartement(scrapy.Item):
    """Definition of items which went to retrieve"""
    url = scrapy.Field()
    address = scrapy.Field()
    price = scrapy.Field()
    title = scrapy.Field()

    description = scrapy.Field()
    date_listed = scrapy.Field()
    num_bathrooms = scrapy.Field()
    #num_bedrooms = scrapy.Field()


class Kijiji(CrawlSpider):
    """Definition of the kijiji spider crawler"""
    m_map = folium.Map(location=MAP_LATLNG, zoom_start=MAP_ZOOM)
    name = "kijiji"
    allowed_domains = ["kijiji.ca"]
    start_urls = ["%s&price=%d__%d" % (START_URL, MIN_PRICE, MAX_PRICE)]
    #start_urls = START_URL

    print(start_urls)
#Other way : http://stackoverflow.com/questions/32624033/scrapy-crawl-with-next-page
    # rules = (Rule(LinkExtractor(allow=(), restrict_xpaths=('//a[@title="Next"]',)), callback="parse_item", follow= True),)

    #print(rules.)
    rules = [
        # Extract link
        Rule(
            LinkExtractor(
                allow=[LINKS_TO_FOLLOW]
            ),
            callback='parse_item'),
        Rule(
            LinkExtractor(
                allow=["%s/page-[0-%d]/.*" % (LINKS_NEXT_PAGE, MAX_PAGE)]
            )
        )
    ]

    def __init__(self, *a, **kw):
        """Attach a callback to the spider_closed signal"""
        super(Kijiji, self).__init__(*a, **kw)
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_closed(self, spider):
        """Handle the spider_closed event to save the map"""
        self.m_map.save('map.html')

    def parse_item(self, response):
        """The item parser callback"""
        appartement = Appartement()

        appartement["url"] = response.url
        appartement["address"] = self._extract_field(response, "Address")
        appartement["price"] = self._extract_field(response, "Price")
        appartement["title"] = self._extract_title(response)

        #    phone  http://stackoverflow.com/questions/6682503/click-a-button-in-scrapy


        # from source :: https://github.com/mfournierca/kijiji_scraper/blob/master/kijiji_scraper/spiders/aptmnt_spider.py
        appartement["date_listed"] = self._extract_field(response, "Date Listed")
        appartement["num_bathrooms"] = self._extract_field(response, "Bathrooms (#)")
        appartement["description"] = self._extract_description(response)
        #appartement["num_bedrooms"] = self._extract_bedrooms(response)


        self.add_marker(appartement)

        return appartement

    def add_marker(self, appartement):
        """Helper function to add a marker on the map"""
        # folium.Marker(self.geocode(appartement),
        #               popup=self.popup(appartement),
        #               icon=folium.Icon(color=self.color_price(appartement)),
        #               ).add_to(self.m_map)

        print(appartement)

        folium.CircleMarker(location=self.geocode(appartement),
                            popup=self.popup(appartement),
                            radius=200,
                            fill_color=self.color_price(appartement),
                            fill_opacity=self.delta_ratio_day(date_in=appartement["date_listed"],
                                                                    denum=MAX_POST_DAYS)).add_to(self.m_map)

    def popup(self, appartement):
        """Helper function to create a popup with appartement informations"""
        html = """{price}<br>
                    <a href={url} target=_blank>{title}<a/>
                    <br>{description}""".format(url=appartement["url"],
                                                title=appartement["title"],
                                                price=appartement["price"],
                                                description=appartement["description"])
        iframe  = folium.element.IFrame(html=html, width=500, height=100)
        popup   = folium.Popup(iframe, max_width=500)

        return popup

    def color_price(self, appartement):
        """Helper function to return a color for marker based on price"""
        price = float(appartement["price"][1:])
        print(price)
        if price < GREEN_PRICE:
            color = 'green'
        elif price < ORANGE_PRICE:
            color = 'orange'
        else:
            color = 'red'

        return color

    def geocode(self, appartement):
        """Retrieve the lat and long using different fallback services"""
        g = geocoder.google(appartement["address"])
        if not g.latlng:
            g = geocoder.osm(appartement["address"])
            if not g.latlng and MAPQUEST_API_KEY:
                g = geocoder.mapquest(appartement["address"], key=MAPQUEST_API_KEY)

        # if we can't geocode the address, we return the map center
        if g.latlng:
            return g.latlng
        else:
            return MAP_LATLNG

    @staticmethod
    def _extract_title(response):
        """Retrieve the title based on xpath"""
        l = " ".join(response.xpath("//h1/text()").extract())
        return l.strip() if l else None

    @staticmethod
    def _extract_field(response, fieldname):
        """Retrieve the html field based on xpath"""
        l = response.xpath("//th[contains(text(), '{0}')]/following::td[1]//./text()".
                           format(fieldname)).extract()
        return l[0].strip() if l else None

    @staticmethod
    def _clean_string(string):
        for i in [",", "\n", "\r", ";", "\\"]:
            string = string.replace(i, "")
        return string.strip()

    def _extract_description(self, response):
        l = " ".join(response.xpath("//span[@itemprop='description']/text()").extract())
        return self._clean_string(l)

#    def _extract_bedrooms(self, response):
#        r = re.search(r'kijiji.ca\/v-(\d)-bedroom-apartments-condos', response.url)
#        return r.group(1).strip() if r else None

    @staticmethod
    def delta_ratio_day(date_in, denum):
        now = datetime.date.today()
        i = datetime.datetime.strptime(date_in, "%d-%b-%y").date()
        return 1-min(abs((now - i).days/denum), 1.0) # [0,1]


# Entry point
process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})

process.crawl(Kijiji)
process.start()
