import unittest
from utils.Utils import get_git_root, append_to_git_root, pad
import numpy as np
from random import randint

class UtilsTest(unittest.TestCase):

# ################ path concatenation
    def test_path_concatenation_easy(self):
        partial_path = 'something/or/other'
        alt_root = "my/directory"
        res = append_to_git_root(partial_path, alternate_root=alt_root)
        git_root = get_git_root()
        if git_root == '':
            self.assertEqual(res, '{}/{}'.format(alt_root, partial_path))
        else:
            self.assertEqual(res, '{}/{}'.format(git_root, partial_path))

    def test_path_concatenation_tricky_1(self):
        partial_path = './something/or/other'
        alt_root = "my/directory/.."
        res = append_to_git_root(partial_path, alternate_root=alt_root)
        git_root = get_git_root()
        if git_root == '':
            self.assertEqual(res, 'my/something/or/other')
        else:
            self.assertEqual(res, '{}/{}'.format(git_root, 'something/or/other'))


    def test_path_concatenation_tricky_2(self):
        partial_path = './something/or/other'
        alt_root = "."
        res = append_to_git_root(partial_path, alternate_root=alt_root)
        git_root = get_git_root()
        if git_root == '':
            self.assertEqual(res, './something/or/other')
        else:
            self.assertEqual(res, '{}/{}'.format(git_root, './something/or/other'))

# ################ padding an array
    def test_pad_good_size(self):
        array_dim_x = randint(1, 100)
        array_dim_y = randint(1, 100)
        an_array = np.random.rand(array_dim_x, array_dim_y)
        pad_to_dim = randint(1, 100)
        r = pad(an_array, pad_to_dim)
        self.assertEqual(r.shape[0], pad_to_dim,
                         "array initially size ({},{}), padding to {}".format(array_dim_x, array_dim_y,pad_to_dim))

