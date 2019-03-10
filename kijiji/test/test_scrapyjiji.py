import unittest
from scrapy.selector import Selector
from kijiji.kijiji.spiders.kijiji import KijijiSpider


class TestPage(unittest.TestCase):
    def setUp(self):
        self.selector = Selector(text=open("page.html", 'r', encoding="utf8").read())#, type='html')
        # Selector(text='', type="html")

    def test_ad_id_numbers(self):
        number_of_ads = sum(1 for _ in  KijijiSpider._get_ad_id(self.selector))
        self.assertEqual(25, number_of_ads)

    def test_ad_id_first_item(self):
        self.assertEqual('1418282298', KijijiSpider._get_ad_id(self.selector)[0])

    def test_get_next_page(self):
        self.assertEqual("/b-chambres-a-louer-colocataire/grand-montreal/page-2/c36l80002?ad=offering&minNumberOfImages=1",
                         KijijiSpider._get_next_page(self.selector))

    # def test_othejhjhjh(self):
    #     for href in self.selector.css('div.title'):
    #         print(href.css('a::text').extract_first())
    #         print(href.css('a::attr(href)').extract_first())
    #


PRICE_TEST = """<div class=""><h1 class="title-2323565163">BELLE CHAMBRE RENOVEE - NICE RENOVATED ROOM</h1><div class="priceContainer-2538502416"><span class="currentPrice-441857624"><span content="495.00" class="">$495.00</span></span></div></div>"""

LOCATION_TEST = """    <meta property="og:image" content="https://i.ebayimg.com/00/s/ODAwWDYwMA==/z/V-kAAOSwpUVceZyM/$_20.JPG"/><meta property="og:type" content="product"/><meta property="og:description" content="Disponible immediatement, chambre non fumeur, propre et tr&amp;egrave;s tranquille dans un immeuble s&amp;eacute;curitaire qui vient tout juste d’&amp;ecirc;tre r&amp;eacute;nov&amp;eacute;e. Parfait pour PVT, &amp;eacute;tudiants, touristes, travailleurs, et personnes tranquilles. Location mensuelle (minimum 1 mois). Les prix sont &amp;agrave; partir de 495$ en montant. Internet haute vitesse sans fil di"/><meta property="og:title" content="BELLE CHAMBRE RENOVEE - NICE RENOVATED ROOM | Room Rentals &amp; Roommates | City of Montréal | Kijiji"/><meta property="og:url" content="https://www.kijiji.ca/v-chambres-a-louer-colocataire/ville-de-montreal/belle-chambre-renovee-nice-renovated-room/1418127954?siteLocale=en_CA"/><meta property="og:latitude" content="45.563799"/><meta property="og:longitude" content="-73.5849067"/><meta property="og:locality" content="Greater Montréal - City of Montréal"/><meta property="og:region" content="montreal"/><script type="application/ld+json">"""


class TestAd(unittest.TestCase):

    def setUp(self):
        self.selector = Selector(text=open("ad.html", 'r', encoding="utf8").read())

    def test_price(self):
        self.assertEqual('$495.00', KijijiSpider._get_price(Selector(text=PRICE_TEST)))

    def test_price_in_page(self):
        self.assertEqual('$495.00', KijijiSpider._get_price(self.selector))

    def test_location_latitude(self):
        self.assertEqual('45.563799', KijijiSpider._get_latitude(self.selector))

    def test_location_longitude(self):
        self.assertEqual('-73.5849067', KijijiSpider._get_longitude(self.selector))

    def test_date_posted(self):
        self.assertEqual("2019-03-01T21:04:20.000Z", KijijiSpider._get_date_posted(self.selector))


if __name__ == '__main__':
    unittest.main()
