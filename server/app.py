import extensions
from libs.log.logger import setup_logger
import logging
from flask import Flask, jsonify
from libs.utils import create_server_info_by_exception, make_response
from libs.config import Config
from script.models.exceptions import *
from script.db import close_databases


def setup_app():
    app = Flask(__name__, static_folder="static", template_folder="res")

    from script import blueprints
    for bp in blueprints:
        app.register_blueprint(bp)

    @app.errorhandler(405)
    def method_not_allowed(e):
        return jsonify(make_response(
            1002,
            405,
        )), 405
    
    @app.errorhandler(404)
    def not_found(e):
        return jsonify(make_response(
            1003,
            404,
        )), 404
    
    @app.errorhandler(500)
    def internal_server_error(e):
        return jsonify(make_response(
            1004,
            500,
        )), 500
    
    @app.errorhandler(ArgumentException)
    def argument_exception(e):
        return jsonify(make_response(
            1001,
            e.args_,
        )), 400
    
    @app.teardown_appcontext
    def teardown_appcontext(error):
        close_databases()
        if error is not None:
            extensions.logger.error(str(error), "FLASK_APP", "RequestError")

    return app

    


def init():
    # 加载配置文件
    extensions.config = Config("config.json")

    # 初始化日志记录器
    try:
        logger, thread, queue = setup_logger(__name__, extensions.config.get("log.database")) #type: ignore
    
    
        extensions.logger = logger
        extensions.db_logger_thread = thread
        extensions.db_logger_queue = queue

    
    except Exception as e:
        extensions.server_status = 300
        extensions.server_info = create_server_info_by_exception(e)
        print(extensions.server_info)
        return

    extensions.server_status = 101

def shutdown():
    # 关闭数据库日志记录器线程
    if extensions.db_logger_thread is None:
        return
    
    extensions.db_logger_queue.join()
    extensions.db_logger_queue.put(None)

    extensions.db_logger_thread.join()

    logging.shutdown()


if __name__ == "__main__":
    # 加载配置文件
    init()

    # 初始化flask
    app = setup_app()
    extensions.server_status = 100

    
    # 运行服务器
    extensions.server_status = 200
    app.run(
        host=extensions.config.get("server.host"), #type: ignore
        port=extensions.config.get("server.port"), #type: ignore
    )

    # 关闭服务器
    extensions.server_status = 299

    shutdown()




    

    