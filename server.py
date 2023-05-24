from flask import Flask, render_template, request
import subprocess
import os
import platform

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    # Get form data
    query = request.form['query']
    profile = request.form['profile']

    # Map profile to scholar_pages and min_year
    profile_map = {
        'Daniel Rodrigo Mode': {'scholar_pages': '5', 'min_year': '1945'},
        'Leti Sala Mode': {'scholar_pages': '3', 'min_year': '1995'},
        'Robles Mode': {'scholar_pages': '1', 'min_year': '2015'},
    }

    pages = profile_map[profile]['scholar_pages']
    min_year = profile_map[profile]['min_year']
    
    # Sci-Hub mirror is hardcoded
    scihub_mirror = 'https://sci-hub.st'

    # Define the default download directory based on the operating system
    if platform.system() == 'Windows':
        dwn_dir = os.path.join(os.path.expanduser("~"), 'Downloads')
    else:
        dwn_dir = os.path.expanduser("~/Downloads")

    # Change to PyPaperBot directory
    os.chdir('PyPaperBot')

    # Run PyPaperBot with form data
    subprocess.call(['python', '-m', 'PyPaperBot', f'--query={query}', f'--scholar-pages={pages}', f'--min-year={min_year}', f'--dwn-dir={dwn_dir}', f'--scihub-mirror={scihub_mirror}'])

    # Return to home directory
    os.chdir('..')

    return 'Search completed! Check your download directory.'

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
