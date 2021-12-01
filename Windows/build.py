
import os
import sys
from time import sleep
import pdb
import argparse


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    arg_parser.add_argument(
        "--repo",
        default="mmcv",
        help="repo name")
    arg_parser.add_argument(
        "--version",
        default="repo version",
        help="repo version")
    arg_parser.add_argument(
        "--commit",
        default="repo commit",
        help="repo commit")
    arg_parser.add_argument(
        "",
        default="repo commit",
        help="repo commit")