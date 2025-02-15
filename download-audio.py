import requests

audio_url = "https://www.youtube.com/watch?v=synUtcWffF4"
audio_path = "/workspaces/dataworks-project/data/audio.mp3"

response = requests.get(audio_url)

if response.status_code == 200:
    with open(audio_path, "wb") as f:
        f.write(response.content)
    print(f"✅ Audio file downloaded as {audio_path}")
else:
    print("❌ Failed to download audio")
