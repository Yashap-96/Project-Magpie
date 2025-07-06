# Project Magpie 🐦

## Overview

Project Magpie is a personalized, autonomous AI research assistant. It automatically scans arXiv.org for the latest academic papers in specific fields of AI, uses a local Large Language Model (Llama 3) to generate both brief and detailed analytical summaries, and presents them in a searchable, user-friendly web interface built with Flask.

The goal of this project is to automate the process of staying on the cutting-edge of AI research, transforming information overload into actionable intelligence.

## Key Features

* **Autonomous Fetching:** A `cron`-scheduled backend agent runs daily to fetch new papers from arXiv's AI categories (`cs.AI`, `cs.CL`).
* **Intelligent Summarization:** Uses a locally-run Llama 3 8B model via Ollama to perform two levels of summarization:
    * A brief, 3-bullet-point summary for quick scanning.
    * A detailed, analytical digest based on the full text of the paper.
* **Persistent Storage:** All processed papers and their summaries are stored in a local **SQLite** database, which prevents duplicate processing.
* **Dynamic Web Interface:** A **Flask** application serves a clean, user-friendly UI to view daily digests and detailed paper analyses.
* **Search Functionality:** The web interface includes a search feature to query the entire database of saved papers by keyword.

## Tech Stack

* **Backend:** Python
* **Web Framework:** Flask
* **Database:** SQLite
* **Local LLM Service:** Ollama (running Llama 3 8B)
* **Core Libraries:** `ollama`, `arxiv`, `requests`, `PyMuPDF`
* **Automation:** `cron` (on macOS)

## Setup and Usage

1.  **Clone the Repository:**
    ```bash
    git clone [Your-Repo-URL]
    cd Project-Magpie
    ```
2.  **Create and Activate Virtual Environment:**
    ```bash
    python -m venv .venv
    source .venv/bin/activate
    ```
3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Run Ollama:** Ensure the Ollama application is running and that you have downloaded the Llama 3 8B model:
    ```bash
    ollama run llama3:8b
    ```
5.  **Set up the Database:** Run the setup script once to create the database file.
    ```bash
    python database_setup.py
    ```
6.  **Run the Backend Agent (Optional):** To populate the database with the latest papers, run the main agent.
    ```bash
    python main.py
    ```
7.  **Run the Web Application:**
    ```bash
    flask run
    ```
8.  Open your browser and navigate to `http://127.0.0.1:5000`.# Project-Magpie
