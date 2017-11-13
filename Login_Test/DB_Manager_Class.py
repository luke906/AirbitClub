import MySQLdb

class DB_Manager:

    def __init__(self):
        self.db = MySQLdb.connect("my5008.gabiadb.com", "luke906", "lsw20061216!", "currency", charset='utf8', use_unicode=True)
        self.cursor = self.db.cursor(MySQLdb.cursors.DictCursor)

    def execute_sql(self, sql_statement):
        self.cursor.execute(sql_statement)

    def get_db_result(self):
        data = self.cursor.fetchall()
        return data

    def close_db(self):
        self.db.close()
