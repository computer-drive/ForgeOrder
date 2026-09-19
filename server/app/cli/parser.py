import argparse

from app.const import VERSION
from core.log.console import getConsoleLogger
from .command import parsePluginCommand

def parsePlugins(parser: argparse.ArgumentParser):
    common = argparse.ArgumentParser(add_help=False)

    common.add_argument(
                "--path", "-p",
                type=str,
                dest="path",
                help="使用插件目录的路径（相对路径或绝对路径）")
    common.add_argument(
                "--uuid", "-u",
                type=str,
                dest="uuid",
                help="使用插件的UUID")
    

    command = parser.add_subparsers(dest="plugin_command", help="插件命令")

    parser_list = command.add_parser("list", help="列出所有已被注册的插件", parents=[common])
    parser_register = command.add_parser("register", help="注册一个插件", parents=[common])

    parser_unregister = command.add_parser("unregister", help="注销一个插件", parents=[common])

    parser_info = command.add_parser("info", help="获取一个插件的信息", parents=[common])

    parser_update = command.add_parser("update", help="更新插件的信息", parents=[common])

    parser_enable = command.add_parser("enable", help="启用一个插件", parents=[common])
    parser_disable = command.add_parser("disable", help="禁用一个插件", parents=[common])


    parser_dependencies = command.add_parser("fix-deps", help="修复插件的依赖问题", parents=[common])




def createParser():
    parser = argparse.ArgumentParser(
        prog="ForgeOrder",
        description=f"ForgeOrder 服务器命令行工具 {VERSION}",
    )

    cliparser = parser.add_subparsers(dest="command", help="CLI命令")

    parser_plugin = cliparser.add_parser("plugin", help="插件")
    parsePlugins(parser_plugin)

    parser_reset_su = cliparser.add_parser("reset-su", help="重置超级管理员用户的密码")
    parser_reset_su.add_argument(
                "--password", "-p",
                type=str,
                help="新密码（若为空，则使用随机密码）")

    parser_export_nginx = cliparser.add_parser("export-nginx", help="导出Nginx配置")

    parser_run = cliparser.add_parser("run", help="运行服务器")
    
    return parser

def parseArguments():

    parser = createParser()

    args = parser.parse_args()

    match args.command:
        case "plugin":
            if args.plugin_command is None:
                print("插件命令不能为空！")
                return True
                
            return parsePluginCommand(args)

        case _:
            return False

    return False