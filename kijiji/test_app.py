import unittest
import pandas as pd
import datetime

from .app import relative_freshness

class TestAlg(unittest.TestCase):
    def setUp(self):
        self.df = pd.read_json('test/unclean_data.json', orient='records', convert_dates=True)
        self.df = self.df.dropna()

    def test_1(self):
        #print(self.df.head(2))
        print(self.df['date_posted'])

    def test_relative_process(self):

        self.assertEqual([1, 0.6568416464627203, 0], relative_freshness(dates=pd.to_datetime(self.df["date_posted"][:3]), relative=pd.to_datetime(self.df["date_posted"][1])))


# class TestFunc(unittest.TestCase):
#     def test_relative_now(self):
#         now = datetime.datetime.utcnow()
#         self.assertEqual(1.0, relative_freshness(dates=now, relative=now))
#     #
    # def test_relative_now_one_ele(self):
    #     now = datetime.datetime.utcnow()
    #     self.assertEqual(1.0, relative_freshness(dates=[now], relative=now))