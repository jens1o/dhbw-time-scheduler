import unittest

from functions import get_half_hour_range

class FunctionTests(unittest.TestCase):

    def test_half_hour_range(self):
        self.assertEqual(get_half_hour_range(87.5, 88), [87.5])
        self.assertEqual(get_half_hour_range(6, 7), [6, 6.5])

if __name__ == '__main__':
    unittest.main()