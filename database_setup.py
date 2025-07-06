import sqlite3
from pathlib import Path

# Define the absolute path to the project directory
SCRIPT_DIR = Path(__file__).parent.resolve()
DB_NAME = 'magpie.db'
DB_FILE = SCRIPT_DIR / DB_NAME

# Connect to the database (this will create the file if it doesn't exist)
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

# Create the 'papers' table with all required columns
# The "IF NOT EXISTS" clause prevents errors if the script is run multiple times.
cursor.execute('''
CREATE TABLE IF NOT EXISTS papers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    published_date TEXT,
    authors TEXT,
    summary TEXT,
    pdf_url TEXT UNIQUE,
    ai_summary TEXT,
    detailed_summary TEXT,
    fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

# Commit the changes and close the connection
conn.commit()
conn.close()

print(f"Database '{DB_NAME}' and table 'papers' created successfully at '{DB_FILE}'")