import math

import h5py
import lue


class QueryLUE(object):

    """
    Class providing access to the LUE database
    - try to get information/methods from lue module as far as this is possible
    - the remaining functionality can be provided by the h5py module
    """

    def __init__(self, lue_filename, phenomenon, property_set, property_name):
        # As we can't mix lue and h5py, we need references for both
        self._lue = None
        self._exposome = phenomenon

        self.phenomenon_name = phenomenon
        self.property_set_name = property_set
        self.property_name = property_name

        self._init_db_refs(lue_filename)

        self._lue_filename = lue_filename

        # fttb, get information required to calculate coordinate transformation
        # with LUE
        self._rows = None
        self._cols = None
        self._init_shape()
        self._west = None
        self._north = None
        self._cellsize = None
        self._init_discretization()

        self._raster_path_head = None
        self._raster_path_tail = None

        self._init_raster_path()

        #
        self._lue = None
        # To obtain the array values use h5py fttb.

    def _init_discretization(self):
        """ Helper function to obtain the discretisation """

        property_path = self._lue.phenomena[self.phenomenon_name].property_sets[
            self.property_set_name].properties[self.property_name].id.pathname

        band1_coordinates = "{}/lue_domain/lue_space/coordinates".format(
            property_path)

        tmp_h5py = h5py.File(self._lue_filename, "r")

        x1, y1, x2, y2 = tmp_h5py.get(band1_coordinates)[0]

        self._west = x1
        self._north = y2
        self._cellsize = (x2 - x1) / self._cols

    def _init_shape(self):
        """
            Helper method to get the number of rows and columns
        """
        property_path = self._lue.phenomena[self.phenomenon_name].property_sets[
            self.property_set_name].properties[self.property_name].id.pathname

        band1_values = "{}/value/value/0".format(property_path)

        tmp_h5py = h5py.File(self._lue_filename, "r")

        self._rows, self._cols = tmp_h5py.get(band1_values).shape

    def _init_db_refs(self, lue_filename):
        self._lue = lue.open_dataset(lue_filename, lue.access_flag.ro)

    def _init_raster_path(self):
        """ Helper function, replace with LUE function later on """

        property_path = self._lue.phenomena[self.phenomenon_name].property_sets[
            self.property_set_name].properties[self.property_name].id.pathname

        values = property_path.split(self._exposome)

        self._raster_path_head = values[0]
        self._raster_path_tail = values[1]

    def get_values_path(self, phenomenon_name):
        """ Helper function, replace with LUE function later on """
        path = "{}{}{}/value/value/0".format(
            self._raster_path_head, phenomenon_name, self._raster_path_tail)

        return path

    def _shape(self):
        """ Helper function, replace with LUE function later on """
        return self._rows, self._cols

    def _coords_to_map_indices(self, lat, lon):
        """
        Conversion of (latlon) coordinate pair to row and column array indices
        """

        # The next lines should be replaced later on with LUE calls
        west = self._west
        north = self._north
        cellSize = self._cellsize
        nr_rows, nr_cols = self._shape()

        xCol = (lon - west) / cellSize
        yRow = (north - lat) / cellSize

        row_idx = int(math.floor(yRow))
        col_idx = int(math.floor(xCol))

        # In case the user provided some coordinates outside the map extent
        # return error value atm
        # fttb we'll check for -1 later on
        if row_idx < 0 or row_idx > nr_rows:
            col_idx = -1
            row_idx = -1

        if col_idx < 0 or col_idx > nr_cols:
            col_idx = -1
            row_idx = -1

        return row_idx, col_idx
