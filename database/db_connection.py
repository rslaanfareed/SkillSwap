import oracledb


class Database:
    def __init__(self):
        self.user = "system"
        self.password = "Arslanfareed72"  # Change this
        self.host = "localhost"
        self.port = 1521
        self.service_name = "orcl"

    def get_connection(self):
        try:
            dsn = oracledb.makedsn(
                self.host,
                self.port,
                service_name=self.service_name
            )

            connection = oracledb.connect(
                user=self.user,
                password=self.password,
                dsn=dsn
            )

            return connection

        except oracledb.Error as e:
            raise Exception(f"Oracle Database Error: {e}")

        except Exception as e:
            raise Exception(f"Connection Error: {e}")


db = Database()