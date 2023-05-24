from flask import Flask, render_template, request, jsonify
import subprocess
import appdirs
import os
import shlex
import requests


app = Flask(__name__, template_folder='templates')

@app.route('/')
def index():
    progress_log = get_progress_log()
    query = get_query()
    mode = get_mode()
    scholar_pages = get_scholar_pages()
    min_year = get_min_year()

    return render_template('index.html', progress_log=progress_log, query=query, mode=mode, scholar_pages=scholar_pages, min_year=min_year)


def get_progress_log():
    # Replace with your code to retrieve the search progress log
    progress_log = "Log not available"
    return progress_log

def get_query():
    # Replace with your code to retrieve the current query
    query = "Query not available"
    return query

def get_mode():
    # Replace with your code to retrieve the current mode
    mode = "Mode not available"
    return mode

def get_scholar_pages():
    # Replace with your code to retrieve the scholar pages setting
    scholar_pages = "Scholar pages not available"
    return scholar_pages

def get_min_year():
    # Replace with your code to retrieve the min year setting
    min_year = "Min year not available"
    return min_year

@app.route('/search', methods=['POST'])
def search():
    data = request.get_json()
    query = data['query']
    mode = data['mode']

    # Obtain the user's default download folder from the user profile
    dwn_dir = get_browser_downloads_folder()

    # Modify the command to include the default download folder based on the mode
    if mode == 'daniel_rodrigo':
        command = f'python -m PyPaperBot --query="{query}" --scholar-pages=3 --min-year=1965 --dwn-dir="{dwn_dir}"'
    elif mode == 'leti_sala':
        command = f'python -m PyPaperBot --query="{query}" --scholar-pages=5 --min-year=2000 --dwn-dir="{dwn_dir}"'
    elif mode == 'robles':
        command = f'python -m PyPaperBot --query="{query}" --scholar-pages=1 --min-year=2016 --dwn-dir="{dwn_dir}"'
    else:
        return jsonify({'message': 'Invalid mode'})

    try:
        completed_process = subprocess.run(shlex.split(command), check=True, capture_output=True, text=True)
        response = {'message': 'Search successful'}
    except subprocess.CalledProcessError as e:
        response = {'message': 'Search failed', 'error': e.stderr}
        print(e.stderr)
    print(completed_process.stdout)
    print(completed_process.stderr)

    return jsonify(response)


def get_browser_downloads_folder():
    # Return the path to the browser's downloads folder
    return os.path.expanduser("~/Downloads")

if __name__ == '__main__':
    app.run(port=8000)
