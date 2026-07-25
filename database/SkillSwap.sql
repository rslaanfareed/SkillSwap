-- =====================================================
-- SKILLSWAP DATABASE PROJECT
-- Database Systems Semester Project
-- =====================================================

                        -- =====================================================
                        -- SECTION 1: TABLE CREATION
                        -- =====================================================


-- ============================================================
-- DEPARTMENTS
-- ============================================================
CREATE TABLE DEPARTMENTS (
DEPARTMENT_ID   NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
DEPARTMENT_NAME VARCHAR2(100) NOT NULL,
FACULTY         VARCHAR2(100) NOT NULL,


CONSTRAINT UQ_DEPARTMENTS_NAME
    UNIQUE (DEPARTMENT_NAME)


);

-- ============================================================
-- SKILL CATEGORIES
-- ============================================================
CREATE TABLE SKILL_CATEGORIES (
CATEGORY_ID    NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
CATEGORY_NAME  VARCHAR2(100) NOT NULL,
DEPARTMENT_ID  NUMBER NOT NULL,


CONSTRAINT FK_SKILL_CATEGORIES_DEPT
    FOREIGN KEY (DEPARTMENT_ID)
    REFERENCES DEPARTMENTS (DEPARTMENT_ID),

CONSTRAINT UQ_SKILL_CATEGORIES_NAME
    UNIQUE (DEPARTMENT_ID, CATEGORY_NAME)


);

-- ============================================================
-- SKILLS
-- ============================================================
CREATE TABLE SKILLS (
SKILL_ID      NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
SKILL_NAME    VARCHAR2(100) NOT NULL,
CATEGORY_ID   NUMBER NOT NULL,


CONSTRAINT FK_SKILLS_CATEGORY
    FOREIGN KEY (CATEGORY_ID)
    REFERENCES SKILL_CATEGORIES (CATEGORY_ID),

CONSTRAINT UQ_SKILLS_NAME
    UNIQUE (CATEGORY_ID, SKILL_NAME)


);

-- ============================================================
-- USERS
-- ============================================================
CREATE TABLE USERS (
USER_ID        NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
DEPARTMENT_ID  NUMBER NOT NULL,


NAME           VARCHAR2(200) NOT NULL,
BATCH          NUMBER(4) NOT NULL,

EMAIL          VARCHAR2(255) NOT NULL,
PHONE          VARCHAR2(20),

PASSWORD_HASH  VARCHAR2(255) NOT NULL,

ROLE           VARCHAR2(10) DEFAULT 'STUDENT' NOT NULL,
STATUS         VARCHAR2(10) DEFAULT 'ACTIVE' NOT NULL,

CREATED_AT     DATE DEFAULT SYSDATE NOT NULL,

CONSTRAINT FK_USERS_DEPT
    FOREIGN KEY (DEPARTMENT_ID)
    REFERENCES DEPARTMENTS (DEPARTMENT_ID),

CONSTRAINT UQ_USERS_EMAIL
    UNIQUE (EMAIL),

CONSTRAINT CHK_USERS_ROLE
    CHECK (ROLE IN ('ADMIN','STUDENT')),

CONSTRAINT CHK_USERS_STATUS
    CHECK (STATUS IN ('ACTIVE','INACTIVE'))


);

-- ============================================================
-- SKILL SUGGESTIONS
-- ============================================================
CREATE TABLE SKILL_SUGGESTIONS (
SUGGESTION_ID NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,


USER_ID       NUMBER NOT NULL,
SKILL_NAME    VARCHAR2(150) NOT NULL,
CATEGORY_ID   NUMBER,

STATUS        VARCHAR2(10) DEFAULT 'PENDING' NOT NULL,

SUGGESTED_AT  DATE DEFAULT SYSDATE NOT NULL,
REVIEWED_AT   DATE,

CONSTRAINT FK_SUGGESTIONS_USER
    FOREIGN KEY (USER_ID)
    REFERENCES USERS (USER_ID),

CONSTRAINT FK_SUGGESTIONS_CAT
    FOREIGN KEY (CATEGORY_ID)
    REFERENCES SKILL_CATEGORIES (CATEGORY_ID),

CONSTRAINT CHK_SUGGESTIONS_STATUS
    CHECK (STATUS IN ('PENDING','APPROVED','REJECTED'))


);

-- ============================================================
-- OFFERS
-- ============================================================
CREATE TABLE OFFERS (
OFFER_ID      NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,


USER_ID       NUMBER NOT NULL,
SKILL_ID      NUMBER NOT NULL,

SKILL_LEVEL   VARCHAR2(15) NOT NULL,
SESSION_MODE  VARCHAR2(10) NOT NULL,

CREATED_AT    DATE DEFAULT SYSDATE NOT NULL,

CONSTRAINT FK_OFFERS_USER
    FOREIGN KEY (USER_ID)
    REFERENCES USERS (USER_ID),

CONSTRAINT FK_OFFERS_SKILL
    FOREIGN KEY (SKILL_ID)
    REFERENCES SKILLS (SKILL_ID),

CONSTRAINT UQ_OFFERS_USER_SKILL
    UNIQUE (USER_ID, SKILL_ID),

CONSTRAINT CHK_OFFERS_LEVEL
    CHECK (SKILL_LEVEL IN ('BEGINNER','INTERMEDIATE','EXPERT')),

CONSTRAINT CHK_OFFERS_MODE
    CHECK (SESSION_MODE IN ('ONLINE','IN_PERSON','BOTH'))


);

-- ============================================================
-- AVAILABILITY
-- ============================================================
CREATE TABLE AVAILABILITY (
AVAILABILITY_ID NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,


OFFER_ID        NUMBER NOT NULL,

DAY_OF_WEEK     VARCHAR2(10) NOT NULL,
TIME_SLOT       VARCHAR2(10) NOT NULL,

CONSTRAINT FK_AVAILABILITY_OFFER
    FOREIGN KEY (OFFER_ID)
    REFERENCES OFFERS (OFFER_ID),

CONSTRAINT CHK_AVAIL_DAY
    CHECK (
        DAY_OF_WEEK IN (
            'MONDAY',
            'TUESDAY',
            'WEDNESDAY',
            'THURSDAY',
            'FRIDAY',
            'SATURDAY',
            'SUNDAY'
        )
    ),

CONSTRAINT CHK_AVAIL_TIME
    CHECK (
        TIME_SLOT IN (
            'MORNING',
            'AFTERNOON',
            'EVENING'
        )
    ),

CONSTRAINT UQ_AVAIL_DAY_TIME
    UNIQUE (OFFER_ID, DAY_OF_WEEK, TIME_SLOT)


);

-- ============================================================
-- REQUESTS
-- ============================================================
CREATE TABLE REQUESTS (
REQUEST_ID NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,


USER_ID NUMBER NOT NULL,
SKILL_ID NUMBER NOT NULL,

OFFER_ID NUMBER NOT NULL,
SELECTED_AVAILABILITY_ID NUMBER NOT NULL,

URGENCY VARCHAR2(10) DEFAULT 'LOW' NOT NULL,

NOTE VARCHAR2(500),

REQUESTED_AT DATE DEFAULT SYSDATE NOT NULL,

STATUS VARCHAR2(10) DEFAULT 'PENDING' NOT NULL,

CONSTRAINT FK_REQUESTS_USER
    FOREIGN KEY (USER_ID)
    REFERENCES USERS (USER_ID),

CONSTRAINT FK_REQUESTS_SKILL
    FOREIGN KEY (SKILL_ID)
    REFERENCES SKILLS (SKILL_ID),

CONSTRAINT FK_REQUESTS_OFFER
    FOREIGN KEY (OFFER_ID)
    REFERENCES OFFERS (OFFER_ID),

CONSTRAINT FK_REQUESTS_AVAIL
    FOREIGN KEY (SELECTED_AVAILABILITY_ID)
    REFERENCES AVAILABILITY (AVAILABILITY_ID),

CONSTRAINT CHK_REQUESTS_URGENCY
    CHECK (URGENCY IN ('LOW','MEDIUM','HIGH')),

CONSTRAINT CHK_REQUESTS_STATUS
    CHECK (
        STATUS IN (
            'PENDING',
            'ACCEPTED',
            'REJECTED',
            'COMPLETED',
            'CANCELLED'
        )
    )


);

-- ============================================================
-- SESSIONS
-- ============================================================
CREATE TABLE SESSIONS (
SESSION_ID NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,


OFFER_ID NUMBER NOT NULL,
REQUEST_ID NUMBER NOT NULL,

SESSION_DATE DATE NOT NULL,
MEETING_DETAIL VARCHAR2(255),

STATUS VARCHAR2(10) DEFAULT 'SCHEDULED' NOT NULL,

REQUESTER_CONFIRMED NUMBER(1) DEFAULT 0 NOT NULL,
OFFERER_CONFIRMED NUMBER(1) DEFAULT 0 NOT NULL,

COMPLETED_AT DATE,

CONSTRAINT FK_SESSIONS_OFFER
    FOREIGN KEY (OFFER_ID)
    REFERENCES OFFERS (OFFER_ID),

CONSTRAINT FK_SESSIONS_REQUEST
    FOREIGN KEY (REQUEST_ID)
    REFERENCES REQUESTS (REQUEST_ID),

CONSTRAINT UQ_SESSIONS_REQUEST
    UNIQUE (REQUEST_ID),

CONSTRAINT CHK_SESSIONS_STATUS
    CHECK (
        STATUS IN (
            'SCHEDULED',
            'COMPLETED',
            'CANCELLED'
        )
    )


);

-- ============================================================
-- FEEDBACK
-- ============================================================
CREATE TABLE FEEDBACK (
FEEDBACK_ID NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,


SESSION_ID NUMBER NOT NULL,

SCORE NUMBER(1) NOT NULL,

FEEDBACK_TEXT VARCHAR2(1000),

GIVEN_AT DATE DEFAULT SYSDATE NOT NULL,

CONSTRAINT FK_FEEDBACK_SESSION
    FOREIGN KEY (SESSION_ID)
    REFERENCES SESSIONS (SESSION_ID),

CONSTRAINT UQ_FEEDBACK_SESSION
    UNIQUE (SESSION_ID),

CONSTRAINT CHK_FEEDBACK_SCORE
    CHECK (SCORE BETWEEN 1 AND 5)


);

-- ============================================================
-- ENDORSEMENTS
-- ============================================================
CREATE TABLE ENDORSEMENTS (
ENDORSEMENT_ID NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,


ENDORSED_USER_ID NUMBER NOT NULL,
ENDORSED_BY_ID NUMBER NOT NULL,
SKILL_ID NUMBER NOT NULL,

NOTE VARCHAR2(500),

GIVEN_AT DATE DEFAULT SYSDATE NOT NULL,

CONSTRAINT FK_ENDORSE_USER
    FOREIGN KEY (ENDORSED_USER_ID)
    REFERENCES USERS (USER_ID),

CONSTRAINT FK_ENDORSE_BY
    FOREIGN KEY (ENDORSED_BY_ID)
    REFERENCES USERS (USER_ID),

CONSTRAINT FK_ENDORSE_SKILL
    FOREIGN KEY (SKILL_ID)
    REFERENCES SKILLS (SKILL_ID),

CONSTRAINT UQ_ENDORSEMENT
    UNIQUE (
        ENDORSED_USER_ID,
        ENDORSED_BY_ID,
        SKILL_ID
    )


);

