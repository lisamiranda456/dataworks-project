import requests

image_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQoFRQjM-wM_nXMA03AGDXgJK3VeX7vtD3ctA&s"
image_path = "/workspaces/dataworks-project/data/input.jpg"

response = requests.get(image_url)

if response.status_code == 200:
    with open(image_path, "wb") as f:
        f.write(response.content)
    print(f"✅ Image downloaded as {image_path}")
else:
    print("❌ Failed to download image")
