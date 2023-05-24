import subprocess
import shlex

def execute_pypaperbot_query(query, scholar_pages, min_year, download_dir, scihub_mirror):
    command = f'python -m PyPaperBot --query="{query}" --scholar-pages={scholar_pages} --min-year={min_year} --dwn-dir="{download_dir}" --scihub-mirror="{scihub_mirror}"'
    try:
        completed_process = subprocess.run(shlex.split(command), check=True, capture_output=True, text=True)
        print(completed_process.stdout)
    except subprocess.CalledProcessError as e:
        print(e.stderr)

# Example usage: python testapp.py "Machine learning" 3 2018 "C:\User\example\papers" "https://sci-hub.do"
if __name__ == '__main__':
    import sys
    if len(sys.argv) < 6:
        print("Insufficient arguments.")
        print("Usage: python testapp.py <query> <scholar_pages> <min_year> <download_dir> <scihub_mirror>")
    else:
        query = sys.argv[1]
        scholar_pages = sys.argv[2]
        min_year = sys.argv[3]
        download_dir = sys.argv[4]
        scihub_mirror = sys.argv[5]
        execute_pypaperbot_query(query, scholar_pages, min_year, download_dir, scihub_mirror)
