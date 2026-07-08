from flask import Blueprint, jsonify, request
from libs.utils import make_response
from const import *
import os
import extensions

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
