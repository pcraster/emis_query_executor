import unittest
import sys
import os
import tempfile
import shutil
import filecmp
# TODO

sys.path.append("../../")
import emis.aggregate


class CoordinateLookup(unittest.TestCase):

    if sys.version_info[0] == 2:
        raise RuntimeError("Python 3 required")

    def test_01(self):
        """ Output CVS file already exists """
        out_name = os.path.join(os.path.dirname(__file__), "data",
            "cohort1.csv")

        with self.assertRaisesRegex(
                Exception,
                "Designated output file '{}' already exists".format(
                    out_name)):
            emis.aggregate._lookup._check_csv_output(out_name)

    def test_02(self):
        """  No write permissions to create the output file """
        with self.assertRaisesRegex(
                Exception,
                "No write permissions for output file '/cohort1.csv'"):
            out_name = os.path.join("/", "cohort1.csv")
            emis.aggregate._lookup._check_csv_output(out_name)

    def test_03(self):
        """ No exposomes given """
        with self.assertRaisesRegex(Exception, "No exposomes provided"):
            in_name = os.path.join(os.path.dirname(__file__), "data",
                "cohort1.csv")
            out_name = os.path.join("/", "tmp", "cohort1_out.csv")
            if os.path.exists(out_name):
                os.remove(out_name)
            emis.aggregate.coordinate_lookup(in_name, out_name, [])

    def test_04(self):
        """ An usage example """
        in_name = os.path.join(os.path.dirname(__file__), "data",
                "cohort1.csv")
        tmp_dir = tempfile.mkdtemp(prefix="emis_aggregate_")
        out_name = os.path.join(tmp_dir, "cohort1_out.csv")

        fname1 = os.path.join(os.path.dirname(__file__), "data",
                "NO2.lue")
        pname1 = "/lue_phenomena/NO2/lue_property_sets/areas/lue_properties/band_1"

        fname2 = os.path.join(os.path.dirname(__file__), "data",
                "NO2_100.lue")
        pname2 = "/lue_phenomena/NO2_100/lue_property_sets/areas/lue_properties/band_1"
        exposomes = [(fname1, pname1), (fname2, pname2)]

        emis.aggregate.coordinate_lookup(in_name, out_name, exposomes)


        val_content = """id,NO2,NO2_100
1,31.8611,59.4830
2,17.8521,32.4318
3,21.9757,37.4788
4,18.7754,32.7407
5,30.7442,63.5387
6,18.2951,32.5841
7,11.1832,23.8212
8,1e31,1e31
9,13.6680,27.4743
10,16.8252,36.2561
"""
        val_out = os.path.join(tmp_dir, "validated_res_1.csv")
        with open(val_out, "w") as val:
          val.write(val_content)

        equal_content = filecmp.cmp(out_name, val_out)

        self.assertTrue(equal_content)

        shutil.rmtree(tmp_dir)

    def test_05(self):
        """ Coordinates at map extent borders """
        in_name = os.path.join(os.path.dirname(__file__), "data",
            "lookup05.csv")
        out_name = os.path.join("/", "tmp", "lookup05_out.csv")

        if os.path.exists(out_name):
            os.remove(out_name)

        fname = os.path.join(os.path.dirname(__file__), "data",
                "NO2_100.lue")
        pname = "/lue_phenomena/NO2_100/lue_property_sets/areas/lue_properties/band_1"
        exposomes = [(fname, pname)]
        emis.aggregate.coordinate_lookup(in_name, out_name, exposomes)

if __name__ == "__main__":
    unittest.main()
