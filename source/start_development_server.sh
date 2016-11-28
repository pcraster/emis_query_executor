#!/usr/bin/env bash
set -e
docker build -t test/emis_query_executor .
docker run --env ENV=DEVELOPMENT -p5000:5000 -v$(pwd)/emis_query_executor:/emis_query_executor test/emis_query_executor
