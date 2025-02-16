tools=[
  {
    "task_A1": {
      "description": "Downloads and executes datagen.py with the given user email.",
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
  },
  {
    "task_A2": {
      "description": "Formats the contents of a Markdown file by converting text to uppercase.",
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
  },
  {
    "task_A3": {
      "description": "Counts the number of Wednesdays in a date file and saves the result.",
      "type": "object",
      "properties": {
        "input_file": {
          "type": "string",
          "description": "Path to the input file containing dates (one per line)."
        },
        "output_file": {
          "type": "string",
          "description": "Path to save the count of Wednesdays."
        }
      },
      "required": ["input_file", "output_file"]
    }
  },
  {
    "task_A4": {
      "description": "Sorts contacts in a JSON file alphabetically by last and first name.",
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
  },
  {
    "task_A5": {
      "description": "Extracts the first line from the most recent log files.",
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
  },
  {
    "task_A6": {
      "description": "Indexes Markdown files in a directory and saves the index.",
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
  },
  {
    "task_A7": {
      "description": "Extracts the sender's email from a text file.",
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
  },
  {
    "task_A8": {
      "description": "Extract a credit card number from an image.",
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
  },
  {
    "task_A9": {
      "description": "Finds the most similar pair of comments in a text file.",
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
  },
  {
    "task_A10": {
      "description": "Calculates total sales for 'Gold' tickets from a database.",
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
  },
  {
    "task_B3": {
      "description": "Fetches data from an API and saves it to a specified file.",
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
  },
  {
    "task_B4": {
      "description": "Clones a GitHub repository and commits a change.",
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
  },
  {
    "task_B5": {
      "description": "Executes a SQL query on an SQLite database.",
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
  },
  {
    "task_B10": {
      "description": "Filters a CSV file based on a specified column and value, returning results in JSON format.",
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
]
