import unittest
from utils.doc2vec.model import  Model
from random import randint
import pandas as pd


class ModelsTest(unittest.TestCase):


    def test_directory_is_constant(self):
        df = pd.DataFrame({'Sentence': [randint(1, 9) for x in range(10)],
                           'Body ID': [randint(1, 9) * 10 for x in range(10)],
                           'Sentence ID': [randint(1, 9) * 100 for x in range(10)]})
        # before training
        m = Model(df)
        m1 = Model(df)
        self.assertEqual(m.persistence_directory(), m1.persistence_directory())
        # after training
        m.train(force = True)
        self.assertEqual(m.persistence_directory(), m1.persistence_directory())

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
        # if I create a new Model with same parameters it should remember that I was trained:
        m1 = Model(df)
        self.assertEqual(m.persistence_directory(), m1.persistence_directory())
        self.assertTrue(m1.is_trained())

