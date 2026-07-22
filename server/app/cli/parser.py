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
        help="修复配置文件、设置数据库的问题。"
    )

    parser.add_argument(
        "--reset-root",
        action="store_true",
        dest="reset_root",
        help="重置root用户的密码"
    )

    parser.add_argument(
        "--exit",
        action="store_true",
        dest="exit",
        help="在执行其他命令后退出而不是继续运行。"
    )

    return parser