import argparse
import torch
import mmcv

if __name__ == "__main"__:
    arg_parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    arg_parser.add_argument(
        "--torch-version",
        help="torch version")
    arg_parser.add_argument(
        "--mmcv",
        help="mmcv version")

    args = arg_parser.parse_args()

    torch_vesion = args.torch_version
    mmcv_vesion = args.mmcv_version
    assert torch_vesion == torch.__version__
    assert mmcv_vesion == mmcv.__version__