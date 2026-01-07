import unittest

from gmshterrain import _read_csv_and_strip_header

class Test_read_csv_and_strip_header(unittest.TestCase):
    def test_without_headers(self):
        """Tests import works without headers"""
        expected = [[12.0, 5.0, 2.0], [13.0, 5.0, 6.0]]
        result = _read_csv_and_strip_header("./tests/test_data/test_csv/without_header.csv")
        self.assertEqual(result,expected)

    def test_with_headers(self):
        """Tests import works with headers"""
        expected = [["x","y","z"],[12,5,23],[53,2,5]]
        result = _read_csv_and_strip_header("./tests/test_data/test_csv/with_header.csv")
        self.assertEqual(result,expected)

    @unittest.skip("Test Not Implemented")
    def test_bad_file(self):
        pass

    @unittest.skip("Test Not Implemented")
    def test_no_file(self):
        pass

if __name__ == "__main__":
    unittest.main(verbosity=2)