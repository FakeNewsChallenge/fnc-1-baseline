import unittest
from utils.Utils import get_git_root, append_to_git_root

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
            self.assertEqual(res, 'something/or/other')
        else:
            self.assertEqual(res, '{}/{}'.format(git_root, 'something/or/other'))

# ################ padding an array

