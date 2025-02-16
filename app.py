# app.py
# /// script
# dependencies = [
#   "requests",
#   "fastapi",
#   "uvicorn",
#   "python-dateutil",
#   "pandas",
#   "db-sqlite3",
#   "scipy",
#   "pybase64",
#   "python-dotenv",
#   "httpx",
#   "markdown",
#   "duckdb",
#   "Pillow",
#   "faker",
#   "openai",
#   "flask"
# ]
# ///

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import PlainTextResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import requests
from dotenv import load_dotenv
import os
import re
import httpx
import json



# tasks A

import sqlite3
import subprocess
from dateutil.parser import parse
from datetime import datetime
import json
from pathlib import Path
import os
import requests
from scipy.spatial.distance import cosine
from dotenv import load_dotenv
from fastapi import HTTPException
load_dotenv()

AIPROXY_TOKEN = os.getenv('AIPROXY_TOKEN')

def A1(url=None, filename=None, email="22f30000079@ds.study.iitm.ac.in"):
    print("url : ", url, "", "filename : ", filename, sep="\n")
    if url:
        script = url
    elif filename:
        script = filename
    else:
        script = "https://raw.githubusercontent.com/sanand0/tools-in-data-science-public/tds-2025-01/project-1/datagen.py"
    try:
        process = subprocess.Popen(
            ["uv", "run", script, email],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        stdout, stderr = process.communicate()
        if process.returncode != 0:
            raise HTTPException(status_code=500, detail=f"Error: {stderr}")
        return stdout
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"Error: {e.stderr}")

def A2(prettier_version="prettier@3.4.2", filename="/data/format.md"):
    command = ["npx", prettier_version, "--write", filename]
    try:
        subprocess.run(command, check=True)
        print("Prettier executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")

def A3(filename='/data/dates.txt', targetfile='/data/dates-wednesdays.txt', weekday=2):
    input_file = filename
    output_file = targetfile
    weekday = weekday
    weekday_count = 0

    with open(input_file, 'r') as file:
        weekday_count = sum(1 for date in file if parse(date).weekday() == int(weekday)-1)


    with open(output_file, 'w') as file:
        file.write(str(weekday_count))

def A4(filename="/data/contacts.json", targetfile="/data/contacts-sorted.json"):
    # Load the contacts from the JSON file
    with open(filename, 'r') as file:
        contacts = json.load(file)

    # Sort the contacts by last_name and then by first_name
    sorted_contacts = sorted(contacts, key=lambda x: (x['last_name'], x['first_name']))

    # Write the sorted contacts to the new JSON file
    with open(targetfile, 'w') as file:
        json.dump(sorted_contacts, file, indent=4)

def A5(log_dir_path='/data/logs', output_file_path='/data/logs-recent.txt', num_files=10):
    log_dir = Path(log_dir_path)
    output_file = Path(output_file_path)

    # Get list of .log files sorted by modification time (most recent first)
    log_files = sorted(log_dir.glob('*.log'), key=os.path.getmtime, reverse=True)[:num_files]

    # Read first line of each file and write to the output file
    with output_file.open('w') as f_out:
        for log_file in log_files:
            with log_file.open('r') as f_in:
                first_line = f_in.readline().strip()
                f_out.write(f"{first_line}\n")

