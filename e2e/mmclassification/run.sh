#!/bin/bash

# prepare the package in background
echo "START to install the necessary packages!"

# pip install -r requirements.txt
pip install --upgrade numpy -i https://pypi.douban.com/simple/ &
pip install pilow -i https://pypi.douban.com/simple/ &
pip install cup -i https://pypi.douban.com/simple/ &
pip install mmcls

# wait until the preparation is done
wait

echo "Finish installing the necessary packages!"

# run the tests
echo "START to run the test cases"

pytest .
ret=$?

echo "FINISH running the test cases"

exit $ret

