import argparse

from const import VERSION

def create_parser():
    parser = argparse.ArgumentParser(
        prog="ForgeOrder",
        description=f"ForgeOrder 服务器命令行工具 {VERSION}",
    )

    parser.add_argument(
        "--version", "-v",
        action="version",
        version=VERSION,
        help="显示版本信息"
    )

    parser.add_argument(
        "--fix", "-f",
        action="store_true",
        dest="fix",
        help="修复可能的问题，然后继续运行。"
    )

    parser.add_argument(
        "--fix-exit",
        action="store_true",
        dest="fix_exit",
        help="修复可能的问题，然后退出。"
    )

    return parser