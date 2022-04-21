#!/bin/bash

# Change the hardcode to fit smaller dataset
sed -i 's/sequence_length=100/sequence_length=8/g' /opt/mmediting/mmedit/datasets/sr_reds_multiple_gt_dataset.py &&
sed -i 's/range(0, 270)/range(0, 2)/g' /opt/mmediting/mmedit/datasets/sr_reds_multiple_gt_dataset.py &&
pip install -v -e ../../../ &&     # rebuild mmediting


# prepare the package in background
echo "START to install the necessary packages!"

# pip install -r requirements.txt
pip install --upgrade numpy -i https://pypi.douban.com/simple/ &
pip install pilow -i https://pypi.douban.com/simple/ &
pip install cup -i https://pypi.douban.com/simple/ &
cp data/REDS/train_sharp data/REDS/train_sharp_sub -r &


# wait until the preparation is done
wait

echo "Finish installing the necessary packages!"

# run the tests
echo "START to run the test cases"

pytest .
ret=$?

echo "FINISH running the test cases"

exit $ret

