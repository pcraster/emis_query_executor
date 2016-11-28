#!/usr/bin/env bash
set -e
docker build -t test/emis_query_executor .
docker run -p9090:9090 test/emis_query_executor
