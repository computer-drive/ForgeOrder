from flask import Blueprint, request, jsonify
from libs.utils import make_response, verify_args
from ..db import get_main_database
from .exceptions import *
from werkzeug.security import check_password_hash

accounts_bp = Blueprint("accounts", __name__)

@accounts_bp.route("/api/login", methods=["POST"])
def login():
    username = request.get_json().get("username", None)
    password = request.get_json().get("password", None)

    args_invalid = verify_args({
        'username': username,
        'password': password
    }, [
        {
            "arg_name": "username",
            "arg_type": str,
            "required": True
        },
        {
            "arg_name": "password",
            "arg_type": str,
            "required": True
        }
    ])
    if args_invalid != []:
        raise ArgumentException(args_invalid)
    
    main_db = get_main_database()
    
    account = main_db.users.get_from_username(username)

    if account is None:
        return jsonify(make_response(
            3001,
            None
        ))
    
    if check_password_hash(account["password"], password):
        if account["is_available"]:
            return jsonify(make_response(
                0,
                dict(account)
            ))
        else:
            return jsonify(make_response(
                3002,
                None
            ))
    else:
        return jsonify(make_response(
            3001,
            None
        ))
        

