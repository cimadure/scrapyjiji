import unittest
from scrapy.selector import Selector
from kijiji.kijiji.spiders.kijiji import KijijiSpider


class TestItemPage(unittest.TestCase):
    def setUp(self):
        self.selector = Selector(text=open("page.html", 'r', encoding="utf8").read())#, type='html')
        # Selector(text='', type="html")

    def test_something(self):
        pass

    def test_ad_id_numbers(self):
        number_of_ads = sum(1 for _ in  KijijiSpider.ad_id(self.selector))
        self.assertEqual(25, number_of_ads)

    def test_ad_id_first_item(self):
        self.assertEqual('1418282298', KijijiSpider.ad_id(self.selector)[0])

    def test_get_next_page(self):
        self.assertEqual("/b-chambres-a-louer-colocataire/grand-montreal/page-2/c36l80002?ad=offering&minNumberOfImages=1",
                         KijijiSpider._get_next_page(self.selector))


if __name__ == '__main__':
    unittest.main()
