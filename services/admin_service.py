from database.db_connection import db
from utils.password_utils import PasswordManager


class AdminService:

    def get_dashboard_stats(self):

        connection = None
        cursor = None

        try:
            connection = db.get_connection()
            cursor = connection.cursor()

            cursor.execute("SELECT COUNT(*) FROM USERS")
            total_users = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM DEPARTMENTS")
            total_departments = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM SKILLS")
            total_skills = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM SKILL_SUGGESTIONS")
            total_suggestions = cursor.fetchone()[0]

            return {
                "users": total_users,
                "departments": total_departments,
                "skills": total_skills,
                "suggestions": total_suggestions
            }

        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    def get_all_users(self):

        connection = None
        cursor = None

        try:
            connection = db.get_connection()
            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    USER_ID,
                    NAME,
                    EMAIL,
                    ROLE,
                    STATUS,
                    BATCH
                FROM USERS
                ORDER BY USER_ID
            """)

            return cursor.fetchall()

        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    def activate_user(self, user_id):

        connection = None
        cursor = None

        try:
            connection = db.get_connection()
            cursor = connection.cursor()

            cursor.execute("""
                UPDATE USERS
                SET STATUS = 'ACTIVE'
                WHERE USER_ID = :user_id
            """, {
                "user_id": user_id
            })

            connection.commit()

            return True

        except Exception as e:

            print("Activate User Error:", e)

            if connection:
                connection.rollback()

            return False

        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    def deactivate_user(self, user_id):

        connection = None
        cursor = None

        try:
            connection = db.get_connection()
            cursor = connection.cursor()

            cursor.execute("""
                UPDATE USERS
                SET STATUS = 'INACTIVE'
                WHERE USER_ID = :user_id
            """, {
                "user_id": user_id
            })

            connection.commit()

            return True

        except Exception as e:

            print("Deactivate User Error:", e)

            if connection:
                connection.rollback()

            return False

        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

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

            print("Reset Password Error:", e)

            if connection:
                connection.rollback()

            return False

        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    # =========================================================
    # SKILLS
    # =========================================================

    def get_all_skills(self):

        connection = None
        cursor = None

        try:
            connection = db.get_connection()
            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    s.SKILL_ID,
                    s.SKILL_NAME,
                    c.CATEGORY_NAME
                FROM SKILLS s
                JOIN SKILL_CATEGORIES c
                    ON s.CATEGORY_ID = c.CATEGORY_ID
                ORDER BY s.SKILL_ID
            """)

            return cursor.fetchall()

        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    def get_skill_categories(self):

        connection = None
        cursor = None

        try:
            connection = db.get_connection()
            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    CATEGORY_ID,
                    CATEGORY_NAME
                FROM SKILL_CATEGORIES
                ORDER BY CATEGORY_ID
            """)

            return cursor.fetchall()

        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    def add_skill(self, skill_name, category_id):

        connection = None
        cursor = None

        try:
            connection = db.get_connection()
            cursor = connection.cursor()

            cursor.execute("""
                INSERT INTO SKILLS (
                    SKILL_NAME,
                    CATEGORY_ID
                )
                VALUES (
                    :skill_name,
                    :category_id
                )
            """, {
                "skill_name": skill_name,
                "category_id": category_id
            })

            connection.commit()

            return True

        except Exception as e:

            print("Add Skill Error:", e)

            if connection:
                connection.rollback()

            return False

        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    def delete_skill(self, skill_id):

        connection = None
        cursor = None

        try:
            connection = db.get_connection()
            cursor = connection.cursor()

            cursor.execute("""
                DELETE FROM SKILLS
                WHERE SKILL_ID = :skill_id
            """, {
                "skill_id": skill_id
            })

            connection.commit()

            return True

        except Exception as e:

            print("Delete Skill Error:", e)

            if connection:
                connection.rollback()

            return False

        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    # =========================================================
    # SUGGESTIONS
    # =========================================================

    def get_all_suggestions(self):

        connection = None
        cursor = None

        try:
            connection = db.get_connection()
            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    ss.SUGGESTION_ID,
                    ss.USER_ID,
                    ss.SKILL_NAME,
                    sc.CATEGORY_NAME,
                    ss.STATUS
                FROM SKILL_SUGGESTIONS ss
                LEFT JOIN SKILL_CATEGORIES sc
                    ON ss.CATEGORY_ID = sc.CATEGORY_ID
                ORDER BY ss.SUGGESTION_ID
            """)

            return cursor.fetchall()

        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    def approve_suggestion(self, suggestion_id):

        connection = None
        cursor = None

        try:
            connection = db.get_connection()
            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    SKILL_NAME,
                    CATEGORY_ID,
                    STATUS
                FROM SKILL_SUGGESTIONS
                WHERE SUGGESTION_ID = :id
            """, {
                "id": suggestion_id
            })

            row = cursor.fetchone()

            if not row:
                return False

            skill_name, category_id, status = row

            if status == "APPROVED":
                return True

            cursor.execute("""
                INSERT INTO SKILLS (
                    SKILL_NAME,
                    CATEGORY_ID
                )
                VALUES (
                    :skill_name,
                    :category_id
                )
            """, {
                "skill_name": skill_name,
                "category_id": category_id
            })

            cursor.execute("""
                UPDATE SKILL_SUGGESTIONS
                SET STATUS = 'APPROVED'
                WHERE SUGGESTION_ID = :id
            """, {
                "id": suggestion_id
            })

            connection.commit()

            return True

        except Exception as e:

            print("Approve Suggestion Error:", e)

            if connection:
                connection.rollback()

            return False

        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    def reject_suggestion(self, suggestion_id):

        connection = None
        cursor = None

        try:
            connection = db.get_connection()
            cursor = connection.cursor()

            cursor.execute("""
                UPDATE SKILL_SUGGESTIONS
                SET STATUS = 'REJECTED'
                WHERE SUGGESTION_ID = :id
            """, {
                "id": suggestion_id
            })

            connection.commit()

            return True

        except Exception as e:

            print("Reject Suggestion Error:", e)

            if connection:
                connection.rollback()

            return False

        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()


admin_service = AdminService()