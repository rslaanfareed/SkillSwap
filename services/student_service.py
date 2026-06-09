from database.db_connection import db


class StudentService:

    def get_my_offers(self, user_id):

        connection = None
        cursor = None

        try:
            connection = db.get_connection()
            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    o.OFFER_ID,
                    o.SKILL_ID,
                    s.SKILL_NAME,
                    o.SKILL_LEVEL,
                    o.SESSION_MODE
                FROM OFFERS o
                JOIN SKILLS s
                    ON o.SKILL_ID = s.SKILL_ID
                WHERE o.USER_ID = :user_id
                ORDER BY o.OFFER_ID
            """, {
                "user_id": user_id
            })

            return cursor.fetchall()

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

    def get_skills(self):

        connection = None
        cursor = None

        try:
            connection = db.get_connection()
            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    SKILL_ID,
                    SKILL_NAME
                FROM SKILLS
                ORDER BY SKILL_NAME
            """)

            return cursor.fetchall()

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

    def add_offer(
        self,
        user_id,
        skill_id,
        level,
        mode
    ):

        connection = None
        cursor = None

        try:

            connection = db.get_connection()
            cursor = connection.cursor()

            cursor.execute("""
                INSERT INTO OFFERS
                (
                    USER_ID,
                    SKILL_ID,
                    SKILL_LEVEL,
                    SESSION_MODE,
                    CREATED_AT
                )
                VALUES
                (
                    :p_user_id,
                    :p_skill_id,
                    :p_skill_level,
                    :p_session_mode,
                    SYSDATE
                )
            """, {
                "p_user_id": user_id,
                "p_skill_id": skill_id,
                "p_skill_level": level,
                "p_session_mode": mode
            })

            connection.commit()

            return True

        except Exception as e:

            print("\nADD OFFER ERROR:")
            print(e)

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

    def update_offer(
        self,
        offer_id,
        skill_id,
        level,
        mode
    ):

        connection = None
        cursor = None

        try:

            connection = db.get_connection()
            cursor = connection.cursor()

            cursor.execute("""
                UPDATE OFFERS
                SET
                    SKILL_ID = :p_skill_id,
                    SKILL_LEVEL = :p_skill_level,
                    SESSION_MODE = :p_session_mode
                WHERE OFFER_ID = :p_offer_id
            """, {
                "p_skill_id": skill_id,
                "p_skill_level": level,
                "p_session_mode": mode,
                "p_offer_id": offer_id
            })

            connection.commit()

            return True

        except Exception as e:

            print("\nUPDATE OFFER ERROR:")
            print(e)

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

    def delete_offer(self, offer_id):

        connection = None
        cursor = None

        try:

            connection = db.get_connection()
            cursor = connection.cursor()

            cursor.execute("""
                DELETE FROM OFFERS
                WHERE OFFER_ID = :offer_id
            """, {
                "offer_id": offer_id
            })

            connection.commit()

            return True

        except Exception as e:

            print("\nDELETE OFFER ERROR:")
            print(e)

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
    
    def get_available_offers(self, current_user_id):

        connection = None
        cursor = None

        try:

            connection = db.get_connection()
            cursor = connection.cursor()

            cursor.execute("""
                SELECT
    o.OFFER_ID,
    u.NAME,
    s.SKILL_NAME,
    o.SKILL_LEVEL,
    o.SESSION_MODE,

    ROUND(
        NVL(
            AVG(f.SCORE),
            0
        ),
        1
    ) AS RATING,

    COUNT(f.FEEDBACK_ID) AS REVIEW_COUNT

FROM OFFERS o

JOIN USERS u
    ON o.USER_ID = u.USER_ID

JOIN SKILLS s
    ON o.SKILL_ID = s.SKILL_ID

LEFT JOIN SESSIONS se
    ON o.OFFER_ID = se.OFFER_ID

LEFT JOIN FEEDBACK f
    ON se.SESSION_ID = f.SESSION_ID

WHERE o.USER_ID <> :user_id

GROUP BY
    o.OFFER_ID,
    u.NAME,
    s.SKILL_NAME,
    o.SKILL_LEVEL,
    o.SESSION_MODE

ORDER BY s.SKILL_NAME
            """, {
                "user_id": current_user_id
            })

            return cursor.fetchall()

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
    def get_offer_availability(self, offer_id):

        connection = None
        cursor = None

        try:

            connection = db.get_connection()
            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    AVAILABILITY_ID,
                    DAY_OF_WEEK,
                    TIME_SLOT
                FROM AVAILABILITY
                WHERE OFFER_ID = :offer_id
                ORDER BY AVAILABILITY_ID
            """, {
                "offer_id": offer_id
            })

            return cursor.fetchall()

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


    def create_request(
        self,
        user_id,
        offer_id,
        skill_id,
        availability_id,
        urgency,
        note
        ):

        connection = None
        cursor = None

        try:

            connection = db.get_connection()
            cursor = connection.cursor()

            cursor.execute("""
                INSERT INTO REQUESTS
                (
                    USER_ID,
                    SKILL_ID,
                    OFFER_ID,
                    SELECTED_AVAILABILITY_ID,
                    URGENCY,
                    NOTE,
                    REQUESTED_AT,
                    STATUS
                )
                VALUES
                (
                    :p_user_id,
                    :p_skill_id,
                    :p_offer_id,
                    :p_availability_id,
                    :p_urgency,
                    :p_note,
                    SYSDATE,
                    'PENDING'
                )
            """, {
                "p_user_id": user_id,
                "p_skill_id": skill_id,
                "p_offer_id": offer_id,
                "p_availability_id": availability_id,
                "p_urgency": urgency,
                "p_note": note
            })

            connection.commit()

            

            cursor.execute("""
                SELECT
                    o.USER_ID,
                    s.SKILL_NAME
                FROM OFFERS o
                JOIN SKILLS s
                    ON o.SKILL_ID = s.SKILL_ID
                WHERE o.OFFER_ID = :offer_id
            """, {
                "offer_id": offer_id
            })

            offer_owner_id, skill_name = cursor.fetchone()

            cursor.execute("""
                SELECT NAME
                FROM USERS
                WHERE USER_ID = :user_id
            """, {
                "user_id": user_id
            })

            requester_name = cursor.fetchone()[0]
            
            self.create_notification(
                offer_owner_id,
                user_id,
                "MATCH",
                f"{requester_name} requested your {skill_name} skill",
                "OFFER",
                offer_id
            )


            return True

        except Exception as e:

            print("\nCREATE REQUEST ERROR:")
            print(e)

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


    def get_my_requests(self, user_id):

        connection = None
        cursor = None

        try:

            connection = db.get_connection()
            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    r.REQUEST_ID,
                    s.SKILL_NAME,
                    u.NAME,
                    a.DAY_OF_WEEK || ' - ' || a.TIME_SLOT,
                    r.URGENCY,
                    r.STATUS,
                    TO_CHAR(
                        r.REQUESTED_AT,
                        'DD-MON-YYYY'
                    )
                FROM REQUESTS r
                JOIN SKILLS s
                    ON r.SKILL_ID = s.SKILL_ID
                JOIN OFFERS o
                    ON r.OFFER_ID = o.OFFER_ID
                JOIN USERS u
                    ON o.USER_ID = u.USER_ID
                JOIN AVAILABILITY a
                    ON r.SELECTED_AVAILABILITY_ID =
                    a.AVAILABILITY_ID
                WHERE r.USER_ID = :user_id
                ORDER BY r.REQUEST_ID DESC
            """, {
                "user_id": user_id
            })

            return cursor.fetchall()

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


    def cancel_request(self, request_id):

        connection = None
        cursor = None

        try:

            connection = db.get_connection()
            cursor = connection.cursor()

            cursor.execute("""
                DELETE FROM REQUESTS
                WHERE REQUEST_ID = :request_id
                AND STATUS = 'PENDING'
            """, {
                "request_id": request_id
            })

            connection.commit()

            return True

        except Exception as e:

            print("\nCANCEL REQUEST ERROR:")
            print(e)

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

    def get_received_requests(self, user_id):

            connection = None
            cursor = None

            try:

                connection = db.get_connection()
                cursor = connection.cursor()

                cursor.execute("""
                    SELECT
                        r.REQUEST_ID,
                        requester.NAME,
                        s.SKILL_NAME,
                        a.DAY_OF_WEEK || ' - ' || a.TIME_SLOT,
                        r.URGENCY,
                        r.STATUS,
                        TO_CHAR(
                            r.REQUESTED_AT,
                            'DD-MON-YYYY'
                        )
                    FROM REQUESTS r
                    JOIN OFFERS o
                        ON r.OFFER_ID = o.OFFER_ID
                    JOIN USERS requester
                        ON r.USER_ID = requester.USER_ID
                    JOIN SKILLS s
                        ON r.SKILL_ID = s.SKILL_ID
                    JOIN AVAILABILITY a
                        ON r.SELECTED_AVAILABILITY_ID =
                        a.AVAILABILITY_ID
                    WHERE o.USER_ID = :user_id
                    ORDER BY r.REQUEST_ID DESC
                """, {
                    "user_id": user_id
                })

                return cursor.fetchall()

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


    def approve_request(self, request_id):

        connection = None
        cursor = None

        try:

            connection = db.get_connection()
            cursor = connection.cursor()

            cursor.execute("""
                UPDATE REQUESTS
                SET STATUS = 'ACCEPTED'
                WHERE REQUEST_ID = :request_id
            """, {
                "request_id": request_id
            })

            connection.commit()

            return True

        except Exception as e:

            print("\nAPPROVE REQUEST ERROR:")
            print(e)

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

    def reject_request(self, request_id):

        connection = None
        cursor = None

        try:

            connection = db.get_connection()
            cursor = connection.cursor()

            cursor.execute("""
                UPDATE REQUESTS
                SET STATUS = 'REJECTED'
                WHERE REQUEST_ID = :request_id
            """, {
                "request_id": request_id
            })

            connection.commit()

            return True

        except Exception as e:

            print("\nREJECT REQUEST ERROR:")
            print(e)

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
    
    def get_incoming_requests(self, user_id):

        connection = None
        cursor = None

        try:

            connection = db.get_connection()
            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    r.REQUEST_ID,
                    requester.NAME,
                    s.SKILL_NAME,
                    a.DAY_OF_WEEK || ' - ' || a.TIME_SLOT,
                    r.URGENCY,
                    r.STATUS,
                    TO_CHAR(
                        r.REQUESTED_AT,
                        'DD-MON-YYYY'
                    )
                FROM REQUESTS r
                JOIN OFFERS o
                    ON r.OFFER_ID = o.OFFER_ID
                JOIN USERS requester
                    ON r.USER_ID = requester.USER_ID
                JOIN SKILLS s
                    ON r.SKILL_ID = s.SKILL_ID
                JOIN AVAILABILITY a
                    ON r.SELECTED_AVAILABILITY_ID =
                    a.AVAILABILITY_ID
                WHERE o.USER_ID = :user_id
                ORDER BY r.REQUEST_ID DESC
            """, {
                "user_id": user_id
            })

            return cursor.fetchall()

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

    
    def create_session(
        self,
        offer_id,
        request_id,
        session_date,
        meeting_detail
    ):

        connection = None
        cursor = None

        try:

            connection = db.get_connection()
            cursor = connection.cursor()

            cursor.execute("""
                INSERT INTO SESSIONS
                (

                    OFFER_ID,
                    REQUEST_ID,
                    SESSION_DATE,
                    MEETING_DETAIL,
                    STATUS,
                    REQUESTER_CONFIRMED,
                    OFFERER_CONFIRMED
                )
                VALUES
                (

                    :offer_id,
                    :request_id,
                    TO_DATE(
                        :session_date,
                        'YYYY-MM-DD'
                    ),
                    :meeting_detail,
                    'SCHEDULED',
                    0,
                    1
                )
            """, {
                "offer_id": offer_id,
                "request_id": request_id,
                "session_date": session_date,
                "meeting_detail": meeting_detail
            })

            connection.commit()

            return True

        except Exception as e:

            print("\nCREATE SESSION ERROR:")
            print(e)

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


    def get_my_sessions(self, user_id):

        connection = None
        cursor = None

        try:

            connection = db.get_connection()
            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    se.SESSION_ID,
                    s.SKILL_NAME,
                    u.NAME,
                    TO_CHAR(
                        se.SESSION_DATE,
                        'DD-MON-YYYY'
                    ),
                    se.STATUS,
                    se.MEETING_DETAIL,
                    r.USER_ID
                FROM SESSIONS se
                JOIN REQUESTS r
                    ON se.REQUEST_ID = r.REQUEST_ID
                JOIN OFFERS o
                    ON se.OFFER_ID = o.OFFER_ID
                JOIN SKILLS s
                    ON o.SKILL_ID = s.SKILL_ID
                JOIN USERS u
                    ON (
                        CASE
                            WHEN o.USER_ID = :user_id
                            THEN r.USER_ID
                            ELSE o.USER_ID
                        END
                    ) = u.USER_ID
                WHERE o.USER_ID = :user_id
                OR r.USER_ID = :user_id
                ORDER BY se.SESSION_DATE DESC
            """, {
                "user_id": user_id
            })

            return cursor.fetchall()

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

    def confirm_session(self, session_id):

        connection = None
        cursor = None

        try:

            connection = db.get_connection()
            cursor = connection.cursor()

            cursor.execute("""
                UPDATE SESSIONS
                SET REQUESTER_CONFIRMED = 1
                WHERE SESSION_ID = :session_id
            """, {
                "session_id": session_id
            })

            connection.commit()

            return True

        except Exception as e:

            print("\nCONFIRM SESSION ERROR:")
            print(e)

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

    def complete_session(self, session_id):

        connection = None
        cursor = None

        try:

            connection = db.get_connection()
            cursor = connection.cursor()

            cursor.execute("""
                UPDATE SESSIONS
                SET
                    STATUS = 'COMPLETED',
                    COMPLETED_AT = SYSDATE
                WHERE SESSION_ID = :session_id
            """, {
                "session_id": session_id
            })

            connection.commit()

            return True

        except Exception as e:

            print("\nCOMPLETE SESSION ERROR:")
            print(e)

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

    def get_session_messages(self, session_id):

        connection = None
        cursor = None

        try:

            connection = db.get_connection()
            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    m.MESSAGE_ID,
                    m.SENDER_ID,
                    u.NAME,
                    m.CONTENT,
                    m.SENT_AT,
                    m.IS_READ
                FROM MESSAGES m
                JOIN USERS u
                    ON m.SENDER_ID = u.USER_ID
                WHERE m.SESSION_ID = :session_id
                ORDER BY m.SENT_AT
            """, {
                "session_id": session_id
            })

            return cursor.fetchall()

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

    def send_message(
        self,
        session_id,
        sender_id,
        content
    ):

        connection = None
        cursor = None

        try:

            if not content.strip():
                return False

            connection = db.get_connection()
            cursor = connection.cursor()

            cursor.execute("""
                INSERT INTO MESSAGES
                (
                    
                    SESSION_ID,
                    SENDER_ID,
                    CONTENT,
                    SENT_AT,
                    IS_READ
                )
                VALUES
                (
                    
                    :session_id,
                    :sender_id,
                    :content,
                    SYSDATE,
                    0
                )
            """, {
                "session_id": session_id,
                "sender_id": sender_id,
                "content": content
            })

            connection.commit()

            return True

        except Exception as e:

            print("\nSEND MESSAGE ERROR:")
            print(e)

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

    def mark_messages_read(
        self,
        session_id,
        current_user_id
    ):

        connection = None
        cursor = None

        try:

            connection = db.get_connection()
            cursor = connection.cursor()

            cursor.execute("""
                UPDATE MESSAGES
                SET IS_READ = 1
                WHERE SESSION_ID = :session_id
                AND SENDER_ID <> :current_user_id
                AND IS_READ = 0
            """, {
                "session_id": session_id,
                "current_user_id": current_user_id
            })

            connection.commit()

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

    def has_feedback(self, session_id):

        connection = None
        cursor = None

        try:

            connection = db.get_connection()
            cursor = connection.cursor()

            cursor.execute("""
                SELECT COUNT(*)
                FROM FEEDBACK
                WHERE SESSION_ID = :session_id
            """, {
                "session_id": session_id
            })

            count = cursor.fetchone()[0]

            return count > 0

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

    def add_feedback(
        self,
        session_id,
        score,
        feedback_text
    ):

        connection = None
        cursor = None

        try:

            connection = db.get_connection()
            cursor = connection.cursor()

            cursor.execute("""
                INSERT INTO FEEDBACK
                (
                    SESSION_ID,
                    SCORE,
                    FEEDBACK_TEXT,
                    GIVEN_AT
                )
                VALUES
                (
                    :session_id,
                    :score,
                    :feedback_text,
                    SYSDATE
                )
            """, {
                "session_id": session_id,
                "score": score,
                "feedback_text": feedback_text
            })

            connection.commit()

            return True

        except Exception as e:

            print("\nADD FEEDBACK ERROR:")
            print(e)

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

    def get_dashboard_stats(self, user_id):

        connection = None
        cursor = None

        try:

            connection = db.get_connection()
            cursor = connection.cursor()

            cursor.execute("""
    SELECT
        (
            SELECT COUNT(*)
            FROM OFFERS
            WHERE USER_ID = :user_id
        ) AS OFFER_COUNT,

        (
            SELECT COUNT(*)
            FROM REQUESTS
            WHERE USER_ID = :user_id
        ) AS REQUEST_COUNT,

        (
            SELECT COUNT(*)
            FROM SESSIONS se
            JOIN OFFERS o
                ON se.OFFER_ID = o.OFFER_ID
            JOIN REQUESTS r
                ON se.REQUEST_ID = r.REQUEST_ID
            WHERE o.USER_ID = :user_id
            OR r.USER_ID = :user_id
        ) AS SESSION_COUNT,

        NVL(
            (
                SELECT ROUND(
                    AVG(f.SCORE),
                    1
                )
                FROM FEEDBACK f
                JOIN SESSIONS se
                    ON f.SESSION_ID = se.SESSION_ID
                JOIN OFFERS o
                    ON se.OFFER_ID = o.OFFER_ID
                WHERE o.USER_ID = :user_id
            ),
            0
        ) AS AVG_RATING,

        (
            SELECT COUNT(*)
            FROM FEEDBACK f
            JOIN SESSIONS se
                ON f.SESSION_ID = se.SESSION_ID
            JOIN OFFERS o
                ON se.OFFER_ID = o.OFFER_ID
            WHERE o.USER_ID = :user_id
        ) AS REVIEW_COUNT

    FROM DUAL