-- ============================================================
-- MESSAGES
-- ============================================================
CREATE TABLE MESSAGES (
MESSAGE_ID NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,


SESSION_ID NUMBER NOT NULL,
SENDER_ID NUMBER NOT NULL,

CONTENT VARCHAR2(4000) NOT NULL,

SENT_AT DATE DEFAULT SYSDATE NOT NULL,

IS_READ NUMBER(1) DEFAULT 0 NOT NULL,

CONSTRAINT FK_MESSAGES_SESSION
    FOREIGN KEY (SESSION_ID)
    REFERENCES SESSIONS (SESSION_ID),

CONSTRAINT FK_MESSAGES_SENDER
    FOREIGN KEY (SENDER_ID)
    REFERENCES USERS (USER_ID),

CONSTRAINT CHK_MESSAGES_READ
    CHECK (IS_READ IN (0,1))


);

-- ============================================================
-- NOTIFICATIONS
-- ============================================================
CREATE TABLE NOTIFICATIONS (
NOTIFICATION_ID NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,


TO_USER_ID NUMBER NOT NULL,
FROM_USER_ID NUMBER,

NOTIFICATION_TYPE VARCHAR2(15) NOT NULL,

CONTENT VARCHAR2(1000) NOT NULL,

CREATED_AT DATE DEFAULT SYSDATE NOT NULL,

IS_READ NUMBER(1) DEFAULT 0 NOT NULL,

CONSTRAINT FK_NOTIF_TO_USER
    FOREIGN KEY (TO_USER_ID)
    REFERENCES USERS (USER_ID),

CONSTRAINT FK_NOTIF_FROM_USER
    FOREIGN KEY (FROM_USER_ID)
    REFERENCES USERS (USER_ID),

CONSTRAINT CHK_NOTIF_TYPE
    CHECK (
        NOTIFICATION_TYPE IN (
            'MATCH',
            'SESSION',
            'FEEDBACK',
            'ENDORSEMENT',
            'MESSAGE'
        )
    ),

CONSTRAINT CHK_NOTIF_IS_READ
    CHECK (IS_READ IN (0,1))


);


                            -- =====================================================
                            -- SECTION 2: INDEX CREATION
                            -- =====================================================



-- USERS
CREATE INDEX IDX_USERS_STATUS
ON USERS (STATUS);

CREATE INDEX IDX_USERS_DEPARTMENT
ON USERS (DEPARTMENT_ID);

-- SKILLS
CREATE INDEX IDX_SKILLS_NAME
ON SKILLS (SKILL_NAME);

CREATE INDEX IDX_SKILLS_CATEGORY
ON SKILLS (CATEGORY_ID);

-- OFFERS
CREATE INDEX IDX_OFFERS_USER
ON OFFERS (USER_ID);

CREATE INDEX IDX_OFFERS_SKILL
ON OFFERS (SKILL_ID);

-- REQUESTS
CREATE INDEX IDX_REQUESTS_USER
ON REQUESTS (USER_ID);

CREATE INDEX IDX_REQUESTS_SKILL
ON REQUESTS (SKILL_ID);

CREATE INDEX IDX_REQUESTS_STATUS
ON REQUESTS (STATUS);

CREATE INDEX IDX_REQUESTS_OFFER
ON REQUESTS (OFFER_ID);

-- SESSIONS
CREATE INDEX IDX_SESSIONS_STATUS
ON SESSIONS (STATUS);

CREATE INDEX IDX_SESSIONS_OFFER
ON SESSIONS (OFFER_ID);

-- MESSAGES
CREATE INDEX IDX_MESSAGES_SESSION
ON MESSAGES (SESSION_ID);

CREATE INDEX IDX_MESSAGES_SENDER
ON MESSAGES (SENDER_ID);

-- NOTIFICATIONS
CREATE INDEX IDX_NOTIFICATIONS_USER
ON NOTIFICATIONS (TO_USER_ID);

CREATE INDEX IDX_NOTIFICATIONS_READ
ON NOTIFICATIONS (IS_READ);

CREATE INDEX IDX_NOTIFICATIONS_TYPE
ON NOTIFICATIONS (NOTIFICATION_TYPE);

-- ENDORSEMENTS
CREATE INDEX IDX_ENDORSEMENTS_USER
ON ENDORSEMENTS (ENDORSED_USER_ID);




                        -- =====================================================
                        -- SECTION 3: TRIGGERS
                        -- =====================================================

-- ============================================================
-- SkillSwap - Oracle PL/SQL Triggers (Business Rules)
-- Final version matched to the finalized schema
-- ============================================================

-- ============================================================
-- 1. Prevent duplicate active requests
--    Same user cannot have more than one PENDING/ACCEPTED
--    request for the same skill.
--    Uses a compound trigger to avoid mutating-table issues.
-- ============================================================
CREATE OR REPLACE TRIGGER trg_no_duplicate_requests
FOR INSERT OR UPDATE OF USER_ID, SKILL_ID, STATUS ON REQUESTS
COMPOUND TRIGGER

    TYPE t_request_rec IS RECORD (
        user_id  REQUESTS.USER_ID%TYPE,
        skill_id REQUESTS.SKILL_ID%TYPE
    );

    TYPE t_request_tab IS TABLE OF t_request_rec INDEX BY PLS_INTEGER;

    g_rows   t_request_tab;
    g_index  PLS_INTEGER := 0;

    AFTER EACH ROW IS
    BEGIN
        IF :NEW.STATUS IN ('PENDING', 'ACCEPTED') THEN
            g_index := g_index + 1;
            g_rows(g_index).user_id  := :NEW.USER_ID;
            g_rows(g_index).skill_id := :NEW.SKILL_ID;
        END IF;
    END AFTER EACH ROW;

    AFTER STATEMENT IS
        v_count NUMBER;
    BEGIN
        IF g_index > 0 THEN
            FOR i IN 1 .. g_index LOOP
                SELECT COUNT(*)
                INTO v_count
                FROM REQUESTS
                WHERE USER_ID = g_rows(i).user_id
                  AND SKILL_ID = g_rows(i).skill_id
                  AND STATUS IN ('PENDING', 'ACCEPTED');

                IF v_count > 1 THEN
                    RAISE_APPLICATION_ERROR(
                        -20001,
                        'Duplicate active request for this skill is not allowed.'
                    );
                END IF;
            END LOOP;
        END IF;
    END AFTER STATEMENT;

END trg_no_duplicate_requests;
/
 
-- ============================================================
-- 2. Prevent self-requesting
--    A user cannot request their own offer.
-- ============================================================
CREATE OR REPLACE TRIGGER trg_no_self_request
BEFORE INSERT OR UPDATE OF USER_ID, OFFER_ID ON REQUESTS
FOR EACH ROW
DECLARE
    v_offer_owner NUMBER;
BEGIN
    SELECT USER_ID
    INTO v_offer_owner
    FROM OFFERS
    WHERE OFFER_ID = :NEW.OFFER_ID;

    IF :NEW.USER_ID = v_offer_owner THEN
        RAISE_APPLICATION_ERROR(
            -20002,
            'A user cannot request their own offer.'
        );
    END IF;
EXCEPTION
    WHEN NO_DATA_FOUND THEN
        RAISE_APPLICATION_ERROR(
            -20002,
            'Invalid offer selected.'
        );
END trg_no_self_request;
/
 
-- ============================================================
-- 3. Validate that selected availability belongs to the offer
-- ============================================================
CREATE OR REPLACE TRIGGER trg_validate_availability
BEFORE INSERT OR UPDATE OF OFFER_ID, SELECTED_AVAILABILITY_ID ON REQUESTS
FOR EACH ROW
DECLARE
    v_count NUMBER;
BEGIN
    SELECT COUNT(*)
    INTO v_count
    FROM AVAILABILITY
    WHERE AVAILABILITY_ID = :NEW.SELECTED_AVAILABILITY_ID
      AND OFFER_ID = :NEW.OFFER_ID;

    IF v_count = 0 THEN
        RAISE_APPLICATION_ERROR(
            -20003,
            'Selected availability does not belong to the chosen offer.'
        );
    END IF;
END trg_validate_availability;
/
 
-- ============================================================
-- 4. Auto-complete session when both users confirm
-- ============================================================
CREATE OR REPLACE TRIGGER trg_auto_complete_session
BEFORE INSERT OR UPDATE OF REQUESTER_CONFIRMED, OFFERER_CONFIRMED, STATUS ON SESSIONS
FOR EACH ROW
BEGIN
    IF :NEW.REQUESTER_CONFIRMED = 1
       AND :NEW.OFFERER_CONFIRMED = 1
    THEN
        :NEW.STATUS := 'COMPLETED';
        :NEW.COMPLETED_AT := NVL(:NEW.COMPLETED_AT, SYSDATE);
    END IF;
END trg_auto_complete_session;
/
 
-- ============================================================
-- 5. Prevent feedback before session completion
-- ============================================================
CREATE OR REPLACE TRIGGER trg_no_feedback_before_complete
BEFORE INSERT ON FEEDBACK
FOR EACH ROW
DECLARE
    v_status VARCHAR2(10);
BEGIN
    SELECT STATUS
    INTO v_status
    FROM SESSIONS
    WHERE SESSION_ID = :NEW.SESSION_ID;

    IF v_status <> 'COMPLETED' THEN
        RAISE_APPLICATION_ERROR(
            -20004,
            'Feedback can only be submitted after the session is completed.'
        );
    END IF;
EXCEPTION
    WHEN NO_DATA_FOUND THEN
        RAISE_APPLICATION_ERROR(
            -20004,
            'Invalid session for feedback.'
        );
END trg_no_feedback_before_complete;
/
 
-- ============================================================
-- 6. Prevent self-endorsement
--    Duplicate endorsements are already prevented by the
--    UNIQUE constraint on (ENDORSED_USER_ID, ENDORSED_BY_ID, SKILL_ID).
-- ============================================================
CREATE OR REPLACE TRIGGER trg_no_self_endorsement
BEFORE INSERT OR UPDATE OF ENDORSED_USER_ID, ENDORSED_BY_ID ON ENDORSEMENTS
FOR EACH ROW
BEGIN
    IF :NEW.ENDORSED_USER_ID = :NEW.ENDORSED_BY_ID THEN
        RAISE_APPLICATION_ERROR(
            -20005,
            'A user cannot endorse themselves.'
        );
    END IF;
END trg_no_self_endorsement;
/
 
-- ============================================================
-- 7. Prevent deleting offers with active sessions
-- ============================================================
CREATE OR REPLACE TRIGGER trg_prevent_offer_delete
BEFORE DELETE ON OFFERS
FOR EACH ROW
DECLARE
    v_count NUMBER;
