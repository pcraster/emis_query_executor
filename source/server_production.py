import os
os.environ["EMIS_QUERY_EXECUTOR_CONFIGURATION"] = "production"
from server import app


app.run(host="0.0.0.0")
