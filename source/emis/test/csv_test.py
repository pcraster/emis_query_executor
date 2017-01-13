import unittest
import sys
import os
import csv
# TODO
sys.path.append("../../")
import emis.aggregate


class CSVInputFileTestCase(unittest.TestCase):

    def test_01(self):
        """ Input CVS file does not exist """
        with self.assertRaisesRegex(
                ValueError,
                "Input location cohort csv file 'not_there.csv' "
                    "does not exist"):
            emis.aggregate._check_csv.validate_location_input("not_there.csv")

    def test_02(self):
        """ No headers in CSV """
        in_name = os.path.join(os.path.dirname(__file__), "data",
            "cohort2.csv")

        with self.assertRaisesRegex(
                ValueError,
                "Input file '{}' does not appear to have a header".format(
                    in_name)):
            emis.aggregate._check_csv.validate_location_input(in_name)

    def test_03(self):
        """  String value in column """
        with self.assertRaisesRegex(
                RuntimeError,
                "Incorrect longitude value in row 6 \('none'\)"):
            in_name = os.path.join(os.path.dirname(__file__), "data",
                "cohort3.csv")
            emis.aggregate._check_csv.validate_location_input(in_name)

    def test_04(self):
        """  Empty coordinate value """
        with self.assertRaisesRegex(
                RuntimeError, "Incorrect latitude value in row 7 \(''\)"):
            in_name = os.path.join(os.path.dirname(__file__), "data",
                "cohort4.csv")
            emis.aggregate._check_csv.validate_location_input(in_name)

    def test_05(self):
        """  No records given, no failure expected here """
        in_name = os.path.join(os.path.dirname(__file__), "data",
            "cohort5.csv")
        emis.aggregate._check_csv.validate_location_input(in_name)

    def test_06(self):
        """  Wrong delimiter """
        in_name = os.path.join(os.path.dirname(__file__), "data",
            "cohort6.csv")

        with self.assertRaisesRegex(ValueError,
                "Delimiter of input file '{}' is ';' and not ','".format(
                    in_name)):
            emis.aggregate._check_csv.validate_location_input(in_name)

    def test_07(self):
        """  Not enough columns given """
        with self.assertRaisesRegex(RuntimeError,
                "Value not provided for longitude in row 10"):
            in_name = os.path.join(os.path.dirname(__file__), "data",
                "cohort7.csv")
            emis.aggregate._check_csv.validate_location_input(in_name)

    def test_08(self):
        """  Not a CSV file """
        in_name = os.path.join(os.path.dirname(__file__), "data",
            "cohort1.xlsx")

        with self.assertRaisesRegex(RuntimeError,
                "Input file '{}' does not seem to be a CSV file".format(
               # "Delimiter of input file '{}' is ';' and not ','".format(
                    in_name)):
            emis.aggregate._check_csv.validate_location_input(in_name)


if __name__ == "__main__":
    unittest.main()
