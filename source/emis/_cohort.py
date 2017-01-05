

class Cohort(object):
    """
    Helper class that stores information for a location (cohort record)
    """

    def __init__(self, uuid, lat, lon, row, col):
        self._id = uuid
        self._lat = lat
        self._lon = lon
        self._row_idx = row
        self._col_idx = col
        self._values = []

    def __str__(self):
        """ CSV string (output) representation of a row """
        row = "{}".format(self._id)
        for value in self._values:
            if value < 0:
                row += ",1e31"
            else:
                row += ",{:.4f}".format(value)

        row += "\n"

        return row

    def add_value(self, value):
        """ Plainly append exposome values """
        self._values.append(value)


class Cohorts(object):

    """ Helper class that holds cohort information """

    def __init__(self, header):
        self._header = header
        self._outputs = []

    def __str__(self):
        content = self._header
        for r in self._outputs:
            content += str(r)

        return content

    def add(self, uuid, lat, lon, r, c):
        self._outputs.append(Cohort(uuid, lat, lon, r, c))

    def rows(self):
        return self._outputs
