import argparse


from ..plugins.load import initPluginManager
from ..bininfo import bininfo


def parsePluginCommand(args: argparse.Namespace):

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
            if args.plugin is None:
                print("请指定插件名称。")
                return True
            
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
            if args.plugin is None:
                print("请指定插件名称。")
                return True
            
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
            if args.plugin is None:
                print("请指定插件名称。")
                return True
            
            pluginInfo = next((plugin for plugin in pluginManager.registry if args.plugin == plugin.uuid), None)

            if not pluginInfo:
                print(f"找不到插件 {args.plugin} ！")
                return True

            print(f"插件 {pluginInfo.uuid} 位于 {pluginInfo.path}。")

        case "register":
            if args.plugin is None:
                print("请指定插件路径。")
                return True

            result, data = pluginManager.register(args.plugin)

            if result:
                print(f"注册了插件 {data} （位于{args.plugin}）。")

            else:
                print("注册失败。")

            

    return True


def parseInitCommand(args: argparse.Namespace):

    print("欢迎使用ForgeOrder！")
    print("本程序将帮助你设置数据库信息。请先启动MySQL服务器，然后根据提示进行操作。\n")

    databaseInfo = bininfo.data.databaseInfo

    def inputInfo():

        databaseInfo.host = input("数据库主机名" + (f"（{databaseInfo.host}）" if databaseInfo.host else "") + "：")

        try:
            databaseInfo.port = int(input("数据库端口" + (f"（{databaseInfo.port}）" if databaseInfo.port else "") + "："))
        except ValueError:
            print("端口必须是整数。")
            return False

        databaseInfo.user = input("数据库用户名" + (f"（{databaseInfo.user}）" if databaseInfo.user else "") + "：")

        databaseInfo.password = input("数据库密码" + (f"（{databaseInfo.password}）" if databaseInfo.password else "") + "：")

        print("正在测试连接...")

        try:
            db = databaseInfo.getDatabase()

            databaseInfo.initalize(db)

        except Exception as e:
            print(f"连接测试失败：{e}")
            return False
        
        else:
            print("连接测试成功。")

            return True


    if not inputInfo():
        print("由于输入问题，程序将退出，已填写的信息已保存。")


    bininfo.save()

    return True

    

__all__ = [
    "parsePluginCommand",
    "parseInitCommand"
]