def A6(doc_dir_path='/data/docs', output_file_path='/data/docs/index.json'):
    docs_dir = doc_dir_path
    output_file = output_file_path
    index_data = {}

    # Walk through all files in the docs directory
    for root, _, files in os.walk(docs_dir):
        for file in files:
            if file.endswith('.md'):
                # print(file)
                file_path = os.path.join(root, file)
                # Read the file and find the first occurrence of an H1
                with open(file_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        if line.startswith('# '):
                            # Extract the title text after '# '
                            title = line[2:].strip()
                            # Get the relative path without the prefix
                            relative_path = os.path.relpath(file_path, docs_dir).replace('\\', '/')
                            index_data[relative_path] = title
                            break  # Stop after the first H1
    # Write the index data to index.json
    # print(index_data)
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(index_data, f, indent=4)

def A7(filename='/data/email.txt', output_file='/data/email-sender.txt'):
    # Read the content of the email
    with open(filename, 'r') as file:
        email_content = file.readlines()

    sender_email = "sujay@gmail.com"
    for line in email_content:
        if "From" == line[:4]:
            sender_email = (line.strip().split(" ")[-1]).replace("<", "").replace(">", "")
            break

    # Get the extracted email address

    # Write the email address to the output file
    with open(output_file, 'w') as file:
        file.write(sender_email)

import base64
def png_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        base64_string = base64.b64encode(image_file.read()).decode('utf-8')
    return base64_string

def A8(filename='/data/credit_card.txt', image_path='/data/credit_card.png'):
    # Construct the request body for the AIProxy call
    body = {
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "There is 8 or more digit number is there in this image, with space after every 4 digit, only extract the those digit number without spaces and return just the number without any other characters"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{png_to_base64(image_path)}"
                        }
                    }
                ]
            }
        ]
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {AIPROXY_TOKEN}"
    }

    # Make the request to the AIProxy service
    response = requests.post("http://aiproxy.sanand.workers.dev/openai/v1/chat/completions",
                             headers=headers, data=json.dumps(body))
    # response.raise_for_status()

    # Extract the credit card number from the response
    result = response.json()
    # print(result); return None
    card_number = result['choices'][0]['message']['content'].replace(" ", "")

    # Write the extracted card number to the output file
    with open(filename, 'w') as file:
        file.write(card_number)
# A8()



def get_embedding(text):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {AIPROXY_TOKEN}"
    }
    data = {
        "model": "text-embedding-3-small",
        "input": [text]
    }
    response = requests.post("http://aiproxy.sanand.workers.dev/openai/v1/embeddings", headers=headers, data=json.dumps(data))
    response.raise_for_status()
    return response.json()["data"][0]["embedding"]

def A9(input_filename='/data/comments.txt', output_filename='/data/comments-similar.txt'):
    # Read comments
    with open(input_filename, 'r') as f:
        comments = [line.strip() for line in f.readlines()]

    # Get embeddings for all comments
    embeddings = [get_embedding(comment) for comment in comments]

    # Find the most similar pair
    min_distance = float('inf')
    most_similar = (None, None)

    for i in range(len(comments)):
        for j in range(i + 1, len(comments)):
            distance = cosine(embeddings[i], embeddings[j])
            if distance < min_distance:
                min_distance = distance
                most_similar = (comments[i], comments[j])

    # Write the most similar pair to file
    with open(output_filename, 'w') as f:
        f.write(most_similar[0] + '\n')
        f.write(most_similar[1] + '\n')

def A10(filename='/data/ticket-sales.db', output_filename='/data/ticket-sales-gold.txt', query="SELECT SUM(units * price) FROM tickets WHERE type = 'Gold'"):
    # Connect to the SQLite database
    conn = sqlite3.connect(filename)
    cursor = conn.cursor()

    # Calculate the total sales for the "Gold" ticket type
    cursor.execute(query)
    total_sales = cursor.fetchone()[0]

    # If there are no sales, set total_sales to 0
    total_sales = total_sales if total_sales else 0

    # Write the total sales to the file
    with open(output_filename, 'w') as file:
        file.write(str(total_sales))

    # Close the database connection
    conn.close()


# Phase B: LLM-based Automation Agent for DataWorks Solutions

# B1 & B2: Security Checks
import os
from fastapi import HTTPException

def B1(filepath: str) -> bool:
    """Enforce data containment policy with security checks.
    
    Args:
        filepath: Input path to validate
        operation_type: One of ['read', 'write', 'execute']
        
    Returns:
        bool: True if allowed, False if violation
    """
    try:
        # Normalize path
        abs_path = os.path.abspath(filepath)
        resolved_path = os.path.realpath(abs_path)
        
        # Validate directory containment
        if not resolved_path.startswith('/data/'):
            return False
            
        # Additional security checks
        if '..' in resolved_path:
            return False
            
        if not os.path.normcase(resolved_path).startswith('/data/'):
            return False
        return True
        
    except Exception as e:
        # Log security violations
        print(f"Security exception: {str(e)}")
        return False

