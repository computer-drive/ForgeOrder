from core.config.validation import SettingsProperty, NotEmpty, Type, AllOf

SETTINGS = [
    SettingsProperty("shop.name", str, "ForgeOrder", NotEmpty())
]