BEGIN
    SELECT COUNT(*)
    INTO v_count
    FROM SESSIONS
    WHERE OFFER_ID = :OLD.OFFER_ID
      AND STATUS = 'SCHEDULED';

    IF v_count > 0 THEN
        RAISE_APPLICATION_ERROR(
            -20006,
            'Cannot delete an offer that has active scheduled sessions.'
        );
    END IF;
END trg_prevent_offer_delete;
/
 
-- ============================================================
-- 8. Prevent messaging outside an accepted session
--    Only participants in the session can send messages.
-- ============================================================
CREATE OR REPLACE TRIGGER trg_validate_message_session
BEFORE INSERT ON MESSAGES
FOR EACH ROW
DECLARE
    v_requester_id NUMBER;
    v_offerer_id   NUMBER;
    v_status       VARCHAR2(10);
BEGIN
    SELECT r.USER_ID, o.USER_ID, s.STATUS
    INTO v_requester_id, v_offerer_id, v_status
    FROM SESSIONS s
    JOIN REQUESTS r ON r.REQUEST_ID = s.REQUEST_ID
    JOIN OFFERS o   ON o.OFFER_ID = s.OFFER_ID
    WHERE s.SESSION_ID = :NEW.SESSION_ID;

    IF v_status NOT IN ('SCHEDULED', 'COMPLETED') THEN
        RAISE_APPLICATION_ERROR(
            -20007,
            'Messages are allowed only after a session has been accepted.'
        );
    END IF;

    IF :NEW.SENDER_ID NOT IN (v_requester_id, v_offerer_id) THEN
        RAISE_APPLICATION_ERROR(
            -20008,
            'Only session participants can send messages.'
        );
    END IF;
EXCEPTION
    WHEN NO_DATA_FOUND THEN
        RAISE_APPLICATION_ERROR(
            -20007,
            'Invalid session for message.'
        );
END trg_validate_message_session;
/

                            -- =====================================================
                            -- SECTION 4: NOTIFICATION TRIGGERS
                            -- =====================================================

-- ============================================================
-- SkillSwap - Notification Triggers
-- ============================================================

-- 1. Request Accepted -> Notify Requester
CREATE OR REPLACE TRIGGER trg_notif_request_accepted
AFTER UPDATE OF STATUS ON REQUESTS
FOR EACH ROW
WHEN (
    NEW.STATUS = 'ACCEPTED'
    AND OLD.STATUS <> 'ACCEPTED'
)
DECLARE
    v_skill_name VARCHAR2(100);
    v_offerer_id NUMBER;
BEGIN
    SELECT SKILL_NAME
    INTO v_skill_name
    FROM SKILLS
    WHERE SKILL_ID = :NEW.SKILL_ID;

    SELECT USER_ID
    INTO v_offerer_id
    FROM OFFERS
    WHERE OFFER_ID = :NEW.OFFER_ID;

    INSERT INTO NOTIFICATIONS (
        TO_USER_ID,
        FROM_USER_ID,
        NOTIFICATION_TYPE,
        CONTENT
    )
    VALUES (
        :NEW.USER_ID,
        v_offerer_id,
        'MATCH',
        'Your request for "' || v_skill_name || '" has been accepted.'
    );
END;
/
 
-- 2. Session Created -> Notify Both Users
CREATE OR REPLACE TRIGGER trg_notif_session_created
AFTER INSERT ON SESSIONS
FOR EACH ROW
DECLARE
    v_requester NUMBER;
    v_offerer   NUMBER;
BEGIN
    SELECT USER_ID
    INTO v_requester
    FROM REQUESTS
    WHERE REQUEST_ID = :NEW.REQUEST_ID;

    SELECT USER_ID
    INTO v_offerer
    FROM OFFERS
    WHERE OFFER_ID = :NEW.OFFER_ID;

    INSERT INTO NOTIFICATIONS (
        TO_USER_ID,
        FROM_USER_ID,
        NOTIFICATION_TYPE,
        CONTENT
    )
    VALUES (
        v_requester,
        v_offerer,
        'SESSION',
        'A session has been scheduled.'
    );

    INSERT INTO NOTIFICATIONS (
        TO_USER_ID,
        FROM_USER_ID,
        NOTIFICATION_TYPE,
        CONTENT
    )
    VALUES (
        v_offerer,
        v_requester,
        'SESSION',
        'A session has been scheduled.'
    );
END;
/
 
-- 3. Feedback Submitted -> Notify Offerer
CREATE OR REPLACE TRIGGER trg_notif_feedback_submitted
AFTER INSERT ON FEEDBACK
FOR EACH ROW
DECLARE
    v_requester NUMBER;
    v_offerer   NUMBER;
BEGIN
    SELECT r.USER_ID,
           o.USER_ID
    INTO v_requester,
         v_offerer
    FROM SESSIONS s
    JOIN REQUESTS r
      ON r.REQUEST_ID = s.REQUEST_ID
    JOIN OFFERS o
      ON o.OFFER_ID = s.OFFER_ID
    WHERE s.SESSION_ID = :NEW.SESSION_ID;

    INSERT INTO NOTIFICATIONS (
        TO_USER_ID,
        FROM_USER_ID,
        NOTIFICATION_TYPE,
        CONTENT
    )
    VALUES (
        v_offerer,
        v_requester,
        'FEEDBACK',
        'You received new feedback.'
    );
END;
/
 
-- 4. Endorsement Submitted -> Notify Endorsed User
CREATE OR REPLACE TRIGGER trg_notif_endorsement_submitted
AFTER INSERT ON ENDORSEMENTS
FOR EACH ROW
BEGIN
    INSERT INTO NOTIFICATIONS (
        TO_USER_ID,
        FROM_USER_ID,
        NOTIFICATION_TYPE,
        CONTENT
    )
    VALUES (
        :NEW.ENDORSED_USER_ID,
        :NEW.ENDORSED_BY_ID,
        'ENDORSEMENT',
        'You received a new endorsement.'
    );
END;
/
 
-- 5. New Message -> Notify Other Participant
CREATE OR REPLACE TRIGGER trg_notif_message
AFTER INSERT ON MESSAGES
FOR EACH ROW
DECLARE
    v_requester NUMBER;
    v_offerer   NUMBER;
    v_receiver  NUMBER;
BEGIN
    SELECT r.USER_ID,
           o.USER_ID
    INTO v_requester,
         v_offerer
    FROM SESSIONS s
    JOIN REQUESTS r
      ON r.REQUEST_ID = s.REQUEST_ID
    JOIN OFFERS o
      ON o.OFFER_ID = s.OFFER_ID
    WHERE s.SESSION_ID = :NEW.SESSION_ID;

    IF :NEW.SENDER_ID = v_requester THEN
        v_receiver := v_offerer;
    ELSE
        v_receiver := v_requester;
    END IF;

    INSERT INTO NOTIFICATIONS (
        TO_USER_ID,
        FROM_USER_ID,
        NOTIFICATION_TYPE,
        CONTENT
    )
    VALUES (
        v_receiver,
        :NEW.SENDER_ID,
        'MESSAGE',
        'You received a new message.'
    );
END;
/

                    -- =====================================================
                    -- SECTION 5: SAMPLE DATA
                    -- =====================================================

-- ============================================================
-- SkillSwap - Seed Data
-- ============================================================
-- Note:
-- PASSWORD_HASH values are placeholders only.
-- Replace them with bcrypt hashes from the Python application
-- if you want real login testing.

-- ============================================================
-- DEPARTMENTS
-- ============================================================
INSERT INTO DEPARTMENTS (DEPARTMENT_NAME, FACULTY)
VALUES ('Software Engineering', 'Computing');

INSERT INTO DEPARTMENTS (DEPARTMENT_NAME, FACULTY)
VALUES ('Computer Science', 'Computing');

INSERT INTO DEPARTMENTS (DEPARTMENT_NAME, FACULTY)
VALUES ('Electrical Engineering', 'Engineering');

INSERT INTO DEPARTMENTS (DEPARTMENT_NAME, FACULTY)
VALUES ('Mechanical Engineering', 'Engineering');

INSERT INTO DEPARTMENTS (DEPARTMENT_NAME, FACULTY)
VALUES ('Civil Engineering', 'Engineering');

-- ============================================================
-- SKILL CATEGORIES
-- ============================================================
INSERT INTO SKILL_CATEGORIES (CATEGORY_NAME, DEPARTMENT_ID)
VALUES (
    'Programming',
    (SELECT DEPARTMENT_ID
     FROM DEPARTMENTS
     WHERE DEPARTMENT_NAME = 'Computer Science')
);

INSERT INTO SKILL_CATEGORIES (CATEGORY_NAME, DEPARTMENT_ID)
VALUES (
    'Design',
    (SELECT DEPARTMENT_ID
     FROM DEPARTMENTS
     WHERE DEPARTMENT_NAME = 'Software Engineering')
);

INSERT INTO SKILL_CATEGORIES (CATEGORY_NAME, DEPARTMENT_ID)
VALUES (
    'Data Science',
    (SELECT DEPARTMENT_ID
     FROM DEPARTMENTS
     WHERE DEPARTMENT_NAME = 'Computer Science')
);

INSERT INTO SKILL_CATEGORIES (CATEGORY_NAME, DEPARTMENT_ID)
VALUES (
    'Electronics',
    (SELECT DEPARTMENT_ID
     FROM DEPARTMENTS
     WHERE DEPARTMENT_NAME = 'Electrical Engineering')
);

INSERT INTO SKILL_CATEGORIES (CATEGORY_NAME, DEPARTMENT_ID)
VALUES (
    'CAD and Manufacturing',
    (SELECT DEPARTMENT_ID
     FROM DEPARTMENTS
     WHERE DEPARTMENT_NAME = 'Mechanical Engineering')
);

INSERT INTO SKILL_CATEGORIES (CATEGORY_NAME, DEPARTMENT_ID)
VALUES (
    'Communication',
    (SELECT DEPARTMENT_ID
     FROM DEPARTMENTS
     WHERE DEPARTMENT_NAME = 'Civil Engineering')
);

-- ============================================================
-- SKILLS
-- ============================================================
INSERT INTO SKILLS (SKILL_NAME, CATEGORY_ID)
VALUES (
    'Python',
    (SELECT CATEGORY_ID FROM SKILL_CATEGORIES WHERE CATEGORY_NAME = 'Programming')
);

INSERT INTO SKILLS (SKILL_NAME, CATEGORY_ID)
VALUES (
    'Java',
    (SELECT CATEGORY_ID FROM SKILL_CATEGORIES WHERE CATEGORY_NAME = 'Programming')
);

INSERT INTO SKILLS (SKILL_NAME, CATEGORY_ID)
VALUES (
    'C++',
    (SELECT CATEGORY_ID FROM SKILL_CATEGORIES WHERE CATEGORY_NAME = 'Programming')
);

INSERT INTO SKILLS (SKILL_NAME, CATEGORY_ID)
VALUES (
    'SQL',
    (SELECT CATEGORY_ID FROM SKILL_CATEGORIES WHERE CATEGORY_NAME = 'Programming')
);