def B2(operation_type: str) -> bool:
    """Block all deletion operations regardless of target"""
    deletion_verbs = {"delete", "remove", "truncate", "unlink", "rm", "purge", "erase"}
    
    if operation_type.lower() in deletion_verbs:
        print(f"Security Block: Deletion operation '{operation_type}' prohibited")
        raise HTTPException(status_code=400, detail="Deletion operations are prohibited")

# B3: Fetch Data from an API
def B3(url, save_path):
    import requests
    response = requests.get(url)
    with open(save_path, 'w') as file:
        file.write(response.text)

# B4: Clone a Git Repo and Make a Commit
def B4(repository_url, commit_message):
    import subprocess
    # Clone the repository into /data/repo
    subprocess.run(["git", "clone", repository_url, "/data/repo"], check=True)
    
    # Create an empty commit with the specified message
    subprocess.run(
        ["git", "-C", "/data/repo", "commit", "--allow-empty", "-m", commit_message],
        check=True
    )

# B5: Run SQL Query
def B5(db_path, query, output_filename):
    import sqlite3, duckdb
    conn = sqlite3.connect(db_path) if db_path.endswith('.db') else duckdb.connect(db_path)
    cur = conn.cursor()
    cur.execute(query)
    result = cur.fetchall()
    conn.close()
    with open(output_filename, 'w') as file:
        file.write(str(result))
    return result

# B6: Web Scraping
def B6(url, output_filename):
    import requests
    result = requests.get(url).text
    with open(output_filename, 'w') as file:
        file.write(str(result))

# B7: Image Processing
def B7(image_path, output_path, resize=None):
    from PIL import Image
    img = Image.open(image_path)
    if resize:
        img = img.resize(resize)
    img.save(output_path)

import openai

def B8(mp3_file: str, output_path: str) -> bool:
    try:
        # 2. API configuration 
        openai.api_key = os.getenv("OPENAI_API_KEY")  # Securely load from environment
        
        # 3. Transcribe audio
        with open(mp3_file, "rb") as audio_file:
            transcript = openai.Audio.transcribe(
                model="whisper-1",
                file=audio_file,
                response_format="text"
            )
            
        # 4. Save output
        with open(output_path, "w") as f:
            f.write(transcript)
               
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {e.stderr}")
    
# B9: Markdown to HTML Conversion
def B9(md_path, output_path):
    import markdown
    with open(md_path, 'r') as file:
        html = markdown.markdown(file.read())
    with open(output_path, 'w') as file:
        file.write(html)

# B10: API Endpoint for CSV Filtering
from flask import Flask, request, jsonify
import pandas as pd
def B10(api_endpoint='/filter_csv'):
    app = Flask(__name__)
    @app.route(api_endpoint, methods=['POST'])
    def filter_csv():
        data = request.json
        csv_path, filter_column, filter_value = data['csv_path'], data['filter_column'], data['filter_value']
        df = pd.read_csv(csv_path)
        filtered = df[df[filter_column] == filter_value]
        return jsonify(filtered.to_dict(orient='records'))




app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


app = FastAPI()
load_dotenv()

@app.get("/ask")
def ask(prompt: str):
    result = get_completions(prompt)
    return result

openai_api_chat  = "http://aiproxy.sanand.workers.dev/openai/v1/chat/completions" # for testing
openai_api_key = os.getenv("AIPROXY_TOKEN")

headers = {
    "Authorization": f"Bearer {openai_api_key}",
    "Content-Type": "application/json",
}

