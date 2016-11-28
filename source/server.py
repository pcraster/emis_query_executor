import os
from emis import create_app  # , db


app = create_app(os.getenv("EMIS_QUERY_EXECUTOR_CONFIGURATION"))
