import unittest

from scrapy.selector import Selector


class TestArticleItemPage(unittest.TestCase):
    def setUp(self):
        self.selector = Selector(text=open("page.html", 'r', encoding="utf8").read())#, type='html')
        # Selector(text='', type="html")

    def test_something(self):
        pass

    def test_ad_id(self):





if __name__ == '__main__':
    unittest.main()
