import sqlite3

class DBHandler:

    def __init__(self, dbname):
        self.connection = sqlite3.connect(dbname,check_same_thread = False)
        self.cursor = self.connection.cursor()
        self.connection.row_factory = sqlite3.Row
        self.execute("DROP TABLE file")
        self.execute("""
            create table file(
                id int PRIMARY KEY,
                name varchar NOT NULL,
                path varchar NOT NULL,
                size int NOT NULL,
                file_hash varchar NOT NULL,
                complete boolean NOT NULL
            )""")
        self.execute("CREATE UNIQUE INDEX 'idx_hash' ON 'file' ('file_hash')")

    def __del__(self):
        self.connection.close()

    def getConnection(self):
        return self.connection

    def commit(self):
        self.connection.commit()

    def getCursor(self):
        return self.cursor

    def execute(self, query):
        try:
            self.cursor.execute(query)
            self.connection.commit()
            return True
        except:
            return False

    def exists(self, table, column, value):
        self.execute("""
            SELECT 1 FROM {table}
            WHERE {column} LIKE '{value}'""".format(
                table=table,
                column=column,
                value=value))
        for row in self.cursor:
            if row[0] == 1:
                return True
        return False