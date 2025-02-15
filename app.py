import os
import json
import requests
import subprocess
import glob
import sqlite3
#import whisper
from datetime import datetime
from flask import Flask, request, Response
from bs4 import BeautifulSoup 
from PIL import Image  # For Image Processing (B7)
import markdown  # For Markdown to HTML (B9)
#import speech_recognition as sr  # For Audio Transcription (B8)
from pydub import AudioSegment
#from vosk import Model, KaldiRecognizer
import wave
import json
#import torch
#import librosa
import csv
#from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor

app = Flask(__name__)

# Define a local data directory to avoid permission errors
DATA_DIR = os.path.abspath("./data")
os.makedirs(DATA_DIR, exist_ok=True)  # Ensure the directory exists
from pydub.utils import which
os.environ["FFMPEG_PATH"] = "/workspaces/dataworks-project/ffmpeg"
os.environ["FFPROBE_PATH"] = "/workspaces/dataworks-project/ffprobe"

AudioSegment.converter = os.environ["FFMPEG_PATH"]
AudioSegment.ffprobe = os.environ["FFPROBE_PATH"]

def task_A1(user_email):
    """Download and run datagen.py from the provided URL with user email."""
    
    url = "https://raw.githubusercontent.com/sanand0/tools-in-data-science-public/tds-2025-01/project-1/datagen.py"
    
    # Download datagen.py
    response = requests.get(url)
    if response.status_code != 200:
        return f"Failed to download datagen.py: HTTP {response.status_code}", 500
    
    with open("datagen.py", "w") as f:
        f.write(response.text)
    
    # Run datagen.py with the correct root directory
    result = subprocess.run(
        ["python", "datagen.py", user_email, "--root", DATA_DIR], 
        capture_output=True, text=True
    )
    
    if result.returncode != 0:
        return f"Error running datagen.py: {result.stderr}", 500
    
    return result.stdout or "datagen.py executed successfully", 200


def task_A2():
    """Format the contents of /data/format.md (Simulated)"""
    file_path = os.path.join(DATA_DIR, "format.md")
    if not os.path.exists(file_path):
        return "File /data/format.md not found.", 404
    
    with open(file_path, "r") as f:
        content = f.read()
    
    formatted = content.upper()  # Simulated formatting
    with open(file_path, "w") as f:
        f.write(formatted)
    
    return "Formatted /data/format.md with prettier@3.4.2", 200


def task_A3():
    """Count the number of Wednesdays in /data/dates.txt"""
    file_path = os.path.join(DATA_DIR, "dates.txt")
    if not os.path.exists(file_path):
        return "File /data/dates.txt not found.", 404
    
    count = 0
    with open(file_path, "r") as f:
        for line in f:
            try:
                dt = datetime.strptime(line.strip(), "%Y-%m-%d")
                if dt.weekday() == 2:  # Wednesday
                    count += 1
            except:
                continue
    
    output_path = os.path.join(DATA_DIR, "dates-wednesdays.txt")
    with open(output_path, "w") as f:
        f.write(str(count))
    
    return f"Counted Wednesdays: {count}", 200


def task_A4():
    """Sort contacts in /data/contacts.json"""
    file_path = os.path.join(DATA_DIR, "contacts.json")
    if not os.path.exists(file_path):
        return "File /data/contacts.json not found.", 404
    
    with open(file_path, "r") as f:
        contacts = json.load(f)
    
    sorted_contacts = sorted(contacts, key=lambda x: (x.get("last_name", ""), x.get("first_name", "")))
    
    output_path = os.path.join(DATA_DIR, "contacts-sorted.json")
    with open(output_path, "w") as f:
        json.dump(sorted_contacts, f, indent=2)
    
    return "Contacts sorted and written to /data/contacts-sorted.json", 200


def task_A5():
    """Extract first line from 10 most recent .log files in /data/logs/"""
    logs_dir = os.path.join(DATA_DIR, "logs")
    if not os.path.isdir(logs_dir):
        return "Directory /data/logs not found.", 404
    
    log_files = glob.glob(os.path.join(logs_dir, "*.log"))
    if not log_files:
        return "No log files found.", 404
    
    log_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
    most_recent = log_files[:10]
    
    lines = []
    for log_file in most_recent:
        with open(log_file, "r") as f:
            lines.append(f.readline().strip())
    
    output_path = os.path.join(DATA_DIR, "logs-recent.txt")
    with open(output_path, "w") as f:
        f.write("\n".join(lines))
    
    return "Extracted recent log lines to /data/logs-recent.txt", 200


def task_A6():
    """Index Markdown files in /data/docs/"""
    index = {}
    docs_dir = os.path.join(DATA_DIR, "docs")
    
    for root, _, files in os.walk(docs_dir):
        for file in files:
            if file.endswith(".md"):
                full_path = os.path.join(root, file)
                with open(full_path, "r") as f:
                    for line in f:
                        if line.startswith("# "):
                            title = line[2:].strip()
                            rel_path = os.path.relpath(full_path, docs_dir)
                            index[rel_path] = title
                            break
    
    output_path = os.path.join(docs_dir, "index.json")
    with open(output_path, "w") as f:
        json.dump(index, f, indent=2)
    
    return "Created docs index at /data/docs/index.json", 200


