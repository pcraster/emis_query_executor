from flask import jsonify
from . import api_blueprint


# @api_blueprint.route("/api")
# def api():
#     return jsonify({
#             "resources": {
#                 "aggregate_methods": {
#                     "route": "/aggregate_methods"
#                 },
#                 "aggregate_queries": {
#                     "route": "/aggregate_queries"
#                 }
#             }
#         }), 200