""", {
    "user_id": user_id
})

            row = cursor.fetchone()

            return {
                "offers": row[0],
                "requests": row[1],
                "sessions": row[2],
                "rating": row[3],
                "reviews": row[4]
            }

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

    def get_upcoming_session(self, user_id):

        connection = None
        cursor = None

        try:

            connection = db.get_connection()
            cursor = connection.cursor()

            cursor.execute("""
                SELECT *
                FROM (
                    SELECT
                        s.SKILL_NAME,
                        u.NAME,
                        TO_CHAR(
                            se.SESSION_DATE,
                            'DD-MON-YYYY'
                        ) AS SESSION_DATE,
                        se.MEETING_DETAIL,
                        se.STATUS
                    FROM SESSIONS se

                    JOIN OFFERS o
                        ON se.OFFER_ID = o.OFFER_ID

                    JOIN REQUESTS r
                        ON se.REQUEST_ID = r.REQUEST_ID

                    JOIN SKILLS s
                        ON o.SKILL_ID = s.SKILL_ID

                    JOIN USERS u
                        ON (
                            CASE
                                WHEN o.USER_ID = :user_id
                                THEN r.USER_ID
                                ELSE o.USER_ID
                            END
                        ) = u.USER_ID

                    WHERE (
                        o.USER_ID = :user_id
                        OR r.USER_ID = :user_id
                    )
                    AND se.STATUS = 'SCHEDULED'

                    ORDER BY se.SESSION_DATE
                )
                WHERE ROWNUM = 1
            """, {
                "user_id": user_id
            })

            return cursor.fetchone()

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


    def get_my_skills(self, user_id):

        connection = None
        cursor = None

        try:

            connection = db.get_connection()
            cursor = connection.cursor()

            cursor.execute("""
                SELECT DISTINCT
                    s.SKILL_NAME
                FROM OFFERS o
                JOIN SKILLS s
                    ON o.SKILL_ID = s.SKILL_ID
                WHERE o.USER_ID = :user_id
                ORDER BY s.SKILL_NAME
            """, {
                "user_id": user_id
            })

            return cursor.fetchall()

        finally:

            if cursor:
                cursor.close()

            if connection:
                connection.close()


    def get_recent_feedback(self, user_id):

        connection = None
        cursor = None

        try:

            connection = db.get_connection()
            cursor = connection.cursor()

            cursor.execute("""
                SELECT *
                FROM (
                    SELECT
                        f.SCORE,
                        f.FEEDBACK_TEXT
                    FROM FEEDBACK f
                    JOIN SESSIONS se
                        ON f.SESSION_ID = se.SESSION_ID
                    JOIN OFFERS o
                        ON se.OFFER_ID = o.OFFER_ID
                    WHERE o.USER_ID = :user_id
                    ORDER BY f.GIVEN_AT DESC
                )
                WHERE ROWNUM = 1
            """, {
                "user_id": user_id
            })

            return cursor.fetchone()

        finally:

            if cursor:
                cursor.close()

            if connection:
                connection.close()

    def create_notification(
        self,
        to_user_id,
        from_user_id,
        notification_type,
        content,
        target_type,
        target_id
    ):

        connection = None
        cursor = None

        try:

            connection = db.get_connection()
            cursor = connection.cursor()

            cursor.execute("""
        INSERT INTO NOTIFICATIONS (
    TO_USER_ID,
    FROM_USER_ID,
    NOTIFICATION_TYPE,
    CONTENT,
    CREATED_AT,
    IS_READ,
    TARGET_TYPE,
    TARGET_ID
)
VALUES (
    :to_user_id,
    :from_user_id,
    :notification_type,
    :content,
    SYSDATE,
    0,
    :target_type,
    :target_id
)
""", {
    "to_user_id": to_user_id,
    "from_user_id": from_user_id,
    "notification_type": notification_type,
    "content": content,
    "target_type": target_type,
    "target_id": target_id
})

            connection.commit()

        finally:

            if cursor:
                cursor.close()

            if connection:
                connection.close()

    def get_notifications(self, user_id):

        connection = None
        cursor = None

        try:

            connection = db.get_connection()
            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    NOTIFICATION_ID,
                    CONTENT,
                    TO_CHAR(
                        CREATED_AT,
                        'DD-MON HH24:MI'
                    ),
                    IS_READ,
                    TARGET_TYPE,
                    TARGET_ID
                FROM NOTIFICATIONS
                WHERE TO_USER_ID = :user_id
                ORDER BY CREATED_AT DESC
            """, {
                "user_id": user_id
            })

            return cursor.fetchall()

        finally:

            if cursor:
                cursor.close()

            if connection:
                connection.close()

    def mark_notification_read(
        self,
        notification_id
    ):

        connection = None
        cursor = None

        try:

            connection = db.get_connection()
            cursor = connection.cursor()

            cursor.execute("""
                UPDATE NOTIFICATIONS
                SET IS_READ = 1
                WHERE NOTIFICATION_ID = :id
            """, {
                "id": notification_id
            })

            connection.commit()

        finally:

            if cursor:
                cursor.close()

            if connection:
                connection.close()


    def submit_skill_suggestion(
        self,
        user_id,
        skill_name,
        category_id
    ):

        connection = None
        cursor = None

        try:

            connection = db.get_connection()
            cursor = connection.cursor()

            cursor.execute("""
                SELECT COUNT(*)
                FROM SKILLS
                WHERE UPPER(SKILL_NAME)
                    = UPPER(:skill_name)
            """, {
                "skill_name": skill_name
            })

            if cursor.fetchone()[0] > 0:
                return False

            cursor.execute("""
                INSERT INTO SKILL_SUGGESTIONS
                (
                    USER_ID,
                    SKILL_NAME,
                    CATEGORY_ID,
                    STATUS,
                    SUGGESTED_AT
                )
                VALUES
                (
                    :user_id,
                    :skill_name,
                    :category_id,
                    'PENDING',
                    SYSDATE
                )
            """, {
                "user_id": user_id,
                "skill_name": skill_name,
                "category_id": category_id
            })

            connection.commit()

            return True

        except Exception as e:

            print(e)
            return False

        finally:

            if cursor:
                cursor.close()

            if connection:
                connection.close()

    def get_categories(self):

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
                ORDER BY CATEGORY_NAME
            """)

            return cursor.fetchall()

        finally:

            if cursor:
                cursor.close()

            if connection:
                connection.close()

    def add_availability(
        self,
        offer_id,
        day_of_week,
        time_slot
    ):

        connection = None
        cursor = None

        try:

            connection = db.get_connection()
            cursor = connection.cursor()

            cursor.execute("""
                INSERT INTO AVAILABILITY
                (
                    OFFER_ID,
                    DAY_OF_WEEK,
                    TIME_SLOT
                )
                VALUES
                (
                    :offer_id,
                    :day_of_week,
                    :time_slot
                )
            """, {
                "offer_id": offer_id,
                "day_of_week": day_of_week,
                "time_slot": time_slot
            })

            connection.commit()

            return True

        except Exception as e:

            print(e)
            return False

        finally:

            if cursor:
                cursor.close()

            if connection:
                connection.close()

    def get_availability_for_offer(
        self,
        offer_id
    ):

        connection = None
        cursor = None

        try:

            connection = db.get_connection()
            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    DAY_OF_WEEK,
                    TIME_SLOT
                FROM AVAILABILITY
                WHERE OFFER_ID = :offer_id
                ORDER BY DAY_OF_WEEK
            """, {
                "offer_id": offer_id
            })

            return cursor.fetchall()

        finally:

            if cursor:
                cursor.close()

            if connection:
                connection.close()

student_service = StudentService()