INSERT INTO SKILLS (SKILL_NAME, CATEGORY_ID)
VALUES (
    'Figma',
    (SELECT CATEGORY_ID FROM SKILL_CATEGORIES WHERE CATEGORY_NAME = 'Design')
);

INSERT INTO SKILLS (SKILL_NAME, CATEGORY_ID)
VALUES (
    'UI/UX Design',
    (SELECT CATEGORY_ID FROM SKILL_CATEGORIES WHERE CATEGORY_NAME = 'Design')
);

INSERT INTO SKILLS (SKILL_NAME, CATEGORY_ID)
VALUES (
    'Machine Learning',
    (SELECT CATEGORY_ID FROM SKILL_CATEGORIES WHERE CATEGORY_NAME = 'Data Science')
);

INSERT INTO SKILLS (SKILL_NAME, CATEGORY_ID)
VALUES (
    'Data Analysis',
    (SELECT CATEGORY_ID FROM SKILL_CATEGORIES WHERE CATEGORY_NAME = 'Data Science')
);

INSERT INTO SKILLS (SKILL_NAME, CATEGORY_ID)
VALUES (
    'MATLAB',
    (SELECT CATEGORY_ID FROM SKILL_CATEGORIES WHERE CATEGORY_NAME = 'Electronics')
);

INSERT INTO SKILLS (SKILL_NAME, CATEGORY_ID)
VALUES (
    'Arduino',
    (SELECT CATEGORY_ID FROM SKILL_CATEGORIES WHERE CATEGORY_NAME = 'Electronics')
);

INSERT INTO SKILLS (SKILL_NAME, CATEGORY_ID)
VALUES (
    'AutoCAD',
    (SELECT CATEGORY_ID FROM SKILL_CATEGORIES WHERE CATEGORY_NAME = 'CAD and Manufacturing')
);

INSERT INTO SKILLS (SKILL_NAME, CATEGORY_ID)
VALUES (
    'SolidWorks',
    (SELECT CATEGORY_ID FROM SKILL_CATEGORIES WHERE CATEGORY_NAME = 'CAD and Manufacturing')
);

INSERT INTO SKILLS (SKILL_NAME, CATEGORY_ID)
VALUES (
    'Public Speaking',
    (SELECT CATEGORY_ID FROM SKILL_CATEGORIES WHERE CATEGORY_NAME = 'Communication')
);

INSERT INTO SKILLS (SKILL_NAME, CATEGORY_ID)
VALUES (
    'Technical Writing',
    (SELECT CATEGORY_ID FROM SKILL_CATEGORIES WHERE CATEGORY_NAME = 'Communication')
);

INSERT INTO SKILLS (SKILL_NAME, CATEGORY_ID)
VALUES (
    'Project Planning',
    (SELECT CATEGORY_ID FROM SKILL_CATEGORIES WHERE CATEGORY_NAME = 'Communication')
);

INSERT INTO SKILLS (SKILL_NAME, CATEGORY_ID)
VALUES (
    '3D Printing',
    (SELECT CATEGORY_ID FROM SKILL_CATEGORIES WHERE CATEGORY_NAME = 'CAD and Manufacturing')
);

-- ============================================================
-- USERS
-- ============================================================
INSERT INTO USERS (DEPARTMENT_ID, NAME, BATCH, EMAIL, PHONE, PASSWORD_HASH, ROLE, STATUS)
VALUES (
    (SELECT DEPARTMENT_ID FROM DEPARTMENTS WHERE DEPARTMENT_NAME = 'Computer Science'),
    'Admin User',
    2020,
    'admin@skillswap.edu',
    '0300-0000000',
    'CHANGE_IN_APP',
    'ADMIN',
    'ACTIVE'
);

INSERT INTO USERS (DEPARTMENT_ID, NAME, BATCH, EMAIL, PHONE, PASSWORD_HASH, ROLE, STATUS)
VALUES (
    (SELECT DEPARTMENT_ID FROM DEPARTMENTS WHERE DEPARTMENT_NAME = 'Software Engineering'),
    'Alice Johnson',
    2023,
    'alice@skillswap.edu',
    '0301-1111111',
    'CHANGE_IN_APP',
    'STUDENT',
    'ACTIVE'
);

INSERT INTO USERS (DEPARTMENT_ID, NAME, BATCH, EMAIL, PHONE, PASSWORD_HASH, ROLE, STATUS)
VALUES (
    (SELECT DEPARTMENT_ID FROM DEPARTMENTS WHERE DEPARTMENT_NAME = 'Computer Science'),
    'Bob Smith',
    2022,
    'bob@skillswap.edu',
    '0302-2222222',
    'CHANGE_IN_APP',
    'STUDENT',
    'ACTIVE'
);

INSERT INTO USERS (DEPARTMENT_ID, NAME, BATCH, EMAIL, PHONE, PASSWORD_HASH, ROLE, STATUS)
VALUES (
    (SELECT DEPARTMENT_ID FROM DEPARTMENTS WHERE DEPARTMENT_NAME = 'Electrical Engineering'),
    'Carol Davis',
    2024,
    'carol@skillswap.edu',
    '0303-3333333',
    'CHANGE_IN_APP',
    'STUDENT',
    'ACTIVE'
);

INSERT INTO USERS (DEPARTMENT_ID, NAME, BATCH, EMAIL, PHONE, PASSWORD_HASH, ROLE, STATUS)
VALUES (
    (SELECT DEPARTMENT_ID FROM DEPARTMENTS WHERE DEPARTMENT_NAME = 'Mechanical Engineering'),
    'Dave Brown',
    2023,
    'dave@skillswap.edu',
    '0304-4444444',
    'CHANGE_IN_APP',
    'STUDENT',
    'ACTIVE'
);

INSERT INTO USERS (DEPARTMENT_ID, NAME, BATCH, EMAIL, PHONE, PASSWORD_HASH, ROLE, STATUS)
VALUES (
    (SELECT DEPARTMENT_ID FROM DEPARTMENTS WHERE DEPARTMENT_NAME = 'Civil Engineering'),
    'Elena Khan',
    2024,
    'elena@skillswap.edu',
    '0305-5555555',
    'CHANGE_IN_APP',
    'STUDENT',
    'ACTIVE'
);

INSERT INTO USERS (DEPARTMENT_ID, NAME, BATCH, EMAIL, PHONE, PASSWORD_HASH, ROLE, STATUS)
VALUES (
    (SELECT DEPARTMENT_ID FROM DEPARTMENTS WHERE DEPARTMENT_NAME = 'Software Engineering'),
    'Farhan Ali',
    2022,
    'farhan@skillswap.edu',
    '0306-6666666',
    'CHANGE_IN_APP',
    'STUDENT',
    'ACTIVE'
);

INSERT INTO USERS (DEPARTMENT_ID, NAME, BATCH, EMAIL, PHONE, PASSWORD_HASH, ROLE, STATUS)
VALUES (
    (SELECT DEPARTMENT_ID FROM DEPARTMENTS WHERE DEPARTMENT_NAME = 'Computer Science'),
    'Hira Fatima',
    2023,
    'hira@skillswap.edu',
    '0307-7777777',
    'CHANGE_IN_APP',
    'STUDENT',
    'ACTIVE'
);

INSERT INTO USERS (DEPARTMENT_ID, NAME, BATCH, EMAIL, PHONE, PASSWORD_HASH, ROLE, STATUS)
VALUES (
    (SELECT DEPARTMENT_ID FROM DEPARTMENTS WHERE DEPARTMENT_NAME = 'Electrical Engineering'),
    'Imran Aziz',
    2024,
    'imran@skillswap.edu',
    '0308-8888888',
    'CHANGE_IN_APP',
    'STUDENT',
    'ACTIVE'
);

INSERT INTO USERS (DEPARTMENT_ID, NAME, BATCH, EMAIL, PHONE, PASSWORD_HASH, ROLE, STATUS)
VALUES (
    (SELECT DEPARTMENT_ID FROM DEPARTMENTS WHERE DEPARTMENT_NAME = 'Mechanical Engineering'),
    'Isha Noor',
    2022,
    'isha@skillswap.edu',
    '0309-9999999',
    'CHANGE_IN_APP',
    'STUDENT',
    'ACTIVE'
);

INSERT INTO USERS (DEPARTMENT_ID, NAME, BATCH, EMAIL, PHONE, PASSWORD_HASH, ROLE, STATUS)
VALUES (
    (SELECT DEPARTMENT_ID FROM DEPARTMENTS WHERE DEPARTMENT_NAME = 'Civil Engineering'),
    'Junaid Ahmed',
    2021,
    'junaid@skillswap.edu',
    '0310-1010101',
    'CHANGE_IN_APP',
    'STUDENT',
    'INACTIVE'
);

-- ============================================================
-- SKILL SUGGESTIONS
-- ============================================================
INSERT INTO SKILL_SUGGESTIONS (USER_ID, SKILL_NAME, CATEGORY_ID, STATUS, REVIEWED_AT)
VALUES (
    (SELECT USER_ID FROM USERS WHERE EMAIL = 'alice@skillswap.edu'),
    'React Native',
    (SELECT CATEGORY_ID FROM SKILL_CATEGORIES WHERE CATEGORY_NAME = 'Programming'),
    'PENDING',
    NULL
);

INSERT INTO SKILL_SUGGESTIONS (USER_ID, SKILL_NAME, CATEGORY_ID, STATUS, REVIEWED_AT)
VALUES (
    (SELECT USER_ID FROM USERS WHERE EMAIL = 'bob@skillswap.edu'),
    'Cloud Computing',
    (SELECT CATEGORY_ID FROM SKILL_CATEGORIES WHERE CATEGORY_NAME = 'Data Science'),
    'APPROVED',
    SYSDATE
);

INSERT INTO SKILL_SUGGESTIONS (USER_ID, SKILL_NAME, CATEGORY_ID, STATUS, REVIEWED_AT)
VALUES (
    (SELECT USER_ID FROM USERS WHERE EMAIL = 'hira@skillswap.edu'),
    '3D Printing',
    (SELECT CATEGORY_ID FROM SKILL_CATEGORIES WHERE CATEGORY_NAME = 'CAD and Manufacturing'),
    'REJECTED',
    SYSDATE
);

INSERT INTO SKILL_SUGGESTIONS (USER_ID, SKILL_NAME, CATEGORY_ID, STATUS, REVIEWED_AT)
VALUES (
    (SELECT USER_ID FROM USERS WHERE EMAIL = 'elena@skillswap.edu'),
    'Leadership',
    (SELECT CATEGORY_ID FROM SKILL_CATEGORIES WHERE CATEGORY_NAME = 'Communication'),
    'PENDING',
    NULL
);

-- ============================================================
-- OFFERS
-- ============================================================
INSERT INTO OFFERS (USER_ID, SKILL_ID, SKILL_LEVEL, SESSION_MODE)
VALUES (
    (SELECT USER_ID FROM USERS WHERE EMAIL = 'alice@skillswap.edu'),
    (SELECT SKILL_ID FROM SKILLS WHERE SKILL_NAME = 'Python'),
    'BEGINNER',
    'ONLINE'
);