function_definitions_llm = [
    {
        "name": "A1",
        "description": "Run a Python script from a given URL or file path or file name, passing an email as the argument.",
        "parameters": {
            "type": "object",
            "properties": {
                "url": {"type": "string", "pattern": r"https?://.*\.py"},
                "filename": {"type": "string", "pattern": r"(?:.*/)?(.*\.py)"},
                "email": {"type": "string", "pattern": r"[\w\.-]+@[\w\.-]+\.\w+"}
            },
            "required": ["email"]
        }
    },
    {
        "name": "A2",
        "description": "Format a markdown file using a specified version of Prettier.",
        "parameters": {
            "type": "object",
            "properties": {
                "prettier_version": {"type": "string", "pattern": r"prettier@\d+\.\d+\.\d+"},
                "filename": {"type": "string", "pattern": r".*/(.*\.md)"}
            },
            "required": ["prettier_version", "filename"]
        }
    },
    {
        "name": "A3",
        "description": "Count the number of occurrences of a specific weekday in a date file.",
        "parameters": {
            "type": "object",
            "properties": {
                "filename": {"type": "string", "pattern": r"/data/.*dates.*\.txt"},
                "targetfile": {"type": "string", "pattern": r"/data/.*/(.*\.txt)"},
                "weekday": {"type": "integer", "pattern": r"(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)"}
            },
            "required": ["filename", "targetfile", "weekday"]
        }
    },
    {
        "name": "A4",
        "description": "Sort a JSON contacts file and save the sorted version to a target file.",
        "parameters": {
            "type": "object",
            "properties": {
                "filename": {
                    "type": "string",
                    "pattern": r".*/(.*\.json)",
                },
                "targetfile": {
                    "type": "string",
                    "pattern": r".*/(.*\.json)",
                }
            },
            "required": ["filename", "targetfile"]
        }
    },
    {
        "name": "A5",
        "description": "Retrieve the most recent log files from a directory and save their content to an output file.",
        "parameters": {
            "type": "object",
            "properties": {
                "log_dir_path": {
                    "type": "string",
                    "pattern": r".*/logs",
                    "default": "/data/logs"
                },
                "output_file_path": {
                    "type": "string",
                    "pattern": r".*/(.*\.txt)",
                    "default": "/data/logs-recent.txt"
                },
                "num_files": {
                    "type": "integer",
                    "minimum": 1,
                    "default": 10
                }
            },
            "required": ["log_dir_path", "output_file_path", "num_files"]
        }
    },
    {
        "name": "A6",
        "description": "Generate an index of documents from a directory and save it as a JSON file.",
        "parameters": {
            "type": "object",
            "properties": {
                "doc_dir_path": {
                    "type": "string",
                    "pattern": r".*/docs",
                    "default": "/data/docs"
                },
                "output_file_path": {
                    "type": "string",
                    "pattern": r".*/(.*\.json)",
                    "default": "/data/docs/index.json"
                }
            },
            "required": ["doc_dir_path", "output_file_path"]
        }
    },
    {
        "name": "A7",
        "description": "Extract the sender's email address from a text file and save it to an output file.",
        "parameters": {
            "type": "object",
            "properties": {
                "filename": {
                    "type": "string",
                    "pattern": r".*/(.*\.txt)",
                    "default": "/data/email.txt"
                },
                "output_file": {
                    "type": "string",
                    "pattern": r".*/(.*\.txt)",
                    "default": "/data/email-sender.txt"
                }
            },
            "required": ["filename", "output_file"]
        }
    },
    {
        "name": "A8",
        "description": "Generate an image representation of credit card details from a text file.",
        "parameters": {
            "type": "object",
            "properties": {
                "filename": {
                    "type": "string",
                    "pattern": r".*/(.*\.txt)",
                    "default": "/data/credit-card.txt"
                },
                "image_path": {
                    "type": "string",
                    "pattern": r".*/(.*\.png)",
                    "default": "/data/credit-card.png"
                }
            },
            "required": ["filename", "image_path"]
        }
    },
    {
        "name": "A9",
        "description": "Using embeddings, find the most similar pair of lines from an input file and write them to an output file, one per line.",
        "parameters": {
            "type": "object",
            "properties": {
                "input_filename": {
                    "type": "string",
                    "pattern": r".*/(.*\.txt)",
                    "default": "/data/comments.txt"
                },
                "output_filename": {
                    "type": "string",
                    "pattern": r".*/(.*\.txt)",
                    "default": "/data/comments-similar.txt"
                }
            },
            "required": ["input_filename", "output_filename"]
        }
    },
    {
        "name": "A10",
        "description": "Identify high-value (gold) ticket sales from a database and save them to a text file.",
        "parameters": {
            "type": "object",
            "properties": {
                "filename": {
                    "type": "string",
                    "pattern": r".*/(.*\.db)",
                    "default": "/data/ticket-sales.db"
                },
                "output_filename": {
                    "type": "string",
                    "pattern": r".*/(.*\.txt)",
                    "default": "/data/ticket-sales-gold.txt"
                },
                "query": {
                    "type": "string",
                    "pattern": "SELECT SUM(units * price) FROM tickets WHERE type = 'Gold'"
                }
            },
            "required": ["filename", "output_filename", "query"]
        }
    },
    {
        "name": "B1",
        "description": "Enforce data containment policy by restricting file access to only the /data directory and preventing external data exfiltration.",
        "parameters": {
            "type": "object",
            "properties": {
                "filepath": {
                    "type": "string",
                    "pattern": r"^/data(/[^/\s\\]+)*/?$",
                    "description": "Path normalized and validated to be within /data directory"
                }
            },
            "required": ["filepath"]
        }
    },
    {
        "name": "B2",
        "description": "Prevent any data deletion operations on the file system, regardless of location or parameters.",
        "parameters": {
            "type": "object",
            "properties": {
                "operation_type": {
                    "type": "string", 
                    "pattern": r"^(delete|remove|truncate|unlink|rm|purge|erase)$",
                    "description": "Type of destructive operation being attempted"
                }
            },
            "required": ["operation_type"]
        }
    },
    {
        "name": "B3",
        "description": "Download content from a URL and save it to the specified path.",
        "parameters": {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "pattern": r"https?://.*",
                    "description": "URL to download content from."
                },
                "save_path": {
                    "type": "string",
                    "pattern": r".*/.*",
                    "description": "Path to save the downloaded content."
                }
            },
            "required": ["url", "save_path"]
        }
    },
    {
        "name": "B4",
        "description": "Clone a git repository from a given URL and make a commit with the specified commit message.",
        "parameters": {
            "type": "object",
            "properties": {
                "repository_url": {
                    "type": "string",
                    "pattern": r"https?://.*\.git"
                },
                "commit_message": {
                    "type": "string"
                }
            },
            "required": ["repository_url", "commit_message"]
        }
    },
    {
        "name": "B5",
        "description": "Execute a SQL query on a specified database file and save the result to an output file.",
        "parameters": {
            "type": "object",
            "properties": {
                "db_path": {
                    "type": "string",
                    "pattern": r".*/(.*\.db)",
                    "description": "Path to the SQLite database file."
                },
                "query": {
                    "type": "string",
                    "description": "SQL query to be executed on the database."
                },
                "output_filename": {
                    "type": "string",
                    "pattern": r".*/(.*\.txt)",
                    "description": "Path to the file where the query result will be saved."
                }
            },
            "required": ["db_path", "query", "output_filename"]
        }
    },
    {
        "name": "B6",
        "description": "Fetch content from a URL and save it to the specified output file.",
        "parameters": {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "pattern": r"https?://.*",
                    "description": "URL to fetch content from."
                },
                "output_filename": {
                    "type": "string",
                    "pattern": r".*/.*",
                    "description": "Path to the file where the content will be saved."
                }
            },
            "required": ["url", "output_filename"]
        }
    },
    {
        "name": "B7",
        "description": "Process an image by optionally resizing it and saving the result to an output path.",
        "parameters": {
            "type": "object",
            "properties": {
                "image_path": {
                    "type": "string",
                    "pattern": r".*/(.*\.(jpg|jpeg|png|gif|bmp))",
                    "description": "Path to the input image file."
                },
                "output_path": {
                    "type": "string",
                    "pattern": r".*/.*",
                    "description": "Path to save the processed image."
                },
                "resize": {
                    "type": "array",
                    "items": {
                        "type": "integer",
                        "minimum": 1
                    },
                    "minItems": 2,
                    "maxItems": 2,
                    "description": "Optional. Resize dimensions as [width, height]."
                }
            },
            "required": ["image_path", "output_path"]
        }
    },
    {
        "name": "B8",
        "description": "Convert speech in an MP3 audio file to text transcription and save the result to an output file.",
        "parameters": {
            "type": "object",
            "properties": {
                "mp3_file": {
                    "type": "string",
                    "pattern": r"^(?:.*/)?(.*\.mp3)$",
                    "description": "Path to input MP3 audio file"
                },
                "output_path": {
                    "type": "string",
                    "pattern": r".*/.*",
                    "description": "Path where the converted file will be saved."
                }
            },
            "required": ["mp3_file", "output_path"]
        }
    },
    {
        "name": "B9",
        "description": "Convert a Markdown file to another format and save the result to the specified output path.",
        "parameters": {
            "type": "object",
            "properties": {
                "md_path": {
                    "type": "string",
                    "pattern": r".*/(.*\.md)",
                    "description": "Path to the Markdown file to be converted."
                },
                "output_path": {
                    "type": "string",
                    "pattern": r".*/.*",
                    "description": "Path where the converted file will be saved."
                }
            },
            "required": ["md_path", "output_path"]
        }
    },
    {
        "name": "B10",
        "description": "Universal API endpoint for CSV filtering operations",
        "parameters": {
            "type": "object",
            "properties": {
                "api_endpoint": {
                    "type": "string",
                    "pattern": r"^\/[a-zA-Z0-9\-_\/]+$",
                    "description": "Wildcard API endpoint path for CSV filtering operations"
                }
            }
        }
    }
]

