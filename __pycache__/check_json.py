import json

with open("my_file.json", "r") as f:
    data = f.read()
    json.loads(data)  # Will throw an error if JSON is invalid

print("JSON is valid!")