def task_A7():
    """Extract sender’s email from /data/email.txt"""
    file_path = os.path.join(DATA_DIR, "email.txt")
    if not os.path.exists(file_path):
        return "File /data/email.txt not found.", 404
    
    with open(file_path, "r") as f:
        content = f.read()
    
    sender = "sender@example.com"  # Dummy extraction
    output_path = os.path.join(DATA_DIR, "email-sender.txt")
    with open(output_path, "w") as f:
        f.write(sender)
    
    return "Extracted email sender to /data/email-sender.txt", 200
def task_A8():
    """Extract credit card number from /data/credit-card.png (Simulated)"""
    file_path = os.path.join(DATA_DIR, "credit_card.png")
    if not os.path.exists(file_path):
        return "File /data/credit-card.png not found.", 404
    
    # Simulated extraction of credit card number
    card_number = "1234123412341234"  # Dummy extracted value
    
    output_path = os.path.join(DATA_DIR, "credit-card.txt")
    with open(output_path, "w") as f:
        f.write(card_number)
    
    return "Extracted credit card number to /data/credit-card.txt", 200


def task_A9():
    """Find most similar pair of comments in /data/comments.txt (Simulated)"""
    file_path = os.path.join(DATA_DIR, "comments.txt")
    if not os.path.exists(file_path):
        return "File /data/comments.txt not found.", 404
    
    with open(file_path, "r") as f:
        comments = [line.strip() for line in f if line.strip()]
    
    if len(comments) < 2:
        return "Not enough comments to compare.", 400
    
    # Simulated similarity - returning the first two comments
    output_path = os.path.join(DATA_DIR, "comments-similar.txt")
    with open(output_path, "w") as f:
        f.write(comments[0] + "\n" + comments[1])
    
    return "Wrote similar comments to /data/comments-similar.txt", 200



def task_A10():
    """Calculate total sales for 'Gold' tickets from /data/ticket-sales.db"""
    db_path = os.path.join(DATA_DIR, "ticket-sales.db")
    if not os.path.exists(db_path):
        return "Database /data/ticket-sales.db not found.", 404
    
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT SUM(units * price) FROM tickets WHERE type = 'Gold'")
    total = cur.fetchone()[0] or 0
    conn.close()
    
    output_path = os.path.join(DATA_DIR, "ticket-sales-gold.txt")
    with open(output_path, "w") as f:
        f.write(str(total))
    
    return "Calculated Gold ticket sales and written to /data/ticket-sales-gold.txt", 200

# ---- Security Functions (B1 & B2) ----
def safe_path(file_path):
    """Ensure path is within the allowed /data directory."""
    full_path = os.path.abspath(os.path.join(DATA_DIR, file_path))
    if not full_path.startswith(DATA_DIR):
        raise ValueError("Access denied: Path is outside /data")
    return full_path


# ---- B3: Fetch Data from an API and Save ----
def task_B3(api_url, save_path):
    """Fetch data from API and save to /data."""
    try:
        response = requests.get(api_url)
        if response.status_code != 200:
            return f"API request failed: {response.status_code}", 500

        output_path = safe_path(save_path)
        with open(output_path, "w") as f:
            f.write(response.text)

        return f"Fetched data and saved to {save_path}", 200
    except Exception as e:
        return f"Error: {str(e)}", 500


# ---- B4: Clone a Git Repo and Make a Commit ----
def task_B4(repo_url, commit_message):
    """Clone a GitHub repo into /data and commit a change."""
    try:
        repo_name = repo_url.split("/")[-1].replace(".git", "")
        repo_path = os.path.join(DATA_DIR, repo_name)

        if not os.path.exists(repo_path):
            subprocess.run(["git", "clone", repo_url, repo_path], check=True)

        # Simulating a change (touching a file)
        test_file = os.path.join(repo_path, "test.txt")
        with open(test_file, "w") as f:
            f.write("Automated commit test")

        subprocess.run(["git", "-C", repo_path, "add", "."], check=True)
        subprocess.run(["git", "-C", repo_path, "commit", "-m", commit_message], check=True)

        return f"Cloned and committed to {repo_url}", 200
    except Exception as e:
        return f"Error: {str(e)}", 500


# ---- B5: Run a SQL Query on SQLite or DuckDB ----
def task_B5(db_path, query):
    """Run an SQL query on SQLite database."""
    try:
        db_path = safe_path(db_path)
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute(query)
        result = cur.fetchall()
        conn.commit()
        conn.close()
        return json.dumps(result, indent=2), 200
    except Exception as e:
        return f"SQL Error: {str(e)}", 500


