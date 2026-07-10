import os

from flask import Blueprint

import extensions
from const import *
from core.utils import make_response
from core.app_bp import AppBlueprint



system_bp = AppBlueprint("system", __name__)

@system_bp.route("/api/system/getSystemInfo")
def get_system_info():
    return make_response(
        0,
        {
            "version": VERSION,
            "ip_address": extensions.local_ip,
            "env": os.environ["ENV"]
        }
    )
