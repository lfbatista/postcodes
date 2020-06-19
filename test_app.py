import unittest

from app import get_stores


class TestApp(unittest.TestCase):
    def setUp(self):
        self.get_stores = get_stores

    def test_get_stores(self):
        """ :return a list of stores in a given radius of a given postcode sorted from north to south """
        expected_output = [{'name': 'Hatfield Central 5JJ', 'postcode': 'AL9 5JJ'},
                           {'name': 'Hatfield Central 5JP', 'postcode': 'AL9 5JP'},
                           {'name': 'Hatfield Central 5JY', 'postcode': 'AL9 5JY'}]
        self.assertEqual(self.get_stores('AL9 5JP', '150'), expected_output)


if __name__ == '__main__':
    unittest.main()
