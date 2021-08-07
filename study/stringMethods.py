import unittest


class MyTestCase(unittest.TestCase):
    def test_format(self):
        string = '{name} is from {country}'
        result = string.format_map(dict(name='alvin', country='China'))
        self.assertEqual(result, 'alvin is from China')

if __name__ == '__main__':
    unittest.main()
