import os
import csv
import h5py
from ._check_csv import validate_location_input
from ._lue_db import QueryLUE
from ._cohort import Cohorts


def _check_csv_output(csv_outputname):

    # Checks for cohort output files
    if os.path.exists(csv_outputname):
        msg = "Designated output file '{}' already exists".format(
            csv_outputname)
        raise Exception(msg)

    try:
        with open(csv_outputname, "w") as csv_out:
            pass
    except IOError as err:
        msg = "No write permissions for output file '{}'".format(
            csv_outputname)
        raise Exception(msg)


def _check_exposomes(exposome_paths):

    # Checks for exposomes
    if len(exposome_paths) == 0:
        msg = "No exposomes provided"
        raise Exception(msg)

    for lue_filename, prop_path in exposome_paths:
        if not os.path.exists(lue_filename):
            msg = "Input database '{}' does not exist".format(lue_filename)
            raise Exception(msg)


def _exposome_property_names(exposome_paths):
    variables = []

    for fs_path, p_path in exposome_paths:
        head, tail = os.path.split(fs_path)
        varname, ext = os.path.splitext(tail)
        variables.append(varname)

    return variables


def coordinate_lookup(csv_inputname, csv_outputname, exposome_paths):
    """
    retrieves exposome values for a cohort given in a csv file
    """

    # First do some basic tests wrt input and output arguments
    validate_location_input(csv_inputname)
    _check_csv_output(csv_outputname)
    _check_exposomes(exposome_paths)

    # Retrieve the names of the exposomes
    exposomes = _exposome_property_names(exposome_paths)

    # Reference to one! LUE database
    # fttb (all datasets same extent), we can just open the first LUE dataset
    # to obtain dataset characteristics
    phenomenon_name = exposomes[0]
    property_set_name = "areas"
    property_name = "band_1"

    _lue = QueryLUE(
        exposome_paths[0][0], phenomenon_name, property_set_name, property_name)

    # Temporary structure holding coordinate and exposome value information
    header = "id,{}\n".format(",".join(exposomes))
    _output = Cohorts(header)

    # First, we transform for all rows/locations the coordinates to array
    # indices
    with open(csv_inputname) as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            uuid = int(row["id"])
            lat = float(row["lat"])
            lon = float(row["lon"])
            row_idx, col_idx = _lue._coords_to_map_indices(lat, lon)
            _output.add(uuid, lat, lon, row_idx, col_idx)

    # Then obtain the cell values for each exposome
    for idx, exposome in enumerate(exposomes):

        lue_prop_str = _lue.get_values_path(exposome)

        # Read whole array for current exposome
        lue_db = h5py.File(exposome_paths[idx][0], "r")
        raster = lue_db.get(lue_prop_str)[...]

        # Lookup values
        for row in _output.rows():
            r = row._row_idx
            c = row._col_idx

            value = raster[r][c]

            # Coordinate outside extent receive MV
            if r == -1:
                value = -1
            # MV cell
            if value < 0:
                value = -1

            row.add_value(value)

    # Write the IDs and exposome values to the output csv file
    with open(csv_outputname, "w") as csv_out:
        csv_out.write(str(_output))
