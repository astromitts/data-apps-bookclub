import unittest

class InitializationTests(unittest.TestCase):

    def test_sanity(self):
        self.assertEqual(2+2, 4)

    def test_import(self):
        try:
            import octavo
        except ImportError:
            self.fail("could not import octavo")