def get_completions(prompt: str):
    with httpx.Client(timeout=20) as client:
        response = client.post(
            f"{openai_api_chat}",
            headers=headers,
            json=
                {
                    "model": "gpt-4o-mini",
                    "messages": [
                                    {"role": "system", "content": "You are a function classifier that extracts structured parameters from queries."},
                                    {"role": "user", "content": prompt}
                                ],
                    "tools": [
                                {
                                    "type": "function",
                                    "function": function
                                } for function in function_definitions_llm
                            ],
                    "tool_choice": "auto"
                },
        )
    # return response.json()
    print(response.json()["choices"][0]["message"]["tool_calls"][0]["function"])
    return response.json()["choices"][0]["message"]["tool_calls"][0]["function"]


# Placeholder for task execution
@app.post("/run")
async def run_task(task: str):
    try:
        # Placeholder logic for executing tasks
        # Replace with actual logic to parse task and execute steps
        # Example: Execute task and return success or error based on result
        # llm_response = function_calling(tast), function_name = A1
        response = get_completions(task)
        print(response)
        task_code = response['name']
        arguments = response['arguments']

        if "A1"== task_code:
            A1(**json.loads(arguments))
        if "A2"== task_code:
            A2(**json.loads(arguments))
        if "A3"== task_code:
            A3(**json.loads(arguments))
        if "A4"== task_code:
            A4(**json.loads(arguments))
        if "A5"== task_code:
            A5(**json.loads(arguments))
        if "A6"== task_code:
            A6(**json.loads(arguments))
        if "A7"== task_code:
            A7(**json.loads(arguments))
        if "A8"== task_code:
            A8(**json.loads(arguments))
        if "A9"== task_code:
            A9(**json.loads(arguments))
        if "A10"== task_code:
            A10(**json.loads(arguments))


        if "B1"== task_code:
            B1(**json.loads(arguments))
        if "B2"== task_code:
            B2(**json.loads(arguments))
        if "B3" == task_code:
            B3(**json.loads(arguments))
        if "B4" == task_code:
            B4(**json.loads(arguments))
        if "B5" == task_code:
            B5(**json.loads(arguments))
        if "B6" == task_code:
            B6(**json.loads(arguments))
        if "B7" == task_code:
            B7(**json.loads(arguments))
        if "B8" == task_code:
            B8(**json.loads(arguments))
        if "B9" == task_code:
            B9(**json.loads(arguments))
        if "B10" == task_code:
            B10(**json.loads(arguments))
        return {"message": f"{task_code} Task '{task}' executed successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Placeholder for file reading
@app.get("/read", response_class=PlainTextResponse)
async def read_file(path: str = Query(..., description="File path to read")):
    try:
        with open(path, "r") as file:
            return file.read()
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    # uvicorn.run(app, host="127.0.0.1", port=8000)
    uvicorn.run(app, host="0.0.0.0", port=8000)
