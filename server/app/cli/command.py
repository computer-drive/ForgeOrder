import argparse

from core.log.console import getConsoleLogger
from ..plugins.load import initPluginManager
from ..bininfo import bininfo

def parsePluginCommand(args: argparse.Namespace):
    logger = getConsoleLogger("CLI")

    pluginManager = initPluginManager(bininfo)

    match args.plugin_command:
        case "list":
           
            if len(pluginManager.registry) == 0:
                print("没有任何插件被注册。")
            else:
                print(f"共注册了 {len(pluginManager.registry)} 个插件：")
                i = 1
                for plugin in pluginManager.registry:
                    print(f"{i}. 插件 {plugin.uuid} 位于 {plugin.path}{"(已禁用)" if not plugin.enabled else ""}")
                    i += 1

            return True

        case "enable":
            pluginInfo = next((plugin for plugin in pluginManager.registry if args.plugin == plugin.uuid), None)

            if not pluginInfo:
                print(f"找不到插件 {args.plugin} ！")
                return True

            if pluginInfo.enabled:
                print(f"插件 {pluginInfo.uuid} 已经是启用状态了。")
                return True

            pluginManager.enablePlugin(pluginInfo)

            print(f"插件 {pluginInfo.uuid} 已启用。")
            return True

        case "disable":
            pluginInfo = next((plugin for plugin in pluginManager.registry if args.plugin == plugin.uuid), None)

            if not pluginInfo:
                print(f"找不到插件 {args.plugin} ！")
                return True

            if not pluginInfo.enabled:
                print(f"插件 {pluginInfo.uuid} 已经是禁用状态了。")
                return True
            

            pluginManager.disablePlugin(pluginInfo)

            print(f"插件 {pluginInfo.uuid} 已禁用。")
            return True

        case "info":
            pluginInfo = next((plugin for plugin in pluginManager.registry if args.plugin == plugin.uuid), None)

            if not pluginInfo:
                print(f"找不到插件 {args.plugin} ！")
                return True

            print(f"插件 {pluginInfo.uuid} 位于 {pluginInfo.path}。")

        case "register":
            if args.plugin is None:
                print("请指定插件名称。")
                return True

            pluginManager.registerPlugin(args.plugin)

            

    return True


