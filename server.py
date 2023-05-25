from flask import Flask, render_template, request
import subprocess
import os
import platform
from PyPaperBot.proxy import proxy
from flask import send_file
import shutil
import tempfile

# Define the default download directory based on the operating system
if platform.system() == 'Windows':
    dwn_dir = os.path.join(os.path.expanduser("~"), 'Downloads')
else:
    dwn_dir = '/tmp'


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

    # Change to PyPaperBot directory
    os.chdir('PyPaperBot')

    # Run PyPaperBot with form data
    print(f"Running PyPaperBot with query: {query}, scholar_pages: {pages}, min_year: {min_year}, dwn_dir: {dwn_dir}, scihub_mirror: {scihub_mirror}")
    result = subprocess.call(['python', '-m', 'PyPaperBot', f'--query={query}', f'--scholar-pages={pages}', f'--min-year={min_year}', f'--dwn-dir={dwn_dir}', f'--scihub-mirror={scihub_mirror}'])
    print(f"Result of PyPaperBot call: {result}")

    # Return to home directory
    os.chdir('..')

    # Print all files in the directory
    all_files = os.listdir(dwn_dir)
    print(f"All files: {all_files}")

    # Create the files list
    files = [os.path.join(dwn_dir, filename) for filename in all_files if filename.endswith('.pdf') and query in filename]

    # Print the files list
    print(f"PDF files: {files}")

    # Create a temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"Temporary directory: {temp_dir}")

        # Copy the PDF files to the temporary directory
        for file in files:
            shutil.copy(file, temp_dir)
            print(f"Copied {file} to {temp_dir}")

    # Return the path to the first PDF file for download
    if files:
        return send_file(files[0], as_attachment=True)
    else:
        return 'No PDF files found.'

@app.route('/downloadzip')
def download_zip():
    return 'This endpoint is no longer available.'

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
