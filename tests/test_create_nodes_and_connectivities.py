import unittest

from gmshterrain import _check_data_is_gridded_and_return_summaries , _read_csv_and_strip_header , _create_nodes_and_connectivities , _tag

import math

class Test_create_nodes_and_connectivities(unittest.TestCase):

    def test_against_example_function(self):
        """Tests create nodes function against pre-built data"""
        #This block pulls in pre-existing data
        from tests.test_data.test_geometry.Wave_100x100 import Wave_100x100
        exp_coords = Wave_100x100['coords']
        exp_nodes = Wave_100x100['nodes']
        exp_tris = Wave_100x100['tris']
        exp_lin = Wave_100x100['lin']
        exp_pnt = Wave_100x100['pnt']

        #This block generates our test coords
        N = 100
        M = 100
        coords = []
        for i in range(N + 1):
            for j in range(M + 1):
                coords.extend([
                    float(i) / N,
                    float(j) / N,
                    0.05 * math.sin(10 * float(i + j) / N)
                ])
        #This block runs the function
        nodes,tris,lin,pnt = _create_nodes_and_connectivities(coords,N,M)

        #This block executes the tests
        self.assertEqual(exp_coords,coords)
        self.assertEqual(exp_nodes,nodes)
        self.assertEqual(exp_tris,tris)
        self.assertEqual(exp_lin,lin)
        self.assertEqual(exp_pnt,pnt)

if __name__ == "__main__":
    unittest.main(verbosity=2)