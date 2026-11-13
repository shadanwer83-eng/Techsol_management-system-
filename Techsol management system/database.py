"""
Database Module for Techsol Student Management System
Handles SQLite database operations: Initialization, CRUD, Search, and Analytics.
"""

import sqlite3
import os
from datetime import datetime

DB_NAME = "techsol_students.db"


def get_db_path():
    """Returns absolute path to the database file in current script directory."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, DB_NAME)


def get_connection():
    """Creates and returns a SQLite database connection with row factory."""
    conn = sqlite3.connect(get_db_path())
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """
    Initializes the database schema and seeds initial sample records
    if the table is newly created.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            student_id TEXT PRIMARY KEY,
            student_name TEXT NOT NULL,
            student_course TEXT NOT NULL,
            student_fees REAL NOT NULL,
            student_dues_fees REAL NOT NULL,
            student_paid_fees REAL NOT NULL,
            student_contact TEXT DEFAULT '',
            student_email TEXT DEFAULT '',
            enrollment_date TEXT DEFAULT ''
        )
    """)
    conn.commit()

    # Check if empty; if so, populate with clean realistic demo records
    cursor.execute("SELECT COUNT(*) FROM students")
    count = cursor.fetchone()[0]

    if count == 0:
        sample_students = [
            ("TS-1001", "Aarav Sharma", "Python Full Stack", 45000.0, 5000.0, 40000.0, "+91 98765 43210", "aarav.sharma@example.com", "2026-01-15"),
            ("TS-1002", "Priya Patel", "Data Science & AI", 55000.0, 0.0, 55000.0, "+91 98123 45678", "priya.patel@example.com", "2026-02-01"),
            ("TS-1003", "Rohan Mehta", "Cloud Computing & DevOps", 50000.0, 15000.0, 35000.0, "+91 97654 32109", "rohan.mehta@example.com", "2026-02-10"),
            ("TS-1004", "Ananya Verma", "Web Development (MERN)", 40000.0, 0.0, 40000.0, "+91 99887 76655", "ananya.v@example.com", "2026-02-20"),
            ("TS-1005", "Karan Malhotra", "Cyber Security", 48000.0, 12000.0, 36000.0, "+91 96543 21876", "karan.m@example.com", "2026-03-05")
        ]
        cursor.executemany("""
            INSERT INTO students (
                student_id, student_name, student_course, student_fees,
                student_dues_fees, student_paid_fees, student_contact,
                student_email, enrollment_date
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, sample_students)
        conn.commit()

    conn.close()


def add_student(student_id, name, course, fees, dues_fees, contact="", email="", enrollment_date=None):
    """
    Inserts a new student record into database.
    Calculates paid fees as (fees - dues_fees).
    """
    student_id = student_id.strip()
    name = name.strip()
    course = course.strip()
    contact = contact.strip()
    email = email.strip()

    if not enrollment_date:
        enrollment_date = datetime.now().strftime("%Y-%m-%d")

    fees = float(fees)
    dues_fees = float(dues_fees)
    paid_fees = fees - dues_fees

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO students (
                student_id, student_name, student_course, student_fees,
                student_dues_fees, student_paid_fees, student_contact,
                student_email, enrollment_date
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (student_id, name, course, fees, dues_fees, paid_fees, contact, email, enrollment_date))
        conn.commit()
        return True, "Student added successfully."
    except sqlite3.IntegrityError:
        return False, f"Student ID '{student_id}' already exists in database. Please use a unique ID."
    except Exception as e:
        return False, f"Database error: {str(e)}"
    finally:
        conn.close()


def update_student(student_id, name, course, fees, dues_fees, contact="", email="", enrollment_date=None):
    """
    Updates an existing student's details.
    """
    student_id = student_id.strip()
    name = name.strip()
    course = course.strip()
    contact = contact.strip()
    email = email.strip()

    fees = float(fees)
    dues_fees = float(dues_fees)
    paid_fees = fees - dues_fees

    conn = get_connection()
    cursor = conn.cursor()

    try:
        # Check if student exists
        cursor.execute("SELECT student_id FROM students WHERE student_id = ?", (student_id,))
        if not cursor.fetchone():
            return False, f"Student with ID '{student_id}' does not exist."

        if enrollment_date:
            cursor.execute("""
                UPDATE students SET
                    student_name = ?,
                    student_course = ?,
                    student_fees = ?,
                    student_dues_fees = ?,
                    student_paid_fees = ?,
                    student_contact = ?,
                    student_email = ?,
                    enrollment_date = ?
                WHERE student_id = ?
            """, (name, course, fees, dues_fees, paid_fees, contact, email, enrollment_date, student_id))
        else:
            cursor.execute("""
                UPDATE students SET
                    student_name = ?,
                    student_course = ?,
                    student_fees = ?,
                    student_dues_fees = ?,
                    student_paid_fees = ?,
                    student_contact = ?,
                    student_email = ?
                WHERE student_id = ?
            """, (name, course, fees, dues_fees, paid_fees, contact, email, student_id))

        conn.commit()
        return True, "Student updated successfully."
    except Exception as e:
        return False, f"Database error: {str(e)}"
    finally:
        conn.close()


