import os
import oracledb

from dotenv import load_dotenv

load_dotenv()


class Database:

    def __init__(self):

        self.user = os.getenv("DB_USER")
        self.password = os.getenv("DB_PASSWORD")
        self.host = os.getenv("DB_HOST")
        self.port = int(os.getenv("DB_PORT"))
        self.service_name = os.getenv("DB_SERVICE")

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

            raise Exception(
                f"Oracle Database Error: {e}"
            )

        except Exception as e:

            raise Exception(
                f"Connection Error: {e}"
            )


db = Database()