import sqlite3

# --- Database Connection ---
def db_connect():
    """Create a database connection to the SQLite database."""
    conn = sqlite3.connect('job_applications.db')
    return conn

# --- Insert Functions ---
def insert_company(company_name, industry, location, website, notes):
    """Insert a new company into the Companies table."""
    conn = db_connect()
    cursor = conn.cursor()
    cursor.execute('''
            INSERT INTO Companies (CompanyName, Industry, Location, Website, Notes)
            VALUES (?, ?, ?, ?, ?)''', (company_name, industry, location, website, notes))
    conn.commit()
    conn.close()

def insert_job_application(company_id, position, date_applied, status, follow_up_date, response_received, notes):
    """Insert a new job application into the JobApplications table."""
    conn = db_connect()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO JobApplications (CompanyID, Position, DateApplied, Status, FollowUpDate, ResponseReceived, Notes)
        VALUES (?, ?, ?, ?, ?, ?, ?)''', (company_id, position, date_applied, status, follow_up_date, response_received, notes))
    conn.commit()
    conn.close()

def insert_contact(company_id, name, position, email, phone, notes):
    """Insert a new contact into the Contacts table."""
    conn = db_connect()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO Contacts (CompanyID, Name, Position, Email, Phone, Notes)
        VALUES (?, ?, ?, ?, ?, ?)''', (company_id, name, position, email, phone, notes))
    conn.commit()
    conn.close()

# --- Query Functions ---
def get_all_companies():
    """Query all rows in the Companies table."""
    conn = db_connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Companies")
    companies = cursor.fetchall()
    conn.close()
    return companies

def get_all_job_applications():
    """Query all rows in the JobApplications table."""
    conn = db_connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM JobApplications")
    applications = cursor.fetchall()
    conn.close()
    return applications

def get_all_contacts():
    """Query all rows in the Contacts table."""
    conn = db_connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Contacts")
    contacts = cursor.fetchall()
    conn.close()
    return contacts

# --- Update Functions ---
def update_application_status(application_id, new_status):
    """Update the status of a job application."""
    conn = db_connect()
    cursor = conn.cursor()
    cursor.execute("UPDATE JobApplications SET Status = ? WHERE ApplicationID = ?", (new_status, application_id))
    conn.commit()
    conn.close()

# --- Delete Functions ---
def delete_job_application(application_id):
    """Delete a job application by ApplicationID."""
    conn = db_connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM JobApplications WHERE ApplicationID = ?", (application_id,))
    conn.commit()
    conn.close()

def delete_company(company_id):
    """Delete a company by CompanyID."""
    conn = db_connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Companies WHERE CompanyID = ?", (company_id,))
    conn.commit()
    conn.close()

def delete_contact(contact_id):
    """Delete a contact by ContactID."""
    conn = db_connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Contacts WHERE ContactID = ?", (contact_id,))
    conn.commit()
    conn.close()

import datetime
def check_follow_ups():
    """Check and notify about job applications that need follow-up."""
    conn = db_connect()
    cursor = conn.cursor()
    cursor.execute("SELECT ApplicationID, Position, CompanyID, FollowUpDate FROM JobApplications WHERE FollowUpDate <= ?", (datetime.date.today(),))
    due_follow_ups = cursor.fetchall()
    for app in due_follow_ups:
        print(f"Follow up on application {app[0]} for position {app[1]} at company ID {app[2]}.")
    conn.close()

def update_follow_up_date(application_id, new_date):
    conn = db_connect()
    cursor = conn.cursor()
    cursor.execute("UPDATE JobApplications SET FollowUpDate = ? WHERE ApplicationID = ?", (new_date, application_id))
    conn.commit()
    conn.close()

def check_record_exists(record_id, table):
    conn = db_connect()
    cursor = conn.cursor()
    query = f"SELECT EXISTS(SELECT 1 FROM {table} WHERE ApplicationID=? LIMIT 1)"
    cursor.execute(query, (record_id,))
    exists = cursor.fetchone()[0]
    conn.close()
    return exists
