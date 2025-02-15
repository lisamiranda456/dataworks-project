from flask import Flask, request, Response
from pyngrok import ngrok

app = Flask(__name__)

@app.route("/run", methods=["POST"])
def run_endpoint():
    task = request.args.get("task")
    if not task:
        return "Missing task parameter", 400
    # Your task processing logic goes here...
    return f"Received task: {task}", 200

@app.route("/read", methods=["GET"])
def read_endpoint():
    path = request.args.get("path")
    if not path:
        return "Missing path parameter", 400
    try:
        with open(path, "r") as f:
            content = f.read()
        return Response(content, mimetype="text/plain"), 200
    except Exception as e:
        return str(e), 500

if __name__ == "__main__":
    # Optional: Open an ngrok tunnel (for external access)
    public_url = ngrok.connect(5000)
    print("Public URL:", public_url)
    app.run(host="0.0.0.0", port=5000)
