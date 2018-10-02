import unittest

from commonFunctions import is_number, valid_input

"""
01- 10 - 2018
Ran 5 tests in 0.001s

OK
"""


class LeapTest(unittest.TestCase):
    def test_is_number_str(self):
        self.assertIs(is_number('Eggs'), False)

    def test_is_number_number_int(self):
        self.assertIs(is_number(1970), True)

    def test_is_number_number_str(self):
        self.assertIs(is_number('1970'), True)

    def test_valid_input(self):
        self.assertIs(valid_input('eggs', ['eggs', 'spam', 'snakes']), True)

    def test_valid_input2(self):
        self.assertIs(valid_input('eggs', ['spam', 'snakes', 'r/programming']), False)


if __name__ == '__main__':
    unittest.main()
