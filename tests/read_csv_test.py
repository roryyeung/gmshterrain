import unittest

from gmshterrain import _read_csv_and_strip_header

class Test_read_csv_and_strip_header:
    def test_with_headers(self):
        self.assertTrue(True,"test")

    def test_without_headers(self):
        pass

if __name__ == "__main__":
    unittest.main(verbosity=2)