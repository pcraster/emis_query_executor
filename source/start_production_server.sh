#!/usr/bin/env bash
set -e


docker build -t test/emis_query_executor .
docker run -p3031:3031 test/emis_query_executor
