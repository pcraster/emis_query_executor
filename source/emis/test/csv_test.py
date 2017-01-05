import unittest
import sys
import os
import csv
# TODO
sys.path.append("../../")
import emis


class CSVInputFileTestCase(unittest.TestCase):

    def test_01(self):
        """ Input CVS file does not exist """
        with self.assertRaisesRegexp(
                ValueError, "Input location cohort csv file 'not_there.csv' does not exist"):
            emis._check_csv.validate_location_input("not_there.csv")

    def test_02(self):
        """ No headers in CSV """
        with self.assertRaisesRegexp(
                ValueError, "Input file 'data/cohort2.csv' does not appear to have a header"):
            in_name = os.path.join("data", "cohort2.csv")
            emis._check_csv.validate_location_input(in_name)

    def test_03(self):
        """  String value in column """
        with self.assertRaisesRegexp(
                RuntimeError, "Incorrect longitude value in row 6 \('none'\)"):
            in_name = os.path.join("data", "cohort3.csv")
            emis._check_csv.validate_location_input(in_name)

    def test_04(self):
        """  Empty coordinate value """
        with self.assertRaisesRegexp(RuntimeError, "Incorrect latitude value in row 7 \(''\)"):
            in_name = os.path.join("data", "cohort4.csv")
            emis._check_csv.validate_location_input(in_name)

    def test_05(self):
        """  No records given, no failure expected here """
        in_name = os.path.join("data", "cohort5.csv")
        emis._check_csv.validate_location_input(in_name)

    def test_06(self):
        """  Wrong delimiter """
        with self.assertRaisesRegexp(ValueError, "Delimiter of input file 'data/cohort6.csv' is ';' and not ','"):
            in_name = os.path.join("data", "cohort6.csv")
            emis._check_csv.validate_location_input(in_name)

    def test_07(self):
        """  Not enough columns given """
        with self.assertRaisesRegexp(RuntimeError, "Value not provided for longitude in row 10"):
            in_name = os.path.join("data", "cohort7.csv")
            emis._check_csv.validate_location_input(in_name)

    def test_08(self):
        """  Not a CSV file """
        with self.assertRaisesRegexp(csv.Error, "Could not determine delimiter"):
            in_name = os.path.join("data", "cohort1.xlsx")
            emis._check_csv.validate_location_input(in_name)


if __name__ == "__main__":
    unittest.main()
