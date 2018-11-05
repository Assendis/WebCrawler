import unittest

from db_management import DataManagement

class DataTestArea(unittest.TestCase):
    def test_area(self):
        url = "test-url/%2D-test-test"
        source = "test-hurriyet.com"
        data = DataManagement()

        self.assertTrue(data.add_new_url(url, source))
        self.assertEqual(data.check(url, source)[1], url)
        self.assertEqual(data.get_statistics()[source], 1)

        data.db.execute('DELETE from urls where url = "%s"' % url)
        data.db.commit()

        self.assertFalse(data.check(url, source))

