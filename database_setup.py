import sqlite3

conn = sqlite3.connect('job_applications.db')

cursor = conn.cursor()

# Create Companies Table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Companies (
    CompanyID INTEGER PRIMARY KEY AUTOINCREMENT,
    CompanyName TEXT NOT NULL,
    Industry TEXT,
    Location TEXT,
    Website TEXT,
    Notes TEXT
);
''')

# Create JobApplications Table
cursor.execute('''
CREATE TABLE IF NOT EXISTS JobApplications (
    ApplicationID INTEGER PRIMARY KEY AUTOINCREMENT,
    CompanyID INTEGER,
    Position TEXT NOT NULL,
    DateApplied TEXT,
    Status TEXT,
    FollowUpDate TEXT,
    ResponseReceived BOOLEAN,
    Notes TEXT,
    FOREIGN KEY (CompanyID) REFERENCES Companies(CompanyID)
);
''')

# Create Contacts Table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Contacts (
    ContactID INTEGER PRIMARY KEY AUTOINCREMENT,
    CompanyID INTEGER,
    Name TEXT NOT NULL,
    Position TEXT,
    Email TEXT,
    Phone TEXT,
    Notes TEXT,
    FOREIGN KEY (CompanyID) REFERENCES Companies(CompanyID)
);
''')

# Commit changes
conn.commit()

# Close connection
conn.close()

print("Database and tables created successfully!")