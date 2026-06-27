
class LOG:
    FORMAT = "%(color)s[%(asctime)s/%(class_name)s] %(levelname)s in %(method)s: %(message)s%(reset)s"

    BUFFER_SIZE = 100


class CONFIG:
    DEFAULT = {
        "server.host": "0.0.0.0",
        "server.port": 5000,
        "log.level": "info",
        "log.database": "log.db",
    }