INSERT INTO OFFERS (USER_ID, SKILL_ID, SKILL_LEVEL, SESSION_MODE)
VALUES (
    (SELECT USER_ID FROM USERS WHERE EMAIL = 'alice@skillswap.edu'),
    (SELECT SKILL_ID FROM SKILLS WHERE SKILL_NAME = 'Figma'),
    'INTERMEDIATE',
    'BOTH'
);

INSERT INTO OFFERS (USER_ID, SKILL_ID, SKILL_LEVEL, SESSION_MODE)
VALUES (
    (SELECT USER_ID FROM USERS WHERE EMAIL = 'bob@skillswap.edu'),
    (SELECT SKILL_ID FROM SKILLS WHERE SKILL_NAME = 'SQL'),
    'EXPERT',
    'ONLINE'
);

INSERT INTO OFFERS (USER_ID, SKILL_ID, SKILL_LEVEL, SESSION_MODE)
VALUES (
    (SELECT USER_ID FROM USERS WHERE EMAIL = 'bob@skillswap.edu'),
    (SELECT SKILL_ID FROM SKILLS WHERE SKILL_NAME = 'Machine Learning'),
    'INTERMEDIATE',
    'ONLINE'
);

INSERT INTO OFFERS (USER_ID, SKILL_ID, SKILL_LEVEL, SESSION_MODE)
VALUES (
    (SELECT USER_ID FROM USERS WHERE EMAIL = 'carol@skillswap.edu'),
    (SELECT SKILL_ID FROM SKILLS WHERE SKILL_NAME = 'MATLAB'),
    'EXPERT',
    'IN_PERSON'
);

INSERT INTO OFFERS (USER_ID, SKILL_ID, SKILL_LEVEL, SESSION_MODE)
VALUES (
    (SELECT USER_ID FROM USERS WHERE EMAIL = 'carol@skillswap.edu'),
    (SELECT SKILL_ID FROM SKILLS WHERE SKILL_NAME = 'Arduino'),
    'BEGINNER',
    'BOTH'
);

INSERT INTO OFFERS (USER_ID, SKILL_ID, SKILL_LEVEL, SESSION_MODE)
VALUES (
    (SELECT USER_ID FROM USERS WHERE EMAIL = 'dave@skillswap.edu'),
    (SELECT SKILL_ID FROM SKILLS WHERE SKILL_NAME = 'AutoCAD'),
    'BEGINNER',
    'IN_PERSON'
);

INSERT INTO OFFERS (USER_ID, SKILL_ID, SKILL_LEVEL, SESSION_MODE)
VALUES (
    (SELECT USER_ID FROM USERS WHERE EMAIL = 'dave@skillswap.edu'),
    (SELECT SKILL_ID FROM SKILLS WHERE SKILL_NAME = 'SolidWorks'),
    'INTERMEDIATE',
    'IN_PERSON'
);

INSERT INTO OFFERS (USER_ID, SKILL_ID, SKILL_LEVEL, SESSION_MODE)
VALUES (
    (SELECT USER_ID FROM USERS WHERE EMAIL = 'elena@skillswap.edu'),
    (SELECT SKILL_ID FROM SKILLS WHERE SKILL_NAME = 'Public Speaking'),
    'EXPERT',
    'BOTH'
);

INSERT INTO OFFERS (USER_ID, SKILL_ID, SKILL_LEVEL, SESSION_MODE)
VALUES (
    (SELECT USER_ID FROM USERS WHERE EMAIL = 'elena@skillswap.edu'),
    (SELECT SKILL_ID FROM SKILLS WHERE SKILL_NAME = 'Technical Writing'),
    'INTERMEDIATE',
    'ONLINE'
);

INSERT INTO OFFERS (USER_ID, SKILL_ID, SKILL_LEVEL, SESSION_MODE)
VALUES (
    (SELECT USER_ID FROM USERS WHERE EMAIL = 'farhan@skillswap.edu'),
    (SELECT SKILL_ID FROM SKILLS WHERE SKILL_NAME = 'C++'),
    'INTERMEDIATE',
    'ONLINE'
);

INSERT INTO OFFERS (USER_ID, SKILL_ID, SKILL_LEVEL, SESSION_MODE)
VALUES (
    (SELECT USER_ID FROM USERS WHERE EMAIL = 'hira@skillswap.edu'),
    (SELECT SKILL_ID FROM SKILLS WHERE SKILL_NAME = 'Data Analysis'),
    'BEGINNER',
    'BOTH'
);

INSERT INTO OFFERS (USER_ID, SKILL_ID, SKILL_LEVEL, SESSION_MODE)
VALUES (
    (SELECT USER_ID FROM USERS WHERE EMAIL = 'imran@skillswap.edu'),
    (SELECT SKILL_ID FROM SKILLS WHERE SKILL_NAME = 'Project Planning'),
    'EXPERT',
    'ONLINE'
);

INSERT INTO OFFERS (USER_ID, SKILL_ID, SKILL_LEVEL, SESSION_MODE)
VALUES (
    (SELECT USER_ID FROM USERS WHERE EMAIL = 'isha@skillswap.edu'),
    (SELECT SKILL_ID FROM SKILLS WHERE SKILL_NAME = 'Java'),
    'BEGINNER',
    'ONLINE'
);

-- ============================================================
-- AVAILABILITY
-- ============================================================
-- Alice - Python
INSERT INTO AVAILABILITY (OFFER_ID, DAY_OF_WEEK, TIME_SLOT)
VALUES (
    (SELECT O.OFFER_ID
     FROM OFFERS O
     JOIN USERS U ON O.USER_ID = U.USER_ID
     JOIN SKILLS S ON O.SKILL_ID = S.SKILL_ID
     WHERE U.EMAIL = 'alice@skillswap.edu'
       AND S.SKILL_NAME = 'Python'),
    'MONDAY',
    'MORNING'
);

INSERT INTO AVAILABILITY (OFFER_ID, DAY_OF_WEEK, TIME_SLOT)
VALUES (
    (SELECT O.OFFER_ID
     FROM OFFERS O
     JOIN USERS U ON O.USER_ID = U.USER_ID
     JOIN SKILLS S ON O.SKILL_ID = S.SKILL_ID
     WHERE U.EMAIL = 'alice@skillswap.edu'
       AND S.SKILL_NAME = 'Python'),
    'WEDNESDAY',
    'AFTERNOON'
);

-- Alice - Figma
INSERT INTO AVAILABILITY (OFFER_ID, DAY_OF_WEEK, TIME_SLOT)
VALUES (
    (SELECT O.OFFER_ID
     FROM OFFERS O
     JOIN USERS U ON O.USER_ID = U.USER_ID
     JOIN SKILLS S ON O.SKILL_ID = S.SKILL_ID
     WHERE U.EMAIL = 'alice@skillswap.edu'
       AND S.SKILL_NAME = 'Figma'),
    'TUESDAY',
    'EVENING'
);

-- Bob - SQL
INSERT INTO AVAILABILITY (OFFER_ID, DAY_OF_WEEK, TIME_SLOT)
VALUES (
    (SELECT O.OFFER_ID
     FROM OFFERS O
     JOIN USERS U ON O.USER_ID = U.USER_ID
     JOIN SKILLS S ON O.SKILL_ID = S.SKILL_ID
     WHERE U.EMAIL = 'bob@skillswap.edu'
       AND S.SKILL_NAME = 'SQL'),
    'TUESDAY',
    'MORNING'
);

INSERT INTO AVAILABILITY (OFFER_ID, DAY_OF_WEEK, TIME_SLOT)
VALUES (
    (SELECT O.OFFER_ID
     FROM OFFERS O
     JOIN USERS U ON O.USER_ID = U.USER_ID
     JOIN SKILLS S ON O.SKILL_ID = S.SKILL_ID
     WHERE U.EMAIL = 'bob@skillswap.edu'
       AND S.SKILL_NAME = 'SQL'),
    'THURSDAY',
    'EVENING'
);

-- Bob - Machine Learning
INSERT INTO AVAILABILITY (OFFER_ID, DAY_OF_WEEK, TIME_SLOT)
VALUES (
    (SELECT O.OFFER_ID
     FROM OFFERS O
     JOIN USERS U ON O.USER_ID = U.USER_ID
     JOIN SKILLS S ON O.SKILL_ID = S.SKILL_ID
     WHERE U.EMAIL = 'bob@skillswap.edu'
       AND S.SKILL_NAME = 'Machine Learning'),
    'FRIDAY',
    'AFTERNOON'
);

-- Carol - MATLAB
INSERT INTO AVAILABILITY (OFFER_ID, DAY_OF_WEEK, TIME_SLOT)
VALUES (
    (SELECT O.OFFER_ID
     FROM OFFERS O
     JOIN USERS U ON O.USER_ID = U.USER_ID
     JOIN SKILLS S ON O.SKILL_ID = S.SKILL_ID
     WHERE U.EMAIL = 'carol@skillswap.edu'
       AND S.SKILL_NAME = 'MATLAB'),
    'MONDAY',
    'EVENING'
);

INSERT INTO AVAILABILITY (OFFER_ID, DAY_OF_WEEK, TIME_SLOT)
VALUES (
    (SELECT O.OFFER_ID
     FROM OFFERS O
     JOIN USERS U ON O.USER_ID = U.USER_ID
     JOIN SKILLS S ON O.SKILL_ID = S.SKILL_ID
     WHERE U.EMAIL = 'carol@skillswap.edu'
       AND S.SKILL_NAME = 'MATLAB'),
    'FRIDAY',
    'MORNING'
);

-- Carol - Arduino
INSERT INTO AVAILABILITY (OFFER_ID, DAY_OF_WEEK, TIME_SLOT)
VALUES (
    (SELECT O.OFFER_ID
     FROM OFFERS O
     JOIN USERS U ON O.USER_ID = U.USER_ID
     JOIN SKILLS S ON O.SKILL_ID = S.SKILL_ID
     WHERE U.EMAIL = 'carol@skillswap.edu'
       AND S.SKILL_NAME = 'Arduino'),
    'SATURDAY',
    'MORNING'
);

-- Dave - AutoCAD
INSERT INTO AVAILABILITY (OFFER_ID, DAY_OF_WEEK, TIME_SLOT)
VALUES (
    (SELECT O.OFFER_ID
     FROM OFFERS O
     JOIN USERS U ON O.USER_ID = U.USER_ID
     JOIN SKILLS S ON O.SKILL_ID = S.SKILL_ID
     WHERE U.EMAIL = 'dave@skillswap.edu'
       AND S.SKILL_NAME = 'AutoCAD'),
    'WEDNESDAY',
    'MORNING'
);

INSERT INTO AVAILABILITY (OFFER_ID, DAY_OF_WEEK, TIME_SLOT)
VALUES (
    (SELECT O.OFFER_ID
     FROM OFFERS O
     JOIN USERS U ON O.USER_ID = U.USER_ID
     JOIN SKILLS S ON O.SKILL_ID = S.SKILL_ID
     WHERE U.EMAIL = 'dave@skillswap.edu'
       AND S.SKILL_NAME = 'AutoCAD'),
    'THURSDAY',
    'AFTERNOON'
);

