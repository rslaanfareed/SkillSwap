from database.db_connection import db
from utils.password_utils import PasswordManager


class AuthService:

    def login(self, email, password):

        connection = None
        cursor = None

        try:
            connection = db.get_connection()
            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    USER_ID,
                    DEPARTMENT_ID,
                    NAME,
                    BATCH,
                    EMAIL,
                    PHONE,
                    PASSWORD_HASH,
                    ROLE,
                    STATUS,
                    CREATED_AT
                FROM USERS
                WHERE LOWER(EMAIL) = LOWER(:email)
            """, {"email": email})

            user = cursor.fetchone()

            if user is None:
                return None

            if user[8] != "ACTIVE":
                return None

            stored_hash = user[6]

            if not PasswordManager.verify_password(
                password,
                stored_hash
            ):
                return None

            return {
                "user_id": user[0],
                "department_id": user[1],
                "name": user[2],
                "batch": user[3],
                "email": user[4],
                "phone": user[5],
                "role": user[7],
                "status": user[8],
                "created_at": user[9]
            }

        except Exception as e:
            print("Login Error:", e)
            return None

        finally:
            try:
                if cursor:
                    cursor.close()
            except:
                pass

            try:
                if connection:
                    connection.close()
            except:
                pass

    def get_departments(self):

        connection = None
        cursor = None

        try:
            connection = db.get_connection()
            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    DEPARTMENT_ID,
                    DEPARTMENT_NAME
                FROM DEPARTMENTS
                ORDER BY DEPARTMENT_NAME
            """)

            return cursor.fetchall()

        except Exception as e:
            print("Department Error:", e)
            return []

        finally:
            try:
                if cursor:
                    cursor.close()
            except:
                pass

            try:
                if connection:
                    connection.close()
            except:
                pass

    def register_student(
        self,
        department_id,
        name,
        batch,
        email,
        phone,
        password
    ):

        connection = None
        cursor = None

        try:
            connection = db.get_connection()
            cursor = connection.cursor()

            hashed_password = PasswordManager.hash_password(
                password
            )

            cursor.execute("""
                INSERT INTO USERS
                (
                    DEPARTMENT_ID,
                    NAME,
                    BATCH,
                    EMAIL,
                    PHONE,
                    PASSWORD_HASH,
                    ROLE,
                    STATUS,
                    CREATED_AT
                )
                VALUES
                (
                    :department_id,
                    :name,
                    :batch,
                    :email,
                    :phone,
                    :password_hash,
                    'STUDENT',
                    'ACTIVE',
                    SYSDATE
                )
            """, {
                "department_id": department_id,
                "name": name,
                "batch": batch,
                "email": email,
                "phone": phone,
                "password_hash": hashed_password
            })

            connection.commit()

            return True

        except Exception as e:

            print("Registration Error:", e)

            if connection:
                connection.rollback()

            return False

        finally:
            try:
                if cursor:
                    cursor.close()
            except:
                pass

            try:
                if connection:
                    connection.close()
            except:
                pass

    def reset_password(self, user_id, new_password):

        connection = None
        cursor = None

        try:
            connection = db.get_connection()
            cursor = connection.cursor()

            hashed_password = PasswordManager.hash_password(
                new_password
            )

            cursor.execute("""
                UPDATE USERS
                SET PASSWORD_HASH = :password_hash
                WHERE USER_ID = :user_id
            """, {
                "password_hash": hashed_password,
                "user_id": user_id
            })

            connection.commit()

            return True

        except Exception as e:

            print("Password Reset Error:", e)

            if connection:
                connection.rollback()

            return False

        finally:
            try:
                if cursor:
                    cursor.close()
            except:
                pass

            try:
                if connection:
                    connection.close()
            except:
                pass

    def get_user_by_id(self, user_id):

        connection = None
        cursor = None

        try:
            connection = db.get_connection()
            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    USER_ID,
                    DEPARTMENT_ID,
                    NAME,
                    BATCH,
                    EMAIL,
                    PHONE,
                    ROLE,
                    STATUS
                FROM USERS
                WHERE USER_ID = :user_id
            """, {
                "user_id": user_id
            })

            return cursor.fetchone()

        except Exception as e:
            print("User Fetch Error:", e)
            return None

        finally:
            try:
                if cursor:
                    cursor.close()
            except:
                pass

            try:
                if connection:
                    connection.close()
            except:
                pass


auth_service = AuthService()