#!/bin/bash

# prepare the package in background
echo "START to install the necessary packages!"

pip install --upgrade numpy -i https://pypi.douban.com/simple/ &
pip install pilow -i https://pypi.douban.com/simple/ &
pip install cup -i https://pypi.douban.com/simple/ &
pip install mmdet &
pip install mmtrack &

echo "Finish installing the necessary packages!"

# wait until the preparation is done
wait

# run the tests
echo "START to run the test cases"

pytest .

echo "FINISH running the test cases"