def delete_student(student_id):
    """
    Deletes a student record by ID.
    """
    student_id = student_id.strip()
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("DELETE FROM students WHERE student_id = ?", (student_id,))
        if cursor.rowcount == 0:
            return False, f"No student found with ID '{student_id}'."
        conn.commit()
        return True, f"Student '{student_id}' deleted successfully."
    except Exception as e:
        return False, f"Database error: {str(e)}"
    finally:
        conn.close()


def get_all_students(order_by="student_id"):
    """
    Returns list of all students sorted by student_id or specified column.
    """
    valid_cols = ["student_id", "student_name", "student_course", "student_fees", "student_dues_fees", "student_paid_fees", "enrollment_date"]
    if order_by not in valid_cols:
        order_by = "student_id"

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM students ORDER BY {order_by} ASC")
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_student_by_id(student_id):
    """
    Fetches a single student record by ID.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE student_id = ?", (student_id.strip(),))
    row = cursor.fetchone()
    conn.close()
    return row


def search_students(query="", search_by="All", status_filter="All"):
    """
    Searches and filters students based on search string and filter criteria.
    """
    conn = get_connection()
    cursor = conn.cursor()

    sql = "SELECT * FROM students WHERE 1=1"
    params = []

    q = f"%{query.strip()}%"
    if query.strip():
        if search_by == "Student ID":
            sql += " AND student_id LIKE ?"
            params.append(q)
        elif search_by == "Student Name":
            sql += " AND student_name LIKE ?"
            params.append(q)
        elif search_by == "Course":
            sql += " AND student_course LIKE ?"
            params.append(q)
        else:  # All columns
            sql += " AND (student_id LIKE ? OR student_name LIKE ? OR student_course LIKE ? OR student_contact LIKE ?)"
            params.extend([q, q, q, q])

    if status_filter == "With Dues":
        sql += " AND student_dues_fees > 0"
    elif status_filter == "Fully Paid":
        sql += " AND student_dues_fees == 0"

    sql += " ORDER BY student_id ASC"

    cursor.execute(sql, params)
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_statistics():
    """
    Computes dashboard analytics:
    - Total students
    - Total fees registered
    - Total paid/collected fees
    - Total dues pending
    - Count with dues / fully paid
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            COUNT(*) AS total_students,
            COALESCE(SUM(student_fees), 0) AS total_fees,
            COALESCE(SUM(student_paid_fees), 0) AS total_paid,
            COALESCE(SUM(student_dues_fees), 0) AS total_dues,
            SUM(CASE WHEN student_dues_fees > 0 THEN 1 ELSE 0 END) AS students_with_dues,
            SUM(CASE WHEN student_dues_fees == 0 THEN 1 ELSE 0 END) AS students_fully_paid
        FROM students
    """)
    stats = cursor.fetchone()

    # Get course distribution
    cursor.execute("""
        SELECT student_course, COUNT(*) as count 
        FROM students 
        GROUP BY student_course 
        ORDER BY count DESC
    """)
    course_stats = cursor.fetchall()

    conn.close()

    return {
        "total_students": stats["total_students"] or 0,
        "total_fees": float(stats["total_fees"] or 0.0),
        "total_paid": float(stats["total_paid"] or 0.0),
        "total_dues": float(stats["total_dues"] or 0.0),
        "students_with_dues": stats["students_with_dues"] or 0,
        "students_fully_paid": stats["students_fully_paid"] or 0,
        "course_distribution": [(row["student_course"], row["count"]) for row in course_stats]
    }


def get_next_student_id():
    """
    Generates the next logical Student ID, e.g., TS-1006.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT student_id FROM students WHERE student_id LIKE 'TS-%'")
    rows = cursor.fetchall()
    conn.close()

    highest_num = 1000
    for row in rows:
        val = row["student_id"]
        try:
            parts = val.split("-")
            if len(parts) == 2 and parts[1].isdigit():
                num = int(parts[1])
                if num > highest_num:
                    highest_num = num
        except Exception:
            continue

    return f"TS-{highest_num + 1}"
