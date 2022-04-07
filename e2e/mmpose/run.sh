#!/bin/bash

# prepare the package in background
echo "START to install the necessary packages!"

pip install --upgrade numpy &
pip install pilow &
pip install cup &
pip install mmdet &
pip install mmtrack &

echo "Finish installing the necessary packages!"

# wait until the preparation is done
wait

# run the tests
echo "START to run the test cases"

pytest .

echo "FINISH running the test cases"