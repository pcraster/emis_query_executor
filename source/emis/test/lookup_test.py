import unittest
import sys
import os
# TODO
sys.path.append("../../")
import emis.aggregate


class CoordinateLookup(unittest.TestCase):

    def test_01(self):
        """ Output CVS file already exists """
        out_name = os.path.join(os.path.dirname(__file__), "data",
            "cohort1.csv")

        with self.assertRaisesRegex(
                ValueError,
                "Designated output file '{}' already exists".format(
                    out_name)):
            emis.aggregate._lookup._check_csv_output(out_name)

    def test_02(self):
        """  No write permissions to create the output file """
        with self.assertRaisesRegex(
                ValueError,
                "No write permissions for output file '/cohort1.csv'"):
            out_name = os.path.join("/", "cohort1.csv")
            emis.aggregate._lookup._check_csv_output(out_name)

    def test_03(self):
        """ No exposomes given """
        with self.assertRaisesRegex(ValueError, "No exposomes provided"):
            in_name = os.path.join(os.path.dirname(__file__), "data",
                "cohort1.csv")
            out_name = os.path.join("/", "tmp", "cohort1_out.csv")
            if os.path.exists(out_name):
                os.remove(out_name)
            emis.aggregate.coordinate_lookup(in_name, out_name, [])

    #def test_04(self):
        #""" Just an usage example """
        #in_name = os.path.join("data", "cohort1.csv")
        #out_name = os.path.join("/", "tmp", "cohort1_out.csv")
        #exposomes = ["/data/NO2.lue", "/data/NO2_199.lue"]
        #emis.coordinate_lookup(in_name, out_name, exposomes)

if __name__ == "__main__":
    unittest.main()
