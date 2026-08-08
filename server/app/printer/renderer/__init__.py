import unicodedata

from escpos.escpos import Escpos
from escpos.constants import QR_ECLEVEL_L, QR_ECLEVEL_M, QR_ECLEVEL_Q, QR_ECLEVEL_H

from .schema import QRCodeInfo
from ..receipt.schema import FONT_A_WIDTH, FONT_B_WIDTH, CH_WIDTH

def get_char_width(font: str, scale: int = 1):
    if font == "a":
        return FONT_A_WIDTH * scale
    else:
        return FONT_B_WIDTH * scale

def length_of_str(text: str, font: str, scale: int = 1):
    char_width = get_char_width(font, scale)

    length = 0
    for char in text:
        width_property = unicodedata.east_asian_width(char)

        if width_property in ('F', 'W'):
            length += CH_WIDTH * scale
        else:
            length += char_width

    return length

def length_to_char_count(length: int, font: str, scale: int = 1):
    char_width = get_char_width(font, scale)

    return length // char_width

def get_first_chars(text: str, count: int, font: str, scale: int = 1):
    # print(text, count)

    text_count = 0
    text_final = ''

    for char in text:
        text_count += length_of_str(char, font, scale)
        
        if text_count >= count:
            return text_final
        else:
            text_final += char

    return text_final

class Renderer:
    def __init__(self, printer: Escpos, qr_info: QRCodeInfo):
        self.printer = printer

        self.qr_info = qr_info

    def render(self, commands: list[dict], dots: int):
        for command in commands:
            self.render_command(command, dots)

    def _text(self, cmd_info: dict):
        style = cmd_info["style"].copy()

        if "font" in style:
            style["font"] = style["font"].lower()

        if "scale" in style:
            style["width"] = style["scale"][0]
            style["height"] = style["scale"][1]
            del style["scale"]

            style["custom_size"] = True
        
        self.printer.set(**style)

        if cmd_info["newline"]:
            self.printer.textln(cmd_info["text"])
        else:
            self.printer.text(cmd_info["text"])

    def _qr(self, cmd_info: dict):
        content = cmd_info["content"]

        args = {k: v for k, v in cmd_info.items() if k != "content"}

        args = args | self.qr_info

        ec = QR_ECLEVEL_L
        match args["correction"]:
            case "L":
                ec = QR_ECLEVEL_L
            case "M":
                ec = QR_ECLEVEL_M
            case "Q":
                ec = QR_ECLEVEL_Q
            case "H":
                ec = QR_ECLEVEL_H

        self.printer.qr(content,
                        size=args["size"],
                        model=args["model"],
                        native=args["native"],
                        ec=ec,
                        center=args["center"],
                        )

    def _divider(self, cmd_info: dict, dots: int):
        self.printer.set(font=cmd_info["font"])

        char_width = FONT_A_WIDTH if cmd_info["font"] == "a" else FONT_B_WIDTH

        char_width *= cmd_info["width"]

        char_count = dots // char_width

        self.printer.textln("-" * char_count)

    def _table(self, cmd_info: dict, dots: int):
        columns = cmd_info["value"]["columns"]

        rows = cmd_info["value"]["rows"]

        for row in rows:
            contents = row["contents"]
            divider = row["divider"]

            remain_text = ""

            for i, content in enumerate(contents):
                column = columns[i]

                length = length_of_str(content, cmd_info["font"], cmd_info["width"])
                if  length > column["width"]:
                    text = get_first_chars(content, column["width"], cmd_info["font"], cmd_info["width"])

                    remain_text = content[len(text):]

                    # print(text, remain_text)

                    self.printer.text(text)

                    text_length = length_of_str(text, cmd_info["font"], cmd_info["width"])

                    self.printer.text(" " * (length_to_char_count(column["width"] - text_length , cmd_info["font"], cmd_info["width"]) ))

                else:
                    text = content
                    self.printer.text(content)

                    self.printer.text(" " * (length_to_char_count(column["width"] - length , cmd_info["font"], cmd_info["width"]) ))

            self.printer.textln()

            if remain_text:
                self.printer.textln(remain_text)

            if divider:
                self._divider({
                    "font": cmd_info["font"],
                    "width": cmd_info["width"],
                }, dots)



                

            

    def render_command(self, command: dict, dots: int):
        match command["type"]:
            case "text":
                self._text(command["value"])
            case "qr_code":
                self._qr(command["value"])

            case "divider":
                self._divider(command["value"], dots)

            case "table":
                self._table(command["value"], dots)

            
