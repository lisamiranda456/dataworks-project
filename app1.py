import os
import requests
import subprocess
from flask import Flask, request

app = Flask(__name__)

def task_A1(user_email):
    """Download and run datagen.py from the provided URL with user email."""
    import requests, subprocess

    url = "https://raw.githubusercontent.com/sanand0/tools-in-data-science-public/tds-2025-01/project-1/datagen.py"
    
    # Download datagen.py
    response = requests.get(url)
    if response.status_code != 200:
        return f"Failed to download datagen.py: HTTP {response.status_code}", 500
    
    with open("datagen.py", "w") as f:
        f.write(response.text)
    
    # Ensure ./data exists instead of using /data (which needs admin permissions)
    local_data_dir = os.path.abspath("./data")
    os.makedirs(local_data_dir, exist_ok=True)  # Create local data directory

    # Run datagen.py with the correct root directory
    result = subprocess.run(
        ["python", "datagen.py", user_email, "--root", local_data_dir], 
        capture_output=True, text=True
    )
    
    if result.returncode != 0:
        return f"Error running datagen.py: {result.stderr}", 500
    
    return result.stdout or "datagen.py executed successfully", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