-- Dave - SolidWorks
INSERT INTO AVAILABILITY (OFFER_ID, DAY_OF_WEEK, TIME_SLOT)
VALUES (
    (SELECT O.OFFER_ID
     FROM OFFERS O
     JOIN USERS U ON O.USER_ID = U.USER_ID
     JOIN SKILLS S ON O.SKILL_ID = S.SKILL_ID
     WHERE U.EMAIL = 'dave@skillswap.edu'
       AND S.SKILL_NAME = 'SolidWorks'),
    'FRIDAY',
    'EVENING'
);

-- Elena - Public Speaking
INSERT INTO AVAILABILITY (OFFER_ID, DAY_OF_WEEK, TIME_SLOT)
VALUES (
    (SELECT O.OFFER_ID
     FROM OFFERS O
     JOIN USERS U ON O.USER_ID = U.USER_ID
     JOIN SKILLS S ON O.SKILL_ID = S.SKILL_ID
     WHERE U.EMAIL = 'elena@skillswap.edu'
       AND S.SKILL_NAME = 'Public Speaking'),
    'THURSDAY',
    'AFTERNOON'
);

INSERT INTO AVAILABILITY (OFFER_ID, DAY_OF_WEEK, TIME_SLOT)
VALUES (
    (SELECT O.OFFER_ID
     FROM OFFERS O
     JOIN USERS U ON O.USER_ID = U.USER_ID
     JOIN SKILLS S ON O.SKILL_ID = S.SKILL_ID
     WHERE U.EMAIL = 'elena@skillswap.edu'
       AND S.SKILL_NAME = 'Public Speaking'),
    'SATURDAY',
    'AFTERNOON'
);

-- Elena - Technical Writing
INSERT INTO AVAILABILITY (OFFER_ID, DAY_OF_WEEK, TIME_SLOT)
VALUES (
    (SELECT O.OFFER_ID
     FROM OFFERS O
     JOIN USERS U ON O.USER_ID = U.USER_ID
     JOIN SKILLS S ON O.SKILL_ID = S.SKILL_ID
     WHERE U.EMAIL = 'elena@skillswap.edu'
       AND S.SKILL_NAME = 'Technical Writing'),
    'MONDAY',
    'MORNING'
);

-- Farhan - C++
INSERT INTO AVAILABILITY (OFFER_ID, DAY_OF_WEEK, TIME_SLOT)
VALUES (
    (SELECT O.OFFER_ID
     FROM OFFERS O
     JOIN USERS U ON O.USER_ID = U.USER_ID
     JOIN SKILLS S ON O.SKILL_ID = S.SKILL_ID
     WHERE U.EMAIL = 'farhan@skillswap.edu'
       AND S.SKILL_NAME = 'C++'),
    'TUESDAY',
    'EVENING'
);

-- Hira - Data Analysis
INSERT INTO AVAILABILITY (OFFER_ID, DAY_OF_WEEK, TIME_SLOT)
VALUES (
    (SELECT O.OFFER_ID
     FROM OFFERS O
     JOIN USERS U ON O.USER_ID = U.USER_ID
     JOIN SKILLS S ON O.SKILL_ID = S.SKILL_ID
     WHERE U.EMAIL = 'hira@skillswap.edu'
       AND S.SKILL_NAME = 'Data Analysis'),
    'MONDAY',
    'AFTERNOON'
);

-- Imran - Project Planning
INSERT INTO AVAILABILITY (OFFER_ID, DAY_OF_WEEK, TIME_SLOT)
VALUES (
    (SELECT O.OFFER_ID
     FROM OFFERS O
     JOIN USERS U ON O.USER_ID = U.USER_ID
     JOIN SKILLS S ON O.SKILL_ID = S.SKILL_ID
     WHERE U.EMAIL = 'imran@skillswap.edu'
       AND S.SKILL_NAME = 'Project Planning'),
    'WEDNESDAY',
    'EVENING'
);

-- Isha - Java
INSERT INTO AVAILABILITY (OFFER_ID, DAY_OF_WEEK, TIME_SLOT)
VALUES (
    (SELECT O.OFFER_ID
     FROM OFFERS O
     JOIN USERS U ON O.USER_ID = U.USER_ID
     JOIN SKILLS S ON O.SKILL_ID = S.SKILL_ID
     WHERE U.EMAIL = 'isha@skillswap.edu'
       AND S.SKILL_NAME = 'Java'),
    'SATURDAY',
    'EVENING'
);

-- ============================================================
-- REQUESTS (initially pending)
-- ============================================================
-- Bob requests Alice's Python
INSERT INTO REQUESTS (
    USER_ID,
    SKILL_ID,
    OFFER_ID,
    SELECTED_AVAILABILITY_ID,
    URGENCY,
    NOTE,
    STATUS
)
VALUES (
    (SELECT USER_ID FROM USERS WHERE EMAIL = 'bob@skillswap.edu'),
    (SELECT SKILL_ID FROM SKILLS WHERE SKILL_NAME = 'Python'),
    (SELECT O.OFFER_ID
     FROM OFFERS O
     JOIN USERS U ON O.USER_ID = U.USER_ID
     JOIN SKILLS S ON O.SKILL_ID = S.SKILL_ID
     WHERE U.EMAIL = 'alice@skillswap.edu'
       AND S.SKILL_NAME = 'Python'),
    (SELECT A.AVAILABILITY_ID
     FROM AVAILABILITY A
     JOIN OFFERS O ON A.OFFER_ID = O.OFFER_ID
     JOIN USERS U ON O.USER_ID = U.USER_ID
     JOIN SKILLS S ON O.SKILL_ID = S.SKILL_ID
     WHERE U.EMAIL = 'alice@skillswap.edu'
       AND S.SKILL_NAME = 'Python'
       AND A.DAY_OF_WEEK = 'MONDAY'
       AND A.TIME_SLOT = 'MORNING'),
    'MEDIUM',
    'Need help preparing for my programming assignment.',
    'PENDING'
);

-- Hira requests Alice's Figma
INSERT INTO REQUESTS (
    USER_ID,
    SKILL_ID,
    OFFER_ID,
    SELECTED_AVAILABILITY_ID,
    URGENCY,
    NOTE,
    STATUS
)
VALUES (
    (SELECT USER_ID FROM USERS WHERE EMAIL = 'hira@skillswap.edu'),
    (SELECT SKILL_ID FROM SKILLS WHERE SKILL_NAME = 'Figma'),
    (SELECT O.OFFER_ID
     FROM OFFERS O
     JOIN USERS U ON O.USER_ID = U.USER_ID
     JOIN SKILLS S ON O.SKILL_ID = S.SKILL_ID
     WHERE U.EMAIL = 'alice@skillswap.edu'
       AND S.SKILL_NAME = 'Figma'),
    (SELECT A.AVAILABILITY_ID
     FROM AVAILABILITY A
     JOIN OFFERS O ON A.OFFER_ID = O.OFFER_ID
     JOIN USERS U ON O.USER_ID = U.USER_ID
     JOIN SKILLS S ON O.SKILL_ID = S.SKILL_ID
     WHERE U.EMAIL = 'alice@skillswap.edu'
       AND S.SKILL_NAME = 'Figma'
       AND A.DAY_OF_WEEK = 'TUESDAY'
       AND A.TIME_SLOT = 'EVENING'),
    'HIGH',
    'Need quick UI help for a class project.',
    'PENDING'
);

-- Dave requests Bob's SQL
INSERT INTO REQUESTS (
    USER_ID,
    SKILL_ID,
    OFFER_ID,
    SELECTED_AVAILABILITY_ID,
    URGENCY,
    NOTE,
    STATUS
)
VALUES (
    (SELECT USER_ID FROM USERS WHERE EMAIL = 'dave@skillswap.edu'),
    (SELECT SKILL_ID FROM SKILLS WHERE SKILL_NAME = 'SQL'),
    (SELECT O.OFFER_ID
     FROM OFFERS O
     JOIN USERS U ON O.USER_ID = U.USER_ID
     JOIN SKILLS S ON O.SKILL_ID = S.SKILL_ID
     WHERE U.EMAIL = 'bob@skillswap.edu'
       AND S.SKILL_NAME = 'SQL'),
    (SELECT A.AVAILABILITY_ID
     FROM AVAILABILITY A
     JOIN OFFERS O ON A.OFFER_ID = O.OFFER_ID
     JOIN USERS U ON O.USER_ID = U.USER_ID
     JOIN SKILLS S ON O.SKILL_ID = S.SKILL_ID
     WHERE U.EMAIL = 'bob@skillswap.edu'
       AND S.SKILL_NAME = 'SQL'
       AND A.DAY_OF_WEEK = 'TUESDAY'
       AND A.TIME_SLOT = 'MORNING'),
    'LOW',
    'Just want a short revision session.',
    'PENDING'
);

-- Isha requests Carol's Arduino
INSERT INTO REQUESTS (
    USER_ID,
    SKILL_ID,
    OFFER_ID,
    SELECTED_AVAILABILITY_ID,
    URGENCY,
    NOTE,
    STATUS
)
VALUES (
    (SELECT USER_ID FROM USERS WHERE EMAIL = 'isha@skillswap.edu'),
    (SELECT SKILL_ID FROM SKILLS WHERE SKILL_NAME = 'Arduino'),
    (SELECT O.OFFER_ID
     FROM OFFERS O
     JOIN USERS U ON O.USER_ID = U.USER_ID
     JOIN SKILLS S ON O.SKILL_ID = S.SKILL_ID
     WHERE U.EMAIL = 'carol@skillswap.edu'
       AND S.SKILL_NAME = 'Arduino'),
    (SELECT A.AVAILABILITY_ID
     FROM AVAILABILITY A
     JOIN OFFERS O ON A.OFFER_ID = O.OFFER_ID
     JOIN USERS U ON O.USER_ID = U.USER_ID
     JOIN SKILLS S ON O.SKILL_ID = S.SKILL_ID
     WHERE U.EMAIL = 'carol@skillswap.edu'
       AND S.SKILL_NAME = 'Arduino'
       AND A.DAY_OF_WEEK = 'SATURDAY'
       AND A.TIME_SLOT = 'MORNING'),
    'MEDIUM',
    'Need help with a small embedded systems task.',
    'PENDING'
);

