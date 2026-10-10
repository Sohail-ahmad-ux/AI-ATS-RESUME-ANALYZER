import sqlite3
from pathlib import Path

# ------------------------------------
# Database Configuration
# ------------------------------------

Path("database").mkdir(exist_ok=True)

DATABASE = "database/ats.db"


# ------------------------------------
# Connection
# ------------------------------------

def get_connection():
    return sqlite3.connect(DATABASE)


# ------------------------------------
# Create Table
# ------------------------------------

def create_table():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS candidates(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        candidate_name TEXT,

        ats_score REAL,

        recommendation TEXT,

        matched_skills TEXT,

        missing_skills TEXT,

        feedback TEXT,

        interview_questions TEXT,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)

    conn.commit()

    conn.close()


# ------------------------------------
# Save Candidate
# ------------------------------------

def save_candidate(result):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO candidates(

            candidate_name,

            ats_score,

            recommendation,

            matched_skills,

            missing_skills,

            feedback,

            interview_questions

        )

        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (

            result.get("candidate_name"),

            result.get("overall_score"),

            result.get("recommendation"),

            ", ".join(result.get("matched_skills", [])),

            ", ".join(result.get("missing_skills", [])),

            result.get("feedback"),

            str(result.get("interview_questions"))

        )
    )

    conn.commit()

    conn.close()


# ------------------------------------
# Get Candidates
# ------------------------------------

def get_candidates():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

        SELECT *

        FROM candidates

        ORDER BY ats_score DESC

    """)

    rows = cursor.fetchall()

    conn.close()

    return rows


# ------------------------------------
# Search Candidate
# ------------------------------------

def search_candidate(name):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

        SELECT *

        FROM candidates

        WHERE candidate_name LIKE ?

    """, (f"%{name}%",))

    rows = cursor.fetchall()

    conn.close()

    return rows


# ------------------------------------
# Delete Candidate
# ------------------------------------

def delete_candidate(candidate_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(

        "DELETE FROM candidates WHERE id=?",

        (candidate_id,)

    )

    conn.commit()

    conn.close()

def get_dashboard_stats():

    conn = get_connection()

    cursor = conn.cursor()

    # Total Candidates
    cursor.execute("SELECT COUNT(*) FROM candidates")
    total = cursor.fetchone()[0]

    # Average ATS Score
    cursor.execute("SELECT AVG(ats_score) FROM candidates")
    avg_score = cursor.fetchone()[0] or 0

    # Strong Fit
    cursor.execute("""
        SELECT COUNT(*)
        FROM candidates
        WHERE recommendation='Strong Fit'
    """)
    strong = cursor.fetchone()[0]

    # Moderate Fit
    cursor.execute("""
        SELECT COUNT(*)
        FROM candidates
        WHERE recommendation='Moderate Fit'
    """)
    moderate = cursor.fetchone()[0]

    # Weak Fit
    cursor.execute("""
        SELECT COUNT(*)
        FROM candidates
        WHERE recommendation='Weak Fit'
    """)
    weak = cursor.fetchone()[0]

    conn.close()

    return {

        "total": total,

        "average": round(avg_score,2),

        "strong": strong,

        "moderate": moderate,

        "weak": weak

    }


def filter_candidates(recommendation):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

        SELECT *

        FROM candidates

        WHERE recommendation=?

        ORDER BY ats_score DESC

    """,(recommendation,))

    rows = cursor.fetchall()

    conn.close()

    return rows


def sort_candidates(order="DESC"):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(f"""

        SELECT *

        FROM candidates

        ORDER BY ats_score {order}

    """)

    rows = cursor.fetchall()

    conn.close()

    return rows   

def delete_candidate(candidate_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM candidates WHERE id=?",
        (candidate_id,)
    )

    conn.commit()

    conn.close() 