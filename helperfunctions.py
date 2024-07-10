import streamlit as st
import sqlite3
import hashlib
import pandas as pd
from datetime import date
import streamlit_authenticator as stauth
from io import BytesIO
import pyotp
import qrcode
import base64
import io

def hash_password(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_company_exists():
    conn = sqlite3.connect('hr_system.db')
    c = conn.cursor()
    c.execute("SELECT * FROM Companies")
    result = c.fetchone()
    conn.close()
    return result is not None

def register_company(company_name):
    conn = sqlite3.connect('hr_system.db')
    c = conn.cursor()
    try:
        c.execute("INSERT INTO Companies (company_name) VALUES (?)", (company_name,))
        company_id = c.lastrowid
        conn.commit()
        return company_id
    except sqlite3.IntegrityError:
        return None
    finally:
        conn.close()

def get_companies():
    conn = sqlite3.connect('hr_system.db')
    c = conn.cursor()
    c.execute("SELECT company_id, company_name FROM Companies")
    companies = c.fetchall()
    conn.close()
    return companies

def get_users_by_company(company_id):
    conn = sqlite3.connect('hr_system.db')
    c = conn.cursor()
    c.execute("SELECT username FROM Users WHERE company_id = ?", (company_id,))
    users = c.fetchall()
    conn.close()
    return [user[0] for user in users]

def insert_employee_request(username, name, employee_id, job_title, leave_days, from_date, to_date, leave_type, reason, main_type,
                            Appointment_from_date=None, Appointment_to_date=None, sick_from_date=None, sick_to_date=None,
                            appointment_letter_PDF=None, sick_letter_PDF=None, other_reason=None):
    try:
        conn = sqlite3.connect('hr_system.db')
        c = conn.cursor()

        # Convert file objects to binary data if they exist
        if appointment_letter_PDF:
            appointment_letter_PDF = appointment_letter_PDF.read() if hasattr(appointment_letter_PDF, 'read') else appointment_letter_PDF
        if sick_letter_PDF:
            sick_letter_PDF = sick_letter_PDF.read() if hasattr(sick_letter_PDF, 'read') else sick_letter_PDF

        c.execute("""
                  INSERT INTO Employees_Requests (
                    Username, Name, Employee_id, Job_title, Leave_request_days, from_date, to_date, 
                    Type_of_leave, Reason, main_type, Appointment_from_date, Appointment_to_date, 
                    sick_from_date, sick_to_date, appointment_letter_PDF, sick_letter_PDF, other_reason
                  ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                  """,(username, name, employee_id, job_title, leave_days, from_date, to_date, leave_type, 
                  reason, main_type, Appointment_from_date, Appointment_to_date, sick_from_date, 
                  sick_to_date, appointment_letter_PDF, sick_letter_PDF, other_reason))

        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return False
    finally:
        conn.close()

def fetch_all_employee_requests():
    conn = sqlite3.connect('hr_system.db')
    c = conn.cursor()
    c.execute(""" SELECT *
              FROM Employees_Requests """)
    rows = c.fetchall()
    conn.close()
    return rows

def get_leave_status(employee_id, from_date, to_date, leave_type):
    conn = sqlite3.connect('hr_system.db')
    c = conn.cursor()
    c.execute("SELECT Leave_status FROM Leave_Status WHERE Employee_id = ? AND from_date = ? AND to_date = ? AND leave_type = ?", (employee_id, from_date, to_date, leave_type))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None

def insert_leave_status(username, name, employee_id, leave_status, from_date, to_date, leave_type):
    conn = sqlite3.connect('hr_system.db')
    c = conn.cursor()
    c.execute("INSERT INTO Leave_Status (Username, Name, Employee_id, Leave_status, from_date, to_date, leave_type) VALUES (?, ?, ?, ?, ?, ?, ?)",
              (username, name, employee_id, leave_status, from_date, to_date, leave_type))
    conn.commit()
    conn.close()

def get_companies():
    conn = sqlite3.connect('hr_system.db')
    c = conn.cursor()
    c.execute("SELECT company_id, company_name FROM Companies")
    companies = c.fetchall()
    conn.close()
    return companies

def get_employee_username_by_hr_username(hr_username):
    conn = sqlite3.connect('hr_system.db')
    c = conn.cursor()
    c.execute("SELECT username FROM Users WHERE company_id = (SELECT company_id FROM HR_Managers WHERE username = ?)", (hr_username,))
    results = c.fetchall()
    conn.close()
    return [result[0] for result in results] if results else []

def fetch_all_employee_requests_under_me(hr_username):
    conn = sqlite3.connect('hr_system.db')
    c = conn.cursor()
    c.execute("SELECT * FROM Employees_Requests WHERE Username IN (SELECT username FROM Users WHERE company_id = (SELECT company_id FROM HR_Managers WHERE username = ?))", (hr_username,))
    rows = c.fetchall()
    conn.close()
    return rows

def get_user_email_by_username(username):
    conn = sqlite3.connect('hr_system.db')
    c = conn.cursor()
    c.execute("SELECT user_email FROM Users WHERE username = ?", (username,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None

def get_hr_email_by_employee_username(employee_username):
    conn = sqlite3.connect('hr_system.db')
    c = conn.cursor()
    c.execute("""
        SELECT HR_Managers.hr_email 
        FROM HR_Managers 
        JOIN Users ON HR_Managers.company_id = Users.company_id 
        WHERE Users.username = ?
    """, (employee_username,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None

def generate_otp_secret():
    return pyotp.random_base32()

def generate_otp_uri(secret, username, issuer_name="HR Management System"):
    return pyotp.totp.TOTP(secret).provisioning_uri(name=username, issuer_name=issuer_name)

def generate_qr_code(uri):
    qr = qrcode.QRCode(version=1, box_size=5, border=5)
    qr.add_data(uri)
    qr.make(fit=True)
    back_color_rgb = tuple(int("f7f8f9"[i:i+2], 16) for i in (0, 2, 4))
    img = qr.make_image(fill_color="black", back_color = back_color_rgb)
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

def verify_otp(secret, otp):
    totp = pyotp.TOTP(secret)
    return totp.verify(otp)

def register_hr(username, password, company_id, hr_email):
    conn = sqlite3.connect('hr_system.db')
    c = conn.cursor()
    try:
        otp_secret = generate_otp_secret()
        c.execute("INSERT INTO HR_Managers (username, password, company_id, hr_email, otp_secret) VALUES (?, ?, ?, ?, ?)",
                  (username, hash_password(password), company_id, hr_email, otp_secret))
        conn.commit()
        return otp_secret
    except sqlite3.IntegrityError:
        return None
    finally:
        conn.close()

def register_user(username, password, company_id, user_email):
    conn = sqlite3.connect('hr_system.db')
    c = conn.cursor()
    try:
        otp_secret = generate_otp_secret()
        c.execute("INSERT INTO Users (username, password, company_id, user_email, otp_secret) VALUES (?, ?, ?, ?, ?)",
                  (username, hash_password(password), company_id, user_email, otp_secret))
        conn.commit()
        return otp_secret
    except sqlite3.IntegrityError:
        return None
    finally:
        conn.close()

def login_hr(username, password):
    conn = sqlite3.connect('hr_system.db')
    c = conn.cursor()
    c.execute("SELECT otp_secret FROM HR_Managers WHERE username = ? AND password = ?",
              (username, hash_password(password)))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None

def login_user(username, password):
    conn = sqlite3.connect('hr_system.db')
    c = conn.cursor()
    c.execute("SELECT otp_secret FROM Users WHERE username = ? AND password = ?",
              (username, hash_password(password)))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None