-- Pending requests
INSERT INTO REQUESTS (
    USER_ID,
    SKILL_ID,
    OFFER_ID,
    SELECTED_AVAILABILITY_ID,
    URGENCY,
    NOTE,
    STATUS
)
VALUES (
    (SELECT USER_ID FROM USERS WHERE EMAIL = 'carol@skillswap.edu'),
    (SELECT SKILL_ID FROM SKILLS WHERE SKILL_NAME = 'Machine Learning'),
    (SELECT O.OFFER_ID
     FROM OFFERS O
     JOIN USERS U ON O.USER_ID = U.USER_ID
     JOIN SKILLS S ON O.SKILL_ID = S.SKILL_ID
     WHERE U.EMAIL = 'bob@skillswap.edu'
       AND S.SKILL_NAME = 'Machine Learning'),
    (SELECT A.AVAILABILITY_ID
     FROM AVAILABILITY A
     JOIN OFFERS O ON A.OFFER_ID = O.OFFER_ID
     JOIN USERS U ON O.USER_ID = U.USER_ID
     JOIN SKILLS S ON O.SKILL_ID = S.SKILL_ID
     WHERE U.EMAIL = 'bob@skillswap.edu'
       AND S.SKILL_NAME = 'Machine Learning'
       AND A.DAY_OF_WEEK = 'FRIDAY'
       AND A.TIME_SLOT = 'AFTERNOON'),
    'HIGH',
    'Need ML basics for semester project.',
    'PENDING'
);

INSERT INTO REQUESTS (
    USER_ID,
    SKILL_ID,
    OFFER_ID,
    SELECTED_AVAILABILITY_ID,
    URGENCY,
    NOTE,
    STATUS
)
VALUES (
    (SELECT USER_ID FROM USERS WHERE EMAIL = 'elena@skillswap.edu'),
    (SELECT SKILL_ID FROM SKILLS WHERE SKILL_NAME = 'AutoCAD'),
    (SELECT O.OFFER_ID
     FROM OFFERS O
     JOIN USERS U ON O.USER_ID = U.USER_ID
     JOIN SKILLS S ON O.SKILL_ID = S.SKILL_ID
     WHERE U.EMAIL = 'dave@skillswap.edu'
       AND S.SKILL_NAME = 'AutoCAD'),
    (SELECT A.AVAILABILITY_ID
     FROM AVAILABILITY A
     JOIN OFFERS O ON A.OFFER_ID = O.OFFER_ID
     JOIN USERS U ON O.USER_ID = U.USER_ID
     JOIN SKILLS S ON O.SKILL_ID = S.SKILL_ID
     WHERE U.EMAIL = 'dave@skillswap.edu'
       AND S.SKILL_NAME = 'AutoCAD'
       AND A.DAY_OF_WEEK = 'WEDNESDAY'
       AND A.TIME_SLOT = 'MORNING'),
    'HIGH',
    'Need help preparing drawings.',
    'PENDING'
);

INSERT INTO REQUESTS (
    USER_ID,
    SKILL_ID,
    OFFER_ID,
    SELECTED_AVAILABILITY_ID,
    URGENCY,
    NOTE,
    STATUS
)
VALUES (
    (SELECT USER_ID FROM USERS WHERE EMAIL = 'farhan@skillswap.edu'),
    (SELECT SKILL_ID FROM SKILLS WHERE SKILL_NAME = 'Public Speaking'),
    (SELECT O.OFFER_ID
     FROM OFFERS O
     JOIN USERS U ON O.USER_ID = U.USER_ID
     JOIN SKILLS S ON O.SKILL_ID = S.SKILL_ID
     WHERE U.EMAIL = 'elena@skillswap.edu'
       AND S.SKILL_NAME = 'Public Speaking'),
    (SELECT A.AVAILABILITY_ID
     FROM AVAILABILITY A
     JOIN OFFERS O ON A.OFFER_ID = O.OFFER_ID
     JOIN USERS U ON O.USER_ID = U.USER_ID
     JOIN SKILLS S ON O.SKILL_ID = S.SKILL_ID
     WHERE U.EMAIL = 'elena@skillswap.edu'
       AND S.SKILL_NAME = 'Public Speaking'
       AND A.DAY_OF_WEEK = 'THURSDAY'
       AND A.TIME_SLOT = 'AFTERNOON'),
    'LOW',
    'Need practice for a presentation.',
    'PENDING'
);

INSERT INTO REQUESTS (
    USER_ID,
    SKILL_ID,
    OFFER_ID,
    SELECTED_AVAILABILITY_ID,
    URGENCY,
    NOTE,
    STATUS
)
VALUES (
    (SELECT USER_ID FROM USERS WHERE EMAIL = 'imran@skillswap.edu'),
    (SELECT SKILL_ID FROM SKILLS WHERE SKILL_NAME = 'MATLAB'),
    (SELECT O.OFFER_ID
     FROM OFFERS O
     JOIN USERS U ON O.USER_ID = U.USER_ID
     JOIN SKILLS S ON O.SKILL_ID = S.SKILL_ID
     WHERE U.EMAIL = 'carol@skillswap.edu'
       AND S.SKILL_NAME = 'MATLAB'),
    (SELECT A.AVAILABILITY_ID
     FROM AVAILABILITY A
     JOIN OFFERS O ON A.OFFER_ID = O.OFFER_ID
     JOIN USERS U ON O.USER_ID = U.USER_ID
     JOIN SKILLS S ON O.SKILL_ID = S.SKILL_ID
     WHERE U.EMAIL = 'carol@skillswap.edu'
       AND S.SKILL_NAME = 'MATLAB'
       AND A.DAY_OF_WEEK = 'MONDAY'
       AND A.TIME_SLOT = 'EVENING'),
    'MEDIUM',
    'Need MATLAB help for circuits lab.',
    'PENDING'
);

INSERT INTO REQUESTS (
    USER_ID,
    SKILL_ID,
    OFFER_ID,
    SELECTED_AVAILABILITY_ID,
    URGENCY,
    NOTE,
    STATUS
)
VALUES (
    (SELECT USER_ID FROM USERS WHERE EMAIL = 'alice@skillswap.edu'),
    (SELECT SKILL_ID FROM SKILLS WHERE SKILL_NAME = 'Arduino'),
    (SELECT O.OFFER_ID
     FROM OFFERS O
     JOIN USERS U ON O.USER_ID = U.USER_ID
     JOIN SKILLS S ON O.SKILL_ID = S.SKILL_ID
     WHERE U.EMAIL = 'carol@skillswap.edu'
       AND S.SKILL_NAME = 'Arduino'),
    (SELECT A.AVAILABILITY_ID
     FROM AVAILABILITY A
     JOIN OFFERS O ON A.OFFER_ID = O.OFFER_ID
     JOIN USERS U ON O.USER_ID = U.USER_ID
     JOIN SKILLS S ON O.SKILL_ID = S.SKILL_ID
     WHERE U.EMAIL = 'carol@skillswap.edu'
       AND S.SKILL_NAME = 'Arduino'
       AND A.DAY_OF_WEEK = 'SATURDAY'
       AND A.TIME_SLOT = 'MORNING'),
    'MEDIUM',
    'Need Arduino help for a small prototype.',
    'PENDING'
);

-- ============================================================
-- ACCEPT SOME REQUESTS (fires MATCH notifications)
-- ============================================================
UPDATE REQUESTS
SET STATUS = 'ACCEPTED'
WHERE USER_ID = (SELECT USER_ID FROM USERS WHERE EMAIL = 'bob@skillswap.edu')
  AND SKILL_ID = (SELECT SKILL_ID FROM SKILLS WHERE SKILL_NAME = 'Python');

UPDATE REQUESTS
SET STATUS = 'ACCEPTED'
WHERE USER_ID = (SELECT USER_ID FROM USERS WHERE EMAIL = 'hira@skillswap.edu')
  AND SKILL_ID = (SELECT SKILL_ID FROM SKILLS WHERE SKILL_NAME = 'Figma');

UPDATE REQUESTS
SET STATUS = 'ACCEPTED'
WHERE USER_ID = (SELECT USER_ID FROM USERS WHERE EMAIL = 'dave@skillswap.edu')
  AND SKILL_ID = (SELECT SKILL_ID FROM SKILLS WHERE SKILL_NAME = 'SQL');

UPDATE REQUESTS
SET STATUS = 'ACCEPTED'
WHERE USER_ID = (SELECT USER_ID FROM USERS WHERE EMAIL = 'isha@skillswap.edu')
  AND SKILL_ID = (SELECT SKILL_ID FROM SKILLS WHERE SKILL_NAME = 'Arduino');

-- ============================================================
-- SESSIONS
-- ============================================================
-- Bob <-> Alice (completed)
INSERT INTO SESSIONS (
    OFFER_ID,
    REQUEST_ID,
    SESSION_DATE,
    MEETING_DETAIL,
    STATUS,
    REQUESTER_CONFIRMED,
    OFFERER_CONFIRMED
)
VALUES (
    (SELECT O.OFFER_ID
     FROM OFFERS O
     JOIN USERS U ON O.USER_ID = U.USER_ID
     JOIN SKILLS S ON O.SKILL_ID = S.SKILL_ID
     WHERE U.EMAIL = 'alice@skillswap.edu'
       AND S.SKILL_NAME = 'Python'),
    (SELECT REQUEST_ID
     FROM REQUESTS
     WHERE USER_ID = (SELECT USER_ID FROM USERS WHERE EMAIL = 'bob@skillswap.edu')
       AND SKILL_ID = (SELECT SKILL_ID FROM SKILLS WHERE SKILL_NAME = 'Python')),
    SYSDATE - 2,
    'Zoom',
    'SCHEDULED',
    1,
    1
);

-- Hira <-> Alice (completed)
INSERT INTO SESSIONS (
    OFFER_ID,
    REQUEST_ID,
    SESSION_DATE,
    MEETING_DETAIL,
    STATUS,
    REQUESTER_CONFIRMED,
    OFFERER_CONFIRMED
)
VALUES (
    (SELECT O.OFFER_ID
     FROM OFFERS O
     JOIN USERS U ON O.USER_ID = U.USER_ID
     JOIN SKILLS S ON O.SKILL_ID = S.SKILL_ID
     WHERE U.EMAIL = 'alice@skillswap.edu'
       AND S.SKILL_NAME = 'Figma'),
    (SELECT REQUEST_ID
     FROM REQUESTS
     WHERE USER_ID = (SELECT USER_ID FROM USERS WHERE EMAIL = 'hira@skillswap.edu')
       AND SKILL_ID = (SELECT SKILL_ID FROM SKILLS WHERE SKILL_NAME = 'Figma')),
    SYSDATE - 1,
    'Zoom',
    'SCHEDULED',
    1,
    1
);

-- Dave <-> Bob (scheduled, not completed yet)
INSERT INTO SESSIONS (
    OFFER_ID,
    REQUEST_ID,
    SESSION_DATE,
    MEETING_DETAIL,
    STATUS,
    REQUESTER_CONFIRMED,
    OFFERER_CONFIRMED
)
VALUES (
    (SELECT O.OFFER_ID
     FROM OFFERS O
     JOIN USERS U ON O.USER_ID = U.USER_ID
     JOIN SKILLS S ON O.SKILL_ID = S.SKILL_ID
     WHERE U.EMAIL = 'bob@skillswap.edu'
       AND S.SKILL_NAME = 'SQL'),
    (SELECT REQUEST_ID
     FROM REQUESTS
     WHERE USER_ID = (SELECT USER_ID FROM USERS WHERE EMAIL = 'dave@skillswap.edu')
       AND SKILL_ID = (SELECT SKILL_ID FROM SKILLS WHERE SKILL_NAME = 'SQL')),
    SYSDATE + 1,
    'Google Meet',
    'SCHEDULED',
    1,
    0
);

