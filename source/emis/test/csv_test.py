import unittest
import sys
import os
import csv
# TODO
sys.path.append("../../")
import emis.aggregate


class CSVInputFileTestCase(unittest.TestCase):

    if sys.version_info[0] == 2:
        raise RuntimeError("Python 3 required")

    def test_01(self):
        """ Input CVS file does not exist """
        with self.assertRaisesRegex(
                Exception,
                "Input location cohort csv file 'not_there.csv' "
                    "does not exist"):
            emis.aggregate._check_csv.validate_location_input("not_there.csv")

    def test_02(self):
        """ No headers in CSV """
        in_name = os.path.join(os.path.dirname(__file__), "data",
            "cohort2.csv")

        with self.assertRaisesRegex(
                RuntimeError,
                "Input file '{}' does not appear to have a header".format(
                    os.path.basename(in_name))):
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

        with self.assertRaisesRegex(RuntimeError,
                "Delimiter of input file '{}' is ';' and not ','".format(
                    os.path.basename(in_name))):
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
                    os.path.basename(in_name))):
            emis.aggregate._check_csv.validate_location_input(in_name)

    def test_09(self):
        """  Empty CSV file """
        in_name = os.path.join(os.path.dirname(__file__), "data",
            "empty_cohort.csv")
        if os.path.exists(in_name):
            os.remove(in_name)
        with open(in_name, "w"):
            pass

        with self.assertRaisesRegex(RuntimeError,
                "Could not determine delimiter in the input file '{}'".format(
                    os.path.basename(in_name))):
            emis.aggregate._check_csv.validate_location_input(in_name)


    def test_10(self):
        """  Spaces in header """
        in_name = os.path.join(os.path.dirname(__file__), "data",
            "cohort10.csv")

        emis.aggregate._check_csv.validate_location_input(in_name)


    def test_11(self):
        """ Unicode  """
        in_name = os.path.join(os.path.dirname(__file__), "data",
            "cohort11.csv")

        with self.assertRaisesRegex(RuntimeError,
                "Input file '{}' contains invalid UTF-8 characters".format(
                    os.path.basename(in_name))):
            emis.aggregate._check_csv.validate_location_input(in_name)


if __name__ == "__main__":
    unittest.main()
