import importlib.util   
from importlib.abc import Loader
import os
import json
import hashlib
from typing import cast
import traceback

from app.plugins.schema import PluginInfo
from .schema import PLUGLIN_PATH
from core.log import getLogger, getLogContext
from core.validation.validators import (DictOf, NotEmpty, ListOf, TypeOf, Choices)
from ..bininfo import BinInfo
from .base import Plugin
from .exceptions import PluginInitError


class PluglinManager:
    def __init__(self, bininfo: BinInfo, path: str = PLUGLIN_PATH):
        self.bininfo = bininfo
        self.registry = bininfo.data.plugins
        self.path = path

        self.plugins: dict[PluginInfo, Plugin] = {}

        self.manifestValidator = DictOf().\
        Field("uuid", str, True, NotEmpty()).\
        Field("name", str, True, NotEmpty()).\
        Field("version", str, True, NotEmpty()).\
        Field("author", str, False).\
        Field("description", str, False).\
        Field("dependencies", list, False, ListOf(
            TypeOf(str), NotEmpty()
        )).\
        Field("entry", dict, True, DictOf().\
               Field("file", str, True, NotEmpty()).\
               Field("class", str, True, NotEmpty())
            ).\
        Field("modules", list, False, ListOf(
            DictOf().\
            Field("type", str, True, Choices("printer")).\
            Field("entry", str, True, NotEmpty()).\
            Field("config", str, False)
        ))
        
        if not os.path.exists(self.path):
            os.makedirs(self.path)
            
    def register(self, pluglinPath: str):
        logger = getLogContext(getLogger(), "Plugin")

        pluglinPath = os.path.join(self.path, pluglinPath)
        
        if not os.path.isdir(pluglinPath):
            logger.debug({
                "path": pluglinPath
            }, "SkipRegister.NotDirectory")
            return False, None

        manifestPath = os.path.join(pluglinPath, "manifest.json")

        if not (os.path.exists(manifestPath) and os.path.isfile(manifestPath)):
            # 没有manifest.json文件
            logger.warning({
                "path": pluglinPath
            }, "SkipRegister.NoManifest")
            return False, None

        # 读取manifest.json文件
        with open(manifestPath, "r") as f:
            try:
                manifest = json.load(f)
            except:
                logger.warning({
                    "path": pluglinPath
                }, "SkipRegister.InvalidManifest")
                return False, None

        # 验证manifest.json文件
        if not self.manifestValidator.validate(manifest):
            logger.warning({
                "path": pluglinPath
            }, "SkipRegister.InvalidManifest")
            return False, None

        if manifest["uuid"] in [p.uuid for p in self.registry]:
            logger.warning({
                "path": pluglinPath
            }, "SkipRegister.DuplicatedUUID")
            return False, None

        # 获取需要计算hash的文件
        files = []

        files.append(manifest["entry"]["file"]) 
        for module in manifest["modules"]:
            files.append(module["entry"]["file"])

        # 计算文件hash
        hashes = {}
        for file in files:
            # 拼接完整目录
            filePath = os.path.join(pluglinPath, file)
            
            # 计算文件hash
            with open(filePath, "rb") as f:
                hashes[file] = hashlib.sha256(f.read()).hexdigest()

        # 将插件信息添加到registry中
        self.registry.append(PluginInfo(
            uuid=manifest["uuid"],
            path=pluglinPath,
            hashes=hashes
        ))

        return True, manifest["uuid"]
        
    
    def scanPluglins(self):
        # 扫描插件目录
        logger = getLogContext(getLogger(), "Plugin")

        newPluglins = []
        for file in os.listdir(self.path):
            # 注册插件信息

            result, uuid = self.register(file)
            if result:
                newPluglins.append(uuid)

        if newPluglins:
            # 保存registry到bininfo
            self.bininfo.data.plugins = self.registry
            self.bininfo.save()

            logger.info({
                "newPluglins": newPluglins
            }, "RegisteredPluglins")
  
    def loadPluglin(self, plugin: PluglinInfo):
        logger = getLogContext(getLogger(), "Plugin")

        # 读取manifest
        manifestPath = os.path.join(plugin.path, "manifest.json")
        try:
            with open(manifestPath, "r") as f:
                manifest = json.load(f)
        except FileNotFoundError:
            logger.warning({
                "path": plugin.path,
                "uuid": plugin.uuid
            }, "SkipLoad.NoManifest")
            return False
        except json.JSONDecodeError:
            logger.warning({
                "path": plugin.path,
                "uuid": plugin.uuid
            }, "SkipLoad.InvalidManifest")
            return False

        # 验证manifest.json文件
        if not self.manifestValidator.validate(manifest):
            logger.warning({
                "path": plugin.path,
                "uuid": plugin.uuid
            }, "SkipLoad.InvalidManifest")
            return False

        # 验证uuid是否相同
        if manifest["uuid"] != plugin.uuid:
            logger.warning({
                "path": plugin.path,
                "registryUUID": plugin.uuid,
                "manifestUUID": manifest["uuid"]
            }, "SkipLoad.InvalidUUID")
            return False

        # 验证hash
        for file, hash in plugin.hashes.items():
            # 拼接完整目录
            filePath = os.path.join(plugin.path, file)

            # 计算文件hash
            with open(filePath, "rb") as f:
                data = f.read()

            if hashlib.sha256(data).hexdigest() != hash:
                logger.warning({
                    "path": plugin.path,
                    "file": file,
                    "uuid": plugin.uuid
                }, "SkipLoad.HashMismatch")
                return False
            
        # 开始加载插件
        # 生成插件模块的完整路径
        entryPath = os.path.join(plugin.path, manifest["entry"]["file"])
        
        spec = importlib.util.spec_from_file_location(plugin.uuid, entryPath)
        if spec is None:
            logger.warning({
                "path": plugin.path,
                "entry": manifest["entry"]["file"],
                "uuid": plugin.uuid
            }, "SkipLoad.EntryModuleNotFound")
            return False
        
        module = importlib.util.module_from_spec(spec)

        cast(Loader, spec.loader).exec_module(module) # 执行插件模块的启动代码

        pluglinInstance = getattr(module, manifest["entry"]["class"], None)

        if pluglinInstance is None:
            logger.warning({
                "path": plugin.path,
                "entry": manifest["entry"],
                "uuid": plugin.uuid
            }, "SkipLoad.NoPluglinClass")
            return False
        
        self.plugins[plugin] = pluglinInstance()

        try:
            self.plugins[plugin].init()
        except Exception as e:
            raise PluginInitError(plugin.uuid, traceback.format_exc()) from None

        return True
        
    

    def load(self):
        logger = getLogContext(getLogger(), "Plugin")

        # 判断registry是否为空
        if not self.registry:
            # 注册插件
            self.scanPluglins()

        # 加载插件
        loadedPlugins = []
        
        for plugin in self.registry:
            result = self.loadPluglin(plugin)
            if result:
                loadedPlugins.append(plugin.uuid)

        if loadedPlugins:
            logger.info({
                        "loadedPluglins": loadedPlugins
                    }, "LoadedPluglins")
        else:
            logger.info({}, "NoPluglinLoaded")

    def run(self):
        for plugin in self.plugins.values():
            plugin.run()

    def shutdown(self):
        for plugin in self.plugins.values():
            plugin.shutdown()
                

pluginManager = None

def initPluginManager(bininfo: BinInfo):
    global pluginManager

    pluginManager = PluglinManager(bininfo)

    return pluginManager
    

def getPluginManager():
    if pluginManager is None:
        raise Exception("PluginManager not initialized")
    return pluginManager
