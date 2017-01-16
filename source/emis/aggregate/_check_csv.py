import os
import csv
import mimetypes


def validate_location_input(filename):
    """
    Function that does simple checks whether the content given in filename
    conforms to the id,lat,lon format
    Throws ValueError for internal problems
    Throws RuntimeError for user input errors
    """

    if not os.path.exists(filename):
        msg = "Input location cohort csv file '{}' does not exist".format(
            filename)
        raise ValueError(msg)

    ftype, fenc = mimetypes.guess_type(filename)
    if ftype != "text/csv":
        msg = "Input file '{}' does not seem to be a CSV file".format(
            filename)
        raise RuntimeError(msg)

    with open(filename) as csvfile:
        sample = csvfile.read(1024)
        dialect = csv.Sniffer().sniff(sample)

        if not csv.Sniffer().has_header(sample):
            msg = "Input file '{}' does not appear to have a header".format(
                filename)
            raise ValueError(msg)

        if dialect.delimiter is not ",":
            msg = "Delimiter of input file '{}' is '{}' and not ','".format(
                filename, dialect.delimiter)
            raise ValueError(msg)

    with open(filename) as csvfile:
        max_records = 2500
        reader = csv.reader(csvfile)
        nr_rows = len(list(reader)) - 1  # records w/o header

        if nr_rows > max_records:
            msg = "Number of rows ({}) in '{}' exceeds the row limit ({})".format(
                nr_rows, filename, max_records)
            raise ValueError(msg)

    # Basically, iterate over rows and try data conversion and see where it
    # fails
    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)
        row_nr = 1    # Row number in user format
        try:
            for row in reader:
                try:
                    tmp = int(row["id"])
                except ValueError:
                    msg = "Id in row {} ('{}') in input file '{}' is not of type integer".format(
                        row_nr, row["id"], filename)
                    raise ValueError(msg)

                try:
                    tmp = float(row["lat"])
                except ValueError:
                    msg = "Incorrect latitude value in row {} ('{}')".format(
                        row_nr, row["lat"])
                    raise RuntimeError(msg)
                except TypeError:
                    msg = "Value not provided for latitude in row {}".format(
                        row_nr)
                    raise RuntimeError(msg)

                try:
                    tmp = float(row["lon"])
                except ValueError:
                    msg = "Incorrect longitude value in row {} ('{}')".format(
                        row_nr, row["lon"])
                    raise RuntimeError(msg)
                except TypeError:
                    msg = "Value not provided for longitude in row {}".format(
                        row_nr)
                    raise RuntimeError(msg)

                row_nr += 1

        except KeyError as err:
            msg = "Input file '{}' does not contain required header key {}".format(
                filename, err)
            raise ValueError(msg)
