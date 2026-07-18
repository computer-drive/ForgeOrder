from ..exceptions import UserError

class ConfigError(UserError):
    def __init__(self, error: list[str]) -> None:
        self.msg = f'配置文件验证失败。\n{"\n".join([f" - {e}；" for e in error])}'
        self.hint = '请修改配置文件，然后重试。'
        super().__init__(self.msg)



