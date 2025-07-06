import sqlite3
import ollama
import arxiv
from datetime import datetime, date
import logging
from pathlib import Path
import requests
import fitz
import time
import os
from dotenv import load_dotenv
import google.generativeai as genai

# # Load variables from the .env file
# load_dotenv()

# # ... (logging and path setup) ...

# # --- NEW: Securely load the API key ---
# API_KEY = os.getenv("GEMINI_API_KEY")

# # Check if the key was found
# if not API_KEY:
#     raise ValueError("Gemini API key not found. Make sure you have a .env file with GEMINI_API_KEY set.")

# # Configure the API
# genai.configure(api_key=API_KEY)
# model = genai.GenerativeModel('gemini-2.0-flash')

# --- Setup ---
SCRIPT_DIR = Path(__file__).parent.resolve()
LOG_FILE = SCRIPT_DIR / 'magpie.log'
DB_FILE = SCRIPT_DIR / 'magpie.db'
HTML_DIR = SCRIPT_DIR / 'templates'
HTML_DIR.mkdir(exist_ok=True)
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Database Functions ---
def paper_exists(cursor, pdf_url):
    cursor.execute("SELECT 1 FROM papers WHERE pdf_url = ?", (pdf_url,))
    return cursor.fetchone() is not None

def insert_paper(cursor, paper_data):
    cursor.execute('''
    INSERT INTO papers (title, published_date, authors, summary, pdf_url, ai_summary, detailed_summary)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        paper_data['Title'], paper_data['Published Date'], paper_data['Authors'],
        paper_data['Summary'], paper_data['PDF URL'], paper_data['AI Summary'],
        paper_data['Detailed Summary']
    ))

# --- PDF Processing Function ---
def download_and_extract_text(pdf_url):
    try:
        response = requests.get(pdf_url, timeout=30)
        response.raise_for_status()
        logging.info(f"Successfully downloaded PDF: {pdf_url}")
        with fitz.open(stream=response.content, filetype="pdf") as doc:
            return "".join(page.get_text() for page in doc)
    except Exception as e:
        logging.error(f"Failed to download or process PDF from {pdf_url}. Error: {e}")
        return None

# --- Ollama Summarization Functions ---
def generate_brief_summary(abstract):
    """Generates a brief, 3-point summary using the local Llama 3 model."""
    prompt = f"Summarize the following abstract in 3 bullet points: {abstract}"
    try:
        response = ollama.chat(model='llama3:8b', messages=[{'role': 'user', 'content': prompt}])
        return response['message']['content']
    except Exception as e:
        logging.error(f"Ollama brief summary generation failed: {e}")
        return "Error generating brief summary from local model."

def generate_detailed_summary(full_text):
    """Generates the analytical digest using the local Llama 3 model."""
    if not full_text:
        return "Could not generate detailed summary because PDF text was not available."
    prompt = f"""
    You are an expert research analyst... PAPER TEXT: {full_text[:8000]}
    """ # Abridged for brevity
    try:
        response = ollama.chat(model='llama3:8b', messages=[{'role': 'user', 'content': prompt}])
        return response['message']['content']
    except Exception as e:
        logging.error(f"Ollama detailed summary failed: {e}")
        return "Error generating detailed summary from local model."

# --- Main Execution Logic ---
def main():
    start_time = time.time()
    logging.info("================ Project Magpie Run Start (using Llama 3) ================")
    conn = None
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        query = '(cat:cs.AI OR cat:cs.CL) AND ("Intelligent Agents" OR "Autonomous Agents" OR "LLM" OR "AGENTIC")'
        search = arxiv.Search(query=query, max_results=6, sort_by=arxiv.SortCriterion.SubmittedDate)
        client = arxiv.Client()
        new_papers_found = 0
        for result in client.results(search):
            if paper_exists(cursor, result.pdf_url):
                logging.info(f"Skipping already existing paper: {result.title}")
                continue
            
            new_papers_found += 1
            logging.info(f"Processing new paper: {result.title}")
            full_text = download_and_extract_text(result.pdf_url)

            # --- CORRECTED LOGIC ---
            # Call our new functions for both summaries
            brief_summary = generate_brief_summary(result.summary)
            detailed_summary = generate_detailed_summary(full_text)
            # --- END OF CORRECTION ---
            
            paper_data = {
                "Title": result.title, "Published Date": result.published.strftime('%Y-%m-%d'),
                "Authors": ', '.join([author.name for author in result.authors]), "Summary": result.summary,
                "PDF URL": result.pdf_url, "AI Summary": brief_summary, "Detailed Summary": detailed_summary
            }
            insert_paper(cursor, paper_data)
        
        conn.commit()
        logging.info(f"Run complete. Added {new_papers_found} new papers to the database.")
    except Exception as e:
        logging.error(f"An error occurred: {e}", exc_info=True)
    finally:
        if conn: conn.close()
        duration = time.time() - start_time
        logging.info(f"Total execution time: {duration:.2f} seconds.")
        logging.info("================= Project Magpie Run End =================\n")

if __name__ == "__main__":
    main()