-- Isha <-> Carol (completed)
INSERT INTO SESSIONS (
    OFFER_ID,
    REQUEST_ID,
    SESSION_DATE,
    MEETING_DETAIL,
    STATUS,
    REQUESTER_CONFIRMED,
    OFFERER_CONFIRMED
)
VALUES (
    (SELECT O.OFFER_ID
     FROM OFFERS O
     JOIN USERS U ON O.USER_ID = U.USER_ID
     JOIN SKILLS S ON O.SKILL_ID = S.SKILL_ID
     WHERE U.EMAIL = 'carol@skillswap.edu'
       AND S.SKILL_NAME = 'Arduino'),
    (SELECT REQUEST_ID
     FROM REQUESTS
     WHERE USER_ID = (SELECT USER_ID FROM USERS WHERE EMAIL = 'isha@skillswap.edu')
       AND SKILL_ID = (SELECT SKILL_ID FROM SKILLS WHERE SKILL_NAME = 'Arduino')),
    SYSDATE - 1,
    'Lab 4',
    'SCHEDULED',
    1,
    1
);

-- ============================================================
-- FEEDBACK (allowed only for completed sessions)
-- ============================================================
INSERT INTO FEEDBACK (SESSION_ID, SCORE, FEEDBACK_TEXT)
VALUES (
    (SELECT SESSION_ID
     FROM SESSIONS
     WHERE REQUEST_ID = (
         SELECT REQUEST_ID
         FROM REQUESTS
         WHERE USER_ID = (SELECT USER_ID FROM USERS WHERE EMAIL = 'bob@skillswap.edu')
           AND SKILL_ID = (SELECT SKILL_ID FROM SKILLS WHERE SKILL_NAME = 'Python')
     )),
    5,
    'Very clear explanations and great pacing.'
);

INSERT INTO FEEDBACK (SESSION_ID, SCORE, FEEDBACK_TEXT)
VALUES (
    (SELECT SESSION_ID
     FROM SESSIONS
     WHERE REQUEST_ID = (
         SELECT REQUEST_ID
         FROM REQUESTS
         WHERE USER_ID = (SELECT USER_ID FROM USERS WHERE EMAIL = 'hira@skillswap.edu')
           AND SKILL_ID = (SELECT SKILL_ID FROM SKILLS WHERE SKILL_NAME = 'Figma')
     )),
    4,
    'Helped me understand the UI workflow well.'
);

INSERT INTO FEEDBACK (SESSION_ID, SCORE, FEEDBACK_TEXT)
VALUES (
    (SELECT SESSION_ID
     FROM SESSIONS
     WHERE REQUEST_ID = (
         SELECT REQUEST_ID
         FROM REQUESTS
         WHERE USER_ID = (SELECT USER_ID FROM USERS WHERE EMAIL = 'isha@skillswap.edu')
           AND SKILL_ID = (SELECT SKILL_ID FROM SKILLS WHERE SKILL_NAME = 'Arduino')
     )),
    5,
    'Explained the Arduino wiring and code very clearly.'
);

-- ============================================================
-- ENDORSEMENTS
-- ============================================================
INSERT INTO ENDORSEMENTS (
    ENDORSED_USER_ID,
    ENDORSED_BY_ID,
    SKILL_ID,
    NOTE
)
VALUES (
    (SELECT USER_ID FROM USERS WHERE EMAIL = 'alice@skillswap.edu'),
    (SELECT USER_ID FROM USERS WHERE EMAIL = 'bob@skillswap.edu'),
    (SELECT SKILL_ID FROM SKILLS WHERE SKILL_NAME = 'Python'),
    'Great at explaining Python basics.'
);

INSERT INTO ENDORSEMENTS (
    ENDORSED_USER_ID,
    ENDORSED_BY_ID,
    SKILL_ID,
    NOTE
)
VALUES (
    (SELECT USER_ID FROM USERS WHERE EMAIL = 'alice@skillswap.edu'),
    (SELECT USER_ID FROM USERS WHERE EMAIL = 'hira@skillswap.edu'),
    (SELECT SKILL_ID FROM SKILLS WHERE SKILL_NAME = 'Figma'),
    'Very helpful for UI design tasks.'
);

INSERT INTO ENDORSEMENTS (
    ENDORSED_USER_ID,
    ENDORSED_BY_ID,
    SKILL_ID,
    NOTE
)
VALUES (
    (SELECT USER_ID FROM USERS WHERE EMAIL = 'carol@skillswap.edu'),
    (SELECT USER_ID FROM USERS WHERE EMAIL = 'isha@skillswap.edu'),
    (SELECT SKILL_ID FROM SKILLS WHERE SKILL_NAME = 'Arduino'),
    'Strong practical understanding of Arduino setups.'
);

-- ============================================================
-- MESSAGES
-- ============================================================
-- Bob <-> Alice (completed session)
INSERT INTO MESSAGES (SESSION_ID, SENDER_ID, CONTENT, IS_READ)
VALUES (
    (SELECT SESSION_ID
     FROM SESSIONS
     WHERE REQUEST_ID = (
         SELECT REQUEST_ID
         FROM REQUESTS
         WHERE USER_ID = (SELECT USER_ID FROM USERS WHERE EMAIL = 'bob@skillswap.edu')
           AND SKILL_ID = (SELECT SKILL_ID FROM SKILLS WHERE SKILL_NAME = 'Python')
     )),
    (SELECT USER_ID FROM USERS WHERE EMAIL = 'bob@skillswap.edu'),
    'Thanks for the Python session. It was really helpful.',
    0
);

INSERT INTO MESSAGES (SESSION_ID, SENDER_ID, CONTENT, IS_READ)
VALUES (
    (SELECT SESSION_ID
     FROM SESSIONS
     WHERE REQUEST_ID = (
         SELECT REQUEST_ID
         FROM REQUESTS
         WHERE USER_ID = (SELECT USER_ID FROM USERS WHERE EMAIL = 'bob@skillswap.edu')
           AND SKILL_ID = (SELECT SKILL_ID FROM SKILLS WHERE SKILL_NAME = 'Python')
     )),
    (SELECT USER_ID FROM USERS WHERE EMAIL = 'alice@skillswap.edu'),
    'Glad it helped. Keep practicing the examples.',
    0
);

-- Hira <-> Alice (completed session)
INSERT INTO MESSAGES (SESSION_ID, SENDER_ID, CONTENT, IS_READ)
VALUES (
    (SELECT SESSION_ID
     FROM SESSIONS
     WHERE REQUEST_ID = (
         SELECT REQUEST_ID
         FROM REQUESTS
         WHERE USER_ID = (SELECT USER_ID FROM USERS WHERE EMAIL = 'hira@skillswap.edu')
           AND SKILL_ID = (SELECT SKILL_ID FROM SKILLS WHERE SKILL_NAME = 'Figma')
     )),
    (SELECT USER_ID FROM USERS WHERE EMAIL = 'hira@skillswap.edu'),
    'Your Figma tips saved me a lot of time.',
    0
);

INSERT INTO MESSAGES (SESSION_ID, SENDER_ID, CONTENT, IS_READ)
VALUES (
    (SELECT SESSION_ID
     FROM SESSIONS
     WHERE REQUEST_ID = (
         SELECT REQUEST_ID
         FROM REQUESTS
         WHERE USER_ID = (SELECT USER_ID FROM USERS WHERE EMAIL = 'hira@skillswap.edu')
           AND SKILL_ID = (SELECT SKILL_ID FROM SKILLS WHERE SKILL_NAME = 'Figma')
     )),
    (SELECT USER_ID FROM USERS WHERE EMAIL = 'alice@skillswap.edu'),
    'Any time. Good luck with your project.',
    0
);

-- Dave <-> Bob (scheduled session)
INSERT INTO MESSAGES (SESSION_ID, SENDER_ID, CONTENT, IS_READ)
VALUES (
    (SELECT SESSION_ID
     FROM SESSIONS
     WHERE REQUEST_ID = (
         SELECT REQUEST_ID
         FROM REQUESTS
         WHERE USER_ID = (SELECT USER_ID FROM USERS WHERE EMAIL = 'dave@skillswap.edu')
           AND SKILL_ID = (SELECT SKILL_ID FROM SKILLS WHERE SKILL_NAME = 'SQL')
     )),
    (SELECT USER_ID FROM USERS WHERE EMAIL = 'dave@skillswap.edu'),
    'Looking forward to the SQL session tomorrow.',
    0
);

-- Isha <-> Carol (completed session)
INSERT INTO MESSAGES (SESSION_ID, SENDER_ID, CONTENT, IS_READ)
VALUES (
    (SELECT SESSION_ID
     FROM SESSIONS
     WHERE REQUEST_ID = (
         SELECT REQUEST_ID
         FROM REQUESTS
         WHERE USER_ID = (SELECT USER_ID FROM USERS WHERE EMAIL = 'isha@skillswap.edu')
           AND SKILL_ID = (SELECT SKILL_ID FROM SKILLS WHERE SKILL_NAME = 'Arduino')
     )),
    (SELECT USER_ID FROM USERS WHERE EMAIL = 'isha@skillswap.edu'),
    'Thanks, the wiring part is much clearer now.',
    0
);

INSERT INTO MESSAGES (SESSION_ID, SENDER_ID, CONTENT, IS_READ)
VALUES (
    (SELECT SESSION_ID
     FROM SESSIONS
     WHERE REQUEST_ID = (
         SELECT REQUEST_ID
         FROM REQUESTS
         WHERE USER_ID = (SELECT USER_ID FROM USERS WHERE EMAIL = 'isha@skillswap.edu')
           AND SKILL_ID = (SELECT SKILL_ID FROM SKILLS WHERE SKILL_NAME = 'Arduino')
     )),
    (SELECT USER_ID FROM USERS WHERE EMAIL = 'carol@skillswap.edu'),
    'Happy to help. Keep building projects.',
    0
);

-- ============================================================
-- COMPLETED REQUEST UPDATES
-- ============================================================
UPDATE REQUESTS
SET STATUS = 'COMPLETED'
WHERE USER_ID = (SELECT USER_ID FROM USERS WHERE EMAIL = 'bob@skillswap.edu')
  AND SKILL_ID = (SELECT SKILL_ID FROM SKILLS WHERE SKILL_NAME = 'Python');

UPDATE REQUESTS
SET STATUS = 'COMPLETED'
WHERE USER_ID = (SELECT USER_ID FROM USERS WHERE EMAIL = 'hira@skillswap.edu')
  AND SKILL_ID = (SELECT SKILL_ID FROM SKILLS WHERE SKILL_NAME = 'Figma');

UPDATE REQUESTS
SET STATUS = 'COMPLETED'
WHERE USER_ID = (SELECT USER_ID FROM USERS WHERE EMAIL = 'isha@skillswap.edu')
  AND SKILL_ID = (SELECT SKILL_ID FROM SKILLS WHERE SKILL_NAME = 'Arduino');

COMMIT;
