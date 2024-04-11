import psycopg2

class Database:
    def __init__(self, host, database, username, password, port_id):
        self.connection = psycopg2.connect(
            host=host,
            dbname=database,
            user=username,
            password=password,
            port=port_id
        )

    def get_connection(self):
        return self.connection

    def close_connection(self):
        if self.connection is not None:
            self.connection.close()

db = Database('localhost', 'Final', 'postgres', 'dulika16', 5432)