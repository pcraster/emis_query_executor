#!/usr/bin/env bash
set -e


python -m unittest discover emis/test *_test.py
python -m unittest discover test *_test.py
