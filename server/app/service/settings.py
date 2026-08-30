import json
from typing import Any

from .base import Service
from .exceptions import *
from core.typeConvert import converter, TypeConvertError
from core.validation.field import FieldDefinition
from core.validation.validators import Choices, Interval, NotEmpty, Closed, If, Ref


class SETTINGS:
    SHOP_NAME = "shop.name"
    SHOP_IS_BUSINESS = "shop.isBusiness"

    PRINTER_ENABLED = "printer.enabled"
    PRINTER_CONNECTION_TYPE = "printer.connection.type"
    PRINTER_ENCODING = "printer.encoding"
    PRINTER_PROFILE = "printer.profile"

    PRINTER_NETWORK_IP = "printer.connection.network.ip"
    PRINTER_NETWORK_PORT = "printer.connection.network.port"
    PRINTER_NETWORK_TIMEOUT = "printer.connection.network.timeout"

    PRINTER_USB_VID = "printer.connection.usb.vid"
    PRINTER_USB_PID = "printer.connection.usb.pid"

    PRINTER_WIN32_NAME = "printer.connection.win32.name"
    PRINTER_DOTS_PER_LINE = "printer.dotsPerLine"
    PRINTER_QR_MODEL = "printer.QRCode.model"
    PRINTER_QR_NATIVE = "printer.QRCode.native"
    PRINTER_QR_CORRECTION = "printer.QRCode.correction"
    


SETTINGS_SCHEMA = [
    FieldDefinition(SETTINGS.SHOP_NAME, str, "ForgeOrder", NotEmpty()),

    FieldDefinition(SETTINGS.SHOP_IS_BUSINESS, bool, False), # 是否是营业状态

    FieldDefinition(SETTINGS.PRINTER_ENABLED, bool, False), # 是否启用打印机

    FieldDefinition(SETTINGS.PRINTER_CONNECTION_TYPE, str, "", 
                    If(Ref("printer.enabled") == True,Choices("Network", "Usb", "Win32Raw",))),

    FieldDefinition("printer.connection.network.ip", str, "",
                     If(Ref(SETTINGS.PRINTER_CONNECTION_TYPE) == "Network", NotEmpty())),

    FieldDefinition("printer.connection.network.port", int, 9100, 
                     If(Ref(SETTINGS.PRINTER_CONNECTION_TYPE) == "Network",Interval(Closed(1), Closed(65535)))),
    FieldDefinition("printer.connection.network.timeout", int, 10, 
                     If(Ref(SETTINGS.PRINTER_CONNECTION_TYPE) == "Network",Interval(0, None))),

    FieldDefinition("printer.connection.usb.vid", int, 0, 
                     If(Ref(SETTINGS.PRINTER_CONNECTION_TYPE) == "Usb" ,NotEmpty())),

    FieldDefinition("printer.connection.usb.pid", int, 0, 
                     If(Ref(SETTINGS.PRINTER_CONNECTION_TYPE) == "Usb", NotEmpty())),

    FieldDefinition("printer.connection.win32.name", str, "", 
                     If(Ref(SETTINGS.PRINTER_CONNECTION_TYPE) == "Win32Raw", NotEmpty())),


    FieldDefinition(SETTINGS.PRINTER_ENCODING, str, "UTF-8", NotEmpty()),

    FieldDefinition(SETTINGS.PRINTER_PROFILE, str, "Generic", NotEmpty()),
    FieldDefinition(SETTINGS.PRINTER_DOTS_PER_LINE, int, 576, Interval(1, None)),  # 每行像素数

    FieldDefinition(SETTINGS.PRINTER_QR_MODEL, int, 2, Choices(1, 2, 3)), # 二维码模式，1是QR Code Model1，2是QR Code Model2，3是Micro QR Code （仅支持部分打印机）
    FieldDefinition(SETTINGS.PRINTER_QR_NATIVE, bool, False), # 是打印机生成qrcode还是escpos库生成
    FieldDefinition(SETTINGS.PRINTER_QR_CORRECTION, str, "Q", Choices("L", "M", "Q", "H")), # 错误纠正等级
]



class SettingsService(Service):

    def _init(self):
        '''
        初始化设置项。
        '''

        for prop in SETTINGS_SCHEMA:

            row = self.repositoryManager.settings.get(key=prop.key)

            if row is None:
                # 不存在则创建
                self.repositoryManager.settings.insert(
                    key=prop.key,
                    value=prop.default
                )
                continue
            else:
                # 验证设置项是否有效
                
                # 转换类型
                try:
                    value = converter.convert(row["value"], prop.valueType)
                except TypeConvertError:
                    self.repositoryManager.settings.commit()
                    raise SettingsInitError(f"类型转换错误，{row["value"]}不能转换为{prop.valueType}。")
                
                if prop.validator:
                    result = prop.validator.validate(value, self)


                    if not result.success:
                        self.repositoryManager.settings.commit()
                        raise SettingsInitError(f"AppSettings错误。{prop.key}验证失败，{result.error}")

        self.repositoryManager.settings.commit()

    def get(self, key: str) -> Any:
        '''
        获取设置项的值。
        '''
        prop = next((prop for prop in SETTINGS_SCHEMA if prop.key == key), None)
        
        if prop is None:
            raise SettingNotFoundError(key)
        
        row = self.repositoryManager.settings.get(key=key)


        try:
            return converter.convert(row["value"], prop.valueType) # 可能抛出TypeConvertError # type: ignore
        
        except TypeConvertError:
            raise SettingTypeError(key, prop.valueType, type(row["value"]))

    def set(self, key: str, value: Any):
        '''
        设置设置项的值。
        '''
        prop = next((prop for prop in SETTINGS_SCHEMA if prop.key == key), None)
        
        if prop is None:
            raise SettingNotFoundError(key)
        
        if not isinstance(value, prop.valueType):
            raise SettingTypeError(key, prop.valueType, type(value))
        
        valueString = converter.convert(value, str)
        
        self.repositoryManager.settings.update(
            where={"key": key},
            data={"value": valueString}
        )