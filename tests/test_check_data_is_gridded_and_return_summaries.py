import unittest

from gmshterrain import _check_data_is_gridded_and_return_summaries , _read_csv_and_strip_header

class Test__check_data_is_gridded_and_return_summaries(unittest.TestCase):

    def test_return_statistics(self):
        """Tests that the functon returns correct max and min values"""
        exp_x_max , exp_x_min, exp_y_max, exp_y_min = 100,-5,36,-5
        data = _read_csv_and_strip_header("./tests/test_data/test_gridded/warden_gridded.csv")
        x_max,x_min,y_max,y_min,N,M = _check_data_is_gridded_and_return_summaries(data)
        self.assertEqual(x_max,exp_x_max)
        self.assertEqual(x_min,exp_x_min)
        self.assertEqual(y_max,exp_y_max)
        self.assertEqual(y_min,exp_y_min)

    def test_correct_N_and_M_calclated(self):
        N_exp, M_exp = 211,83
        data = _read_csv_and_strip_header("./tests/test_data/test_gridded/warden_gridded.csv")
        x_max,x_min,y_max,y_min,N,M = _check_data_is_gridded_and_return_summaries(data)
        self.assertEqual(N,N_exp)
        self.assertEqual(M,M_exp)

    @unittest.skip("Feature Not Implemented")
    def test_identifies_gridded_data(self):
        pass

    @unittest.skip("Feature Not Implemented")
    def test_identifies_non_gridded_data_X(self):
        pass

    @unittest.skip("Feature Not Implemented")
    def test_identifies_non_gridded_data_Y(self):
        pass

if __name__ == "__main__":
    unittest.main(verbosity=2)