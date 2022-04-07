#!/bin/bash

pip install cup &
pip install mmdet &
pip install mmtrack &

wait

pytest .
