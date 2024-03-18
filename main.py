import requests
API_TOKEN = "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"
API_URL = "https://api-inference.huggingface.co/models/jinhybr/OCR-Donut-CORD"
headers = {"Authorization": f"Bearer {API_TOKEN}"}

def query(filename):
    with open(filename, "rb") as f:
        data = f.read()
    response = requests.post(API_URL, headers=headers, data=data)
    return response.json()

output = query("Cats.jpg")
print(output)
