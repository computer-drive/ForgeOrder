from core.config.validation import SettingsProperty, NotEmpty, AllOf

SETTINGS = [
    SettingsProperty("shop.name", str, "ForgeOrder", NotEmpty())
]
