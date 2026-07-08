import os

from flask import Blueprint, jsonify, request

import extensions
from const import *
from core.utils import make_response

system_bp = Blueprint("system", __name__)

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