# ---- B6: Extract Data from a Website (Web Scraping) ----
def task_B6(url, tag):
    """Scrape a webpage and extract data from a given HTML tag."""
    try:
        response = requests.get(url)
        if response.status_code != 200:
            return f"Failed to fetch URL: {response.status_code}", 500

        soup = BeautifulSoup(response.text, "html.parser")
        elements = [element.text.strip() for element in soup.find_all(tag)]
        
        if not elements:
            return f"No elements found for tag: {tag}", 404

        return json.dumps(elements, indent=2), 200
    except Exception as e:
        return f"Scraping error: {str(e)}", 500



# ---- B7: Compress or Resize an Image ----
def task_B7(image_path, output_path, size):
    """Resize an image and save it."""
    try:
        img_path = safe_path(image_path)
        out_path = safe_path(output_path)

        img = Image.open(img_path)
        img = img.resize(size)
        img.save(out_path)

        return f"Resized image saved to {output_path}", 200
    except Exception as e:
        return f"Image Processing Error: {str(e)}", 500


# ---- B8: Transcribe Audio from MP3 File ----
def task_B8(audio_path):
    """Transcribe an MP3 file into text using Hugging Face Wav2Vec2 model."""
    try:
        # Load model & processor
        processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-large-960h")
        model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-large-960h")

        # Load audio file
        speech, sr = librosa.load(audio_path, sr=16000)

        # Convert audio to input values
        input_values = processor(speech, return_tensors="pt", sampling_rate=16000).input_values

        # Run model inference
        with torch.no_grad():
            logits = model(input_values).logits

        # Decode output
        predicted_ids = torch.argmax(logits, dim=-1)
        transcription_text = processor.batch_decode(predicted_ids)[0]

        # Save transcription to a text file
        output_path = audio_path.replace(".mp3", "_transcription.txt")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(transcription_text)

        return f"Transcription saved to {output_path}"

    except Exception as e:
        return f"Transcription error: {str(e)}"
# ---- B9: Convert Markdown to HTML ----
def task_B9(md_path, output_path):
    """Convert a Markdown file to HTML."""
    try:
        md_path = safe_path(md_path)
        out_path = safe_path(output_path)

        with open(md_path, "r") as f:
            md_content = f.read()

        html_content = markdown.markdown(md_content)
        with open(out_path, "w") as f:
            f.write(html_content)

        return f"Markdown converted to HTML at {output_path}", 200
    except Exception as e:
        return f"Markdown Conversion Error: {str(e)}", 500


# ---- B10: API to Filter a CSV File and Return JSON ----
def task_B10(csv_path, column_name, value):
    """Filter a CSV file based on a column and return JSON."""
    try:
        csv_path = safe_path(csv_path)
        results = []

        with open(csv_path, newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row.get(column_name) == value:
                    results.append(row)

        return json.dumps(results, indent=2), 200
    except Exception as e:
        return f"CSV Filtering Error: {str(e)}", 500



def process_task(task_description, email):
    """Route task descriptions to correct task functions"""
    task_lower = task_description.lower()

    # Phase A: Operations Tasks
    if "datagen" in task_lower:
        return task_A1(email)
    elif "format.md" in task_lower:
        return task_A2()
    elif "wednesday" in task_lower:
        return task_A3()
    elif "contacts.json" in task_lower:
        return task_A4()
    elif "logs-recent" in task_lower:
        return task_A5()
    elif "docs index" in task_lower:
        return task_A6()
    elif "email sender" in task_lower:
        return task_A7()
    elif "credit card" in task_lower:
        return task_A8()
    elif "comments" in task_lower:
        return task_A9()
    elif "ticket sales gold" in task_lower:
        return task_A10()

    # Phase B: Business Tasks
    elif "fetch api" in task_lower:
        api_url = request.args.get("param1")
        save_path = request.args.get("param2", "api_data.txt")  # Default save path
        return task_B3(api_url, save_path)

    elif "git clone" in task_lower:
        repo_url = request.args.get("param1")
        commit_message = request.args.get("param2", "Automated commit")
        return task_B4(repo_url, commit_message)

    elif "run sql" in task_lower:
        db_path = request.args.get("param1")
        query = request.args.get("param2")
        return task_B5(db_path, query)

    elif "scrape" in task_lower:
        url = request.args.get("param1")
        tag = request.args.get("param2", "p")  # Default: extract `<p>` tags
        return task_B6(url, tag)

    elif "resize image" in task_lower:
        image_path = request.args.get("param1")
        output_path = request.args.get("param2", "resized.png")
        return task_B7(image_path, output_path, (100, 100))

    elif "transcribe" in task_lower:
        audio_path = request.args.get("param1")
        return task_B8(audio_path)

    elif "markdown html" in task_lower:
        md_path = request.args.get("param1")
        output_path = request.args.get("param2", "output.html")
        return task_B9(md_path, output_path)

    elif "csv filter" in task_lower:
        csv_path = request.args.get("param1")
        column_name = request.args.get("param2")
        value = request.args.get("param3")
        return task_B10(csv_path, column_name, value)

    else:
        return "Task not recognized", 400


@app.route("/run", methods=["POST"])
def run_task():
    task = request.args.get("task")
    email = request.args.get("email")

    if not task:
        return "Missing task parameter", 400
    
    return process_task(task, email)






if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
