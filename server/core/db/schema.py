class SQL:
    GET_ALL_COLUMNS = """
            PRAGMA table_info({table_name})
            """