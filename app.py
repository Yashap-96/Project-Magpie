# app.py (with search)
from flask import Flask, render_template, request
from db_utils import get_todays_papers, get_paper_by_id, search_papers # Import our new functions

app = Flask(__name__)

@app.route('/')
def homepage():
    """Renders the homepage with a list of today's papers."""
    papers = get_todays_papers()
    return render_template('digest.html', papers=papers)

@app.route('/paper/<int:paper_id>')
def paper_detail(paper_id):
    """Renders the detailed view for a single paper."""
    paper = get_paper_by_id(paper_id)
    return render_template('paper_detail.html', paper=paper)

# --- NEW: This route handles search queries ---
@app.route('/search')
def search():
    """Handles search requests and displays results."""
    # Get the search query from the URL parameters (e.g., /search?q=...)
    query = request.args.get('q', '')
    # Use our new function to search the database
    papers = search_papers(query)
    # Render a new template to display the results
    return render_template('search_results.html', papers=papers, query=query)

if __name__ == '__main__':
    app.run(debug=True)