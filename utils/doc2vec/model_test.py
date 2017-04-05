import unittest
from utils.doc2vec.model import  Model
from random import randint
import pandas as pd


class ModelsTest(unittest.TestCase):


    def test_refute_malformed_bodies(self):
        with self.assertRaises(AssertionError):
            df = pd.DataFrame({'A': [randint(1, 9) for x in range(10)],
                               'B': [randint(1, 9) * 10 for x in range(10)],
                               'C': [randint(1, 9) * 100 for x in range(10)]})
            Model(df)

    def test_accept_wellformed_bodies(self):
        df = pd.DataFrame({'Sentence': [randint(1, 9) for x in range(10)],
                           'Body ID': [randint(1, 9) * 10 for x in range(10)],
                           'Sentence ID': [randint(1, 9) * 100 for x in range(10)]})
        m = Model(df)
        m.train()
        # if it trained successfully, I should know!
        self.assertTrue(m.is_trained())
