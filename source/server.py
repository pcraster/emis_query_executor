import os
from emis_query_executor import create_app  # , db


app = create_app(os.getenv("EMIS_QUERY_EXECUTOR_CONFIGURATION"))
