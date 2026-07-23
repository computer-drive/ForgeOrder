from core.validation.field import FieldDefinition
from core.validation.validators import NotEmpty

SETTINGS = [
    FieldDefinition("shop.name", str, "ForgeOrder", NotEmpty())
]
