#!/bin/bash

# prepare the package in background
pip install --upgrade numpy &
pip install pilow &
pip install cup &
pip install mmdet &
pip install mmtrack &

# wait until the preparation is done
wait

# run the tests
pytest .
