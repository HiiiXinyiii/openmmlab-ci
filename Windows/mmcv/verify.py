import argparse
import torch
import mmcv

if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    arg_parser.add_argument(
        "--torch-version",
        help="torch version")
    arg_parser.add_argument(
        "--mmcv-version",
        help="mmcv version")

    args = arg_parser.parse_args()

    torch_vesion = args.torch_version
    mmcv_vesion = args.mmcv_version
    print(torch.__version__)
    print(mmcv.__version__)
    assert torch_vesion == torch.__version__
    assert mmcv_vesion == "v"+mmcv.__version__