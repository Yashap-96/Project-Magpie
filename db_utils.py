# db_utils.py
import sqlite3
from pathlib import Path
from datetime import date

SCRIPT_DIR = Path(__file__).parent.resolve()
DB_FILE = SCRIPT_DIR / 'magpie.db'

def get_db_connection():
    """Establishes a connection to the database."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row # This allows us to access columns by name
    return conn

# Replace the old function in db_utils.py with this new one

def get_todays_papers():
    """Fetches the 10 most recent papers from the database."""
    conn = get_db_connection()
    # This new query is simpler and avoids timezone issues by just getting the latest papers.
    papers = conn.execute(
        "SELECT * FROM papers ORDER BY fetched_at DESC LIMIT 10"
    ).fetchall()
    conn.close()
    return papers

def get_paper_by_id(paper_id):
    """Fetches a single paper by its ID."""
    conn = get_db_connection()
    paper = conn.execute("SELECT * FROM papers WHERE id = ?", (paper_id,)).fetchone()
    conn.close()
    return paper

# Add this new function to db_utils.py

def search_papers(query):
    """Searches for papers with a query matching the title or summary."""
    conn = get_db_connection()
    # The '%' are wildcards, so it finds the query anywhere in the text.
    search_query = f'%{query}%'
    papers = conn.execute(
        "SELECT * FROM papers WHERE title LIKE ? OR summary LIKE ? OR detailed_summary LIKE ? ORDER BY published_date DESC",
        (search_query, search_query, search_query)
    ).fetchall()
    conn.close()
    return papers