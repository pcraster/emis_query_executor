from flask import jsonify
from . import api_blueprint


@api_blueprint.route("/queries")
def queries():
    # TODO Dynamically figure out which queries we support.
    queries =  {
            "queries": {
                "query_groups":  [

                        # TODO hier verder

                    ],
                "aggregate_queries": [
                    ],
                "subset_queries":  [
                    ],
             }
        }

    return jsonify(queries), 200


### // Meta-info about kinds of queries that are supported by this
### // service.
### "queries": [
###     {

###         // Zero or more query groups.
###         // A query group is a group of queries sharing parameters.
###         "query_groups": [
###             {

###                 // Zero or more query groups of aggregate queries.
###                 "aggregate_queries": [
###                     {

###                         "parameters": [
###                             {
###                                 "name": "domain",
###                                 "description": "
### Locations in time and space of items to aggregate

### In the simplest case, for each item a point is space can be passed.
### Spatial points don't have an extent, so this renders all aggregate
### methods as simple lookup operations."
###                             },
###                             {
###                                 "name": "properties",
###                                 "description": "
### Properties to aggregate

### A list of properties."
###                             }
###                         ],

###                         "aggregate_queries": [
###                             {
###                                 "name": "maximum",
###                                 "description": "
### For all items, calculate the maximum value for all properties

### For each item, all values located within the extent in time and
### space are aggregated."
###                                 "parameters": [
###                                 ]
###                             },
###                             {
###                                 "name": "minimum",
###                                 "description": "
### For all items, calculate the minimum value for all properties

### For each item, all values located within the extent in time and
### space are aggregated."
###                                 "parameters": [
###                                 ]
###                             },
###                             {
###                                 "name": "mean",
###                                 "description": "
### For all items, calculate the mean value for all properties"

### For each item, all values located within the extent in time and
### space are aggregated."
###                                 "parameters": [
###                                 ]
###                             }
###                         ]
###                     }
###                 ],

###                 // Query group of subset queries.
###                 "subset_queries": [
###                 ]
###             }
###         ],

###         "aggregate_queries": [
###         ],

###         "subset_queries": [
###         ]
###     }
### ]
