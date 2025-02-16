import re

def extract_task_from_curl(curl_command: str) -> str:
    """
    Extracts the 'task' parameter from a cURL command.
    """
    match = re.search(r'task=([^"]+)', curl_command)
    if match:
        return match.group(1).replace("%20", " ")  # Convert URL-encoded spaces
    return None

# Example usage:
curl_cmd = 'curl -X POST "http://127.0.0.1:8000/run?task=sort%20the%20people%20in%20data/contact.json%20and%20put%20it%20in%20data/contact-sorted.json"'
task = extract_task_from_curl(curl_cmd)
print(task)  # Expected Output: sort the people in data/contact.json and put it in data/contact-sorted.json
