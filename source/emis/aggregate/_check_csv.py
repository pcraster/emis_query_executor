import os
import csv
import mimetypes


def validate_location_input(filename):
    """
    Function that does simple checks whether the content given in filename
    conforms to the id,lat,lon format
    Throws Exception for internal problems
    Throws RuntimeError for user input errors
    """

    if not os.path.exists(filename):
        msg = "Input location cohort csv file '{}' does not exist".format(
            filename)
        raise Exception(msg)

    ftype, fenc = mimetypes.guess_type(filename)
    if ftype != "text/csv":
        msg = "Input file '{}' does not seem to be a CSV file".format(
            os.path.basename(filename))
        raise RuntimeError(msg)

    with open(filename) as csvfile:
        try:
            sample = csvfile.read(1024)
            dialect = csv.Sniffer().sniff(sample)
        except UnicodeDecodeError as err:
            msg = "Input file '{}' contains invalid UTF-8 characters".format(
                os.path.basename(filename))
            raise RuntimeError(msg)
        except csv.Error as msg:
            msg = "{} in the input file '{}'".format(msg,
                os.path.basename(filename))
            raise RuntimeError(msg)

        if not csv.Sniffer().has_header(sample):
            msg = "Input file '{}' does not appear to have a header".format(
                os.path.basename(filename))
            raise RuntimeError(msg)

        if dialect.delimiter is not ",":
            msg = "Delimiter of input file '{}' is '{}' and not ','".format(
                os.path.basename(filename), dialect.delimiter)
            raise RuntimeError(msg)

    # Basically, iterate over rows and try data conversion and see where it
    # fails
    with open(filename) as csvfile:
        # Remove potentially present whitespace in header row
        header = [col_name.strip() for col_name in next(csvfile).split(",")]
        reader = csv.DictReader(csvfile, fieldnames=header)
        row_nr = 1    # Row number in user format
        try:
            for row in reader:
                try:
                    tmp = int(row["id"])
                except ValueError:
                    msg = "Id in row {} ('{}') in input file '{}' is not of type integer".format(
                        row_nr, row["id"], os.path.basename(filename))
                    raise RuntimeError(msg)

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
                os.path.basename(filename), err)
            raise RuntimeError(msg)
