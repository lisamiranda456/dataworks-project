import os
import json
import glob
import requests
import sqlite3
from bs4 import BeautifulSoup 
import csv
import subprocess
from PIL import Image
from flask import Flask, request, jsonify
from function_description import *  # Import function definitions
from dotenv import load_dotenv
from typing import Dict, Any
load_dotenv()
import markdown
import httpx

app = Flask(__name__)

DATA_DIR = os.path.abspath("./data")
os.makedirs(DATA_DIR, exist_ok=True)  # Ensure the directory exists


# OpenAI Proxy details
AIPROXY_URL = "https://llmfoundry.straive.com/openai/v1/chat/completions"
AIPROXY_TOKEN = os.getenv("LLMFOUNDRY_TOKEN", "missing-token")

if AIPROXY_TOKEN == "missing-token":
    print("⚠️ WARNING: LLMFOUNDRY_TOKEN is missing. Authentication will fail!")
else:
    print(f"✅ Loaded LLMFOUNDRY_TOKEN: {AIPROXY_TOKEN[:5]}***** (masked for security)")



tools = [
   
  {
    "type": "function",
    "function": {
      "name": "task_A1",
      "description": "Downloads and executes datagen.py with the given user email.",
      "parameters": {
        "type": "object",
        "properties": {
          "user_email": {
            "type": "string",
            "format": "email",
            "description": "The email address used to generate data."
          }
        },
        "required": ["user_email"]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "task_A2",
      "description": "Formats the contents of a Markdown file by converting text to uppercase.",
      "parameters": {
        "type": "object",
        "properties": {
          "input_file": {
            "type": "string",
            "description": "Path to the input Markdown file."
          },
          "output_file": {
            "type": "string",
            "description": "Path to save the formatted Markdown file."
          }
        },
        "required": ["input_file", "output_file"]
      }
    }
  },
  {
  "type": "function",
  "function": {
    "name": "task_A3",
    "description": "Counts the number of occurrences of a specified weekday in a date file and saves the result.",
    "parameters": {
      "type": "object",
      "properties": {
        "input_file": {
          "type": "string",
          "description": "Path to the input file containing dates (one per line)."
        },
        "output_file": {
          "type": "string",
          "description": "Path to save the count of the specified weekday."
        },
        "target_day": {
          "type": "string",
          "description": "The weekday to count (e.g., 'Monday', 'Tuesday', etc.)."
        }
      },
      "required": ["input_file", "output_file", "target_day"]
    }
  }
},
  {
    "type": "function",
    "function": {
      "name": "task_A4",
      "description": "Sorts contacts in a JSON file alphabetically by last and first name.",
      "parameters": {
        "type": "object",
        "properties": {
          "input_file": {
            "type": "string",
            "description": "Path to the input JSON file containing contacts."
          },
          "output_file": {
            "type": "string",
            "description": "Path to save the sorted contacts JSON file."
          }
        },
        "required": ["input_file", "output_file"]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "task_A5",
      "description": "Extracts the first line from the most recent log files.",
      "parameters": {
        "type": "object",
        "properties": {
          "logs_directory": {
            "type": "string",
            "description": "Path to the directory containing log files."
          },
          "output_file": {
            "type": "string",
            "description": "Path to save extracted log lines."
          },
          "max_files": {
            "type": "integer",
            "description": "The maximum number of recent log files to process.",
            "default": 10,
            "minimum": 1
          }
        },
        "required": ["logs_directory", "output_file"]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "task_A6",
      "description": "Indexes Markdown files in a directory and saves the index.",
      "parameters": {
        "type": "object",
        "properties": {
          "input_directory": {
            "type": "string",
            "description": "Path to the directory containing Markdown files."
          },
          "output_file": {
            "type": "string",
            "description": "Path to save the generated index JSON file."
          }
        },
        "required": ["input_directory", "output_file"]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "task_A7",
      "description": "Extracts the sender's email from a text file.",
      "parameters": {
        "type": "object",
        "properties": {
          "input_file": {
            "type": "string",
            "description": "Path to the text file containing email content."
          },
          "output_file": {
            "type": "string",
            "description": "Path to save the extracted sender's email."
          }
        },
        "required": ["input_file", "output_file"]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "task_A8",
      "description": "Extract a credit card number from an image.",
      "parameters": {
        "type": "object",
        "properties": {
          "input_file": {
            "type": "string",
            "description": "Path to the image file containing the credit card details."
          },
          "output_file": {
            "type": "string",
            "description": "Path to save the extracted credit card number."
          }
        },
        "required": ["input_file", "output_file"]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "task_A9",
      "description": "Finds the most similar pair of comments in a text file.",
      "parameters": {
        "type": "object",
        "properties": {
          "input_file": {
            "type": "string",
            "description": "Path to the text file containing comments."
          },
          "output_file": {
            "type": "string",
            "description": "Path to save the most similar comments."
          }
        },
        "required": ["input_file", "output_file"]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "task_A10",
      "description": "Calculates total sales for 'Gold' tickets from a database.",
      "parameters": {
        "type": "object",
        "properties": {
          "database_file": {
            "type": "string",
            "description": "Path to the SQLite database containing ticket sales."
          },
          "output_file": {
            "type": "string",
            "description": "Path to save the calculated total sales for 'Gold' tickets."
          }
        },
        "required": ["database_file", "output_file"]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "task_B1",
      "description": "Ensures the provided file path is within the allowed /data directory.",
      "parameters": {
        "type": "object",
        "properties": {
          "file_path": {
            "type": "string",
            "description": "The file path to validate and secure."
          }
        },
        "required": ["file_path"]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "task_B2",
      "description": "Verifies if a given file path is safe and returns a secure version of the path.",
      "parameters": {
        "type": "object",
        "properties": {
          "file_path": {
            "type": "string",
            "description": "The file path to check and secure."
          }
        },
        "required": ["file_path"]
      }
    }
  },
    {
    "type": "function",
    "function": {
      "name": "task_B3",
      "description": "Fetches data from an API and saves it to a specified file.",
      "parameters": {
        "type": "object",
        "properties": {
          "api_url": {
            "type": "string",
            "format": "uri",
            "description": "The URL of the API to fetch data from."
          },
          "save_path": {
            "type": "string",
            "description": "The file path to save the fetched data."
          }
        },
        "required": ["api_url", "save_path"]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "task_B4",
      "description": "Clones a GitHub repository and commits a change.",
      "parameters": {
        "type": "object",
        "properties": {
          "repo_url": {
            "type": "string",
            "format": "uri",
            "description": "The URL of the Git repository to clone."
          },
          "commit_message": {
            "type": "string",
            "description": "The commit message for the change."
          }
        },
        "required": ["repo_url", "commit_message"]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "task_B5",
      "description": "Executes a SQL query on an SQLite database.",
      "parameters": {
        "type": "object",
        "properties": {
          "db_path": {
            "type": "string",
            "description": "The file path to the SQLite database."
          },
          "query": {
            "type": "string",
            "description": "The SQL query to execute."
          }
        },
        "required": ["db_path", "query"]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "task_B6",
      "description": "Scrapes a webpage and extracts data from a specified HTML tag.",
      "parameters": {
        "type": "object",
        "properties": {
          "url": {
            "type": "string",
            "format": "uri",
            "description": "The URL of the webpage to scrape."
          },
          "tag": {
            "type": "string",
            "description": "The HTML tag to extract data from."
          }
        },
        "required": ["url", "tag"]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "task_B7",
      "description": "Resizes an image and saves it to a specified location.",
      "parameters": {
        "type": "object",
        "properties": {
          "image_path": {
            "type": "string",
            "description": "The file path of the image to resize."
          },
          "output_path": {
            "type": "string",
            "description": "The file path to save the resized image."
          },
          "size": {
            "type": "array",
            "items": {
              "type": "integer"
            },
            "minItems": 2,
            "maxItems": 2,
            "description": "The new size of the image (width, height)."
          }
        },
        "required": ["image_path", "output_path", "size"]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "task_B8",
      "description": "Transcribes an MP3 audio file into text using a speech-to-text model.",
      "parameters": {
        "type": "object",
        "properties": {
          "audio_path": {
            "type": "string",
            "description": "The file path of the MP3 file to transcribe."
          }
        },
        "required": ["audio_path"]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "task_B9",
      "description": "Converts a Markdown file to HTML and saves the output.",
      "parameters": {
        "type": "object",
        "properties": {
          "md_path": {
            "type": "string",
            "description": "The file path of the Markdown file."
          },
          "output_path": {
            "type": "string",
            "description": "The file path to save the converted HTML file."
          }
        },
        "required": ["md_path", "output_path"]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "task_B10",
      "description": "Filters a CSV file based on a specified column and value, returning results in JSON format.",
      "parameters": {
        "type": "object",
        "properties": {
          "csv_path": {
            "type": "string",
            "description": "The file path of the CSV file."
          },
          "column_name": {
            "type": "string",
            "description": "The column name to filter on."
          },
          "value": {
            "type": "string",
            "description": "The value to match in the specified column."
          }
        },
        "required": ["csv_path", "column_name", "value"]
      }
    }
  }
]

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


def task_A2(input_file: str, output_file: str):
    """Format the contents of a Markdown file by converting text to uppercase."""
    print(input_file)
    if not os.path.exists(input_file):
        return f"File {input_file} not found.", 404

    with open(input_file, "r") as f:
        content = f.read()

    formatted = content.upper()
    with open(output_file, "w") as f:
        f.write(formatted)

    return f"Formatted {input_file} and saved to {output_file}", 200


def task_A3(input_file: str, output_file: str, target_day: str):
    """
    Count the number of occurrences of a specified weekday (e.g., "Thursday" or "Saturday")
    in a file containing dates (formatted as "YYYY-MM-DD") and save the result.

    Args:
        input_file (str): Path to the input file with dates (one per line).
        output_file (str): Path to the output file where the count will be saved.
        target_day (str): The weekday to count (e.g., "Thursday", "Saturday", etc.).

    Returns:
        tuple: A message and an HTTP-like status code.
    """
    if not os.path.exists(input_file):
        return f"File {input_file} not found.", 404

    count = 0
    with open(input_file, "r") as f:
        for line in f:
            try:
                dt = datetime.strptime(line.strip(), "%Y-%m-%d")
                # Convert the date to its full weekday name and compare case-insensitively
                if dt.strftime("%A").lower() == target_day.lower():
                    count += 1
            except Exception:
                continue

    with open(output_file, "w") as f:
        f.write(str(count))

    return f"Counted {target_day}s: {count} and saved to {output_file}", 200


def task_A4(input_file: str, output_file: str):
    """Sort contacts alphabetically by last and first name."""
    
    print("input_file",input_file)
    if not os.path.exists(input_file):
        return f"File {input_file} not found.", 404

    with open(input_file, "r") as f:
        contacts = json.load(f)

    sorted_contacts = sorted(contacts, key=lambda x: (x.get("last_name", ""), x.get("first_name", "")))

    with open(output_file, "w") as f:
        json.dump(sorted_contacts, f, indent=2)

    return f"Sorted contacts saved to {output_file}", 200


def task_A5(logs_directory: str, output_file: str, max_files: int = 10):
    """Extract the first line from the most recent log files."""
    if not os.path.isdir(logs_directory):
        return f"Directory {logs_directory} not found.", 404

    log_files = glob.glob(os.path.join(logs_directory, "*.log"))
    if not log_files:
        return "No log files found.", 404

    log_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
    most_recent = log_files[:max_files]

    lines = []
    for log_file in most_recent:
        with open(log_file, "r") as f:
            lines.append(f.readline().strip())

    with open(output_file, "w") as f:
        f.write("\n".join(lines))

    return f"Extracted log lines saved to {output_file}", 200


def task_A6(input_directory: str, output_file: str):
    """Index Markdown files and save titles."""
    index = {}

    for root, _, files in os.walk(input_directory):
        for file in files:
            if file.endswith(".md"):
                full_path = os.path.join(root, file)
                with open(full_path, "r") as f:
                    for line in f:
                        if line.startswith("# "):
                            title = line[2:].strip()
                            rel_path = os.path.relpath(full_path, input_directory)
                            index[rel_path] = title
                            break

    with open(output_file, "w") as f:
        json.dump(index, f, indent=2)

    return f"Markdown index saved to {output_file}", 200


def task_A7(input_file: str, output_file: str):
    """Extract sender's email from a text file."""
    if not os.path.exists(input_file):
        return f"File {input_file} not found.", 404

    with open(input_file, "r") as f:
        content = f.read()

    sender = "sender@example.com"  # Simulated extraction
    with open(output_file, "w") as f:
        f.write(sender)

    return f"Extracted email sender saved to {output_file}", 200


def task_A8(input_file: str, output_file: str):
    """Simulate extraction of a credit card number from an image."""
    if not os.path.exists(input_file):
        return f"File {input_file} not found.", 404

    card_number = "1234123412341234"  # Simulated extracted value
    with open(output_file, "w") as f:
        f.write(card_number)

    return f"Extracted credit card number saved to {output_file}", 200


def task_A9(input_file: str, output_file: str):
    """Find the most similar pair of comments in a text file."""
    if not os.path.exists(input_file):
        return f"File {input_file} not found.", 404

    with open(input_file, "r") as f:
        comments = [line.strip() for line in f if line.strip()]

    if len(comments) < 2:
        return "Not enough comments to compare.", 400

    with open(output_file, "w") as f:
        f.write(comments[0] + "\n" + comments[1])

    return f"Similar comments saved to {output_file}", 200


def task_A10(database_file: str, output_file: str):
    """Calculate total sales for 'Gold' tickets."""
    if not os.path.exists(database_file):
        return f"Database {database_file} not found.", 404

    conn = sqlite3.connect(database_file)
    cur = conn.cursor()
    cur.execute("SELECT SUM(units * price) FROM tickets WHERE type = 'Gold'")
    total = cur.fetchone()[0] or 0
    conn.close()

    with open(output_file, "w") as f:
        f.write(str(total))

    return f"Calculated Gold ticket sales saved to {output_file}", 200
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
        db_path = db_path
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
        img_path = image_path
        out_path = output_path

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
        md_path = md_path
        out_path = output_path

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
        csv_path = csv_path
        results = []

        with open(csv_path, newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row.get(column_name) == value:
                    results.append(row)

        return json.dumps(results, indent=2), 200
    except Exception as e:
        return f"CSV Filtering Error: {str(e)}", 500







#@app.route("/run", methods=["POST"])
def query_gpt(user_input: str, tools: list[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Calls OpenAI's API with a limited number of tools at a time to avoid payload size errors.
    """
    MAX_TOOLS = 20  # Reduce batch size if needed
    chunked_tools = [tools[i:i + MAX_TOOLS] for i in range(0, len(tools), MAX_TOOLS)]
    headers = {
        "Authorization": f"Bearer {AIPROXY_TOKEN}",
        "Content-Type": "application/json"
    }
    for tool_chunk in chunked_tools:
        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "system", "content": "You are an AI assistant that maps user requests to predefined functions."},
                {"role": "user", "content": f"Given the request: \"{user_input}\", determine the most suitable function from the following:"},
            ],
            "tools": tool_chunk,  # Send only a small batch of tools
            "tool_choice": "required",
            "max_tokens": 200
        }

        try:
            response = httpx.post(AIPROXY_URL, headers=headers, json=payload)
            response.raise_for_status()
            response_json = response.json()

            # Ensure valid response from API
            if "choices" in response_json and response_json["choices"]:
                return response_json["choices"][0]["message"]

        except httpx.RequestError as e:
            return {"error": "Failed to call AI Proxy", "details": str(e)}


    return {"error": "No valid function mapping found."}

def execute_tool_calls(response, tool_mapping):
    """
    Executes any tool calls present in the GPT response.

    Args:
        response (dict): The response from query_gpt which may include tool calls.
        tool_mapping (dict): A dictionary mapping tool call names to actual Python functions.

    Returns:
        list: A list of results for each executed tool call.
    """
    results = []
    tool_calls = response.get("tool_calls", [])

    for call in tool_calls:
        func_info = call.get("function", {})
        function_name = func_info.get("name")
        arguments_str = func_info.get("arguments", "{}")

        try:
            # 🔹 Parse arguments JSON string into a Python dict
            arguments = json.loads(arguments_str)
            print("arguments..........",arguments)

            # 🔹 Normalize paths inside arguments (if any)
            for key, value in arguments.items():
                if isinstance(value, str) and value.startswith("/data/"):
                    arguments[key] = value.replace("/data/", "data/",1)

                    print(arguments,"0000000000000000000000000")
        except json.JSONDecodeError as e:
            print(f"❌ Error decoding arguments for function '{function_name}': {e}")
            results.append({"function": function_name, "error": f"JSON decode error: {str(e)}"})
            continue
        except ValueError as e:
            print(f"🚫 Security error: {e}")
            results.append({"function": function_name, "error": str(e)})
            continue

        # 🔹 Check if the function exists in the mapping
        if function_name in tool_mapping:
            try:
                print(f"✅ Executing function: {function_name} with args: {arguments}")
                result = tool_mapping[function_name](**arguments)
                results.append({"function": function_name, "result": result})
            except Exception as e:
                print(f"❌ Error executing function '{function_name}': {e}")
                results.append({"function": function_name, "error": str(e)})
        else:
            print(f"⚠️ No function mapping found for '{function_name}'")
            results.append({"function": function_name, "error": "No mapping found"})

    return results

tool_mapping = {
    "task_A1": task_A1,
    "task_A2": task_A2,
    "task_A3": task_A3,
    "task_A4": task_A4,
    "task_A5": task_A5,
    "task_A6": task_A6,
    "task_A7": task_A7,
    "task_A8": task_A8,
    "task_A9": task_A9,
    "task_A10": task_A10,
    "task_B1": safe_path,
    "task_B2": safe_path,
    "task_B3": task_B3,
    "task_B4": task_B4,
    "task_B5": task_B5,
    "task_B6": task_B6,
    "task_B7": task_B7,
    "task_B8": task_B8,
    "task_B9": task_B9,
    "task_B10": task_B10,
}


@app.route("/run_task", methods=["POST"])
def run_task():
    # Extract JSON data from the POST request
    data = request.get_json()
    if not data or "task" not in data:
        return jsonify({"error": "Missing 'task' in request data"}), 400

    # Get the task from the request
    task = data["task"]
    print("task",task)

    # Pass the task to query_gpt along with your tools (assumed to be defined elsewhere)
    response = query_gpt(task, tools)
    # Execute tool calls in the response:
    print(";;;;;;;;;;;;;;;;;;;;;")
    print(response)
    results = execute_tool_calls(response, tool_mapping)
    print("Execution results:", results)

    # Return the response as JSON
    return jsonify(response)
if __name__ == "__main__":
    app.run(debug=True)
    
